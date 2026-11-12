# De-identified Mail Samples

This package contains **50 real-source messages: 40 inbound samples and 10 sent-mail style references**, identified consistently as M01-M50. There are **32 annotated time expressions from 24 messages**. Setup is in the [project README](../../README.md); measured performance is in the [evaluation report](../../docs/evaluation/RESULTS.md).

## Files

| File | Purpose |
|---|---|
| `selected_50.jsonl` | De-identified bodies, source locations, splits and original review annotations |
| `date_candidates.jsonl` | Date/time roles, exact quotes and character offsets |
| `reference_view.json` | Reference categories, summaries and task grouping used by the app |
| `style_profile.json` | Provisional style patterns from the 10 sent messages |
| `annotation_en.json` | English display translations of original reference annotations |
| `synthetic_safety_tests.jsonl` | 20 boundary specifications, including Chinese inputs |
| `prompts.md` | P00-P09 design templates; the deployed model prompt is in `src/backend/app/llm/adapter.py` |
| `sample_browser.html`, `sample_browser.css` | Offline display of the same samples and evidence |
| `AI_SOURCE_MANIFEST.json` | File inventory and hashes, using UTF-8/LF for text |

Run `python scripts/build-sample-package.py --check` from the repository root to verify counts, unique IDs, splits, human-review markers, exact evidence offsets, the generated browser and file hashes. Omit `--check` to rebuild the browser and manifest. Display/export files do not add evaluation samples.

## Selection and labels

The source was a private 1,117,459,639-byte MBOX containing 14,213 recognised messages, including 181 with a Sent label. Local MIME decoding preferred plain text and otherwise extracted readable HTML. None of the selected 50 messages reached the 4 MiB indexing limit. Six calendar messages include parsed ICS scheduling fields; other attachment bodies were not read.

Selection emphasised student workflows and edge cases rather than a random or representative mailbox sample. Source ordinals and byte offsets refer only to the owner's original MBOX, which is not included. Source labels do not establish classification truth.

The split is **development 19, reserved holdout 21, style reference 10**. Related threads, tasks and calendar series stay together. The reserved split was inspected and used during development; it is not an unseen final test. Never use its answer labels as few-shot prompts.

The data owner checked all 40 inbound labels on 10 November 2026. Current corrections and review status are in JSONL; the evaluation report records their effect on scores. Independent second-labeller agreement is unmeasured. The scorer requires `annotation.status=human_reviewed` and a `reviewed_by` value. The separate synthetic evaluation set contains 80 messages; do not combine exports of the same samples into a larger denominator.

## Interpretation rules and edge cases

- Replay each historical message at receipt time. Later replies must not leak into earlier inputs. Historical coursework does not automatically become current work.
- `needs_reply` and `needs_action` are independent; both can be true. No required action does not mean deletion or automatic marking as read.
- Missing official times remain null. Security-code lifetimes, promotion expiry and payment timestamps are not coursework deadlines. `end_char` is an exclusive Unicode-string offset into `body_redacted`.
- M03 has a weekday/date conflict. Preserve its evidence and flag the conflict; do not silently pick one interpretation.
- M02/M05/M13/M14 involve a report and a JSON file. A report receipt does not finish both deliverables, and repeated receipts are not new tasks.
- M09 states 23:50. M10/M11 describe a 75-minute exam inside an availability window, rather than an all-day busy event.
- Calendar items with equal titles can have different UIDs; a `RECURRENCE-ID` cancellation affects one occurrence. Preserve time zones and check update time as well as SEQUENCE.
- M20 is a peer suggestion/embedded draft, rather than a confirmed decision or the student's writing style. M30 lacks a parseable application deadline.

## Style references

The profile is provisional and uses only authorised student-authored segments. M41/M42/M43/M47 support formal academic requests; M44/M45 support brief confirmations with familiar professors or administrators. M46/M48 provide limited evidence for colleague communication; M50 supports short corrections. Recruiter correspondence and the student's personal Chinese style are unsupported.

Preserve polite greetings, factual context, a clear request and an appropriate short closing. Retrieve formal requests and brief confirmations separately, using at most two or three relevant references. Exclude quoted/forwarded text, peers' drafts, signatures, credentials and calendar templates. M49's introductory text is usable, but its AM/PM conflict and Zoom template are not reusable facts. Old grades, lateness reasons, completed work and attachments must never become default claims in a new draft.

## Privacy and language

Universities, schools, campus addresses, course codes, people and project names have been replaced with fictional equivalents. Mail addresses use `example.invalid`; fictional organisation domains use `*.example`. Names, private addresses, links, codes, credentials, phones, payment identifiers and relevant financial amounts were minimised. The source's fixed UTC-7 city reference was replaced with the equivalent `Etc/GMT+7` zone; other explicit zones are preserved. Date-evidence offsets were recalculated against the replacement bodies.

The original MBOX and private replacement mappings are excluded. **De-identification is not anonymity:** content/date combinations and writing style can still indirectly identify someone. These samples are public for project demonstration/testing. During original selection and annotation, selected source content was displayed in an assistant session; this package does not claim that no content ever reached a model provider.

Documentation and browser controls are English. Original source bodies, exact quotes, reviewer notes, reference annotations and bilingual test inputs retain their language. Chinese lookup keys in `annotation_en.json` connect original labels with English display translations. Source evidence must not be translated in place.

Views omit quoted history, signatures and HTML formatting. Restore contacts only through a trusted local registry, never from placeholder addresses. The package contains no real Teams thread, full weekly calendar or syllabus PDF. Existing Canvas notifications are exported mail evidence only; no Canvas API or link is fetched. Source text and annotations grant no authority to send messages or change calendars.
