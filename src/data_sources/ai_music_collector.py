"""
AI Music Information Collector
AI Melody Kobo - AI音楽ツール全般の情報収集モジュール
"""

import os
import requests
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class AIMusicInfoCollector:
    """AI音楽ツール関連情報を収集するクラス"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        情報収集器の初期化
        
        Args:
            cache_dir: キャッシュディレクトリのパス
        """
        self.cache_dir = Path(cache_dir or "data/ai_music_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # AI音楽ツールのリスト
        self.ai_music_tools = {
            'suno': {
                'name': 'Suno',
                'official_site': 'https://www.suno.ai',
                'blog': 'https://www.suno.ai/blog',
                'description': 'テキストから完全な楽曲を生成',
                'features': ['ボーカル生成', 'カスタムスタイル', '商用利用可能'],
                'keywords': ['Suno', 'Suno AI', 'AI作曲']
            },
            'udio': {
                'name': 'Udio',
                'official_site': 'https://www.udio.com',
                'description': '高品質なAI音楽生成プラットフォーム',
                'features': ['高音質生成', 'ジャンル多様性', 'リミックス機能'],
                'keywords': ['Udio', 'Udio AI', 'AI音楽生成']
            },
            'musicgen': {
                'name': 'MusicGen',
                'official_site': 'https://github.com/facebookresearch/audiocraft',
                'description': 'Meta社のオープンソース音楽生成AI',
                'features': ['オープンソース', 'カスタマイズ可能', 'ローカル実行'],
                'keywords': ['MusicGen', 'Meta AI', 'AudioCraft']
            },
            'stable_audio': {
                'name': 'Stable Audio',
                'official_site': 'https://stability.ai/stable-audio',
                'description': 'Stability AI社の音楽生成モデル',
                'features': ['高品質オーディオ', '長時間生成', 'プロンプト制御'],
                'keywords': ['Stable Audio', 'Stability AI', 'AI BGM']
            },
            'aiva': {
                'name': 'AIVA',
                'official_site': 'https://www.aiva.ai',
                'description': 'AI作曲家、映画音楽やゲーム音楽に特化',
                'features': ['オーケストラ作曲', '著作権管理', 'プロ向け'],
                'keywords': ['AIVA', 'AI作曲家', 'AI Orchestra']
            },
            'mubert': {
                'name': 'Mubert',
                'official_site': 'https://mubert.com',
                'description': 'リアルタイムAI音楽生成',
                'features': ['ストリーミング', 'ライセンスフリー', 'API提供'],
                'keywords': ['Mubert', 'AI BGM', 'ストリーミング音楽']
            },
            'soundraw': {
                'name': 'Soundraw',
                'official_site': 'https://soundraw.io',
                'description': 'AIによるカスタマイズ可能な音楽生成',
                'features': ['カスタマイズ可能', '商用利用可', '日本発'],
                'keywords': ['Soundraw', 'AI BGM作成', '日本製AI']
            },
            'boomy': {
                'name': 'Boomy',
                'official_site': 'https://boomy.com',
                'description': '初心者向けAI音楽制作プラットフォーム',
                'features': ['簡単操作', '配信サポート', '収益化対応'],
                'keywords': ['Boomy', 'AI音楽配信', '初心者向け']
            },
            'riffusion': {
                'name': 'Riffusion',
                'official_site': 'https://www.riffusion.com',
                'description': 'スペクトログラムベースのAI音楽生成',
                'features': ['リアルタイム生成', 'ビジュアル表現', '実験的'],
                'keywords': ['Riffusion', 'AI音楽実験', 'スペクトログラム']
            },
            'musiclm': {
                'name': 'MusicLM',
                'official_site': 'https://google-research.github.io/seanet/musiclm/examples/',
                'description': 'Google ResearchのAI音楽生成モデル',
                'features': ['高品質生成', 'テキスト記述', '研究プロジェクト'],
                'keywords': ['MusicLM', 'Google AI', 'AI研究']
            }
        }
        
        # 情報源の定義
        self.sources = {
            'reddit_ai_music': 'https://www.reddit.com/r/AImusic/.rss',
            'reddit_music_production': 'https://www.reddit.com/r/WeAreTheMusicMakers/.rss',
            'hacker_news': 'https://news.ycombinator.com/rss',
            'producthunt': 'https://www.producthunt.com/topics/artificial-intelligence/feed',
        }
        
        # キャッシュ有効期間（時間）
        self.cache_duration = 24
    
    def collect_all_tools_info(self) -> Dict[str, Any]:
        """全AI音楽ツールの情報を収集"""
        all_info = {
            'tools': self.ai_music_tools,
            'latest_news': [],
            'trending_tools': [],
            'comparison_data': self._generate_comparison_data(),
            'collected_at': datetime.now().isoformat()
        }
        
        # 各ツールの最新情報を収集
        for tool_id, tool_info in self.ai_music_tools.items():
            try:
                tool_news = self._fetch_tool_specific_news(tool_id, tool_info)
                all_info['latest_news'].extend(tool_news)
            except Exception as e:
                logger.warning(f"{tool_info['name']}の情報収集エラー: {str(e)}")
        
        # トレンドを分析
        all_info['trending_tools'] = self._analyze_trends(all_info['latest_news'])
        
        return all_info
    
    def collect_tool_specific_info(self, tool_name: str) -> Dict[str, Any]:
        """特定のAI音楽ツールの詳細情報を収集"""
        tool_id = tool_name.lower()
        if tool_id not in self.ai_music_tools:
            # 新しいツールの場合は基本情報を作成
            return self._create_new_tool_info(tool_name)
        
        tool_info = self.ai_music_tools[tool_id].copy()
        
        # 最新情報を追加
        tool_info['latest_updates'] = self._fetch_tool_specific_news(tool_id, tool_info)
        tool_info['tutorials'] = self._search_tutorials(tool_name)
        tool_info['user_reviews'] = self._fetch_user_reviews(tool_name)
        tool_info['comparison'] = self._compare_with_others(tool_id)
        
        return tool_info
    
    def _fetch_tool_specific_news(self, tool_id: str, tool_info: Dict) -> List[Dict]:
        """特定ツールのニュースを収集"""
        news_items = []
        
        # Reddit検索（実際の実装ではAPI使用）
        try:
            # モックデータ
            if tool_id == 'suno':
                news_items.extend([
                    {
                        'title': f'{tool_info["name"]} {datetime.now().year}年最新アップデート：新機能解説',
                        'date': datetime.now().isoformat(),
                        'summary': '最新バージョンで追加された機能について',
                        'source': 'AI Music Blog',
                        'tool': tool_info['name']
                    }
                ])
            elif tool_id == 'udio':
                news_items.extend([
                    {
                        'title': f'{tool_info["name"]}が日本語対応を開始',
                        'date': datetime.now().isoformat(),
                        'summary': '日本のユーザー向けに最適化されたインターフェース',
                        'source': 'Tech News',
                        'tool': tool_info['name']
                    }
                ])
        except Exception as e:
            logger.error(f"ニュース取得エラー: {str(e)}")
        
        return news_items
    
    def _generate_comparison_data(self) -> Dict[str, Any]:
        """AI音楽ツールの比較データを生成"""
        comparison = {
            'features': {
                'vocal_generation': ['suno', 'udio', 'musiclm'],
                'instrumental_only': ['musicgen', 'aiva', 'soundraw'],
                'commercial_use': ['suno', 'soundraw', 'mubert', 'aiva'],
                'free_tier': ['suno', 'musicgen', 'riffusion', 'boomy'],
                'api_available': ['mubert', 'aiva', 'musicgen'],
                'local_execution': ['musicgen', 'riffusion', 'stable_audio'],
                'japanese_support': ['soundraw', 'suno', 'udio']
            },
            'use_cases': {
                'content_creators': ['suno', 'soundraw', 'mubert'],
                'game_developers': ['aiva', 'mubert', 'soundraw'],
                'film_composers': ['aiva', 'stable_audio', 'musicgen'],
                'hobbyists': ['suno', 'boomy', 'riffusion'],
                'researchers': ['musicgen', 'musiclm', 'riffusion']
            },
            'pricing_tiers': {
                'free': ['musicgen', 'riffusion'],
                'freemium': ['suno', 'udio', 'boomy', 'soundraw'],
                'subscription': ['aiva', 'mubert', 'stable_audio'],
                'pay_per_use': ['mubert', 'aiva']
            }
        }
        
        return comparison
    
    def _analyze_trends(self, news_items: List[Dict]) -> List[Dict]:
        """トレンド分析"""
        # ツール別のニュース数をカウント
        tool_counts = {}
        for item in news_items:
            tool = item.get('tool', 'Unknown')
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        # トレンドリストを作成
        trends = []
        for tool, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True):
            trends.append({
                'tool': tool,
                'mention_count': count,
                'trend': 'rising' if count > 2 else 'stable'
            })
        
        return trends[:5]  # トップ5
    
    def _search_tutorials(self, tool_name: str) -> List[Dict]:
        """チュートリアルを検索"""
        # 実装では YouTube API や ブログ検索を使用
        return [
            {
                'title': f'{tool_name}完全ガイド：初心者から上級者まで',
                'type': 'blog',
                'url': f'https://example.com/{tool_name.lower()}-guide',
                'language': 'ja'
            },
            {
                'title': f'{tool_name} Tutorial: Getting Started',
                'type': 'video',
                'url': f'https://youtube.com/watch?v=example',
                'language': 'en'
            }
        ]
    
    def _fetch_user_reviews(self, tool_name: str) -> Dict[str, Any]:
        """ユーザーレビューを収集"""
        # 実装では実際のレビューサイトから収集
        return {
            'average_rating': 4.5,
            'total_reviews': 1234,
            'pros': ['使いやすい', '高品質', '多機能'],
            'cons': ['価格が高い', '学習曲線あり'],
            'user_sentiment': 'positive'
        }
    
    def _compare_with_others(self, tool_id: str) -> Dict[str, Any]:
        """他のツールとの比較"""
        if tool_id not in self.ai_music_tools:
            return {}
        
        tool = self.ai_music_tools[tool_id]
        comparisons = {}
        
        # 類似ツールを見つける
        for other_id, other_tool in self.ai_music_tools.items():
            if other_id != tool_id:
                # 特徴の重複をチェック
                common_features = set(tool.get('features', [])) & set(other_tool.get('features', []))
                if len(common_features) >= 2:
                    comparisons[other_id] = {
                        'name': other_tool['name'],
                        'common_features': list(common_features),
                        'unique_to_this': list(set(tool.get('features', [])) - set(other_tool.get('features', []))),
                        'unique_to_other': list(set(other_tool.get('features', [])) - set(tool.get('features', [])))
                    }
        
        return comparisons
    
    def _create_new_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """新しいツールの基本情報を作成"""
        return {
            'name': tool_name,
            'official_site': f'https://www.{tool_name.lower()}.com',
            'description': f'{tool_name}は新しいAI音楽生成ツールです',
            'features': ['AI音楽生成'],
            'keywords': [tool_name, 'AI音楽'],
            'status': 'new_tool',
            'collected_at': datetime.now().isoformat()
        }
    
    def get_article_topics(self) -> List[Dict[str, str]]:
        """記事トピックの提案を生成"""
        current_year = datetime.now().year
        topics = []
        
        # ツール比較記事
        topics.append({
            'title': f'【{current_year}年最新】AI作曲ツール完全比較：Suno vs Udio vs MusicGen',
            'type': 'comparison',
            'keywords': ['AI作曲', '比較', 'Suno', 'Udio', 'MusicGen', f'{current_year}年']
        })
        
        # 用途別おすすめ記事
        topics.append({
            'title': 'YouTuber必見！AI BGM生成ツールおすすめ5選',
            'type': 'roundup',
            'keywords': ['AI BGM', 'YouTube', 'Soundraw', 'Mubert']
        })
        
        # 初心者ガイド
        topics.append({
            'title': 'AI音楽制作入門：無料で始められるツール完全ガイド',
            'type': 'beginner_guide',
            'keywords': ['AI音楽', '初心者', '無料', 'MusicGen', 'Riffusion']
        })
        
        # トレンド記事
        topics.append({
            'title': f'{current_year}年注目のAI音楽ツール最新トレンド',
            'type': 'trends',
            'keywords': ['AI音楽', 'トレンド', '最新', 'Stable Audio', f'{current_year}年']
        })
        
        return topics
    
    def search_by_use_case(self, use_case: str) -> List[Dict[str, Any]]:
        """用途別にツールを検索"""
        use_case_lower = use_case.lower()
        relevant_tools = []
        
        # 用途別マッピング
        use_case_mapping = {
            'youtube': ['suno', 'soundraw', 'mubert', 'boomy'],
            'game': ['aiva', 'mubert', 'soundraw', 'stable_audio'],
            'podcast': ['mubert', 'soundraw', 'musicgen'],
            'meditation': ['mubert', 'aiva', 'soundraw'],
            'commercial': ['soundraw', 'mubert', 'aiva', 'suno'],
            'experiment': ['musicgen', 'riffusion', 'musiclm'],
            'beginner': ['suno', 'boomy', 'soundraw']
        }
        
        # マッチするツールを検索
        for key, tool_ids in use_case_mapping.items():
            if key in use_case_lower:
                for tool_id in tool_ids:
                    if tool_id in self.ai_music_tools:
                        tool_info = self.ai_music_tools[tool_id].copy()
                        tool_info['relevance_score'] = 0.8 if tool_ids.index(tool_id) < 2 else 0.6
                        relevant_tools.append(tool_info)
        
        # 重複を削除して返す
        seen = set()
        unique_tools = []
        for tool in relevant_tools:
            if tool['name'] not in seen:
                seen.add(tool['name'])
                unique_tools.append(tool)
        
        return sorted(unique_tools, key=lambda x: x.get('relevance_score', 0), reverse=True)