from __future__ import annotations

import csv
import io
import json
import logging
from pathlib import Path
from zipfile import ZipFile

from ..config import RunConfig, serialize_path
from ..contracts import IngestManifest, ValidationManifest

logger = logging.getLogger(__name__)

REQUIRED_CSV_COLUMNS = [
    "法令種別",
    "法令番号",
    "法令名",
    "法令名読み",
    "旧法令名",
    "公布日",
    "改正法令名",
    "改正法令番号",
    "改正法令公布日",
    "施行日",
    "施行日備考",
    "法令ID",
    "本文URL",
    "未施行",
]


def _read_csv_header_from_zip(zip_path: Path, csv_entry: str) -> list[str]:
    with ZipFile(zip_path, "r") as zf, zf.open(csv_entry, "r") as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8", newline="")
        reader = csv.reader(text)
        try:
            raw_header = next(reader)
            return [c.lstrip("\ufeff").strip() for c in raw_header]
        except StopIteration as exc:
            raise ValueError(f"csv is empty: {csv_entry}") from exc


def validate_input(
    config: RunConfig, ingest_manifest: IngestManifest
) -> ValidationManifest:
    logger.info("Starting validation...")
    logger.debug(f"Reading CSV header from: {ingest_manifest.csv_entry}")
    header = _read_csv_header_from_zip(config.input_zip, ingest_manifest.csv_entry)
    missing = [col for col in REQUIRED_CSV_COLUMNS if col not in header]
    contract_ok = len(missing) == 0 and len(header) == len(REQUIRED_CSV_COLUMNS)

    xsd_exists = config.xsd_path.exists()
    logger.debug(f"XSD path: {config.xsd_path}, exists={xsd_exists}")

    if not xsd_exists:
        logger.error(f"XSD not found: {config.xsd_path}")
        raise FileNotFoundError(f"xsd not found: {config.xsd_path}")
    if not contract_ok:
        logger.error(
            f"CSV contract validation failed: columns={len(header)}, missing={missing}"
        )
        raise ValueError(
            f"csv contract validation failed: columns={len(header)} missing={missing}"
        )

    logger.info(
        f"Validation complete: CSV columns={len(header)}, contract_ok={contract_ok}"
    )
    return ValidationManifest(
        run_id=ingest_manifest.run_id,
        xsd_path=serialize_path(config.xsd_path),
        xsd_exists=xsd_exists,
        csv_entry=ingest_manifest.csv_entry,
        csv_column_count=len(header),
        csv_header=header,
        missing_required_columns=missing,
        csv_contract_ok=contract_ok,
    )


def write_validation_manifest(config: RunConfig, manifest: ValidationManifest) -> Path:
    out_dir = config.output_root / manifest.run_id / "stages" / "02_validate"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "manifest.json"
    with out_file.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest.to_dict(), f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")

    return out_file
