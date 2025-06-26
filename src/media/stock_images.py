"""
Stock Image Manager for AI Melody Kobo
記事に適した画像を自動で取得・管理
"""

import os
import requests
import logging
from typing import Dict, List, Optional
from pathlib import Path
import json
from datetime import datetime
import random

logger = logging.getLogger(__name__)


class StockImageManager:
    """ストック画像を管理するクラス"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        画像マネージャーの初期化
        
        Args:
            cache_dir: キャッシュディレクトリ
        """
        self.cache_dir = Path(cache_dir or "cache/images")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Unsplash API (無料枠)
        self.unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY', 'demo')
        
        # AI音楽関連の画像テーマ
        self.music_themes = {
            'instruments': [
                'synthesizer', 'midi keyboard', 'music studio',
                'electronic music', 'digital piano', 'music production'
            ],
            'technology': [
                'artificial intelligence', 'computer music', 'digital audio',
                'music software', 'audio interface', 'music technology'
            ],
            'jpop': [
                'tokyo neon', 'japanese city', 'japan music',
                'tokyo night', 'shibuya', 'japanese culture'
            ],
            'general': [
                'music notes', 'sound waves', 'headphones',
                'music studio', 'audio production', 'creative workspace'
            ]
        }
        
        # デモ用の画像URL（Unsplash APIキーがない場合の代替）
        self.demo_images = {
            'synthesizer': 'https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=1200&h=800&fit=crop',
            'music_studio': 'https://images.unsplash.com/photo-1598653222000-6b7b7a552625?w=1200&h=800&fit=crop',
            'midi_keyboard': 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=1200&h=800&fit=crop',
            'headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1200&h=800&fit=crop',
            'sound_waves': 'https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=1200&h=800&fit=crop',
            'tokyo_night': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1200&h=800&fit=crop',
            'music_production': 'https://images.unsplash.com/photo-1519508234439-4f23643125c1?w=1200&h=800&fit=crop',
            'ai_technology': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=800&fit=crop'
        }
    
    def get_image_for_topic(self, topic: str, keywords: List[str] = None) -> Dict[str, str]:
        """
        トピックに適した画像を取得
        
        Args:
            topic: 記事のトピック
            keywords: 追加のキーワード
            
        Returns:
            画像情報の辞書
        """
        # キーワードから適切なテーマを選択
        theme = self._select_theme(topic, keywords)
        
        # デモモードでの画像選択
        if self.unsplash_access_key == 'demo':
            return self._get_demo_image(theme)
        
        # 実際のAPI呼び出し（将来の実装用）
        # return self._fetch_from_unsplash(theme)
        
        return self._get_demo_image(theme)
    
    def _select_theme(self, topic: str, keywords: List[str] = None) -> str:
        """トピックとキーワードから適切なテーマを選択"""
        topic_lower = topic.lower()
        
        if keywords:
            keywords_lower = [k.lower() for k in keywords]
            if any('jpop' in k or 'j-pop' in k for k in keywords_lower):
                return 'jpop'
            elif any('ai' in k or '人工知能' in k for k in keywords_lower):
                return 'technology'
        
        if 'jpop' in topic_lower or 'j-pop' in topic_lower:
            return 'jpop'
        elif 'シンセ' in topic or 'synth' in topic_lower:
            return 'instruments'
        elif 'ai' in topic_lower or '人工知能' in topic:
            return 'technology'
        
        return 'general'
    
    def _get_demo_image(self, theme: str) -> Dict[str, str]:
        """デモ画像を取得"""
        # テーマに基づいて画像を選択
        if theme == 'jpop':
            image_key = 'tokyo_night'
        elif theme == 'technology':
            image_key = 'ai_technology'
        elif theme == 'instruments':
            image_key = random.choice(['synthesizer', 'midi_keyboard', 'music_studio'])
        else:
            image_key = random.choice(['headphones', 'sound_waves', 'music_production'])
        
        return {
            'url': self.demo_images[image_key],
            'alt': f"AI音楽制作 - {image_key.replace('_', ' ').title()}",
            'credits': 'Photo by Unsplash',
            'description': self._get_image_description(image_key)
        }
    
    def _get_image_description(self, image_key: str) -> str:
        """画像の説明文を生成"""
        descriptions = {
            'synthesizer': 'モダンなシンセサイザーでAI音楽を制作',
            'music_studio': 'プロフェッショナルな音楽制作スタジオ',
            'midi_keyboard': 'MIDIキーボードでメロディを入力',
            'headphones': '高品質なヘッドフォンで音楽制作',
            'sound_waves': 'デジタル音波のビジュアライゼーション',
            'tokyo_night': '東京の夜景とJ-POPカルチャー',
            'music_production': 'DAWを使った音楽プロダクション',
            'ai_technology': 'AI技術と音楽の融合'
        }
        return descriptions.get(image_key, 'AI音楽制作のイメージ')
    
    def get_multiple_images(self, topics: List[str], count: int = 3) -> List[Dict[str, str]]:
        """
        複数の画像を取得
        
        Args:
            topics: トピックのリスト
            count: 取得する画像数
            
        Returns:
            画像情報のリスト
        """
        images = []
        used_keys = set()
        
        for i, topic in enumerate(topics[:count]):
            theme = self._select_theme(topic, None)
            
            # 重複を避けて画像を選択
            available_keys = [k for k in self.demo_images.keys() if k not in used_keys]
            if not available_keys:
                available_keys = list(self.demo_images.keys())
            
            # テーマに合った画像を優先
            theme_keys = []
            if theme == 'jpop':
                theme_keys = [k for k in available_keys if 'tokyo' in k or 'japan' in k]
            elif theme == 'technology':
                theme_keys = [k for k in available_keys if 'ai' in k or 'tech' in k]
            elif theme == 'instruments':
                theme_keys = [k for k in available_keys if 'synth' in k or 'midi' in k or 'studio' in k]
            
            if not theme_keys:
                theme_keys = available_keys
            
            image_key = random.choice(theme_keys)
            used_keys.add(image_key)
            
            images.append({
                'url': self.demo_images[image_key],
                'alt': f"AI音楽制作 - {topic}",
                'credits': 'Photo by Unsplash',
                'description': self._get_image_description(image_key)
            })
        
        return images
    
    def download_image(self, url: str, filename: str = None) -> str:
        """
        画像をダウンロードしてローカルに保存
        
        Args:
            url: 画像URL
            filename: 保存ファイル名
            
        Returns:
            保存したファイルパス
        """
        if not filename:
            filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        filepath = self.cache_dir / filename
        
        # キャッシュが存在する場合はそれを返す
        if filepath.exists():
            logger.info(f"Using cached image: {filepath}")
            return str(filepath)
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Downloaded image: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to download image: {str(e)}")
            raise