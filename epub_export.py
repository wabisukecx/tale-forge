"""
EPUB3形式でのエクスポート機能を提供するモジュール
改善版：縦書きレイアウト、フォント、デザインの強化
"""
import os
import shutil
import tempfile
from ebooklib import epub
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_style_sheet():
    """EPUBのスタイルシートを生成"""
    return '''
        @charset "UTF-8";

        /* 基本スタイル - 横書き */
        .horizontal {
            font-family: "Noto Serif CJK JP", "Yu Mincho", "Hiragino Mincho ProN", serif;
            margin: 5% 3%;
            line-height: 1.8;
            font-size: 1em;
            color: #2C3E50;
        }

        /* 縦書きレイアウト */
        .vertical {
            font-family: "Noto Serif CJK JP", "Yu Mincho", "Hiragino Mincho ProN", serif;
            writing-mode: vertical-rl;
            -webkit-writing-mode: vertical-rl;
            -epub-writing-mode: vertical-rl;
            text-orientation: upright;
            -webkit-text-orientation: upright;
            -epub-text-orientation: upright;
            margin: 3% 5%;
            line-height: 2;
            font-size: 1em;
        }

        /* 共通のヘッダースタイル */
        h1 {
            font-family: "Noto Sans CJK JP", "Yu Gothic", sans-serif;
            color: #34495E;
            margin: 1em 0;
            font-size: 1.5em;
            font-weight: bold;
            letter-spacing: 0.1em;
        }

        /* シーンコンテンツのスタイル */
        .scene-content {
            margin: 2em 0;
            padding: 1em;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 0.5em;
        }

        /* 選択肢のスタイル */
        .choices {
            margin: 2em 0;
            padding: 1.5em;
            background: #F7F9FA;
            border-radius: 0.5em;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .choice {
            margin: 1em 0;
            padding: 1em;
            background: white;
            border-left: 4px solid #3498DB;
            transition: all 0.3s ease;
        }

        .choice a {
            color: #2980B9;
            text-decoration: none;
            font-weight: 500;
        }

        .choice:hover {
            background: #F5F9FA;
            border-left-color: #2574A9;
        }

        /* 画像のスタイル */
        .scene-image {
            text-align: center;
            margin: 2em 0;
        }

        .scene-image img {
            max-width: 100%;
            height: auto;
            border-radius: 0.5em;
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        }

        /* ページブレークの制御 */
        .scene {
            page-break-before: always;
        }

        /* 装飾的な要素 */
        .scene-divider {
            text-align: center;
            margin: 2em 0;
            color: #95A5A6;
            font-size: 1.5em;
        }

        .scene-divider::before {
            content: "❧";
        }
    '''

def create_xhtml_content(scene_id, story, choices, image_path=None, vertical=False):
    """EPUBチャプターのXHTMLコンテンツを生成"""
    layout_class = "vertical" if vertical else "horizontal"
    
    content = []
    content.append(f'''<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>シーン {scene_id}</title>
</head>
<body class="{layout_class}">''')
    
    content.append(f'<div class="scene" id="scene_{scene_id}">')
    content.append(f'<h1>シーン {scene_id}</h1>')

    # 画像の追加
    if image_path and os.path.exists(image_path):
        image_name = os.path.basename(image_path)
        content.append(f'<div class="scene-image"><img src="images/{image_name}" alt="シーン {scene_id}"/></div>')

    # ストーリー内容
    story_text = str(story).strip().replace('\n', '<br/>')
    content.append(f'<div class="scene-content"><p>{story_text}</p></div>')

    # 区切り要素
    content.append('<div class="scene-divider"></div>')

    # 選択肢
    if choices:
        content.append('<div class="choices">')
        for choice in choices:
            if choice.get("text") and choice.get("destination"):
                content.append(
                    f'<div class="choice"><a href="scene_{choice["destination"]}.xhtml">{choice["text"]}</a></div>'
                )
        content.append('</div>')

    content.append('</div></body></html>')
    return '\n'.join(content)

def export_to_epub(df, image_data, title="ゲームブック", vertical=False):
    """データフレームをEPUB3形式に変換"""
    logger.info("Starting EPUB export with enhanced styling")
    book = epub.EpubBook()
    
    # メタデータ設定
    book.set_identifier('id123456')
    book.set_title(title)
    book.set_language('ja')
    
    # スタイルシートの追加
    style = epub.EpubItem(
        uid="style_default",
        file_name="style/default.css",
        media_type="text/css",
        content=create_style_sheet()
    )
    book.add_item(style)
    
    chapters = []
    
    # シーンの処理
    for _, row in df.iterrows():
        try:
            scene_id = str(row['ID']).strip()
            if not scene_id or scene_id.lower() == 'none':
                continue

            story = str(row['ストーリー']).strip()
            if not story or story.lower() == 'none':
                continue

            logger.debug(f"Processing scene {scene_id}")

            # 選択肢の処理
            choices = []
            for i in range(1, 4):
                choice_text = str(row[f'選択{i}']).strip()
                destination = str(row[f'選択{i}遷移先']).strip()
                
                if (choice_text and destination and 
                    choice_text.lower() != 'none' and 
                    destination.lower() != 'none'):
                    choices.append({
                        'text': choice_text,
                        'destination': destination
                    })

            # 画像の処理
            image_path = image_data.get(scene_id)
            if image_path and os.path.exists(image_path):
                try:
                    image_name = os.path.basename(image_path)
                    with open(image_path, 'rb') as img_file:
                        image_item = epub.EpubItem(
                            uid=f'image_{scene_id}',
                            file_name=f'images/{image_name}',
                            media_type='image/jpeg',
                            content=img_file.read()
                        )
                        book.add_item(image_item)
                        logger.debug(f"Added image for scene {scene_id}")
                except Exception as e:
                    logger.error(f"Error adding image for scene {scene_id}: {str(e)}")

            # チャプター内容の生成
            content = create_xhtml_content(scene_id, story, choices, image_path, vertical)
            
            # チャプターの作成
            chapter = epub.EpubHtml(
                title=f'シーン {scene_id}',
                file_name=f'scene_{scene_id}.xhtml',
                lang='ja',
                content=content
            )
            chapter.add_item(style)
            book.add_item(chapter)
            chapters.append(chapter)
            logger.debug(f"Added chapter for scene {scene_id}")

        except Exception as e:
            logger.error(f"Error processing scene {scene_id}: {str(e)}")
            continue

    if not chapters:
        raise ValueError("有効なチャプターが見つかりませんでした。データを確認してください。")

    logger.info(f"Created {len(chapters)} chapters")

    # 目次とナビゲーション
    book.toc = [(epub.Section('シーン'), chapters)]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapters
    
    # EPUB生成
    temp_dir = tempfile.mkdtemp()
    epub_path = os.path.join(temp_dir, 'game_book.epub')
    
    try:
        logger.info("Writing EPUB file")
        epub.write_epub(epub_path, book, {})
        
        with open(epub_path, 'rb') as f:
            epub_data = f.read()
        
        logger.info("Successfully created EPUB file")
        return epub_data
    
    finally:
        shutil.rmtree(temp_dir)