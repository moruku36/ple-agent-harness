# Current rules reconciliation and stopped local preflight

Date checked: 2026-11-13 (UTC). Evidence class: live public-page review and local preflight, not model inference. English is primary; Japanese summary below.

## Objective and identifiers

Determine whether real development artifacts can be produced without paid APIs or GCP billing while retaining Argon as the final model candidate. Assess a bounded synthetic local smoke test before any competition-data run.

- Entry source reference: `b3abc782eb03991766163b699a20f9a5dfaef4ee`, reverified as remote main during the review. This local documentation correction is not a new published commit.
- Official kit reference: `8320f0402fdca9f42476607f72bcfd5271cd50c9`.
- Inherited template: `22c26a93a9e4974b16e4351faab0e860ff9fb24f`.
- Declared candidate remains `google-cloud/gemini-4-argon`; no runtime code, dependencies or model declaration changed in this correction.
- No development dataset, task selection, inference output or judge result exists for this attempt.

## Procedure and findings

1. Inspect the live [Kaggle Rules](https://www.kaggle.com/competitions/physical-engineerings-last-exam/rules) and [Overview](https://www.kaggle.com/competitions/physical-engineerings-last-exam/overview). Rules B.2 says one entry per team, not one per day. A Writeup of at most 2,000 words can be unsubmitted, edited and resubmitted before the deadline; no numerical daily retry allowance was found in those pages.
2. Reconcile Minimum Requirements 3–4 with older repository guidance. Actual development artifacts may use a self-hosted open-weight model or personal API without GCP billing. Before commit, `model_api` may switch to one of the eight eligible Google models, including Argon. Disclose the actual local model/judge. Paid local judging is not mandatory; organizers rescore. This does not authorize invented artifacts, claims of measured Argon performance or arbitrary post-run harness changes.
3. Confirm the remaining artifact requirements: actual, untouched, unpacked `eval/run.py` exports, within 512 MiB and 10,000 files, without Git LFS or symlinks. `kit check` and `kit artifacts` must pass. No special validation order after the permitted model switch was specified on the inspected page.
4. Separate sponsored evaluation from development access. Stage 2 covers the top 100 Stage 1 entries, not an on-demand free development API. General Argon has no Free tier, the official local Vertex proxy bills GCP, and current default kit/evaluator paths can call both models and judges. None was executed.
5. Perform a limited existing-runtime preflight. An existing local model/runtime candidate was found, but the GPU safety condition was not satisfied and CPU/RAM capacity could not be verified. No safety-threshold relaxation or inference was attempted. The preflight therefore stopped before inference.
6. Correct the English/Japanese documentation and engineering guidance locally. Preserve historical experiment results; add a supersession pointer where the earlier artifact/model conclusion needs correction.

## Additional pinned source review, not execution

The [source-only feasibility section](../no-charge-paths.md#source-only-feasibility-checks-only-pilot-not-executed) records a conditional checks-only route that avoids the kit's LLM judge, requires genuine measured exports and preserves actual local-model/harness provenance. The permitted later model declaration switch creates a provenance warning rather than automatic artifact refusal; it does not establish final full-check readiness. The local-model readiness gate and a real Argon proxy requirement leave the zero-charge final check unresolved.

The evaluation CLI has no request/token/short-timeout cap; staging sets a six-hour agent timeout even with existing task data. One task, trial or attempt is not one model request. No pilot was run, no task was assumed fast, and no request/time budget was established by this source review. Exact pinned source citations are in the linked section.

## Results, failures and limitations

- Model requests: **0**. GCP requests: **0**. Paid provider/judge requests: **0**. Competition submissions: **0**. New runtime/model downloads or installations: **0**.
- No inference latency, completion quality, tool-use result, token usage, development score or official score was measured. No benchmark artifacts were generated.
- Runtime availability remains blocked by unverified resource-safety prerequisites. Static source feasibility is not an installed-runtime test or permission to bypass those prerequisites.
- The previously recorded 27 synthetic/mock tests were not rerun for this correction. This note makes no new serializer, build, runtime, cancellation or end-to-end verification claim.
- Official pages can change. The checked Kaggle pages did not display a modification date; no exact publication sequence relative to the kit documentation is asserted.
- This is a local-only documentation correction. No commit, push, PR, public publication, credential setup, data download or submission occurred.

## Next decision

First establish safe capacity and explicit local-only routing for an existing verified runtime, with a one-request synthetic budget, bounded resources, no paid fallback and cleanup. Do not proceed while those checks are unavailable. Only after a successful synthetic smoke run and separately satisfied data/runtime gates should a genuine development pilot be considered. See the [current no-paid-API route guide](../no-charge-paths.md) for sources and constraints.

## 日本語要約

- 現行規約はチーム当たり応募1件で、1日1件ではありません。Writeupは締切まで取消・編集・再提出できますが、日次回数の数字は確認できません。
- 自己ホスト等の別モデルで実際の開発生成物を作り、コミット前に `model_api` をArgon等へ変更できます。実際の生成モデル・採点設定を開示します。有料のローカル採点は必須ではありません。以前の同一モデル必須という説明を訂正しました。
- 無料のStage 2評価はStage 1上位100件向けです。随時使える無料開発APIではなく、一般Argon APIや既定のキット呼び出しが無料になるわけでもありません。
- 実行環境の事前確認ではリソースの安全条件を確認できず、推論前に停止しました。安全条件を緩和していません。実モデル呼び出し・GCP・有料採点・大会提出はすべて0件で、性能結果や評価生成物はありません。
- 英語本文と日本語版をローカルで訂正しました。既存の27件の合成・モックテストは再実行せず、コード変更や公開操作も行っていません。

- 追加の固定版ソース確認では、checks専用タスクでLLM採点を避け、実測の生成物と実際のモデル情報を保存する経路を確認しました。モデル宣言変更後の警告は拒否とは異なりますが、無課金Argonの最終チェックは未解決です。
- CLIに呼び出し数・トークン数・短い期限の指定はなく、準備処理は期限を6時間にします。1タスク・1試行は1呼び出しではありません。実行や予算の安全性を確認した結果ではなく、ソース上の調査結果です。
