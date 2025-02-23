# story_viewer.py
"""ストーリービューア関連の機能を提供するモジュール"""
import os
import streamlit as st
import re

def get_svg_dimensions(svg_content):
    """SVGファイルからviewBox属性を取得し、適切なサイズを計算する"""
    viewbox_match = re.search(r'viewBox=["\']([-\d\s,.]+)["\']', svg_content)
    if viewbox_match:
        viewbox = viewbox_match.group(1).split()
        if len(viewbox) == 4:
            return float(viewbox[2]), float(viewbox[3])
    
    width_match = re.search(r'width=["\']([\d.]+)["\']', svg_content)
    height_match = re.search(r'height=["\']([\d.]+)["\']', svg_content)
    
    width = float(width_match.group(1)) if width_match else 300
    height = float(height_match.group(1)) if height_match else 300
    
    return width, height

def show_scene_image(image_path):
    """シーン画像の表示"""
    try:
        if image_path.lower().endswith('.svg'):
            with open(image_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
                width, height = get_svg_dimensions(svg_content)
                container_width = 600
                scale = container_width / width
                display_height = int(height * scale)
                
                wrapper_style = f"""
                    <div style="width: {container_width}px; 
                              height: {display_height}px; 
                              overflow: hidden;">
                        <div style="width: 100%; 
                                  height: 100%; 
                                  display: flex; 
                                  justify-content: center; 
                                  align-items: center;">
                            {svg_content}
                        </div>
                    </div>
                """
                st.components.v1.html(wrapper_style, height=display_height)
        else:
            st.image(image_path, use_container_width=True)
    except Exception as e:
        st.error(f"画像の読み込みに失敗しました: {e}")

def show_story_content(current_scene):
    """ストーリーコンテンツの表示"""
    story_text = str(current_scene['ストーリー']).strip()
    if story_text and story_text.lower() != 'none':
        st.write(story_text)
    
    st.divider()
    
    show_choices(current_scene)

def show_choices(current_scene):
    """選択肢の表示"""
    for i in range(1, 4):
        choice = str(current_scene[f'選択{i}']).strip()
        destination = str(current_scene[f'選択{i}遷移先']).strip()
        
        if (choice and destination and 
            choice.lower() != 'none' and 
            destination.lower() != 'none'):
            if st.button(f"{choice}", key=f"choice_{st.session_state.current_scene}_{i}"):
                st.session_state.current_scene = destination
                st.rerun()

def show_story_view():
    """シナリオビューを表示"""
    if 'current_scene' not in st.session_state:
        st.session_state.current_scene = 'BG'

    current_scene = st.session_state.data[
        st.session_state.data['ID'] == st.session_state.current_scene
    ].iloc[0]

    st.subheader(f"{st.session_state.current_scene}")

    has_image = (
        st.session_state.current_scene in st.session_state.image_data and 
        os.path.exists(st.session_state.image_data[st.session_state.current_scene])
    )

    if has_image:
        cols = st.columns([1, 1])
        with cols[0]:
            show_scene_image(st.session_state.image_data[st.session_state.current_scene])
        with cols[1]:
            show_story_content(current_scene)
    else:
        show_story_content(current_scene)