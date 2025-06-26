#!/usr/bin/env python3
"""
連続記事生成システム - 10分ごとに自動で記事を生成・投稿
"""

import os
import sys
import time
import logging
from datetime import datetime, timedelta
import signal
import random

# プロジェクトのパスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from production_article_test import generate_production_article, generate_random_article_config

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# グローバル変数で停止フラグ
stop_generation = False

def signal_handler(signum, frame):
    """Ctrl+Cなどのシグナルをキャッチして安全に停止"""
    global stop_generation
    logger.info("⚠️ 停止シグナルを受信しました。安全に停止します...")
    stop_generation = True

def continuous_article_generation():
    """10分ごとに記事を生成し続ける"""
    global stop_generation
    
    # シグナルハンドラーを設定
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("🚀 連続記事生成システムを開始します")
    logger.info("📝 10分ごとに記事を生成し、WordPressに下書きとして投稿します")
    logger.info("⏹️ 停止するには Ctrl+C を押してください")
    
    article_count = 0
    start_time = datetime.now()
    
    while not stop_generation:
        try:
            article_count += 1
            current_time = datetime.now()
            elapsed_time = current_time - start_time
            
            logger.info("=" * 60)
            logger.info(f"📊 記事生成状況")
            logger.info(f"   開始時刻: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"   現在時刻: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"   経過時間: {elapsed_time}")
            logger.info(f"   生成回数: {article_count}回目")
            logger.info("=" * 60)
            
            # 記事生成
            logger.info(f"🎯 第{article_count}回目の記事生成を開始...")
            result = generate_production_article()
            
            if result['success']:
                logger.info(f"✅ 記事生成成功！")
                logger.info(f"   投稿ID: {result['post_id']}")
                logger.info(f"   URL: {result['url']}")
                logger.info(f"   タイトル: {result['title']}")
            else:
                logger.error(f"❌ 記事生成失敗: {result.get('error')}")
            
            # 次の生成まで待機（10分）
            if not stop_generation:
                next_generation = current_time + timedelta(minutes=10)
                logger.info(f"⏰ 次の記事生成: {next_generation.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"💤 10分間待機します...")
                
                # 10分を1秒ごとにチェック（停止シグナルに素早く反応するため）
                for _ in range(600):  # 600秒 = 10分
                    if stop_generation:
                        break
                    time.sleep(1)
            
        except Exception as e:
            logger.error(f"❌ エラーが発生しました: {str(e)}")
            logger.error(f"   詳細: {e.__class__.__name__}")
            # エラーが発生しても継続
            if not stop_generation:
                logger.info("⚡ 1分後に再試行します...")
                time.sleep(60)
    
    # 終了処理
    end_time = datetime.now()
    total_time = end_time - start_time
    logger.info("=" * 60)
    logger.info("🏁 連続記事生成システムを終了します")
    logger.info(f"   開始時刻: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"   終了時刻: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"   稼働時間: {total_time}")
    logger.info(f"   生成記事数: {article_count - 1}件")
    logger.info("=" * 60)

if __name__ == "__main__":
    continuous_article_generation()