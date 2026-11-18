# 2026-11-18: Local Qwen CPU integration and typed-tool isolation

Status: completed; several negative results, with one narrowly successful synthetic I/O probe.
Evidence class: real local runtime tests, local dev evaluation, and synthetic tests. **Not an official competition result.**

## Question and hypothesis

Can the existing CPU-hosted Qwen3-1.7B-Q8_0 complete the local PLE integration path, and can narrower tools reduce the navigation failures observed after transport repair?

This is a separate local-research lineage. It does not establish eligibility of a competition entry, an Argon result, or submission readiness.

## Conditions

- UTC date: 2026-11-18. Local-dev attempts below ran approximately 09:32–09:59 UTC; synthetic isolation followed.
- Official kit commit: `8320f0402fdca9f42476607f72bcfd5271cd50c9`.
- Dataset revision: `b3857a3fea39a695e18f845d4a88f29442e96e75`. One already-accessible checks-graded development task was selected. Task contents, identity-specific logic, grader content and raw trajectories are excluded from this note.
- Host: existing Linux x86_64 CPU machine, approximately 32 GB RAM. Local model: Qwen3-1.7B Q8_0 via llama.cpp b12502 / `398f00d65`; two inference threads, no GPU.
- Official kit Python 3.12.16; Harbor 0.20.0; Docker 29.1.3. Docker official Buildx v0.39.0 was added to the user CLI-plugin directory after authorization; its downloaded asset SHA256 matched the release metadata.
- Official-run model context: 8192, output ceiling 1024, thinking disabled. Agent deadline capped at 300 seconds, outer supervisor 480 seconds plus 120 seconds cleanup grace. The existing short-task finalization reserve adapts to about 75 seconds, not a fixed 180 seconds.
- Four local-dev invocations in this sequence, each one task, one trial, one attempt, no automatic whole-task retry. Each later invocation followed a concrete repair or candidate change.
- Bridge-only, temporary authenticated model gate; no LAN-wide listener, firewall or SSH changes. Temporary credential file permissions 0600 inside 0700 directory.
- Synthetic probes: pinned Python image `sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`, network none, non-root, read-only mounts/root, CPU 2, memory 4 GB, outer limit 175 seconds. Model context 4096, output ceiling 192, temperature 0, at most four requests, internal 150-second budget.
- No paid API route, additional GPU, or submission used. Incremental API charges were avoided; electricity/host cost was not measured and is not asserted to be zero.

## Procedure

1. Run the official local evaluation entry with one checks task and no export, under an external supervisor.
2. Diagnose the first setup failure; install the authorized official Buildx dependency, then retry once.
3. Diagnose StreamCut from content-free timing and gate code. Increase gate idle read timeout from 30 to 55 seconds, below the client's 60 seconds, without increasing global budgets. Replace silent termination with explicit HTTP/SSE errors and content-free request timing/byte/error records. Retry once.
4. Add generic stateless-shell and early-deliverable guidance plus feedback for standalone cd in a separate candidate. Three focused CPU/structural checks passed. Compare once on the same task and limits.
5. Stop unchanged official-task repetitions. Test explicit per-call cwd in an isolated synthetic read/transform/write fixture.
6. Test a narrower typed read/write interface in a separate isolated exact-copy fixture. No arithmetic was included in this second fixture.

All evaluated candidate copies remained separate. No scored result was hand-edited. No competition artifact was published.

## Results

### Local development runs

| Stage | Whole-run duration | Agent duration | Measurement/status | Outcome |
| --- | ---: | ---: | --- | --- |
| Initial setup | about 34 s | not reached | incomplete, unmeasured | Buildx absent; sidecar image could not build |
| After Buildx | about 219 s | 121 s | measured, harness error | reward 0; StreamCut |
| Gate repair | about 269 s | 228 s | complete, measured, status ok | reward 0; zero created files, empty final message |
| Navigation guidance | about 297 s | 228 s | complete, measured, status ok | reward 0; zero created files, 1336-byte final message |

The initial displayed zero was a placeholder for an unmeasured failure, not a measured score. The second zero came with a harness failure and must not be treated as a clean assessment of answer quality.

After the gate repair, nine logged transport requests had no recorded transport exception. The navigation candidate still repeated standalone cd and ls without progressing to file creation. Input/output token totals increased from 25,469/297 to 43,871/569. Its logs contained one IncompleteRead (99.005 s); the harness nevertheless ended with status ok. Cancellation, model-side framing interruption and other causes were not isolated.

The comparison used the same task/model/agent deadline/outer cap/gate timeout, one sample per candidate. The navigation candidate required a rebuild. It was neither randomized nor a statistical performance study.

### Synthetic explicit-cwd probe

The implementation quotes cwd and runs `cd -- <cwd> && command`, rather than silently assuming persistent shell state. Three CPU checks passed: space-containing cwd, nonexistent cwd failing closed, and relative cwd rejection.

One model trial took **43.278 s**, four requests. Standalone cd calls dropped to zero, but the model shortened the space-containing path and generated invalid shell arithmetic. **No requested output file was created.**

### Synthetic typed read/write probe

The implementation restricts each tool to an exact allowed path in both its schema enum and execution check, uses a directory fd with O_NOFOLLOW, and caps writes at 1024 bytes. Three CPU checks passed: traversal rejection, input-overwrite rejection and symlink-write rejection.

One model trial took **11.005 s**, two requests. It read the allowed file, then wrote the exact **16 bytes**, including the newline, to the allowed output. Actual file content verification passed.

**This was an exact-copy task, not the prior arithmetic task.** The fixed path enum and task simplification changed multiple factors. The result supports this narrow I/O capability only, not a causal A/B claim about typed tools, general reasoning improvement, or a PLE score gain.

## Cleanup and limitations

After each local-dev invocation, the model was stopped, both temporary listening ports were closed, no owned task/serve containers remained, and no temporary credential files remained. The authorized shared serve-egress Docker network remains; existing unrelated services were preserved. Both synthetic containers and model processes were stopped.

No additional official-task run followed the negative navigation comparison. No broader benchmark, eligible Google-model evaluation, GPU run, paid external model call, or submission was performed.

Raw restricted task material and credentials are not included here. Synthetic test code and structured observations were retained separately. Sleep use was retrieval of an existing approved public Docker-requirement reference, not training or adoption of a new failure rule. Scientist stored the synthetic code, structured observation and Sleep reference; all three artifacts and the manifest were read back.

## Evidence identifiers

SHA256 identifiers, not downloadable raw task artifacts:

- Gate-repaired local result: `f113e61fff7e529ed1fff6697ba22abc27ecf692551c214427eaba7659ec4e8a`
- Navigation local result: `43aee05781af28bb93f7377ca05cbfb28940c906eeb847a5150989505ad8e447`
- Navigation candidate: `0f5715e881ce8c4b453428b4493d7a4a85a3c957a31c0afa6e9a94850757a8b2`
- Explicit-cwd synthetic probe: `aed905f454043d6690d1c380b45da683b5a6ec5bb98f320e7c8a0396c206b76c`
- Typed-I/O synthetic probe: `0e6b258e00155f42c5b74805d474c660f7ffad6418312a61146d0eeeba856df0`
- Typed-I/O raw synthetic result: `77f3d00d6087dad2bbb9e4fdbadd37569cc87374c12c1faec87ac9470b4548a1`
- Typed-I/O Scientist manifest: `5fd4cd918506b7e8e9cd16cc49a1714a21fdd05cefe84a0296861398da191709`

## Decision and next step

Do not repeat the unchanged official task. Prioritize narrow typed operations with explicit allowed paths and actual file checks, then isolate task difficulty separately before any broader run. A repeated-call/result fingerprint could stop unproductive loops, but must distinguish valid polling and changed files. Context deduplication must invalidate on changed content and compaction. Diagnose IncompleteRead before changing time or retry budgets.

None of these proposals authorizes new paid work, network exposure, data access, or submission.

References: [official PLE evaluation guide](https://github.com/google-research/ple/blob/main/eval/README.md), [Docker Buildx](https://github.com/docker/buildx).

## 日本語要約

ローカルCPUのQwenで公式キット経路を通し、Buildx不足とStreamCutを修正しました。正常終了した2回の実測はともに0点、成果物0でした。注意文だけではcd/ls反復を改善できませんでした。

明示cwdの合成試験もパス・shell算術の誤りで失敗。一方、固定許可パスの型付きread/writeによる単純コピーは、2リクエスト・11.0秒で実ファイル検証に成功しました。ただし算術も除いた別条件の1例で、PLE性能改善や因果的な比較とは扱いません。

費用の発生するAPI・GPU・提出なし。実行後はモデル・所有コンテナ・一時認証を停止／削除し、ポート閉鎖を確認。共有ネットワークだけ承認どおり残しています。秘密・制限付き課題本文・生trajectoryは公開していません。同条件の反復は停止し、失敗と未検証を含めて記録しました。

## Follow-up: typed numeric transformation (2026-11-18 UTC)

Question: with the typed I/O implementation unchanged, can the same model read an integer, add four, and save the result, rather than merely copy text?

One additional synthetic model trial used the same exact path enums (including a space), tool execution code, model, sampling and isolation/resource/time limits as the typed-copy probe. Only the fixture input, requested transformation and expected output changed. The previous three safety tests were **not rerun** because the safety implementation was unchanged. No official task was executed.

Result: **2 requests, 10.425 seconds, pass**. The model first read the input, then wrote the correct three-byte result including its newline. Actual file contents were checked; this was not a claim inferred from a final message. No tool error occurred. Model termination and container removal were verified.

Probe SHA256: `03e72548d9b0a79be8c41578f13b276e8ce536d159e72f61ebc27113b6c293e6`.

Interpretation: a small numeric transformation succeeds when shell syntax and path choice are constrained. This single fixture does not establish general arithmetic reliability, superiority over a matched shell baseline, or a PLE score improvement. It narrows the earlier shell failure: inability to perform this elementary transformation is not demonstrated by that failure alone. More elaborate tasks and unrestricted path selection remain untested. No additional charge, network exposure, GPU, or submission was introduced.

日本語追記: 型付きI/Oの実装を変えず、コピーから「整数を読み4加えて保存」へ変更した1回は、2リクエスト・10.425秒で成功しました。実ファイル3byteを確認済み。既存安全試験は再実行せず、モデル／コンテナ停止も確認しました。小さな合成変換の成功であり、一般能力や公式課題の得点改善は未検証です。

## Follow-up: generic typed text I/O adapter (2026-11-18 UTC)

Status: implemented as a separate experimental candidate; bounded CPU checks completed. **No model call or official-task evaluation of this candidate.**

### Design and rules review

The pinned official kit's minimal sample exposes only bash/read_file/write_file and forwards operations through the task session. Its protocol describes runtime workdir and filesystem operations. This supports a custom narrow tool wrapper as an engineering approach; it is not individual organizer approval of this implementation. Current organizer agent instructions were inspected. The Kaggle rules page body could not be retrieved, so a complete review of current competition rules is **not** claimed.

References: [pinned protocol](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/protocol.md), [pinned rules](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/rules.md), [organizer agent instructions](https://ple-bench.com/competition/agents).

Unlike the fixed synthetic path enums, this candidate derives its root only from the current session.workdir, discovers names with list_directory, and accepts relative paths under that root. It has no task-ID branch, known answer, fixed task directory, or access to graders/reference artifacts.

### Implementation boundary

- Model tools: list_directory, read_text, write_text, make_directory. Names and file contents remain untrusted task data.
- Execution uses **official session.exec** to run a small Python filesystem operation inside the task container, not a host filesystem API. This prototype intentionally uses descriptor-based traversal instead of assuming a lexical prefix around a symlink-following API is sufficient.
- The root and every directory component are opened with O_DIRECTORY/O_NOFOLLOW; absolute user paths, parent traversal, empty/dot components, symlinks and an unrestricted root of "/" are rejected.
- Listings are capped at 128 entries. UTF-8 read/write size is capped at 64 KiB; special/nonregular files and NUL-bearing text are rejected. Writes default to exclusive creation; explicit overwrite is required for existing regular files. Missing parents are not silently created.
- Unknown tool names are denied even if guessed by the model. Shell, legacy edit operations and MCP are not dispatchable in this candidate; MCP-bearing tasks fail closed.
- The candidate's own tool log records only the recognized operation name, not arguments, paths or content. Official protocol/evaluator records remain a separate consideration and must not be publicly copied.
- Per-operation time is capped at 10 seconds and remaining session time. Existing overall budgets are unchanged. No new network or permission configuration was introduced.

### Minimal validation and failure accounting

Five distinct CPU cases passed in an isolated network-none container: dynamic directory/text round trip with spaces; parent traversal rejection; symlink-parent rejection; implicit overwrite rejection preserving original content; and denial of an undeclared shell call with content-free tool logging.

The first invocation completed the first four checks, then the isolated AST dispatch test failed because its test namespace omitted the Any annotation symbol. The test namespace was corrected and **only the fifth case** was rerun. Total: five distinct passing cases, six case-attempts, two invocations. This was a test-fixture error, not evidence that the first four checks were rerun. Containers were removed. No model or task run was used to validate this change.

This checks selected boundaries, not exhaustive security coverage. The session.exec transport was represented by a local subprocess-backed test session; the full official WebSocket/evaluator integration remains **unrun**. Size caps and other static branches are implemented but were not separately exercised in this five-case budget.

Candidate serve SHA256: `fe0987cae8fcec7b95343a5cd24d81078659780055f8c8ed8c6a40100e18aef3`.
Typed adapter SHA256: `375f6dd2bd07222227d2e301166c0be24e6ac1fc5b7cdd9fa2c585b065aabd21`.

### Decision

This is a **text-only research prototype**, not a replacement for the full PLE agent: binary office/PDF deliverables, code execution and MCP tasks are unsupported. The prior real-model successes do not validate this new dynamic-path integration. Do not claim a score gain or immediately rerun an incompatible real task. Resolve the remaining rules/logging/transport checks and choose an appropriate minimal synthetic integration step before any further local-dev evaluation.

日本語追記: 課題固有パスを固定せず、session.workdir内の動的探索と型付きテキストI/Oを行う別候補を実装しました。パス逸脱・symlink・無断上書き・未宣言shell呼出しを拒否し、独自ログは操作名だけです。CPU5ケース成功、試験側の型注釈不足で最後の1ケースのみ再実行しました。公式WebSocket統合・モデル・実課題は未実行。binary/MCP非対応と最新Kaggle規約本文の未確認を残し、実課題評価へは進めていません。

## Follow-up: real WebSocket, synthetic evaluator peer (2026-11-18 UTC)

Status: two minimal CPU-only connection cases passed. No model call, restricted task, official evaluator run, or submission.

The exact taskbridge.py used by the candidate matches the pinned official local-model sample byte-for-byte: SHA256 `2f15766091ff1be44d58128d690177c7756c75e06650a46f706533e6b31b12a6`. The existing websockets 17.4 package was mounted read-only; nothing was installed.

Inside one network-none, non-root, read-only container (CPU1/256 MiB, outer40-second limit), a loopback-only ephemeral WebSocket server invoked the official taskbridge._session and Session implementation. A synthetic evaluator peer sent task/result/cancel frames and executed the generated operations solely against temporary synthetic files. No host port was published.

1. **Round trip:** task → four exec/result pairs (directory listing, read, write, readback) → content-free progress log → done. Request IDs were unique and matched to replies; saved bytes matched the synthetic input.
2. **Pending-request cancellation:** task → exec request → cancel → done. The official pending future raised Cancelled and the handler observed it, without executing the pending filesystem operation.

Both loopback ports were closed after their server contexts exited; the container was removed. Persisted output contained only the result summary and frame types, not raw frames, generated commands or file contents; stderr was empty. This specifically checks the synthetic probe's progress-log path. It is **not** an end-to-end audit of all possible SDK/model/evaluator logs.

Probe SHA256: `9d14b11f26bd04451ef7fa904e388bae90c374da5e18bd980f699a99e44aa9e0`.

The transport is now exercised over a real WebSocket rather than only a fake session, but the peer is a fixture, not the official evaluator. Full candidate inference, evaluator/egress integration, scoring and binary/MCP capabilities remain unrun or unsupported.

### Rules recheck and remaining gate

The repository's exact [Kaggle competition rules URL](https://www.kaggle.com/competitions/physical-engineerings-last-exam/rules) was retried; no rules body could be retrieved. An alternate path and search did not yield the competition-specific text. General Kaggle terms or another competition's rules were not substituted.

The current [organizer guide](https://ple-bench.com/competition/guide), [agent instructions](https://ple-bench.com/competition/agents), and pinned kit protocol/rules support operating through the evaluator protocol and prohibit task-identity routing, hard-coded answers, grader/reference access, proxy bypass and copying restricted task content into independent logs. Stdout/stderr, exceptions, SDK debug, model server and relay logs all need review; suppressing Session.log alone is insufficient.

Thus the synthetic connection check is complete, but the Kaggle-specific participation/data/publication conditions and the boundary between official evaluator records and prohibited independent logging are not fully verified. **No real-task rerun was performed or unlocked by this result.**

日本語追記: 固定公式taskbridgeを実WebSocketで使用し、合成peerとの読取→書込→読戻しとpending中cancelの2ケースが成功しました。network none内のloopbackだけで実施し、ポート閉鎖・コンテナ削除を確認。モデル・実課題は未実行です。Kaggle大会固有規約の本文は再取得できず、ログ経路全体の確認も残るため、実課題評価へ進める根拠にはしていません。

## Follow-up: logging boundary and legitimate rules access (2026-11-18 UTC)

### Correction: rules page is readable in the browser

The earlier failed text-fetch attempts were a retrieval limitation, not a requirement to sign in. The exact Kaggle rules page was opened through an existing Chrome session and its body was visible **while signed out**. No login, Join, acceptance, permission change or owner intervention was needed.

The browser review identified B4 restrictions on competition-data use and disclosure to nonparticipants; B6 conditional use of external data/models/tools subject to host restrictions; C5(d)/C6 restrictions on private code/data sharing outside the team; and C4(b) restrictions on incorporating manual labels/predictions for validation/test without explicit permission. These observations do not authorize sending restricted tasks to another model service. Long paragraphs were truncated in the accessibility output, so a complete clause-by-clause review and the owner's participation/acceptance state remain unverified. The older statements that the body could not be retrieved describe the earlier web-text route and are superseded by this browser-access finding.

### Candidate-owned log hardening

Static review found remaining content-bearing paths beyond tool-call logs: task workdir startup output, exception strings in model retry/compaction handling, taskbridge malformed-frame diagnostics and handler errors, subprocess stderr forwarding, and optional SDK/transport debug logging.

A separate quiet candidate now:
- emits only a fixed startup label rather than the workdir;
- allowlists recognized typed-operation names in Session.log and replaces other diagnostics with a fixed redaction label;
- disables standard Python logging for the harness process and uses exception-type-only top-level/async diagnostics;
- suppresses raw malformed frames, handler exception messages and subprocess stderr in its derived taskbridge diagnostics.

This bridge is **modified from the official sample**, unlike the byte-identical bridge in the prior WebSocket test. No claim is made that the previous complete round-trip test was rerun on every new branch.

Three new synthetic sentinel scenarios passed in a network-none container: allowlisted session logging plus standard-log/top-level/async error handling; a real WebSocket handler exception; and a malformed frame followed by cancellation. The sentinel appeared in neither captured stderr nor returned diagnostic frames. All cases used synthetic content, no model or real task. Container removal was verified.

Quiet serve SHA256: `0f368da9b443ed292610977335eb6ee901f9e826052d11e5da6f5328aa5ee5b6`.
Derived bridge SHA256: `5cdb7cbf76e10ae806833488b7acaa5743593a74aa427a2deaf805347a645142`.
Diagnostic guard SHA256: `48212bc46f79607980ef2fb5cc66dfeaef7ea9bdbacc36ee47b32ed5e674df4d`.
Sentinel probe SHA256: `a5e42634fce96e36208a9325b5b5e4091a4211c24971cb2f00a60eee63e4d043`.

### What this does not close

The official evaluator separately constructs trajectory records and saves harness/serve/egress logs (pinned kit harbor_agent.py). Its exec/result records can contain task data even when independent harness diagnostics are content-free. These required official records must not be confused with additional debugging logs or automatically included in a public report. The evaluator/export format was **not modified**.

The existing temporary gate records only request IDs, timings, status/byte counts and exception classes; model stdout/stderr was directed to the null device. These checks do not prove that every future deployment, dependency or optional debug setting is content-free.

The real-task hold remains: confirm the applicable data/record-retention interpretation and remaining rules clauses, then review the exact run configuration. No new real-task run, external task transmission, paid inference or security-boundary expansion occurred.

日本語追記: 規約本文は既存Chromeなら未ログインで閲覧でき、本人操作は不要でした。データ公開・チーム外共有等の制限を確認しましたが、長文省略と参加状態の未確認は残ります。独自ログの残存経路を別候補で抑制し、合成sentinel3ケースが成功。公式評価器のtrajectory等は別経路のため、独自ログ対策だけで実課題の保持・公開条件を満たしたとは扱わず、実課題保留を継続します。

## Follow-up: official trajectory retention remains unresolved (2026-11-18 UTC)

Read-only source review confirmed that the pinned official evaluator records the opening instruction as a user step, builds a trajectory from steps/tool arguments/observations/final output, and saves it alongside run logs. See [relay.py](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/relay.py#L1006) and [harbor_agent.py](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/harbor_agent.py#L777-L895).

The pinned [artifact documentation](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/artifacts.md) classifies trajectory.json as optional inspection evidence, never graded, and omits oversized trajectories from export. This does **not** by itself establish permission to publish raw trajectories or retain them indefinitely. The [evaluation README](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/eval/README.md) documents run-local protocol transcripts, trajectory and serve/egress logs.

**Correction/clarification: --no-export is not a content-nonretention mode.** It prevents updating the entry's artifacts directory; local run records and run-side artifacts can still remain. No setting was changed to bypass this behavior.

The pinned rules distinguish public dev tasks and hidden test tasks and explicitly prohibit retaining test-task prompts/files. The current organizer agent instructions use broader wording about copies of task content. No explicit retention period or general exception reconciling that wording with the evaluator's automatic dev-run records was found. This is an unresolved interpretation, not a declaration that all official dev records are forbidden or that all are safe to publish.

A metadata-only inventory found three existing trajectory files from the earlier local runs. Their contents were not reopened for this inventory. They were not deleted, moved, modified or uploaded. No raw trajectory, task content or credential was added to this report.

Participation/acceptance status is also unverified. Public rules are readable without login, but that does not establish the participant's account state. Checking participation requires an authenticated view of the competition; joining or accepting rules would be a separate authorized decision.

### Safe handling pending clarification

- Keep real-task evaluation on hold; continue only unrelated synthetic development if requested.
- Do not make independent content-bearing harness/model/gate logs.
- Do not automatically publish raw official run records or treat the repository's public report as an approved artifact export.
- Do not alter official scored records to manufacture compliance, and do not delete existing evidence without an appropriate decision.
- Seek a precise answer on whether automatically generated local dev trajectories may be kept, any retention limit, and which exports are permitted. No organizer message has been sent.

日本語追記: 公式評価器がinstruction・操作・結果をtrajectoryへ保存することを確認しました。trajectoryは任意・非採点ですが、それだけで公開や無期限保持の許可にはなりません。--no-exportも内容非保持ではありません。保持禁止との適用関係・保存期間の明示を確認できず、参加状態も未確認のため実課題は保留継続。既存trajectoryは本文を開かず件数だけ確認し、削除・改変・公開していません。


## Follow-up: quiet bridge + typed I/O synthetic integration (2026-11-18 UTC)

Status: **one integrated synthetic case passed**. No model inference, real task, official evaluator, external task transmission, paid API, additional GPU, or submission.

The quiet candidate's four component hashes still match the previously recorded serve, derived bridge, typed adapter and diagnostic guard. Inspection found that its copied WS-TEST metadata referred to the **older generic bridge**, not this quiet implementation. That copied result was not counted as quiet integration evidence.

### Scope and execution

The new probe uses the quiet bridge, diagnostic wrapper and typed adapter together over a real WebSocket with a synthetic evaluator peer. It does **not** execute serve.py's model/tool-selection loop. The existing dependency-bearing image was used without downloads or installation, with network none, ephemeral loopback only, no published host port, non-root, read-only root/mounts, CPU1, 512 MiB, pids32, outer45-second limit and per-exec5-second limit.

The first invocation failed **before exercising the boundary** because the image's system Python did not expose the existing websockets dependency. This was an unmeasured setup failure, not a failed task or a scored zero. Only the interpreter path was changed to the image's existing harness virtual environment. Candidate code, probe and image were unchanged; the previously unexecuted integrated case was then run once.

### Observed result

- Six uniquely identified exec/result exchanges: five synthetic commands covering mkdir, write, read, list and a rejected parent-traversal write; the sixth response injected a synthetic error.
- Saved bytes matched the generated synthetic input; directory listing matched; the out-of-root write was rejected and no escaped output appeared.
- The required synthetic data correctly crossed the exec/result channel. That necessary dataflow was **not** misclassified as diagnostic leakage.
- Allowlisted operation logging remained available; other log text was redacted. The injected error produced a content-free terminal error frame, and captured stderr contained no synthetic sentinel. Stderr was 29 bytes, **not empty**.
- The loopback listener was closed and the owned container was absent after both invocations.

No raw frames, generated commands, synthetic runtime payloads, restricted task data or credentials were persisted in the observation. Persisted evidence contains code, counts, component hashes and boolean checks.

Probe SHA256: `86fd0759a49fa990c3d2b1f93d9a9162eb5c200821668ea638f6c1eab2cf0bc9`.
Scientist manifest SHA256: `c101204e24d0bc883c79b14a79c4c93221b9d5437bfa2dc0ad435f61bd342998`.

Sleep retrieved the existing approved public Docker-requirement excerpt only; no new rule was adopted and no consumer/provider was dispatched. Scientist stored five exact-byte artifacts and the manifest, then verified every readback. Its first import attempt was refused before writes because an optional environment field referenced an evidence-kind artifact; the empty store was checked, the optional fields left unspecified, and the corrected import succeeded. This recording correction did not rerun the experiment.

### Interpretation and remaining hold

This closes a narrow previously untested connection between the **quiet** bridge, typed operations and diagnostic guard. It is not a model capability result, full-candidate inference test, comprehensive leak audit, official protocol/evaluator certification or score improvement.

The quiet serve/model loop, official evaluator/egress integration, participation status and trajectory retention interpretation remain unverified or on hold. No real-task evaluation was enabled by this synthetic success, and no existing official records were reopened, deleted, changed or published.

日本語追記: quiet版のbridge・型付きI/O・診断抑制を、実WebSocketと合成peerで初めて組み合わせて確認しました。旧generic版のコピー結果はquiet版の証拠に数えません。初回は既存依存を参照できないPythonで起動前失敗し、既存venvへ起動位置だけ直して未実行の1ケースを実施。6RPCで読書き・一覧・パス逸脱拒否・エラー時の診断非漏洩が成功し、ポート閉鎖とコンテナ削除を確認しました。必要なデータ通信と診断ログを区別し、モデル呼出し・公式課題は0。Sleepの既存公開参照取得とScientistの保存・読戻しも記録済み。実モデルloopと公式評価器・参加/trajectory条件は引き続き未検証・保留です。
