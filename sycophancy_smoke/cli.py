from __future__ import annotations

import argparse
from pathlib import Path

from .parser import TranscriptParseError
from .render import render_comparison, render_report
from .scoring import score_transcript


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sycophancy_smoke_test.py",
        description=(
            "Score local chat transcripts for lightweight sycophancy signals such as "
            "over-agreement, unsupported certainty, and missing pushback."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    score_parser = subparsers.add_parser(
        "score",
        help="Score a single transcript file.",
        description=(
            "Transcript format: one message per line as '<speaker>: <text>'. "
            "Use indented continuation lines for multi-line messages. "
            "Supported speakers: system, user, assistant."
        ),
    )
    score_parser.add_argument("transcript", type=Path, help="Path to a local transcript file.")
    score_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    score_parser.set_defaults(handler=_handle_score)

    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare two transcript files.",
        description="Compare overall and per-signal scores for two local transcripts.",
    )
    compare_parser.add_argument("left", type=Path, help="Reference transcript path.")
    compare_parser.add_argument("right", type=Path, help="Candidate transcript path.")
    compare_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    compare_parser.set_defaults(handler=_handle_compare)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except (FileNotFoundError, TranscriptParseError) as exc:
        parser.exit(status=2, message=f"error: {exc}\n")


def _handle_score(args: argparse.Namespace) -> int:
    report = score_transcript(args.transcript)
    print(render_report(report, args.format))
    return 0


def _handle_compare(args: argparse.Namespace) -> int:
    left_report = score_transcript(args.left)
    right_report = score_transcript(args.right)
    print(render_comparison(left_report, right_report, args.format))
    return 0
