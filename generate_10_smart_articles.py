#!/usr/bin/env python3
"""
10記事生成スクリプト（スマートコンテンツジェネレーター版）
タイトルと内容の一貫性を保ちながら10記事を生成
"""

import sys
import os
import time
import random
from datetime import datetime
import logging
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.article_generator.smart_content_generator import SmartContentGenerator

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 記事トピックのリスト（10個）
ARTICLE_TOPICS = [
    # Suno関連（3記事）
    ("【2025年最新版】Suno AIの使い方完全ガイド", ["Suno", "AI音楽", "使い方", "初心者向け"], "tutorial"),
    ("【2025年最新版】Sunoで作った曲を収益化する方法", ["Suno", "収益化", "AI音楽", "稼ぐ方法"], "practical"),
    ("【2025年最新版】Suno vs Udio徹底比較！どっちがおすすめ？", ["Suno", "Udio", "比較", "AI音楽"], "comparison"),
    
    # Stable Audio関連（2記事）
    ("【2025年最新版】Stable Audioの始め方完全ガイド", ["Stable Audio", "始め方", "初心者", "入門"], "tutorial"),
    ("【2025年最新版】Stable Audioの技術的仕組み解説", ["Stable Audio", "技術", "仕組み", "AI"], "technical"),
    
    # 技術・開発関連（3記事）
    ("【2025年最新版】ReactでAI音楽プレイヤーを作る方法", ["React", "音楽プレイヤー", "開発", "TypeScript"], "development"),
    ("【2025年最新版】Transformerで音楽生成の仕組みを理解", ["Transformer", "音楽生成", "AI技術", "深層学習"], "technical"),
    ("【2025年最新版】PythonでAI音楽APIを活用する方法", ["Python", "API", "AI音楽", "開発"], "development"),
    
    # その他（2記事）
    ("【2025年最新版】AI音楽で副業を始める完全ガイド", ["副業", "AI音楽", "収益化", "始め方"], "practical"),
    ("【2025年最新版】AI音楽ツール総まとめ2025年版", ["AI音楽", "ツール", "まとめ", "比較"], "comparison"),
]

def generate_and_save_articles():
    """10記事を生成して保存"""
    
    logger.info("🚀 10記事生成を開始します（スマートコンテンツジェネレーター版）")
    logger.info("📝 タイトルと内容の一貫性を保ちながら生成します")
    logger.info("=" * 60)
    
    success_count = 0
    failed_count = 0
    
    # 出力ディレクトリ作成
    output_dir = "generated_articles"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, (topic, keywords, article_type) in enumerate(ARTICLE_TOPICS, 1):
        try:
            logger.info(f"\n📊 記事生成進捗: {i}/10")
            logger.info(f"🎯 生成中: {topic}")
            logger.info(f"   キーワード: {keywords}")
            logger.info(f"   記事タイプ: {article_type}")
            
            # 記事生成
            content = SmartContentGenerator.generate_article(topic, keywords, article_type)
            
            # 文字数チェック
            char_count = len(content)
            logger.info(f"   文字数: {char_count:,}文字")
            
            # ファイルに保存
            filename = f"{i:02d}_{topic.replace('【2025年最新版】', '').replace('/', '_')}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"   ✅ 保存完了: {filepath}")
            success_count += 1
            
            # サーバー負荷軽減のため待機
            if i < 10:
                time.sleep(1)
            
        except Exception as e:
            failed_count += 1
            logger.error(f"❌ 記事{i}でエラー発生: {str(e)}", exc_info=True)
            continue
    
    # 最終結果
    logger.info("\n" + "=" * 60)
    logger.info("🎉 10記事生成完了！")
    logger.info(f"✅ 成功: {success_count}件")
    logger.info(f"❌ 失敗: {failed_count}件")
    logger.info(f"📁 生成ファイル: {output_dir}/")

if __name__ == "__main__":
    try:
        generate_and_save_articles()
    except KeyboardInterrupt:
        logger.info("\n⚠️ ユーザーによって中断されました")
    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}", exc_info=True)