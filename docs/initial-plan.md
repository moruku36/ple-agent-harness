# Initial implementation plan

## Baseline

Use the official Pi harness as the source reference baseline. Apply task-content logging safeguards before any real run. Record its upstream commit, dependency locks, kit revision, model route and dataset revision. Do not report the template author's artifacts or scores as this project's run.

## First engineering change

Logging hardening is implemented and covered by [16 synthetic/mock checks](experiments/2026-11-13-logging-sentinels.md). Fixed event types and a capped stderr byte count replace task-content-bearing logs. Final responses and tool results remain protocol data. Pinned dependencies, real processes and official cancellation remain unverified. No score claim follows from these tests.

## First real pilot, currently blocked

Only proceed if a genuinely no-charge sponsored route is verified and access/setup requirements are satisfied. Do not use user-billed GCP or paid local APIs. Choose one public dev task with programmatic grading to limit initial judge cost. Define the exact model, one-task cap, concurrency 1, retries, monetary cap and deadline before starting. Measure completion, valid deliverable paths, cancellation/cleanup and token usage. Stop on failed setup or budget uncertainty. Do not automatically run all 29 tasks.

After the baseline is measured, change one factor at a time, such as deadline-aware completion or a task-agnostic deliverable checklist. Compare fixed tasks and model settings, recording failures and missing results. Never fingerprint tasks or tune to hidden material.

## Open gates

- Signed-in participation/rules acceptance has not been verified.
- Gated development-data terms/access have not been verified or accepted by this project.
- Local Docker host, resource availability and conflicts need confirmation; the current cloud workspace has no Docker executable/socket.
- User-billed GCP and paid local API calls are out of scope. A no-charge sponsored development route and approved credential setup have not been established.
- Full source, container, model, smoke, MCP, cancellation and artifact checks remain unfinished.
- Public input-data redistribution is not authorized. Generated artifacts need a publication review.

## Submission

Current Kaggle pages describe one Writeup per team, up to 2,000 words, editable/resubmittable before the deadline. Final deadline: January 5, 2027 at 23:59 UTC, January 6 at 08:59 JST. Confirm the live page again before submission. A public code repository is allowed; a private competition repository must become public at competition close. This project has not submitted or installed the submission GitHub App.
