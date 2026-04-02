from __future__ import annotations

import json
from pathlib import Path

from ..config import RunConfig, serialize_path
from ..contracts import TimelineManifest
from ..core.planner import build_law_timelines, law_versions_from_jsonl


def create_timelines(
    config: RunConfig,
    *,
    run_id: str,
    versions_jsonl: Path,
) -> TimelineManifest:
    law_versions = law_versions_from_jsonl(versions_jsonl)
    timelines = build_law_timelines(law_versions)

    out_dir = config.output_root / run_id / "stages" / "04_build_timelines"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_jsonl = out_dir / "law_timelines.jsonl"
    with out_jsonl.open("w", encoding="utf-8", newline="\n") as f:
        for timeline in timelines:
            f.write(json.dumps(timeline.to_dict(), ensure_ascii=False, sort_keys=True))
            f.write("\n")

    manifest = TimelineManifest(
        run_id=run_id,
        source_versions_jsonl=serialize_path(versions_jsonl),
        timeline_count=len(timelines),
        output_jsonl=serialize_path(out_jsonl),
    )
    with (out_dir / "manifest.json").open("w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest.to_dict(), f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")

    return manifest
