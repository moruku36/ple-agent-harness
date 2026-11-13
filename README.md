# PLE Agent Harness

[English](README.md) | [日本語](README.ja.md)

An early agent-harness workspace for [Google - Agent Harness on Physical-Engineering's Last Exam](https://www.kaggle.com/competitions/physical-engineerings-last-exam).

## Status

Source preparation only. The harness has not been built, connected to a model, run on the development set, or submitted. There is no measured score for this repository. No competition input data, API credentials, task outputs, or upstream dev-set artifacts are included.

The starting implementation is the official Pi / Claude Opus 5.5 template, pinned to [commit 22c26a93a9e4974b16e4351faab0e860ff9fb24f](https://github.com/physical-engineerings-last-exam/submission-template/tree/22c26a93a9e4974b16e4351faab0e860ff9fb24f). The harness code and dependency locks are initially unchanged. The entry name, ignore rules and project documentation are new. Because the entry differs from the template, its existing dev-set artifacts are not claimed as our results and must not be reused as this entry's evaluation.

## Current sources

- [Kaggle competition and timeline](https://www.kaggle.com/competitions/physical-engineerings-last-exam)
- [Kaggle rules](https://www.kaggle.com/competitions/physical-engineerings-last-exam/rules)
- [Current organizer instructions](https://ple-bench.com/competition/agents)
- [Official kit](https://github.com/google-research/ple)
- [Model configuration and local costs](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/models.md)

The old template AGENTS.md and secret-committing advice were not copied. Current entries use an eligible Google-sponsored model with evaluator-injected credentials. Never commit a key, even to a private repository. Local model and judge calls are billed to the configured account and require an approved budget before execution.

## Before running

1. Verify current rules, data-access terms and the account's participation status.
2. Select a local Docker environment. On Windows, use WSL 2 and its Linux filesystem as the official kit requires. Keep the kit and this entry as separate sibling repositories.
3. Resolve the initial template's logging of tool arguments and subprocess errors. Runtime logs must not retain task prompts or file contents. This inherited behavior has not yet been hardened or live-tested.
4. Confirm the model/proxy, judge, credentials route, monetary cap, task count and stop conditions. Do not assume sponsored final evaluation makes local checks free. `kit check` includes model calls.
5. Run the official checks, cancellation test and a bounded pilot, then the authorized dev-set evaluation. Preserve the unmodified `eval/run.py` export and record source/data revisions.
6. Inspect generated artifacts for copied raw inputs and secrets before publication. Do not manually edit benchmark outputs to improve their score. Commit the verified code and artifacts together only after review.

The initial source check is not an official kit check, a test of cancellation, or evidence of score, eligibility or submission success.

## Experiment notes

English is the primary documentation language, with a Japanese README and Japanese summaries in experiment notes. Keep both README versions synchronized when status or usage changes.

Use the [experiment index](docs/experiments/README.md) and [note template](docs/experiments/TEMPLATE.md). Each actual experiment records its objective, exact code/configuration, environment and resource limits, procedure, measured results, failures, limitations and next decision. Record unsuccessful runs too. Source reviews and synthetic tests are labeled separately from live model runs, local dev-set scores and official results. Never fill an unrun stage with an assumed result.

Public notes contain code/configuration identifiers and reviewed aggregate results, not credentials, task prompts, input files, raw trajectories or copied task outputs. Benchmark artifacts have a separate review and publication requirement; notes do not replace them.

## License

Apache-2.0. Original Google copyright and license notices are retained. See [LICENSE](LICENSE). Competition data is subject to separate competition and dataset terms and is not included here. Kaggle Writeup and documentation licensing at submission must also satisfy the current competition rules.
