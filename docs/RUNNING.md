# Student Work Assistant: Running, Testing and Configuration

## Prerequisites

- Python 3.12 or later (tested on 3.14.7) and Node.js 20.19+ or 22.12+ (tested on 24.21).
- By default the sample data is the **de-identified copy** in this repository, `data/samples_deidentified` (schools, course codes, people and project names are replaced with fictional ones; see `DEIDENTIFICATION.md` in that folder). The app reads `selected_50.jsonl`, `date_candidates.jsonl`, `style_profile.json` and `reference_view.json`. The original, non-de-identified mail export is never read by the app and is not in this repository.
- The reference grouping (topic category, "important" flag, summary) comes from `reference_view.json` in the copy and is shown as a "suggested label". Only when that file is missing does the app fall back to the design pack's `ui/index.html`.
- Both locations can be changed in `.env` with `SAMPLE_DATA_DIR` and `DESIGN_DIR`.

## Start with one command (offline, no keys needed)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run.ps1
```

Open http://127.0.0.1:8000, go to the **Mail** page and click **Refresh mail** to import the 40 inbound mails and the 10 tone references.

On Windows you can also double-click `Start-Local.cmd` and `Stop-Local.cmd` once the dependencies are installed and the frontend is built.

`run.ps1` checks Python dependencies on every run using `requirements-dev.txt` constrained by `requirements.lock`, reinstalls frontend dependencies with `npm ci`, and stops if any step fails. This also repairs interrupted installs. Add `-SetupOnly` to finish installation/build without starting the server. `Start-Local.cmd` controls a background service; the foreground server from `run.ps1` is stopped with Ctrl+C.

## Development mode (two terminals)

```powershell
# Terminal 1: backend
cd src/backend
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt -c requirements.lock
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: frontend (Vite proxies /api to port 8000)
cd src/frontend
npm ci
npm run dev        # http://127.0.0.1:5173
```

## Tests

```powershell
cd src/backend
.venv\Scripts\python -m pytest -q          # temporary database; model/provider writes disabled
cd ../frontend
npm run build                              # TypeScript type check and production build
cd ../..
src/backend/.venv/Scripts/python scripts/smoke.py   # smoke check against a running server
```

The evaluation scripts (`scripts/eval-mail.py`, `scripts/eval-safety.py`, `scripts/eval-planner.py`) are described in `docs/evaluation/README.md`.

Run `python scripts/build-sample-package.py --check` from the repository root to verify sample counts, human-review markers, exact date evidence, the English browser/overview and the file inventory. Omit `--check` to regenerate derived files. Original-language messages and reviewer records remain unchanged; see `data/samples_deidentified/GETTING_STARTED.md` for the language policy.

Saved model results describe the public baseline linked in `docs/evaluation/PROVENANCE.md`. Later privacy fixes are covered by regression tests; the saved model evaluation has not been rerun for those fixes.

## Local data

- `local-data/` holds the SQLite database and copies of uploaded PDFs. It is in `.gitignore`; do not commit it.
- To reset the demo data, stop the server and delete `local-data/app.sqlite3*`.

## Connecting real services (optional; offline features work without them)

| Capability | What to configure | Notes |
|---|---|---|
| Model analysis and drafting | `LLM_PROVIDER=openai`, `OPENAI_API_KEY`, `OPENAI_MODEL`, `ALLOW_MODEL_PROCESSING=true`, then allow it under **Settings** | Uses the Responses API with a strict JSON schema and `store=false`; only the subject, the de-identified body, the time and the time zone are sent |
| Gmail read-only, Google free/busy | `GOOGLE_CLIENT_ID/SECRET`; register the redirect URI `http://127.0.0.1:8000/api/connections/google/callback` in Google Cloud | Read-only scopes are `gmail.readonly` and `calendar.events.freebusy` |
| Outlook mail and calendar read-only, Teams chat read-only | `MICROSOFT_CLIENT_ID`, `MICROSOFT_CLIENT_SECRET`, `MICROSOFT_TENANT_ID=common`; register the redirect URI `http://localhost:8000/api/connections/microsoft/callback` on the Web platform in Microsoft Entra | Permissions are `Mail.Read`, `Calendars.Read` (read-only) and `Chat.Read` (Teams, work or school accounts only); optional `Mail.Send` and `Calendars.ReadWrite` (writes only to the Outlook study calendar the app creates). A school tenant may require admin consent. Full steps in `docs/OUTLOOK_SETUP.md`; check the setup with `scripts/check-outlook.py [--live]` |
| Real sending and calendar writes | `APP_MODE=live`, `ENABLE_EXTERNAL_WRITES=true`, real writes switched on in Settings, and the extra write permission granted on the account | Every action still needs its own review and confirmation; de-identified sample addresses can never be used for a real send |

OAuth tokens are stored in the Windows Credential Manager (through `keyring`); the database only holds a reference, and tokens never appear in the browser, a URL or the logs. With `APP_MODE=live`, the server prints a one-time local session code to the console at start-up.
