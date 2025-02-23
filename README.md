# Tale Forge (ゲームブック・シナリオエディタ)

Tale Forgeは、インタラクティブなゲームブックシナリオを簡単に作成、編集、プレビューできる多機能なWebアプリケーションです。Streamlitを使用して構築され、直感的なユーザーインターフェースで物語の分岐を管理できます。

## 🌟 主な特徴

### 1. シーン編集

- 動的な行追加に対応したデータエディター
- シーンごとに最大3つの選択肢を設定可能
- TOMLファイルによるシナリオのインポート/エクスポート

### 2. 画像管理

- シーンごとに画像をアップロード可能
- 対応フォーマット: PNG, JPG, JPEG, SVG
- SVG画像は自動的にアスペクト比を維持してリサイズ
- 画像の追加、削除が可能

### 3. シーン関係図

- グラフィカルな物語構造の可視化
- 左から右へのフロー形式
- シーンIDと簡略化されたストーリープレビューを表示
- 選択肢のテキストを矢印のラベルとして表示

### 4. シナリオプレビュー

- インタラクティブなゲームブック体験
- レスポンシブなレイアウト
- 画像とテキストの自動調整
- シーン間を選択肢で移動可能

### 5. キャラクター管理

- キャラクター能力値の生成と管理
- 技能値、体力値、幸運値のトラッキング
- オプションで恐怖値の追加が可能
- ダイスロール機能（戦闘、幸運判定）

## 🛠 必要要件

- Python 3.8以上
- 必要なPythonパッケージ:
  - streamlit
  - pandas
  - graphviz
  - toml

## 🚀 インストールと起動

1. リポジトリをクローン:

```bash
git clone https://github.com/wabisukecx/tale-forge.git
cd tale-forge
```

2. 仮想環境の作成（推奨）:

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

3. 必要なパッケージをインストール:

```bash
pip install -r requirements.txt
```

4. アプリケーションを起動:

```bash
streamlit run app.py
```

## 📂 プロジェクト構造

```bash
tale-forge/
├── app.py             # メインアプリケーション
├── editor.py          # シーン編集機能
├── graph.py           # シーン関係図機能
├── gameplay.py        # ゲームプレイ機能
├── story_viewer.py    # ストーリービューア
├── toml_export.py     # TOMLインポート/エクスポート
├── requirements.txt   # 依存パッケージリスト
├── scenario.toml      # 現在のシナリオデータ
└── images/            # アップロードされた画像の保存先
```

## 📖 データ形式

シナリオデータはTOML形式で保存されます：

```toml
[シーンID]
story = "シーンのストーリーテキスト"
choices = ["選択肢1", "選択肢2", "選択肢3"]
destinations = ["遷移先1", "遷移先2", "遷移先3"]
image = "images/シーンID.拡張子"  # オプション
```

## 🔧 エラー処理

- 各機能で包括的なエラーハンドリングを実装
- エラー発生時に適切なエラーメッセージを表示
- デバッグを容易にするためのログ出力

## 🤝 貢献方法

1. リポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 🙏 謝辞

このプロジェクトは、インタラクティブなゲームブック作成を楽しく、簡単にすることを目指しています。ゲームブックの愛好家とクリエイターの皆さんに捧げます。
