# Experiment notes

English is primary. Each note includes a Japanese summary. This index covers preparation and experiments; preparation is not a benchmark result.

## Index

| Date (UTC) | Note | Evidence class | Outcome |
| --- | --- | --- | --- |
| 2026-11-13 | [Argon image/routing guard](2026-11-13-argon-image-routing.md) | Synthetic configuration/process-boundary tests | Final 27/27 passed after one corrected integration-test error; no live calls |
| 2026-11-13 | [Pinned Pi request-path trace](2026-11-13-pi-static-request-trace.md) | Exact-version static source review | Conditional thinking-field omission confirmed; no actual serialization |
| 2026-11-13 | [Official source validation](2026-11-13-official-source-validation.md) | Official schema function, local-only | Passed; no model, process or Docker call |
| 2026-11-13 | [Offline wire prerequisites](2026-11-13-argon-offline-wire-prerequisites.md) | Static review and failed package setup | npm registry DNS failure; actual wire test not run |
| 2026-11-13 | [Argon configuration](2026-11-13-argon-config.md) | Synthetic generated-config/CLI tests | 7 new checks passed; combined suite 23/23; no live request or score |
| 2026-11-13 | [Logging sentinel checks](2026-11-13-logging-sentinels.md) | Synthetic/mock tests | 16 passed; pinned runtime and real integration unverified |
| 2026-11-13 | [Source preparation](2026-11-13-source-preparation.md) | Static source/provenance review | 7 focused checks passed; no runtime or score |

## Recording rules

- Start from [TEMPLATE.md](TEMPLATE.md). Record conditions, result, failures and limitations even for unsuccessful runs.
- Identify immutable source revisions or file hashes, dependency/runtime versions, configuration, task selection method and dataset revision where applicable. Do not publish restricted task content.
- Record resource limits, model/judge routes, execution count and measured cost when available. If a limit or cost is unknown, say so; do not assume it is zero.
- Label source checks, mock/synthetic checks, real runtime tests, local dev evaluations and official competition scores separately.
- Separate observed results from interpretation. Mark not-run stages explicitly. Include skipped, failed, timed-out and missing results in aggregate reporting.
- Do not publish credentials, raw task prompts/files, raw trajectories or copied outputs in notes. Review exact files before publication. Official evaluation artifacts have their own unmodified-export and review requirements.
- A note is not a substitute for the required `eval/run.py` artifacts. Never hand-create or edit scored outputs.

## 日本語

英語本文に日本語要約を添えて記録します。条件・結果・失敗・制約を残し、静的確認や合成テストと、実モデル実行・開発評価・大会スコアを区別します。未実施項目や未把握の費用を成功・ゼロとして扱いません。秘密情報や大会入力、未加工の実行履歴は公開ノートに含めません。
