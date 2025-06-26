"""
Configuration Settings
AI Melody Kobo - システム設定管理
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logging

# 環境変数の読み込み
load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    """システム設定を管理するクラス"""
    
    # デフォルト設定
    DEFAULT_CONFIG = {
        'wordpress': {
            'api_url': os.getenv('WORDPRESS_API_URL'),
            'username': os.getenv('WORDPRESS_USERNAME'),
            'default_status': 'draft',
            'default_category': 'Suno',
            'auto_tags': ['Suno', 'AI作曲', 'AIメロディ工房']
        },
        'ai': {
            'default_client': 'claude',
            'temperature': 0.7,
            'max_tokens': 4000,
            'retry_attempts': 3
        },
        'article': {
            'min_words': 1500,
            'max_words': 3000,
            'default_type': 'news',
            'required_keywords': ['Suno'],
            'cta_positions': ['middle', 'end']
        },
        'suno_info': {
            'cache_duration_hours': 24,
            'sources': {
                'official_blog': True,
                'reddit': True,
                'discord': False,
                'twitter': False
            }
        },
        'logging': {
            'level': 'INFO',
            'file': 'logs/ai_melody_kobo.log',
            'max_bytes': 10485760,  # 10MB
            'backup_count': 5
        },
        'paths': {
            'data_dir': 'data',
            'cache_dir': 'data/cache',
            'history_dir': 'data/generation_history',
            'persona_file': 'data/alisa_persona.json'
        }
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        設定の初期化
        
        Args:
            config_file: カスタム設定ファイルのパス
        """
        self.config_file = config_file or "config/settings.json"
        self.config = self.DEFAULT_CONFIG.copy()
        
        # カスタム設定を読み込み
        self._load_config()
        
        # 必要なディレクトリを作成
        self._create_directories()
    
    def _load_config(self):
        """設定ファイルから設定を読み込み"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    custom_config = json.load(f)
                    self._merge_config(self.config, custom_config)
                logger.info(f"設定ファイルを読み込みました: {self.config_file}")
            except Exception as e:
                logger.error(f"設定ファイル読み込みエラー: {str(e)}")
    
    def _merge_config(self, base: Dict, custom: Dict):
        """カスタム設定をベース設定にマージ"""
        for key, value in custom.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def _create_directories(self):
        """必要なディレクトリを作成"""
        for path_key, path_value in self.config['paths'].items():
            if path_value and 'dir' in path_key:
                Path(path_value).mkdir(parents=True, exist_ok=True)
        
        # ログディレクトリ
        log_file = self.config['logging']['file']
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    def save_config(self):
        """現在の設定をファイルに保存"""
        try:
            # 設定ファイルのディレクトリを作成
            Path(self.config_file).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.info(f"設定を保存しました: {self.config_file}")
        except Exception as e:
            logger.error(f"設定保存エラー: {str(e)}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        ドット記法で設定値を取得
        
        Args:
            key_path: 設定キーのパス（例: 'wordpress.default_status'）
            default: デフォルト値
            
        Returns:
            設定値
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        ドット記法で設定値を設定
        
        Args:
            key_path: 設定キーのパス
            value: 設定する値
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def get_wordpress_config(self) -> Dict[str, Any]:
        """WordPress関連の設定を取得"""
        return self.config.get('wordpress', {})
    
    def get_ai_config(self) -> Dict[str, Any]:
        """AI関連の設定を取得"""
        return self.config.get('ai', {})
    
    def get_article_config(self) -> Dict[str, Any]:
        """記事生成関連の設定を取得"""
        return self.config.get('article', {})
    
    def validate_config(self) -> bool:
        """設定の妥当性を検証"""
        errors = []
        
        # WordPress設定の検証
        if not self.get('wordpress.api_url'):
            errors.append("WordPress API URLが設定されていません")
        
        if not self.get('wordpress.username'):
            errors.append("WordPressユーザー名が設定されていません")
        
        # 必須キーワードの検証
        required_keywords = self.get('article.required_keywords', [])
        if 'Suno' not in required_keywords:
            errors.append("必須キーワードに'Suno'が含まれていません")
        
        if errors:
            for error in errors:
                logger.error(f"設定エラー: {error}")
            return False
        
        return True
    
    def export_config(self, export_path: str):
        """設定をエクスポート"""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.info(f"設定をエクスポートしました: {export_path}")
        except Exception as e:
            logger.error(f"設定エクスポートエラー: {str(e)}")
    
    def import_config(self, import_path: str):
        """設定をインポート"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
                self._merge_config(self.config, imported_config)
            logger.info(f"設定をインポートしました: {import_path}")
            self.save_config()
        except Exception as e:
            logger.error(f"設定インポートエラー: {str(e)}")


# グローバル設定インスタンス
config = Config()