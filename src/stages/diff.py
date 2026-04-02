from __future__ import annotations

import json
import logging
from collections import defaultdict
from pathlib import Path

from ..config import RunConfig
from ..contracts import DiffManifest

logger = logging.getLogger(__name__)

COMPARE_FIELDS = [
    "law_type",
    "law_num",
    "law_name",
    "promulgation_date",
    "amendment_law_name",
    "amendment_law_num",
    "amendment_promulgation_date",
    "effective_date",
    "effective_note",
    "is_marked_unenforced",
]


def _read_snapshot_records(snapshot_jsonl: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    with snapshot_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def _group_by_law_id(
    records: list[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for rec in records:
        grouped[str(rec.get("law_id", ""))].append(rec)

    # Stable ordering: law_id asc, then version_id asc.
    for law_id, versions in grouped.items():
        versions.sort(key=lambda r: str(r.get("version_id", "")))

    return dict(sorted(grouped.items(), key=lambda kv: kv[0]))


def _make_diff_record(
    prev_rec: dict[str, object], next_rec: dict[str, object]
) -> dict[str, object]:
    changed_fields: list[str] = []
    for field in COMPARE_FIELDS:
        if prev_rec.get(field) != next_rec.get(field):
            changed_fields.append(field)

    return {
        "law_id": next_rec.get("law_id", ""),
        "from_version_id": prev_rec.get("version_id", ""),
        "to_version_id": next_rec.get("version_id", ""),
        "from_effective_date": prev_rec.get("effective_date", ""),
        "to_effective_date": next_rec.get("effective_date", ""),
        "changed_field_count": len(changed_fields),
        "changed_fields": changed_fields,
    }


def create_diff_records(
    config: RunConfig, run_id: str, snapshot_jsonl: Path
) -> DiffManifest:
    logger.info("Creating diff records...")
    records = _read_snapshot_records(snapshot_jsonl)
    grouped = _group_by_law_id(records)

    diffs: list[dict[str, object]] = []
    for versions in grouped.values():
        if len(versions) < 2:
            continue
        for i in range(1, len(versions)):
            diffs.append(_make_diff_record(versions[i - 1], versions[i]))

    out_dir = config.output_root / run_id / "stages" / "04_diff"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_jsonl = out_dir / "version_diffs.jsonl"
    with out_jsonl.open("w", encoding="utf-8", newline="\n") as f:
        for rec in diffs:
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True))
            f.write("\n")

    manifest = DiffManifest(
        run_id=run_id,
        source_snapshot_jsonl=str(snapshot_jsonl),
        diff_record_count=len(diffs),
        output_jsonl=str(out_jsonl),
    )

    out_manifest = out_dir / "manifest.json"
    with out_manifest.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest.to_dict(), f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")

    logger.info(f"Diff records created: {len(diffs)} diffs from {len(grouped)} laws")
    return manifest
