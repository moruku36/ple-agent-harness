# Work on this PLE entry

Read the current Kaggle rules and organizer instructions linked in README.md before evaluation or submission. The historical starter instructions differ from current rules and are not authoritative for this entry.

- This repository contains code, not competition inputs or credentials. Keep all keys and local environment files outside it. Never force-add secrets.
- For the submitted Stage 2 entry, only currently eligible Google-sponsored models may be declared. Current Kaggle Minimum Requirements 3–4 permit local self-hosted open-weight models or personal APIs for development artifacts, followed by switching `model_api` to an eligible `google-cloud/<id>` model before commit. Disclose the actual development model and judge; this permission does not establish local runtime availability or an Argon measurement.
- Do not use user-billed GCP or paid local API calls. Verify a safe no-paid-API route, including any judge, before live calls. Local self-hosted development is permitted, but runtime capacity and routing still require verification. Stage 2 sponsorship is conditional on top-100 Stage 1 selection, not free development access.
- Do not start paid model/judge calls, download gated tasks, create credentials, accept data terms, grant GitHub App access, or submit without the required authorization.
- Do not log, retain, publish or share hidden task prompts/files. Keep diagnostics content-free and verify them in the pinned runtime before any real run.
- Do not hard-code task answers, detect task identities, inspect graders from the harness, or read artifacts from the harness at build/run time.
- Use the official kit and a local Docker daemon; keep the kit and entry in separate repositories. Follow Windows WSL and Linux-filesystem guidance when applicable.
- Dev artifacts must be actual, untouched, unpacked exports from eval/run.py for the evaluated harness: at most 512 MiB and 10,000 files, with no Git LFS or symlinks. Do not hand-create or edit artifacts. The permitted pre-commit model_api switch is not permission for arbitrary post-run harness changes; other harness changes require corresponding validation and dev-set reruns. Both kit check and kit artifacts must pass; inspect model/judge billing before running checks.
- Keep tests focused. Clearly distinguish source checks, mock protocol tests, actual runtime checks, local dev scores and official competition results.
- Use English as the main documentation language and maintain README.ja.md alongside README.md. Give experiment notes a Japanese summary.
- Record every experiment, including failed or interrupted attempts, under docs/experiments/ with its conditions, exact source/configuration identifiers, results, failures, limitations and next step. Never report an unrun stage as completed. Keep raw task content and secrets out of public notes.
- Before public commits, check the exact staged files and history for secrets, raw data, task trajectories and unintended generated outputs. Do not publish restricted competition data.
