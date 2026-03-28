from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


GOAL_DIR = Path(__file__).resolve().parents[1]
CLI = GOAL_DIR / "sycophancy_smoke_test.py"
FIXTURES_DIR = GOAL_DIR / "fixtures"


class SycophancySmokeCliTests(unittest.TestCase):
    maxDiff = None

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=GOAL_DIR,
            text=True,
            capture_output=True,
            check=True,
        )

    def test_help_exits_successfully(self) -> None:
        result = self.run_cli("--help")
        self.assertIn("score", result.stdout)
        self.assertIn("compare", result.stdout)

    def test_score_bad_fixture_json_has_flagged_turns(self) -> None:
        result = self.run_cli(
            "score",
            str(FIXTURES_DIR / "bad-chat.txt"),
            "--format",
            "json",
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["path"], str(FIXTURES_DIR / "bad-chat.txt"))
        self.assertGreater(payload["overall_score"], 0)
        self.assertTrue(payload["flagged_turns"])

    def test_compare_reports_bad_fixture_as_higher_scoring(self) -> None:
        result = self.run_cli(
            "compare",
            str(FIXTURES_DIR / "good-chat.txt"),
            str(FIXTURES_DIR / "bad-chat.txt"),
            "--format",
            "json",
        )
        payload = json.loads(result.stdout)
        self.assertGreater(payload["delta"], 0)
        self.assertGreater(
            payload["right"]["overall_score"],
            payload["left"]["overall_score"],
        )
        self.assertEqual(
            payload["higher_overall_score_path"],
            str(FIXTURES_DIR / "bad-chat.txt"),
        )
        self.assertIn("affirmation_bias", payload["signal_deltas"])


if __name__ == "__main__":
    unittest.main()
