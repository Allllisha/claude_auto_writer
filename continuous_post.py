#!/usr/bin/env python3
"""
Continuous Post - 高頻度記事投稿システム
AI Melody Kobo - 10分に1回記事を自動生成・投稿
"""

import os
import sys
import time
import json
import random
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Set, Dict, List
import signal

# プロジェクトのパスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.article_generator.content_builder import ArticleGenerator
from src.wordpress.api_client import WordPressClient
from src.wordpress.category_manager import CategoryManager
from src.media.modern_thumbnail_generator import ModernThumbnailGenerator
from file_organizer import FileOrganizer
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('continuous_post.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ContinuousArticlePublisher:
    """高頻度記事投稿システム"""
    
    def __init__(self, interval_minutes: int = 10):
        """
        初期化
        
        Args:
            interval_minutes: 投稿間隔（分）
        """
        self.interval_minutes = interval_minutes
        self.interval_seconds = interval_minutes * 60
        
        logger.info(f"連続投稿システムを初期化中... (間隔: {interval_minutes}分)")
        
        # WordPressクライアント
        self.wp_client = WordPressClient()
        
        # カテゴリーマネージャー
        self.category_manager = CategoryManager(self.wp_client)
        self.category_manager.setup_categories()
        
        # 記事生成器
        self.article_generator = ArticleGenerator(
            ai_client_type="claude",
            category_manager=self.category_manager
        )
        
        # サムネイル生成器
        self.thumbnail_generator = ModernThumbnailGenerator()
        
        # 記事履歴管理
        self.history_file = Path("data/post_history.json")
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.post_history = self._load_history()
        
        # トピック管理
        self.topic_manager = TopicManager()
        
        # ファイル整理システム
        self.file_organizer = FileOrganizer()
        
        # 実行中フラグ
        self.running = False
        
        logger.info("連続投稿システムの初期化完了")
    
    def _load_history(self) -> Dict:
        """投稿履歴を読み込み"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"履歴ファイル読み込みエラー: {e}")
        
        return {
            'posts': [],
            'used_topics': set(),
            'last_post_time': None,
            'total_posts': 0
        }
    
    def _save_history(self):
        """投稿履歴を保存"""
        try:
            # setをlistに変換して保存
            history_data = self.post_history.copy()
            history_data['used_topics'] = list(self.post_history['used_topics'])
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"履歴保存エラー: {e}")
    
    def _get_unique_topic(self, article_type: str, tool_name: str) -> str:
        """重複しないトピックを生成"""
        max_attempts = 10
        
        for attempt in range(max_attempts):
            topic = self.topic_manager.generate_topic(article_type, tool_name)
            topic_hash = hashlib.md5(topic.encode()).hexdigest()
            
            # 重複チェック
            if topic_hash not in self.post_history['used_topics']:
                self.post_history['used_topics'].add(topic_hash)
                return topic
            
            logger.info(f"トピック重複検出、再生成中... (試行 {attempt + 1}/{max_attempts})")
        
        # 最大試行回数に達した場合は時刻を付加
        timestamp = datetime.now().strftime("%m月%d日")
        unique_topic = f"【{timestamp}】{topic}"
        topic_hash = hashlib.md5(unique_topic.encode()).hexdigest()
        self.post_history['used_topics'].add(topic_hash)
        
        return unique_topic
    
    def generate_and_publish_once(self) -> Dict:
        """1回分の記事生成・投稿"""
        try:
            # 記事タイプとツールを選択
            article_type = self.topic_manager.select_article_type()
            tool_name = self.topic_manager.select_tool_name()
            
            # ユニークなトピックを生成
            topic = self._get_unique_topic(article_type, tool_name)
            
            logger.info(f"記事生成開始: {topic}")
            logger.info(f"タイプ: {article_type}, ツール: {tool_name}")
            
            # 記事生成
            result = self.article_generator.generate_article(
                topic=topic,
                article_type=article_type,
                tool_name=tool_name,
                use_latest_info=False  # 高頻度投稿では外部情報収集を軽量化
            )
            
            # 生成された記事をアーカイブ
            if result['success']:
                self.file_organizer.archive_generated_article(
                    result['generation_metadata']['markdown_content'],
                    {
                        'article_type': article_type,
                        'tool_name': tool_name,
                        'topic': topic,
                        'generated_at': datetime.now().isoformat()
                    },
                    title=topic
                )
            
            if not result['success']:
                raise Exception("記事生成に失敗しました")
            
            article_data = result['article_data']
            
            # サムネイル生成
            thumbnail_data = self.thumbnail_generator.generate_from_article_data(
                article_data,
                article_type=article_type,
                tool_name=tool_name
            )
            
            # 画像をアーカイブ
            thumbnail_filename = f"thumbnail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.file_organizer.archive_image(
                thumbnail_data,
                thumbnail_filename,
                {
                    'article_title': article_data['title'],
                    'article_type': article_type,
                    'tool_name': tool_name,
                    'generated_for': 'thumbnail'
                }
            )
            
            # 画像アップロード
            media_result = self.wp_client.upload_media(
                file_data=thumbnail_data,
                filename=f"thumb_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                title=f"{article_data['title']} - アイキャッチ画像",
                alt_text=article_data['title']
            )
            
            # 記事投稿
            post_result = self.wp_client.create_post(
                title=article_data['title'],
                content=article_data['content'],
                status='draft',  # 高頻度投稿では安全のため下書きに
                categories=article_data.get('categories', []),
                tags=article_data.get('tags', []),
                featured_media=media_result['id'],
                excerpt=article_data.get('excerpt', ''),
                meta_description=article_data.get('meta_description', '')
            )
            
            # 履歴に記録
            post_record = {
                'id': post_result['id'],
                'title': post_result['title']['rendered'],
                'url': post_result['link'],
                'article_type': article_type,
                'tool_name': tool_name,
                'posted_at': datetime.now().isoformat(),
                'status': post_result['status']
            }
            
            self.post_history['posts'].append(post_record)
            self.post_history['last_post_time'] = datetime.now().isoformat()
            self.post_history['total_posts'] += 1
            self._save_history()
            
            # 投稿済み記事をアーカイブ
            self.file_organizer.archive_published_article(
                post_result['id'],
                post_result['link'],
                post_result['title']['rendered'],
                article_data['content'],
                {
                    'article_type': article_type,
                    'tool_name': tool_name,
                    'categories': article_data.get('categories', []),
                    'tags': article_data.get('tags', []),
                    'status': post_result['status']
                }
            )
            
            logger.info(f"✅ 投稿完了: {post_result['title']['rendered']}")
            logger.info(f"   URL: {post_result['link']}")
            logger.info(f"   累計投稿数: {self.post_history['total_posts']}")
            
            return {
                'success': True,
                'post_id': post_result['id'],
                'title': post_result['title']['rendered'],
                'url': post_result['link']
            }
            
        except Exception as e:
            logger.error(f"❌ 投稿失敗: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_continuous(self):
        """連続投稿を開始"""
        self.running = True
        
        logger.info(f"🚀 連続投稿開始 (間隔: {self.interval_minutes}分)")
        logger.info(f"   累計投稿数: {self.post_history['total_posts']}")
        logger.info("   停止するには Ctrl+C を押してください")
        
        try:
            while self.running:
                start_time = time.time()
                
                # 記事投稿
                result = self.generate_and_publish_once()
                
                if result['success']:
                    logger.info(f"⏰ 次回投稿まで {self.interval_minutes}分待機...")
                else:
                    logger.warning("⚠️  投稿に失敗しましたが、処理を継続します")
                
                # 待機時間の計算
                elapsed = time.time() - start_time
                wait_time = max(0, self.interval_seconds - elapsed)
                
                if wait_time > 0:
                    time.sleep(wait_time)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 停止シグナルを受信しました")
        except Exception as e:
            logger.error(f"💥 予期しないエラー: {str(e)}")
        finally:
            self.running = False
            logger.info("📊 最終統計:")
            logger.info(f"   累計投稿数: {self.post_history['total_posts']}")
            logger.info(f"   最終投稿: {self.post_history.get('last_post_time', 'なし')}")
            logger.info("🔚 連続投稿システムを終了しました")
    
    def status(self):
        """現在の状況を表示"""
        print(f"\n📈 AI Melody Kobo 連続投稿システム")
        print(f"   投稿間隔: {self.interval_minutes}分")
        print(f"   累計投稿数: {self.post_history['total_posts']}")
        print(f"   最終投稿: {self.post_history.get('last_post_time', 'なし')}")
        print(f"   重複回避済みトピック数: {len(self.post_history['used_topics'])}")
        
        # 最近の投稿を表示
        recent_posts = self.post_history['posts'][-5:]
        if recent_posts:
            print(f"\n📝 最近の投稿:")
            for post in recent_posts:
                posted_time = datetime.fromisoformat(post['posted_at']).strftime('%m/%d %H:%M')
                print(f"   {posted_time} - {post['title'][:50]}...")


class TopicManager:
    """トピック管理クラス"""
    
    def __init__(self):
        # 記事タイプ別の詳細なトピックテンプレート
        self.topic_templates = {
            'beginner_guide': [
                "{tool}を始めよう！初心者向け完全ガイド【{month}月版】",
                "【保存版】{tool}の基本的な使い方を徹底解説",
                "初めての{tool}！知っておきたい基礎知識",
                "{tool}入門：最初に覚えるべき3つの機能",
                "【{month}月最新】{tool}スタートアップガイド",
                "{tool}を使った初心者向け音楽制作入門",
                "ゼロから始める{tool}講座：基本操作編",
                "{tool}の始め方：アカウント作成から最初の楽曲まで"
            ],
            'tutorial': [
                "{tool}でプロ級の楽曲を作る5つの方法",
                "【実践】{tool}の高度なテクニック完全版",
                "{tool}で作る！{genre}風音楽制作ガイド",
                "{tool}マスターが教える上級テクニック",
                "{tool}の隠れた便利機能10選",
                "{tool}でできる音楽制作の裏技集",
                "プロが実践する{tool}活用術",
                "{tool}で理想の楽曲を作るワークフロー"
            ],
            'prompt_guide': [
                "{tool}のプロンプト作成術：効果的な指示の書き方",
                "【検証】{tool}に最適なプロンプトパターン集",
                "プロが教える{tool}プロンプトの極意",
                "{tool}で思い通りの楽曲を作るプロンプト設計",
                "{tool}プロンプトエンジニアリング入門",
                "効果的な{tool}プロンプトの法則",
                "{tool}で使える実践的プロンプト集",
                "{tool}プロンプト最適化テクニック"
            ],
            'tool_comparison': [
                "【{month}月最新】AI音楽ツール徹底比較！",
                "{tool1} vs {tool2}：どちらがおすすめ？",
                "AI音楽ツール選びの決定版{month}月版",
                "5大AI音楽ツールの特徴と使い分け",
                "目的別AI音楽ツール比較ガイド",
                "初心者にオススメのAI音楽ツールは？",
                "プロが選ぶAI音楽ツールランキング",
                "AI音楽ツール価格・機能比較表"
            ],
            'voice_synthesis': [
                "AI音声合成の最前線！{month}月の技術動向",
                "リアルな音声を生成するAI技術解説",
                "音声クローン技術の現在地と未来",
                "【実装】PythonでAI音声合成を試してみた",
                "AI音声合成ツールの比較と選び方",
                "Text-to-Speechの最新技術トレンド",
                "AI音声技術の倫理と可能性",
                "音声合成AIの商用利用ガイド"
            ],
            'app_development': [
                "AI音楽アプリを開発しよう！{month}月版",
                "WebでAI音楽を活用：実装ガイド",
                "【コード付き】{tool} APIの使い方",
                "AI音楽機能を搭載したアプリ作成術",
                "音楽生成AIをWebアプリに組み込む方法",
                "AI音楽サービスの技術スタック解説",
                "開発者向け：AI音楽API活用法",
                "モバイルアプリでAI音楽を実装する"
            ],
            'industry_news': [
                "{month}月のAI音楽業界ニュースまとめ",
                "AI音楽業界の最新動向【{month}月版】",
                "{tool}の新機能アップデート情報",
                "AI音楽市場の現状と未来予測",
                "{month}月に注目すべきAI音楽技術",
                "音楽業界を変えるAIの最新事例",
                "AI音楽の法的課題と業界の対応",
                "投資家が注目するAI音楽スタートアップ"
            ],
            'singing_synthesis': [
                "AI歌声合成の最新技術動向{month}月版",
                "ボーカロイドとAIシンガーの違いとは？",
                "リアルなAI歌声を作る技術解説",
                "AI歌声合成ツールの比較と選び方",
                "歌声合成AIの商用利用ガイド",
                "Synthesizer VとAI歌声の進化",
                "AI歌手の可能性と音楽業界への影響",
                "歌声合成技術の倫理的課題"
            ]
        }
        
        # ジャンル例
        self.genres = [
            "ポップス", "ロック", "ジャズ", "クラシック", "エレクトロニック",
            "ヒップホップ", "R&B", "カントリー", "フォーク", "アンビエント",
            "ボサノバ", "レゲエ", "ファンク", "ブルース", "メタル"
        ]
        
        # ツール重み（Sunoを重視）
        self.tool_weights = {
            'Suno': 0.4,
            'Udio': 0.2,
            'MusicGen': 0.15,
            'Stable Audio': 0.15,
            'AIVA': 0.1
        }
        
        # 記事タイプの重み（バランス良く）
        self.type_weights = {
            'beginner_guide': 0.25,
            'tutorial': 0.25,
            'prompt_guide': 0.15,
            'tool_comparison': 0.1,
            'voice_synthesis': 0.1,
            'app_development': 0.1,
            'industry_news': 0.05
        }
    
    def generate_topic(self, article_type: str, tool_name: str) -> str:
        """トピックを生成"""
        templates = self.topic_templates.get(article_type, self.topic_templates['tutorial'])
        template = random.choice(templates)
        
        # 変数を置換
        current_month = datetime.now().month
        
        topic = template.format(
            tool=tool_name or "AI音楽ツール",
            month=current_month,
            genre=random.choice(self.genres),
            tool1=random.choice(['Suno', 'Udio', 'MusicGen']),
            tool2=random.choice(['Stable Audio', 'AIVA'])
        )
        
        return topic
    
    def select_article_type(self) -> str:
        """記事タイプを重み付きで選択"""
        types = list(self.type_weights.keys())
        weights = list(self.type_weights.values())
        return random.choices(types, weights=weights)[0]
    
    def select_tool_name(self) -> str:
        """ツール名を重み付きで選択"""
        tools = list(self.tool_weights.keys())
        weights = list(self.tool_weights.values())
        return random.choices(tools, weights=weights)[0]


def signal_handler(signum, frame):
    """シグナルハンドラー"""
    logger.info("\n🛑 停止シグナルを受信しました")
    sys.exit(0)


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AI Melody Kobo - 連続記事投稿システム'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='投稿間隔（分）デフォルト: 10分'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='現在の状況を表示'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='1回だけテスト投稿'
    )
    
    args = parser.parse_args()
    
    # シグナルハンドラーを設定
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        publisher = ContinuousArticlePublisher(interval_minutes=args.interval)
        
        if args.status:
            publisher.status()
        elif args.test:
            logger.info("🧪 テスト投稿を実行中...")
            result = publisher.generate_and_publish_once()
            if result['success']:
                print(f"✅ テスト投稿成功: {result['title']}")
            else:
                print(f"❌ テスト投稿失敗: {result.get('error')}")
        else:
            publisher.run_continuous()
            
    except Exception as e:
        logger.error(f"💥 システムエラー: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()