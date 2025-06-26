#!/usr/bin/env python3
"""
記事をサムネイル付きでWordPressに投稿するスクリプト
"""

import os
import sys
import glob
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

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

def upload_thumbnail_to_wordpress(image_path, title):
    """サムネイルをWordPressにアップロード"""
    
    with open(image_path, 'rb') as img_file:
        files = {'file': (os.path.basename(image_path), img_file, 'image/png')}
        
        response = requests.post(
            f"{WP_URL}/index.php?rest_route=/wp/v2/media",
            files=files,
            auth=(WP_USERNAME, WP_PASSWORD),
            headers={'Content-Disposition': f'attachment; filename="{os.path.basename(image_path)}"'}
        )
        
        if response.status_code == 201:
            media_id = response.json()['id']
            media_url = response.json()['source_url']
            logger.info(f"   ✅ サムネイルアップロード成功: ID={media_id}")
            return media_id
        else:
            logger.error(f"   ❌ サムネイルアップロード失敗: {response.status_code}")
            logger.error(f"   エラー: {response.text}")
            return None

def post_article_with_thumbnail(title, content, thumbnail_path, status='draft'):
    """サムネイル付きで記事をWordPressに投稿"""
    
    # まずサムネイルをアップロード
    media_id = None
    if thumbnail_path and os.path.exists(thumbnail_path):
        media_id = upload_thumbnail_to_wordpress(thumbnail_path, title)
    
    # WordPressの投稿データ
    post_data = {
        'title': title,
        'content': content,
        'status': status,
        'categories': [27, 29, 31],  # AI音楽ツール、使い方・始め方、最新情報
        'tags': [],  # タグは後で追加
    }
    
    # サムネイルがある場合は追加
    if media_id:
        post_data['featured_media'] = media_id
    
    # 投稿API URL
    api_url = f"{WP_URL}/index.php?rest_route=/wp/v2/posts"
    
    try:
        response = requests.post(
            api_url,
            json=post_data,
            auth=(WP_USERNAME, WP_PASSWORD)
        )
        
        if response.status_code == 201:
            post_id = response.json()['id']
            post_link = response.json()['link']
            logger.info(f"✅ 投稿成功: {title}")
            logger.info(f"   ID: {post_id}")
            logger.info(f"   URL: {post_link}")
            logger.info(f"   サムネイル: {'あり' if media_id else 'なし'}")
            return True
        else:
            logger.error(f"❌ 投稿失敗: {title}")
            logger.error(f"   ステータス: {response.status_code}")
            logger.error(f"   エラー: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 投稿エラー: {str(e)}")
        return False

def main():
    """メイン処理"""
    
    logger.info("📝 サムネイル付き記事投稿を開始します...")
    
    # サムネイルジェネレーター初期化
    thumbnail_generator = ModernThumbnailGenerator()
    
    # 記事ファイルを取得
    article_files = sorted(glob.glob("generated_articles/*.md"))
    
    if not article_files:
        logger.error("記事ファイルが見つかりません")
        return
    
    logger.info(f"📊 {len(article_files)}件の記事が見つかりました")
    
    success_count = 0
    failed_count = 0
    
    for i, filepath in enumerate(article_files, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"処理中 {i}/{len(article_files)}: {os.path.basename(filepath)}")
        
        try:
            # ファイルを読み込み
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # タイトルを抽出（最初の行）
            lines = content.split('\n')
            title = lines[0].replace('# ', '').strip()
            
            # タイトルから年を除去してサムネイル用に
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
            thumbnail_path = f"temp_thumbnail_{i}.png"
            thumbnail_data = thumbnail_generator.generate_thumbnail(
                title=clean_title,
                article_type='general',
                tool_name=tool_name,
                keywords=[tool_name, 'AI音楽', '最新']
            )
            
            # バイトデータをファイルに保存
            with open(thumbnail_path, 'wb') as f:
                f.write(thumbnail_data)
            
            logger.info(f"   🖼️ サムネイル生成完了")
            
            # 投稿
            if post_article_with_thumbnail(title, content, thumbnail_path):
                success_count += 1
            else:
                failed_count += 1
            
            # 一時ファイルを削除
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
                
        except Exception as e:
            logger.error(f"ファイル処理エラー: {str(e)}")
            failed_count += 1
            continue
    
    # 最終結果
    logger.info(f"\n{'='*60}")
    logger.info("🎉 投稿処理完了！")
    logger.info(f"✅ 成功: {success_count}件")
    logger.info(f"❌ 失敗: {failed_count}件")
    logger.info(f"📊 成功率: {success_count/len(article_files)*100:.1f}%")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️ ユーザーによって中断されました")
    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}", exc_info=True)