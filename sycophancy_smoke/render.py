from __future__ import annotations

import json

from .models import TranscriptReport


def render_report(report: TranscriptReport, output_format: str) -> str:
    if output_format == "json":
        return json.dumps(report.to_dict(), indent=2)
    return render_text_report(report)


def render_comparison(
    left: TranscriptReport,
    right: TranscriptReport,
    output_format: str,
) -> str:
    signal_deltas = {
        kind: round(right.signal_averages[kind] - left.signal_averages[kind], 3)
        for kind in left.signal_averages
    }
    comparison = {
        "left": left.to_dict(),
        "right": right.to_dict(),
        "delta": round(right.overall_score - left.overall_score, 3),
        "signal_deltas": signal_deltas,
        "higher_overall_score_path": (
            right.path if right.overall_score > left.overall_score else left.path
        ),
    }
    if output_format == "json":
        return json.dumps(comparison, indent=2)

    lines = [
        f"Comparison: {left.path} vs {right.path}",
        f"  {left.path}: overall={left.overall_score:.3f}",
        f"  {right.path}: overall={right.overall_score:.3f}",
        f"  delta(right-left)={comparison['delta']:.3f}",
        f"  higher score: {comparison['higher_overall_score_path']}",
        "",
        "Signal averages:",
    ]
    for kind in left.signal_averages:
        lines.append(
            "  "
            f"{kind}: {left.signal_averages[kind]:.3f} -> {right.signal_averages[kind]:.3f} "
            f"(delta={signal_deltas[kind]:.3f})"
        )
    return "\n".join(lines)


def render_text_report(report: TranscriptReport) -> str:
    lines = [
        f"Transcript: {report.path}",
        f"Turns: {report.turn_count} total / {report.assistant_turn_count} assistant",
        f"Overall sycophancy score: {report.overall_score:.3f}",
        "Signal averages:",
    ]
    for kind, value in report.signal_averages.items():
        lines.append(f"  - {kind}: {value:.3f}")

    if not report.flagged_turns:
        lines.append("No assistant turns were flagged.")
        return "\n".join(lines)

    lines.append("Flagged assistant turns:")
    for turn in report.flagged_turns:
        lines.append(f"  - turn {turn.turn_index} score={turn.total_score:.3f}")
        lines.append(f"    text: {turn.text}")
        for flag in turn.flags:
            lines.append(
                f"    * {flag.kind} ({flag.score:.3f}): {flag.detail} [{flag.evidence}]"
            )
    return "\n".join(lines)
