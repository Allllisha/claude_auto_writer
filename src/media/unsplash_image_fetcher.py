"""
Unsplash Image Fetcher for AI Melody Kobo
Unsplash APIから記事内容に応じた画像を取得
"""

import os
import requests
import logging
from typing import Dict, Optional, List, Tuple
from dotenv import load_dotenv
import random
import time

load_dotenv()

logger = logging.getLogger(__name__)


class UnsplashImageFetcher:
    """Unsplash APIから画像を取得するクラス"""
    
    def __init__(self, access_key: Optional[str] = None):
        """
        初期化
        
        Args:
            access_key: Unsplash APIアクセスキー
        """
        self.access_key = access_key or os.getenv('UNSPLASH_ACCESS_KEY')
        if not self.access_key:
            logger.warning("Unsplash APIキーが設定されていません。")
        
        self.base_url = "https://api.unsplash.com"
        self.headers = {
            "Authorization": f"Client-ID {self.access_key}"
        }
        
        # 画像検索キーワードマッピング
        self.keyword_mappings = {
            # 音楽関連
            "音楽生成": ["music production", "music studio", "synthesizer", "electronic music"],
            "AI音楽": ["artificial intelligence music", "digital music", "music technology", "future music"],
            "作曲": ["music composition", "composer", "music writing", "sheet music"],
            "BGM": ["background music", "soundtrack", "ambient music", "music studio"],
            
            # ツール別
            "Suno": ["music software", "digital audio workstation", "music app", "music creation"],
            "Udio": ["music interface", "audio software", "music dashboard", "sound design"],
            "MusicGen": ["music generator", "ai technology", "machine learning", "neural network"],
            "AudioCraft": ["audio production", "sound engineering", "music technology", "audio interface"],
            "Stable Audio": ["audio waves", "sound visualization", "frequency", "audio spectrum"],
            
            # 技術関連
            "プログラミング": ["programming", "coding", "developer", "computer code"],
            "API": ["api development", "software development", "technology", "coding"],
            "React": ["react javascript", "web development", "frontend", "coding"],
            "Python": ["python programming", "code editor", "software development", "programming"],
            "Transformer": ["neural network", "machine learning", "ai technology", "deep learning"],
            
            # ビジネス関連
            "収益化": ["business success", "money growth", "financial", "entrepreneur"],
            "副業": ["side business", "freelance", "work from home", "laptop business"],
            "起業": ["startup", "entrepreneur", "business meeting", "innovation"],
            
            # インターフェース関連
            "インターフェース": ["user interface", "app design", "ux design", "dashboard"],
            "UI": ["ui design", "interface design", "mobile app", "web design"],
            "ダッシュボード": ["dashboard design", "analytics", "data visualization", "admin panel"],
            
            # その他
            "チュートリアル": ["tutorial", "learning", "education", "teaching"],
            "ガイド": ["guide book", "instruction", "how to", "learning"],
            "初心者": ["beginner", "learning", "first step", "starting"],
            "設定": ["settings", "configuration", "setup", "preferences"],
            "グラフ": ["graph", "chart", "data visualization", "analytics"],
            "波形": ["sound wave", "audio waveform", "frequency", "oscilloscope"]
        }
    
    def search_images(self, query: str, per_page: int = 30) -> List[Dict]:
        """
        画像を検索
        
        Args:
            query: 検索クエリ
            per_page: 取得する画像数
            
        Returns:
            画像情報のリスト
        """
        if not self.access_key:
            logger.warning("Unsplash APIキーが設定されていないため、検索できません")
            return []
        
        url = f"{self.base_url}/search/photos"
        params = {
            "query": query,
            "per_page": per_page,
            "orientation": "landscape"  # 横向きの画像を優先
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get("results", [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Unsplash API エラー: {str(e)}")
            return []
    
    def get_image_for_content(self, content_description: str, 
                            article_context: Optional[str] = None) -> Optional[Dict]:
        """
        コンテンツに適した画像を取得
        
        Args:
            content_description: 画像の説明（日本語）
            article_context: 記事のコンテキスト
            
        Returns:
            画像情報（URL、作者情報など）
        """
        # 日本語キーワードから英語検索クエリを生成
        search_queries = self._generate_search_queries(content_description, article_context)
        
        all_images = []
        for query in search_queries[:3]:  # 最初の3つのクエリを試す
            images = self.search_images(query, per_page=10)
            all_images.extend(images)
            
            if len(all_images) >= 5:
                break
            
            # レート制限対策
            time.sleep(0.5)
        
        if not all_images:
            logger.warning(f"画像が見つかりませんでした: {content_description}")
            return None
        
        # ランダムに1つ選択（重複を避けるため）
        selected_image = random.choice(all_images)
        
        return {
            "url": selected_image["urls"]["regular"],  # 通常サイズ
            "download_url": selected_image["links"]["download"],
            "author": selected_image["user"]["name"],
            "author_url": selected_image["user"]["links"]["html"],
            "description": selected_image.get("description", selected_image.get("alt_description", "")),
            "unsplash_url": selected_image["links"]["html"]
        }
    
    def _generate_search_queries(self, description: str, context: Optional[str]) -> List[str]:
        """
        日本語の説明から英語検索クエリを生成
        
        Args:
            description: 日本語の説明
            context: 記事のコンテキスト
            
        Returns:
            検索クエリのリスト
        """
        queries = []
        
        # キーワードマッピングから関連するクエリを探す
        for jp_keyword, en_keywords in self.keyword_mappings.items():
            if jp_keyword in description or (context and jp_keyword in context):
                queries.extend(en_keywords)
        
        # 一般的なフォールバック
        if not queries:
            if "音楽" in description:
                queries = ["music", "sound", "audio"]
            elif "AI" in description or "人工知能" in description:
                queries = ["artificial intelligence", "technology", "future"]
            elif "ビジネス" in description or "収益" in description:
                queries = ["business", "success", "entrepreneur"]
            else:
                queries = ["technology", "digital", "modern"]
        
        # コンテキストから追加のクエリを生成
        if context:
            if "Suno" in context:
                queries.append("music creation software")
            elif "React" in context or "プログラミング" in context:
                queries.append("web development")
            elif "収益化" in context:
                queries.append("online business")
        
        # 重複を削除して返す
        return list(set(queries))
    
    def download_image(self, image_info: Dict) -> bytes:
        """
        画像をダウンロード
        
        Args:
            image_info: get_image_for_contentで取得した画像情報
            
        Returns:
            画像データ（bytes）
        """
        try:
            # Unsplashのダウンロードトリガー（統計用）
            if "download_url" in image_info and self.access_key:
                requests.get(image_info["download_url"], headers=self.headers)
            
            # 実際の画像をダウンロード
            response = requests.get(image_info["url"])
            response.raise_for_status()
            
            return response.content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"画像ダウンロードエラー: {str(e)}")
            raise
    
    def get_attribution_html(self, image_info: Dict) -> str:
        """
        画像の帰属表示HTMLを生成
        
        Args:
            image_info: 画像情報
            
        Returns:
            帰属表示のHTML
        """
        return f'Photo by <a href="{image_info["author_url"]}?utm_source=ai_melody_kobo&utm_medium=referral" target="_blank">{image_info["author"]}</a> on <a href="{image_info["unsplash_url"]}?utm_source=ai_melody_kobo&utm_medium=referral" target="_blank">Unsplash</a>'


# Pexels APIも追加可能
class PexelsImageFetcher:
    """Pexels APIから画像を取得するクラス（代替オプション）"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('PEXELS_API_KEY')
        self.base_url = "https://api.pexels.com/v1"
        self.headers = {
            "Authorization": self.api_key
        } if self.api_key else {}
    
    # 実装は省略（Unsplashと同様のインターフェース）