# Student Work Assistant

DSS5105 Group 09, Track 4: a local assistant for mail triage, deadline extraction, study planning, group discussion summaries and reply drafts. A FastAPI/SQLite backend serves a React/TypeScript frontend. Every send and calendar write requires review and confirmation; offline actions are simulated.

## Requirements

- Python 3.12+ (tested on 3.14.7).
- Node.js 20.19+ or 22.12+ and Git.
- Chrome or Edge for the interface.

## Install and run

```bash
git clone https://github.com/YichenLi-02/student-work-assistant.git
cd student-work-assistant
```

Copy `.env.example` to `.env`. The defaults support the offline demo; no API key or account connection is needed.

```powershell
# Windows PowerShell
Copy-Item .env.example .env
powershell -ExecutionPolicy Bypass -File scripts/run.ps1
```

The script installs locked Python dependencies, runs `npm ci`, builds the frontend and starts the server. Add `-SetupOnly` to install/build without starting it. After setup, `Start-Local.cmd` and `Stop-Local.cmd` control the background service; Ctrl+C stops the foreground server.

On macOS/Linux:

```bash
cp .env.example .env
cd src/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt -c requirements.lock
cd ../frontend
npm ci
npm run build
cd ../backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000**, go to **Mail** and click **Refresh mail**. The repository includes 40 inbound samples and 10 sent-mail style references. Leave `SAMPLE_DATA_DIR` empty to use them. Their timestamps are historical; review dates before planning current work. See the [sample guide](data/samples_deidentified/GETTING_STARTED.md) for labels, privacy and data limits, or open `data/samples_deidentified/sample_browser.html` locally.

On **Study plan**, the offline demo supports **Simulate a new meeting** for conflict repair and **Load sample history** for estimate calibration. All generated actions still pass through review.

## Tests and evaluation

```powershell
# Backend behaviour tests: temporary database, no real sends or calendar writes
cd src/backend
.venv/Scripts/python -m pytest -q
cd ../frontend
npm run build
cd ../..

# Dataset and source-evidence checks: no model or network calls
python scripts/build-sample-package.py --check
python data/synthetic/mail_eval_v1/build_dataset.py --check

# Planner evaluation: no model or network calls
src/backend/.venv/Scripts/python scripts/eval-planner.py
```

On macOS/Linux, use `src/backend/.venv/bin/python` for the evaluation command and `.venv/bin/python` inside the backend directory. With the server running, `src/backend/.venv/Scripts/python scripts/smoke.py` checks sample import through HTTP.

`src/backend/tests/` checks application behaviour, such as approval invalidation, duplicate-send prevention and planning constraints. `src/backend/evaluation/` measures system quality: mail classification, deadline extraction, planning and safety. The planner uses 27 fixed cases with rule-derived expected answers, 200 fixed-seed cases and conflict-repair scenarios. The team checked the Chinese summaries of all 27 inputs and expected outcomes on 12 November 2026 and confirmed them as reasonable. The review is recorded in `scenarios.json`.

The [evaluation guide](docs/evaluation/README.md) explains reproduction. [RESULTS.md](docs/evaluation/RESULTS.md) contains metrics and 14 failure analyses; [PROVENANCE.md](docs/evaluation/PROVENANCE.md) identifies the evaluated code. Saved model scores describe the historical baseline. Later privacy fixes have regression coverage but have not received a new model evaluation. Time saved and blind draft quality remain unmeasured.

## Optional service connections

| Feature | Configuration |
|---|---|
| Model analysis and drafting | Set `LLM_PROVIDER=openai`, `OPENAI_API_KEY`, `OPENAI_MODEL` and `ALLOW_MODEL_PROCESSING=true`; also allow processing in Settings. Fresh model calls incur usage charges. |
| Gmail and Google Calendar | Supply your own Google OAuth client ID/secret. Register `http://127.0.0.1:8000/api/connections/google/callback`. Reading uses `gmail.readonly` and `calendar.events.freebusy`; study-calendar writes request an additional permission. A testing-mode OAuth app requires the account to be a test user. |
| Outlook mail/calendar and optional Teams | Follow [OUTLOOK_SETUP.md](docs/OUTLOOK_SETUP.md). Register `http://localhost:8000/api/connections/microsoft/callback`. A school tenant may require admin consent; Teams requires a work/school account. |
| Real sending and calendar writes | Set `APP_MODE=live` and `ENABLE_EXTERNAL_WRITES=true`, enable writes in Settings, grant the account permission and confirm each reviewed action. Sample placeholder addresses cannot be real recipients. |

Offline import, reference annotations, planning and simulated actions work without these services. The model receives minimised input using `store=false`. Credentials belong only in `.env`; OAuth tokens are held by the system credential store. Live mode requires the one-time local session code printed at startup.

Keep `.env`, `local-data/`, raw mail exports and credentials out of Git. Local data includes the SQLite database and uploaded PDFs. To reset it, stop the app and delete `local-data/app.sqlite3*`. After connecting a real mailbox, samples can be shown again under **Settings > Demo data**.

## Troubleshooting

| Problem | Fix |
|---|---|
| Python or Node is not recognised | Install the required version and add it to PATH. |
| PowerShell blocks the script | Use `-ExecutionPolicy Bypass` as shown above. |
| Port 8000 is occupied | Stop the previous app process before starting another. |
| The page shows an old build | Click Reload or press Ctrl+F5. |
| Sample import fails | Check `data/samples_deidentified/` and the `SAMPLE_DATA_DIR` setting. |
| Google sign-in is unavailable | Check the OAuth testing mode, test-user list and redirect URI. |

To use another port, stop the server, set `APP_ORIGIN=http://127.0.0.1:8010` in `.env`, then run `python -m uvicorn app.main:app --host 127.0.0.1 --port 8010` from `src/backend` with the virtual environment active. Open that same address. If using OAuth, update the callback port in `.env` and the registered redirect URIs as well.

## Project files

- [IMPLEMENTATION.md](docs/IMPLEMENTATION.md): architecture, capabilities and limitations.
- [OUTLOOK_SETUP.md](docs/OUTLOOK_SETUP.md): Microsoft account configuration.
- [Sample guide](data/samples_deidentified/GETTING_STARTED.md): data inventory, annotation rules and privacy.
- [Evaluation](docs/evaluation/README.md): methods, evidence and reproduction commands.
- [Strategic recommendations](docs/strategy/Strategic_Recommendations.pdf): three higher-education opportunities, demand evidence and implementation approaches; [LaTeX source](docs/strategy/Strategic_Recommendations.tex).

Project documentation and generated report labels are English. Original messages, exact evidence quotes, reviewer notes and bilingual test inputs retain their source language. They are evidence, rather than untranslated instructions.

To rebuild `docs/evaluation/Evaluation.pdf`, install Pandoc and Chrome/Chromium/Edge, then run `python scripts/build-evaluation-pdf.py`. Use `--browser PATH` or `CHROME_PATH` if needed. This optional tooling is not required to run the app.
