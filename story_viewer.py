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

def prepare_svg_content(svg_content):
    """SVGコンテンツを表示用に準備する"""
    # width/height属性を削除（viewBoxに依存するため）
    svg_content = re.sub(r'width=["\'][^"\']*["\']', '', svg_content)
    svg_content = re.sub(r'height=["\'][^"\']*["\']', '', svg_content)
    
    # style属性を追加してレスポンシブ対応
    svg_content = svg_content.replace('<svg ', '<svg style="width: 100%; height: 100%; display: block;" ')
    return svg_content

def show_scene_image(image_path):
    """シーン画像の表示"""
    try:
        if not os.path.exists(image_path):
            return
            
        if image_path.lower().endswith('.svg'):
            with open(image_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
                # SVGのサイズを取得
                width, height = get_svg_dimensions(svg_content)
                # アスペクト比を維持しながら表示サイズを調整
                container_width = 500  # コンテナの幅
                scale = container_width / width
                display_height = int(height * scale)
                                
                # SVGを包むdivスタイルを設定
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

def get_scene(df, scene_id):
    """シーンデータを取得する"""
    try:
        scene_id_str = str(scene_id)
        matching_scenes = df[df['ID'].astype(str) == scene_id_str]
        
        if matching_scenes.empty:
            st.error(f"シーン {scene_id} が見つかりません。")
            return None
            
        return matching_scenes.iloc[0]
    except Exception as e:
        st.error(f"シーンデータの取得に失敗しました: {e}")
        return None

def show_story_content(scene_data):
    """ストーリーコンテンツの表示"""
    if scene_data is None:
        return
    
    # ストーリーテキストの表示
    story_text = str(scene_data['ストーリー']).strip()
    if story_text and story_text.lower() != 'none':
        st.markdown(story_text)
    
    st.divider()
    
    # 選択肢の表示
    for i in range(1, 4):
        choice_key = f'選択{i}'
        dest_key = f'選択{i}遷移先'
        
        if choice_key in scene_data.index and dest_key in scene_data.index:
            choice = str(scene_data[choice_key]).strip()
            destination = str(scene_data[dest_key]).strip()
            
            if (choice and destination and 
                choice.lower() != 'none' and 
                destination.lower() != 'none'):
                if st.button(f"{choice}", key=f"choice_{st.session_state.current_scene}_{i}"):
                    st.session_state.current_scene = destination
                    st.rerun()

def show_story_view():
    """シナリオビューを表示"""
    try:
        # 初期シーンの設定
        if 'current_scene' not in st.session_state:
            st.session_state.current_scene = 'BG'

        # データの存在チェック
        if 'data' not in st.session_state:
            st.error("シナリオデータが読み込まれていません。")
            return

        # 現在のシーンデータを取得
        current_scene = get_scene(st.session_state.data, st.session_state.current_scene)
        if current_scene is None:
            return

        st.subheader(f"シーン {st.session_state.current_scene}")

        # 画像の有無をチェック
        image_path = st.session_state.image_data.get(st.session_state.current_scene)
        has_image = image_path and os.path.exists(image_path)

        # レイアウトの表示
        if has_image:
            cols = st.columns([1, 1])
            with cols[0]:
                show_scene_image(image_path)
            with cols[1]:
                show_story_content(current_scene)
        else:
            show_story_content(current_scene)
            
    except Exception as e:
        st.error(f"シーンの表示中にエラーが発生しました: {str(e)}")