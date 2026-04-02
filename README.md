# gitlaw-ja

日本の法律の改正履歴・沿革を構造的なディレクトリ・ファイル実体とGitで追跡可能なコミットデータに変換する試み。

- `src/`: バルクデータをGitのコミット・ブランチデータへ直接変換するPythonスクリプト
- `laws/`: ファイル実体が保管されています。
  - `{law_id[:3]}/{law_id}/`: e-gov 法令APIの法令IDに基づいています。
    - `current.json`:
    - `current.xml`: all_xml.zip内に存在する各法令・版のXMLをそのまま各コミットが適用しています。当ファイルの来歴を見ることで法令の差分を確認することが可能です。

## 使用方法

- python: uvを利用することが一番簡単です
- e-gov 法令APIから`all_xml.zip`と`XMLSchemaForJapanaeseLaw_v3.xsd`をダウンロードし、`payload/`ディレクトリに配置してください
- main.pyがエントリーポイントになっています。

## パイプライン

- `01_ingest`: 入力 ZIP の識別と `run_id` の決定
- `02_validate`: CSV / XSD 契約の検証
- `03_normalize_versions`: CSV/XML から `LawVersion` を生成
- `04_build_timelines`: 法令ごとの版列 (`LawTimeline`) を構築
- `05_graph_plan`: `EnforcementUnit` / `AmendmentEvent` から commit graph plan を構築
- `06_git_sink`: plan をそのまま Git object / refs に反映

## コミット生成ロジック方針

- 施行ブランチ (`enforcements/<run_id>`) は施行単位 (`EnforcementUnit`) の線形履歴。
- 公布ブランチ (`promulgations/<run_id>`) は改正法ごとの side lineage を merge した PR 風 DAG。
- 公布と施行の対応付けは SHA ではなく `Amendment-Id` / `Unit-Id` trailer と `graph_plan.json` で持つ。
- `--as-of` 未指定で Git 反映を行う場合は、JST の当日を既定値として未来施行を除外する。
- 日時は `YYYY-MM-DD` と和暦文字列（例: `令和六年七月一日`）を正規化して扱う。
- 日時の優先順位は `amendment_promulgation_date` → `effective_date` → `revision_id` 先頭日付 → sentinel。
- `diff` は補助出力であり、commit 生成の主要入力には使わない。

## Appendix

- e-gov 法令API
  - <https://laws.e-gov.go.jp/bulkdownload/>
  - <https://laws.e-gov.go.jp/api/2/redoc/#tag/laws-api/operation/get-laws>
  - <https://laws.e-gov.go.jp/api/2/swagger-ui>
- 法令データドキュメンテーション: <https://laws.e-gov.go.jp/docs/>
- 日本法令索引: <https://hourei.ndl.go.jp/>
