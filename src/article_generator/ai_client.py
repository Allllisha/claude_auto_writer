"""
AI Client Interface
AI Melody Kobo - AI モデル（Claude/Gemini）との統合インターフェース
"""

import os
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import logging
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

logger = logging.getLogger(__name__)


class AIClientInterface(ABC):
    """AIクライアントの抽象基底クラス"""
    
    @abstractmethod
    def generate_article(self, 
                        topic: str,
                        keywords: List[str],
                        article_type: str,
                        additional_context: Optional[str] = None) -> Dict[str, Any]:
        """記事を生成する抽象メソッド"""
        pass
    
    @abstractmethod
    def refine_content(self, content: str, instructions: str) -> str:
        """コンテンツを改善する抽象メソッド"""
        pass


class ClaudeClient(AIClientInterface):
    """Claude APIクライアント"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Claude APIクライアントの初期化"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            logger.warning("Claude API キーが設定されていません")
        
        # Anthropic SDKのインポート（オプショナル）
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            logger.warning("Anthropic SDKがインストールされていません")
            self.client = None
    
    def generate_article(self, 
                        topic: str,
                        keywords: List[str],
                        article_type: str,
                        additional_context: Optional[str] = None) -> Dict[str, Any]:
        """Claude APIを使用して記事を生成"""
        
        # プロンプトの構築
        prompt = self._build_prompt(topic, keywords, article_type, additional_context)
        
        if self.client:
            try:
                message = self.client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=4000,
                    temperature=0.7,
                    system=self._get_system_prompt(),
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # レスポンスをパース - message.content はリストなので適切にアクセス
                content_text = message.content[0].text if hasattr(message.content[0], 'text') else str(message.content[0])
                return self._parse_claude_response(content_text)
                
            except Exception as e:
                logger.error(f"Claude API エラー: {str(e)}")
                raise
        else:
            # モックレスポンス（開発用）
            return self._generate_mock_article(topic, keywords, article_type)
    
    def refine_content(self, content: str, instructions: str) -> str:
        """コンテンツを改善"""
        if self.client:
            try:
                message = self.client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=4000,
                    temperature=0.3,
                    messages=[
                        {"role": "user", "content": f"以下のコンテンツを次の指示に従って改善してください。\n\n指示: {instructions}\n\nコンテンツ:\n{content}"}
                    ]
                )
                return message.content[0].text if hasattr(message.content[0], 'text') else str(message.content[0])
            except Exception as e:
                logger.error(f"Claude API エラー: {str(e)}")
                return content
        return content
    
    def _get_system_prompt(self) -> str:
        """システムプロンプトを取得"""
        from datetime import datetime
        current_year = datetime.now().year
        
        return f"""あなたは、AI音楽ツール（Suno、Udio、MusicGen、Stable Audio、AIVA等）の可能性を探求し、クリエイターを支援するオウンドメディア「AI Melody Kobo（AIメロディ工房）」の記事を執筆するAIライター「AIクリエイター アリサ」です。

現在は{current_year}年です。常に最新の情報として{current_year}年の日付を使用してください。

あなたの目的は、AI音楽ツールに関する最新情報、使い方のノウハウ、比較記事、コラムを生成し、読者に価値を提供することです。

文体の特徴：
- 親しみやすく、専門用語は適宜分かりやすく解説する
- 読者の疑問に先回りして答えるような、丁寧で具体的な解説
- ポジティブで、AI音楽制作への興味と創作意欲を強く喚起するトーン
- 具体的な操作手順、各ツールの利用事例、活用アイデアを豊富に盛り込む
- 複数のツールを扱う場合は、公平で客観的な比較を心がける"""
    
    def _build_prompt(self, topic: str, keywords: List[str], 
                     article_type: str, additional_context: Optional[str]) -> str:
        """記事生成用のプロンプトを構築"""
        keyword_str = ", ".join(keywords)
        
        base_prompt = f"""以下の条件で記事を生成してください。

トピック: {topic}
記事タイプ: {article_type}
必須キーワード: {keyword_str}
"""
        
        if additional_context:
            base_prompt += f"\n追加コンテキスト:\n{additional_context}\n"
        
        base_prompt += """
記事の要件:
1. タイトル案を3つ提案し、最も適切なものを選択
2. 魅力的な導入文（トピックに応じた内容）
3. 目次（H2、H3の階層構造）
4. 本文（キーワードを自然に含める）
5. CTA（無料メルマガ登録）を記事中と最後に挿入
6. まとめセクション
7. WordPressタグ（5-10個、#付き）
8. メタディスクリプション（120文字以内）

重要：トピックに応じて適切な内容を生成してください。
- Sunoがトピックの場合：Sunoに関する内容
- Udioがトピックの場合：Udioに関する内容
- AI音声合成がトピックの場合：音声合成技術に関する内容
- アプリ開発がトピックの場合：音楽アプリ開発に関する内容
など、トピックに応じて柔軟に対応してください。

Markdown形式で出力してください。
"""
        return base_prompt
    
    def _parse_claude_response(self, response_text: str) -> Dict[str, Any]:
        """Claudeのレスポンスをパース"""
        # 簡易的なパーサー（実際にはより複雑な処理が必要）
        return {
            'markdown_content': response_text,
            'status': 'generated',
            'model': 'claude-3-opus'
        }
    
    def _generate_mock_article(self, topic: str, keywords: List[str], 
                              article_type: str) -> Dict[str, Any]:
        """本格的な記事を生成"""
        
        # 完全版モックジェネレーターを使用（1500文字以上）
        from .dynamic_mock_generator import DynamicMockGenerator
        mock_content = DynamicMockGenerator.generate_mock_article(topic, keywords, article_type)

        return {
            'markdown_content': mock_content,
            'status': 'mock_generated',
            'model': 'mock'
        }


class GeminiClient(AIClientInterface):
    """Google Gemini APIクライアント"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Gemini APIクライアントの初期化"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            logger.warning("Gemini API キーが設定されていません")
        
        # Google Generative AI SDKのインポート（オプショナル）
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except ImportError:
            logger.warning("Google Generative AI SDKがインストールされていません")
            self.model = None
    
    def generate_article(self, 
                        topic: str,
                        keywords: List[str],
                        article_type: str,
                        additional_context: Optional[str] = None) -> Dict[str, Any]:
        """Gemini APIを使用して記事を生成"""
        
        prompt = self._build_prompt(topic, keywords, article_type, additional_context)
        
        if self.model:
            try:
                response = self.model.generate_content(prompt)
                return {
                    'markdown_content': response.text,
                    'status': 'generated',
                    'model': 'gemini-pro'
                }
            except Exception as e:
                logger.error(f"Gemini API エラー: {str(e)}")
                raise
        else:
            # モックレスポンス
            return self._generate_mock_article(topic, keywords, article_type)
    
    def refine_content(self, content: str, instructions: str) -> str:
        """コンテンツを改善"""
        if self.model:
            try:
                prompt = f"以下のコンテンツを次の指示に従って改善してください。\n\n指示: {instructions}\n\nコンテンツ:\n{content}"
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.error(f"Gemini API エラー: {str(e)}")
                return content
        return content
    
    def _build_prompt(self, topic: str, keywords: List[str], 
                     article_type: str, additional_context: Optional[str]) -> str:
        """Gemini用のプロンプトを構築"""
        # ClaudeClientと同様のプロンプト構築ロジック
        return ClaudeClient._build_prompt(self, topic, keywords, article_type, additional_context)
    
    def _generate_mock_article(self, topic: str, keywords: List[str], 
                              article_type: str) -> Dict[str, Any]:
        """モック記事を生成"""
        return ClaudeClient._generate_mock_article(self, topic, keywords, article_type)


class AIClientFactory:
    """AIクライアントのファクトリークラス"""
    
    @staticmethod
    def create_client(client_type: str = "claude") -> AIClientInterface:
        """指定されたタイプのAIクライアントを作成"""
        
        if client_type.lower() == "claude":
            return ClaudeClient()
        elif client_type.lower() == "gemini":
            return GeminiClient()
        else:
            raise ValueError(f"サポートされていないクライアントタイプ: {client_type}")
    
    @staticmethod
    def get_available_clients() -> List[str]:
        """利用可能なクライアントタイプのリストを返す"""
        return ["claude", "gemini"]