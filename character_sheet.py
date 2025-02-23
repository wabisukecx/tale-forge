import streamlit as st
import random
import toml
from pathlib import Path

def load_settings():
    """設定ファイルを読み込む"""
    try:
        settings_path = Path('settings.toml')
        if settings_path.exists():
            settings = toml.load(settings_path)
            return settings.get('show_fear', False)
    except Exception:
        pass
    return False

def roll_dice(num_dice=2):
    """指定された数のダイスを振る"""
    return [random.randint(1, 6) for _ in range(num_dice)]

def generate_initial_stats():
    """初期能力値を生成"""
    skill_rolls = roll_dice()
    stamina_rolls = roll_dice()
    luck_rolls = roll_dice()
    fear_rolls = roll_dice() if st.session_state.show_fear else None
    
    stats = {
        'skill': {'initial': sum(skill_rolls) + 6, 'current': sum(skill_rolls) + 6},
        'stamina': {'initial': sum(stamina_rolls) + 12, 'current': sum(stamina_rolls) + 12},
        'luck': {'initial': sum(luck_rolls) + 6, 'current': sum(luck_rolls) + 6},
    }
    
    rolls = {
        'skill': skill_rolls,
        'stamina': stamina_rolls,
        'luck': luck_rolls,
    }

    if st.session_state.show_fear:
        stats['fear'] = {'max': sum(fear_rolls) + 3, 'current': 0}
        rolls['fear'] = fear_rolls
    
    return stats, rolls

def show_character_management():
    """キャラクター作成UIの表示"""
    # 設定の読み込みと保存
    if 'show_fear' not in st.session_state:
        st.session_state.show_fear = load_settings()
    
    if 'character' not in st.session_state:
        initial_stats = {
            'name': '',
            'skill': {'initial': 0, 'current': 0},
            'stamina': {'initial': 0, 'current': 0},
            'luck': {'initial': 0, 'current': 0},
        }
        if st.session_state.show_fear:
            initial_stats['fear'] = {'max': 0, 'current': 0}
        st.session_state.character = initial_stats

    # キャラクター名入力
    st.session_state.character['name'] = st.text_input("キャラクター名", st.session_state.character['name'])

    # 能力値生成ボタン
    if st.button("能力値を決定"):
        stats, rolls = generate_initial_stats()
        st.session_state.character.update(stats)

def modify_stat(stat_name, value):
    """能力値を変更（上限を超えない）"""
    char = st.session_state.character
    
    if stat_name == 'fear':
        # 恐怖値は0から最大値の間
        new_value = max(0, min(char['fear']['max'], char['fear']['current'] + value))
        char['fear']['current'] = new_value
    else:
        # その他の能力値は初期値を超えない
        current_max = char[stat_name]['initial']
        new_value = min(current_max, char[stat_name]['current'] + value)
        # 下限は0
        new_value = max(0, new_value)
        char[stat_name]['current'] = new_value

def show_character_stats():
    """キャラクターステータスの表示"""
    if 'character' not in st.session_state:
        return

    char = st.session_state.character
    if not char['name']:
        return
    
    # 基本能力値の表示と調整
    stats_to_show = [
        ('skill', '技能値 (SKILL)'),
        ('stamina', '体力値 (STAMINA)'),
        ('luck', '幸運値 (LUCK)'),
    ]
    
    # 恐怖値が有効な場合は追加
    if st.session_state.show_fear:
        stats_to_show.append(('fear', '恐怖値 (FEAR)'))
    
    # 全ステータスを横に並べて表示
    cols = st.columns(len(stats_to_show))
    
    for idx, (stat_name, label) in enumerate(stats_to_show):
        with cols[idx]:
            if stat_name == 'fear':
                value = f"{char[stat_name]['current']}/{char[stat_name]['max']}"
            else:
                value = f"{char[stat_name]['current']}/{char[stat_name]['initial']}"
            st.metric(label, value)
            
            # ±ボタンを横に並べる
            col1, col2 = st.columns(2)
            with col1:
                if st.button("-1", key=f"dec_{stat_name}"):
                    modify_stat(stat_name, -1)
                    st.rerun()
            with col2:
                if st.button("+1", key=f"inc_{stat_name}"):
                    modify_stat(stat_name, 1)
                    st.rerun()

def show_dice_controls():
    """ダイスロール機能の表示"""
    if 'character' not in st.session_state or not st.session_state.character['name']:
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("戦闘ロール (2d6)"):
            rolls = roll_dice()
            total = sum(rolls)
            st.write(f"🎲 {rolls[0]} + {rolls[1]} = {total}")
    
    with col2:
        if st.button("幸運判定 (2d6)"):
            rolls = roll_dice()
            total = sum(rolls)
            current_luck = st.session_state.character['luck']['current']
            result = "成功！" if total <= current_luck else "失敗..."
            st.write(f"🎲 {rolls[0]} + {rolls[1]} = {total} ({result})")
    
    with col3:
        if st.button("d6を振る"):
            roll = random.randint(1, 6)
            st.write(f"🎲 {roll}")