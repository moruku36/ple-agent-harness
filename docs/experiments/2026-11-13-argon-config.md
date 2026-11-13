# Gemini 4 Argon: local configuration and CLI checks

## Status and question

**Completed: source configuration and synthetic/mock checks only. No Pi execution, model
request, official kit check, real task, benchmark score, or submission.**

Date: November 13, 2026 (UTC).

Can this entry select the planned sponsored Gemini 4 Argon model and generate
the recommended Pi 1.1.0 fallback configuration without changing other models'
defaults or weakening the existing content-free logging changes?

This note records local preparation. It does not establish model access,
request compatibility, free development access, or competition acceptance.

## Changes and pinned guidance

- Set `submission.yaml` to `model_api: google-cloud/gemini-4-argon`.
- Select Pi CLI `--thinking high` for the exact model ID `gemini-4-argon`.
  Other models retain the inherited `max` default. Argon supports low, medium
  and high; native MAX is weaker than high.
- When Argon is absent from Pi's catalog, use **1,048,576 context tokens** and
  **65,536 output tokens**, with `input: ["text"]`. Keep `reasoning` unset.
  Other uncatalogued models retain 128,000 / 16,384 and text-only input.
  Existing catalog behavior is unchanged for recognized models.
- Preserve the native Google route: `GOOGLE_GEMINI_BASE_URL` plus `/v1beta`,
  `api: google-generative-ai`, and an API-key environment-variable reference.
  Preserve the existing OpenAI-compatible fallback route when the native
  provider environment variables are absent.
- Retain Google copyright/license notices and add modification notices.
  Preserve the previous logging changes and all dependency pins.

Official guidance at kit revision
`8320f0402fdca9f42476607f72bcfd5271cd50c9`:

- [Pi sample, lines 41–52](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/sample_submissions/pi-opus/README.md#L41-L52)
  states that Argon is missing from Pi 1.1.0's catalog, recommends these token
  limits, and advises leaving `reasoning` unset. Setting it to true causes Pi
  to emit a token-based thinking budget, which Argon rejects.
- [Model guidance, lines 150–170](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/models.md#L150-L170)
  describes Argon's thinking behavior and token limits. The same document
  lists sponsored eligibility and supported APIs in its model table. A token `thinkingBudget`, including
  zero, is rejected with HTTP 400.
- [Proxy default effort, lines 227–269](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/model_proxy/effort_default.py#L227-L269)
  supplies HIGH when neither a thinking budget nor a thinking level is sent.

These references informed source preparation. **CLI `high` and an absent
`reasoning` field in `models.json` do not prove the outgoing API request shape.**
No wire request was generated or inspected. The text-only fallback has not
been widened to images, audio, video or other modalities. It can limit tasks
requiring direct visual input even if the underlying model supports more.

## Conditions and exact source identifiers

- Upstream template: `22c26a93a9e4974b16e4351faab0e860ff9fb24f`.
- Original project runtime base: `5d9f2dde9035fb2bdd6d69cbc39b976f0800ba7d`.
- Documentation-only base: `7c728650703305326c75a3df8d1e4b5b25bea49e`.
- Subsequent published logging base: [9bd26bd1557c9d2cc334848288cbbd12d3a701fa](https://github.com/moruku36/ple-agent-harness/commit/9bd26bd1557c9d2cc334848288cbbd12d3a701fa),
  on draft [PR #1](https://github.com/moruku36/ple-agent-harness/pull/1).
  The source snapshot used here has **no local `.git` directory**. These are
  source references, not a claimed locally verified HEAD or the commit of
  this Argon change. Publication is handled separately from these checks.
- Pre-change `harness.py` SHA-256:
  `852889215f6782d1b3df7662d0dca48fb27ab05d8e412624ab8427e90b365a08`.
- Pre-change `submission.yaml` SHA-256:
  `51402c8af49dbea32aeb54847d417554d1e9881dc7717296cdd78352d7fa07d6`.
- Python 3.12.14 on Linux x86-64. Available `websockets` is **16.0**, not the
  pinned **15.0.1**. It is imported for the mock tests but not used for a live
  WebSocket connection. No dependency installation or update was performed.
- Pi remains pinned to `@earendil-works/pi-coding-agent` **1.1.0**. Neither Pi
  nor its model catalog probe was executed; catalog membership was mocked.
- Standard-library `unittest` and mocks; local temporary directories and
  synthetic `.invalid` endpoints only. No credentials, competition inputs,
  dataset revision, model revision returned by an API, or judge was used.
- Exactly one focused new-suite run and one final combined regression run.
  The runs are sequential; no benchmark retries or token-spending budget.
  No model/judge/provider calls or metered provider usage were initiated.
  Billing was not measured; this is not a live-cost experiment.
- No Docker/GPU execution, downloads, external API/network requests,
  credential creation/configuration, data-term acceptance, or submission
  was performed by this experiment.

Final tested source/configuration SHA-256 values:

```text
967bdb0150c4cf6992ff9958b0d7ab15ceaaf7895573e65c509140f3f65ed48c  harness.py
06a971a9e17f04b4b637e8def6318c53205cd6206c326f1d601ee67810d87503  submission.yaml
bd17f5da19a67094829bb268fc6f44c9badacc8d6bf3bc22ce59f1fb6dad8520  tests/test_argon_config.py
5185c66dd1dd16d87d2bc11379368eb3ba485f761c13efc804990387738c8342  taskbridge.py
003639c01c11d4ff40540182f5d5e432db29b03568392c8a37922df8f455cb17  tests/test_logging_sentinels.py
8f7872ae7c9695b9afbb3b2070810b86788d347eaf1a1a202a575f5a627e6ad5  package.json
47f90f401e029537bbf1245eb5effd5dbd85d81fef18f88d8f4cba7eb3891093  package-lock.json
9ec828179a682425537349fb41440b48a47b1ef006b7b3e1d1542566d3ec6943  requirements.txt
```

`taskbridge.py` and the logging test hashes match the prior
[logging experiment](2026-11-13-logging-sentinels.md). No logging test was
removed or changed. Historical hashes in that note describe its earlier
tested source and should not be substituted for this changed `harness.py`.

## Procedure and observed results

From the repository root, the focused command was:

```sh
python -B -m unittest discover -s tests -p 'test_argon_config.py' -v
```

Observed result, exit code 0:

```text
Ran 7 tests in 0.037s
OK
```

The seven cases cover the submission declaration; native Google configuration;
OpenAI-compatible fallback configuration; unchanged other-model fallback;
unchanged recognized-model catalog behavior; high CLI selection on both Argon
routes; and the inherited max CLI default for other models. Tests inspect
generated files and captured command arguments. All process execution and
relay startup are mocked. A synthetic assistant event checks the final-response
path without starting Pi.

The final combined command is:

```sh
python -B -m unittest discover -s tests -v
```

Observed final combined result, exit code 0:

```text
Ran 23 tests in 0.070s
OK
```

All 7 new cases and all 16 existing logging cases passed. There were zero
failures, errors or skipped tests. No source or test code was changed after
this final combined run; this note was updated with its result.

## Failures, limits and next decision

Both runs had no failures, errors or skipped tests. The prior logging
experiment separately records its earlier failures and negative control.
These timings measure local unit tests, not model performance.

Unverified stages include the pinned dependency runtime, the Pi 1.1.0 request
serializer and model catalog, live API authentication/access, actual thinking
level and token-budget payloads, model tool calls and token accounting, direct
image input, real process cancellation, official kit checks, development
evaluation, hidden evaluation and submission acceptance. No score or official
evaluation export was created or reused.

The user's constraint is to avoid GCP charges. The official local Vertex proxy
bills the configured user's GCP project. Sponsored evaluation injects a key
restricted to the declared model; it does **not** show that this user has free
local access. No no-charge participant development allocation or free judge
route has been verified. The default development judge is Claude Opus 5.5 and
can add a separate charge. Changing this entry's model does not change that
judge or supply credentials.

Keep live execution blocked until a genuinely no-charge route for both the
model and any required judge is verified and the separate setup/data/run
permissions are satisfied. Source publication is a separate action and does
not authorize calls, costs, merging, or competition submission. Once a
permitted route exists, inspect the exact Pi-generated request in the pinned
environment before a bounded official check. Do not infer wire compatibility
from these mocks or assume the sponsorship covers local evaluation.

## 日本語要約

- 提出設定を `google-cloud/gemini-4-argon` に変更し、Argon の CLI 思考設定を
  `high` にした。Pi 1.1.0 のカタログにない場合だけ、文脈長1,048,576、
  出力上限65,536を使う。他モデルの既定値と従来のログ保護は維持した。
- `reasoning` は設定していない。true にすると Argon が拒否するトークン予算を
  Pi が送るため。入力はテキストのみに据え置き、画像等への対応は未確認。
- 新規7件の合成・モックテストは成功。最終の合同回帰テストも23件すべて成功し、
  従来のログ保護テスト16件を含む。所要時間はそれぞれ0.037秒と0.070秒。
  テストは設定ファイルと CLI 引数を確認するもので、実際の API 通信形式や
  モデル動作を確認したものではない。新規テストの失敗・エラー・スキップはない。
- Python 3.12.14、websockets 16.0で確認した。指定の15.0.1とは異なる。
  依存関係のインストール、Pi・Docker・GPU・実モデル・評価用 judge の実行、
  データ取得、認証情報の設定、提出は行っていない。大会スコアはない。
- GCP課金を避ける方針を維持する。公式ローカルプロキシは利用者の GCP に課金される。
  本番評価の支給キーから、無料の開発利用権があるとは判断しない。
  無料のモデル経路・judge 経路・実際の利用権はいずれも未確認。
  開発評価の既定 judge は Claude Opus 5.5で、別料金の可能性がある。
- 次は無料経路と必要な許可の確認。公開への許可は、API実行・課金・マージ・大会提出の
  許可ではない。公開済みの基点と検証したファイルのハッシュを本文に記録した。
