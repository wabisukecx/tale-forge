# gameplay.py (メインモジュール)
"""ゲームプレイ機能を統括するメインモジュール"""
import streamlit as st
from character_sheet import (
    show_character_management, show_character_stats,
    show_dice_controls
)
from story_viewer import show_story_view

def show_gameplay_tab():
    """ゲームプレイタブの表示"""
    try:
        show_character_management()
        show_character_stats()
        show_dice_controls()
        
        st.divider()
        
        show_story_view()

        # JavaScriptを使用してページトップへスクロール
        js_code = """
            <script>
                window.scrollTo(0, 0);
            </script>
        """
        st.components.v1.html(js_code, height=0)

    except Exception as e:
        st.error(f"シーンの表示に失敗しました: {str(e)}")