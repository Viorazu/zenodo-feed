# Zenodo Feed

Viorazu.のZenodo論文一覧を自動取得し、GitHub Pagesで配信する。

## 仕組み

- GitHub Actionsが毎日Zenodo APIからレコードを取得
- `docs/data.json` に保存
- GitHub Pagesで `https://viorazu.github.io/zenodo-feed/data.json` として配信
- viorazu.com のウィジェットがこのJSONを読んで表示

## 手動更新

Actions タブ → "Update Zenodo Feed" → "Run workflow"
