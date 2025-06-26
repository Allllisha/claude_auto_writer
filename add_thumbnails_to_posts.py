#!/usr/bin/env python3
"""
投稿済み記事にサムネイルを追加するスクリプト
"""

import os
import sys
import requests
import logging
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import io

# .envファイルを読み込み
load_dotenv()

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.media.modern_thumbnail_generator import ModernThumbnailGenerator

# WordPress設定
WP_USERNAME = os.getenv('WORDPRESS_USERNAME')
WP_PASSWORD = os.getenv('WORDPRESS_APP_PASSWORD')
WP_URL = 'https://aimelodykobo.com'

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def upload_image_to_wordpress(image_path):
    """画像をWordPressにアップロード"""
    
    with open(image_path, 'rb') as img_file:
        media_data = {
            'file': img_file,
            'caption': 'AI Music Thumbnail',
            'alt_text': 'AI音楽記事のサムネイル'
        }
        
        response = requests.post(
            f"{WP_URL}/index.php?rest_route=/wp/v2/media",
            files={'file': img_file},
            auth=(WP_USERNAME, WP_PASSWORD)
        )
        
        if response.status_code == 201:
            media_id = response.json()['id']
            media_url = response.json()['source_url']
            logger.info(f"   画像アップロード成功: ID={media_id}")
            return media_id
        else:
            logger.error(f"   画像アップロード失敗: {response.status_code}")
            return None

def update_post_thumbnail(post_id, media_id):
    """記事のアイキャッチ画像を更新"""
    
    update_data = {
        'featured_media': media_id
    }
    
    response = requests.post(
        f"{WP_URL}/index.php?rest_route=/wp/v2/posts/{post_id}",
        json=update_data,
        auth=(WP_USERNAME, WP_PASSWORD)
    )
    
    if response.status_code == 200:
        logger.info(f"   アイキャッチ画像設定成功")
        return True
    else:
        logger.error(f"   アイキャッチ画像設定失敗: {response.status_code}")
        return False

def add_thumbnails_to_draft_posts():
    """下書き記事にサムネイルを追加"""
    
    # サムネイルジェネレーター初期化
    thumbnail_generator = ModernThumbnailGenerator()
    
    logger.info("📝 下書き記事を取得中...")
    
    # 下書き記事を取得
    response = requests.get(
        f"{WP_URL}/index.php?rest_route=/wp/v2/posts",
        params={
            'per_page': 50,
            'orderby': 'date',
            'order': 'desc',
            'status': 'draft'  # 下書きのみ
        },
        auth=(WP_USERNAME, WP_PASSWORD)
    )
    
    if response.status_code != 200:
        logger.error(f"投稿の取得に失敗: {response.status_code}")
        return
    
    posts = response.json()
    logger.info(f"📊 {len(posts)}件の投稿が見つかりました")
    
    # アイキャッチ画像がない投稿を処理
    processed_count = 0
    
    for post in posts:
        post_id = post['id']
        title = post['title']['rendered']
        featured_media = post.get('featured_media', 0)
        
        # すでにアイキャッチ画像がある場合はスキップ
        if featured_media != 0:
            logger.info(f"✓ スキップ: {title} (既にサムネイルあり)")
            continue
        
        logger.info(f"\n処理中: {title}")
        
        try:
            # タイトルから年を除去
            clean_title = title.replace('【2025年最新版】', '').strip()
            
            # ツール名を判定
            tool_name = 'AI音楽'
            if 'Suno' in title:
                tool_name = 'Suno'
            elif 'Udio' in title:
                tool_name = 'Udio'
            elif 'Stable Audio' in title:
                tool_name = 'Stable Audio'
            elif 'MusicGen' in title:
                tool_name = 'MusicGen'
            elif 'AIVA' in title:
                tool_name = 'AIVA'
            elif 'React' in title:
                tool_name = 'React'
            elif 'Python' in title:
                tool_name = 'Python'
            elif 'Transformer' in title:
                tool_name = 'AI技術'
            
            # サムネイル生成
            thumbnail_path = f"temp_thumbnail_{post_id}.png"
            thumbnail_generator.generate_modern_thumbnail(
                title=clean_title,
                tool_name=tool_name,
                output_path=thumbnail_path
            )
            
            # WordPressにアップロード
            media_id = upload_image_to_wordpress(thumbnail_path)
            
            if media_id:
                # アイキャッチ画像として設定
                if update_post_thumbnail(post_id, media_id):
                    processed_count += 1
                    logger.info(f"✅ 完了: {title}")
                else:
                    logger.error(f"❌ 失敗: アイキャッチ設定エラー")
            else:
                logger.error(f"❌ 失敗: アップロードエラー")
            
            # 一時ファイルを削除
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
                
        except Exception as e:
            logger.error(f"エラー: {str(e)}")
            continue
    
    # 結果サマリー
    logger.info(f"\n{'='*60}")
    logger.info(f"🎉 処理完了！")
    logger.info(f"✅ サムネイル追加: {processed_count}件")

if __name__ == "__main__":
    try:
        add_thumbnails_to_draft_posts()
    except KeyboardInterrupt:
        logger.info("\n⚠️ ユーザーによって中断されました")
    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}", exc_info=True)