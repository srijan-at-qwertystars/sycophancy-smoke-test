# Sycophancy Smoke Test

Offline CLI for scoring plain-text chat transcripts for lightweight sycophancy signals: over-agreement, missing pushback, unsupported certainty, and lack of evidence-seeking.

## Requirements

- Python 3.11+ (Python 3.12 works too)
- No third-party packages

## Install

From this goal directory:

```bash
python3 -m venv .venv
. .venv/bin/activate
```

No additional dependencies are required. You can also run the script directly with your system `python3`.

## Transcript format

Write one message per line:

```text
system: You are a helpful assistant.
user: Am I right to assume this will definitely work?
assistant: What evidence do you have so far?
```

- Supported speakers: `system`, `user`, `assistant`
- Use indented continuation lines for multi-line messages
- Blank lines and `#` comments are ignored

## Usage

Show help:

```bash
python3 sycophancy_smoke_test.py --help
```

Score one transcript:

```bash
python3 sycophancy_smoke_test.py score fixtures/bad-chat.txt --format json
```

Compare two transcripts:

```bash
python3 sycophancy_smoke_test.py compare fixtures/good-chat.txt fixtures/bad-chat.txt --format json
```

The comparison JSON includes:

- `delta`: overall score difference (`right - left`)
- `signal_deltas`: per-signal score differences
- `higher_overall_score_path`: the transcript with the higher overall score

## Tests

Run the goal-local test suite with:

```bash
python3 -m unittest discover -s tests -v
```

## Fixtures

- `fixtures/good-chat.txt`: a healthier assistant that asks for evidence and pushes back
- `fixtures/bad-chat.txt`: a clearly sycophantic assistant that validates strong claims without evidence
