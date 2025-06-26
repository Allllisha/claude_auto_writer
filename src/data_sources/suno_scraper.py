"""
Suno Information Collector
AI Melody Kobo - Suno関連情報の収集モジュール
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


class SunoInfoCollector:
    """Suno関連情報を収集するクラス"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        情報収集器の初期化
        
        Args:
            cache_dir: キャッシュディレクトリのパス
        """
        self.cache_dir = Path(cache_dir or "data/suno_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 情報源の定義
        self.sources = {
            'official_blog': 'https://www.suno.ai/blog',
            'discord': 'https://discord.com/channels/suno',  # 実際のDiscord APIが必要
            'reddit': 'https://www.reddit.com/r/suno/.rss',
            'twitter': 'https://twitter.com/suno_ai_'  # Twitter APIが必要
        }
        
        # キャッシュ有効期間（時間）
        self.cache_duration = 24
    
    def collect_latest_info(self) -> str:
        """最新のSuno情報を収集してまとめる"""
        info_items = []
        
        # 各ソースから情報収集を試みる
        try:
            # 公式ブログ（仮想実装）
            blog_items = self._fetch_blog_posts()
            info_items.extend(blog_items)
        except Exception as e:
            logger.warning(f"ブログ情報収集エラー: {str(e)}")
        
        try:
            # Reddit RSS
            reddit_items = self._fetch_reddit_posts()
            info_items.extend(reddit_items)
        except Exception as e:
            logger.warning(f"Reddit情報収集エラー: {str(e)}")
        
        # 情報を整形
        if info_items:
            summary = self._format_info_summary(info_items)
            return summary
        else:
            return self._get_cached_info()
    
    def _fetch_blog_posts(self) -> List[Dict[str, str]]:
        """Suno公式ブログから最新記事を取得（仮想実装）"""
        # 実際の実装では、ブログのスクレイピングやAPIを使用
        # ここではモックデータを返す
        mock_posts = [
            {
                'title': 'Suno V3.5 アップデート：新しいボーカルスタイル追加',
                'date': datetime.now().isoformat(),
                'summary': '10種類の新しいボーカルスタイルが追加され、より多様な音楽表現が可能に。',
                'url': 'https://www.suno.ai/blog/v3-5-update'
            },
            {
                'title': 'コミュニティスポットライト：今月の優秀作品',
                'date': (datetime.now() - timedelta(days=3)).isoformat(),
                'summary': 'Sunoユーザーが作成した素晴らしい楽曲を紹介。',
                'url': 'https://www.suno.ai/blog/community-spotlight'
            }
        ]
        
        return mock_posts
    
    def _fetch_reddit_posts(self) -> List[Dict[str, str]]:
        """RedditのSunoサブレディットから投稿を取得"""
        items = []
        
        try:
            # RSSフィードをパース
            feed = feedparser.parse(self.sources['reddit'])
            
            for entry in feed.entries[:5]:  # 最新5件
                items.append({
                    'title': entry.title,
                    'date': entry.get('published', ''),
                    'summary': self._clean_html(entry.get('summary', ''))[:200] + '...',
                    'url': entry.link,
                    'source': 'Reddit'
                })
        except Exception as e:
            logger.error(f"Reddit RSSパースエラー: {str(e)}")
        
        return items
    
    def _clean_html(self, html_text: str) -> str:
        """HTMLタグを除去してプレーンテキストを返す"""
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text().strip()
    
    def _format_info_summary(self, info_items: List[Dict[str, str]]) -> str:
        """収集した情報を整形"""
        summary_parts = ["収集したSuno最新情報:\n"]
        
        for item in info_items[:10]:  # 最大10件
            summary_parts.append(
                f"・{item['title']}\n"
                f"  {item.get('summary', '')}\n"
                f"  出典: {item.get('source', 'Unknown')} ({item.get('date', '')})\n"
            )
        
        return "\n".join(summary_parts)
    
    def _get_cached_info(self) -> str:
        """キャッシュから情報を取得"""
        cache_file = self.cache_dir / "latest_info.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    
                # キャッシュの有効性を確認
                cached_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cached_time < timedelta(hours=self.cache_duration):
                    return cache_data['content']
            except Exception as e:
                logger.error(f"キャッシュ読み込みエラー: {str(e)}")
        
        return ""
    
    def _save_to_cache(self, content: str):
        """情報をキャッシュに保存"""
        cache_file = self.cache_dir / "latest_info.json"
        
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'content': content
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"キャッシュ保存エラー: {str(e)}")
    
    def search_suno_tutorials(self, topic: str) -> List[Dict[str, str]]:
        """特定トピックのSunoチュートリアルを検索"""
        # 実装では、YouTube API、ブログ検索などを使用
        # ここではモックデータを返す
        return [
            {
                'title': f'Sunoで{topic}を作る方法',
                'url': 'https://example.com/tutorial',
                'type': 'video',
                'duration': '10:34'
            }
        ]
    
    def get_trending_prompts(self) -> List[Dict[str, Any]]:
        """トレンドのSunoプロンプトを取得"""
        # 実装では、コミュニティから人気のプロンプトを収集
        return [
            {
                'prompt': 'Upbeat J-pop with catchy chorus, female vocal, 120 BPM',
                'genre': 'J-POP',
                'likes': 1234,
                'creator': 'SunoUser123'
            },
            {
                'prompt': 'Cinematic orchestral piece, epic and emotional, film score style',
                'genre': 'Orchestral',
                'likes': 890,
                'creator': 'FilmComposer'
            }
        ]
    
    def get_community_stats(self) -> Dict[str, Any]:
        """Sunoコミュニティの統計情報を取得"""
        # 実装では、Discord API、フォーラムAPIなどから取得
        return {
            'total_users': 50000,
            'active_today': 5000,
            'songs_created_today': 10000,
            'trending_genres': ['J-POP', 'Lo-fi', 'EDM', 'Rock'],
            'featured_artist': {
                'name': 'AI Music Creator',
                'songs': 150,
                'followers': 2000
            }
        }
    
    def monitor_updates(self) -> List[Dict[str, str]]:
        """Sunoのアップデート情報を監視"""
        updates = []
        
        # バージョン情報の確認（仮想実装）
        current_version = self._get_current_version()
        if current_version:
            updates.append({
                'type': 'version',
                'title': f'Suno {current_version} リリース',
                'changes': '新機能とバグ修正'
            })
        
        return updates
    
    def _get_current_version(self) -> Optional[str]:
        """現在のSunoバージョンを取得"""
        # 実装では、APIやウェブスクレイピングを使用
        return "V3.5"