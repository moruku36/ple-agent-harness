# 2026-11-20: Offline replay provenance and STEP envelope controls

Status: offline controls completed; development-set A/B not run.
Evidence class: synthetic CPU tests and pinned source review.

## Question and hypothesis

Can the preflight distinguish malformed inputs and prevent treating a changed grading run as an exact replay?

## Conditions

- UTC date: 2026-11-20. Local CPU; self-authored synthetic fixtures only.
- Evaluator source reviewed at [google-research/ple 8320f040](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/eval/run.py).
- No benchmark input, model, judge, official grader, or competition submission was used.

## Procedure and results

- A basic STEP envelope and reference-integrity precheck matched 7/7 expected outcomes. This is not an IFC schema or geometry validation.
- A separate offline replay-receipt comparison matched 7/7 expected outcomes. It refused missing evidence and mismatches in revision, task-tree manifest, grader, A/B identity or frozen deliverable. A matching deliverable alone did not establish comparability.

## Failures and limitations

The pinned evaluator can fall back to newer data if a prior dataset revision cannot be recovered. A local directory path does not bind the bytes in that directory. Separately, `--no-export` does not prevent the evaluator from writing material to its local run directory. The synthetic tests do not establish organizer approval, task provenance, grading correctness, or a benchmark score.

## Decision and next step

Require a verified immutable local snapshot and matching frozen deliverables before comparing any replay results. Keep the fixed order-only A/B unrun until the unused, pinned assets and evaluator-side retention requirements are confirmed. The [existing organizer question](https://www.kaggle.com/competitions/physical-engineerings-last-exam/discussion/759332#3557288) is pending.

## 日本語要約

自作データでSTEP外枠7/7、再採点の証跡照合7/7。いずれも大会スコアではない。課題の版、ファイル一式、採点器と成果物を同じ条件で照合できるようにする。固定版の未使用課題と公式評価器のログ保持条件が確認できるまで、実課題A/Bは保留。
