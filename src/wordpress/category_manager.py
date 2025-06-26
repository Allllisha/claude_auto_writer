"""
カテゴリー・タグ管理システム
AI Melody Kobo - AI音楽ツール専門のカテゴリー構造
"""

from typing import Dict, List, Optional, Tuple
import logging
from .api_client import WordPressClient

logger = logging.getLogger(__name__)


class CategoryManager:
    """AI音楽ツール向けカテゴリー・タグ管理"""
    
    # AI音楽ツールのカテゴリー構造
    CATEGORY_STRUCTURE = {
        'AI音楽ツール': {
            'description': 'AI音楽制作ツールの総合カテゴリー',
            'slug': 'ai-music-tools',
            'children': {
                'Suno': {
                    'description': 'Suno AI音楽生成プラットフォームに関する記事',
                    'slug': 'suno'
                },
                'Udio': {
                    'description': 'Udio音楽生成ツールに関する記事',
                    'slug': 'udio'
                },
                'MusicGen': {
                    'description': 'Meta MusicGenに関する記事',
                    'slug': 'musicgen'
                },
                'Stable Audio': {
                    'description': 'Stable Audioに関する記事',
                    'slug': 'stable-audio'
                },
                'AIVA': {
                    'description': 'AIVA AI作曲ツールに関する記事',
                    'slug': 'aiva'
                }
            }
        },
        'チュートリアル': {
            'description': 'AI音楽ツールの使い方・実践ガイド',
            'slug': 'tutorials',
            'children': {
                '初心者向け': {
                    'description': 'AI音楽制作を始める方向けの基礎ガイド',
                    'slug': 'beginner-guides'
                },
                '実践テクニック': {
                    'description': '上級者向けの実践的なテクニック',
                    'slug': 'advanced-techniques'
                },
                'プロンプト作成': {
                    'description': '効果的なプロンプトの書き方',
                    'slug': 'prompt-engineering'
                }
            }
        },
        'AI音楽ニュース': {
            'description': 'AI音楽業界の最新ニュース・アップデート',
            'slug': 'ai-music-news',
            'children': {
                'ツールアップデート': {
                    'description': '各ツールの新機能・アップデート情報',
                    'slug': 'tool-updates'
                },
                '業界動向': {
                    'description': 'AI音楽業界のトレンド・動向',
                    'slug': 'industry-trends'
                }
            }
        },
        '作品紹介': {
            'description': 'AI音楽ツールで作成された作品の紹介',
            'slug': 'showcase',
            'children': {
                'ユーザー作品': {
                    'description': 'コミュニティメンバーの作品紹介',
                    'slug': 'user-creations'
                },
                '注目作品': {
                    'description': '特に優れたAI音楽作品の紹介',
                    'slug': 'featured-works'
                }
            }
        },
        '比較・レビュー': {
            'description': 'AI音楽ツールの比較・レビュー記事',
            'slug': 'reviews',
            'children': {
                'ツール比較': {
                    'description': '複数のAI音楽ツールの比較記事',
                    'slug': 'tool-comparisons'
                },
                '詳細レビュー': {
                    'description': '各ツールの詳細なレビュー',
                    'slug': 'detailed-reviews'
                }
            }
        }
    }
    
    # 記事タイプに基づくカテゴリーマッピング
    ARTICLE_TYPE_CATEGORY_MAP = {
        'tutorial': ['チュートリアル'],
        'beginner_guide': ['チュートリアル', '初心者向け'],
        'advanced_technique': ['チュートリアル', '実践テクニック'],
        'prompt_guide': ['チュートリアル', 'プロンプト作成'],
        'tool_update': ['AI音楽ニュース', 'ツールアップデート'],
        'industry_news': ['AI音楽ニュース', '業界動向'],
        'user_showcase': ['作品紹介', 'ユーザー作品'],
        'featured_showcase': ['作品紹介', '注目作品'],
        'tool_comparison': ['比較・レビュー', 'ツール比較'],
        'tool_review': ['比較・レビュー', '詳細レビュー'],
        'suno_specific': ['AI音楽ツール', 'Suno'],
        'udio_specific': ['AI音楽ツール', 'Udio'],
        'musicgen_specific': ['AI音楽ツール', 'MusicGen'],
        'stable_audio_specific': ['AI音楽ツール', 'Stable Audio'],
        'aiva_specific': ['AI音楽ツール', 'AIVA'],
        # 新しい専門技術記事タイプ
        'voice_synthesis': ['チュートリアル', '実践テクニック'],
        'app_development': ['チュートリアル', '実践テクニック'],
        'music_analysis': ['チュートリアル', '実践テクニック'],
        'industry_analysis': ['AI音楽ニュース', '業界動向'],
        'technical_guide': ['チュートリアル', '実践テクニック']
    }
    
    # 推奨タグリスト
    RECOMMENDED_TAGS = {
        'suno': ['Suno', 'Suno AI', 'AI音楽生成', 'AI作曲', 'テキストto音楽'],
        'udio': ['Udio', 'AI音楽', '音楽生成AI', 'AIミュージック'],
        'musicgen': ['MusicGen', 'Meta', 'オープンソース', 'AI音楽生成'],
        'stable_audio': ['Stable Audio', 'Stability AI', 'AI音楽', '音楽生成'],
        'aiva': ['AIVA', 'AI作曲家', 'クラシック音楽', 'BGM制作'],
        'general': ['AI音楽', 'AI作曲', '音楽生成', 'AIツール', '音楽制作'],
        'tutorial': ['チュートリアル', '使い方', 'ガイド', 'How to'],
        'beginner': ['初心者', '入門', '基礎', 'はじめて'],
        'advanced': ['上級', 'テクニック', 'プロ', '応用'],
        'prompt': ['プロンプト', 'プロンプトエンジニアリング', 'テキスト指示'],
        'comparison': ['比較', 'レビュー', 'おすすめ', '選び方'],
        'news': ['ニュース', 'アップデート', '最新情報', '新機能'],
        # 新しい専門技術タグ
        'voice_synthesis': ['音声合成', 'AI音声', '音声技術', '音声クローン', 'TTS'],
        'app_development': ['アプリ開発', 'プログラミング', 'API', 'ウェブ開発', 'モバイルアプリ'],
        'music_analysis': ['音楽分析', 'データ解析', '機械学習', '音楽データ', '可視化'],
        'industry_analysis': ['業界分析', '市場動向', '著作権', 'ビジネス', 'トレンド'],
        'technical_guide': ['技術解説', 'AI技術', '機械学習', 'アルゴリズム', '実装']
    }
    
    def __init__(self, wp_client: WordPressClient):
        """
        カテゴリーマネージャーの初期化
        
        Args:
            wp_client: WordPressクライアントインスタンス
        """
        self.wp_client = wp_client
        self.category_cache = {}
        self.tag_cache = {}
        
    def setup_categories(self) -> Dict[str, int]:
        """
        カテゴリー構造をセットアップ
        
        Returns:
            カテゴリー名とIDのマッピング
        """
        logger.info("カテゴリー構造のセットアップを開始")
        category_ids = {}
        
        # 既存のカテゴリーを取得
        existing_categories = self.wp_client.get_categories()
        for cat in existing_categories:
            self.category_cache[cat['name']] = cat['id']
        
        # カテゴリー構造を作成
        for parent_name, parent_info in self.CATEGORY_STRUCTURE.items():
            # 親カテゴリーを作成
            parent_id = self._ensure_category_exists(
                parent_name, 
                parent_info['description'],
                parent_info['slug']
            )
            category_ids[parent_name] = parent_id
            
            # 子カテゴリーを作成
            if 'children' in parent_info:
                for child_name, child_info in parent_info['children'].items():
                    child_id = self._ensure_category_exists(
                        child_name,
                        child_info['description'],
                        child_info['slug'],
                        parent_id
                    )
                    category_ids[child_name] = child_id
        
        logger.info(f"カテゴリー構造のセットアップ完了: {len(category_ids)}個のカテゴリー")
        return category_ids
    
    def _ensure_category_exists(self, name: str, description: str = "", 
                               slug: str = None, parent: int = 0) -> int:
        """
        カテゴリーが存在することを確認し、なければ作成
        
        Args:
            name: カテゴリー名
            description: カテゴリーの説明
            slug: URLスラッグ
            parent: 親カテゴリーID
            
        Returns:
            カテゴリーID
        """
        # キャッシュから確認
        if name in self.category_cache:
            return self.category_cache[name]
        
        # WordPressから取得
        try:
            categories = self.wp_client.get_categories()
            for cat in categories:
                if cat['name'] == name:
                    self.category_cache[name] = cat['id']
                    return cat['id']
            
            # カテゴリーが存在しない場合は作成
            logger.info(f"新規カテゴリーを作成: {name}")
            new_cat = self.wp_client.create_category(name, description, slug, parent)
            self.category_cache[name] = new_cat['id']
            return new_cat['id']
            
        except Exception as e:
            logger.error(f"カテゴリー作成エラー ({name}): {str(e)}")
            return 1  # デフォルトカテゴリー
    
    def get_categories_for_article(self, article_type: str, 
                                  tool_name: Optional[str] = None) -> List[int]:
        """
        記事タイプに基づいて適切なカテゴリーを取得
        
        Args:
            article_type: 記事のタイプ
            tool_name: 対象のツール名（Suno, Udio等）
            
        Returns:
            カテゴリーIDのリスト
        """
        category_ids = []
        
        # 記事タイプに基づくカテゴリー
        if article_type in self.ARTICLE_TYPE_CATEGORY_MAP:
            category_names = self.ARTICLE_TYPE_CATEGORY_MAP[article_type]
            for cat_name in category_names:
                if cat_name in self.category_cache:
                    category_ids.append(self.category_cache[cat_name])
        
        # ツール固有のカテゴリー
        if tool_name:
            tool_category_key = f"{tool_name.lower()}_specific"
            if tool_category_key in self.ARTICLE_TYPE_CATEGORY_MAP:
                tool_categories = self.ARTICLE_TYPE_CATEGORY_MAP[tool_category_key]
                for cat_name in tool_categories:
                    if cat_name in self.category_cache:
                        cat_id = self.category_cache[cat_name]
                        if cat_id not in category_ids:
                            category_ids.append(cat_id)
        
        # デフォルトカテゴリーを追加
        if not category_ids and 'AI音楽ツール' in self.category_cache:
            category_ids.append(self.category_cache['AI音楽ツール'])
        
        return category_ids
    
    def get_tags_for_article(self, article_type: str, 
                           tool_name: Optional[str] = None,
                           custom_tags: List[str] = None) -> List[int]:
        """
        記事に適したタグを取得・作成
        
        Args:
            article_type: 記事のタイプ
            tool_name: 対象のツール名
            custom_tags: カスタムタグのリスト
            
        Returns:
            タグIDのリスト
        """
        tag_names = []
        
        # ツール固有のタグ
        if tool_name and tool_name.lower() in self.RECOMMENDED_TAGS:
            tag_names.extend(self.RECOMMENDED_TAGS[tool_name.lower()])
        
        # 記事タイプに基づくタグ
        if article_type:
            # tutorialタイプの場合
            if 'tutorial' in article_type or 'guide' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('tutorial', []))
            if 'beginner' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('beginner', []))
            if 'advanced' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('advanced', []))
            if 'prompt' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('prompt', []))
            if 'comparison' in article_type or 'review' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('comparison', []))
            if 'news' in article_type or 'update' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('news', []))
            # 技術系タグ
            if 'voice_synthesis' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('voice_synthesis', []))
            if 'singing_synthesis' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('singing_synthesis', []))
            if 'voice_conversion' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('voice_conversion', []))
            if 'source_separation' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('source_separation', []))
            if 'music_analysis' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('music_analysis', []))
            if 'programming' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('programming', []))
            if 'library' in article_type or 'api' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('library', []))
            if 'app_development' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('app_dev', []))
            if 'model_training' in article_type:
                tag_names.extend(self.RECOMMENDED_TAGS.get('ml_model', []))
        
        # 一般的なタグを追加
        tag_names.extend(self.RECOMMENDED_TAGS.get('general', []))
        
        # カスタムタグを追加
        if custom_tags:
            tag_names.extend(custom_tags)
        
        # 重複を削除
        tag_names = list(set(tag_names))
        
        # タグIDを取得または作成
        return self.wp_client.find_or_create_tags(tag_names[:15])  # 最大15個のタグ
    
    def analyze_content_for_categories(self, title: str, content: str) -> Tuple[str, Optional[str]]:
        """
        コンテンツを分析して適切な記事タイプとツール名を判定
        
        Args:
            title: 記事タイトル
            content: 記事本文
            
        Returns:
            (記事タイプ, ツール名)のタプル
        """
        title_lower = title.lower()
        content_lower = content.lower()
        
        # ツール名の検出
        tool_name = None
        tool_checks = {
            'Suno': ['suno', 'スーノ'],
            'Udio': ['udio', 'ウディオ'],
            'MusicGen': ['musicgen', 'ミュージックジェン'],
            'Stable Audio': ['stable audio', 'ステーブルオーディオ'],
            'AIVA': ['aiva', 'アイヴァ']
        }
        
        # 音声技術キーワードの検出
        voice_tech_checks = {
            'voice_synthesis': ['音声合成', 'tts', 'text-to-speech', 'テキスト読み上げ', '音声クローン'],
            'singing_synthesis': ['歌声合成', 'aiシンガー', 'ボーカロイド', 'vocaloid', 'synthesizer v'],
            'voice_conversion': ['音声変換', 'voice conversion', 'ボイスチェンジャー', '声質変換'],
            'source_separation': ['音源分離', 'ボーカル抽出', 'カラオケ', 'ステムズ', 'stems']
        }
        
        # 開発関連キーワードの検出
        dev_checks = {
            'programming': ['python', 'javascript', 'プログラミング', 'コード', '実装'],
            'library_api': ['ライブラリ', 'api', 'sdk', 'フレームワーク'],
            'app_development': ['アプリ開発', 'web開発', 'モバイルアプリ', '開発事例'],
            'model_training': ['機械学習', 'ディープラーニング', 'モデル学習', 'ファインチューニング']
        }
        
        for tool, keywords in tool_checks.items():
            for keyword in keywords:
                if keyword in title_lower or keyword in content_lower[:1000]:
                    tool_name = tool
                    break
            if tool_name:
                break
        
        # 記事タイプの検出
        article_type = 'general'
        
        # まず音声技術関連をチェック
        for tech_type, keywords in voice_tech_checks.items():
            for keyword in keywords:
                if keyword in title_lower or keyword in content_lower[:1000]:
                    article_type = tech_type
                    break
            if article_type != 'general':
                break
        
        # 開発関連をチェック
        if article_type == 'general':
            for dev_type, keywords in dev_checks.items():
                for keyword in keywords:
                    if keyword in title_lower or keyword in content_lower[:1000]:
                        article_type = dev_type
                        break
                if article_type != 'general':
                    break
        
        # 一般的な記事タイプをチェック
        if article_type == 'general':
            if any(word in title_lower for word in ['チュートリアル', 'ガイド', '使い方', 'how to']):
                if any(word in title_lower for word in ['初心者', '入門', '基礎', 'はじめて']):
                    article_type = 'beginner_guide'
                elif any(word in title_lower for word in ['上級', 'プロ', 'テクニック', '応用']):
                    article_type = 'advanced_technique'
                else:
                    article_type = 'tutorial'
            elif any(word in title_lower for word in ['プロンプト', 'prompt']):
                article_type = 'prompt_guide'
            elif any(word in title_lower for word in ['比較', '選び方', 'vs', '対']):
                article_type = 'tool_comparison'
            elif any(word in title_lower for word in ['レビュー', '評価', '感想']):
                article_type = 'tool_review'
            elif any(word in title_lower for word in ['アップデート', '新機能', 'update']):
                article_type = 'tool_update'
            elif any(word in title_lower for word in ['ニュース', 'news', '発表']):
                article_type = 'industry_news'
            elif any(word in title_lower for word in ['作品', '制作', 'showcase']):
                article_type = 'user_showcase'
            elif tool_name:
                article_type = f"{tool_name.lower()}_specific"
        
        return article_type, tool_name