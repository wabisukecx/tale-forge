"""
TOML形式でのエクスポート/インポート機能を提供するモジュール
"""
import os
import toml
import pandas as pd
import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def export_to_toml(df, image_data):
    """DataFrameをTOML形式に変換

    Args:
        df (pd.DataFrame): 変換するDataFrame
        image_data (dict): 画像データの辞書

    Returns:
        str: TOML形式の文字列
    """
    logger.debug("Starting TOML export")
    logger.debug(f"DataFrame columns: {df.columns.tolist()}")
    logger.debug(f"DataFrame shape: {df.shape}")

    scenes = {}
    for _, row in df.iterrows():
        try:
            scene_id = str(row['ID']).strip()
            if not scene_id or scene_id.lower() == 'none':
                continue

            story = str(row['ストーリー']).strip()
            if not story or story.lower() == 'none':
                continue

            choices = []
            destinations = []
            for i in range(1, 4):
                choice_key = f'選択{i}'
                dest_key = f'選択{i}遷移先'
                
                if choice_key in row and dest_key in row:
                    choice = str(row[choice_key]).strip()
                    dest = str(row[dest_key]).strip()
                    
                    if (choice and dest and 
                        choice.lower() != 'none' and 
                        dest.lower() != 'none'):
                        choices.append(choice)
                        destinations.append(dest)

            scenes[scene_id] = {
                'story': story,
                'choices': choices,
                'destinations': destinations
            }

            # 画像パスの保存
            if scene_id in image_data:
                image_path = image_data[scene_id]
                # オリジナルのファイル拡張子を保持
                _, ext = os.path.splitext(image_path)
                scenes[scene_id]['image'] = f"images/{scene_id}{ext}"
                logger.debug(f"Added image path for scene {scene_id}: {scenes[scene_id]['image']}")

            logger.debug(f"Successfully processed scene {scene_id}")

        except Exception as e:
            logger.error(f"Error processing scene: {str(e)}")
            continue

    logger.debug(f"Total scenes processed: {len(scenes)}")
    return toml.dumps(scenes, encoder=toml.TomlEncoder())

def import_from_toml(toml_string):
    """TOML文字列からDataFrameを生成

    Args:
        toml_string (str): TOML形式の文字列

    Returns:
        tuple: (pd.DataFrame, dict) データフレームと画像データの辞書
    """
    try:
        logger.debug("Starting TOML import")
        data = toml.loads(toml_string)
        rows = []
        image_data = {}
        
        for scene_id, scene_data in data.items():
            try:
                if not isinstance(scene_data, dict):
                    logger.warning(f"Invalid scene data format for {scene_id}")
                    continue

                if not scene_data.get('story'):
                    logger.warning(f"Missing story for scene {scene_id}")
                    continue

                row = {
                    'ID': scene_id,
                    'ストーリー': scene_data.get('story', ''),
                }

                # 選択肢と遷移先の設定
                choices = scene_data.get('choices', [])
                destinations = scene_data.get('destinations', [])
                
                for i in range(1, 4):
                    row[f'選択{i}'] = choices[i-1] if i <= len(choices) else ''
                    row[f'選択{i}遷移先'] = destinations[i-1] if i <= len(destinations) else ''

                rows.append(row)

                # 画像パスの読み込み
                if 'image' in scene_data:
                    image_data[scene_id] = scene_data['image']

                logger.debug(f"Successfully imported scene {scene_id}")

            except Exception as e:
                logger.error(f"Error processing scene {scene_id}: {str(e)}")
                continue

        df = pd.DataFrame(rows)
        logger.debug(f"Created DataFrame with shape: {df.shape}")
        logger.debug(f"DataFrame columns: {df.columns.tolist()}")
        
        return df, image_data

    except Exception as e:
        logger.error(f"Error during TOML import: {str(e)}")
        raise Exception(f"TOMLファイルの読み込みに失敗しました: {str(e)}")