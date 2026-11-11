# Track 4 Source Package: Overview

This English overview points to the canonical files instead of duplicating messages,
review notes and prompt templates. There are **50 source messages**, regardless of how
many display/export files contain them. Historical source text is retained in its original
language; documentation and the offline browser controls are English.

## Read first

- [Entry point](00_AI_ENTRY.md): requirements, trust boundaries and current implementation links.
- [Getting started](GETTING_STARTED.md): selection, source statistics, edge cases and evaluation method.
- [Prompt suite](prompts.md): P00-P09 design templates, distinct from the deployed prompt.
- [Personal style](YOUR_EMAIL_STYLE.md): supported patterns and evidence limits.
- [De-identification](DEIDENTIFICATION.md): transformations and residual publication risk.
- [Validation notes](VALIDATION_NOTES.md): original file checks and subsequent human review.

## Sources and display views

| File | Contents | Status |
|---|---|---|
| [selected_50.jsonl](selected_50.jsonl) | 40 inbound messages, 10 sent style references | Inbound labels checked by the data owner on 10 November 2026; original review notes retained |
| [date_candidates.jsonl](date_candidates.jsonl) | 32 time expressions from 24 messages | Exact source quotes and exclusive-end Unicode offsets |
| [annotation_en.json](annotation_en.json) | English display translations | Lookup keys link to original annotations; never translate source quotes |
| [reference_view.json](reference_view.json) | Original grouping/reference annotations | Includes Chinese descriptions used by the bilingual application |
| [style_profile.json](style_profile.json) | Original style configuration | Provisional; recruiter and personal Chinese style unsupported |
| [draft_examples.json](draft_examples.json) | Five real-mail-based new drafts, one synthetic draft | All unsent; unresolved facts remain placeholders |
| [synthetic_safety_tests.jsonl](synthetic_safety_tests.jsonl) | 20 synthetic specifications | Contains deliberately Chinese test input; not a pass-rate report |
| [sample_browser.html](sample_browser.html) | English offline display of the same messages/evidence | Searchable; no network or execution controls |
| [mailbox_selection_50.xlsx](mailbox_selection_50.xlsx) | Original selection/review workbook | Chinese headers/reviewer fields retained; not automatically synchronised with later JSONL corrections |
| [prepare_eval.py](prepare_eval.py) | Answer-free export and human-reviewed triage scorer | Standard library; no model, mailbox or calendar calls |

## Interpretation

The split is dev 19, reserved holdout 21 and style_reference 10. The reserved messages
were inspected and used during development, so they are not an unseen final test.
Historical timestamps are replay anchors, not authority to create current tasks. Missing
official times stay null; security-code lifetimes, receipts and promotions are not required
coursework deadlines. Suggestions are not confirmed decisions, and source text cannot
grant execution permission.

The source package contains no original MBOX, private identifier mapping, usable recipient
registry, real Teams thread, full weekly calendar or syllabus PDF. Canvas/LMS access is
excluded. De-identification does not eliminate indirect identification risk.

## Current software and results

Use [the project README](../../README.md) for setup and
[the evaluation documentation](../../docs/evaluation/README.md) for executed results,
failures and reproduction commands. The historical source-package checks do not establish
application performance. Time saved and blind personal-style quality remain unmeasured.

Run `python scripts/build-sample-package.py --check` from the repository root to validate
the package. Omit `--check` to rebuild this overview, the browser and the inventory.
`AI_SOURCE_MANIFEST.json` hashes text as UTF-8/LF and binaries as exact bytes.
