# 2026-11-13: Source preparation

Status: completed preparation; runtime evaluation not started.
Evidence class: static source/provenance review, not a benchmark experiment.

## Objective

Prepare a code-only Apache-2.0 repository from the official template without copying competition inputs, secrets or the template author's evaluation artifacts. Establish the initial source state and identify prerequisites for a real run.

## Conditions

- Static check timestamp: 2026-11-13 12:42:13 UTC.
- Resulting initial repository commit: [5d9f2dde9035fb2bdd6d69cbc39b976f0800ba7d](https://github.com/moruku36/ple-agent-harness/commit/5d9f2dde9035fb2bdd6d69cbc39b976f0800ba7d).
- Official template: [22c26a93a9e4974b16e4351faab0e860ff9fb24f](https://github.com/physical-engineerings-last-exam/submission-template/tree/22c26a93a9e4974b16e4351faab0e860ff9fb24f).
- Official kit documentation inspected at [8320f0402fdca9f42476607f72bcfd5271cd50c9](https://github.com/google-research/ple/tree/8320f0402fdca9f42476607f72bcfd5271cd50c9). The kit was not executed.
- Initial dependency declarations: Pi 1.1.0, websockets 15.0.1. Declaration/lock inspection is not proof those dependencies have been installed or work at runtime.
- Environment: cloud Linux workspace with Python available; no Docker executable or Docker socket found. No GPU was used.
- Model calls, judge calls and benchmark tasks: 0 each. No credential setup, data download or paid API execution.

## Procedure and results

The initial repository has 13 files. Seven focused checks passed:

1. Eight upstream files were byte-identical: `LICENSE`, `serve.py`, `harness.py`, `taskbridge.py`, `task-tools.ts`, `requirements.txt`, `package.json`, `package-lock.json`.
2. All three Python source files parsed with Python's AST parser.
3. The declared Pi version was pinned and matched the package lock.
4. The websockets version was pinned.
5. `submission.yaml` differed from upstream only in the entry name.
6. The prepared file set contained no data/artifacts directories or obvious credential filenames.
7. A bounded secret-pattern scan found no matches.

After publication, all 13 remote files were fetched at the initial commit and matched the prepared contents. The recursive remote tree contained no unexpected extra files. This establishes source publication, not runtime correctness.

## Failures, risks and limitations

- No static check failed. Pattern scanning is limited and does not guarantee absence of every possible secret.
- Source review found inherited logging of tool arguments and subprocess errors. That behavior requires hardening before real tasks because task content must not be retained in logs.
- The template's historic instructions conflict with current organizer guidance about model eligibility and credential handling. They were not copied into the new project instructions.
- The author's development artifacts were not copied or treated as our results. Changes to this entry require its own corresponding evaluation.
- Official kit checks, dependency installation, container build, model connectivity, smoke/MCP/cancellation tests, development evaluation, judge and submission were **not run**.
- Participation/rules acceptance, gated data access, a usable Docker environment, credential route and a model/judge budget remain unverified or unapproved. This note does not authorize any of them.

## Decision and next step

Keep the public repository code-only. Add a narrowly scoped logging change and synthetic sentinel tests before considering a real task. No score is reported. Resolve the prerequisites and caps separately before any paid pilot.

## 日本語要約

公式テンプレートからコード中心の公開リポジトリを準備しました。静的な出典・構文・設定チェックは7項目通過し、初期13ファイルの公開後の読戻しも一致しました。これは実行試験でもスコア測定でもありません。

ツール引数や子プロセスのエラーをログへ出す既存実装に課題があり、実タスクの前に修正と合成テストを行います。コンテナ、モデル接続、開発評価、採点、提出は未実施です。大会データや秘密情報、作者の評価生成物は含めていません。
