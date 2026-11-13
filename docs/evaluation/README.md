# Evaluation

How well the assistant works and where it fails. Results and failure analysis: [RESULTS.md](RESULTS.md).

These are historical model results, not a fresh measurement of the current code. [PROVENANCE.md](PROVENANCE.md) maps the original private evaluation SHA to an identical public backend snapshot and lists subsequent changes, including the privacy fix. The saved predictions and PDF remain historical evidence.

## What is here

| Path | What it is |
|---|---|
| `RESULTS.md` | The written evaluation: measures, how the sets were built, results by category, 14 failure cases, next steps |
| `PROVENANCE.md`, `baseline-code.json` | Public baseline mapping, per-file source hashes and post-evaluation changes |
| `results/mail_summary.md` | Triage and deadline numbers for every run side by side |
| `results/mail_<set>_run<n>.report.md` | One run in full: tables, confusion matrices and every single error |
| `results/mail_<set>_run<n>.predictions.json` | Raw output of that run (labels, model candidates, tasks, stored text) |
| `results/safety.md`, `safety_run<n>.json` | Safety red-team: 20 specifications, three runs, worst outcome counts |
| `results/planner.md` | Planner evaluation report |
| `../../data/synthetic/mail_eval_v1/` | The 80 fictional mails, their answer key and the labelling rules |
| `../../src/backend/evaluation/` | `mail_eval.py`, `safety_eval.py`, `planner_eval.py` |
| `../../src/backend/tests/test_mail_eval_scoring.py` | Tests of the scorer itself |

## Tests, evaluation and expected answers

`src/backend/tests/` checks application behaviour and regressions using temporary data and simulated providers. Mail evaluation compares outputs with reviewed labels; planning evaluation checks constraints, coverage and expected outcomes; safety evaluation checks approval boundaries and failure handling. These files are part of the reproducible submission evidence.

The 27 fixed planning scenarios in `src/backend/evaluation/scenarios.json` contain tasks, deadlines, calendar conflicts, preferences and rule-derived expected results. S02, for example, splits 300 minutes across days as 120 + 120 + 60 under a 120-minute daily cap. All 27 pass the automated checks. Their expectations were AI-drafted from the rules. On 12 November 2026, the team checked the Chinese case-by-case summaries of all 27 inputs and expected outcomes and confirmed them as reasonable; reviewer, date, scope and case hash are recorded in `scenarios.json`. The 200 seeded cases, separate constraint checker and single-task exhaustive search provide complementary evidence.

## Reproduce

From the repository root, after the normal setup in the main README. The mail and safety runs need the model
settings in `.env` and spend tokens (about 1,400 per mail; the whole evaluation used roughly half a million).

The commands below use macOS/Linux virtual-environment paths. On Windows replace `src/backend/.venv/bin/python` with `src/backend/.venv/Scripts/python.exe`. To reproduce the original analysis rather than evaluate the fixes, use the public baseline described in `PROVENANCE.md`. Back up saved results before a new run: the run/score/merge commands write under `docs/evaluation/results/`.

```bash
src/backend/.venv/bin/python data/synthetic/mail_eval_v1/build_dataset.py --check   # dataset matches its manifest
src/backend/.venv/bin/python scripts/eval-mail.py smoke                              # 2 throwaway mails, checks the plumbing
src/backend/.venv/bin/python scripts/eval-mail.py run --set synthetic --run 1        # repeat with --run 2, --run 3
src/backend/.venv/bin/python scripts/eval-mail.py run --set samples --run 1
src/backend/.venv/bin/python scripts/eval-mail.py score                              # no model: scores every saved run
src/backend/.venv/bin/python scripts/eval-safety.py --run 1                          # repeat with --run 2, --run 3
src/backend/.venv/bin/python scripts/eval-planner.py                                 # no model
```

Model output varies, so a new run will not reproduce the numbers exactly; the saved predictions do
(`eval-mail.py score` and `eval-safety.py --merge` recompute everything from them).

## What a run touches

Each run creates an empty database under `local-data/eval/` and never opens the app's own data. Login tokens are
kept in memory, not in the system keychain. The app runs in demo mode with external writes off. All outbound
requests go through a transport that serves the synthetic mailbox as a read-only Gmail API, lets the configured
model endpoint through, and refuses and records everything else. In the safety run, live mode is switched on only
with every mail and calendar provider replaced by a recorder.

## Rules we kept

- The answer key was frozen (`MANIFEST.json`) before the first run and is never read by the app.
- No prompt, rule or threshold of the app was changed for or during the historical evaluation. Subsequent application changes are listed separately in `PROVENANCE.md`.
- Checks were not loosened after seeing results. The five subsequent scoring/scenario/review changes are listed in `RESULTS.md` section 2, including the human label reviews completed on 10 November.
- If the app is changed in response to these results, this mail set becomes development data and a new set is needed.

## Time-saved pilot (needs people)

```bash
src/backend/.venv/bin/python scripts/time-pilot.py start --participant 1    # about 15 minutes, in a terminal
src/backend/.venv/bin/python scripts/time-pilot.py summary --mails-per-week 120
```

Each participant handles 15 mails by hand and 15 with the assistant's saved output shown first, answering the same
three questions each time (reply needed, action needed, deadline dates). Odd-numbered participants do block A by
hand and block B assisted; even-numbered the reverse, starting with the assisted block. The two blocks have the same
category mix. Time with the assistant includes checking and correcting it. Report the result as a pilot with the
number of participants, state the weekly mail volume you assume, and do not extend it to planning time, which is
not measured.

## Review status and remaining work

1. The team has checked the synthetic answer key, all 40 inbound sample labels and the 27 fixed planning expectations. Saved runs have been re-scored. A second independent labeller is still needed to measure agreement.
2. Collect and label a fresh real-mail hold-out.
3. Run the time pilot.

## Rebuilding the PDF (optional)

Install Pandoc and Chrome, Chromium or Edge, then run `python scripts/build-evaluation-pdf.py`. Browser discovery supports Windows, macOS and Linux; override it with `--browser PATH` or `CHROME_PATH`. The PDF renders `RESULTS.md`; rebuilding it does not run an evaluation or update the historical numbers. Keep new post-fix results separately labelled.
