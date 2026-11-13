# No-charge development and evaluation paths

Checked: November 13, 2026 (UTC). English is primary; Japanese summary below.

## Current decision

Keep preparing and validating source without model calls. Do not use user-billed GCP or paid local APIs. A complete no-charge Argon development-to-submission path has **not** been verified.

## What the official sources establish

| Stage or route | Verified status | Consequence |
| --- | --- | --- |
| Organizer-hosted competition evaluation | [Google's announcement](https://cloud.google.com/blog/products/ai-machine-learning/introducing-physical-engineerings-last-exam-for-agents) describes sponsored models running free on the organizer's servers; the [guide](https://ple-bench.com/competition/guide) describes injected evaluation credentials. | This does not establish participant access to a free development API. |
| General Gemini 4 Argon API | The [official pricing page](https://aistudio.google.com/docs/pricing#gemini-4-argon) explicitly excludes Argon from the Free tier. | Do not use a general Gemini API key assuming Argon is free. |
| Official local Vertex proxy | [Kit model documentation](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/models.md#L30-L49) bills the participant's GCP project. | Not an approved route for this project. |
| Local development judging | [Evaluation documentation](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/eval/README.md#L18-L37) uses a separate default Claude Opus 5.5 judge. | A free model route alone would not establish free judging. |
| Participant Argon allowance, credits or Kaggle-specific environment | No confirmed allocation, access instructions, numerical quota or expiry was found in the inspected official materials. Kaggle discussion content was not readable in this inspection. | Unverified, not proof that no such program exists. Do not infer entitlement. |

## Useful work without provider calls

- Inspect and improve source, using synthetic data only.
- Run local mock tests while clearly separating them from actual client serialization, live runtime behavior and benchmark scores.
- Use the official source validator when its existing local dependencies are available. At kit revision `8320f0402fdca9f42476607f72bcfd5271cd50c9`, [cmd_validate](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/__main__.py#L66) calls [spec.load](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/spec.py#L161), which performs local YAML and schema checks. It does not run the declared install/serve commands or invoke a model, judge or Docker.
- Review artifact structure locally after genuine artifacts exist. The [artifact inspection command](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/__main__.py#L296) is distinct from evaluation. It may hash files and invoke Git, so inspect its scope and existing Git configuration before using it. Do not use `--from` to import another entry's artifacts.

Use an existing Python environment for source-only validation. `uv run` can provision dependencies; it is not interchangeable with a purely local validation call. `kit check`, including `--no-smoke`, still tests model connectivity. `eval/run.py --artifacts` can call the judge. Do not treat those commands as no-charge checks.

These are available kinds of work, not claims that each check has run. Experiment notes record the actual attempted commands and results.

## A different-model option is a separate decision

[Gemini 3.8 Flash pricing](https://aistudio.google.com/docs/pricing#gemini-3.8-flash) lists a general API Free tier, unlike Argon. This account's eligibility and quota are unverified, and free-tier inputs are subject to product-improvement use. No key was obtained or call made. This is not approval to transmit competition data or switch models.

A Flash experiment could not supply evaluation artifacts for the declared Argon entry. The [competition rules](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/rules.md#fair-play) require artifacts from the submitted harness and declared model. Official starter outputs and other models' results must not be relabeled as this project's Argon run.

## Questions that remain unresolved

1. Is there a participant development allocation for Argon separate from organizer-hosted final evaluation?
2. If so, how is access obtained, what are the request/token caps and expiry, and can it be used without enabling GCP billing?
3. Does it also cover the required development judge, or is there an official no-charge judging service?
4. Which development artifacts are mandatory for the current submission flow, and is a no-charge organizer-supported generation route available?

No organizer message, account setup, credential request, terms acceptance, data download or submission was made as part of this review. Those actions are separate from reading documentation.

## 日本語要約

- 主催者サーバー上の大会評価はスポンサー提供ですが、参加者向けの無料開発 API があることまでは確認できていません。
- 一般 Gemini API の Argon は無料枠の対象外です。公式ローカルプロキシは利用者の GCP に課金され、開発時の採点モデルも別呼び出しです。これらの有料経路は使いません。
- モデルを呼ばないソース検査と合成テストは進められます。公式の source validate は YAML と設定の検証のみです。`kit check --no-smoke` や評価用 artifacts の生成を、無料の静的確認と混同しません。
- Flash の一般無料枠は別の選択肢ですが、本人の利用資格・上限・データ利用条件は未確認です。他モデルやスターターの結果を Argon の評価生成物に転用できません。
- 大会独自の Argon 開発枠、取得方法、上限・期限、採点費用の扱いが未解決です。未確認を「制度がない」と断定せず、実呼び出しは保留します。
