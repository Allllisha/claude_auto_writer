"""
Content Builder - 記事生成パイプライン
AI Melody Kobo - 記事コンテンツの構築と生成を管理
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path

from .ai_client import AIClientFactory, AIClientInterface
from .persona import AlisaPersona
from ..wordpress.converter import ArticleConverter
from ..wordpress.category_manager import CategoryManager
from ..data_sources.suno_scraper import SunoInfoCollector
from ..data_sources.ai_music_collector import AIMusicInfoCollector
from ..seo.keyword_strategy import SEOKeywordStrategy
from ..seo.content_optimizer import SEOContentOptimizer

logger = logging.getLogger(__name__)


class ArticleGenerator:
    """記事生成パイプライン全体を管理するクラス"""
    
    def __init__(self, 
                 ai_client_type: str = "claude",
                 persona_data_path: Optional[str] = None,
                 category_manager: Optional[CategoryManager] = None,
                 enable_seo_optimization: bool = True):
        """
        記事生成器の初期化
        
        Args:
            ai_client_type: 使用するAIクライアントのタイプ
            persona_data_path: ペルソナデータのパス
            category_manager: カテゴリーマネージャーインスタンス
            enable_seo_optimization: SEO最適化を有効にするか
        """
        self.ai_client = AIClientFactory.create_client(ai_client_type)
        self.persona = AlisaPersona(persona_data_path)
        self.converter = ArticleConverter()
        self.category_manager = category_manager
        self.suno_collector = SunoInfoCollector()
        self.ai_music_collector = AIMusicInfoCollector()
        
        # SEO最適化システム
        self.enable_seo = enable_seo_optimization
        if self.enable_seo:
            self.seo_keyword_strategy = SEOKeywordStrategy()
            self.seo_content_optimizer = SEOContentOptimizer()
        
        # 生成履歴の保存先
        self.history_dir = Path("data/generation_history")
        self.history_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_article(self,
                        topic: str,
                        article_type: str = "news",
                        keywords: Optional[List[str]] = None,
                        use_latest_info: bool = True,
                        custom_context: Optional[str] = None,
                        tool_name: Optional[str] = None) -> Dict[str, Any]:
        """
        記事を生成するメインメソッド
        
        Args:
            topic: 記事のトピック
            article_type: 記事タイプ（news, howto, column）
            keywords: SEOキーワードのリスト
            use_latest_info: 最新のSuno情報を収集するか
            custom_context: カスタムコンテキスト
            
        Returns:
            生成された記事データ
        """
        logger.info(f"記事生成開始: {topic}")
        
        # 現在の年を動的に取得
        current_year = datetime.now().year
        
        # SEO最適化キーワードの生成
        if self.enable_seo:
            seo_keywords = self.seo_keyword_strategy.generate_seo_optimized_keywords(
                article_type=article_type,
                tool_name=tool_name,
                target_difficulty="medium"
            )
            
            # SEO最適化されたタイトルを生成
            seo_titles = self.seo_keyword_strategy.generate_seo_title_variations(
                topic, seo_keywords, max_length=60
            )
            if seo_titles:
                topic = seo_titles[0]  # 最適化されたタイトルを使用
            
            # キーワードリストを拡張
            if not keywords:
                keywords = []
            keywords.extend(seo_keywords.get('primary', []))
            keywords.extend(seo_keywords.get('semantic', [])[:3])
            keywords.extend(seo_keywords.get('seasonal', []))
            
            # SEO最適化された記事構造を取得
            article_structure = self.seo_content_optimizer.optimize_article_structure(
                article_type, topic, seo_keywords
            )
            
            # SEO最適化されたプロンプトを生成
            seo_prompts = self.seo_content_optimizer.generate_optimized_prompts(
                article_structure, seo_keywords, article_type
            )
            
            # カスタムコンテキストにSEOガイダンスを追加
            if not custom_context:
                custom_context = ""
            custom_context += f"\n\n{seo_prompts['keyword_guidance']}"
            custom_context += f"\n\n{seo_prompts['quality_checklist']}"
            
        else:
            # 従来のキーワード設定
            if not keywords:
                keywords = ["AI音楽", "AI作曲", "AIメロディ工房", f"{current_year}年"]
            else:
                year_keywords = [f"{current_year}年", f"{current_year}年最新"]
                keywords.extend([k for k in year_keywords if k not in keywords])
        
        # 1. Suno関連情報の収集（オプション）
        additional_context = custom_context or ""
        if use_latest_info:
            try:
                latest_info = self.suno_collector.collect_latest_info()
                if latest_info:
                    additional_context += f"\n\n最新のSuno情報:\n{latest_info}"
                    logger.info("最新のSuno情報を収集しました")
            except Exception as e:
                logger.warning(f"Suno情報収集エラー: {str(e)}")
        
        # 2. ペルソナスタイルプロンプトの追加
        persona_prompt = self.persona.get_style_prompt()
        full_context = f"{persona_prompt}\n\n{additional_context}" if additional_context else persona_prompt
        
        # 3. AI記事生成
        try:
            ai_response = self.ai_client.generate_article(
                topic=topic,
                keywords=keywords,
                article_type=article_type,
                additional_context=full_context
            )
            
            markdown_content = ai_response.get('markdown_content', '')
            logger.info("AI記事生成完了")
            
        except Exception as e:
            logger.error(f"AI記事生成エラー: {str(e)}")
            raise
        
        # 4. ペルソナスタイルの適用
        styled_content = self.persona.apply_persona_style(markdown_content)
        
        # 4.5. SEO最適化
        if self.enable_seo and 'seo_keywords' in locals():
            styled_content = self.seo_keyword_strategy.optimize_content_structure(
                styled_content, seo_keywords
            )
            
            # SEO分析を実行
            seo_analysis = self.seo_content_optimizer.analyze_content_seo(
                styled_content, seo_keywords
            )
            logger.info(f"SEO分析結果: スコア {seo_analysis['seo_score']}/100")
            
            # メタディスクリプションを生成
            meta_description = self.seo_keyword_strategy.generate_meta_description(
                topic, seo_keywords
            )
        
        # 5. CTAブロックの処理
        styled_content = self._process_cta_blocks(styled_content)
        
        # 6. WordPress用に変換
        article_data = self.converter.convert_to_wordpress_html(styled_content)
        
        # 6.5. カテゴリーとタグの自動設定
        if self.category_manager:
            # コンテンツを分析してカテゴリーとツールを判定
            detected_type, detected_tool = self.category_manager.analyze_content_for_categories(
                article_data.get('title', topic),
                styled_content
            )
            
            # 明示的に指定されていない場合は検出結果を使用
            final_article_type = article_type if article_type != "news" else detected_type
            final_tool_name = tool_name or detected_tool
            
            # カテゴリーIDを取得
            category_ids = self.category_manager.get_categories_for_article(
                final_article_type,
                final_tool_name
            )
            article_data['categories'] = category_ids
            
            # タグIDを取得（既存のタグに追加）
            existing_tags = article_data.get('tags', [])
            try:
                tag_ids = self.category_manager.get_tags_for_article(
                    final_article_type,
                    final_tool_name,
                    existing_tags
                )
                article_data['tags'] = tag_ids
            except Exception as e:
                logger.warning(f"タグ取得エラー（スキップします）: {str(e)}")
                tag_ids = []
                article_data['tags'] = []
            
            logger.info(f"カテゴリー設定: {category_ids}, タグ設定: {len(tag_ids)}個")
        
        # 7. 生成履歴の保存
        generation_data = {
            'topic': topic,
            'article_type': article_type,
            'keywords': keywords,
            'generated_at': datetime.now().isoformat(),
            'ai_model': ai_response.get('model', 'unknown'),
            'title': article_data.get('title', ''),
            'markdown_content': styled_content,
            'html_content': article_data.get('content', ''),
            'tags': article_data.get('tags', []),
            'categories': article_data.get('categories', []),
            'meta_description': article_data.get('meta_description', ''),
            'tool_name': tool_name,
            'detected_article_type': final_article_type if self.category_manager else article_type,
            'seo_optimization': {
                'enabled': self.enable_seo,
                'keywords': seo_keywords if self.enable_seo and 'seo_keywords' in locals() else None,
                'analysis': seo_analysis if self.enable_seo and 'seo_analysis' in locals() else None
            }
        }
        
        self._save_generation_history(generation_data)
        
        # 8. ペルソナ学習用にサンプルを追加
        self.persona.add_writing_sample(
            styled_content[:1000],  # 最初の1000文字
            metadata={
                'topic': topic,
                'article_type': article_type,
                'generated_at': generation_data['generated_at']
            }
        )
        
        return {
            'success': True,
            'article_data': article_data,
            'generation_metadata': generation_data
        }
    
    def _process_cta_blocks(self, content: str) -> str:
        """CTAブロックを適切に処理（しつこすぎる場合は調整）"""
        cta_template = self.persona.get_cta_template()
        
        # 既存のCTAブロックをすべて除去
        content = self._remove_existing_ctas(content)
        
        # 中盤と最後の2回だけ挿入
        lines = content.split('\n')
        h2_sections = []
        
        # H2セクションの位置を特定
        for i, line in enumerate(lines):
            if line.startswith('## ') and not line.startswith('### '):
                h2_sections.append(i)
        
        # 中盤のH2セクション後にCTA挿入（H2が4個以上ある場合のみ）
        if len(h2_sections) >= 4:
            mid_section = h2_sections[len(h2_sections) // 2]  # 中間のH2セクション
            # そのH2セクションの内容の後ろを探す
            insert_pos = mid_section + 1
            while insert_pos < len(lines) and not lines[insert_pos].startswith('## '):
                insert_pos += 1
            lines.insert(insert_pos, '\n' + cta_template + '\n')
        
        # 最後にCTA挿入
        content_with_cta = '\n'.join(lines)
        if not content_with_cta.strip().endswith('---'):
            content_with_cta += '\n\n' + cta_template
        
        return content_with_cta
    
    def _remove_existing_ctas(self, content: str) -> str:
        """既存のCTAブロックを除去"""
        import re
        
        # CTAブロックのパターンを除去
        patterns = [
            r'---\s*\n.*?メルマガ.*?\n.*?---',  # ---で囲まれたメルマガCTA
            r'###\s*.*?メルマガ.*?\n.*?➡️.*?\n',  # ### メルマガ見出しとリンク
            r'🎵.*?メルマガ.*?\n.*?登録.*?\n.*?➡️.*?\n',  # 絵文字付きメルマガCTA
            r'\*\*.*?メルマガ.*?\*\*.*?\n.*?➡️.*?\n'  # **太字**メルマガCTA
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 連続する改行を整理
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()
    
    def _save_generation_history(self, generation_data: Dict[str, Any]):
        """生成履歴を保存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"article_{timestamp}.json"
        filepath = self.history_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(generation_data, f, ensure_ascii=False, indent=2)
            logger.info(f"生成履歴を保存: {filepath}")
        except Exception as e:
            logger.error(f"履歴保存エラー: {str(e)}")
    
    def generate_weekly_news(self, 
                           news_items: List[Dict[str, str]]) -> Dict[str, Any]:
        """週刊ニュース記事を生成"""
        # ニュースアイテムをコンテキストとして整形
        news_context = "今週のSunoニュース:\n"
        for item in news_items:
            news_context += f"- {item.get('title', '')}: {item.get('summary', '')}\n"
        
        return self.generate_article(
            topic="今週のSuno最新ニュース＆アップデート情報",
            article_type="tool_update",
            keywords=["Suno", "最新情報", "アップデート", "新機能"],
            custom_context=news_context,
            tool_name="Suno"
        )
    
    def generate_howto_article(self,
                             feature_name: str,
                             steps: Optional[List[str]] = None) -> Dict[str, Any]:
        """ハウツー記事を生成"""
        context = ""
        if steps:
            context = "手順:\n" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
        
        return self.generate_article(
            topic=f"Sunoの{feature_name}を完全マスター！初心者向けステップバイステップガイド",
            article_type="beginner_guide",
            keywords=["Suno", feature_name, "使い方", "初心者"],
            custom_context=context,
            tool_name="Suno"
        )
    
    def generate_column_article(self,
                              theme: str,
                              perspective: Optional[str] = None) -> Dict[str, Any]:
        """コラム記事を生成"""
        context = f"視点: {perspective}" if perspective else ""
        
        return self.generate_article(
            topic=theme,
            article_type="industry_news",
            keywords=["Suno", "AI作曲", "音楽制作", "未来"],
            custom_context=context,
            tool_name="Suno"
        )
    
    def batch_generate_articles(self,
                              article_specs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """複数の記事を一括生成"""
        results = []
        
        for spec in article_specs:
            try:
                result = self.generate_article(**spec)
                results.append(result)
                logger.info(f"記事生成成功: {spec.get('topic', 'Unknown')}")
            except Exception as e:
                logger.error(f"記事生成失敗: {spec.get('topic', 'Unknown')} - {str(e)}")
                results.append({
                    'success': False,
                    'error': str(e),
                    'spec': spec
                })
        
        return results