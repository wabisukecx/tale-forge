# tale-forge

Tale Forgeは、インタラクティブなゲームブックシナリオを作成・編集・プレビューできるWebアプリケーションです。Streamlitを使用して構築されており、直感的なUIで物語の分岐を管理できます。

## 機能

- シーンの作成と編集
- 選択肢による分岐の設定
- シーンごとの画像管理
- シーン関係図の自動生成
- シナリオのプレビュー機能
- TOMLファイルによるインポート/エクスポート

## 必要要件

- Python 3.8以上
- 以下のPythonパッケージ:
  - streamlit
  - pandas
  - toml
  - graphviz
  - Pillow (画像処理用)

## インストール

1. リポジトリをクローン:
```bash
https://github.com/wabisukecx/tale-forge.git
cd tale-forge
```

2. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

3. アプリケーションを起動:
```bash
streamlit run app.py
```

## 使用方法

### シーン編集

1. 「シーン編集」タブでシーンを追加・編集できます
2. 各シーンには以下の要素を設定できます:
   - シーンID (一意の識別子)
   - ストーリーテキスト
   - 最大3つの選択肢と遷移先

### 画像管理

1. シーン編集タブの下部で画像をアップロードできます
2. 対応フォーマット: PNG, JPG, JPEG
3. 各シーンに1つの画像を関連付けられます

### シーン関係図

- 「シーン関係図」タブで物語の構造を視覚的に確認できます
- 矢印は選択肢による遷移を表します

### シナリオプレビュー

- 「シナリオプレビュー」タブで実際のゲーム体験をテストできます
- 画像とテキストが表示され、選択肢を選んで物語を進められます

## データ形式

シナリオデータは以下のようなTOML形式で保存されます:

```toml
[シーンID]
story = "シーンのストーリーテキスト"
choices = ["選択肢1", "選択肢2", "選択肢3"]
destinations = ["遷移先1", "遷移先2", "遷移先3"]
image = "画像ファイルのパス"
```

## ディレクトリ構造

```
tale-forge/
├── app.py               # メインアプリケーション
├── requirements.txt     # 依存パッケージリスト
├── images/             # アップロードされた画像の保存先
└── scene_template.toml # シーンテンプレート（オプション）
```

## 制限事項

- 1シーンあたりの選択肢は最大3つまで
- 画像は1シーンにつき1枚まで
- 画像ファイルサイズの上限は5MB

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
