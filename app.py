"""
Tale Forge - ゲームブックシナリオエディタ
シナリオの作成、編集、プレビューを行うStreamlitアプリケーション
"""

from pathlib import Path
import pandas as pd
import streamlit as st

from editor import show_editor_tab
from graph import show_graph_tab
from gameplay import show_gameplay_tab
from toml_export import import_from_toml

# 選択肢の数を定数で管理
NUM_CHOICES = 3

def load_scenario_file(path):
    """シナリオファイルを読み込む"""
    try:
        scenario_content = path.read_text(encoding='utf-8')
        df, image_data = import_from_toml(scenario_content)
        return df, image_data
    except Exception:
        st.error("シナリオファイルの読み込みに失敗しました。")
        return None, None

def initialize_session_state():
    """セッション状態の初期化"""
    if 'data' not in st.session_state:
        default_scenario_path = Path('scenario.toml')
        if default_scenario_path.exists():
            df, image_data = load_scenario_file(default_scenario_path)
            if df is not None:
                st.session_state.data = df
                st.session_state.image_data = image_data
        else:
            # 新規データフレームを作成
            st.session_state.data = pd.DataFrame({
                'ID': ['BG'],
                'ストーリー': [''],
                **{f'選択{i}': [''] for i in range(1, NUM_CHOICES + 1)},
                **{f'選択{i}遷移先': [''] for i in range(1, NUM_CHOICES + 1)}
            })
            st.session_state.image_data = {}

def main():
    """メイン関数"""
    st.set_page_config(layout="wide")
    st.title("Tale Forge")

    # セッション状態の初期化
    initialize_session_state()

    # タブの作成と各機能の表示
    tab1, tab2, tab3 = st.tabs(["シーン編集", "シーン関係図", "ゲームブックを遊ぶ"])
    
    with tab1:
        show_editor_tab()
        
    with tab2:
        show_graph_tab()
        
    with tab3:
        show_gameplay_tab()

if __name__ == "__main__":
    main()