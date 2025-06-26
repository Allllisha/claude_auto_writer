#!/usr/bin/env python3
"""
生成記事をWordPressに投稿するスクリプト
"""

import os
import glob
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

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

def post_article_to_wordpress(title, content, status='draft'):
    """記事をWordPressに投稿"""
    
    # タイトルから年を取り除く
    clean_title = title.replace('【2025年最新版】', '').strip()
    
    # WordPressの投稿データ
    post_data = {
        'title': title,
        'content': content,
        'status': status,
        'categories': [27, 29, 31],  # AI音楽ツール、使い方・始め方、最新情報
        'tags': [],  # タグは後で追加
    }
    
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
    
    logger.info("📝 記事の投稿を開始します...")
    
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
            
            # 投稿
            if post_article_to_wordpress(title, content):
                success_count += 1
            else:
                failed_count += 1
                
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