# Student Work Assistant

The runnable version of our DSS5105 Track 4 group project.

- **What it does:** organises mail, extracts tasks and deadlines, builds a study plan, summarises group discussions and drafts replies. Every send and calendar write must be reviewed and confirmed first. The offline version only simulates them.
- **How it is built:** a FastAPI + SQLite backend and a React + TypeScript + Vite frontend. The backend and built frontend run on one machine; no hosted server is needed.

This guide covers setup from a clean checkout, offline use and optional service connections.

---

## 1. Prepare your environment

| Software | Version | Check with |
|---|---|---|
| Python | 3.12 or later (tested on 3.14.7) | `python --version` |
| Node.js | 20.19 or later, or 22.12 or later | `node --version` |
| Git | Any recent version | `git --version` |

If something is missing, install Python from python.org (on Windows, tick "Add Python to PATH" during setup) and the LTS version of Node.js from nodejs.org.

## 2. Get the code

```bash
git clone https://github.com/YichenLi-02/student-work-assistant.git
cd student-work-assistant
```

## 3. Sample data (already in the repo)

The de-identified mail samples are in `data/samples_deidentified/`, so you get them when you clone and have nothing else to prepare. Schools, courses and names have been replaced with fictional ones, and mail addresses now use `example.invalid`. See `DEIDENTIFICATION.md` in that folder for details.

There are **40 inbound messages and 10 sent-mail style references**, with 32 annotated time expressions from 24 messages. The data owner checked the 40 inbound labels on 10 November 2026. The reserved 21-message split was used during development and is not an unseen final test.

The package guides, prompt design templates and offline browser interface are English. Source messages, exact evidence quotes, original reviewer notes, reference annotations and Chinese safety-test inputs retain their original language. `annotation_en.json` supplies English display translations; its Chinese lookup keys refer to the original labels. The original review workbook retains its Chinese headers and is not automatically synchronised with later JSONL corrections. Start with [the sample guide](data/samples_deidentified/GETTING_STARTED.md) or open `sample_browser.html` locally.

> These samples are published with this public repository. De-identified does not mean fully anonymous: course content and date combinations could still indirectly identify someone. Use them only for demonstrating and testing this project.

## 4. Configure `.env`

Copy the template in the project root:

```bash
# Windows PowerShell
Copy-Item .env.example .env
# macOS / Linux
cp .env.example .env
```

The defaults work as they are. If `SAMPLE_DATA_DIR` is empty, the app uses the samples in the repo. You only need to set this path if you move the samples somewhere else.

Leave the other settings at their defaults. Git ignores `.env`, so **do not commit it or post it in the group chat**.

## 5. Start the app

### Windows (one command)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run.ps1
```

The script creates or repairs the Python environment, checks dependencies against `requirements.lock`, runs `npm ci` and builds the frontend. A failed install or build stops startup; rerun the same command after fixing the cause. When ready, it shows `Uvicorn running on http://127.0.0.1:8000`.

To install and build without starting a server, add `-SetupOnly`. After setup, `Start-Local.cmd` and `Stop-Local.cmd` start/stop the recorded background service. The foreground `run.ps1` process is stopped with Ctrl+C.

### macOS / Linux (manual)

```bash
# Backend dependencies
cd src/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt -c requirements.lock

# Frontend build
cd ../frontend
npm ci
npm run build

# Start (from src/backend)
cd ../backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Open the app

Go to **http://127.0.0.1:8000** in your browser, open the **Mail** page and click **Refresh mail** to import the samples.

Use Chrome or Edge. Some features may not work fully in the VS Code built-in preview browser.

## 6. Development (changes apply as you edit)

Open two terminals:

```bash
# Terminal 1: backend (auto-reload)
cd src/backend
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload   # Windows
# .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload    # macOS / Linux

# Terminal 2: frontend (hot reload)
cd src/frontend
npm run dev
```

During development, use **http://127.0.0.1:5173**.

## 7. Run the tests

```bash
cd src/backend
.venv\Scripts\python -m pytest -q     # macOS / Linux: .venv/bin/python -m pytest -q
cd ../frontend
npm run build                          # also runs the TypeScript type check
```

All backend tests should pass. They use a temporary database and disable model/provider writes. Tests that depend on sample data are skipped automatically if it is missing. The Windows setup and the manual commands both use the locked Python dependency constraints.

Planner evaluation (27 fixed scenarios, 200 fixed-seed random scenarios and a conflict-repair evaluation; the report is written to `local-data/planner-eval/`):

```bash
src/backend/.venv/Scripts/python scripts/eval-planner.py      # macOS / Linux: src/backend/.venv/bin/python
```

Check the sample inventory, exact evidence offsets and generated English browser without any model/network call:

```bash
python scripts/build-sample-package.py --check
```

Omit `--check` to rebuild the sample browser, English source overview and manifest after changing a package source. Text hashes use UTF-8/LF so Windows line endings do not create false mismatches.

The [evaluation guide](docs/evaluation/README.md) covers saved-output scoring, safety results and optional model runs. [Evaluation provenance](docs/evaluation/PROVENANCE.md) maps the historical evaluation code to a public commit and records changes made afterwards. Saved model results describe that historical baseline, not a new run of the current code. Known failures include false-positive tasks, duplicate deadlines, injected instructions becoming task suggestions and ambiguous relative dates. Time saved and blind draft quality have not been measured.

**To demo conflict handling (no real calendar needed):** in demo mode, generate a plan on the **Study plan** page, expand **Simulate a new meeting**, place a meeting on a study block and click **Add meeting and check** to list the conflicts. Click **Show fix suggestions** to compare the options, pick one, then review and save as usual. **Edit** on a study block changes its time or length by hand. For details, see the "Plan conflicts" section of `docs/IMPLEMENTATION.md`.

**To demo estimate calibration:** on the same page, open **Estimates from your own history** and click **Load sample history** (synthetic data). You will see a suggested estimate for the sample report, with expandable reasoning, and a completion-rate hint. After accepting a suggestion, click **Re-plan**. In real use, data builds up as you enter the actual time when marking a task complete. For details, see the "Calibrating estimates from check-ins" section of `docs/IMPLEMENTATION.md`.

## 8. Optional: connect real services

**Offline sample import, reference annotations, planning and simulated sends work without these services.** Fresh model analysis and model-written drafts need model configuration; real mailbox/calendar access needs OAuth.

| Feature | What you need | Notes |
|---|---|---|
| Model classification and drafting | Your own OpenAI API key | Set `LLM_PROVIDER=openai`, `OPENAI_API_KEY`, `OPENAI_MODEL` and `ALLOW_MODEL_PROCESSING=true` in `.env`, then allow it under **Settings → Data processing**. Model calls incur usage charges; cost depends on the chosen model and input |
| Read Gmail / Google Calendar (read-only) | A Google OAuth client ID and secret | Either ask Yichen to add your Gmail as a **test user** of the Cloud project `dss5105-student` and get the client ID and secret privately, or create your own Google Cloud project using the steps in `docs/RUNNING.md`. The redirect URI must be `http://127.0.0.1:8000/api/connections/google/callback` |
| Read Outlook mail / calendar (read-only; optionally send mail and write to the app's Outlook study calendar) | A client ID and secret from a Microsoft Entra app registration | Follow `docs/OUTLOOK_SETUP.md`. The redirect URI is `http://localhost:8000/api/connections/microsoft/callback`. Use a personal Outlook account for demos, because school accounts usually need admin consent. After setup, check it with `scripts/check-outlook.py` |
| Teams chat | Same as above, work or school accounts only | Optional |

Keep keys and secrets only in `.env` on your own computer. Do not put them in code, screenshots or uploads. Sign-in credentials are stored in your system credential store (Windows Credential Manager), not in the project files.

## 9. Things to note

- **Never commit** `.env`, `local-data/` (the local database and uploads) or raw, non-de-identified mail data. They are already in `.gitignore`, but check `git status` before you commit.
- **Real writes are off by default.** In the offline version, sending mail, sending Teams messages and writing to calendars are only simulated, and the interface says that nothing was sent.
- **To reset local data,** stop the app, delete `local-data/app.sqlite3*` and start it again.
- **To see the demo samples** after connecting a real mailbox, where they hide automatically, turn them back on under **Settings → Demo data**.

## 10. Troubleshooting

| Problem | Fix |
|---|---|
| `python` is not recognised as a command | Reinstall Python with Add to PATH ticked, or use the `py` command |
| PowerShell refuses to run the script | Use `-ExecutionPolicy Bypass` exactly as shown in step 5 |
| Port 8000 is in use | Stop the app you started earlier (Ctrl+C in its terminal), or start on a different port |
| The page still looks old | Click **Reload** when the update notice appears at the top, or press Ctrl+F5 |
| **Refresh mail** says it cannot find the sample data | Check that `data/samples_deidentified/` exists, and leave `SAMPLE_DATA_DIR` in `.env` empty or set it to the correct path (use `/` on Windows) |
| Google's sign-in page says the app is unverified | This is normal in testing mode, so choose to continue. If you are told you have no access, you are not a test user yet |
| `npm ci` reports a Node version error | Upgrade to Node 20.19+ or 22.12+ |

## More documentation

The project documentation is in English. Original source/reviewer material and bilingual test inputs retain their language as described above.

- `docs/RUNNING.md`: details on starting, testing and configuring external services
- `docs/OUTLOOK_SETUP.md`: how to connect a real Outlook mailbox, and common errors
- `docs/IMPLEMENTATION.md`: what is implemented, how it differs from the design contract, and what is still simulated
- `docs/UI_AUDIT.md`: the interface design audit (based on the open-source refactoring-ui guidelines)
- `docs/evaluation/README.md`: evaluation methods, reproduction commands and optional time-pilot protocol
- `docs/evaluation/PROVENANCE.md`: public baseline mapping and changes after the saved model evaluation

To rebuild the historical evaluation PDF, install Pandoc and Chrome, Chromium or Edge, then run `python scripts/build-evaluation-pdf.py`. The script discovers the browser on Windows, macOS and Linux; use `--browser PATH` or `CHROME_PATH` to select one explicitly. This is optional and is not needed to run the app. Keep historical results distinct from any new post-fix evaluation.
