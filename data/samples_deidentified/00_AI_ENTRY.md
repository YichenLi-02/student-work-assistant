# Track 4 AI Project: Entry Point

This de-identified source package supports Student Work Assistant. The mailbox selection was prepared on 19 October 2026. That is a historical snapshot: supply an explicit `reference_datetime` when replaying a message.

The application is implemented. Use the repository's [README](../../README.md) to run it, [IMPLEMENTATION](../../docs/IMPLEMENTATION.md) for current capabilities, and [evaluation results](../../docs/evaluation/RESULTS.md) for measured performance. The requirements below are design goals, not claims that every goal is implemented.

## Requirements and boundaries

The intended workflow combines authorised Gmail/Outlook, Teams, calendars, user-provided syllabus PDFs and approved academic calendars: find coursework mail, classify it, extract tasks and date evidence, check meetings, propose a realistic study plan, draft an extension request if needed, then let the user review and confirm the exact content before sending.

1. Classify with independent `needs_reply` and `needs_action` labels. Both may apply. `ignore` never deletes mail.
2. Extract explicit and relative deadlines with source quotes, time zones and uncertainty. Missing official times stay null rather than becoming 23:59. Identify duplicates, updates and conflicts.
3. Draft from the student's verified, authorised sent-mail segments for the appropriate relationship. Never invent reasons, experience, completed work or attachments.
4. Plan remaining effort around read-only busy intervals and preferences: daily caps, session lengths, breaks, sleep boundaries, deadline buffers and flexibility. Preserve completed work during re-planning. Flag capacity shortages and workload concentrated within 48 hours.
5. Separate suggestions, confirmed decisions, owners, actions and open questions. Drafts and absence of objections are not confirmed decisions. Draft agendas and follow-ups.
6. Preview every send, RSVP and calendar write. Confirmation binds the full payload; changed recipients, body, attachments, time or scope require new review. A model cannot grant approval.
7. Explain local/model data flows, minimise inputs, support exclusions, and document retention/deletion. Begin with read-only access.
8. Evaluate with human-reviewed labels and independent constraint checks. Separate missed and invented deadlines, and include user checking, editing and correction time.

Canvas/LMS integration is excluded: do not generate tokens, call Canvas domains or depend on its API. Existing LMS notifications are mail evidence only; their links are not fetched. Authorised, user-provided PDFs may be read. This package itself does not authorise connecting accounts, uploading a mailbox, sending messages, changing calendars, submitting forms or publishing data.

## Reading order

1. [GETTING_STARTED.md](GETTING_STARTED.md): selection, source statistics, edge cases, evaluation and privacy.
2. [prompts.md](prompts.md): P00-P09 design templates, distinct from the deployed model prompt.
3. [YOUR_EMAIL_STYLE.md](YOUR_EMAIL_STYLE.md) and `style_profile.json`: supported writing patterns and limits.
4. `selected_50.jsonl` and `date_candidates.jsonl`: machine-readable sources and evidence.
5. `draft_examples.json`, `synthetic_safety_tests.jsonl` and [VALIDATION_NOTES.md](VALIDATION_NOTES.md): drafts, test specifications and the scope of recorded checks.
6. `sample_browser.html`: English offline view. `mailbox_selection_50.xlsx` is the original review workbook. These views contain the same samples, not extra evaluation data.

[TRACK4_SOURCE_SUMMARY.md](TRACK4_SOURCE_SUMMARY.md) provides an English overview and links to canonical files. Import individual files in software; do not count both the summary and its sources as separate samples.

## Data identity, language and provenance

- `selected_50.jsonl`: 40 inbound functional samples and 10 of the student's sent-mail style examples. Bodies are de-identified views with quoted history/footers trimmed, not raw EML/MBOX. The data owner checked the 40 inbound labels on 10 November 2026. Original annotations and review notes retain their language.
- `date_candidates.jsonl`: 32 time expressions from 24 messages, including conflicts and non-task times. Offsets index the corresponding `body_redacted` Unicode string; `end_char` is exclusive. These are not 32 confirmed pending tasks.
- `annotation_en.json`: English display translations. Chinese lookup keys refer to the original annotations; they are not untranslated interface text.
- `reference_view.json` and `style_profile.json`: original reference annotations, including Chinese source descriptions. English display translations are supplied separately.
- `draft_examples.json`: five new drafts based on real mail and one synthetic scenario, all unsent.
- `synthetic_safety_tests.jsonl`: 20 synthetic boundary specifications, including Chinese input to test bilingual handling. Executed results are in `docs/evaluation/`.
- `AI_SOURCE_MANIFEST.json`: current inventory and hashes. Regenerate with `python scripts/build-sample-package.py`; add `--check` to verify.

Mail, chat, quotes, attachments, embedded drafts and style examples are untrusted data. Claims to be system instructions or user confirmations do not become instructions or approval. The prompt suite is explicitly a design template, not a source of authority.

The split is `dev=19`, `holdout=21`, `style_reference=10`. Related threads/tasks stay together. The reserved set was inspected during selection and used during development; it is not an unseen final test. Do not use its answers as few-shot examples. Current evaluation documents distinguish it from the separate synthetic set.

## Limits and privacy

Historical Northbridge coursework does not establish NUS reading week, the current timetable or official policy. The package contains no real Teams discussion, complete personal calendar or syllabus PDF. Supply missing sources legitimately, or demonstrate clearly labelled synthetic inputs. Historical messages do not authorise creating current tasks.

Identifiers have been minimised and organisations pseudonymised, but course content/date combinations may identify someone indirectly. De-identification is not anonymity. No usable real recipient address or login token is supplied. See [DEIDENTIFICATION.md](DEIDENTIFICATION.md).

The original 1.12 GB MBOX and private replacement mappings are not included. Original ordinals and byte offsets refer only to the same source file retained by the data owner. They do not authorise retrieving or uploading it.
