"""
シナリオプレビュー機能を提供するモジュール
"""
import os
import logging
import streamlit as st

logger = logging.getLogger(__name__)

def show_preview_tab():
    """シナリオプレビュータブの表示"""
    try:
        if 'current_scene' not in st.session_state:
            st.session_state.current_scene = 'BG'

        current_scene = st.session_state.data[st.session_state.data['ID'] == st.session_state.current_scene].iloc[0]
        st.subheader(f"シーン: {st.session_state.current_scene}")

        # 画像の有無で列のレイアウトを変更
        has_image = (st.session_state.current_scene in st.session_state.image_data and 
                    os.path.exists(st.session_state.image_data[st.session_state.current_scene]))

        if has_image:
            # 画像がある場合は2列レイアウト
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                # イメージの表示
                image_path = st.session_state.image_data[st.session_state.current_scene]
                st.image(image_path, use_container_width=True)

            with col2:
                # ストーリーテキストの表示
                story_text = str(current_scene['ストーリー']).strip()
                if story_text and story_text.lower() != 'none':
                    st.write(story_text)
                
                st.divider()  # 区切り線
                
                # 選択肢の表示
                st.subheader("選択肢:")
                _show_choices(current_scene)
        else:
            # 画像がない場合は1列レイアウト
            # ストーリーテキストの表示
            story_text = str(current_scene['ストーリー']).strip()
            if story_text and story_text.lower() != 'none':
                st.write(story_text)
            
            st.divider()  # 区切り線
            
            # 選択肢の表示
            st.subheader("選択肢:")
            _show_choices(current_scene)

    except Exception as e:
        logger.error(f"Error in preview: {str(e)}")
        st.error("シーンのプレビューに失敗しました。データを確認してください。")

def _show_choices(current_scene):
    """選択肢を表示する補助関数"""
    valid_choices = False  # 有効な選択肢があるかどうかのフラグ
    
    for i in range(1, 4):
        choice = str(current_scene[f'選択{i}']).strip()
        destination = str(current_scene[f'選択{i}遷移先']).strip()
        
        if (choice and destination and 
            choice.lower() != 'none' and 
            destination.lower() != 'none'):
            valid_choices = True
            button_key = f"choice_{st.session_state.current_scene}_{i}"
            if st.button(f"{choice}", key=button_key, use_container_width=True):
                st.session_state.current_scene = destination
                st.rerun()

    if not valid_choices:
        st.info("このシーンには選択肢がありません。")