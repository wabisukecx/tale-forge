"""
シーン編集機能を提供するモジュール
"""
import os
import streamlit as st
from toml_export import export_to_toml, import_from_toml
import re

def get_svg_dimensions(svg_content):
    """SVGファイルからviewBox属性を取得し、適切なサイズを計算する"""
    viewbox_match = re.search(r'viewBox=["\']([-\d\s,.]+)["\']', svg_content)
    if viewbox_match:
        viewbox = viewbox_match.group(1).split()
        if len(viewbox) == 4:
            width = float(viewbox[2])
            height = float(viewbox[3])
            return width, height
    
    # viewBoxが見つからない場合は、width/height属性を探す
    width_match = re.search(r'width=["\']([\d.]+)["\']', svg_content)
    height_match = re.search(r'height=["\']([\d.]+)["\']', svg_content)
    
    width = float(width_match.group(1)) if width_match else 300
    height = float(height_match.group(1)) if height_match else 300
    
    return width, height

def save_image(image_file, scene_id):
    """画像を保存し、パスを返す"""
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

def save_scenario_toml(df, image_data):
    """シナリオをTOMLファイルに保存"""
    try:
        toml_string = export_to_toml(df, image_data)
        with open("scenario.toml", "w", encoding='utf-8') as f:
            f.write(toml_string)
        return True
    except Exception as e:
        st.error(f"TOMLファイルの保存中にエラーが発生しました: {str(e)}")
        return False

def show_editor_tab():
    """シーン編集タブの表示"""
    # インポート機能
    uploaded_file = st.file_uploader("TOMLファイルをインポート", type=['toml'])
    if uploaded_file is not None:
        try:
            toml_content = uploaded_file.read().decode('utf-8')
            df, image_data = import_from_toml(toml_content)
            if df is not None:
                st.session_state.data = df
                st.session_state.image_data.update(image_data)
                st.success("TOMLファイルを正常にインポートしました！")
        except Exception as e:
            st.error(f"TOMLファイルの読み込みに失敗しました: {str(e)}")

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
            # 編集内容を反映したらscenario.tomlにも自動保存
            if save_scenario_toml(edited_df, st.session_state.image_data):
                st.success("データが更新され、scenario.tomlに保存されました！")
            else:
                st.warning("データは更新されましたが、scenario.tomlの保存に失敗しました。")

    with col2:
        try:
            toml_string = export_to_toml(edited_df, st.session_state.image_data)
            st.download_button(
                label="TOMLファイルをダウンロード",
                data=toml_string,
                file_name="scenario.toml",
                mime="application/toml"
            )
        except Exception as e:
            st.error(f"TOMLの生成に失敗しました: {str(e)}")

    # 画像管理セクション
    st.subheader("画像管理")
    selected_scene = st.selectbox(
        "画像を追加するシーンを選択",
        options=[row['ID'] for _, row in edited_df.iterrows() if row['ID']]
    )

    if selected_scene:
        image_file = st.file_uploader(
            f"シーン {selected_scene} の画像をアップロード",
            type=['png', 'jpg', 'jpeg', 'svg'],
            key=f"image_{selected_scene}"
        )
        
        if image_file:
            saved_path = save_image(image_file, selected_scene)
            if saved_path:
                st.session_state.image_data[selected_scene] = saved_path
                # 画像を追加したらscenario.tomlにも自動保存
                if save_scenario_toml(edited_df, st.session_state.image_data):
                    st.success("画像が追加され、scenario.tomlに保存されました！")
                else:
                    st.warning("画像は追加されましたが、scenario.tomlの保存に失敗しました。")

    # 保存済み画像の表示
    if st.session_state.image_data:
        st.subheader("登録済みの画像")
        cols = st.columns(3)
        for i, (scene_id, image_path) in enumerate(st.session_state.image_data.items()):
            with cols[i % 3]:
                try:
                    if os.path.exists(image_path):
                        if image_path.lower().endswith('.svg'):
                            with open(image_path, 'r', encoding='utf-8') as f:
                                svg_content = f.read()
                                # SVGのサイズを取得
                                width, height = get_svg_dimensions(svg_content)
                                # アスペクト比を維持しながら表示サイズを調整
                                container_width = 300  # コンテナの幅
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
                            st.image(image_path, caption=f"シーン {scene_id}", use_container_width=True)
                        
                        if st.button(f"削除 (シーン {scene_id})", key=f"del_{scene_id}"):
                            os.remove(image_path)
                            del st.session_state.image_data[scene_id]
                            # 画像を削除したらscenario.tomlにも自動保存
                            if save_scenario_toml(edited_df, st.session_state.image_data):
                                st.success("画像が削除され、scenario.tomlが更新されました！")
                            else:
                                st.warning("画像は削除されましたが、scenario.tomlの更新に失敗しました。")
                            st.rerun()
                    else:
                        st.error(f"画像ファイルが見つかりません: {image_path}")
                except Exception as e:
                    st.error(f"画像の表示中にエラーが発生しました: {str(e)}")