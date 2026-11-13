# PLE Agent Harness

[English](README.md) | [日本語](README.ja.md)

[Google - Agent Harness on Physical-Engineering's Last Exam](https://www.kaggle.com/competitions/physical-engineerings-last-exam) 向けの、初期段階のエージェント・ハーネス開発リポジトリです。英語を主文とし、この日本語版も更新します。

## 現在の状態

ソースの準備と、27件の合成・モックテスト（ログ16件、Argon設定・経路11件）が完了しています。コンテナのビルド、モデル接続、開発用データセットでの実行、大会への提出は未実施です。このリポジトリに実測スコアはありません。大会の入力データ、API 認証情報、タスク出力、上流テンプレートの評価生成物は含めていません。

出発点は公式の Pi / Claude Opus 5.5 テンプレートで、[コミット 22c26a93a9e4974b16e4351faab0e860ff9fb24f](https://github.com/physical-engineerings-last-exam/submission-template/tree/22c26a93a9e4974b16e4351faab0e860ff9fb24f) に固定しています。エントリー名、除外設定、プロジェクト文書を新しくし、既存のログ出力を修正しました。依存ロックは元のままです。テンプレートとの差分があるため、作者の評価生成物を本プロジェクトの結果として扱ったり、そのまま流用したりしません。

公式の未改変 `kit.spec.load(entry)` でも、このモデル宣言の設定検証に通過しました。公式 CLI 全体や `kit check` の成功ではありません。[設定検証ノート](docs/experiments/2026-11-13-official-source-validation.md)に記録しています。固定版 Pi の実際の送信形式を検証する準備は、npm レジストリの名前解決エラーで止まったため、思考フィールドや画像処理は未確認です。[試行記録](docs/experiments/2026-11-13-argon-offline-wire-prerequisites.md)に失敗と制約を残しています。

## 参照する公式情報

- [大会概要・日程](https://www.kaggle.com/competitions/physical-engineerings-last-exam)
- [大会規約](https://www.kaggle.com/competitions/physical-engineerings-last-exam/rules)
- [主催者の現行ガイド](https://ple-bench.com/competition/agents)
- [公式キット](https://github.com/google-research/ple)
- [モデル設定とローカル実行の費用](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/models.md)

古いテンプレートの AGENTS.md や、秘密情報をコミットする助言は採用していません。現行の大会エントリーでは対象の Google 提供モデルを使用し、評価側が認証情報を注入します。非公開リポジトリであってもキーをコミットしません。ローカルのモデル・採点モデル呼び出しは設定先アカウントへの課金を伴う場合があります。本プロジェクトでは利用者負担の GCP や有料のローカル API 呼び出しを行いません。実呼び出し前に無償の大会支給経路を確認します。最終評価の支給は、手元での無料利用を保証しません。

## 使用予定モデル：Gemini 4 Argon

`submission.yaml` は[大会対象モデル](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/docs/models.md)である `google-cloud/gemini-4-argon` を宣言しています。これは候補設定であり、API の利用権限や実測性能が確認されたという意味ではありません。

Pi 1.1.0 の未登録モデル用設定を、コンテキスト1,048,576トークン・最大出力65,536トークン・テキストと画像入力・`--thinking high` にしました。[公式 Pi ガイド](https://github.com/google-research/ple/blob/8320f0402fdca9f42476607f72bcfd5271cd50c9/sample_submissions/pi-opus/README.md#L41-L52)に従い、Argon が拒否するトークン予算を送らないよう `reasoning` は未設定にしています。Gemini のネイティブ `MAX` は `high` より推論が弱いと公式に記載されています。生成設定のテストだけでは実リクエストの形式は検証できず、Pi 連携と画像の実送信・認識は未確認です。[固定版の静的ソース追跡](docs/experiments/2026-11-13-pi-static-request-trace.md)では、正しくモデル登録される経路で思考フィールドを両方省略することを確認しています。CLI の high を直接送るのではなく、主催者ゲートウェイの既定HIGHに依存します。

[一般 API の公式料金表](https://aistudio.google.com/docs/pricing#gemini-4-argon)では Argon は無料枠の対象外です。大会参加者向けの無料開発枠や、API の具体的な利用上限は確認できていません。公式のローカル Vertex プロキシは利用者の GCP に課金され、標準の開発採点では別途 Claude Opus 5.5 を呼びます。どちらの有料経路も実行しません。評価時に支給される認証情報は、手元での無料利用を保証しません。[Argon設定ノート](docs/experiments/2026-11-13-argon-config.md)と[無償経路の調査](docs/no-charge-paths.md)に条件と制約を記録しています。

## ネイティブ Gemini のバックエンド保護

ネイティブ Google 経路では、`GOOGLE_GENAI_USE_ENTERPRISE` と `GOOGLE_GENAI_USE_VERTEXAI` の各変数が未設定か、小文字の `false` である場合だけ許可します。有効・曖昧な値ならカタログ/Piの実行前に停止します。安全な値を子プロセス用のコピーで明示的に `false` にし、元の環境変数や端末設定は変更しません。他経路の動作も維持します。

この保護は環境フラグによる Vertex/Enterprise 選択を防ぐもので、接続先の課金や無料利用を保証しません。実呼び出しは引き続き保留します。[画像・経路の実験記録](docs/experiments/2026-11-13-argon-image-routing.md)に、修正内容、途中で直した1件のテストエラー、最終27/27件の成功を記録しています。

## 実行前に必要なこと

1. 現行規約、データ利用条件、アカウントの参加状態を確認します。
2. ローカル Docker 環境を選びます。Windows では公式キットに従い WSL 2 と Linux 側のファイルシステムを使用し、キットと本エントリーを別々のリポジトリにします。
3. 実タスク前に、指定された依存環境と公式キットでログ修正を確認します。合成テストは通過しましたが、テスト環境の websockets は16.0で、指定の15.0.1とは異なります。実プロセス、WebSocket 通信、モデル連携は未確認です。
4. モデルとプロキシ、採点モデル、認証経路、金額上限、タスク数、停止条件を確定します。最終評価が提供されることとローカル実行が無料であることは別です。`kit check` もモデルを呼び出します。
5. 公式チェック、キャンセル動作、上限付きパイロットを確認してから、承認された開発用データセット評価へ進みます。`eval/run.py` の未改変の出力と、ソース・データの版を記録します。
6. 生成物に入力データのコピーや秘密情報が含まれないか、公開前に確認します。スコアをよく見せるために評価出力を手修正しません。コードと対応する生成物は、確認してから一緒にコミットします。

初回の静的ソースチェックは、公式キットのチェック、キャンセル試験、スコア測定、参加資格確認、提出成功を示すものではありません。

## 実験ノート

[実験一覧](docs/experiments/README.md)と[記録テンプレート](docs/experiments/TEMPLATE.md)を使用します。英語本文に日本語要約を添え、目的、正確なコード・設定、環境と実行上限、手順、実測結果、失敗、制約、次の判断を記録します。失敗や中断も残します。静的レビュー、合成テスト、実モデル実行、ローカル開発評価、大会の公式結果を区別し、未実施の項目を実施済みと書きません。

公開ノートにはコード・設定の識別子と確認済みの集計結果を記載し、認証情報、タスクのプロンプトや入力ファイル、未加工の実行履歴、タスク出力のコピーは含めません。大会で必要な評価生成物は別途レビューして公開する必要があり、実験ノートで代用はできません。

## ライセンス

Apache-2.0 です。Google の著作権表示・ライセンス表示を保持しています。[LICENSE](LICENSE) を参照してください。大会データには別の大会規約・データ利用条件が適用され、本リポジトリには含めません。提出する Kaggle Writeup と文書のライセンスも、現行規約に合わせる必要があります。
