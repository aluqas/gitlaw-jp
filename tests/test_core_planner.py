from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.core.models import (
    LawVersion,
    branch_name,
    branch_ref_name,
    revision_to_effective_date_hint,
)
from src.core.planner import (
    build_amendment_events,
    build_commit_graph_plan,
    build_enforcement_units,
    build_law_timelines,
    write_graph_plan,
)
from src.core.strategies import (
    AmendmentLawNumGroupingStrategy,
    AsOfEnforcementProjectionStrategy,
    DefaultDateResolutionStrategy,
)


def _law_version(
    *,
    law_id: str,
    revision_id: str,
    amendment_law_num: str,
    amendment_law_name: str,
    amendment_promulgation_date: str,
    effective_date: str,
    is_marked_unenforced: bool = False,
) -> LawVersion:
    return LawVersion(
        law_id=law_id,
        revision_id=revision_id,
        law_type="法律",
        law_num="法律第1号",
        law_name="Test Law",
        promulgation_date="2024-01-01",
        amendment_law_name=amendment_law_name,
        amendment_law_num=amendment_law_num,
        amendment_promulgation_date=amendment_promulgation_date,
        effective_date=effective_date,
        effective_note="",
        is_marked_unenforced=is_marked_unenforced,
        source_body_url="https://example.invalid",
        xml_entry=f"{law_id}_{revision_id}/{law_id}_{revision_id}.xml",
    )


class PlannerV3Tests(unittest.TestCase):
    def test_revision_effective_date_hint_and_branch_helpers(self) -> None:
        self.assertEqual(
            revision_to_effective_date_hint("20251001_505AC0000000053"),
            "2025-10-01",
        )
        self.assertIsNone(revision_to_effective_date_hint("invalid"))
        self.assertEqual(
            branch_name("promulgation", "20260331"), "promulgations/20260331"
        )
        self.assertEqual(
            branch_ref_name("enforcement", "20260331"),
            "refs/heads/enforcements/20260331",
        )

    def test_default_date_resolution_strategy(self) -> None:
        strategy = DefaultDateResolutionStrategy()
        self.assertEqual(strategy.normalize_date("2024/6/1"), "2024-06-01")
        self.assertEqual(strategy.normalize_date("令和五年六月十四日"), "2023-06-14")

        date, source = strategy.resolve_commit_date(
            amendment_promulgation_date="令和五年六月十四日",
            effective_date="2024-01-01",
            revision_id="20251001_505AC0000000053",
        )
        self.assertEqual(date, "2023-06-14")
        self.assertEqual(source, "amendment_promulgation_date")

    def test_builds_timelines_and_amendment_events(self) -> None:
        versions = [
            _law_version(
                law_id="100AC0000000001",
                revision_id="20270401_506AC0000000033",
                amendment_law_num="令和六年法律第三十三号",
                amendment_law_name="A法等の一部を改正する法律",
                amendment_promulgation_date="2024-05-24",
                effective_date="2027-04-01",
            ),
            _law_version(
                law_id="100AC0000000001",
                revision_id="20260401_506AC0000000033",
                amendment_law_num="令和六年法律第三十三号",
                amendment_law_name="A法等の一部を改正する法律",
                amendment_promulgation_date="2024-05-24",
                effective_date="2026-04-01",
            ),
            _law_version(
                law_id="200AC0000000002",
                revision_id="20240101_505AC0000000053",
                amendment_law_num="令和五年法律第五十三号",
                amendment_law_name="B法等の一部を改正する法律",
                amendment_promulgation_date="2023-06-14",
                effective_date="2028-06-13",
            ),
        ]
        grouping = AmendmentLawNumGroupingStrategy()

        timelines = build_law_timelines(versions)
        self.assertEqual(len(timelines), 2)
        self.assertEqual(
            timelines[0].versions[0].revision_id, "20260401_506AC0000000033"
        )

        events = build_amendment_events(versions, grouping=grouping)
        self.assertEqual(len(events), 2)
        self.assertEqual(
            events[0].amendment_id, "promulgation:令和五年法律第五十三号:2023-06-14"
        )

    def test_builds_enforcement_units_with_as_of_filter(self) -> None:
        timelines = build_law_timelines(
            [
                _law_version(
                    law_id="100AC0000000001",
                    revision_id="20260401_506AC0000000033",
                    amendment_law_num="令和六年法律第三十三号",
                    amendment_law_name="A法等の一部を改正する法律",
                    amendment_promulgation_date="2024-05-24",
                    effective_date="2026-04-01",
                ),
                _law_version(
                    law_id="100AC0000000001",
                    revision_id="20270401_506AC0000000033",
                    amendment_law_num="令和六年法律第三十三号",
                    amendment_law_name="A法等の一部を改正する法律",
                    amendment_promulgation_date="2024-05-24",
                    effective_date="2027-04-01",
                ),
                _law_version(
                    law_id="200AC0000000002",
                    revision_id="20260401_506AC0000000033",
                    amendment_law_num="令和六年法律第三十三号",
                    amendment_law_name="A法等の一部を改正する法律",
                    amendment_promulgation_date="2024-05-24",
                    effective_date="2026-04-01",
                    is_marked_unenforced=True,
                ),
            ]
        )

        units = build_enforcement_units(
            timelines,
            grouping=AmendmentLawNumGroupingStrategy(),
            projection=AsOfEnforcementProjectionStrategy(),
            as_of="2026-12-31",
        )

        self.assertEqual(len(units), 1)
        self.assertEqual(
            units[0].unit_id, "enforcement:100AC0000000001:20260401_506AC0000000033:p1"
        )

    def test_build_commit_graph_plan_creates_pr_style_promulgation_and_linear_enforcement(
        self,
    ) -> None:
        timelines = build_law_timelines(
            [
                _law_version(
                    law_id="100AC0000000001",
                    revision_id="20230614_100AC0000000001",
                    amendment_law_num="令和五年法律第五十三号",
                    amendment_law_name="テスト改正法",
                    amendment_promulgation_date="2023-06-14",
                    effective_date="2023-09-01",
                ),
                _law_version(
                    law_id="100AC0000000001",
                    revision_id="20231001_100AC0000000001",
                    amendment_law_num="令和五年法律第五十三号",
                    amendment_law_name="テスト改正法",
                    amendment_promulgation_date="2023-06-14",
                    effective_date="2023-10-01",
                ),
            ]
        )

        plan = build_commit_graph_plan(
            run_id="run1",
            timelines=timelines,
            target_dir="laws",
            promulgation_branch_prefix="promulgations",
            enforcement_branch_prefix="enforcements",
        )

        prom_commits = [
            c for c in plan.planned_commits if c.projection == "promulgation"
        ]
        enf_commits = [c for c in plan.planned_commits if c.projection == "enforcement"]
        self.assertEqual(len(prom_commits), 3)
        self.assertEqual(len(enf_commits), 2)

        merge_commit = prom_commits[-1]
        self.assertEqual(len(merge_commit.parent_commit_ids), 1)
        self.assertIsNotNone(merge_commit.tree_source_commit_id)
        self.assertIn("Amendment-Id", merge_commit.trailers)
        self.assertTrue(prom_commits[0].files[0].path.endswith("/current.xml"))
        self.assertTrue(prom_commits[0].files[1].path.endswith("/current.json"))
        self.assertTrue(enf_commits[0].files[0].path.endswith("/current.xml"))
        self.assertTrue(enf_commits[0].files[1].path.endswith("/current.json"))

        self.assertEqual(enf_commits[0].parent_commit_ids, [])
        self.assertEqual(enf_commits[1].parent_commit_ids, [enf_commits[0].commit_id])
        self.assertEqual(enf_commits[0].trailers["Projection"], "enforcement")
        self.assertIn("[gitlaw][施行][法律]", enf_commits[0].message)
        self.assertIn("[gitlaw][公布][法律]", merge_commit.message)
        self.assertEqual(
            enf_commits[0].files[0].xml_entry,
            "100AC0000000001_20230614_100AC0000000001/100AC0000000001_20230614_100AC0000000001.xml",
        )

    def test_build_commit_graph_plan_keeps_promulgation_units_when_as_of_filters_enforcement(
        self,
    ) -> None:
        timelines = build_law_timelines(
            [
                _law_version(
                    law_id="100AC0000000001",
                    revision_id="20260401_100AC0000000001",
                    amendment_law_num="令和六年法律第三十三号",
                    amendment_law_name="未来改正法",
                    amendment_promulgation_date="2024-05-24",
                    effective_date="2026-04-01",
                    is_marked_unenforced=True,
                )
            ]
        )

        plan = build_commit_graph_plan(
            run_id="run3",
            timelines=timelines,
            target_dir="laws",
            promulgation_branch_prefix="promulgations",
            enforcement_branch_prefix="enforcements",
            as_of="2025-01-01",
        )

        prom_commits = [
            c for c in plan.planned_commits if c.projection == "promulgation"
        ]
        enf_commits = [c for c in plan.planned_commits if c.projection == "enforcement"]
        self.assertEqual(len(prom_commits), 2)
        self.assertEqual(len(enf_commits), 0)

    def test_write_graph_plan(self) -> None:
        timelines = build_law_timelines(
            [
                _law_version(
                    law_id="100AC0000000001",
                    revision_id="20230614_100AC0000000001",
                    amendment_law_num="令和五年法律第五十三号",
                    amendment_law_name="テスト改正法",
                    amendment_promulgation_date="2023-06-14",
                    effective_date="2023-09-01",
                )
            ]
        )
        plan = build_commit_graph_plan(
            run_id="run2",
            timelines=timelines,
            target_dir="laws",
            promulgation_branch_prefix="promulgations",
            enforcement_branch_prefix="enforcements",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "graph_plan.json"
            write_graph_plan(plan, out_file)
            payload = json.loads(out_file.read_text(encoding="utf-8"))
            self.assertEqual(payload["metadata"]["run_id"], "run2")
            self.assertGreaterEqual(len(payload["planned_commits"]), 2)

    def test_git_max_commits_applies_per_projection(self) -> None:
        timelines = build_law_timelines(
            [
                _law_version(
                    law_id="100AC0000000001",
                    revision_id="20230614_100AC0000000001",
                    amendment_law_num="令和五年法律第五十三号",
                    amendment_law_name="テスト改正法",
                    amendment_promulgation_date="2023-06-14",
                    effective_date="2023-09-01",
                ),
                _law_version(
                    law_id="200AC0000000002",
                    revision_id="20230615_100AC0000000002",
                    amendment_law_num="令和五年法律第五十四号",
                    amendment_law_name="テスト改正法2",
                    amendment_promulgation_date="2023-06-15",
                    effective_date="2023-10-01",
                ),
            ]
        )
        plan = build_commit_graph_plan(
            run_id="run3",
            timelines=timelines,
            target_dir="laws",
            promulgation_branch_prefix="promulgations",
            enforcement_branch_prefix="enforcements",
            max_commits=2,
        )

        prom_commits = [
            c for c in plan.planned_commits if c.projection == "promulgation"
        ]
        enf_commits = [c for c in plan.planned_commits if c.projection == "enforcement"]
        self.assertEqual(len(prom_commits), 2)
        self.assertEqual(len(enf_commits), 2)


if __name__ == "__main__":
    unittest.main()
