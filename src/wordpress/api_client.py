"""
WordPress REST API Client
AI Melody Kobo - WordPress記事自動投稿システム
"""

import os
import base64
import json
import requests
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import logging
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

logger = logging.getLogger(__name__)


class WordPressAPIError(Exception):
    """WordPress API関連のエラー"""
    pass


class WordPressClient:
    """WordPress REST APIクライアント"""
    
    def __init__(self, 
                 api_url: Optional[str] = None,
                 username: Optional[str] = None,
                 app_password: Optional[str] = None):
        """
        WordPress APIクライアントの初期化
        
        Args:
            api_url: WordPress REST APIのURL
            username: WordPressユーザー名
            app_password: アプリケーションパスワード
        """
        self.api_url = api_url or os.getenv('WORDPRESS_API_URL')
        self.username = username or os.getenv('WORDPRESS_USERNAME')
        self.app_password = app_password or os.getenv('WORDPRESS_APP_PASSWORD')
        
        if not all([self.api_url, self.username, self.app_password]):
            raise ValueError("WordPress認証情報が不足しています")
        
        # Basic認証ヘッダーの準備
        self.headers = self._prepare_auth_headers()
        
    def _prepare_auth_headers(self) -> Dict[str, str]:
        """認証ヘッダーを準備"""
        credentials = f"{self.username}:{self.app_password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode('ascii')
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Melody-Kobo/1.0',
            'Accept': 'application/json'
        }
    
    def test_connection(self) -> bool:
        """APIへの接続をテスト"""
        try:
            response = requests.get(
                f"{self.api_url}/users/me",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"接続テスト失敗: {str(e)}")
            return False
    
    def create_post(self, 
                   title: str,
                   content: str,
                   status: str = 'draft',
                   categories: List[int] = None,
                   tags: List[int] = None,
                   featured_media: Optional[int] = None,
                   excerpt: Optional[str] = None,
                   meta_description: Optional[str] = None) -> Dict:
        """
        新規記事を作成
        
        Args:
            title: 記事タイトル
            content: 記事本文（HTML）
            status: 公開ステータス（'draft', 'publish', 'private'）
            categories: カテゴリーIDのリスト
            tags: タグIDのリスト
            featured_media: アイキャッチ画像のメディアID
            excerpt: 抜粋
            meta_description: メタディスクリプション
            
        Returns:
            作成された記事の情報
        """
        data = {
            'title': title,
            'content': content,
            'status': status,
            'author': 1,  # AIクリエイター アリサ
            'format': 'standard',
            'comment_status': 'open',
            'ping_status': 'open'
        }
        
        if categories:
            data['categories'] = categories
        if tags:
            data['tags'] = tags
        if featured_media:
            data['featured_media'] = featured_media
        if excerpt:
            data['excerpt'] = excerpt
        if meta_description:
            data['meta'] = {'description': meta_description}
        
        try:
            response = requests.post(
                f"{self.api_url}/posts",
                headers=self.headers,
                data=json.dumps(data),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"記事作成エラー: {str(e)}")
            raise WordPressAPIError(f"記事の作成に失敗しました: {str(e)}")
    
    def update_post(self, post_id: int, **kwargs) -> Dict:
        """既存の記事を更新"""
        try:
            response = requests.post(
                f"{self.api_url}/posts/{post_id}",
                headers=self.headers,
                data=json.dumps(kwargs),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"記事更新エラー: {str(e)}")
            raise WordPressAPIError(f"記事の更新に失敗しました: {str(e)}")
    
    def get_post(self, post_id: int) -> Dict:
        """投稿を取得"""
        try:
            response = requests.get(
                f"{self.api_url}/posts/{post_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"投稿取得エラー: {str(e)}")
            raise WordPressAPIError(f"投稿の取得に失敗しました: {str(e)}")
    
    def get_categories(self) -> List[Dict]:
        """カテゴリー一覧を取得"""
        try:
            response = requests.get(
                f"{self.api_url}/categories",
                headers=self.headers,
                params={'per_page': 100},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"カテゴリー取得エラー: {str(e)}")
            return []
    
    def create_category(self, name: str, description: str = "", 
                       slug: Optional[str] = None, parent: int = 0) -> Dict:
        """新規カテゴリーを作成"""
        data = {
            'name': name,
            'description': description,
            'parent': parent
        }
        if slug:
            data['slug'] = slug
            
        try:
            response = requests.post(
                f"{self.api_url}/categories",
                headers=self.headers,
                data=json.dumps(data),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"カテゴリー作成エラー: {str(e)}")
            raise WordPressAPIError(f"カテゴリーの作成に失敗しました: {str(e)}")
    
    def get_tags(self) -> List[Dict]:
        """タグ一覧を取得"""
        try:
            response = requests.get(
                f"{self.api_url}/tags",
                headers=self.headers,
                params={'per_page': 100},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"タグ取得エラー: {str(e)}")
            return []
    
    def create_tag(self, name: str, description: str = "", 
                  slug: Optional[str] = None) -> Dict:
        """新規タグを作成"""
        # タグ名の検証と修正
        if not name or not name.strip():
            logger.warning("空のタグ名は作成できません")
            return None
            
        # タグ名をトリムして正規化
        name = name.strip()
        
        # WordPressのタグ名制限（200文字）を確認
        if len(name) > 200:
            name = name[:200]
            logger.warning(f"タグ名が長すぎるため切り詰めました: {name}")
        
        # スラッグを自動生成（日本語対応）
        if not slug:
            import unicodedata
            import re
            # 日本語をローマ字に変換せず、そのまま使用
            # WordPressが自動的に適切なスラッグを生成
            slug = None
        
        data = {
            'name': name,
            'description': description
        }
        if slug:
            data['slug'] = slug
            
        try:
            logger.debug(f"タグ作成リクエスト: {data}")
            response = requests.post(
                f"{self.api_url}/tags",
                headers=self.headers,
                data=json.dumps(data),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"タグ作成エラー - タグ名: '{name}', エラー: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"レスポンス内容: {e.response.text}")
            # タグ作成に失敗した場合は、既存のタグを探す
            try:
                existing_tags = self.get_tags()
                for tag in existing_tags:
                    if tag['name'] == name:
                        logger.info(f"既存のタグを使用: {name}")
                        return tag
            except:
                pass
            # それでも見つからない場合はエラー
            raise WordPressAPIError(f"タグの作成に失敗しました: {str(e)}")
    
    def upload_media(self, file_path: str = None, file_data: bytes = None,
                    filename: str = None, title: str = None, 
                    alt_text: str = None, mime_type: str = 'image/png') -> Dict:
        """メディア（画像等）をアップロード
        
        Args:
            file_path: アップロードするファイルのパス
            file_data: ファイルのバイトデータ（file_pathの代替）
            filename: ファイル名（file_data使用時は必須）
            title: メディアのタイトル
            alt_text: 代替テキスト
            mime_type: MIMEタイプ
            
        Returns:
            アップロードされたメディアの情報
        """
        if file_path:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                filename = os.path.basename(file_path)
        elif not file_data or not filename:
            raise ValueError("file_pathまたは(file_dataとfilename)が必要です")
        
        files = {
            'file': (filename, file_data, mime_type)
        }
        
        headers = self.headers.copy()
        headers.pop('Content-Type')  # multipart/form-dataの場合は削除
        
        data = {}
        if title:
            data['title'] = title
        if alt_text:
            data['alt_text'] = alt_text
        
        try:
            response = requests.post(
                f"{self.api_url}/media",
                headers=headers,
                files=files,
                data=data,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"メディアアップロードエラー: {str(e)}")
            raise WordPressAPIError(f"メディアのアップロードに失敗しました: {str(e)}")
    
    def find_or_create_category(self, name: str) -> int:
        """カテゴリーを検索し、なければ作成"""
        categories = self.get_categories()
        for cat in categories:
            if cat['name'] == name:
                return cat['id']
        
        # カテゴリーが存在しない場合は作成
        new_cat = self.create_category(name)
        return new_cat['id']
    
    def find_or_create_tags(self, tag_names: List[str]) -> List[int]:
        """タグを検索し、なければ作成"""
        existing_tags = self.get_tags()
        tag_ids = []
        
        for tag_name in tag_names:
            # 空のタグ名はスキップ
            if not tag_name or not tag_name.strip():
                continue
                
            tag_name = tag_name.strip()
            tag_id = None
            
            # 既存のタグを検索
            for tag in existing_tags:
                if tag['name'].lower() == tag_name.lower():
                    tag_id = tag['id']
                    break
            
            if not tag_id:
                # タグが存在しない場合は作成
                try:
                    new_tag = self.create_tag(tag_name)
                    if new_tag:
                        tag_id = new_tag['id']
                        # 新しく作成したタグを既存タグリストに追加
                        existing_tags.append(new_tag)
                except Exception as e:
                    logger.warning(f"タグ '{tag_name}' の作成をスキップ: {str(e)}")
                    continue
            
            if tag_id:
                tag_ids.append(tag_id)
        
        return tag_ids