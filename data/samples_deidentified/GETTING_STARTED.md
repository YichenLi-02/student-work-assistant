# Track 4 Mailbox Selection and Prompt Development Kit

The package contains **50 real-source messages: 40 inbound functional samples and 10 sent-mail style references**. The workbook, JSONL and browser use M01-M50 consistently. Original preparation did not modify the MBOX, connect a live mailbox, send mail, process RSVPs or change calendars.

Selection was completed on 19 October 2026. The data owner checked the 40 inbound labels on 10 November. Current application results are in [docs/evaluation](../../docs/evaluation/README.md).

## Files and language

| File | Purpose |
|---|---|
| `sample_browser.html` | English offline browser: source bodies, annotations, date evidence, search and split filter |
| `mailbox_selection_50.xlsx` | Original sample/date review workbook; original Chinese headers and reviewer fields retained |
| `prompts.md` | English P00-P09 design templates; the deployed prompt is in `src/backend/app/llm/adapter.py` |
| `YOUR_EMAIL_STYLE.md`, `style_profile.json` | English explanation and original machine-readable style annotations |
| `selected_50.jsonl` | Selected bodies, provenance, splits and original review annotations |
| `date_candidates.jsonl` | 32 time expressions from 24 messages, with negative examples, quotes and offsets |
| `annotation_en.json` | English display translations keyed to original annotations |
| `reference_view.json` | Original reference grouping, including Chinese source descriptions |
| `draft_examples.json` | Five real-mail-based drafts and one synthetic missing-reason scenario; all unsent |
| `synthetic_safety_tests.jsonl` | 20 boundary specifications, including intentionally Chinese inputs |
| `prepare_eval.py` | Standard-library helper for answer-free inputs and human-reviewed triage scoring |

Documentation and browser controls are English. Original messages, evidence quotes, human review notes, reference annotations and bilingual test inputs retain their language. Translating them in place would change the evidence or evaluation inputs. Chinese keys in `annotation_en.json` link the original labels to their English display translations.

## Source and selection

The source was 1,117,459,639 bytes, with 14,213 recognised messages: 181 carried a Sent label and one carried Spam. Parseable dates ranged from 26 July 2022 to 19 October 2026. Provider labels are metadata, not classification truth. No Trash label was found; a filename containing that word is not proof of folder contents.

Local Python decoded MIME, preferring plain text and otherwise extracting readable HTML without executing scripts or visiting links. Candidate indexing read at most 4 MiB per message: 28 reached the cap, but **none of the selected 50 did**. Large attachments were not analysed. Six calendar mails additionally had ICS VEVENT scheduling fields parsed; no other attachment bodies were read.

Subjects, labels, task terms and threads identified candidates, followed by inspection of each selected body. Selection deliberately emphasised student workflows and edge cases. It was neither random nor representative of the mailbox's natural category proportions. Original ordinals are one-based; byte offsets/lengths refer only to that exact MBOX.

The original proposed inbound counts were action-only 16, reply-and-action 3, reply-only 2 and no required action 19. These are historical selection counts, not corrected evaluation counts. Outbound messages have no inbound classification. `ignore` means no required immediate handling; optional opportunities/security notices remain visible without deletion, unsubscribe or automatic marking as read.

Use only information available at receipt. Later replies must not leak into earlier inputs. Replay updates and receipts chronologically for cross-message state; preserve uncertainty when the source time zone is unknown. Historical coursework does not automatically become a current task.

## Edge cases

1. M03 says 'Friday, Dec 6', conflicting with the 2025 calendar. M13/M14 receipts say 6 December 2025, 11:59 PM MST. Preserve evidence and flag the conflict rather than silently repairing it.
2. M02/M05/M13/M14 concern a report and a JSON file. A report receipt does not complete both; repeated receipts are not new assignments.
3. M09 specifies **23:50**, not 23:59. M10/M11 concern the same 75-minute exam within an availability window, not an all-day busy event.
4. M26/M27 share a title but have different UIDs. M26/M34 share a UID and advance SEQUENCE 5 to 6, with cancellation in the latter. M35 has a RECURRENCE-ID limiting cancellation to one occurrence.
5. M24/M25 share UID/SEQUENCE but change RRULE UNTIL. Check update time and current server state; SEQUENCE alone is insufficient. ICS uses America/New_York while the body displays UTC-7: preserve zones before converting.
6. M20 is a peer suggestion/embedded draft, not a confirmed decision or the student's style. M30 is a truncated recruiting preview without a parseable application deadline.
7. M31's 15 minutes is a code lifetime, M40 is promotion expiry and M15 is grading time. None is a new coursework deadline.

## Development and evaluation

The split is **dev 19, reserved holdout 21, style_reference 10**. Related tasks, repeated notices, calendar series and directly related personal replies stay together. Style examples related to development messages cannot count as independent test evidence.

The reserved split was inspected during selection and used during development. It is not blind. Do not use its answers as few-shot prompts; a stricter final test needs fresh labelled threads.

The data owner checked all 40 inbound labels on 10 November 2026. JSONL records review status and corrections; the evaluation report explains score changes. Independent second-labeller agreement remains unmeasured. The original workbook is not automatically synchronised with later JSONL corrections. The helper scorer requires `annotation.status=human_reviewed` and `reviewed_by` in the supplied reference.

Recommended measures:

- **Triage:** per-label precision/recall/F1/confusion matrices, both-label exact match and positive denominators.
- **Dates:** match course, deliverable and time role; separate misses, invented tasks, date/time/zone accuracy, correct nulls and conflicts. A receipt may contain valid deadline metadata while opening a pending task is a state error.
- **Merging:** merge repeated notices while preserving distinct deliverables, different UIDs and single-occurrence cancellation scope.
- **Style:** blind ratings of naturalness, relationship fit and resemblance to the student, with factual accuracy separate.
- **Planning:** independent checks of conflicts, caps, breaks, buffers, remaining effort, preserved progress and justified infeasibility; report coverage alongside violations.
- **Confirmation:** test unapproved execution, changed recipients/body/attachments, recurrence scope and duplicate sends. Specifications alone establish no pass rate.
- **Time saved:** include reading, editing, confirmation and correction; counterbalance manual/assisted conditions and report participants and step times.

Only 24 messages have annotated time expressions. Do not call this 50 deadline messages or a 100-mail experiment. Report the separate 80-mail synthetic set and each dataset's limits explicitly.

## Coverage and privacy

These historical Northbridge messages do not establish current NUS calendars or policy. Existing Canvas notifications are exported mail evidence only: no token generation, API call or link fetch. The package contains no real Teams threads, complete weekly calendar or syllabus PDF.

Parsing/indexing were local. During original selection and annotation, some candidate bodies, subjects and sent examples were displayed to an assistant and entered that model session. Do not claim no source content ever reached a model provider. No separate third-party upload of the full MBOX was made.

Names, addresses, links, codes, credentials, phones, payment identifiers, private billing addresses and relevant financial amounts were minimised; organisations/courses were later pseudonymised. Content, dates and style can still identify someone indirectly. Review residual risk before reuse; see [DEIDENTIFICATION.md](DEIDENTIFICATION.md).

Views omit quoted history, signatures and HTML formatting. Attachments are metadata only except selected ICS fields; do not claim CV/recommendation contents were read. Restore contacts only through a trusted local registry, never placeholder addresses.

The original full-body index and private mappings were removed from delivery. The MBOX remains with its owner. Files do not expire automatically; follow configured retention/deletion controls. Provider retention depends on the actual service configuration, not this script.
