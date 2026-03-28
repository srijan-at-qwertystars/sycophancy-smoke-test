from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class Turn:
    speaker: str
    text: str
    line_start: int
    line_end: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SignalFlag:
    kind: str
    score: float
    evidence: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class TurnScore:
    turn_index: int
    speaker: str
    text: str
    flags: list[SignalFlag] = field(default_factory=list)
    total_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["flags"] = [flag.to_dict() for flag in self.flags]
        return payload


@dataclass(slots=True)
class TranscriptReport:
    path: str
    turn_count: int
    assistant_turn_count: int
    overall_score: float
    signal_averages: dict[str, float]
    flagged_turns: list[TurnScore]

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "turn_count": self.turn_count,
            "assistant_turn_count": self.assistant_turn_count,
            "overall_score": self.overall_score,
            "signal_averages": self.signal_averages,
            "flagged_turns": [turn.to_dict() for turn in self.flagged_turns],
        }
