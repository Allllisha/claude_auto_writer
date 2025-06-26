"""
SEO Keyword Strategy System
AI Melody Kobo - SEO最適化キーワード戦略システム
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import random
import re

logger = logging.getLogger(__name__)


class SEOKeywordStrategy:
    """SEO戦略に基づくキーワード管理システム"""
    
    def __init__(self, strategy_file: str = None):
        """
        初期化
        
        Args:
            strategy_file: SEO戦略データファイルのパス
        """
        self.strategy_file = Path(strategy_file or "data/seo_strategy.json")
        self.strategy_file.parent.mkdir(parents=True, exist_ok=True)
        
        # SEO戦略データ
        self.seo_data = self._load_strategy_data()
        
        # 月別検索トレンド（仮想データ）
        self.seasonal_trends = self._get_seasonal_trends()
    
    def _load_strategy_data(self) -> Dict:
        """SEO戦略データを読み込み"""
        if self.strategy_file.exists():
            try:
                with open(self.strategy_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"SEO戦略データ読み込みエラー: {e}")
        
        # デフォルトのSEO戦略データ
        return {
            "primary_keywords": {
                # 高検索ボリューム・低競合を狙う
                "suno": {
                    "main": ["Suno", "Suno AI", "スーノ"],
                    "search_volume": 50000,
                    "competition": "medium",
                    "variations": [
                        "Suno 使い方", "Suno AI 音楽生成", "Suno とは",
                        "Suno 料金", "Suno 商用利用", "Suno プロンプト",
                        "Suno 無料", "Suno ダウンロード", "Suno 日本語"
                    ]
                },
                "ai_music": {
                    "main": ["AI音楽", "AI作曲", "AIミュージック"],
                    "search_volume": 30000,
                    "competition": "high",
                    "variations": [
                        "AI音楽 作り方", "AI作曲 無料", "AI音楽生成",
                        "AI音楽 ツール", "AI作曲 アプリ", "AI音楽 著作権"
                    ]
                },
                "voice_synthesis": {
                    "main": ["AI音声合成", "音声合成", "TTS"],
                    "search_volume": 20000,
                    "competition": "medium",
                    "variations": [
                        "AI音声合成 無料", "音声合成 ソフト", "TTS エンジン",
                        "音声クローン", "AI声優", "テキスト読み上げ"
                    ]
                }
            },
            
            "long_tail_keywords": {
                # ロングテールで確実にランクインを狙う
                "tutorial": [
                    "Suno AI 使い方 初心者",
                    "AI音楽 作り方 無料 アプリ",
                    "音声合成 Python 実装方法",
                    "AI作曲 プロンプト 書き方",
                    "Suno プロ版 料金 比較"
                ],
                "comparison": [
                    "Suno vs Udio 比較",
                    "AI音楽ツール おすすめ 2024",
                    "音声合成ソフト 比較 無料",
                    "AI作曲アプリ ランキング",
                    "MusicGen Suno 違い"
                ],
                "technical": [
                    "AI音楽 API 開発",
                    "音声合成 モデル 学習",
                    "Suno API 使い方",
                    "AI音楽 著作権 商用利用",
                    "音声クローン 技術 解説"
                ]
            },
            
            "semantic_keywords": {
                # 関連語・共起語で文脈を強化
                "music_production": [
                    "音楽制作", "楽曲制作", "作曲", "編曲", "ミックス",
                    "マスタリング", "DAW", "プロデューサー", "ビート制作"
                ],
                "ai_technology": [
                    "人工知能", "機械学習", "ディープラーニング", "ニューラルネットワーク",
                    "生成AI", "ChatGPT", "大規模言語モデル", "Transformer"
                ],
                "audio_tech": [
                    "オーディオ", "サウンド", "音響", "デジタル音楽", "ストリーミング",
                    "音質", "サンプリング", "シンセサイザー", "エフェクト"
                ]
            },
            
            "intent_based_keywords": {
                # 検索意図別キーワード
                "informational": [
                    "とは", "仕組み", "原理", "歴史", "特徴", "メリット", "デメリット"
                ],
                "navigational": [
                    "公式サイト", "ダウンロード", "ログイン", "アカウント作成"
                ],
                "transactional": [
                    "無料", "有料", "料金", "価格", "購入", "契約", "プラン"
                ],
                "commercial": [
                    "比較", "おすすめ", "ランキング", "レビュー", "評価", "口コミ"
                ]
            }
        }
    
    def _get_seasonal_trends(self) -> Dict:
        """季節的検索トレンドを取得"""
        return {
            "1": {"boost": ["新年", "目標", "始める", "2024年"], "factor": 1.3},
            "2": {"boost": ["バレンタイン", "恋愛", "ラブソング"], "factor": 1.1},
            "3": {"boost": ["卒業", "新生活", "春"], "factor": 1.2},
            "4": {"boost": ["入学", "新年度", "フレッシュ"], "factor": 1.4},
            "5": {"boost": ["GW", "連休", "趣味"], "factor": 1.2},
            "6": {"boost": ["梅雨", "インドア", "音楽"], "factor": 1.0},
            "7": {"boost": ["夏休み", "夏", "フェス"], "factor": 1.3},
            "8": {"boost": ["お盆", "休暇", "制作"], "factor": 1.2},
            "9": {"boost": ["秋", "芸術", "文化"], "factor": 1.1},
            "10": {"boost": ["ハロウィン", "イベント"], "factor": 1.2},
            "11": {"boost": ["紅葉", "秋", "落ち着く"], "factor": 1.0},
            "12": {"boost": ["クリスマス", "年末", "まとめ"], "factor": 1.4}
        }
    
    def generate_seo_optimized_keywords(self, 
                                      article_type: str,
                                      tool_name: str = None,
                                      target_difficulty: str = "medium") -> Dict[str, List[str]]:
        """
        SEO最適化されたキーワードセットを生成
        
        Args:
            article_type: 記事タイプ
            tool_name: 対象ツール名
            target_difficulty: 難易度 (easy/medium/hard)
            
        Returns:
            キーワードセット
        """
        current_month = str(datetime.now().month)
        seasonal_boost = self.seasonal_trends.get(current_month, {"boost": [], "factor": 1.0})
        
        # プライマリキーワード選択
        primary_keywords = []
        if tool_name and tool_name.lower() in self.seo_data["primary_keywords"]:
            tool_data = self.seo_data["primary_keywords"][tool_name.lower()]
            primary_keywords.extend(tool_data["main"])
            # 検索ボリュームが高い関連キーワードを追加
            primary_keywords.extend(random.sample(tool_data["variations"], 3))
        
        # 記事タイプ別キーワード
        type_keywords = []
        if article_type in ["tutorial", "beginner_guide"]:
            type_keywords.extend(random.sample(self.seo_data["long_tail_keywords"]["tutorial"], 2))
        elif article_type in ["tool_comparison", "tool_review"]:
            type_keywords.extend(random.sample(self.seo_data["long_tail_keywords"]["comparison"], 2))
        elif article_type in ["programming", "app_development"]:
            type_keywords.extend(random.sample(self.seo_data["long_tail_keywords"]["technical"], 2))
        
        # セマンティックキーワード
        semantic_keywords = []
        semantic_keywords.extend(random.sample(self.seo_data["semantic_keywords"]["music_production"], 2))
        semantic_keywords.extend(random.sample(self.seo_data["semantic_keywords"]["ai_technology"], 2))
        
        # 検索意図キーワード
        intent_keywords = []
        if article_type in ["beginner_guide", "tutorial"]:
            intent_keywords.extend(random.sample(self.seo_data["intent_based_keywords"]["informational"], 2))
        elif article_type == "tool_comparison":
            intent_keywords.extend(random.sample(self.seo_data["intent_based_keywords"]["commercial"], 2))
        
        # 季節的キーワード
        seasonal_keywords = random.sample(seasonal_boost["boost"], min(2, len(seasonal_boost["boost"])))
        
        return {
            "primary": primary_keywords,
            "long_tail": type_keywords,
            "semantic": semantic_keywords,
            "intent": intent_keywords,
            "seasonal": seasonal_keywords,
            "search_volume_estimate": self._estimate_search_volume(primary_keywords),
            "competition_level": target_difficulty
        }
    
    def _estimate_search_volume(self, keywords: List[str]) -> int:
        """キーワードの検索ボリュームを推定"""
        total_volume = 0
        for keyword in keywords:
            for tool, data in self.seo_data["primary_keywords"].items():
                if keyword.lower() in [k.lower() for k in data["main"]]:
                    total_volume += data["search_volume"]
                    break
            else:
                # デフォルト値
                total_volume += 1000
        return total_volume
    
    def generate_seo_title_variations(self, 
                                    base_topic: str,
                                    keywords: Dict[str, List[str]],
                                    max_length: int = 60) -> List[str]:
        """
        SEO最適化されたタイトルのバリエーションを生成
        
        Args:
            base_topic: ベースとなるトピック
            keywords: キーワードセット
            max_length: 最大文字数
            
        Returns:
            タイトルのバリエーション
        """
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # タイトルテンプレート
        templates = [
            "【{year}年最新】{primary} {topic}",
            "{primary}で{topic}する方法【完全ガイド】",
            "【保存版】{primary} {topic} - {benefit}",
            "{primary} {topic}の始め方｜{month}月版",
            "【実践】{primary}を使った{topic}テクニック",
            "{primary} {topic}入門 - 初心者向け完全解説",
            "プロが教える{primary} {topic}の極意",
            "{comparison}？{primary} {topic}を徹底比較"
        ]
        
        variations = []
        
        for template in templates:
            try:
                title = template.format(
                    year=current_year,
                    month=current_month,
                    primary=random.choice(keywords.get("primary", ["AI音楽"])),
                    topic=base_topic,
                    benefit=random.choice(["初心者でも簡単", "プロ級のクオリティ", "無料で始められる"]),
                    comparison=random.choice(["どっちがいい", "何が違う", "比較検証"])
                )
                
                if len(title) <= max_length:
                    variations.append(title)
            except (KeyError, IndexError):
                continue
        
        return variations[:5]  # 上位5つを返す
    
    def optimize_content_structure(self, content: str, keywords: Dict[str, List[str]]) -> str:
        """
        コンテンツをSEO最適化
        
        Args:
            content: 元のコンテンツ
            keywords: キーワードセット
            
        Returns:
            最適化されたコンテンツ
        """
        # キーワード密度の最適化（自然な形で）
        optimized_content = content
        
        # プライマリキーワードを適切な位置に配置
        primary_keywords = keywords.get("primary", [])
        if primary_keywords:
            main_keyword = primary_keywords[0]
            
            # 見出しにキーワードを含める
            optimized_content = self._optimize_headings(optimized_content, main_keyword)
            
            # 導入部分でキーワードを言及
            optimized_content = self._optimize_introduction(optimized_content, main_keyword)
            
            # まとめ部分でキーワードを再度使用
            optimized_content = self._optimize_conclusion(optimized_content, main_keyword)
        
        # セマンティックキーワードを自然に配置
        semantic_keywords = keywords.get("semantic", [])
        optimized_content = self._add_semantic_keywords(optimized_content, semantic_keywords)
        
        return optimized_content
    
    def _optimize_headings(self, content: str, keyword: str) -> str:
        """見出しを最適化"""
        lines = content.split('\n')
        optimized_lines = []
        
        for line in lines:
            if line.startswith('## ') and keyword.lower() not in line.lower():
                # H2見出しの最初のものにキーワードを含める
                if len([l for l in optimized_lines if l.startswith('## ')]) == 0:
                    heading_text = line[3:].strip()
                    line = f"## {keyword}で{heading_text}"
            optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _optimize_introduction(self, content: str, keyword: str) -> str:
        """導入部分を最適化"""
        lines = content.split('\n')
        
        # 最初の段落にキーワードを含めるかチェック
        first_paragraph_end = 0
        for i, line in enumerate(lines):
            if line.strip() == '' and i > 5:  # 空行で段落区切り
                first_paragraph_end = i
                break
        
        first_paragraph = '\n'.join(lines[:first_paragraph_end])
        if keyword.lower() not in first_paragraph.lower():
            # 最初の文にキーワードを含める
            if lines and not lines[0].startswith('#'):
                lines[0] = f"{keyword}について詳しく解説します。" + lines[0]
        
        return '\n'.join(lines)
    
    def _optimize_conclusion(self, content: str, keyword: str) -> str:
        """まとめ部分を最適化"""
        lines = content.split('\n')
        
        # まとめセクションを探す
        summary_index = -1
        for i, line in enumerate(lines):
            if any(word in line.lower() for word in ['まとめ', 'conclusion', '最後に']):
                summary_index = i
                break
        
        if summary_index > 0 and keyword.lower() not in lines[summary_index:]:
            # まとめ部分にキーワードを追加
            for i in range(summary_index + 1, len(lines)):
                if lines[i].strip() and not lines[i].startswith('#'):
                    lines[i] = f"{keyword}を活用することで、" + lines[i]
                    break
        
        return '\n'.join(lines)
    
    def _add_semantic_keywords(self, content: str, semantic_keywords: List[str]) -> str:
        """セマンティックキーワードを追加"""
        # 自然な形でセマンティックキーワードを配置
        # 実装は簡略化（実際にはより高度な自然言語処理が必要）
        return content
    
    def generate_meta_description(self, title: str, keywords: Dict[str, List[str]]) -> str:
        """SEO最適化されたメタディスクリプションを生成"""
        # キーワードリストが空でないことを確認
        primary_keywords = keywords.get("primary", ["AI音楽"])
        if not primary_keywords:
            primary_keywords = ["AI音楽"]
        primary_keyword = primary_keywords[0]
        intent_keywords = keywords.get("intent", [])
        
        templates = [
            f"{primary_keyword}の使い方を詳しく解説。初心者でも簡単に始められる方法をステップバイステップで紹介します。",
            f"【最新版】{primary_keyword}の特徴・料金・使い方を徹底解説。他ツールとの比較も含めて完全ガイド。",
            f"{primary_keyword}で高品質な音楽を作る方法を解説。プロが教えるコツとテクニックをお伝えします。",
            f"{primary_keyword}について知りたい方必見！基本から応用まで分かりやすく解説した完全ガイドです。"
        ]
        
        meta_desc = random.choice(templates)
        
        # 120文字以内に調整
        if len(meta_desc) > 120:
            meta_desc = meta_desc[:117] + "..."
        
        return meta_desc
    
    def get_keyword_suggestions(self, base_keyword: str) -> List[str]:
        """関連キーワードの提案"""
        suggestions = []
        
        # 既存のキーワードデータから関連語を抽出
        for category, keywords in self.seo_data["long_tail_keywords"].items():
            for keyword in keywords:
                if base_keyword.lower() in keyword.lower():
                    suggestions.append(keyword)
        
        # セマンティックキーワードからも提案
        for category, keywords in self.seo_data["semantic_keywords"].items():
            suggestions.extend(random.sample(keywords, min(2, len(keywords))))
        
        return suggestions[:10]


def main():
    """テスト用メイン関数"""
    seo_strategy = SEOKeywordStrategy()
    
    # キーワード生成テスト
    keywords = seo_strategy.generate_seo_optimized_keywords(
        article_type="tutorial",
        tool_name="Suno",
        target_difficulty="medium"
    )
    
    print("🎯 生成されたキーワードセット:")
    for category, kw_list in keywords.items():
        print(f"  {category}: {kw_list}")
    
    # タイトル生成テスト
    titles = seo_strategy.generate_seo_title_variations(
        "音楽制作の始め方",
        keywords
    )
    
    print(f"\n📝 SEO最適化タイトル案:")
    for i, title in enumerate(titles, 1):
        print(f"  {i}. {title}")
    
    # メタディスクリプション生成テスト
    meta_desc = seo_strategy.generate_meta_description(titles[0], keywords)
    print(f"\n📋 メタディスクリプション:")
    print(f"  {meta_desc}")


if __name__ == "__main__":
    main()