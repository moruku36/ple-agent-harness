# Content-free logging: synthetic sentinel checks

## Status

**Synthetic source/mock checks only. No competition benchmark, score, official
kit check, real cancellation test, model call, or submission was performed.**

Date: November 13, 2026 (UTC).

## Question and change

Can the inherited Python harness avoid copying task content into its own logs
while preserving intended final responses, usage reports, tool-result payloads,
and cancellation/deadline control flow?

The inherited implementation logged tool names/arguments, model error text,
retry/compaction event objects, malformed evaluator frames, reader/handler
exceptions, and subprocess stderr. It also retained a stderr tail and included
it in the exception raised when the model produced no reply. Truncating those
strings does not make them safe to retain or publish, even in private logs.

Changes:

- Replace those log messages with fixed event labels. Untrusted tool names and
  exception class names are excluded as well as exception messages.
- Drain subprocess stderr without decoding, printing, or storing its content.
  Emit one numeric byte-count diagnostic per process when stderr was present.
  The count is capped at `2**63 - 1`.
- Keep `Finished.stderr` as an empty compatibility field; add `stderr_bytes`.
  The legacy `log_prefix` argument is accepted but ignored, because a caller
  could put task content in it.
- Preserve exit status and deadline-stop state. The no-reply exception reports
  an exit code, not captured stderr.
- Retrieve exceptions from tasks cancelled during session cleanup so a late
  handler failure cannot trigger asyncio's unhandled-task traceback logger.
- Preserve assistant final text, token usage, evaluator tool results, and relay
  tool-error payloads. These are protocol data, not progress logs. A fatal
  handler error without a summary now has the fixed protocol error message
  `harness_error`; a previously produced summary still reaches `done`.
- Retain original Google copyright/license notices and add modification notices
  to both changed upstream Python files.

## Revisions and conditions

- Upstream template: `22c26a93a9e4974b16e4351faab0e860ff9fb24f`.
- Project runtime source base:
  [`5d9f2dde9035fb2bdd6d69cbc39b976f0800ba7d`](https://github.com/moruku36/ple-agent-harness/commit/5d9f2dde9035fb2bdd6d69cbc39b976f0800ba7d).
- Subsequent documentation-only project base:
  [`7c728650703305326c75a3df8d1e4b5b25bea49e`](https://github.com/moruku36/ple-agent-harness/commit/7c728650703305326c75a3df8d1e4b5b25bea49e).
  The runtime source was unchanged by that documentation update.
- Work was performed in a source snapshot without a local `.git` directory.
  The SHA-256 hashes below identify the exact tested files; this note does not
  claim a locally verified Git HEAD or a published implementation commit.
- Python: 3.12.14 on Linux x86-64.
- Available `websockets`: **16.0**, whereas `requirements.txt` pins **15.0.1**.
  No dependencies were installed or updated. Tests use the installed package
  only to import the module; they do not exercise a real WebSocket connection.
- Test runner and fakes use the Python standard library (`unittest`,
  `unittest.mock`, in-memory streams, and async tasks).
- Inputs are a deliberately synthetic sentinel, synthetic event objects,
  in-memory frames, mock subprocess streams, and synthetic exceptions. No task
  prompts, competition files, credentials, model endpoint, or dataset revision
  were used.
- Actual process creation and process-group stopping are mocked. No Pi process,
  subprocess command, Docker/container/GPU, network request, or paid service
  was started by the checks. The mocked `solve` check creates temporary local
  directories only.

Tested file SHA-256 values:

```text
852889215f6782d1b3df7662d0dca48fb27ab05d8e412624ab8427e90b365a08  harness.py
5185c66dd1dd16d87d2bc11379368eb3ba485f761c13efc804990387738c8342  taskbridge.py
003639c01c11d4ff40540182f5d5e432db29b03568392c8a37922df8f455cb17  tests/test_logging_sentinels.py
```

## Procedure and observed results

Run from the repository root in an environment with `websockets` available:

```sh
python -B -m unittest discover -s tests -v
```

1. Before implementation, the initial 14-case suite produced 8 failures and
   1 error. Failures exposed the inherited log/exception content. The error
   identified the not-yet-added `Finished.stderr_bytes` field. The failing test
   run also emitted two unretrieved `Cancelled` future warnings because its
   assertions stopped before consuming the futures; those test assertions were
   reordered to ensure pending exceptions are consumed first.
2. After the first implementation, those 14 cases passed in 0.030 seconds.
3. Added capped-count and late-handler-failure cases, plus cleanup exception
   retrieval. The final suite produced:

   ```text
   Ran 16 tests in 0.045s
   OK
   ```

4. As a targeted negative control, temporarily mocked the exception-retrieval
   callback to a no-op in memory and ran only the late-handler-failure case.
   It failed as expected, detecting the synthetic exception in asyncio's
   fallback logger context. No source file was changed by this negative
   control. This is an expected test failure, not an unresolved code failure.

The final checks cover fixed tool/retry/compaction/model-error logs; ignored
invalid/unknown stdout events; malformed evaluator frames and reader failure;
normal/failure-after-summary/failure-without-summary protocol responses;
cooperative cancellation; late handler failure; preserved relay tool errors;
stderr discard/count/cap; unchanged stdin/stdout callback data; deadline stop;
mocked process cleanup on task cancellation; and the no-assistant-reply error.
Durations are local unit-test elapsed times, not agent-performance measurements.

## Limitations and next gate

These checks do not establish that every dependency, OS process, or logging
configuration is content-free. `Session.log` remains a general protocol method;
future callers must follow its documented content-free logging contract.
Intentional final messages and tool responses may contain task content and
must not be treated as safe publication material. No raw diagnostic capture
opt-in was introduced.

Real process-group termination, signal delivery, WebSocket behavior, Pi/model
integration, the pinned dependency environment, official kit cancellation,
container build, token accounting against a live provider, deliverable quality,
development scores, hidden evaluation and submission eligibility remain
unverified. No official evaluation artifacts were created or reused.

After the existing setup/data/credential/budget approvals, verify the exact
published harness in the pinned runtime and official kit, then run only the
authorized bounded pilot. Any later benchmark must record the exact harness,
kit/model/data revisions and keep untouched official exports separate from
these synthetic tests. Do not infer a score improvement from this change.

## 日本語要約

- ツール引数、モデルのエラー、再試行イベント、不正な受信フレーム、
  例外本文、子プロセスの標準エラーを、そのままログへ出さないようにした。
  ログは固定イベント名と上限付きバイト数に限定し、標準エラー本文は保存しない。
- 最終回答、トークン使用量、ツールの応答データは保持した。終了時に遅れて
  発生する例外も回収し、asyncio が例外本文をログへ出す経路を抑えた。
- 合成データとモックによる16件のテストが通過した。修正前の失敗と、
  例外回収を一時的に無効にすると検知できることも確認した。
- **公式評価・実モデル実行・実プロセスのキャンセル試験は未実施。スコアはない。**
  ネットワーク接続、データ取得、認証情報設定、課金、コンテナ実行は行っていない。
- テスト環境の websockets は16.0で、指定の15.0.1とは異なる。
  実際の通信、モデル連携、プロセス終了、公式キットでの検証は今後の確認事項。
  生ログが非公開でも安全だとは扱わず、最終回答やツール応答も公開前に確認する。
