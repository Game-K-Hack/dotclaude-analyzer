![banner](./images/banner.png)

<p align="center">
  <a href="https://github.com/Game-K-Hack/dotclaude-analyzer/releases/latest"><img src="https://img.shields.io/github/v/release/Game-K-Hack/dotclaude-analyzer?label=%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89&style=for-the-badge&logo=windows" alt="ダウンロード"></a>
</p>

[:fr: Français](./README.fr.md) | 
[:uk: English](../README.md) | 
[:kr: 한국어](./README.ko.md) | 
**:jp: 日本語** | 
[:cn: 中文](./README.zh.md) | 
[:it: Italiano](./README.it.md) | 
[:es: Español](./README.es.md) | 
[:ru: Русский](./README.ru.md) | 
[:de: Deutsch](./README.de.md)

### DotClaude Analyzer

**DotClaude Analyzer** は、`.claude` フォルダを探索し、Claude Code でのアクティビティをより深く理解・活用するためのグラフィカルアプリケーションです。

このアシスタントでは次のことが可能です:

- 設定と接続情報を確認する;
- プロジェクトを閲覧し、すべての会話を読み返す;
- Claude が作成または変更したすべてのファイルを一覧表示する;
- 指定した日付のプロジェクトの完全なバージョンをエクスポートする。

---

### インストール

```
git clone https://github.com/Game-K-Hack/dotclaude-analyzer.git
pip install -r requirements.txt
```

#### グラフィカルインターフェースの起動

```
python main.py
```

#### EXE のビルド

```
pyinstaller --noconfirm build.spec
```

---

### デモ

![screenshot-1](./images/welcome.png)

`User` フォルダ内にある `.claude` フォルダを選択します

![screenshot-2](./images/source.png)

取得したいプロジェクトを選択します(会話を読み返せます)

![screenshot-3](./images/conv.png)

エクスポートするファイルのバージョンを選択します

![screenshot-4](./images/files.png)
