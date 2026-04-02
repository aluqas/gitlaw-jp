from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from src.cli import build_parser, main
from src.contracts import ApplyResult, PipelineResult


class CliArchitectureTests(unittest.TestCase):
    def test_parser_reads_branch_prefix_options(self) -> None:
        parser = build_parser()
        args = parser.parse_args(
            [
                "full",
                "--input-zip",
                "payload.zip",
                "--promulgation-branch-prefix",
                "pub",
                "--enforcement-branch-prefix",
                "enf",
            ]
        )

        self.assertEqual(args.branch_model, "dual")
        self.assertEqual(args.promulgation_branch_prefix, "pub")
        self.assertEqual(args.enforcement_branch_prefix, "enf")

    def test_main_dispatches_pipeline_runner(self) -> None:
        with (
            patch("src.cli.configure_logging"),
            patch("src.cli.run_full") as run_full,
            patch(
                "sys.argv",
                ["gitlaw-ja", "full", "--input-zip", "payload.zip"],
            ),
        ):
            run_full.return_value = PipelineResult(
                run_id="run-v2",
                manifest_path=Path("runs/run-v2/manifest.json"),
            )

            exit_code = main()

            self.assertEqual(exit_code, 0)
            run_full.assert_called_once()

    def test_main_passes_branch_prefixes_to_config(self) -> None:
        with (
            patch("src.cli.configure_logging"),
            patch("src.cli.run_full") as run_full,
            patch(
                "sys.argv",
                [
                    "gitlaw-ja",
                    "full",
                    "--input-zip",
                    "payload.zip",
                    "--promulgation-branch-prefix",
                    "promulgations",
                    "--enforcement-branch-prefix",
                    "enforcements",
                ],
            ),
        ):
            run_full.return_value = PipelineResult(
                run_id="run-v2",
                manifest_path=Path("runs/run-v2/manifest.json"),
            )

            main()

            called_conf = run_full.call_args.args[0]
            self.assertEqual(called_conf.promulgation_branch_prefix, "promulgations")
            self.assertEqual(called_conf.enforcement_branch_prefix, "enforcements")

    def test_main_dispatches_apply(self) -> None:
        with (
            patch("src.cli.configure_logging"),
            patch("src.cli.run_apply") as run_apply,
            patch(
                "sys.argv",
                ["gitlaw-ja", "apply", "--run-manifest", "runs/x/manifest.json"],
            ),
        ):
            run_apply.return_value = ApplyResult(
                run_id="run-v2",
                manifest_path=Path("runs/x/manifest.json"),
            )

            exit_code = main()

            self.assertEqual(exit_code, 0)
            run_apply.assert_called_once()


if __name__ == "__main__":
    unittest.main()
