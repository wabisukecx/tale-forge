"""
シーン関係図機能を提供するモジュール
グラフの表示を改善し、より見やすく整理された形で表示する
"""
import graphviz
import streamlit as st
import pandas as pd

def process_value(value) -> str:
    """DataFrameの値を適切な文字列に変換する

    Args:
        value: DataFrameのセル値

    Returns:
        str: 処理された文字列
    """
    if pd.isna(value):
        return ""
    return str(value).strip()

def create_scene_graph(data: pd.DataFrame) -> graphviz.Digraph:
    """シーン関係図を生成する

    Args:
        data (pd.DataFrame): シーンデータを含むDataFrame

    Returns:
        graphviz.Digraph: 生成されたグラフ
    """
    # グラフの基本設定
    graph = graphviz.Digraph()
    graph.attr(
        rankdir='LR',
        splines='ortho',
        concentrate='true',
        nodesep='0.5',
        ranksep='1.0'
    )

    # ノードの属性を設定
    graph.attr('node',
        shape='rectangle',
        style='rounded,filled',
        fillcolor='lightgray',
        fontname='Helvetica',
        margin='0.2'
    )

    # エッジの属性を設定
    graph.attr('edge',
        fontname='Helvetica',
        fontsize='10',
        len='1.5'
    )

    # 有効なシーンIDを収集
    valid_scenes = set()
    destination_scenes = set()

    # まず全ての有効なシーンIDとその遷移先を収集
    for _, row in data.iterrows():
        scene_id = process_value(row['ID'])
        if not scene_id:
            continue
        
        valid_scenes.add(scene_id)
        
        # 遷移先を収集
        for i in range(1, 4):  # 選択肢1から3まで
            dest = process_value(row[f'選択{i}遷移先'])
            if dest:
                destination_scenes.add(dest)

    # 全ての関連シーンのノードを作成
    all_scenes = valid_scenes.union(destination_scenes)
    for scene_id in all_scenes:
        # シーンIDに対応するデータを探す
        scene_data = data[data['ID'].astype(str).str.strip() == scene_id]
        
        if not scene_data.empty:
            # ストーリーテキストの準備
            story = process_value(scene_data.iloc[0]['ストーリー'])
            story_preview = story[:20] + "..." if len(story) > 20 else story
            label = f"{scene_id}\n{story_preview}"
        else:
            # データが見つからない場合
            label = f"{scene_id}\n(未定義のシーン)"
            
        graph.node(scene_id, label)

    # エッジの作成
    for _, row in data.iterrows():
        scene_id = process_value(row['ID'])
        if not scene_id:
            continue

        # 各選択肢についてエッジを追加
        for i in range(1, 4):
            choice = process_value(row[f'選択{i}'])
            dest = process_value(row[f'選択{i}遷移先'])

            if choice and dest:
                choice_preview = choice[:15] + "..." if len(choice) > 15 else choice
                graph.edge(
                    scene_id,
                    dest,
                    choice_preview,
                    tooltip=choice
                )

    return graph

def show_graph_tab():
    """シーン関係図タブの表示"""
    try:
        st.subheader("シーン関係図")
        
        # データの存在確認
        if 'data' not in st.session_state:
            st.error("シナリオデータが読み込まれていません。")
            return
            
        # グラフの生成と表示
        graph = create_scene_graph(st.session_state.data)
        st.graphviz_chart(graph)
        
        # 使用方法の説明
        with st.expander("グラフの見方"):
            st.markdown("""
            - グラフは左から右に読みます
            - 各ノードはシーンを表し、シーンIDとストーリーの冒頭を表示しています
            - 矢印は選択肢を表し、選択肢のテキストが表示されています
            - 未定義のシーンは「(未定義のシーン)」と表示されます
            - ノードやエッジにカーソルを合わせると詳細が表示されます
            """)
        
    except Exception as e:
        st.error(f"シーン関係図の生成に失敗しました: {str(e)}")
        st.exception(e)  # デバッグ情報の表示