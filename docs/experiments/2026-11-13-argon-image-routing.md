# Gemini 4 Argon: image metadata and native-backend guard

Status: **local source changes and synthetic/mock regression completed**.
Date: November 13, 2026 (UTC).
Evidence class: generated configuration and mocked process boundaries, not
executed Pi/SDK serialization or live model behavior.

## Result and scope

Two source-backed changes were made in `harness.py`:

1. Argon's uncatalogued-model fallback now declares `input: ["text", "image"]`.
   The existing context window **1,048,576**, output limit **65,536**, omitted
   `reasoning`, and CLI `--thinking high` are unchanged. No audio, video or
   other modality was added. Other models retain their previous fallback
   metadata, catalog behavior and thinking defaults. The Argon fallback is
   shared by the native Google and existing OpenAI-compatible routes.
2. On the native Google route only, fail closed if either inherited SDK cloud
   backend flag is enabled or ambiguous. Both the catalog probe and the Pi
   session receive explicitly disabled flags in private environment copies.
   Non-Google routes retain their original flag values and provider priority.

The image change corrects declared capability. It does **not** establish real
image transmission, tool-result serialization, image understanding or improved
task performance. The guard prevents these inherited Vertex/Enterprise
selectors from enabling a cloud backend on the supported native route. It
does **not** certify a free Gemini endpoint or prevent every possible charge.
**Live calls remain blocked** until genuinely no-charge access and the
necessary permissions are separately verified.

Only `harness.py`, `tests/test_argon_config.py` and this new note were changed
by this experiment. Google copyright and Apache license notices were preserved,
and a modification notice was added. No publication, submission, dependency
change or user-machine setting change was performed.

## Evidence and immutable references

The following exact-model documentation was verified in the preceding research
and supplied as evidence for this change. These model pages are mutable web
references, not immutable versioned snapshots:

- [Google AI Studio: Gemini 4 Argon](https://aistudio.google.com/docs/models/gemini-4-argon),
  reached from the official ai.google.dev model page, documents image input.
- [Google Cloud: Gemini 4 Argon](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-argon)
  independently documents image input for the exact model. This citation is
  capability evidence, not authorization to use that billed backend.

Exact-version source references are immutable:

- Pi `v1.1.0`, commit `abe508e1b89912adde45528136c3221eb69acdd7`:
  [Google tool-result conversion, lines 284–337](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/ai/src/api/google-shared.ts#L284-L337)
  drops image blocks when `model.input` excludes `image`.
- The same Pi revision's
  [GoogleGenAI construction, lines 348–366](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/ai/src/api/google-generative-ai.ts#L348-L366)
  does not explicitly disable the SDK's Vertex/Enterprise backend selection.
- Google SDK `@google/genai` **2.21.0**, commit
  `27af8977598edb68ffccadcd34fae967205a8740`:
  [Node backend resolution, lines 48–87](https://github.com/googleapis/js-genai/blob/27af8977598edb68ffccadcd34fae967205a8740/src/node/node_client.ts#L48-L87)
  reads `GOOGLE_GENAI_USE_ENTERPRISE` and `GOOGLE_GENAI_USE_VERTEXAI` when
  backend selection is not explicitly supplied.
- Official kit reference `8320f0402fdca9f42476607f72bcfd5271cd50c9`:
  [Pi sample guidance, lines 41–52](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/sample_submissions/pi-opus/README.md#L41-L52)
  recommends Argon's limits and leaving `reasoning` unset. This experiment
  does not alter the existing thinking configuration.

The preceding [static request-path trace](2026-11-13-pi-static-request-trace.md)
records the detailed source branches and their limitations. The sources were
not fetched again or executed in this experiment. Locally inspected
`taskbridge.Relay.env()` copies `os.environ` before adding relay variables,
which explains how inherited selectors can reach Pi.

## Strict environment policy

For each of `GOOGLE_GENAI_USE_ENTERPRISE` and `GOOGLE_GENAI_USE_VERTEXAI`:

- Accept a missing variable or exactly the lowercase string `false`.
- Reject every other present value, including `true`, `1`, `0`, an empty
  string, uppercase/case variants, surrounding whitespace and unknown strings.
  This is intentionally stricter than interpreting arbitrary false-like values.
- Check both the current inherited environment and the supplied subprocess
  environment. A safe value in one cannot mask an unsafe value in the other.
- Validate all flags before setting both to `false` in the returned copy.
  Do not silently turn an unsafe inherited value into a safe one and proceed.
- Reject with the fixed error `pi: native_google_cloud_backend_flag_rejected`.
  No raw value, URL, key or task content is included in this error.

`configure()` validates before writing configuration or calling `in_catalog()`
and passes a safe copy to that probe. `solve()` starts with its own copy of the
relay environment, then uses the provider returned by `configure()` to prepare
the safe session environment before `run_process()`. Neither the input mapping
nor `os.environ` is mutated by the guard. No credentials are read or set by the
guard, and no operating-system, browser, account or network settings change.

This protects those two environment selectors on the supported harness path.
It does not validate the base URL, guarantee which executable is found on PATH,
prove the selected package bytes, control a separately invoked client, approve
authentication, establish sponsorship or restrict all possible billing paths.
The ordinary Gemini API may itself be paid. No endpoint allowlist or automatic
claim of free access was introduced.

## Conditions and source identifiers

- Published source reference:
  [main `775f1b30128cb93e23998a3b02da1c1651c28ac4`](https://github.com/moruku36/ple-agent-harness/commit/775f1b30128cb93e23998a3b02da1c1651c28ac4),
  verified against remote main. The local snapshot has no `.git`.
  This is the pre-change reference, not a commit containing these local fixes.
- Pre-change `harness.py` SHA-256:
  `967bdb0150c4cf6992ff9958b0d7ab15ceaaf7895573e65c509140f3f65ed48c`.
- Pre-change `tests/test_argon_config.py` SHA-256:
  `bd17f5da19a67094829bb268fc6f44c9badacc8d6bf3bc22ce59f1fb6dad8520`.
- Python **3.12.14**, Linux x86-64, available `websockets` **16.0** rather
  than pinned **15.0.1**. No real WebSocket connection was made.
- Pi remains pinned to **1.1.0** and the Google SDK to **2.21.0**. Their
  packages remain unavailable after the previously recorded npm DNS failure.
  No installation retry, substitute dependency or Pi invocation was attempted.
- Tests use standard-library `unittest`, synthetic `.invalid` endpoints,
  controlled environments, temporary directories and mocks. Relay startup,
  catalog subprocesses and Pi session execution are mocked. No credential
  values, competition inputs or real task artifacts were inspected or used.
- No network calls, provider/model/judge calls, GCP, Docker/GPU execution,
  data downloads, credential setup, permission changes, terms acceptance or
  submission were initiated. Billing was not measured.
- The earlier official `kit.spec.load` check is a separate YAML-parser result.
  It was not rerun here and does not validate this changed runtime or its API
  requests. No official evaluation or score was produced by these tests.

Final tested SHA-256 values:

```text
a74d7d54e8624c13175f71deadde87ae6597a0c85732dda45ebad766193e6ec0  harness.py
ef92d8ebd0e3913a59619a7a23573124fb3a6a013e8fc13724283d1266b74844  tests/test_argon_config.py
003639c01c11d4ff40540182f5d5e432db29b03568392c8a37922df8f455cb17  tests/test_logging_sentinels.py
5185c66dd1dd16d87d2bc11379368eb3ba485f761c13efc804990387738c8342  taskbridge.py
06a971a9e17f04b4b637e8def6318c53205cd6206c326f1d601ee67810d87503  submission.yaml
d57fe9024b30b6cf6eb57eb18fcfd2af5177f682c73d90745df9b70216d84d5e  task-tools.ts
8f7872ae7c9695b9afbb3b2070810b86788d347eaf1a1a202a575f5a627e6ad5  package.json
47f90f401e029537bbf1245eb5effd5dbd85d81fef18f88d8f4cba7eb3891093  package-lock.json
9ec828179a682425537349fb41440b48a47b1ef006b7b3e1d1542566d3ec6943  requirements.txt
```

Only the first two hashes changed from their pre-experiment values. Existing
logging tests, taskbridge, submission configuration, task tools and dependency
files retain their earlier hashes.

## Procedure, results and recorded failure

One focused command was run:

```sh
python -B -m unittest discover -s tests -p 'test_argon_config.py' -v
```

Result: **11 tests passed in 0.106 seconds**, exit code 0.

The first combined regression command was:

```sh
python -B -m unittest discover -s tests -v
```

Result: **27 tests ran in 0.141 seconds: 26 passed, 1 error**, exit code 1.
The existing `test_no_reply_error_does_not_echo_subprocess_stderr` mocks
`configure()` and does not provide `MODEL_BASE_URL`. An unnecessary new early
`provider()` call in `solve()` bypassed that mocked boundary and raised
`KeyError: 'MODEL_BASE_URL'`. The intermediate harness SHA-256 was
`7a029759a75dbdd18312d52fe52ba98ef09712bab0d3a8827e24ee580a1e3d83`;
the test file already had its final hash above.

Corrected only `harness.py`: keep the pre-catalog guard in `configure()` and
prepare the final process environment using its returned provider. The
existing logging test was not weakened or edited. The corrected final
combined run used the same combined command and observed:

```text
Ran 27 tests in 0.140s
OK
```

All **11 configuration/routing tests and 16 existing logging tests** passed,
with zero failures, errors or skipped tests in the final run. There was one
focused run, one failed combined run and one corrected final combined run.
No source or test code changed after the successful final run; only this note
was added. These are unit-test timings, not model performance measurements.

Coverage includes generated Argon image metadata and unchanged token/thinking
settings; other-model defaults; both absent and exact-false flags producing
explicitly safe child flags; enabled, ambiguous and conflicting values rejected
before catalog or session process calls; content-free errors; unmodified
inherited and supplied environments; and unchanged non-Google flag handling
and Anthropic-before-Google provider priority.

## Limits and next step

The preceding source trace supports the reason for these fixes, while these
tests establish Python configuration and boundary behavior only. They do not
execute Pi's catalog or model registration, the image serializer, SDK transport,
gateway behavior, token accounting, model reasoning or image understanding.
Actual executable selection and compiled-package equivalence remain unverified.
The `websockets` version mismatch is unresolved.

When exact packages become available through an authorized route, validate the
actual pinned client in a strictly contained, network-free synthetic transport
test before considering live use. Keep live model and judge execution blocked
until a genuinely no-charge route and the separate setup/data/run permissions
are verified. The new flag guard is not a replacement for that gate. No existing
score or official development export applies to this changed harness.

## 日本語要約

- Argon の代替設定をテキスト＋画像に修正した。公式の画像対応資料と Pi 1.1.0 の
  固定ソースが根拠。文脈長1,048,576、出力上限65,536、`reasoning` 未指定、CLI の
  `high` は維持した。他モデルの既定値は変更していない。画像の実送信・理解は未検証。
- ネイティブ Gemini 経路では、Vertex/Enterprise を選ぶ2つの環境変数について、
  未設定か小文字の `false` だけを許可する。それ以外は Pi・カタログ処理の前に停止。
  親環境と子プロセス用環境の両方を確認し、子プロセス用のコピーだけで両方を
  `false` にする。元の環境・認証情報・端末設定は変更しない。他経路の扱いは維持。
- この保護は環境変数による Vertex/Enterprise 選択を防ぐもので、無料の Gemini
  接続先や課金ゼロを保証しない。通常の Gemini API でも課金され得る。無料経路と
  必要な許可が確認できるまで実 API・judge 実行は引き続き停止する。
- 対象11テストは成功。最初の合同実行は既存ログテストのモックとの境界で1エラー。
  原因は早すぎる provider 判定で、harness.py だけを修正。最後は27件すべて成功し、
  従来のログ保護16件も維持した。失敗・修正内容・ハッシュ・実行時間を本文に記録。
- Pi/SDK の実行、通信、GCP、モデル・judge、Docker/GPU、データ取得、認証設定、
  公開、提出は行っていない。websockets 16.0と指定15.0.1の差は未解消。
  次は固定クライアントの通信を遮断した合成検証であり、今回の成功は大会スコアではない。
