# Gemini 4 Argon: offline wire-test prerequisites

Status: **package preparation failed; static review completed; wire test not run**.
Evidence class: source/lockfile inspection and a failed dependency installation.
Date: November 13, 2026 (UTC).

## Question and result

Can the actual locked Pi 1.1.0 client generate a native Gemini request for
Argon without making a network connection, so that its thinking fields and
direct image handling can be inspected?

**Not established.** Node and npm are available, but the pinned Pi packages
are not installed. An isolated, script-disabled installation failed while
resolving the official npm registry. No Pi serializer, model, judge or
competition task was executed. In particular:

- Presence or absence of a wire `thinkingBudget`: **unresolved**.
- Presence, absence or value of a wire `thinkingLevel`: **unresolved**.
- Whether image content is omitted, rejected or otherwise handled by Pi:
  **unresolved**.
- The existing text-only fallback is confirmed in source. No modality or
  runtime configuration was changed.

This is not a repetition of the earlier 23 mock tests. Those tests were not
rerun and their previous success does not resolve these wire questions.

## Conditions and identifiers

- Source reference: [main commit
  775f1b30128cb93e23998a3b02da1c1651c28ac4](https://github.com/moruku36/ple-agent-harness/commit/775f1b30128cb93e23998a3b02da1c1651c28ac4),
  tree `e871ddcb423ecdece48ce6c5723d9c4e8efa184a`, independently checked
  before this work. The local source snapshot has no `.git` directory.
- Official kit guidance reference:
  `8320f0402fdca9f42476607f72bcfd5271cd50c9`, as recorded in the
  [configuration experiment](2026-11-13-argon-config.md).
- Linux x86-64, Node **24.22.1**, npm **11.9.0**, Python **3.12.14**.
  No `pi` executable was found on PATH; the source snapshot initially had no
  `node_modules`. The inspected local package trees contained no pinned Pi
  1.1.0 runtime. An unrelated Google SDK 2.27.0 and Pi TUI 1.0.3 were not used.
- The lockfile has 146 dependency entries. Every nonempty `resolved` URL uses
  `https://registry.npmjs.org/`. Relevant exact locked versions are
  `@earendil-works/pi-coding-agent` **1.1.0**, `pi-agent-core` **1.1.0**,
  `pi-ai` **1.1.0**, and `@google/genai` **2.21.0**. Caret ranges in package
  dependency declarations do not override those lockfile versions.
- Only `package.json` and `package-lock.json` were copied into a new sibling
  preparation directory. It had a new HOME, new npm cache, and empty user and
  global npm configuration files. The shell environment passed to npm was
  cleared except for PATH and that isolated HOME. No existing user config,
  authentication files or credentials were read.
- Lifecycle scripts, audit and funding requests were disabled. No dependency
  pins were changed. Installation was one corrected attempt after one
  configuration error, with npm fetch retries set to zero and a 20-second
  fetch timeout. There was no retry after the network failure.
- No provider endpoints, real prompts, hidden tasks, datasets, credentials,
  GCP project, GPU, Docker, judge or submission were used. Package-registry
  requests were attempted; this experiment was not wholly network-free.
  No model/judge calls or metered provider usage were initiated. Billing was
  not measured.

Source/configuration SHA-256 values, unchanged by this experiment:

```text
967bdb0150c4cf6992ff9958b0d7ab15ceaaf7895573e65c509140f3f65ed48c  harness.py
06a971a9e17f04b4b637e8def6318c53205cd6206c326f1d601ee67810d87503  submission.yaml
d57fe9024b30b6cf6eb57eb18fcfd2af5177f682c73d90745df9b70216d84d5e  task-tools.ts
5185c66dd1dd16d87d2bc11379368eb3ba485f761c13efc804990387738c8342  taskbridge.py
8f7872ae7c9695b9afbb3b2070810b86788d347eaf1a1a202a575f5a627e6ad5  package.json
47f90f401e029537bbf1245eb5effd5dbd85d81fef18f88d8f4cba7eb3891093  package-lock.json
9ec828179a682425537349fb41440b48a47b1ef006b7b3e1d1542566d3ec6943  requirements.txt
```

The lockfile retains npm SHA-512 integrity values for all relevant packages.
They identify the intended tarballs, not downloaded or executed bytes.

## Procedure and observed failures

1. Read `AGENTS.md`, the earlier Argon experiment, the lockfile, `harness.py`
   and the image-related portions of `task-tools.ts`. Inventory Node/npm and
   local dependency availability. This was static inspection, without imports
   or execution of the Pi packages.
2. Create the isolated preparation directory and copy the two package files.
   An initial npm invocation set both user and global config to `/dev/null`.
   It exited **1** before config resolution with:

   ```text
   Exit prior to config file resolving
   double-loading config "/dev/null" as "global", previously loaded as "user"
   ```

3. Correct that local setup error by using two distinct empty files. From the
   preparation directory, the actual corrected command was:

   ```sh
   env -i PATH="$PATH" HOME="$PWD/home" npm ci \
     --ignore-scripts --no-audit --no-fund \
     --registry=https://registry.npmjs.org \
     --userconfig="$PWD/user.npmrc" --globalconfig="$PWD/global.npmrc" \
     --cache="$PWD/cache" --fetch-retries=0 --fetch-timeout=20000
   ```

   It exited **1**. npm reported `Exit handler never called!`; its debug log
   showed `EAI_AGAIN` on registry requests. That is the observed DNS-resolution
   failure, not evidence that the requested package versions do not exist.
   npm also attempted its update-notifier metadata request at
   `https://registry.npmjs.org/npm`; that failed with the same error. All
   tarball URLs came from the unchanged lockfile. Nothing was installed or
   updated. A subsequent file count found **zero regular files** under the
   attempted `node_modules`, and all four relevant package manifests were
   absent. The copied and original lockfile hashes still matched.
4. Stop package retrieval. No alternative registry, network-route bypass,
   authentication, unpinned replacement or provider probe was attempted.
   Produce a local prerequisite inventory and this experiment note.

The first final documentation check used `Path(".").parent` rather than the
absolute working directory and failed to locate the sibling inventory file.
It did not test or change runtime code. The corrected check uses `Path.cwd()`.

Local-only evidence is retained outside the source snapshot in the sibling
`offline-wire-runtime` directory: `npm-ci.log`, `npm-ci-corrected.log`, the npm
debug log and `prerequisite-audit.json`. None is a competition artifact or
benchmark export. Log SHA-256 values:

```text
250e369d730a46c4d41df37449a5c58c169b4b1d2ab546951a8bed0285805a95  initial setup output
34b3757a791050843731a918ef47f21d53450c31c2a73c0a0cfbb23f378e3aae  corrected install output
8d22c2a62eceaa08d82790fbbf72d554b6b1a0cd3f581b0330e563b35eecf375  corrected install debug log
```

## What static inspection does and does not establish

### Thinking and route

`harness.py:99-116` selects the native Google API when
`GOOGLE_GEMINI_BASE_URL` is supplied, provided the higher-priority Anthropic
variable is absent. It sets `api: google-generative-ai`, appends `/v1beta`
and names the Gemini API-key environment variable. The alternate route is
OpenAI-compatible; the two routes must not be conflated.

`harness.py:76-81,165-173` adds Argon's fallback when the catalog probe does
not recognize it: 1,048,576 context tokens, 65,536 output tokens and text-only
input, with no `reasoning` property. `harness.py:286-303` selects CLI thinking
`high`. The harness does not serialize the provider request. Conversion of
these settings into a Pi model, resolution of CLI thinking for an uncatalogued
model, and the subsequent Google SDK request serialization all remain beyond
the inspected source boundary.

The previously checked official
[Pi sample](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/sample_submissions/pi-opus/README.md#L41-L52)
recommends these Argon token limits and leaving `reasoning` unset because true
emits a rejected token budget. The official
[gateway default](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/model_proxy/effort_default.py#L227-L269)
supplies HIGH **if neither a thinking budget nor a thinking level is supplied**.
That condition cannot yet be verified for this client. Therefore neither
"Pi sends HIGH" nor "the gateway definitely selects HIGH" is a result of
this experiment. The
[Argon guidance](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/models.md#L150-L170)
also warns that a token budget, including zero, is rejected and that native
MAX is weaker than high.

The executable selection is another future check: `harness.py:54` prefers
`pi` from PATH before the source-local executable. A later runtime test must
identify the actual executable and dependency versions, not infer them from
the lockfile alone. No wrong executable was found or executed here.

### Image path

There is a real source-level capability mismatch to investigate:

- `task-tools.ts:35-40` recognizes PNG, JPEG, GIF and WebP extensions.
- `task-tools.ts:147-151` obtains file bytes through the task relay and decodes
  base64. `task-tools.ts:161-168` supplies these bytes and MIME detection to
  Pi's `createReadToolDefinition`.
- Argon's fallback metadata nevertheless advertises only text input.

Thus the harness has an image-aware read path, but does not advertise image
input for the fallback model. Whether that materially blocks a specific task
depends on the unavailable Pi read-tool/conversation/serializer behavior and
the authorized gateway. No image was read through a live relay or sent to a
model. The cited Pi sample paragraph supplies no recommendation to widen
Argon's modalities. Direct image support is not established; keep the current
metadata until both official evidence and a synthetic pinned-client test
support a change.

## Decision and next gates

No confirmed runtime bug was established, so no runtime change was made.
The only source-snapshot addition is this note. No new speculative serializer
test was added against an unavailable package, and no source was published.

1. Obtain the exact lockfile packages through an authorized official npm
   registry route or a verified permitted package transfer. Preserve pins,
   disable lifecycle scripts and use isolated config/cache/HOME. Also disable
   npm's update notifier in future setup. An empty `node_modules` directory is
   not a successful installation.
2. Inspect the installed Pi and Google SDK source first. Build a synthetic
   in-memory transport test that fails closed before any network-capable
   import or transport call, uses only `.invalid` endpoints and dummy keys,
   and never reads existing authentication. A fetch mock alone is not enough
   if the actual dependency can use another transport. Verify that transport
   containment before executing the real locked serializer.
3. Capture the actual JSON request, distinguishing missing fields from zero
   or explicit values. Test the current unset-reasoning/high configuration
   and a synthetic image case. A reasoning-enabled negative control may be
   useful offline; do not send it to Argon. Distinguish Pi CLI/model-resolution
   behavior, provider serialization, SDK wire serialization and gateway
   defaults rather than treating one stage as proof of the others.
4. Live execution remains a separate gate: verify a genuinely no-charge model
   route and any required judge route, plus setup/data/run permissions.
   Sponsored evaluation does not establish free local GCP access. Official
   validation/evaluation and all scores remain unrun by this experiment.

The known Python `websockets` 16.0 versus pinned 15.0.1 discrepancy remains
unchanged. This work does not validate process cancellation, the full pinned
runtime, tool execution, request acceptance, billing or competition acceptance.

## 日本語要約

- Pi 1.1.0 の実際の送信形式をオフラインで調べるため、Node 24.22.1、npm
  11.9.0と依存関係を確認した。指定された Pi 一式と Google SDK 2.21.0は未導入。
- 隔離した HOME・npm設定・キャッシュで、スクリプトを無効にして固定依存関係の
  導入を試みた。最初は設定ファイルの重複指定で失敗。修正後も公式 npm レジストリの
  名前解決が `EAI_AGAIN` で失敗し、導入されたファイルは0件。別経路での再試行や
  バージョン変更はしていない。
- 実際の `thinkingBudget` の有無、`thinkingLevel` の値、画像の送信処理は未確認。
  CLI の `high` と設定上の `reasoning` 未指定だけでは証明にならない。
  ゲートウェイの HIGH 既定値も、両フィールドを送らない場合という条件付き。
- 読み込みツールには PNG/JPEG/GIF/WebP の画像経路がある一方、Argon の代替設定は
  テキスト専用。この不一致は要確認だが、画像が実際に除去・拒否されるとはまだ言えない。
  公式根拠と固定クライアントの合成テストなしに画像対応を広げていない。
- 既存23件のモックテストは再実行していない。変更はこの実験ノートのみ。モデル・judge・
  GCP・Docker・実データ・大会評価・提出は実行せず、スコアはない。
- 次は許可された経路で固定パッケージを取得し、通信を確実に遮断する合成テストで送信JSONを
  確認する。実モデルの実行には、無料経路と必要な許可の確認が別途必要。
