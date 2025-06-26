"""
AI Creator Alisa Persona Manager
AI Melody Kobo - AIクリエイター アリサのペルソナ管理
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class AlisaPersona:
    """AIクリエイター アリサのペルソナを管理するクラス"""
    
    def __init__(self, persona_data_path: Optional[str] = None):
        """
        ペルソナマネージャーの初期化
        
        Args:
            persona_data_path: ペルソナデータファイルのパス
        """
        self.persona_data_path = persona_data_path or "data/alisa_persona.json"
        self.writing_samples = []
        self.style_guidelines = self._load_default_guidelines()
        self.vocabulary_preferences = self._load_default_vocabulary()
        
        # 既存のペルソナデータを読み込み
        self._load_persona_data()
    
    def _load_default_guidelines(self) -> Dict[str, str]:
        """デフォルトの文体ガイドラインを定義"""
        return {
            "tone": "親しみやすく、専門用語は適宜分かりやすく解説する",
            "approach": "読者の疑問に先回りして答えるような、丁寧で具体的な解説",
            "emotion": "ポジティブで、Sunoを使った作曲への興味と創作意欲を強く喚起するトーン",
            "content_style": "具体的な操作手順、Sunoの利用事例、活用アイデアを豊富に盛り込む",
            "formatting": "箇条書き、太字、引用ブロックなどを効果的に使用し、読みやすさと視覚的な魅力を高める",
            "interaction": "読者に語りかけるようなインタラクティブな表現も適宜用いる"
        }
    
    def _load_default_vocabulary(self) -> Dict[str, List[str]]:
        """デフォルトの語彙・表現パターンを定義"""
        return {
            "greetings": [
                "こんにちは！AIクリエイター アリサです。",
                "音楽制作の新しい扉を開く時が来ました。",
                "Sunoと一緒に、素晴らしい音楽の旅に出かけましょう！"
            ],
            "encouragements": [
                "大丈夫、きっとできます！",
                "一緒に挑戦してみましょう。",
                "Sunoがあなたの創造性を解放します。",
                "音楽制作の楽しさを体験してください。"
            ],
            "transitions": [
                "それでは、",
                "次に、",
                "ここで重要なのは、",
                "実は、",
                "さらに興味深いことに、"
            ],
            "emphasis_patterns": [
                "**{}**",  # 太字強調
                "「{}」",  # 鍵括弧強調
                "✨ {} ✨",  # 装飾的強調
            ],
            "suno_specific": [
                "Sunoの魔法",
                "AI作曲の新時代",
                "音楽創作の民主化",
                "クリエイティブな可能性",
                "プロンプトの力",
                "AIメロディ工房"
            ]
        }
    
    def _load_persona_data(self):
        """保存されたペルソナデータを読み込み"""
        if os.path.exists(self.persona_data_path):
            try:
                with open(self.persona_data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.writing_samples = data.get('writing_samples', [])
                    self.style_guidelines.update(data.get('style_guidelines', {}))
                    self.vocabulary_preferences.update(data.get('vocabulary_preferences', {}))
                logger.info("ペルソナデータを読み込みました")
            except Exception as e:
                logger.error(f"ペルソナデータの読み込みエラー: {str(e)}")
    
    def save_persona_data(self):
        """ペルソナデータを保存"""
        try:
            # ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(self.persona_data_path), exist_ok=True)
            
            data = {
                'writing_samples': self.writing_samples,
                'style_guidelines': self.style_guidelines,
                'vocabulary_preferences': self.vocabulary_preferences
            }
            
            with open(self.persona_data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info("ペルソナデータを保存しました")
        except Exception as e:
            logger.error(f"ペルソナデータの保存エラー: {str(e)}")
    
    def add_writing_sample(self, sample_text: str, metadata: Optional[Dict] = None):
        """執筆サンプルを追加"""
        sample = {
            'text': sample_text,
            'metadata': metadata or {}
        }
        self.writing_samples.append(sample)
        self.save_persona_data()
    
    def get_style_prompt(self) -> str:
        """AIモデル用のスタイルプロンプトを生成"""
        prompt_parts = [
            "あなたは「AIクリエイター アリサ」として記事を執筆してください。",
            "",
            "文体の特徴："
        ]
        
        for key, value in self.style_guidelines.items():
            prompt_parts.append(f"- {value}")
        
        prompt_parts.extend([
            "",
            "よく使う表現パターン："
        ])
        
        # 挨拶表現
        if self.vocabulary_preferences.get('greetings'):
            prompt_parts.append(f"挨拶: {', '.join(self.vocabulary_preferences['greetings'][:3])}")
        
        # 励まし表現
        if self.vocabulary_preferences.get('encouragements'):
            prompt_parts.append(f"励まし: {', '.join(self.vocabulary_preferences['encouragements'][:3])}")
        
        # Suno特有の表現
        if self.vocabulary_preferences.get('suno_specific'):
            prompt_parts.append(f"Suno関連: {', '.join(self.vocabulary_preferences['suno_specific'][:3])}")
        
        # 執筆サンプルがある場合は追加
        if self.writing_samples:
            prompt_parts.extend([
                "",
                "過去の執筆例を参考にしてください："
            ])
            # 最新の3つのサンプルを使用
            for sample in self.writing_samples[-3:]:
                excerpt = sample['text'][:200] + "..." if len(sample['text']) > 200 else sample['text']
                prompt_parts.append(f"- {excerpt}")
        
        return "\n".join(prompt_parts)
    
    def apply_persona_style(self, text: str) -> str:
        """テキストにアリサのペルソナスタイルを適用"""
        styled_text = text
        
        # 個人的な体験談を追加する例
        if "Sunoを使って" in text and "私も" not in text:
            personal_experiences = [
                "実は私も最初は半信半疑でした。",
                "私も実際に試してみて驚きました。",
                "私の経験では、"
            ]
            # ランダムに選択して挿入（実際の実装では適切な位置に）
            # ここでは簡略化
        
        # 読者への語りかけを追加
        if "できます。" in styled_text:
            styled_text = styled_text.replace(
                "できます。",
                "できます。きっとあなたにも素晴らしい音楽が作れるはずです。"
            )
        
        return styled_text
    
    def get_cta_template(self) -> str:
        """CTA（Call to Action）のテンプレートを取得"""
        return """---
<div style="text-align: center; padding: 20px 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; margin: 25px auto; max-width: 600px; box-shadow: 0 8px 25px rgba(0,0,0,0.15);">

<h3 style="color: white; margin: 0 0 12px 0; font-size: 22px; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
✨ AI Melody Kobo 無料メルマガ ✨
</h3>

<p style="color: white; font-size: 15px; margin-bottom: 10px; line-height: 1.5; font-weight: 500;">
AI音楽の最新情報とテクニックを配信中！
</p>

<p style="color: #ffeb3b; font-size: 16px; margin-bottom: 20px; font-weight: bold; text-shadow: 0 1px 3px rgba(0,0,0,0.3);">
🎁 登録特典：AI音楽プロンプト100選を無料配布
</p>

<div style="display: inline-block;">
<a href="#newsletter-signup" 
   onmouseover="this.style.background='linear-gradient(45deg, #ff5252, #ff1744)'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 5px 20px rgba(238,90,111,0.4)';" 
   onmouseout="this.style.background='linear-gradient(45deg, #ff6b6b, #ee5a6f)'; this.style.transform='translateY(0)'; this.style.boxShadow='0 3px 15px rgba(238,90,111,0.3)';" 
   style="display: block; background: linear-gradient(45deg, #ff6b6b, #ee5a6f); color: white; padding: 13px 45px 12px 45px; text-decoration: none; border-radius: 30px; font-weight: bold; font-size: 16px; box-shadow: 0 3px 15px rgba(238,90,111,0.3); transition: all 0.3s ease; text-shadow: 0 1px 2px rgba(0,0,0,0.2); line-height: 1; position: relative;">
🚀 無料登録
</a>
</div>

</div>
---"""
    
    def get_article_structure_template(self) -> Dict[str, str]:
        """記事構造のテンプレートを取得"""
        return {
            "introduction": "読者の共感を呼び、Sunoの魅力を伝える導入",
            "toc": "論理的で分かりやすい目次構成（H2、H3）",
            "main_content": "具体例とステップバイステップガイド",
            "cta_mid": "記事中盤でのCTA挿入",
            "conclusion": "ポジティブで行動を促すまとめ",
            "cta_end": "記事末尾でのCTA挿入",
            "tags": "Suno関連のWordPressタグ",
            "meta": "SEO最適化されたメタディスクリプション"
        }
    
    def analyze_writing_style(self, text: str) -> Dict[str, any]:
        """テキストの文体を分析"""
        analysis = {
            "sentence_count": len(text.split('。')),
            "exclamation_count": text.count('！'),
            "question_count": text.count('？'),
            "emoji_count": sum(1 for char in text if ord(char) > 0x1F300),
            "suno_mentions": text.lower().count('suno'),
            "personal_pronouns": sum(text.count(pronoun) for pronoun in ['私', 'あなた', '皆さん']),
            "encouragement_phrases": sum(1 for phrase in self.vocabulary_preferences['encouragements'] if phrase in text)
        }
        
        return analysis