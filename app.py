"""
Tale Forge - ゲームブックシナリオエディタ
シナリオの作成、編集、プレビューを行うStreamlitアプリケーション
"""

import os
from pathlib import Path

import graphviz
import pandas as pd
import streamlit as st
import toml

# 選択肢の数を定数で管理
NUM_CHOICES = 3


def initialize_session_state():
    """セッション状態の初期化."""
    if 'data' not in st.session_state:
        template_path = Path('scene_template.toml')
        if template_path.exists():
            template_content = template_path.read_text(encoding='utf-8')
            st.session_state.data = load_template_data(template_content)
        else:
            st.session_state.data = pd.DataFrame({
                'ID': ['BG'],
                'ストーリー': [''],
                **{f'選択{i}': [''] for i in range(1, NUM_CHOICES + 1)},
                **{f'選択{i}遷移先': [''] for i in range(1, NUM_CHOICES + 1)}
            })

    if 'image_data' not in st.session_state:
        st.session_state.image_data = {}

    if 'current_scene' not in st.session_state:
        st.session_state.current_scene = 'BG'

    if 'scene_history' not in st.session_state:
        st.session_state.scene_history = []


def save_image(image_file, scene_id):
    """画像を保存し、パスを返す.

    Args:
        image_file: アップロードされた画像ファイル
        scene_id: シーンID

    Returns:
        str: 保存された画像のパス、エラー時はNone
    """
    try:
        image_dir = "images"
        os.makedirs(image_dir, exist_ok=True)

        file_extension = os.path.splitext(image_file.name)[1].lower()
        image_path = os.path.join(image_dir, f"{scene_id}{file_extension}")

        with open(image_path, "wb") as f:
            f.write(image_file.getvalue())

        return image_path
    except Exception as e:
        st.error(f"画像の保存中にエラーが発生しました: {str(e)}")
        return None


def load_template_data(toml_string):
    """TOMLテンプレートからDataFrameを生成.

    Args:
        toml_string: TOML形式の文字列

    Returns:
        pd.DataFrame: 生成されたデータフレーム、エラー時はNone
    """
    try:
        data = toml.loads(toml_string)
        rows = []
        for scene_id, scene_data in data.items():
            row = {
                'ID': scene_id,
                'ストーリー': scene_data.get('story', ''),
            }
            
            # 選択肢と遷移先の設定
            for i in range(1, NUM_CHOICES + 1):
                choices = scene_data.get('choices', [])
                destinations = scene_data.get('destinations', [])
                row[f'選択{i}'] = choices[i-1] if i <= len(choices) else ''
                row[f'選択{i}遷移先'] = destinations[i-1] if i <= len(destinations) else ''
            
            rows.append(row)
            
        return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"テンプレートの読み込みに失敗しました: {str(e)}")
        return None


def export_to_toml(df):
    """DataFrameをTOML形式に変換.

    Args:
        df: 変換するDataFrame

    Returns:
        str: TOML形式の文字列
    """
    scenes = {}
    for _, row in df.iterrows():
        scene_id = str(row['ID']).strip()
        if not scene_id:
            continue

        choices = [
            str(row[f'選択{i}']).strip()
            for i in range(1, NUM_CHOICES + 1)
            if str(row[f'選択{i}']).strip() and
            str(row[f'選択{i}']).strip().lower() != 'none'
        ]

        destinations = [
            str(row[f'選択{i}遷移先']).strip()
            for i in range(1, NUM_CHOICES + 1)
            if str(row[f'選択{i}遷移先']).strip() and
            str(row[f'選択{i}遷移先']).strip().lower() != 'none'
        ]

        story = str(row['ストーリー']).strip()
        if story.lower() == 'none':
            continue

        scenes[scene_id] = {
            'story': story,
            'choices': choices,
            'destinations': destinations
        }

        if scene_id in st.session_state.image_data:
            scenes[scene_id]['image'] = st.session_state.image_data[scene_id]

    return toml.dumps(scenes, encoder=toml.TomlEncoder())


def import_from_toml(toml_string):
    """TOML文字列からDataFrameを生成.

    Args:
        toml_string: TOML形式の文字列

    Returns:
        pd.DataFrame: 生成されたデータフレーム、エラー時はNone
    """
    try:
        data = toml.loads(toml_string)
        rows = []
        for scene_id, scene_data in data.items():
            if not scene_data or not scene_data.get('story'):
                continue

            row = {
                'ID': scene_id,
                'ストーリー': scene_data.get('story', ''),
            }

            # 選択肢と遷移先の設定
            for i in range(1, NUM_CHOICES + 1):
                choices = scene_data.get('choices', [])
                destinations = scene_data.get('destinations', [])
                row[f'選択{i}'] = choices[i-1] if i <= len(choices) else ''
                row[f'選択{i}遷移先'] = destinations[i-1] if i <= len(destinations) else ''

            rows.append(row)

            if 'image' in scene_data and scene_data['image']:
                st.session_state.image_data[scene_id] = scene_data['image']

        st.success(f"{len(rows)}シーンを読み込みました")
        return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"TOMLファイルの読み込みに失敗しました: {str(e)}")
        return None


@st.cache_data
def create_scene_graph(df):
    """シーン関係図を生成.

    Args:
        df: シーンデータを含むDataFrame

    Returns:
        graphviz.Digraph: 生成された有向グラフ
    """
    graph = graphviz.Digraph(format='svg')
    graph.attr(rankdir='LR')

    for _, row in df.iterrows():
        scene_id = str(row['ID']).strip()
        story_preview = (
            f"{row['ストーリー'][:20]}..."
            if len(row['ストーリー']) > 20
            else row['ストーリー']
        )
        graph.node(scene_id, f"{scene_id}\n{story_preview}")

        for i in range(1, NUM_CHOICES + 1):
            dest = str(row.get(f'選択{i}遷移先', '')).strip()
            choice_text = str(row.get(f'選択{i}', '')).strip()
            if dest and choice_text:
                graph.edge(
                    scene_id,
                    dest,
                    label=f"選択{i}: {choice_text[:10]}..."
                )

    return graph


def add_image_uploader(scene_id):
    """シーンごとの画像アップローダーを追加.

    Args:
        scene_id: 画像を追加するシーンのID
    """
    image_file = st.file_uploader(
        f"シーン {scene_id} の画像をアップロード",
        type=['png', 'jpg', 'jpeg'],
        key=f"image_{scene_id}"
    )
    if image_file:
        st.image(image_file, caption=f"シーン {scene_id} の画像")
        saved_path = save_image(image_file, scene_id)
        if saved_path:
            st.session_state.image_data[scene_id] = saved_path
            st.success(f"画像が保存されました: {saved_path}")


def show_scene_images():
    """保存済みの画像を表示."""
    st.subheader("登録済みの画像")
    cols = st.columns(3)
    for i, (scene_id, image_path) in enumerate(st.session_state.image_data.items()):
        with cols[i % 3]:
            try:
                st.image(
                    image_path,
                    caption=f"シーン {scene_id} の画像",
                    use_container_width=True
                )
                if st.button(f"削除 (シーン {scene_id})", key=f"del_{scene_id}"):
                    del st.session_state.image_data[scene_id]
                    Path(image_path).unlink(missing_ok=True)
                    st.success(f"シーン {scene_id} の画像を削除しました")
                    st.rerun()
            except Exception as e:
                st.error(f"画像の表示中にエラーが発生しました: {str(e)}")


def get_scene_data(scene_id):
    """指定されたシーンIDのデータを取得.

    Args:
        scene_id: 取得するシーンのID

    Returns:
        pd.Series: シーンデータ、見つからない場合はNone
    """
    scene = st.session_state.data[st.session_state.data['ID'] == scene_id]
    if len(scene) == 0:
        return None
    return scene.iloc[0]


def format_story_text(text):
    """ストーリーテキストを整形.

    Args:
        text: 整形前のテキスト

    Returns:
        str: HTML改行タグを含む整形済みテキスト
    """
    return text.replace('\n', '<br>')


def show_preview():
    """シナリオのプレビューを表示."""
    scene_data = get_scene_data(st.session_state.current_scene)
    if scene_data is None:
        st.error(f"シーン '{st.session_state.current_scene}' が見つかりません")
        return

    with st.container():
        st.subheader(f"シーン: {st.session_state.current_scene}")

        main_content = st.container()
        with main_content:
            if st.session_state.current_scene in st.session_state.image_data:
                try:
                    col1, col2 = st.columns([1, 1.5])
                    with col1:
                        image_path = st.session_state.image_data[
                            st.session_state.current_scene
                        ]
                        if os.path.exists(image_path):
                            with open(image_path, "rb") as f:
                                image_data = f.read()
                            st.image(image_data, use_container_width=True)
                        else:
                            st.error(f"画像ファイルが見つかりません: {image_path}")

                    with col2:
                        formatted_story = format_story_text(scene_data['ストーリー'])
                        st.markdown(formatted_story, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"画像の表示中にエラーが発生しました: {str(e)}")
                    formatted_story = format_story_text(scene_data['ストーリー'])
                    st.markdown(formatted_story, unsafe_allow_html=True)
            else:
                formatted_story = format_story_text(scene_data['ストーリー'])
                st.markdown(formatted_story, unsafe_allow_html=True)

            st.divider()
            choice_container = st.container()
            with choice_container:
                for i in range(1, NUM_CHOICES + 1):
                    choice = scene_data[f'選択{i}']
                    destination = scene_data[f'選択{i}遷移先']
                    if (choice and destination and
                            choice != "None" and destination != "None"):
                        if st.button(
                            f"{i}. {choice}",
                            key=f"choice_{st.session_state.current_scene}_{i}",
                            use_container_width=True
                        ):
                            st.session_state.scene_history.append(
                                st.session_state.current_scene
                            )
                            st.session_state.current_scene = destination
                            st.rerun()


def add_import_export_section():
    """インポート/エクスポートセクションを追加."""
    uploaded_file = st.file_uploader("TOMLファイルをインポート", type=['toml'])
    if uploaded_file is not None:
        toml_content = uploaded_file.read().decode('utf-8')
        imported_df = import_from_toml(toml_content)
        if imported_df is not None:
            st.session_state.data = imported_df
            st.success("TOMLファイルを正常にインポートしました！")


def add_image_management():
    """画像管理セクションを追加."""
    st.subheader("画像管理")
    selected_scene = st.selectbox(
        "画像を追加するシーンを選択",
        options=[
            row['ID'] for _, row in st.session_state.data.iterrows() if row['ID']
        ]
    )

    if selected_scene:
        add_image_uploader(selected_scene)
        show_scene_images()


def main():
    """メイン関数."""
    st.set_page_config(layout="wide")
    st.title("Tale Forge - ゲームブックシナリオエディタ")

    initialize_session_state()

    tab1, tab2, tab3 = st.tabs(["シーン編集", "シーン関係図", "シナリオプレビュー"])

    with tab1:
        # インポート機能
        add_import_export_section()

        # データエディター
        edited_df = st.data_editor(
            st.session_state.data,
            use_container_width=True,
            num_rows="dynamic",
            height=300
        )

        # 保存とエクスポートボタン
        col1, col2 = st.columns(2)
        with col1:
            if st.button("編集内容を反映"):
                st.session_state.data = edited_df
                st.success("データが更新されました！")

        with col2:
            toml_string = export_to_toml(st.session_state.data)
            st.download_button(
                label="シナリオをファイルに保存",
                data=toml_string,
                file_name="scenario.toml",
                mime="application/toml"
            )

        # 画像管理セクション
        add_image_management()

    with tab2:
        if 'data' in st.session_state:
            graph = create_scene_graph(st.session_state.data)
            st.graphviz_chart(graph)

    with tab3:
        show_preview()


if __name__ == "__main__":
    main()