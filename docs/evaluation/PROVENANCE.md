# Evaluation Code Provenance and Subsequent Changes

## Public baseline for the saved model results

The saved predictions, safety runs, `RESULTS.md` and `Evaluation.pdf` record original
evaluation commit `14f3950`. That commit belonged to the earlier development repository
and is not available in this public repository's history.

The application snapshot is publicly available in
[`b5d7dc06776b3db9343aac899a5fde4e5449ea54`](https://github.com/YichenLi-02/student-work-assistant/commit/b5d7dc06776b3db9343aac899a5fde4e5449ea54).
All **47 files under `src/backend/app/` are byte-for-byte identical** to the original
`14f3950` snapshot. This comparison was performed against the data owner's retained
local development repository. [baseline-code.json](baseline-code.json) records their
paths, byte counts and SHA-256 hashes using Git blob bytes, independent of checkout
line endings. The original metadata is preserved rather than relabelled as a new run.

Public commit `6d41088cd03243c58b85b4981d291db4933d2f5d` changed two sample-directory
defaults in `app/config.py` to `data/samples_deidentified`; the remaining 46 application
files stayed identical. It also translated documentation/headings. Commit
`9a630dc554d02854a737796beebeb58d4006c027` standardised the project name in documents
and the calendar verification helper; it did not change application behaviour.

The public baseline already contains later scorer/label-review work described in
`RESULTS.md` section 2. The 47-file equivalence concerns application code, not a claim
that every evaluation script remained unchanged after the original runs.

To verify the published application snapshot, run this from the repository root:

```python
import hashlib
import json
import subprocess
from pathlib import Path

snapshot = json.loads(Path('docs/evaluation/baseline-code.json').read_text())
for entry in snapshot['files']:
    content = subprocess.check_output([
        'git', 'show', snapshot['public_baseline_commit'] + ':' + entry['path']
    ])
    assert len(content) == entry['bytes']
    assert hashlib.sha256(content).hexdigest() == entry['sha256'], entry['path']
print('All 47 baseline application files verified')
```

## Changes after the model evaluation (11 November 2026)

- **Privacy fix:** Chinese verification-code phrases without word boundaries and
  Singapore-format eight-digit phone numbers with spaces/hyphens are now scrubbed.
  Regression tests cover those cases while retaining coursework dates/times. This
  changes preprocessing for new mail/chat/document inputs. It does not automatically
  scrub previously stored data; re-import/re-sync affected sources after removal if
  needed. The historical secret-leak failure remains in the report as evidence of
  the evaluated baseline.
- **Setup reliability:** `run.ps1` checks each command's exit status, checks Python
  dependencies against the lock constraints every run, handles incomplete virtual
  environments, runs `npm ci`, and offers `-SetupOnly`.
- **PDF tooling:** the generator discovers Chrome/Chromium/Edge on Windows, macOS
  and Linux and accepts `--browser` / `CHROME_PATH`. Pandoc remains an explicit
  optional dependency. This changes rendering tooling, not evaluation scores.
- **Documentation and sample views:** README/setup/review status are reconciled;
  sample-package guides and prompt design templates are English. The offline browser
  uses existing English display annotations. The old duplicated source summary is
  an English index. The package inventory can be rebuilt and checked. Source mail,
  exact quotes, original annotations/reviewer notes, the original workbook and
  bilingual boundary inputs remain in their original language.

The deployed model prompt and task-generation rules were not tuned in this revision.
Changing preprocessing still means that the saved model scores describe the historical
baseline, **not measured performance of the revised application**. The existing mail
set is development evidence for these fixes. A new performance claim needs a fresh
evaluation set and separately labelled post-fix runs. Deterministic regression tests
do not replace a model evaluation, and no time-saving or blind-style result is claimed.

The failures concerning injected instructions becoming task suggestions, ambiguous
relative dates, duplicate deadlines and false-positive tasks are not declared fixed
by these maintenance changes. Consult the original failure analysis before a demo.
