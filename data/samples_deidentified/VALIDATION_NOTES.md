# Source Package Validation Notes

## Original selection checks (19 October 2026)

The delivery covered selection, draft annotations, style profiling, prompt design and file validation. Recorded checks were:

- Consistent IDs, 40 inbound/10 outbound composition and source locations; none of the selected 50 reached the MIME cap.
- Exact character-offset checks for 32 time expressions across 24 messages. Original proposed counts were 5 reply-required and 19 action-required; both can apply.
- Related-task split isolation and answer-free export for 21 reserved messages. The helper refuses references without human review.
- Confusion-matrix/exact-match arithmetic checked with four synthetic inputs, not a model performance experiment.
- Workbook filters, frozen first six rows/two columns, review dropdowns and three count formulas checked. Cached values then were 5, 19 and 50. The original delivery recorded rendered inspection of both sheets/evidence areas and no cell errors.
- All 50 browser cards, search, split filter and expand/collapse checked without external requests or script errors.
- Text/XLSX XML scanned for private addresses/token links being replaced and principal contact names.

These historical checks describe the source package, not an application pass rate or current workbook review status.

## Subsequent review and current evidence

The data owner checked all 40 inbound labels on 10 November 2026. JSONL records review status, corrections and original-language notes. The evaluation report explains score changes. Independent second-labeller agreement is unmeasured; the style profile remains provisional.

Executed mail, planning and safety results are in [docs/evaluation](../../docs/evaluation/README.md). The 20 records in `synthetic_safety_tests.jsonl` remain specifications; their existence does not prove an implementation passed. Time saved and blind style quality are unmeasured.

Workbook review columns do not write back into JSONL. Keep an explicitly reviewed JSONL reference for scoring. Do not treat the historical workbook as synchronised with later corrected labels.

## Current package checks

From the repository root:

```bash
python scripts/build-sample-package.py --check
```

This checks counts, unique IDs, split sizes, human-review markers, exact date-evidence offsets, generated summary/browser and manifest. Text hashes use UTF-8 with LF line endings; binary hashes use exact bytes. This avoids false mismatches from Windows checkout line endings. Regenerate derived files without `--check` after a source change.

English documentation/display translations do not replace source messages, quotes, reviewer evidence or Chinese boundary inputs. Generated views do not add samples.
