# gitlaw-ja

日本の法律の改正履歴・沿革を構造的なディレクトリ・ファイル実体とGitで追跡可能なコミットデータに変換する試み。

- `src/`: バルクデータをGitのコミット・ブランチデータへ直接変換するPythonスクリプト
- `laws/`: ファイル実体が保管されています。
  - `{law_id[:3]}/{law_id}/`: e-gov 法令APIの法令IDに基づいています。先頭3文字は和暦になっています。
    - `current.json`:
    - `current.xml`: all_xml.zip内に存在する各法令・版のXMLをそのまま各コミットが適用しています。当ファイルの来歴を見ることで法令の差分を確認することが可能です。

## ブランチについて

1. 公布`runs/<run_id>/promulgations`と施行`runs/<run_id>/enforcements`はブランチを分ける
2. 公布ブランチでは改正法＝commitの単位としたい。
    - 改正法は複数の法律の条文を一気に変える場合がある。
     ![](https://laws.e-gov.go.jp/docs/_next/static/media/210-amendment-of-multiple-laws.a7d76cae.svg)
    - 改正法＝commit単位は個人的に直感的だと思うので。
3. 施行ブランチでは各法令の条文の溶け込み・各法令の版をcommitの単位としている。
   - 同じ改正法の同じ方に対する変更はそのまま同じ時に適用されるわけではない
   - 例えば、制度上緩和措置として「この業界だけは猶予を与える」ということは多いが、法律でも同じで、同じ改正法でも〇〇法は〇月から施行、〇〇法は〇月から施行が起きる。
   - またN段ロケットと呼ばれるものもあり、同じ改正規定が同じ法に対しても、段階的に改正を適用することがある。
4. 公布-施行ブランチの対応の両立
   - これが一番の課題で、これについては今後どのような形であれば自然か、扱いやすいかなどは考えていくつもり。
   - 今のところ、版単位のcommitを最も小さい単位として、公布ブランチ側では改正法ごとに束ねるmerge commit的なcommitを生成している。

## 使用方法

- python: uvを利用することが一番簡単です
- e-gov 法令APIから`all_xml.zip`と`XMLSchemaForJapanaeseLaw_v3.xsd`をダウンロードし、`payload/`ディレクトリに配置してください
  - `--input-zip`と`--xsd-path`で変更が可能です。
- デフォルトでは`法律`のみを対象にします。`--law-type 政令`のように追加でき、`--all-law-types`で全種別を対象にできます。
- main.pyがエントリーポイントになっています。
  - `plan`: runs配下にapplyで適用されるcommit/branchに関する情報を構築し、jsonファイルを含むディレクトリとして`runs/<run_id>`配下に出力します。
    - 詳細はパイプラインを確認してください。
    - `dataset_id`はzipのhash値に基づきます。`run_id`は`日時_dataset_id`です。
    - 既存runを明示的に上書きする場合は`--force`を利用します。
  - `apply`: planで生成された`runs/<run_id>/manifest.json`を--run-manifestで渡し、実際にcommit/branchを生成します。
    - 既存refを明示的に更新する場合は`--force-refs`を利用します。
  - `full`: plan/applyの両方をまとめて行います。この場合--run-manifestは必要ありません。
  - 詳しくは`-h`または`--help`

## パイプライン

- `01_ingest`: 入力Zipの識別と`run_id`の決定
- `02_validate`: CSV / XSDスキーマの検証
- `03_normalize_versions`: CSV / XML から`LawVersion`を生成
- `04_build_timelines`: 法令ごとの版列(`LawTimeline`)を構築
- `05_graph_plan`: `EnforcementUnit` / `AmendmentEvent`からcommit graph planを構築
- `06_git_sink`: planをそのままGit object / refsに反映

## Appendix

- e-gov 法令API
  - <https://laws.e-gov.go.jp/bulkdownload/>
  - <https://laws.e-gov.go.jp/api/2/redoc/#tag/laws-api/operation/get-laws>
  - <https://laws.e-gov.go.jp/api/2/swagger-ui>
- 法令データドキュメンテーション: <https://laws.e-gov.go.jp/docs/>
- 日本法令索引: <https://hourei.ndl.go.jp/>
