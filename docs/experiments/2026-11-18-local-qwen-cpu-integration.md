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
