# Planner Evaluation

- Generated: 2026-11-10T18:38:59+08:00 (schema 1)
- Fixed scenarios: 27/27 passed
- Known algorithm gaps against rule-derived expectations: none
- Seeded scenarios: 200, seed 5105

## Fixed Scenarios

| ID | Scenario | Category | Result | Status | New minutes | Unplaced minutes | Coverage | Violations |
|---|---|---|---|---|---|---|---|---|
| S01 | Standard single task | basic | Pass | feasible | 120 | 0 | 100% | 0 |
| S02 | Daily cap spreads work across days | daily_cap | Pass | feasible | 300 | 0 | 100% | 0 |
| S03 | Deadline buffer leaves 15 minutes unplaced | deadline_buffer | Pass | needs_adjustment | 105 | 15 | 88% | 0 |
| S04 | Insufficient total capacity | infeasible | Pass | infeasible | 240 | 360 | 40% | 0 |
| S05 | Fragmented free intervals | fragmented_free_time | Pass | infeasible | 30 | 90 | 25% | 0 |
| S06 | Work already completed today | progress_today | Pass | feasible | 240 | 0 | 100% | 0 |
| S07 | Existing study block for the selected task | written_blocks | Pass | feasible | 60 | 0 | 100% | 0 |
| S08 | Repeat generation and generation after saving | repeat_generation | Pass | feasible | 60 | 0 | 100% | 0 |
| S09 | Other tasks consume time and daily allowance | written_blocks | Pass | feasible | 120 | 0 | 100% | 0 |
| S10 | Task with less than 30 minutes remaining | short_remainders | Pass | feasible | 20 | 0 | 100% | 0 |
| S11 | Merge a short remainder into the preceding session | short_remainders | Pass | feasible | 80 | 0 | 100% | 0 |
| S12 | Short remainder across days | short_remainders | Pass | feasible | 135 | 0 | 100% | 0 |
| S13 | Calendar read failure | calendar_failure | Pass | needs_information | 0 | 60 | 0% | 0 |
| S14 | Dense deadlines: feasible | dense_deadlines | Pass | feasible | 240 | 0 | 100% | 0 |
| S15 | Dense deadlines: infeasible | dense_deadlines | Pass | infeasible | 120 | 120 | 50% | 0 |
| S16 | Weekly flex time | weekly_flex | Pass | feasible | 240 | 0 | 100% | 0 |
| S17 | Busy morning | busy_calendar | Pass | feasible | 60 | 0 | 100% | 0 |
| S18 | Insufficient evening time without late-night scheduling | infeasible | Pass | infeasible | 105 | 75 | 58% | 0 |
| S19 | Daily allowance already exhausted | progress_today | Pass | feasible | 60 | 0 | 100% | 0 |
| S20 | Completed work and written blocks both consume the cap | progress_today | Pass | feasible | 120 | 0 | 100% | 0 |
| S21 | Short remainder after a written block | short_remainders | Pass | feasible | 25 | 0 | 100% | 0 |
| S22 | Multiple tasks: unavoidable gap from session granularity | dense_deadlines | Pass | needs_adjustment | 400 | 10 | 98% | 0 |
| S23 | Multiple tasks: a different ordering fits all work | dense_deadlines | Pass | feasible | 475 | 0 | 100% | 0 |
| S24 | Meeting shorter than the required break | busy_calendar | Pass | feasible | 120 | 0 | 100% | 0 |
| S25 | Per-task daily cap | task_cap | Pass | feasible | 300 | 0 | 100% | 0 |
| S26 | Two tasks each respect the per-task daily cap | task_cap | Pass | feasible | 300 | 0 | 100% | 0 |
| S27 | Provable infeasibility under the per-task daily cap | task_cap | Pass | infeasible | 240 | 60 | 80% | 0 |

## Random Scenarios: Summary

- Status distribution: {'feasible': 117, 'infeasible': 75, 'needs_adjustment': 3, 'needs_information': 5}
- Hard-rule violations: {'overlaps_busy': 0, 'overlaps_flex': 0, 'overlaps_sessions': 0, 'break_violations': 0, 'daily_cap_exceeded': 0, 'buffer_violations': 0, 'outside_window': 0, 'short_sessions': 0, 'task_cap_exceeded': 0} (0 scenarios with a violation)
- Total unplaced minutes: 11095 (78 scenarios with unplaced work)
- Coverage: mean 0.8751, minimum 0.3, P10 0.5648
- Against the independently enumerated single-task optimum: 53/53 optimal; total gap 0 minutes
- Unplaced work without proven infeasibility: 3 scenarios, including R022, R081, R182

Zero violations alone do not establish plan quality: an empty plan also has none. Read coverage and unplaced work together. The fixed cases use AI-drafted, rule-derived expected answers. The project reviewer reviewed the Chinese summaries of all 27 inputs and expected outcomes on 2026-11-12 and confirmed them as reasonable. This review followed the saved runs.
The single-task optimum is enumerated independently of the planner. Multi-task global optimality is not established; unproven shortfalls require further analysis.

## Conflict Repair (a new meeting added to the random scenarios)

- Scenarios: 191; meetings hit written blocks in 4, with a move offered in 4
- Independently checked hard-rule violations in the recommended repair, including the new meeting: 0
- Fully resolved: 113/191; no more unplaced work than before the meeting: 185/191
- No more unplaced work than a full re-plan: 191/191
- For the 189 cases with equal work placed, mean blocks changed: recommended 1.29, full re-plan 1.67; recommended repair changed no more blocks in 189 cases
- Recommended strategy distribution: {'replan': 5, 'shift': 183, 'yield_later': 3}
- Recommended repairs that relaxed a rule: 0; cases with additional rule-relaxing alternatives: 77; relaxations without additional work placed: 0

A meeting may remove the only free time before a deadline. Full resolution need not reach 100%; compare unplaced work and the number of changed blocks with both baselines.

## Estimate Calibration (simulated, not real student data)

- 200 simulated students, 8 consecutive tasks each; three equally represented groups, actual/estimated ratios {'accurate': [1.0, 1.0], 'under': [1.2, 1.6], 'over': [0.6, 0.85]}, with per-task log-normal noise SD 0.2
- Each suggestion uses only earlier completed tasks; the calibrated condition assumes every suggestion is accepted
- No suggestions for the first three tasks: yes
- Across eligible tasks, median estimate error: 24.2% -> 17.8%

| Student group | Tasks | Suggestions | Median error (original -> calibrated) | Tasks estimated below 80% of actual time (original -> calibrated) |
|---|---|---|---|---|
| Accurate estimators | 335 | 63 | 14.1% -> 14.0% | 43 -> 36 |
| Habitual underestimators | 335 | 311 | 26.4% -> 15.7% | 226 -> 60 |
| Habitual overestimators | 330 | 172 | 38.3% -> 28.0% | 3 -> 6 |

Shortening needs at least five completed tasks and closes only half the gap, limiting new underestimates. These assumed populations test the direction and safety of the rules; the gains are not real-student accuracy.
