# Work on this PLE entry

Read the current Kaggle rules and organizer instructions linked in README.md before evaluation or submission. The historical starter instructions differ from current rules and are not authoritative for this entry.

- This repository contains code, not competition inputs or credentials. Keep all keys and local environment files outside it. Never force-add secrets.
- Only currently eligible Google-sponsored models may be declared for a competition entry. Local alternatives are research-only and do not establish submission eligibility.
- Do not start paid model/judge calls, download gated tasks, create credentials, accept data terms, grant GitHub App access, or submit without the required authorization.
- Do not log, retain, publish or share hidden task prompts/files. Review the inherited logger before any real run.
- Do not hard-code task answers, detect task identities, inspect graders from the harness, or read artifacts from the harness at build/run time.
- Use the official kit and a local Docker daemon; keep the kit and entry in separate repositories. Follow Windows WSL and Linux-filesystem guidance when applicable.
- Dev artifacts must be untouched exports from eval/run.py for the exact evaluated harness. Do not hand-create or edit artifacts. A harness change requires the corresponding validation and dev-set rerun.
- Keep tests focused. Clearly distinguish source checks, mock protocol tests, actual runtime checks, local dev scores and official competition results.
- Before public commits, check the exact staged files and history for secrets, raw data, task trajectories and unintended generated outputs. Do not publish restricted competition data.
