from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

CommitLayer = Literal["promulgation", "enforcement"]
ProjectionName = Literal["promulgation", "enforcement"]
PlannedFileKind = Literal["inline_text", "zip_xml"]

PROMULGATION_BRANCH_PREFIX = "promulgations"
ENFORCEMENT_BRANCH_PREFIX = "enforcements"


def revision_to_effective_date_hint(revision_id: str) -> str | None:
    """Extract YYYY-MM-DD hint from revision id prefix."""
    prefix = revision_id.split("_", 1)[0]
    if len(prefix) != 8 or not prefix.isdigit():
        return None
    return f"{prefix[:4]}-{prefix[4:6]}-{prefix[6:8]}"


def branch_name(layer: CommitLayer, timing_id: str) -> str:
    if layer == "promulgation":
        return f"{PROMULGATION_BRANCH_PREFIX}/{timing_id}"
    return f"{ENFORCEMENT_BRANCH_PREFIX}/{timing_id}"


def branch_ref_name(layer: CommitLayer, timing_id: str) -> str:
    return f"refs/heads/{branch_name(layer, timing_id)}"


def law_storage_dir(law_id: str) -> str:
    prefix = law_id[:3] if law_id else "unknown"
    return f"{prefix}/{law_id}"


@dataclass(frozen=True)
class LawRevisionRef:
    law_id: str
    revision_id: str
    xml_entry: str = ""

    @property
    def effective_date_hint(self) -> str | None:
        return revision_to_effective_date_hint(self.revision_id)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class LawVersion:
    law_id: str
    revision_id: str
    law_type: str
    law_num: str
    law_name: str
    promulgation_date: str
    amendment_law_name: str
    amendment_law_num: str
    amendment_promulgation_date: str
    effective_date: str
    effective_note: str
    is_marked_unenforced: bool
    source_body_url: str
    xml_entry: str = ""
    xml_sha256: str = ""
    xml_mvp: dict[str, object] | None = None

    @property
    def effective_date_hint(self) -> str | None:
        return revision_to_effective_date_hint(self.revision_id)

    @property
    def revision_ref(self) -> LawRevisionRef:
        return LawRevisionRef(
            law_id=self.law_id,
            revision_id=self.revision_id,
            xml_entry=self.xml_entry,
        )

    def to_dict(self) -> dict:
        payload = {
            "law_id": self.law_id,
            "revision_id": self.revision_id,
            "law_type": self.law_type,
            "law_num": self.law_num,
            "law_name": self.law_name,
            "promulgation_date": self.promulgation_date,
            "amendment_law_name": self.amendment_law_name,
            "amendment_law_num": self.amendment_law_num,
            "amendment_promulgation_date": self.amendment_promulgation_date,
            "effective_date": self.effective_date,
            "effective_note": self.effective_note,
            "is_marked_unenforced": self.is_marked_unenforced,
            "source_body_url": self.source_body_url,
            "xml_entry": self.xml_entry,
            "xml_sha256": self.xml_sha256,
        }
        if self.xml_mvp is not None:
            payload["xml_mvp"] = self.xml_mvp
        return payload


@dataclass(frozen=True)
class LawTimeline:
    law_id: str
    versions: list[LawVersion]

    def to_dict(self) -> dict:
        return {
            "law_id": self.law_id,
            "versions": [version.to_dict() for version in self.versions],
        }


@dataclass(frozen=True)
class AmendmentEvent:
    amendment_id: str
    group_key: str
    amendment_law_num: str
    amendment_law_name: str
    amendment_promulgation_date: str
    affected_law_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["affected_law_ids"] = list(self.affected_law_ids)
        return payload


@dataclass(frozen=True)
class EnforcementUnit:
    unit_id: str
    law_revision: LawRevisionRef
    law_type: str
    law_name: str
    law_num: str
    amendment_event: AmendmentEvent
    effective_date: str
    effective_note: str
    phase_index: int
    is_marked_unenforced: bool

    def to_dict(self) -> dict:
        return {
            "unit_id": self.unit_id,
            "law_revision": self.law_revision.to_dict(),
            "law_type": self.law_type,
            "law_name": self.law_name,
            "law_num": self.law_num,
            "amendment_event": self.amendment_event.to_dict(),
            "effective_date": self.effective_date,
            "effective_note": self.effective_note,
            "phase_index": self.phase_index,
            "is_marked_unenforced": self.is_marked_unenforced,
        }


@dataclass(frozen=True)
class PlannedFile:
    path: str
    kind: PlannedFileKind
    content: str | None = None
    law_id: str | None = None
    revision_id: str | None = None
    xml_entry: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class PlannedCommit:
    commit_id: str
    projection: ProjectionName
    parent_commit_ids: list[str]
    files: list[PlannedFile]
    message: str
    trailers: dict[str, str]
    author_date: str
    target_ref: str | None = None
    tree_source_commit_id: str | None = None

    def to_dict(self) -> dict:
        return {
            "commit_id": self.commit_id,
            "projection": self.projection,
            "parent_commit_ids": list(self.parent_commit_ids),
            "files": [planned_file.to_dict() for planned_file in self.files],
            "message": self.message,
            "trailers": dict(self.trailers),
            "author_date": self.author_date,
            "target_ref": self.target_ref,
            "tree_source_commit_id": self.tree_source_commit_id,
        }


@dataclass(frozen=True)
class RefUpdate:
    ref_name: str
    commit_id: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CommitGraphPlan:
    planned_commits: list[PlannedCommit]
    ref_updates: list[RefUpdate]
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "planned_commits": [commit.to_dict() for commit in self.planned_commits],
            "ref_updates": [ref_update.to_dict() for ref_update in self.ref_updates],
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class GraphSinkResult:
    commit_count: int
    promulgation_commit_count: int
    enforcement_commit_count: int
    updated_refs: list[str]

    def to_dict(self) -> dict:
        return asdict(self)
