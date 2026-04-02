from __future__ import annotations

import csv
import hashlib
import io
import json
import logging
import time
from pathlib import Path
from zipfile import ZipFile

from ..config import RunConfig, serialize_path
from ..contracts import IngestManifest, LawXmlParser, SnapshotManifest
from ..core.models import LawVersion
from ..law_types import normalize_law_type
from ..xml_parser import XsdataLawXmlParser

logger = logging.getLogger(__name__)


def _extract_revision_id(url: str) -> str:
    normalized = url.strip().rstrip("/")
    if not normalized:
        return ""
    return normalized.split("/")[-1]


def _read_csv_rows(zip_path: Path, csv_entry: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with ZipFile(zip_path, "r") as zf, zf.open(csv_entry, "r") as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8", newline="")
        reader = csv.DictReader(text)
        for row in reader:
            normalized_row = {
                (k or "").lstrip("\ufeff").strip(): (v or "").strip()
                for k, v in row.items()
            }
            rows.append(normalized_row)
    return rows


def _filter_rows_by_law_id(
    rows: list[dict[str, str]], allowed_law_ids: tuple[str, ...]
) -> list[dict[str, str]]:
    if not allowed_law_ids:
        return rows
    allowed = {law_id for law_id in allowed_law_ids if law_id}
    return [row for row in rows if row.get("法令ID", "") in allowed]


def _filter_rows_by_law_type(
    rows: list[dict[str, str]], allowed_law_types: tuple[str, ...]
) -> list[dict[str, str]]:
    if not allowed_law_types:
        return rows
    allowed = {
        normalize_law_type(law_type) for law_type in allowed_law_types if law_type
    }
    return [
        row
        for row in rows
        if normalize_law_type(row.get("法令種別", ""), row.get("法令番号", ""))
        in allowed
    ]


def _normalize_entries(entries: list[str]) -> list[str]:
    return sorted(entry.replace("\\", "/") for entry in entries)


def _resolve_xml_entry(
    entries: list[str],
    entry_lookup: set[str],
    *,
    csv_entry: str,
    law_id: str,
    revision_id: str,
) -> str:
    if not law_id:
        raise ValueError("law_id is empty")
    if not revision_id:
        raise ValueError(f"revision_id is empty: law_id={law_id}")

    file_name = f"{law_id}_{revision_id}.xml"
    csv_parent = Path(csv_entry).parent.as_posix()

    candidates: list[str] = []
    if csv_parent and csv_parent != ".":
        candidates.append(f"{csv_parent}/{law_id}_{revision_id}/{file_name}")
    candidates.append(f"{law_id}_{revision_id}/{file_name}")
    candidates.append(file_name)

    for candidate in candidates:
        if candidate in entry_lookup:
            return candidate

    fallback = sorted(
        name for name in entries if name == file_name or name.endswith(f"/{file_name}")
    )
    if len(fallback) == 1:
        return fallback[0]
    if len(fallback) > 1:
        raise ValueError(
            f"multiple xml entries matched for {law_id}:{revision_id}: {fallback[:3]}"
        )

    raise FileNotFoundError(f"xml entry not found for {law_id}:{revision_id}")


def _build_xml_mvp(parsed_xml: object) -> dict[str, object]:
    from ..contracts import ParsedLawXml

    if not isinstance(parsed_xml, ParsedLawXml):
        raise TypeError("parsed_xml must be ParsedLawXml")

    first_sentence = (
        parsed_xml.structure[0].sentence_text if parsed_xml.structure else ""
    )
    return {
        "law_meta": parsed_xml.law_meta.to_dict(),
        "flags": {
            "delete": parsed_xml.has_delete,
            "hide": parsed_xml.has_hide,
            "extract": parsed_xml.has_extract,
        },
        "amend": {
            "suppl_provisions": [
                item.to_dict() for item in parsed_xml.suppl_provisions
            ],
        },
        "structure_summary": {
            "sentence_count": len(parsed_xml.structure),
            "first_sentence": first_sentence,
        },
    }


def _to_law_version(
    row: dict[str, str],
    *,
    xml_entry: str,
    xml_sha256: str,
    xml_mvp: dict[str, object] | None,
) -> LawVersion:
    law_id = row.get("法令ID", "")
    body_url = row.get("本文URL", "")
    revision_id = _extract_revision_id(body_url)
    return LawVersion(
        law_id=law_id,
        revision_id=revision_id,
        law_type=row.get("法令種別", ""),
        law_num=row.get("法令番号", ""),
        law_name=row.get("法令名", ""),
        promulgation_date=row.get("公布日", ""),
        amendment_law_name=row.get("改正法令名", ""),
        amendment_law_num=row.get("改正法令番号", ""),
        amendment_promulgation_date=row.get("改正法令公布日", ""),
        effective_date=row.get("施行日", ""),
        effective_note=row.get("施行日備考", ""),
        is_marked_unenforced=row.get("未施行", "") == "○",
        source_body_url=body_url,
        xml_entry=xml_entry,
        xml_sha256=f"sha256:{xml_sha256}",
        xml_mvp=xml_mvp,
    )


def create_normalized_versions(
    config: RunConfig,
    ingest_manifest: IngestManifest,
    law_xml_parser: LawXmlParser | None = None,
) -> SnapshotManifest:
    need_xml_parse = config.snapshot_parse_xml
    parser = (law_xml_parser or XsdataLawXmlParser()) if need_xml_parse else None
    rows = _read_csv_rows(config.input_zip, ingest_manifest.csv_entry)
    rows = _filter_rows_by_law_id(rows, config.law_ids)
    rows = _filter_rows_by_law_type(rows, config.law_types)
    records: list[LawVersion] = []
    started_at = time.perf_counter()

    with ZipFile(config.input_zip, "r") as zf:
        entries = _normalize_entries(zf.namelist())
        entry_lookup = set(entries)
        for idx, row in enumerate(rows, start=1):
            law_id = row.get("法令ID", "")
            revision_id = _extract_revision_id(row.get("本文URL", ""))
            xml_entry = _resolve_xml_entry(
                entries,
                entry_lookup,
                csv_entry=ingest_manifest.csv_entry,
                law_id=law_id,
                revision_id=revision_id,
            )
            with zf.open(xml_entry, "r") as raw:
                xml_bytes = raw.read()
                parsed_xml = None
                if parser is not None:
                    parsed_xml = parser.parse(
                        law_id=law_id,
                        version_id=revision_id,
                        xml_bytes=xml_bytes,
                    )

            xml_sha256 = hashlib.sha256(xml_bytes).hexdigest()
            xml_mvp = _build_xml_mvp(parsed_xml) if parsed_xml is not None else None
            records.append(
                _to_law_version(
                    row,
                    xml_entry=xml_entry,
                    xml_sha256=xml_sha256,
                    xml_mvp=xml_mvp,
                )
            )

            if idx % 500 == 0:
                elapsed = max(time.perf_counter() - started_at, 1e-9)
                logger.debug(
                    "Normalize progress: %s/%s records processed (%.1f rec/s)",
                    idx,
                    len(rows),
                    idx / elapsed,
                )

    records.sort(key=lambda version: (version.law_id, version.revision_id))

    out_dir = (
        config.output_root / ingest_manifest.run_id / "stages" / "03_normalize_versions"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    out_jsonl = out_dir / "law_versions.jsonl"
    with out_jsonl.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False, sort_keys=True))
            f.write("\n")

    manifest = SnapshotManifest(
        dataset_id=ingest_manifest.dataset_id,
        run_id=ingest_manifest.run_id,
        source_csv_entry=ingest_manifest.csv_entry,
        record_count=len(records),
        output_jsonl=serialize_path(out_jsonl),
        xml_parsed_count=len(records) if need_xml_parse else 0,
        xml_parse_policy="strict_fail_fast",
    )

    out_manifest = out_dir / "manifest.json"
    with out_manifest.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest.to_dict(), f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")

    return manifest
