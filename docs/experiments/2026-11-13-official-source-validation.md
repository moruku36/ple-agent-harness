# Official source-only schema validation

## Result

**Passed on 2026-11-13 (UTC):** the unmodified official
`kit.spec.load(entry)` accepted this entry's `submission.yaml` with
`google-cloud/gemini-4-argon`. The process exited **0**.

This is a YAML/schema and declared-model validation only. It is **not** a
full `python -m kit validate` CLI invocation, `kit check`, container test,
Pi integration test, model call, dev-set evaluation or competition result.

## Exact sources and conditions

- Entry commit: [`775f1b30128cb93e23998a3b02da1c1651c28ac4`](https://github.com/moruku36/ple-agent-harness/commit/775f1b30128cb93e23998a3b02da1c1651c28ac4).
- Entry tree: `e871ddcb423ecdece48ce6c5723d9c4e8efa184a`.
  The GitHub commit/tree mapping was read back, and all **21 tracked files**
  in the local source snapshot matched that tree's Git blob hashes before this note.
- Validated `submission.yaml`: Git blob
  `b175a2da6749a6e33041249cce7a5f72f863f004`; SHA-256
  `06a971a9e17f04b4b637e8def6318c53205cd6206c326f1d601ee67810d87503`.
  Its bytes matched immediately before validation and were unchanged afterward.
- Official kit: [`google-research/ple@8320f0402fdca9f42476607f72bcfd5271cd50c9`](https://github.com/google-research/ple/tree/8320f0402fdca9f42476607f72bcfd5271cd50c9).
  Four exact files were retrieved through the read-only GitHub connector into
  a separate scratch directory, not the entry directory. Local Git blob hashes
  matched the connector's returned hashes:
  - `kit/__init__.py`: `58d482ea3866250ed5f1eb02fdf1da14377214c6`
  - `kit/__main__.py`: `d54397c5541cc364e02259df5b00fc72af4a9f3b`
  - `kit/spec.py`: `ff6bc389530fed0de6b28e8134d83aa9b311f0df`
  - `kit/models.py`: `2803b4ead7daa555c8d6f6515c479bb617581e63`
- Existing Python **3.12.14** and PyYAML **6.0.3** were used. No dependency
  installation, package manager, `uv run`, credential setup or authentication
  flow was run.

## Import and call-path review

The files were inspected before execution:

- [`cmd_validate`, lines 65–96](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/__main__.py#L65-L96)
  calls `spec.load`, formats model/egress information, and prints an optional
  local-only note. The full CLI has unrelated imports for build, check, stack
  and artifacts, so it was not imported or executed.
- [`spec.py`](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/spec.py)
  imports the standard library, PyYAML and `kit.models`.
  `load` reads local UTF-8 YAML; `parse` uses `yaml.safe_load` and
  `validate`; validation checks fields, names, placeholders, shell-command
  syntax and model identifiers. It does not execute `install` or `serve`.
- [`models.py`](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/kit/models.py)
  imports only the standard library. Its Google Cloud model branch checks a
  fixed dictionary containing `gemini-4-argon`. URL handling is string/syntax
  parsing, not DNS resolution or an API request. `kit/__init__.py` contains
  only license comments.

## Actual command and stdout

Working directory: the separate `ple-official-source-validation-20261113`
scratch directory containing the verified `kit/` files. The entry source
snapshot was at the relative path shown below. The audit guard is an
in-process check, not an operating-system network sandbox.

```bash
python -I -B - ../ple-harness-20261113/candidate <<'PY'
import hashlib
import pathlib
import sys

denied = []
def local_only_audit(event, args):
    if event.startswith("socket.") or event.startswith("subprocess.") or event in {
        "os.system", "os.exec", "os.posix_spawn", "os.fork", "os.forkpty"
    }:
        denied.append(event)
        raise RuntimeError("Source-only validation forbids " + event)

sys.addaudithook(local_only_audit)
sys.path.insert(0, str(pathlib.Path.cwd()))
from kit import spec
import yaml

entry = pathlib.Path(sys.argv[1]).resolve()
before = (entry / "submission.yaml").read_bytes()
expected = "b175a2da6749a6e33041249cce7a5f72f863f004"
assert hashlib.sha1(f"blob {len(before)}\0".encode() + before).hexdigest() == expected

submission = spec.load(entry)

assert (entry / "submission.yaml").read_bytes() == before
print("function: kit.spec.load(entry)")
print(f"Python {sys.version.split()[0]}; PyYAML {yaml.__version__}")
print(f"ok: {submission.name}, {submission.model.api} ({submission.model.label})")
print(f"allowed_hosts: {submission.allowed_hosts!r}")
print(f"local_only_reason: {spec.local_only(submission.model)!r}")
print(f"submission.yaml unchanged: True; git_blob: {expected}")
print("loaded kit modules: " + ", ".join(sorted(
    name for name in sys.modules if name == "kit" or name.startswith("kit.")
)))
print(f"guarded network/process attempts: {len(denied)}")
PY
```

Stdout (exit **0**; no stderr or schema failure):

```text
function: kit.spec.load(entry)
Python 3.12.14; PyYAML 6.0.3
ok: ple-agent-harness, google-cloud/gemini-4-argon (Gemini 4 Argon)
allowed_hosts: []
local_only_reason: ''
submission.yaml unchanged: True; git_blob: b175a2da6749a6e33041249cce7a5f72f863f004
loaded kit modules: kit, kit.models, kit.spec
guarded network/process attempts: 0
```

## Failures, limits and next step

- Initial `git status`/revision inspection exited **128** because the local
  entry is a materialized source snapshot without `.git`. No validator had
  run at that point. Source identity was instead verified against the pinned
  remote commit/tree and local Git blob hashes as described above.
- No model/provider/judge call, GCP operation, Docker/GPU use, task-data download,
  submission, legal-term acceptance or public write occurred. GitHub source
  retrieval was the only remote work for this experiment.
- The guard observed zero covered network/process attempts after it was
  installed. This supports the inspected call path; it is not a general
  security certification.
- `allowed_hosts: []` and an empty local-only reason are schema outputs for the
  sponsored-model declaration. They do **not** establish free local access,
  endpoint availability, actual Argon request behavior or zero runtime egress.
- No entry runtime files changed, no evaluation artifacts were created, and
  the existing 23 local mock tests were not rerun.
- Next: keep the no-charge access investigation and pinned Pi/container
  verification separate. Do not start live calls until a genuinely no-charge
  route and any required authorization are established.

## 日本語要約

公式 kit の固定コミットから取得し、ハッシュを確認した `kit.spec.load(entry)`
だけを実行し、Gemini 4 Argon を指定した `submission.yaml` の検証に成功しました
（終了コード 0）。既存の Python / PyYAML を使用し、依存関係の追加、
モデル呼び出し、GCP 操作、Docker 実行、データ取得、提出は行っていません。

これは設定ファイルの検証です。公式 CLI 全体、Pi の実リクエスト、
コンテナ動作、無料 API 利用、スコアは未検証です。ローカルに `.git` が
なかったため最初の Git 確認は失敗しましたが、固定コミットの tree と
既存 21 ファイルの Git blob ハッシュの一致を別途確認しました。
