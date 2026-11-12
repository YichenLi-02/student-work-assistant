# System Architecture and Implementation

## Architecture and data flow

A React/TypeScript/Vite frontend calls a same-origin FastAPI backend. SQLite stores local messages, tasks, proposals and study history; uploaded PDFs are stored under `local-data/`. Pure planning and calibration functions are separate from API/database orchestration. FastAPI exposes the current API schema at `/docs` and `/openapi.json`.

Mail provider -> bounded sync -> input minimisation -> local storage -> reference annotations or model analysis -> evidence validation -> task review -> study plan or reply draft -> reviewed proposal -> explicit confirmation -> provider executor.

| Directory | Responsibility |
|---|---|
| `src/frontend/src/` | Pages, components, English/Chinese translations and shared CSS tokens |
| `src/backend/app/api/` | Session-protected API routes |
| `src/backend/app/services/` | Import, analysis, tasks, documents, drafts, plans, repair and calibration |
| `src/backend/app/providers/` | OAuth, mail/calendar readers, credential references and write executors |
| `src/backend/app/llm/` | Structured model adapter |
| `src/backend/evaluation/` | Mail scoring, planning constraints and safety evaluation |
| `src/backend/tests/` | Automated behaviour and regression tests |

## Mail, evidence and tasks

Offline import reads the 40 inbound and 10 sent-style messages in `data/samples_deidentified/`. Reference annotations are identified separately from fresh model results. Google and Microsoft sync use bounded paging/retries and record partial failures. Mail attachment names/sizes are stored, rather than their contents. Outlook keeps immutable message IDs and its original-message web link.

Model mail analysis uses a strict response schema. Source IDs, exact quotes and date formats are checked locally; cached results are keyed by content, prompt, schema and model version. Missing configuration disables model features. Mail analysis and drafting use the model; group discussion organisation uses keyword rules.

Tasks distinguish official dates, missing times/time zones, estimates, progress and review status. The model path still has known false positives, duplicate deadlines and ambiguous relative-date failures; [RESULTS.md](evaluation/RESULTS.md) analyses these individually.

## Documents, group discussion and drafts

Authorised PDF uploads are parsed locally with page evidence; there is no OCR or model-based document extraction. Pasted group discussion is organised into suggestions, decisions, actions and open questions using local rules. Synthetic course documents and a group discussion are available for the offline demo.

Drafts use verified sent-mail style references when supported and a generic fallback otherwise. Missing factual reasons remain placeholders that block sending. A past explanation, grade or attachment must not be reused as a new fact. Source messages, quoted instructions and model output cannot approve an action.

## Study planning

The planner schedules remaining estimated work around busy intervals, study hours, overall/per-task daily caps, session lengths, breaks, deadline buffers and weekly flex time. Completed minutes and retained written blocks consume the appropriate allowance. Calendar-read failure produces `needs_information`, rather than assuming an empty calendar. Capacity shortages report unplaced minutes; rules are not silently relaxed.

The deterministic evaluation includes 27 fixed scenarios and 200 fixed-seed scenarios. An independent checker measures constraint violations, coverage and unplaced work. Single-task cases are also compared with an independently enumerated optimum. Multi-task global optimality is not established.

## Conflict repair and manual editing

Conflict checks reread the plan's own calendar source, account and date range. Expired plans request a new plan instead. Repair candidates move affected blocks, yield time from later deadlines or re-plan the week. They are ranked by preserved rules, unplaced work and number of changed blocks. Rule-relaxing options appear only when they help, are labelled explicitly and are never recommended automatically.

The student chooses an option or edits a block. Hard conflicts are refused; soft exceptions require explicit acceptance and remain attached to the edited block. Changed tasks, calendars or preferences invalidate stale suggestions. Written blocks can be moved inside the app's dedicated study calendar through a reviewed create/delete proposal. In demo mode, a synthetic meeting can exercise this flow without a real calendar.

## Estimate calibration

The initial effort estimate is retained separately from subsequent changes. A suggestion uses at least three previously completed tasks, preferring the same course and then task type. It uses the median actual/estimated ratio, bounds extreme ratios and changes suggestions by at most half/double. Shortening requires at least five completed tasks and closes only half the gap. Only accepting a suggestion updates the estimate.

Study check-ins preserve completed progress. Exhausting an estimate without finishing prompts the student for remaining effort. With enough recent check-ins, a low completion rate can suggest additional weekly flex time. Synthetic history can demonstrate the feature and is excluded from real calibration when demo data is hidden. Reported calibration gains are from simulated students, not a real-user study.

## Confirmation and external services

Sessions, CSRF and Origin checks protect local mutations. Live mode also requires a startup session code. Every send/calendar action needs a pending proposal whose reviewed payload hash still matches. Recipient, body, attachment or schedule changes invalidate prior approval. Unknown provider outcomes are recorded and never blindly resent.

OAuth uses PKCE/state and incremental permissions. Credentials are referenced through the system credential store. The model adapter uses `store=false` and minimised input. Local data and credentials are excluded from Git. Canvas/LMS access is excluded.

Google and Outlook calendar writes target the app's dedicated study calendar. Each moved block retains its source account, and busy-time checks preserve conflicts in other accounts. Outlook events have no attendees, use UTC and carry a transaction ID to limit duplication. Microsoft's `Calendars.ReadWrite` permission is broad; the dedicated-calendar boundary is enforced by application code. Concurrent changes between external reads and writes remain possible.

Gmail, Google Calendar and Outlook have been exercised with real accounts. Teams has not been verified with a real school account. Automated connector tests replace providers with recorders; they do not establish live account compatibility.

## Demo behaviour and limits

- Offline sends and calendar writes are recorded as `simulated`.
- The sample timetable, course documents, planning task and group discussion are synthetic and labelled as such.
- Model evaluation scores describe the baseline in [PROVENANCE.md](evaluation/PROVENANCE.md), with subsequent changes stated separately.
- Time saved, blind personal-style quality, real-user calibration and daylight-saving edge cases remain unmeasured.
- There is no OCR, general calendar-event editing/cancellation or exam-sitting placement. Group discussion rules can miss complex Chinese/English phrasing.

Setup and tests are in the [README](../README.md); Microsoft configuration is in [OUTLOOK_SETUP.md](OUTLOOK_SETUP.md).
