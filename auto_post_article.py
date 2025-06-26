#!/usr/bin/env python3
"""
Auto Post Article - 記事自動生成・投稿スクリプト
AI Melody Kobo - 記事を自動生成してWordPressに投稿
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path
import random

# プロジェクトのパスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.article_generator.content_builder import ArticleGenerator
from src.wordpress.api_client import WordPressClient
from src.wordpress.category_manager import CategoryManager
from src.media.modern_thumbnail_generator import ModernThumbnailGenerator
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_post.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AutoArticlePublisher:
    """記事の自動生成・投稿を管理するクラス"""
    
    def __init__(self):
        """初期化"""
        logger.info("自動投稿システムを初期化中...")
        
        # WordPressクライアントの初期化
        self.wp_client = WordPressClient()
        
        # カテゴリーマネージャーの初期化
        self.category_manager = CategoryManager(self.wp_client)
        self.category_manager.setup_categories()
        
        # 記事生成器の初期化
        self.article_generator = ArticleGenerator(
            ai_client_type="claude",
            category_manager=self.category_manager
        )
        
        # サムネイル生成器の初期化
        self.thumbnail_generator = ModernThumbnailGenerator()
        
        logger.info("自動投稿システムの初期化完了")
    
    def generate_and_publish(self, 
                           topic: str = None,
                           article_type: str = None,
                           tool_name: str = None,
                           status: str = 'draft') -> dict:
        """
        記事を生成して投稿する
        
        Args:
            topic: 記事のトピック（指定しない場合は自動選択）
            article_type: 記事タイプ
            tool_name: ツール名（Suno、Udio等）
            status: 投稿ステータス（draft/publish）
            
        Returns:
            投稿結果の辞書
        """
        try:
            # トピックが指定されていない場合は自動選択
            if not topic:
                topic = self._select_topic(article_type, tool_name)
                logger.info(f"自動選択されたトピック: {topic}")
            
            # 記事タイプが指定されていない場合は自動選択
            if not article_type:
                article_type = self._select_article_type()
                logger.info(f"自動選択された記事タイプ: {article_type}")
            
            # ツール名が指定されていない場合は自動選択
            if not tool_name:
                tool_name = self._select_tool_name()
                logger.info(f"自動選択されたツール: {tool_name}")
            
            # 1. 記事を生成
            logger.info("記事生成を開始...")
            result = self.article_generator.generate_article(
                topic=topic,
                article_type=article_type,
                tool_name=tool_name,
                use_latest_info=True
            )
            
            if not result['success']:
                raise Exception("記事生成に失敗しました")
            
            article_data = result['article_data']
            logger.info(f"記事生成完了: {article_data['title']}")
            
            # 2. サムネイル画像を生成
            logger.info("サムネイル画像を生成中...")
            thumbnail_data = self.thumbnail_generator.generate_from_article_data(
                article_data,
                article_type=article_type,
                tool_name=tool_name
            )
            
            # 3. 画像をアップロード
            media_result = self.wp_client.upload_media(
                file_data=thumbnail_data,
                filename=f"thumbnail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                title=f"{article_data['title']} - アイキャッチ画像",
                alt_text=article_data['title']
            )
            logger.info(f"サムネイル画像アップロード完了: ID {media_result['id']}")
            
            # 4. 記事を投稿
            logger.info("WordPressに投稿中...")
            post_result = self.wp_client.create_post(
                title=article_data['title'],
                content=article_data['content'],
                status=status,
                categories=article_data.get('categories', []),
                tags=article_data.get('tags', []),
                featured_media=media_result['id'],
                excerpt=article_data.get('excerpt', ''),
                meta_description=article_data.get('meta_description', '')
            )
            
            logger.info(f"投稿完了！ ID: {post_result['id']}, URL: {post_result['link']}")
            
            return {
                'success': True,
                'post_id': post_result['id'],
                'url': post_result['link'],
                'title': post_result['title']['rendered'],
                'status': post_result['status'],
                'article_type': article_type,
                'tool_name': tool_name
            }
            
        except Exception as e:
            logger.error(f"投稿エラー: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _select_topic(self, article_type: str = None, tool_name: str = None) -> str:
        """トピックを自動選択"""
        topics = {
            'beginner_guide': [
                f"{tool_name or 'AI音楽'}を始めよう！初心者向け完全ガイド",
                f"【保存版】{tool_name or 'AI音楽ツール'}の使い方を基礎から解説",
                f"初めての{tool_name or 'AI作曲'}！スタートガイド"
            ],
            'tutorial': [
                f"{tool_name or 'AI音楽'}でプロ級の楽曲を作る方法",
                f"【実践】{tool_name or 'AI音楽ツール'}の高度なテクニック10選",
                f"{tool_name or 'AI'}で作る！ジャンル別音楽制作ガイド"
            ],
            'prompt_guide': [
                f"{tool_name or 'AI音楽'}のプロンプト作成術：効果的な指示の書き方",
                f"【検証】{tool_name or 'AI'}に最適なプロンプトパターン集",
                f"プロが教える{tool_name or 'AI音楽'}プロンプトの極意"
            ],
            'tool_comparison': [
                "【2024年最新】AI音楽ツール徹底比較！あなたに最適なツールは？",
                "Suno vs Udio vs MusicGen：3大AI音楽ツールを比較検証",
                "AI音楽ツール選びの決定版！各ツールの特徴と使い分け"
            ],
            'voice_synthesis': [
                "AI音声合成の最前線！リアルな音声を生成する技術",
                "【実装】Pythonで音声合成アプリを作ってみた",
                "音声クローン技術の現在地：倫理と可能性"
            ],
            'app_development': [
                "AI音楽アプリを開発しよう！実装ガイド",
                "WebでAI音楽を活用：APIとライブラリの使い方",
                "【コード付き】AI音楽生成機能の実装方法"
            ]
        }
        
        # 記事タイプに応じたトピックを選択
        topic_list = topics.get(article_type, topics['tutorial'])
        return random.choice(topic_list)
    
    def _select_article_type(self) -> str:
        """記事タイプを自動選択（バランスよく）"""
        types = [
            'beginner_guide',
            'tutorial',
            'prompt_guide',
            'tool_comparison',
            'tool_review',
            'voice_synthesis',
            'app_development',
            'industry_news'
        ]
        return random.choice(types)
    
    def _select_tool_name(self) -> str:
        """ツール名を自動選択（バランスよく）"""
        tools = ['Suno', 'Udio', 'MusicGen', 'Stable Audio', 'AIVA', None]
        weights = [0.3, 0.2, 0.15, 0.15, 0.1, 0.1]  # Sunoを優先
        return random.choices(tools, weights=weights)[0]
    
    def run_daily_posts(self, post_count: int = 1, status: str = 'draft'):
        """
        日次投稿を実行
        
        Args:
            post_count: 投稿する記事数
            status: 投稿ステータス
        """
        logger.info(f"日次投稿開始: {post_count}記事を生成")
        
        results = []
        for i in range(post_count):
            logger.info(f"\n--- 記事 {i+1}/{post_count} ---")
            
            result = self.generate_and_publish(status=status)
            results.append(result)
            
            if result['success']:
                logger.info(f"✅ 成功: {result['title']}")
            else:
                logger.error(f"❌ 失敗: {result.get('error', '不明なエラー')}")
        
        # サマリーを出力
        success_count = sum(1 for r in results if r['success'])
        logger.info(f"\n=== 投稿完了 ===")
        logger.info(f"成功: {success_count}/{post_count}")
        logger.info(f"失敗: {post_count - success_count}/{post_count}")
        
        return results


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description='AI Melody Kobo - 記事自動生成・投稿ツール'
    )
    parser.add_argument(
        '--topic',
        help='記事のトピック（指定しない場合は自動選択）'
    )
    parser.add_argument(
        '--type',
        choices=['beginner_guide', 'tutorial', 'prompt_guide', 'tool_comparison', 
                 'tool_review', 'voice_synthesis', 'app_development', 'industry_news'],
        help='記事タイプ'
    )
    parser.add_argument(
        '--tool',
        choices=['Suno', 'Udio', 'MusicGen', 'Stable Audio', 'AIVA'],
        help='ツール名'
    )
    parser.add_argument(
        '--status',
        choices=['draft', 'publish'],
        default='draft',
        help='投稿ステータス（デフォルト: draft）'
    )
    parser.add_argument(
        '--daily',
        type=int,
        metavar='COUNT',
        help='日次投稿モード：指定した数の記事を生成'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='接続テストのみ実行'
    )
    
    args = parser.parse_args()
    
    # Publisher初期化
    try:
        publisher = AutoArticlePublisher()
    except Exception as e:
        logger.error(f"初期化エラー: {str(e)}")
        sys.exit(1)
    
    # 接続テスト
    if args.test:
        if publisher.wp_client.test_connection():
            print("✅ WordPress接続テスト成功！")
            sys.exit(0)
        else:
            print("❌ WordPress接続テスト失敗")
            sys.exit(1)
    
    # 日次投稿モード
    if args.daily:
        results = publisher.run_daily_posts(
            post_count=args.daily,
            status=args.status
        )
        sys.exit(0 if all(r['success'] for r in results) else 1)
    
    # 単一記事の投稿
    result = publisher.generate_and_publish(
        topic=args.topic,
        article_type=args.type,
        tool_name=args.tool,
        status=args.status
    )
    
    if result['success']:
        print("\n✅ 投稿成功！")
        print(f"タイトル: {result['title']}")
        print(f"ステータス: {result['status']}")
        print(f"投稿ID: {result['post_id']}")
        print(f"URL: {result['url']}")
    else:
        print("\n❌ 投稿失敗")
        print(f"エラー: {result.get('error', '不明なエラー')}")
        sys.exit(1)


if __name__ == "__main__":
    main()