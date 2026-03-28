from __future__ import annotations

from pathlib import Path

from .models import Turn

ALLOWED_SPEAKERS = {"system", "user", "assistant"}


class TranscriptParseError(ValueError):
    """Raised when a transcript file does not match the local format."""


def parse_transcript_file(path: str | Path) -> list[Turn]:
    return parse_transcript_text(Path(path).read_text(encoding="utf-8"))


def parse_transcript_text(text: str) -> list[Turn]:
    turns: list[Turn] = []
    current_speaker: str | None = None
    current_lines: list[str] = []
    start_line = 0
    end_line = 0

    def flush() -> None:
        nonlocal current_speaker, current_lines, start_line, end_line
        if current_speaker is None:
            return
        body = "\n".join(current_lines).strip()
        if not body:
            raise TranscriptParseError(
                f"Empty message for speaker '{current_speaker}' near line {start_line}."
            )
        turns.append(
            Turn(
                speaker=current_speaker,
                text=body,
                line_start=start_line,
                line_end=end_line,
            )
        )
        current_speaker = None
        current_lines = []
        start_line = 0
        end_line = 0

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if raw_line[0].isspace():
            if current_speaker is None:
                raise TranscriptParseError(
                    f"Continuation line without a message header at line {line_number}."
                )
            current_lines.append(stripped)
            end_line = line_number
            continue

        if ":" not in raw_line:
            raise TranscriptParseError(
                f"Expected '<speaker>: <text>' at line {line_number}, got: {raw_line!r}"
            )

        speaker_raw, content = raw_line.split(":", 1)
        speaker = speaker_raw.strip().lower()
        if speaker not in ALLOWED_SPEAKERS:
            raise TranscriptParseError(
                f"Unsupported speaker '{speaker_raw}' at line {line_number}. "
                f"Expected one of: {', '.join(sorted(ALLOWED_SPEAKERS))}."
            )

        flush()
        current_speaker = speaker
        current_lines = [content.strip()]
        start_line = line_number
        end_line = line_number

    flush()

    if not turns:
        raise TranscriptParseError("Transcript is empty.")

    return turns
