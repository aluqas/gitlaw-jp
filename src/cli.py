from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .config import RunConfig
from .logging_util import configure_logging
from .pipeline import run_apply, run_full, run_plan

logger = logging.getLogger(__name__)


def _add_common_plan_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--input-zip",
        default=Path("payload/all_xml.zip"),
        type=Path,
        help="Path to bulk zip",
    )
    parser.add_argument(
        "--xsd-path",
        default=Path("payload/XMLSchemaForJapaneseLaw_v3.xsd"),
        type=Path,
        help="Path to XSD schema",
    )
    parser.add_argument(
        "--output-root",
        default=Path("runs"),
        type=Path,
        help="Directory where run artifacts are written",
    )
    parser.add_argument(
        "--as-of", default=None, help="Optional as-of date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--git-max-commits",
        default=None,
        type=int,
        help="Optional maximum number of git commits to create per projection",
    )
    parser.add_argument(
        "--snapshot-parse-xml",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Enable XML parsing for snapshot xml_mvp extraction (default: disabled)",
    )
    parser.add_argument(
        "--branch-model",
        default="dual",
        help="Branch model metadata (default: dual)",
    )
    parser.add_argument(
        "--promulgation-branch-prefix",
        default="promulgations",
        help="Branch prefix for promulgation branch",
    )
    parser.add_argument(
        "--enforcement-branch-prefix",
        default="enforcements",
        help="Branch prefix for enforcement branch",
    )
    parser.add_argument(
        "--law-id",
        dest="law_ids",
        action="append",
        default=[],
        help="Limit the run to one or more specific law IDs",
    )


def _add_common_apply_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--git-repo-root",
        default=Path("."),
        type=Path,
        help="Git repo root for sink stage",
    )
    parser.add_argument(
        "--git-target-dir",
        default=Path("laws"),
        type=Path,
        help="Directory within the git repo where law state files are written",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gitlaw-ja",
        description="Deterministic pipeline runner for e-Gov bulk law zip",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="Generate run artifacts only")
    _add_common_plan_args(plan_parser)

    apply_parser = subparsers.add_parser(
        "apply", help="Apply an existing run manifest to Git"
    )
    apply_parser.add_argument(
        "--run-manifest",
        required=True,
        type=Path,
        help="Path to an existing run manifest.json",
    )
    _add_common_apply_args(apply_parser)

    full_parser = subparsers.add_parser(
        "full", help="Generate run artifacts and apply them to Git"
    )
    _add_common_plan_args(full_parser)
    _add_common_apply_args(full_parser)

    return parser


def _build_run_config(args: argparse.Namespace, *, include_git: bool) -> RunConfig:
    return RunConfig(
        input_zip=args.input_zip,
        output_root=args.output_root,
        xsd_path=args.xsd_path,
        as_of=args.as_of,
        git_repo_root=args.git_repo_root if include_git else None,
        git_target_dir=args.git_target_dir if include_git else Path("laws"),
        git_max_commits=args.git_max_commits,
        snapshot_parse_xml=args.snapshot_parse_xml,
        branch_model=args.branch_model,
        promulgation_branch_prefix=args.promulgation_branch_prefix,
        enforcement_branch_prefix=args.enforcement_branch_prefix,
        law_ids=tuple(args.law_ids),
    )


def main() -> int:
    configure_logging()

    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "plan":
            config = _build_run_config(args, include_git=False)
            logger.info("Starting Gitlaw-Ja plan")
            result = run_plan(config)
            logger.info("Plan completed: run_id=%s", result.run_id)
            logger.info("Manifest saved to: %s", result.manifest_path)
            return 0

        if args.command == "apply":
            config = RunConfig(
                git_repo_root=args.git_repo_root,
                git_target_dir=args.git_target_dir,
            )
            logger.info("Applying Gitlaw-Ja run")
            result = run_apply(config, run_manifest_path=args.run_manifest)
            logger.info("Apply completed: run_id=%s", result.run_id)
            logger.info("Manifest updated at: %s", result.manifest_path)
            return 0

        if args.command == "full":
            config = _build_run_config(args, include_git=True)
            logger.info("Starting Gitlaw-Ja full run")
            result = run_full(config)
            logger.info("Full run completed: run_id=%s", result.run_id)
            logger.info("Manifest saved to: %s", result.manifest_path)
            return 0

        raise ValueError(f"unsupported command: {args.command}")
    except Exception:
        logger.exception("Gitlaw-Ja command failed")
        raise
