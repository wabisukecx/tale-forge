"""
ゲームプレイ機能管理モジュール

インタラクティブなゲームブックアプリケーション用の
キャラクター管理、統計表示、ダイスコントロール、
ストーリービューを統括するモジュール。
"""

import streamlit as st

from character_sheet import (
    show_character_management,
    show_character_stats,
    show_dice_controls,
    show_notes
)
from story_viewer import show_story_view


def show_gameplay_tab():
    """
    ゲームプレイタブを表示する。

    この関数は以下のコンポーネントを順に表示する:
    - キャラクター管理
    - キャラクター統計
    - ダイスコントロール
    - メモ
    - ストーリービュー

    JavaScriptを使用してページトップにスクロールする機能も含む。
    """
    try:
        show_character_management()
        show_character_stats()
        show_dice_controls()
        show_notes()

        st.divider()

        show_story_view()

        # JavaScriptを使用してページトップへスクロール
        scroll_script = """
            <script>
                window.scrollTo(0, 0);
            </script>
        """
        st.components.v1.html(scroll_script, height=0)

    except Exception as e:
        st.error(f"シーンの表示に失敗しました: {str(e)}")