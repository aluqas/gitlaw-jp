from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class IngestManifest:
    run_id: str
    input_zip: str
    input_sha256: str
    csv_entry: str
    xml_entry_count: int
    xml_entries_sample: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ValidationManifest:
    run_id: str
    xsd_path: str
    xsd_exists: bool
    csv_entry: str
    csv_column_count: int
    csv_header: list[str]
    missing_required_columns: list[str]
    csv_contract_ok: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class SnapshotManifest:
    run_id: str
    source_csv_entry: str
    record_count: int
    output_jsonl: str
    xml_parsed_count: int | None = None
    xml_parse_policy: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class TimelineManifest:
    run_id: str
    source_versions_jsonl: str
    timeline_count: int
    output_jsonl: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class GraphPlanManifest:
    run_id: str
    source_timelines_jsonl: str
    planned_commit_count: int
    ref_update_count: int
    output_json: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class DiffManifest:
    run_id: str
    source_snapshot_jsonl: str
    diff_record_count: int
    output_jsonl: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class PipelineResult:
    run_id: str
    manifest_path: Path


@dataclass(frozen=True)
class ApplyResult:
    run_id: str
    manifest_path: Path


@dataclass(frozen=True)
class XmlLawMeta:
    law_num: str
    era: str
    year: str
    num: str
    law_type: str
    lang: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class XmlStructureItem:
    article_num: str
    paragraph_num: str
    sentence_text: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class XmlSupplProvision:
    suppl_type: str
    amend_law_num: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ParsedLawXml:
    law_meta: XmlLawMeta
    structure: list[XmlStructureItem]
    has_delete: bool
    has_hide: bool
    has_extract: bool
    suppl_provisions: list[XmlSupplProvision]

    def to_dict(self) -> dict:
        return {
            "law_meta": self.law_meta.to_dict(),
            "structure": [item.to_dict() for item in self.structure],
            "has_delete": self.has_delete,
            "has_hide": self.has_hide,
            "has_extract": self.has_extract,
            "suppl_provisions": [item.to_dict() for item in self.suppl_provisions],
        }


class LawXmlParser(Protocol):
    """Parses a law XML payload into a typed intermediate model."""

    def parse(
        self, *, law_id: str, version_id: str, xml_bytes: bytes
    ) -> ParsedLawXml: ...
