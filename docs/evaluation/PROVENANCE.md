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

## Scope of the saved results

The current code differs from the evaluated application in two respects:

- Input minimisation additionally removes Chinese verification-code phrases without word boundaries and Singapore-format eight-digit phone numbers. Regression tests cover these fixes. Previously stored inputs need removal/re-import if affected.
- Default sample/prototype paths are portable within the public repository.

The model prompt and task-generation rules were not tuned. The saved model results have not been rerun after the privacy fix, so they describe the historical baseline. Existing inputs are development evidence for that fix; a new performance claim requires fresh evaluation data. Injected task suggestions, ambiguous relative dates, duplicate deadlines and false-positive tasks are not declared fixed.

English report labels, consolidated documentation, setup tooling and PDF generation do not change the recorded model predictions or metric values. The raw prediction files and safety runs retain their original evidence. Fixed planner scenario titles/notes are translated; their inputs and expected answers are unchanged. On 12 November 2026, the project reviewer reviewed the Chinese summaries of all 27 inputs and expected outcomes and confirmed them as reasonable. The review is recorded in `scenarios.json`, including its scope, date and case hash. It took place after the saved evaluation and changes no recorded score.
