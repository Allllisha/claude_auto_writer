#!/usr/bin/env python3
"""
AI Clientを使用して記事を生成するスクリプト
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.article_generator.ai_client import AIClientFactory
from src.article_generator.smart_content_generator import SmartContentGenerator

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 記事トピックの定義
ARTICLE_TOPICS = [
    {
        'topic': 'Suno AIの使い方完全ガイド',
        'keywords': ['Suno', 'AI音楽', '音楽生成', '使い方', 'プロンプト'],
        'article_type': 'suno_specific'
    },
    {
        'topic': 'Sunoで作った曲を収益化する方法',
        'keywords': ['Suno', '収益化', '商用利用', 'ライセンス', 'YouTube'],
        'article_type': 'suno_specific'
    },
    {
        'topic': 'Suno vs Udio徹底比較！どっちがおすすめ？',
        'keywords': ['Suno', 'Udio', '比較', 'AI音楽ツール', '違い'],
        'article_type': 'tool_comparison'
    },
    {
        'topic': 'Stable Audioの始め方完全ガイド',
        'keywords': ['Stable Audio', 'AI音楽', '使い方', '初心者', 'チュートリアル'],
        'article_type': 'tutorial'
    },
    {
        'topic': 'Stable Audioの技術的仕組み解説',
        'keywords': ['Stable Audio', '技術解説', 'ディフュージョン', 'AI', '音楽生成'],
        'article_type': 'technical'
    },
    {
        'topic': 'ReactでAI音楽プレイヤーを作る方法',
        'keywords': ['React', 'AI音楽', 'プレイヤー', '開発', 'JavaScript'],
        'article_type': 'programming'
    },
    {
        'topic': 'Transformerで音楽生成の仕組みを理解',
        'keywords': ['Transformer', '音楽生成', '機械学習', 'AI', '技術解説'],
        'article_type': 'technical'
    },
    {
        'topic': 'PythonでAI音楽APIを活用する方法',
        'keywords': ['Python', 'API', 'AI音楽', 'プログラミング', '実装'],
        'article_type': 'programming'
    },
    {
        'topic': 'AI音楽で副業を始める完全ガイド',
        'keywords': ['AI音楽', '副業', '収益化', 'フリーランス', '始め方'],
        'article_type': 'business'
    },
    {
        'topic': 'AI音楽ツール総まとめ2025年版',
        'keywords': ['AI音楽', '2025年', 'ツール比較', 'まとめ', '最新情報'],
        'article_type': 'comparison'
    }
]

def ensure_newsletter_cta(content: str) -> str:
    """記事にニュースレターCTAが含まれているか確認し、必要に応じて追加"""
    
    # CTAのフォーマット
    cta_format = """
---

**💌 無料メルマガ登録で限定特典をゲット！**

{cta_message}

[CTAボタン: 無料メルマガに登録する]

---
"""
    
    # 記事内にCTAが含まれているかチェック
    if "無料メルマガ" not in content:
        # 記事の中間あたりに挿入
        lines = content.split('\n')
        mid_point = len(lines) // 2
        
        # 適切な挿入位置を探す（セクションの区切りなど）
        insert_pos = mid_point
        for i in range(mid_point - 10, mid_point + 10):
            if i < len(lines) and lines[i].startswith('##'):
                insert_pos = i
                break
        
        # CTAメッセージを生成
        cta_message = "AI音楽制作の最新情報や、プロ級のテクニックを無料でお届け！今すぐ登録して、AI音楽制作マスターへの第一歩を踏み出しましょう。"
        cta = cta_format.format(cta_message=cta_message)
        
        # CTAを挿入
        lines.insert(insert_pos, cta)
        content = '\n'.join(lines)
    
    # 記事の最後にもCTAを追加（まとめの後）
    if content.count("無料メルマガ") < 2:
        final_cta_message = "AI Melody Koboの無料メルマガで、AI音楽制作の最新トレンドをいち早くキャッチ！実践的なノウハウも満載です。"
        final_cta = cta_format.format(cta_message=final_cta_message)
        
        # まとめセクションの後に挿入
        if "## まとめ" in content:
            content = content.replace("**WordPressタグ:", final_cta + "\n**WordPressタグ:")
        else:
            # まとめがない場合は記事の最後に追加
            content = content.replace("**WordPressタグ:", final_cta + "\n**WordPressタグ:")
    
    return content

def generate_articles():
    """記事を生成"""
    
    logger.info("📝 AI Clientを使用した記事生成を開始します...")
    
    # 出力ディレクトリの作成
    output_dir = Path("generated_articles_with_ai")
    output_dir.mkdir(exist_ok=True)
    
    # AIクライアントを作成（Claudeを使用、なければモック）
    ai_client = AIClientFactory.create_client("claude")
    
    success_count = 0
    failed_count = 0
    
    for i, article_config in enumerate(ARTICLE_TOPICS, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"処理中 {i}/{len(ARTICLE_TOPICS)}: {article_config['topic']}")
        
        try:
            # 記事を生成
            result = ai_client.generate_article(
                topic=article_config['topic'],
                keywords=article_config['keywords'],
                article_type=article_config['article_type']
            )
            
            # マークダウンコンテンツを取得
            content = result.get('markdown_content', '')
            
            # ニュースレターCTAを確認・追加
            content = ensure_newsletter_cta(content)
            
            # ファイル名を生成
            safe_filename = f"{i:02d}_{article_config['topic'].replace(' ', '_').replace('/', '_')}.md"
            output_path = output_dir / safe_filename
            
            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ 生成成功: {output_path}")
            logger.info(f"   文字数: {len(content)}")
            logger.info(f"   モデル: {result.get('model', 'unknown')}")
            success_count += 1
            
        except Exception as e:
            logger.error(f"❌ 生成失敗: {str(e)}")
            failed_count += 1
            continue
    
    # 最終結果
    logger.info(f"\n{'='*60}")
    logger.info("🎉 記事生成完了！")
    logger.info(f"✅ 成功: {success_count}件")
    logger.info(f"❌ 失敗: {failed_count}件")
    logger.info(f"📂 出力先: {output_dir.absolute()}")

if __name__ == "__main__":
    try:
        generate_articles()
    except KeyboardInterrupt:
        logger.info("\n⚠️ ユーザーによって中断されました")
    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}", exc_info=True)