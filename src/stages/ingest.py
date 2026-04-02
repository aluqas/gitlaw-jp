from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from zipfile import ZipFile

from ..config import RunConfig, serialize_path
from ..contracts import IngestManifest

logger = logging.getLogger(__name__)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _normalize_entries(entries: list[str]) -> list[str]:
    return sorted(e.replace("\\", "/") for e in entries)


def ingest_zip(config: RunConfig) -> IngestManifest:
    logger.info(f"Reading input ZIP: {config.input_zip}")
    zip_path = config.input_zip
    if not zip_path.exists():
        logger.error(f"Input ZIP not found: {zip_path}")
        raise FileNotFoundError(f"input zip not found: {zip_path}")

    logger.debug("Computing SHA256 hash of input ZIP...")
    input_sha = _sha256_file(zip_path)
    run_id = input_sha[:12]
    logger.debug(f"Input SHA256: {input_sha}, Run ID: {run_id}")

    logger.debug("Extracting file list from ZIP...")
    with ZipFile(zip_path, "r") as zf:
        names = _normalize_entries(zf.namelist())
    logger.debug(f"Total entries in ZIP: {len(names)}")

    csv_candidates = [n for n in names if n.endswith("all_law_list.csv")]
    if len(csv_candidates) != 1:
        logger.error(f"Expected 1 all_law_list.csv, got {len(csv_candidates)}")
        raise ValueError(
            f"expected one all_law_list.csv in zip, got {len(csv_candidates)}"
        )

    xml_entries = [n for n in names if n.endswith(".xml")]
    if not xml_entries:
        logger.error("No XML files found in input ZIP")
        raise ValueError("no xml files found in input zip")

    logger.info(f"Ingest complete: run_id={run_id}, XML entries={len(xml_entries)}")
    return IngestManifest(
        run_id=run_id,
        input_zip=serialize_path(zip_path),
        input_sha256=input_sha,
        csv_entry=csv_candidates[0],
        xml_entry_count=len(xml_entries),
        xml_entries_sample=xml_entries[:10],
    )


def write_ingest_manifest(config: RunConfig, manifest: IngestManifest) -> Path:
    out_dir = config.output_root / manifest.run_id / "stages" / "01_ingest"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "manifest.json"
    with out_file.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest.to_dict(), f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")

    return out_file
