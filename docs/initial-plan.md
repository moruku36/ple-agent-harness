# Initial implementation plan

## Baseline

Use the official Pi harness as the source reference baseline. Apply task-content logging safeguards before any real run. Record its upstream commit, dependency locks, kit revision, model route and dataset revision. Do not report the template author's artifacts or scores as this project's run.

## First engineering change

Logging hardening is implemented and covered by [16 synthetic/mock checks](experiments/2026-11-13-logging-sentinels.md). Fixed event types and a capped stderr byte count replace task-content-bearing logs. Final responses and tool results remain protocol data. Pinned dependencies, real processes and official cancellation remain unverified. No score claim follows from these tests.

## Model candidate

The candidate now declares Gemini 4 Argon, with model-specific limits and high CLI thinking; reasoning remains unset as the official Pi guide requires. After the initial configuration, [image metadata and native-backend protection](experiments/2026-11-13-argon-image-routing.md) were added. The final combined 27-test suite passes. This is not a live API or score result. The fallback now declares text/image, and unsafe Vertex/Enterprise environment flags fail closed on the native route. Actual request serialization, image handling and a no-charge route still need verification. See the [no-charge review](no-charge-paths.md).

## First real pilot, currently blocked

Current Kaggle requirements permit self-hosted open-weight development and a pre-commit switch to an eligible Google model, with disclosure of the actual development model/judge. Paid local judging is not mandatory. This permission is not proof of a usable runtime. The [local preflight](experiments/2026-11-13-rules-and-local-preflight.md) stopped before inference because resource-safety prerequisites could not be verified. Only proceed after a safe no-paid-API model/judge route and access/setup requirements are verified. Do not use user-billed GCP or paid local APIs. Start with one synthetic task to verify local inference; it is not a PLE score or development artifact. A later authorized development pilot may choose programmatic grading, but inspect the actual evaluator and judge behavior first. Define the exact model, one-task cap, model-call cap, concurrency 1, retries, monetary cap and deadline before starting. One task can trigger multiple model calls and does not guarantee a free run. Measure completion, valid deliverable paths, cancellation/cleanup and token usage. Stop on failed setup or budget uncertainty. Do not automatically run all 29 tasks.

After the baseline is measured, change one factor at a time, such as deadline-aware completion or a task-agnostic deliverable checklist. Compare fixed tasks and model settings, recording failures and missing results. Never fingerprint tasks or tune to hidden material.

## Open gates

- Signed-in participation/rules acceptance has not been verified.
- Gated development-data terms/access have not been verified or accepted by this project.
- Local Docker host, resource availability and conflicts need confirmation; the current cloud workspace has no Docker executable/socket.
- User-billed GCP and paid local API calls are out of scope. A safe, available self-hosted runtime has not been established. Any necessary credential setup remains a separate gate; local development does not require GCP billing.
- Full source, container, model, smoke, MCP, cancellation and artifact checks remain unfinished.
- Public input-data redistribution is not authorized. Generated artifacts need a publication review.

## Submission

Current Kaggle Rules B.2 permits one entry per team, not one per day. The Writeup is up to 2,000 words, editable/resubmittable before the deadline; the inspected pages specify no numerical daily retry limit. Sponsored Stage 2 evaluation is for the top 100 Stage 1 entries, not an on-demand development API. Actual unpacked eval/run.py exports must fit 512 MiB and 10,000 files, without Git LFS or symlinks; kit check and kit artifacts must pass. Disclose the development model/judge when using the permitted pre-commit model_api switch. This is not permission for unrelated post-run harness changes. Final deadline: January 5, 2027 at 23:59 UTC, January 6 at 08:59 JST. Confirm the live page again before submission. A public code repository is allowed; a private competition repository must become public at competition close. This project has not submitted or installed the submission GitHub App.
