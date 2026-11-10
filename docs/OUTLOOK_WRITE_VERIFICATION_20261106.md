# Outlook Study Calendar Writes: Acceptance Record

Date: 2026-11-06. Project: Studyspace / DSS5105 Group 09.

Conclusion: the core write path was verified on this machine's real FastAPI environment, the production frontend build and a real personal Outlook account. The review found and fixed two places where busy times from different calendars were mixed, and added 4 regression tests. The backend ended at **136 passed** at the time. This record does not mean that every account, every error branch or the whole system is free of defects.

## 1. Environment and scope

- The project's own `src/backend/.venv/Scripts/python.exe` was used, not a substitute FastAPI.
- The frontend was built with `npm run build`, which includes `tsc -b` and the Vite production build.
- The local server ran in live mode at `http://127.0.0.1:8000`.
- A personal Outlook.com account was used; the Google connection and its existing study calendar were present at the same time.
- Real operations were confirmed by the user and limited to creating the dedicated study calendar and writing, moving and cleaning up one five-minute test block: no attendees, no mail sent, no meeting invitations.
- Checked for Google and Outlook: calendar creation, writing, deleting old events, the free/busy re-check before writing, reading back written blocks, and the review preview.

## 2. Automated results

| Check | Result | Explanation |
| --- | --- | --- |
| Full backend tests before the change | 132 passed | Matches the code notes received for this round |
| New cross-account regression tests, before the fix | 4 failed | Reproduced in both directions, Google→Outlook and Outlook→Google |
| New cross-account regression tests, after the fix | 4 passed | Both code paths now separate providers |
| Full backend tests after the fix | **136 passed** | One Starlette/httpx deprecation warning, which does not affect the results |
| Production frontend build | **Passed** | 44 modules transformed, production `dist` produced |
| Fixed planner scenarios | **27/27 passed** | Known gaps: none |
| Random planner scenarios | 200, hard-rule violations **0** | Includes infeasible and incomplete scenarios; it does not mean every scenario is fully scheduled |
| Repair after a new meeting | 191, hard-rule violations **0** | Rules relaxed by the recommended repair: 0; on average 1.29 blocks changed versus 1.67 for a full re-plan |
| Estimate calibration simulation | 24.2% → 17.8% | Median error over 200 simulated students; not an accuracy figure for real users |
| Outlook read-only diagnostics | **Passed** | Mailbox and main calendar readable; dedicated study calendar exists with canEdit=true |

Commands to reproduce (project root, PowerShell):

```powershell
Push-Location src\backend
.venv\Scripts\python.exe -m pytest -q
Pop-Location

Push-Location src\frontend
npm run build
Pop-Location

src\backend\.venv\Scripts\python.exe scripts\eval-planner.py
src\backend\.venv\Scripts\python.exe scripts\check-outlook.py --live
```

The last two write local reports; `check-outlook.py --live` is read-only and never creates a calendar or writes an event.

## 3. Problems found and fixed

### 3.1 The pre-write re-check could ignore the other account's busy time

The old logic removed the full time range of every block about to be moved from the busy time of every study calendar, without checking which provider the old block belonged to.

Example: Google has an old study block at 09:30–10:00 and Outlook has a different event at 09:30–10:00. When the Google block was moved, the old logic also removed Outlook's busy time and could wrongly allow the new write. The same happened in the other direction.

Fix: `proposal_service.recheck_busy_before_write()` only removes the time of blocks being moved within the provider currently being read; the other account's busy time is kept in full.

### 3.2 Reconciling read-back blocks during re-planning could cancel the other account's events

The old logic already compared providers when deciding which blocks to keep, but when computing the remaining busy time of the study calendars it still removed every kept block.

Fix: `plan_service.reconcile_study_blocks()` only uses kept blocks of the same provider to explain that provider's busy time. An event of the other account at the same time still takes the time.

Code files changed in this round:

```text
src/backend/app/services/proposal_service.py
src/backend/app/services/plan_service.py
src/backend/tests/test_cross_provider_study_busy.py
```

The new tests cover both code paths in both provider directions, 4 in total. They do not call real Microsoft or Google services and do not touch the real database.

## 4. Acceptance with a real Outlook account

All times below are Asia/Singapore (UTC+8).

| Step | What was done, and the evidence | Result |
| --- | --- | --- |
| Permission | The permissions returned by Microsoft include Calendars.ReadWrite | Passed |
| Create calendar | Creating "Track4 study plan" confirmed in the app's review screen; the API returned success; reading the calendar again gave canEdit=true | Passed |
| Plan input | Only one new five-minute test task selected, with Outlook as the busy-time source; no other real task was included in the write | Passed |
| Write review | The review screen showed "the app's study calendar in Outlook", 17:20–17:25, no attendees | Passed |
| Real write | After confirming in the app, the event read back from Graph: 17:20–17:25, five minutes, attendees=[] | Passed |
| Re-plan | Re-planning in the interface kept the written block, shown as "already written, kept"; the time still to schedule dropped to 0 minutes | Passed |
| Move review | Edited in the app to 17:25–17:30; the review screen listed both the new block and the old 17:20–17:25 block to be removed | Passed |
| Move | The new event exists at the right time; reading the old event returns 404; only one test event remains in the study calendar window | Passed |
| Outlook web check | Opened the Outlook web calendar, selected the study calendar and saw the test event with its 17:25–17:30 details | Passed |
| Main calendar comparison | For a fixed seven-day window, a digest of the main calendar's events (id/changeKey/start/end/showAs/isCancelled, normalised) was identical to the baseline after writing, moving and cleaning up | Passed |
| Clean-up | The test event was deleted in Outlook on the web; reading it through Graph returns 404 and the window holds 0 test events; the local test task was marked ignored | Passed |

The dedicated study calendar was kept and can be used normally. Only this test event was cleaned up; real tasks, existing study blocks and other people's events were not changed. The main calendar baseline had 0 events in the query window, so "the main calendar did not change" applies to that window only and is not a full audit of every calendar and all history.

The test block has been cleaned up and is no longer visible in the calendar. Screenshots of what was shown, the review records and the API read-back results were saved to a local evidence folder.

## 5. Permission notes and limits of this acceptance

1. `Calendars.ReadWrite` itself can read and write all of the user's calendars. Writing only to the app's study calendar is enforced by the study calendar ID stored by the backend and by the write path; it is not a narrow permission offered by Microsoft. This round only touched that calendar.
2. The pre-write re-check narrows the window in which the calendar can change after the preview, but it cannot make reading and writing an external calendar one atomic transaction. A concurrent change between the re-check and the write is still possible.
3. This round tested creating, reading back, moving and deleting a five-minute block inside Outlook; a real migration between Google and Outlook was not run. Existing automated tests cover choosing the target calendar, and the new tests cover busy-time separation between providers; that should not be called a real cross-account migration test.
4. No system time or completion progress was faked for the test. The new Outlook block was cleaned up before it ended, so the "Did you finish it?" prompt was not triggered by this real block; completion feedback is not a new real-account result of this round.
5. Reading back the study calendar still matches by time range against the local write records. Changes made directly on the Outlook or Google websites, such as moving a time or adding an overlapping event, are not the same as matching every event by ID; this round verified the in-app move path.
6. No rate limiting, network failure, revoked permission or deletion of the whole study calendar was provoked on the real account. One success does not prove that all of those recovery paths work.
7. The previously recorded expired model key was not fixed in this round; the calendar path and the planner tests above do not depend on a successful model call. This report is not an acceptance of model processing.

## 6. Evidence and hand-over

This report can be shared with the code. The private evidence on the test machine is:

```text
local-data/outlook-write-qa-20261106/state.json
local-data/outlook-write-qa-20261106/create-calendar-review.png
local-data/outlook-write-qa-20261106/write-review.png
local-data/outlook-write-qa-20261106/write-executed.png
local-data/outlook-write-qa-20261106/readback-kept.png
local-data/outlook-write-qa-20261106/move-review.png
local-data/outlook-write-qa-20261106/move-executed.png
local-data/outlook-write-qa-20261106/outlook-event-proof.png
local-data/outlook-check.json
local-data/planner-eval/report.md
```

These local files may contain the account, internal event IDs or task information. They stay in the ignored `local-data/` folder; do not commit that folder to a public repository. The local review scripts never send mail and never confirm proposals on the user's behalf.
