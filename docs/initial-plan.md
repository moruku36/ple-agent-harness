# Initial implementation plan

## Baseline

Use the official Pi harness as an unmodified code baseline before performance experiments. Record its upstream commit, dependency locks, kit revision, model route and dataset revision. Do not report the template author's artifacts or scores as this project's run.

## First engineering change

Review and harden runtime logging before real tasks: the inherited code logs tool arguments and subprocess error text. Replace task-content-bearing logs with bounded event types and numeric counters while preserving useful failure diagnosis. Verify with synthetic sentinel inputs and an isolated protocol test. No score claim follows from this test.

## First real pilot, pending approvals

Choose one public dev task with programmatic grading to limit initial judge cost. Define the exact model, one-task cap, concurrency 1, retries, monetary cap and deadline before starting. Measure completion, valid deliverable paths, cancellation/cleanup and token usage. Stop on failed setup or budget uncertainty. Do not automatically run all 29 tasks.

After the baseline is measured, change one factor at a time, such as deadline-aware completion or a task-agnostic deliverable checklist. Compare fixed tasks and model settings, recording failures and missing results. Never fingerprint tasks or tune to hidden material.

## Open gates

- Signed-in participation/rules acceptance has not been verified.
- Gated development-data terms/access have not been verified or accepted by this project.
- Local Docker host, resource availability and conflicts need confirmation; the current cloud workspace has no Docker executable/socket.
- No PLE model/judge spending budget or approved credential setup has been established.
- Full source, container, model, smoke, MCP, cancellation and artifact checks remain unfinished.
- Public input-data redistribution is not authorized. Generated artifacts need a publication review.

## Submission

Current Kaggle pages describe one Writeup per team, up to 2,000 words, editable/resubmittable before the deadline. Final deadline: January 5, 2027 at 23:59 UTC, January 6 at 08:59 JST. Confirm the live page again before submission. A public code repository is allowed; a private competition repository must become public at competition close. This project has not submitted or installed the submission GitHub App.
