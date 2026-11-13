# Pinned Pi and Google SDK: static request-path trace

Status: static review completed on November 13, 2026 (UTC).
Evidence class: exact-version source inspection, **not executed serialization**.

## Question

What does the intended custom-model registration path construct for Argon when `reasoning` is omitted and the CLI requests `high`? Which assumptions remain after package installation failed?

## Provenance and conditions

- Entry reference: [775f1b30128cb93e23998a3b02da1c1651c28ac4](https://github.com/moruku36/ple-agent-harness/commit/775f1b30128cb93e23998a3b02da1c1651c28ac4).
- Official Pi tag `v1.1.0` resolves to `abe508e1b89912adde45528136c3221eb69acdd7`. The manifests identify the expected package names and version 1.1.0: [coding-agent](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/coding-agent/package.json#L1-L4), [agent-core](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/agent/package.json#L1-L4), [pi-ai](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/ai/package.json#L1-L4).
- Pi's AI package pins `@google/genai` 2.21.0, matching the entry lockfile. Official SDK tag `v2.21.0` resolves to `27af8977598edb68ffccadcd34fae967205a8740`; its [manifest](https://github.com/googleapis/js-genai/blob/27af8977598edb68ffccadcd34fae967205a8740/package.json#L1-L8) confirms the package and version.
- The tags and source files were read through GitHub. No package installation, Pi/SDK execution, network transport test, provider call, task data, credentials or score was involved.
- npm tarball contents and their equivalence to the repository's compiled output were not independently verified. The [failed package-preparation experiment](2026-11-13-argon-offline-wire-prerequisites.md) remains a separate result.

## Registered-model thinking path

1. The entry writes an explicit Argon model into `models.json` after a negative catalog probe. Pi's [provider composition](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/coding-agent/src/core/provider-composer.ts#L210-L248) registers the custom model, preserving input/context/output metadata. Omitted `reasoning` defaults to false.
2. Requested CLI `high` is clamped to the model's supported level. A model marked non-reasoning supports only `off`: see [session setup](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/coding-agent/src/core/sdk.ts#L253-L278) and [clamping](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/ai/src/models.ts#L1222-L1253). [Agent core](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/agent/src/agent.ts#L467-L477) converts `off` to undefined reasoning.
3. The Google provider's [simple stream path](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/ai/src/api/google-generative-ai.ts#L305-L345) selects disabled thinking, but [both thinking-configuration branches](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/ai/src/api/google-generative-ai.ts#L403-L413) also require truthy `model.reasoning`. With false, neither branch constructs `thinkingConfig`. In particular, it does not construct budget zero merely because the session level is `off`.
4. SDK 2.21.0 [copies thinkingConfig only when present](https://github.com/googleapis/js-genai/blob/27af8977598edb68ffccadcd34fae967205a8740/src/converters/_models_converters.ts#L1722-L1727), [maps config to generationConfig](https://github.com/googleapis/js-genai/blob/27af8977598edb68ffccadcd34fae967205a8740/src/converters/_models_converters.ts#L2036-L2072), and [JSON-serializes the converted body](https://github.com/googleapis/js-genai/blob/27af8977598edb68ffccadcd34fae967205a8740/src/models.ts#L850-L872). No default token budget is inserted on this inspected path.

Thus the source supports omission of **both thinkingBudget and thinkingLevel** on the intended registered native-Gemini path. It does not support claiming that CLI `high` is sent directly to Argon. The [official gateway/proxy](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/model_proxy/effort_default.py#L227-L269) supplies HIGH when neither field is present. Actual gateway execution is still untested.

## Important alternate path

The result depends on successful custom-model registration. Pi's [CLI-only unknown-model fallback](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/coding-agent/src/core/model-resolver.ts#L570-L595) can force `reasoning: true` when a non-off thinking level is requested.

Argon does not match this Pi version's discrete-level model patterns. With reasoning enabled, the [provider fallback](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/ai/src/api/google-generative-ai.ts#L431-L470) can construct budget -1 for enabled thinking; [disabled thinking](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/ai/src/api/google-shared.ts#L67-L110) can construct budget zero. The kit says Argon rejects token budgets. Do not generalize the safe registered path to an unregistered CLI-only invocation.

## Images and backend selection

- Pi's [Google tool-result conversion](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/ai/src/api/google-shared.ts#L284-L337) discards image blocks when `model.input` excludes `image`. For the text-only entry at the reference commit, this is a source-level limitation. An image-only successful tool result can become an empty output string. This is not a measured task failure.
- Pi's [GoogleGenAI construction](https://github.com/earendil-works/pi/blob/abe508e1b89912adde45528136c3221eb69acdd7/packages/ai/src/api/google-generative-ai.ts#L348-L366) passes key/base URL/headers but does not explicitly choose `vertexai: false`.
- SDK [backend resolution](https://github.com/googleapis/js-genai/blob/27af8977598edb68ffccadcd34fae967205a8740/src/node/node_client.ts#L48-L87) can read `GOOGLE_GENAI_USE_ENTERPRISE` and `GOOGLE_GENAI_USE_VERTEXAI` from the process environment. An inherited flag can alter backend selection. No such runtime switch or charge was observed here; it is a conditional routing risk that warrants a fail-closed native-Gemini guard.

## Limits and decision

This inspection resolves source-level branches, not end-to-end behavior. Custom registration, the actual selected executable, compiled-package equivalence, transport containment, model access and request acceptance must still be tested in the pinned runtime. A future source change requires its own focused verification.

Continue with a small image-metadata correction only after checking exact-model capability evidence, and reject unsafe/ambiguous cloud-backend flags before a native-Gemini process starts. Neither change establishes a free model or judge route. Live calls remain blocked until no-charge access and the necessary permissions are verified.

## 日本語要約

- Pi 1.1.0 と Google SDK 2.21.0 の公式固定ソースを追跡した。パッケージの実行や実API呼び出しはしていない。
- Argon が `models.json` で正しく登録される経路では、未指定の `reasoning` は false となり、CLI の high は内部で off に制限される。ただし予算0は送らず、thinkingBudget/Level の両方を構築しない。主催者側の既定HIGHに依存する形で、実通信は未確認。
- 登録に失敗して CLI の未知モデル用経路へ入ると、拒否されるトークン予算を構築し得る。この経路を混同しない。
- テキスト専用設定では画像ツール結果が除去される。SDKは環境フラグによりVertex/Enterprise側へ切り替わり得るため、対応する設定修正と誤ルーティング防止が必要。
- これはソース上の条件分岐の確認であり、画像処理の実績、課金の発生、無料枠、スコアを示さない。
