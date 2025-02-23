# character_sheet.py
"""キャラクターシート関連の機能を提供するモジュール"""
import random
import streamlit as st
import toml
from pathlib import Path

def display_dice(value):
    """サイコロの目を表示する"""
    dice_faces = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
    return dice_faces.get(value, "")

def load_saved_characters():
    """保存されているキャラクター情報を読み込む"""
    save_file = Path("characters.toml")
    if save_file.exists():
        with open(save_file, "r", encoding="utf-8") as f:
            return toml.load(f)
    return {}

def save_characters(characters):
    """キャラクター情報を保存する"""
    with open("characters.toml", "w", encoding="utf-8") as f:
        toml.dump(characters, f)

def save_current_character(character_name):
    """現在のキャラクター情報を保存する"""
    saved_characters = load_saved_characters()
    saved_characters[character_name] = {
        "name": character_name,
        "skill_initial": st.session_state.get('skill_initial', 0),
        "skill_current": st.session_state.get('skill_current', 0),
        "stamina_initial": st.session_state.get('stamina_initial', 0),
        "stamina_current": st.session_state.get('stamina_current', 0),
        "luck_initial": st.session_state.get('luck_initial', 0),
        "luck_current": st.session_state.get('luck_current', 0),
        "fear_max": st.session_state.get('fear_max', 0),
        "fear_current": st.session_state.get('fear_current', 0)
    }
    save_characters(saved_characters)

def load_character(character_data):
    """保存されているキャラクター情報をロードする"""
    for key, value in character_data.items():
        st.session_state[key] = value

def show_character_management():
    """キャラクター管理UIの表示"""
    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
    
    with col1:
        character_name = st.text_input("キャラクター名", 
                                     value=st.session_state.get('character_name', ''), 
                                     label_visibility="collapsed")
        st.session_state.character_name = character_name

    with col2:
        if st.button("🎲 生成", use_container_width=True):
            generate_new_character()

    with col3:
        if st.button("💾 保存", use_container_width=True) and character_name:
            save_current_character(character_name)

    with col4:
        show_character_selector()

def generate_new_character():
    """新しいキャラクターを生成する"""
    st.session_state.is_generating = True
    for key in list(st.session_state.keys()):
        if key not in ['data', 'image_data', 'current_scene', 'is_generating']:
            del st.session_state[key]
    
    st.session_state.update({
        'skill_initial': random.randint(1, 6) + 6,
        'stamina_initial': sum(random.randint(1, 6) for _ in range(2)) + 12,
        'luck_initial': random.randint(1, 6) + 6,
        'fear_max': random.randint(1, 6) + 6,
        'character_name': ""
    })
    
    # 現在値を初期値と同じに設定
    for stat in ['skill', 'stamina', 'luck']:
        st.session_state[f'{stat}_current'] = st.session_state[f'{stat}_initial']
    st.session_state.fear_current = 0
    
    st.rerun()

def show_character_selector():
    """保存済みキャラクター選択UIの表示"""
    saved_characters = load_saved_characters()
    if saved_characters:
        character_options = ["選択してください"] + list(saved_characters.keys())
        selected_character = st.selectbox("保存済み", character_options, 
                                        label_visibility="collapsed")
        if selected_character != "選択してください":
            load_character(saved_characters[selected_character])

def show_character_stats():
    """キャラクターステータスUIの表示"""
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    stats = [
        ("技能", "skill", 12),
        ("体力", "stamina", 24),
        ("幸運", "luck", 12),
        ("恐怖", "fear", 12)
    ]
    
    columns = [stats_col1, stats_col2, stats_col3, stats_col4]
    
    for (stat_name, stat_key, max_value), col in zip(stats, columns):
        with col:
            show_stat_input(stat_name, stat_key, max_value)

def show_stat_input(stat_name, stat_key, max_value):
    """個別のステータス入力UIを表示"""
    st.markdown(f"**{stat_name}**")
    
    if stat_key != "fear":
        initial = st.number_input(
            "初期値",
            key=f"{stat_key}_initial_display",
            value=st.session_state.get(f'{stat_key}_initial', 0),
            disabled=True,
            min_value=0,
            max_value=max_value
        )
        current = st.number_input(
            "現在値",
            key=f"{stat_key}_current_input",
            value=st.session_state.get(f'{stat_key}_current', 0),
            min_value=0,
            max_value=initial
        )
        st.session_state[f'{stat_key}_current'] = current
    else:
        max_fear = st.number_input(
            "上限",
            key="fear_max_display",
            value=st.session_state.get('fear_max', 0),
            disabled=True,
            min_value=0,
            max_value=max_value
        )
        current = st.number_input(
            "現在値",
            key="fear_current_input",
            value=st.session_state.get('fear_current', 0),
            min_value=0,
            max_value=max_fear
        )
        st.session_state.fear_current = current

def show_dice_controls():
    """サイコロ制御UIの表示"""
    dice_col1, dice_col2, dice_col3 = st.columns([1, 1, 4])
    
    with dice_col1:
        if st.button("1D6", use_container_width=True):
            st.session_state.dice_results = [random.randint(1, 6)]
            st.rerun()
    
    with dice_col2:
        if st.button("2D6", use_container_width=True):
            st.session_state.dice_results = [random.randint(1, 6) for _ in range(2)]
            st.rerun()

    with dice_col3:
        show_dice_results()

def show_dice_results():
    """サイコロ結果の表示"""
    if 'dice_results' in st.session_state and st.session_state.dice_results:
        results = st.session_state.dice_results
        dice_faces = " ".join(display_dice(r) for r in results)
        total = sum(results)
        st.markdown(f"#### {dice_faces} = {total}")