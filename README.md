# PLE Agent Harness

[English](README.md) | [日本語](README.ja.md)

An early agent-harness workspace for [Google - Agent Harness on Physical-Engineering's Last Exam](https://www.kaggle.com/competitions/physical-engineerings-last-exam).

## Status

Source preparation and 23 synthetic/mock tests are complete (16 logging checks and 7 Argon configuration checks). The harness has not been built, connected to a model, run on the development set, or submitted. There is no measured score for this repository. No competition input data, API credentials, task outputs, or upstream dev-set artifacts are included.

The starting implementation is the official Pi / Claude Opus 5.5 template, pinned to [commit 22c26a93a9e4974b16e4351faab0e860ff9fb24f](https://github.com/physical-engineerings-last-exam/submission-template/tree/22c26a93a9e4974b16e4351faab0e860ff9fb24f). The entry name, ignore rules and project documentation are new. The inherited logging has been hardened; dependency locks remain unchanged. Because the entry differs from the template, its existing dev-set artifacts are not claimed as our results and must not be reused as this entry's evaluation.

## Current sources

- [Kaggle competition and timeline](https://www.kaggle.com/competitions/physical-engineerings-last-exam)
- [Kaggle rules](https://www.kaggle.com/competitions/physical-engineerings-last-exam/rules)
- [Current organizer instructions](https://ple-bench.com/competition/agents)
- [Official kit](https://github.com/google-research/ple)
- [Model configuration and local costs](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/models.md)

The old template AGENTS.md and secret-committing advice were not copied. Current entries use an eligible Google-sponsored model with evaluator-injected credentials. Never commit a key, even to a private repository. Local model and judge calls can be billed to the configured account. This project will not use user-billed GCP or paid local API calls. Verify a genuinely no-charge sponsored route before any live call; sponsorship of final evaluation does not establish free local access.

## Planned model: Gemini 4 Argon

`submission.yaml` declares `google-cloud/gemini-4-argon`, an [eligible sponsored model](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/models.md). This is a candidate configuration, not confirmation of API access or a measured model result.

The Pi 1.1.0 fallback uses a 1,048,576-token context, 65,536-token maximum output, text-only input and `--thinking high`. The `reasoning` field is deliberately unset, following the [official Pi guidance](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/sample_submissions/pi-opus/README.md#L41-L52), because enabling it makes Pi emit a token budget Argon rejects. Native Gemini `MAX` is documented as weaker than `high`. Generated-config tests do not establish the actual request shape; Pi integration and image support remain unverified.

No free participant development allocation or numerical API quota has been verified. The official local Vertex proxy bills the user's GCP project; the default development judge is a separate Claude Opus 5.5 call. Do not invoke either paid route. Evaluation-injected credentials do not establish free local access. See the [Argon configuration note](docs/experiments/2026-11-13-argon-config.md).

## Before running

1. Verify current rules, data-access terms and the account's participation status.
2. Select a local Docker environment. On Windows, use WSL 2 and its Linux filesystem as the official kit requires. Keep the kit and this entry as separate sibling repositories.
3. Verify the logging change in the pinned runtime and official kit before real tasks. The focused synthetic tests pass, but installed test-time websockets was 16.0 rather than the pinned 15.0.1. Real process, WebSocket and model behavior is not validated.
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
