"""
キャラクターシート管理モジュール

インタラクティブなゲームブックアプリケーション用の
キャラクターの統計生成、管理、ダイスロール、メモ機能を提供するモジュール。
"""

import random
import streamlit as st
import toml
from pathlib import Path


def load_settings():
    """
    設定ファイル（settings.toml）から設定を読み込む。

    戻り値:
        bool: 恐怖値メカニクスが有効かどうか。
    """
    try:
        settings_path = Path('settings.toml')
        if settings_path.exists():
            settings = toml.load(settings_path)
            return settings.get('show_fear', False)
    except Exception:
        pass
    return False


def roll_dice(num_dice=2):
    """
    指定された数のサイコロを振る。

    引数:
        num_dice (int, オプション): 振るサイコロの数。デフォルトは2。

    戻り値:
        list: サイコロロールの結果のリスト。
    """
    return [random.randint(1, 6) for _ in range(num_dice)]


def generate_initial_stats():
    """
    サイコロロールに基づいて初期キャラクター統計を生成する。

    戻り値:
        tuple: 生成された統計とその統計を得たサイコロロールのタプル。
    """
    skill_rolls = roll_dice()
    stamina_rolls = roll_dice()
    luck_rolls = roll_dice()
    fear_rolls = roll_dice() if st.session_state.show_fear else None

    stats = {
        'skill': {
            'initial': sum(skill_rolls) + 6,
            'current': sum(skill_rolls) + 6
        },
        'stamina': {
            'initial': sum(stamina_rolls) + 12,
            'current': sum(stamina_rolls) + 12
        },
        'luck': {
            'initial': sum(luck_rolls) + 6,
            'current': sum(luck_rolls) + 6
        }
    }

    rolls = {
        'skill': skill_rolls,
        'stamina': stamina_rolls,
        'luck': luck_rolls,
    }

    if st.session_state.show_fear:
        stats['fear'] = {
            'max': sum(fear_rolls) + 3,
            'current': 0
        }
        rolls['fear'] = fear_rolls

    return stats, rolls


def initialize_character_if_needed():
    """
    セッション状態にキャラクター情報がない場合に初期化する。
    """
    # 設定の読み込みと恐怖値の初期化
    if 'show_fear' not in st.session_state:
        st.session_state.show_fear = load_settings()

    # キャラクターが存在しない場合の初期化
    if 'character' not in st.session_state:
        initial_stats = {
            'name': '',
            'skill': {'initial': 0, 'current': 0},
            'stamina': {'initial': 0, 'current': 0},
            'luck': {'initial': 0, 'current': 0},
            'notes': ''  # 所持品とヒントを統合したメモ欄
        }
        if st.session_state.show_fear:
            initial_stats['fear'] = {'max': 0, 'current': 0}
        st.session_state.character = initial_stats


def show_character_management():
    """
    キャラクター作成のためのUI管理機能を表示する。
    キャラクターの初期化と名前入力を行う。
    """
    # キャラクターの初期化
    initialize_character_if_needed()

    # キャラクター名の入力
    st.session_state.character['name'] = st.text_input(
        "キャラクター名", 
        st.session_state.character['name']
    )

    # 能力値生成ボタン
    if st.button("能力値を決定"):
        stats, _ = generate_initial_stats()
        st.session_state.character.update(stats)


def modify_stat(stat_name, value):
    """
    定められた制約内でキャラクターの能力値を変更する。

    引数:
        stat_name (str): 変更する能力値の名前。
        value (int): 現在の能力値に加える値。
    """
    char = st.session_state.character

    if stat_name == 'fear':
        # 恐怖値は0から最大値の間で変動
        new_value = max(0, min(char['fear']['max'], char['fear']['current'] + value))
        char['fear']['current'] = new_value
    else:
        # 他の能力値は初期値を超えない
        current_max = char[stat_name]['initial']
        new_value = min(current_max, char[stat_name]['current'] + value)
        # 値が0未満にならないようにする
        new_value = max(0, new_value)
        char[stat_name]['current'] = new_value


def show_character_stats():
    """
    キャラクターの能力値を表示し、変更を可能にする。
    """
    # キャラクターの初期化
    initialize_character_if_needed()

    char = st.session_state.character
    if not char['name']:
        return

    # 表示する能力値の定義
    stats_to_show = [
        ('skill', '技能値 (SKILL)'),
        ('stamina', '体力値 (STAMINA)'),
        ('luck', '幸運値 (LUCK)'),
    ]

    # 恐怖値が有効な場合に追加
    if st.session_state.show_fear:
        stats_to_show.append(('fear', '恐怖値 (FEAR)'))

    # 能力値表示用のカラムを作成
    cols = st.columns(len(stats_to_show))

    for idx, (stat_name, label) in enumerate(stats_to_show):
        with cols[idx]:
            # 能力値の表示
            if stat_name == 'fear':
                value = f"{char[stat_name]['current']}/{char[stat_name]['max']}"
            else:
                value = f"{char[stat_name]['current']}/{char[stat_name]['initial']}"
            st.metric(label, value)

            # 能力値変更ボタンの作成
            col1, col2 = st.columns(2)
            with col1:
                if st.button("-1", key=f"dec_{stat_name}"):
                    modify_stat(stat_name, -1)
                    st.rerun()
            with col2:
                if st.button("+1", key=f"inc_{stat_name}"):
                    modify_stat(stat_name, 1)
                    st.rerun()


def show_notes():
    """
    所持品とヒントの統合メモ機能を表示する。
    """
    # キャラクターの初期化
    initialize_character_if_needed()

    char = st.session_state.character
    if not char['name']:
        return

    # メモエリア
    char['notes'] = st.text_area(
        "所持品、ヒント、その他の重要な情報をメモ", 
        value=char.get('notes', ''),
        key="character_notes",
        height=68
    )


def show_dice_controls():
    """
    ゲームプレイ用のダイスロールコントロールを表示する。
    """
    # キャラクターの初期化
    initialize_character_if_needed()

    char = st.session_state.character
    if not char['name']:
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
            current_luck = char['luck']['current']
            result = "成功！" if total <= current_luck else "失敗..."
            st.write(f"🎲 {rolls[0]} + {rolls[1]} = {total} ({result})")

    with col3:
        if st.button("d6を振る"):
            roll = random.randint(1, 6)
            st.write(f"🎲 {roll}")