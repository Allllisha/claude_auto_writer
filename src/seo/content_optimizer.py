"""
SEO Content Optimizer
AI Melody Kobo - SEO最適化コンテンツ生成システム
"""

import re
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random

logger = logging.getLogger(__name__)


class SEOContentOptimizer:
    """SEO最適化コンテンツ生成システム"""
    
    def __init__(self):
        """初期化"""
        # SEO要件定義
        self.seo_requirements = {
            "title_length": {"min": 30, "max": 60},
            "meta_description_length": {"min": 120, "max": 160},
            "heading_structure": {
                "h1_count": 1,
                "h2_min": 3,
                "h2_max": 8,
                "h3_per_h2": {"min": 1, "max": 4}
            },
            "content_length": {
                "min_words": 1500,
                "max_words": 4000,
                "optimal": 2500
            },
            "keyword_density": {
                "primary": {"min": 1.0, "max": 3.0, "optimal": 2.0},
                "secondary": {"min": 0.5, "max": 1.5},
                "semantic": {"total": 5.0}
            },
            "readability": {
                "sentence_length_max": 25,
                "paragraph_length_max": 150,
                "bullet_points_min": 3
            }
        }
        
        # 記事構造テンプレート
        self.content_structures = {
            "beginner_guide": {
                "sections": [
                    "導入（問題提起）",
                    "基本概念の説明", 
                    "ステップバイステップガイド",
                    "よくある間違いと対策",
                    "実践例・サンプル",
                    "応用テクニック",
                    "まとめ・次のアクション"
                ],
                "cta_positions": [3, 6]  # CTAを配置する位置
            },
            "tutorial": {
                "sections": [
                    "概要と前提知識",
                    "必要な準備・ツール",
                    "基本的な手順",
                    "詳細な実装方法",
                    "トラブルシューティング",
                    "発展的な活用法",
                    "まとめ・参考資料"
                ],
                "cta_positions": [2, 5]
            },
            "comparison": {
                "sections": [
                    "比較対象の紹介",
                    "評価基準の設定",
                    "機能・性能比較",
                    "価格・コスト比較",
                    "使いやすさ比較",
                    "総合評価・推奨",
                    "選択ガイド・まとめ"
                ],
                "cta_positions": [4, 6]
            },
            "review": {
                "sections": [
                    "製品・サービス概要",
                    "特徴・機能詳細",
                    "実際の使用感",
                    "メリット・デメリット",
                    "価格・コストパフォーマンス",
                    "競合との比較",
                    "総合評価・推奨度"
                ],
                "cta_positions": [3, 6]
            }
        }
        
        # E-A-T（専門性・権威性・信頼性）強化要素
        self.eat_elements = {
            "expertise_indicators": [
                "実際に使用して検証",
                "業界経験に基づく",
                "専門知識を活用した",
                "最新の技術動向を踏まえた",
                "実践的な観点から"
            ],
            "authority_signals": [
                "多くのユーザーに支持されている",
                "業界標準として認知されている",
                "公式情報に基づく",
                "信頼できるソースからの情報",
                "専門家の見解として"
            ],
            "trust_factors": [
                "2024年最新情報",
                "定期的にアップデート",
                "正確性を期すため複数ソースで確認",
                "実際の検証結果",
                "透明性のある評価基準"
            ]
        }
    
    def optimize_article_structure(self, 
                                 article_type: str,
                                 topic: str,
                                 keywords: Dict[str, List[str]]) -> Dict[str, any]:
        """
        記事構造をSEO最適化
        
        Args:
            article_type: 記事タイプ
            topic: 記事トピック
            keywords: キーワードセット
            
        Returns:
            最適化された記事構造
        """
        structure = self.content_structures.get(article_type, self.content_structures["tutorial"])
        
        # キーワードリストが空でないことを確認
        primary_keywords = keywords.get("primary", ["AI音楽"])
        if not primary_keywords:
            primary_keywords = ["AI音楽"]
        primary_keyword = primary_keywords[0]
        
        # SEO最適化された見出し構造を生成
        optimized_sections = []
        for i, section in enumerate(structure["sections"]):
            heading_level = "##" if i == 0 else "##"
            
            # キーワードを自然に組み込んだ見出しを生成
            optimized_heading = self._create_seo_heading(
                section, primary_keyword, keywords, heading_level
            )
            
            optimized_sections.append({
                "heading": optimized_heading,
                "level": 2,
                "section_type": section,
                "target_length": self._calculate_section_length(len(structure["sections"]), i),
                "keywords_to_include": self._select_section_keywords(keywords, i),
                "cta_after": i in structure.get("cta_positions", [])
            })
        
        return {
            "sections": optimized_sections,
            "total_target_length": self.seo_requirements["content_length"]["optimal"],
            "keyword_distribution": self._plan_keyword_distribution(keywords, len(optimized_sections)),
            "internal_links": self._suggest_internal_links(topic, primary_keyword),
            "external_links": self._suggest_external_links(primary_keyword),
            "schema_markup": self._generate_schema_suggestions(article_type, topic)
        }
    
    def _create_seo_heading(self, 
                           section: str,
                           primary_keyword: str,
                           keywords: Dict[str, List[str]],
                           level: str) -> str:
        """SEO最適化された見出しを作成"""
        
        heading_templates = {
            "導入（問題提起）": [
                f"{primary_keyword}とは？初心者が知るべき基本知識",
                f"{primary_keyword}を始める前に知っておきたいこと",
                f"なぜ{primary_keyword}が注目されているのか"
            ],
            "基本概念の説明": [
                f"{primary_keyword}の基本的な仕組みと特徴",
                f"{primary_keyword}で押さえておくべき重要ポイント",
                f"{primary_keyword}の核となる機能と使い方"
            ],
            "ステップバイステップガイド": [
                f"{primary_keyword}の始め方｜5つのステップで完全マスター",
                f"初心者向け{primary_keyword}実践ガイド",
                f"{primary_keyword}を使いこなすための具体的手順"
            ]
        }
        
        if section in heading_templates:
            return f"{level} {random.choice(heading_templates[section])}"
        else:
            # デフォルトの見出し生成
            semantic_keyword = random.choice(keywords.get("semantic", ["音楽制作"]))
            return f"{level} {primary_keyword}で{semantic_keyword}をレベルアップする方法"
    
    def _calculate_section_length(self, total_sections: int, section_index: int) -> int:
        """セクションごとの目標文字数を計算"""
        total_length = self.seo_requirements["content_length"]["optimal"]
        
        # 導入とまとめは短め、中間セクションは長めに
        if section_index == 0:  # 導入
            return int(total_length * 0.15)
        elif section_index == total_sections - 1:  # まとめ
            return int(total_length * 0.10)
        else:  # 中間セクション
            remaining_length = total_length * 0.75
            middle_sections = total_sections - 2
            return int(remaining_length / middle_sections)
    
    def _select_section_keywords(self, keywords: Dict[str, List[str]], section_index: int) -> List[str]:
        """セクションごとに使用するキーワードを選択"""
        all_keywords = []
        
        # プライマリキーワードは全セクションで使用
        all_keywords.extend(keywords.get("primary", [])[:1])
        
        # セマンティックキーワードを分散配置
        semantic_keywords = keywords.get("semantic", [])
        if semantic_keywords:
            keyword_per_section = max(1, len(semantic_keywords) // 6)
            start_idx = (section_index * keyword_per_section) % len(semantic_keywords)
            selected_semantic = semantic_keywords[start_idx:start_idx + keyword_per_section]
            all_keywords.extend(selected_semantic)
        
        # インテントキーワードを適切なセクションに配置
        intent_keywords = keywords.get("intent", [])
        if intent_keywords and section_index < len(intent_keywords):
            all_keywords.append(intent_keywords[section_index])
        
        return all_keywords
    
    def _plan_keyword_distribution(self, keywords: Dict[str, List[str]], section_count: int) -> Dict:
        """キーワードの配置計画を作成"""
        # キーワードリストが空でないことを確認
        primary_keywords = keywords.get("primary", ["AI音楽"])
        if not primary_keywords:
            primary_keywords = ["AI音楽"]
        primary_keyword = primary_keywords[0]
        target_density = self.seo_requirements["keyword_density"]["primary"]["optimal"]
        total_words = self.seo_requirements["content_length"]["optimal"]
        
        # プライマリキーワードの出現回数を計算
        target_occurrences = int((total_words * target_density) / 100)
        
        return {
            "primary_keyword": primary_keyword,
            "target_occurrences": target_occurrences,
            "occurrences_per_section": target_occurrences // section_count,
            "density_target": f"{target_density}%",
            "keyword_placement_strategy": {
                "title": 1,
                "meta_description": 1,
                "first_paragraph": 1,
                "headings": section_count // 2,
                "conclusion": 1,
                "natural_mentions": target_occurrences - 4 - (section_count // 2)
            }
        }
    
    def _suggest_internal_links(self, topic: str, primary_keyword: str) -> List[Dict]:
        """内部リンクの提案"""
        # 実際の実装では、既存記事のデータベースから関連記事を検索
        return [
            {
                "anchor_text": f"{primary_keyword}の基礎知識",
                "url": "/basic-guide",
                "relevance": "high",
                "placement": "導入部分"
            },
            {
                "anchor_text": "AI音楽ツール比較",
                "url": "/comparison",
                "relevance": "medium", 
                "placement": "まとめ部分"
            },
            {
                "anchor_text": "音楽制作のコツ",
                "url": "/tips",
                "relevance": "medium",
                "placement": "中間セクション"
            }
        ]
    
    def _suggest_external_links(self, primary_keyword: str) -> List[Dict]:
        """外部リンクの提案"""
        return [
            {
                "anchor_text": f"{primary_keyword}公式サイト",
                "url": "https://official-site.com",
                "purpose": "権威性向上",
                "placement": "製品紹介部分"
            },
            {
                "anchor_text": "音楽著作権について（JASRAC）",
                "url": "https://jasrac.or.jp",
                "purpose": "信頼性向上", 
                "placement": "注意事項部分"
            }
        ]
    
    def _generate_schema_suggestions(self, article_type: str, topic: str) -> Dict:
        """構造化データ（Schema.org）の提案"""
        base_schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": topic,
            "author": {
                "@type": "Person",
                "name": "AI Creator Alisa"
            },
            "publisher": {
                "@type": "Organization",
                "name": "AI Melody Kobo"
            }
        }
        
        if article_type == "tutorial":
            base_schema["@type"] = "HowTo"
            base_schema["step"] = []
        elif article_type == "review":
            base_schema["@type"] = "Review"
            base_schema["itemReviewed"] = {"@type": "SoftwareApplication"}
        
        return base_schema
    
    def generate_optimized_prompts(self,
                                 article_structure: Dict,
                                 keywords: Dict[str, List[str]],
                                 article_type: str) -> Dict[str, str]:
        """
        SEO最適化されたAI生成プロンプトを作成
        
        Args:
            article_structure: 記事構造
            keywords: キーワードセット
            article_type: 記事タイプ
            
        Returns:
            最適化されたプロンプトセット
        """
        # キーワードリストが空でないことを確認
        primary_keywords = keywords.get("primary", ["AI音楽"])
        if not primary_keywords:
            primary_keywords = ["AI音楽"]
        primary_keyword = primary_keywords[0]
        target_length = article_structure["total_target_length"]
        
        # メインプロンプト
        main_prompt = f"""
あなたは日本のAI音楽専門メディア「AI Melody Kobo」のライター「アリサ」です。

## 執筆指示
- トピック: {primary_keyword}について
- 記事タイプ: {article_type}
- 目標文字数: {target_length}文字
- ターゲット: AI音楽に興味がある初心者〜中級者

## SEO要件
- メインキーワード「{primary_keyword}」を記事全体で{article_structure['keyword_distribution']['target_occurrences']}回自然に使用
- キーワード密度: {article_structure['keyword_distribution']['density_target']}
- 関連キーワード: {', '.join(keywords.get('semantic', [])[:5])}

## 記事構造
以下の見出し構造で執筆してください：
"""
        
        for section in article_structure["sections"]:
            main_prompt += f"\n{section['heading']}"
            main_prompt += f"\n（目標: {section['target_length']}文字、キーワード: {', '.join(section['keywords_to_include'])}）"
        
        main_prompt += f"""

## 品質要件
- E-A-T（専門性・権威性・信頼性）を意識した執筆
- 実用性の高い具体的な情報を提供
- 読みやすい文章構造（1文25文字以内、1段落150文字以内）
- {article_structure['keyword_distribution']['keyword_placement_strategy']}
- 自然で読みやすい文章を心がける

## アリサのペルソナ
- AI音楽制作の専門知識を持つライター
- 読者に寄り添う親しみやすい文体
- 実践的で具体的なアドバイスを提供
- 初心者にも分かりやすい説明を心がける

上記の要件を満たした、SEO最適化された記事を執筆してください。
"""
        
        # タイトル生成プロンプト
        title_prompt = f"""
以下の条件でSEO最適化されたタイトルを5つ提案してください：

- メインキーワード: {primary_keyword}
- 記事タイプ: {article_type}
- 文字数: 30-60文字
- 検索意図: {', '.join(keywords.get('intent', [])[:3])}
- 現在の年月: {datetime.now().strftime('%Y年%m月')}

タイトルの要件:
- クリック率の高い魅力的な表現
- キーワードを自然に含む
- 記事の価値を明確に示す
- 数字や年度を含める
- 感情に訴える表現を使用
"""
        
        # メタディスクリプション生成プロンプト
        meta_prompt = f"""
以下の記事のメタディスクリプションを作成してください：

- メインキーワード: {primary_keyword}
- 記事の内容: {article_type}についての詳細解説
- 文字数: 120-160文字
- ターゲット: {primary_keyword}について知りたい人

要件:
- キーワードを自然に含める
- 記事の価値・メリットを明確に
- クリックを促す魅力的な表現
- 完結で分かりやすい説明
"""
        
        return {
            "main_content": main_prompt,
            "title_generation": title_prompt,
            "meta_description": meta_prompt,
            "keyword_guidance": self._create_keyword_guidance(keywords),
            "quality_checklist": self._create_quality_checklist()
        }
    
    def _create_keyword_guidance(self, keywords: Dict[str, List[str]]) -> str:
        """キーワード使用ガイダンス"""
        guidance = "## キーワード使用ガイダンス\n\n"
        
        for category, keyword_list in keywords.items():
            if keyword_list and isinstance(keyword_list, (list, tuple)):
                guidance += f"**{category.title()}キーワード:**\n"
                for keyword in keyword_list[:3]:
                    guidance += f"- {keyword}: 自然な文脈で使用\n"
                guidance += "\n"
        
        return guidance
    
    def _create_quality_checklist(self) -> str:
        """品質チェックリスト"""
        return """
## 品質チェックリスト

### SEO要件
- [ ] タイトルに主要キーワードが含まれている
- [ ] メタディスクリプションが120-160文字
- [ ] H2見出しが3つ以上ある
- [ ] キーワード密度が適切（1-3%）
- [ ] 内部リンクが2つ以上ある

### コンテンツ品質
- [ ] 1500文字以上の内容がある
- [ ] 実用的で具体的な情報を提供
- [ ] 読みやすい文章構造
- [ ] 専門性・権威性・信頼性を示す要素がある
- [ ] CTAが適切に配置されている

### ユーザビリティ
- [ ] 段落が適切な長さ（150文字以内）
- [ ] 箇条書きやリストを効果的に使用
- [ ] 画像挿入指示が適切にある
- [ ] モバイルでも読みやすい構造
"""
    
    def analyze_content_seo(self, content: str, keywords: Dict[str, List[str]]) -> Dict:
        """コンテンツのSEO分析"""
        # 文字数カウント
        word_count = len(content.replace(' ', ''))
        
        # キーワード密度分析
        # キーワードリストが空でないことを確認
        primary_keywords = keywords.get("primary", ["AI音楽"])
        if not primary_keywords:
            primary_keywords = ["AI音楽"]
        primary_keyword = primary_keywords[0]
        primary_occurrences = content.lower().count(primary_keyword.lower())
        primary_density = (primary_occurrences / word_count) * 100 if word_count > 0 else 0
        
        # 見出し構造分析
        h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
        h3_count = len(re.findall(r'^### ', content, re.MULTILINE))
        
        # 読みやすさ分析
        sentences = re.split(r'[。．！？]', content)
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
        
        return {
            "word_count": word_count,
            "keyword_analysis": {
                "primary_keyword": primary_keyword,
                "occurrences": primary_occurrences,
                "density": round(primary_density, 2)
            },
            "structure_analysis": {
                "h2_count": h2_count,
                "h3_count": h3_count,
                "heading_ratio": round(h2_count / (word_count / 500), 2) if word_count > 0 else 0
            },
            "readability": {
                "avg_sentence_length": round(avg_sentence_length, 1),
                "readability_score": self._calculate_readability_score(avg_sentence_length)
            },
            "seo_score": self._calculate_seo_score(word_count, primary_density, h2_count),
            "recommendations": self._generate_recommendations(word_count, primary_density, h2_count)
        }
    
    def _calculate_readability_score(self, avg_sentence_length: float) -> str:
        """読みやすさスコアを計算"""
        if avg_sentence_length <= 20:
            return "excellent"
        elif avg_sentence_length <= 25:
            return "good"
        elif avg_sentence_length <= 30:
            return "fair"
        else:
            return "poor"
    
    def _calculate_seo_score(self, word_count: int, keyword_density: float, h2_count: int) -> int:
        """SEOスコアを計算（100点満点）"""
        score = 0
        
        # 文字数スコア（30点）
        if 1500 <= word_count <= 4000:
            score += 30
        elif 1000 <= word_count < 1500 or 4000 < word_count <= 5000:
            score += 20
        elif word_count >= 500:
            score += 10
        
        # キーワード密度スコア（40点）
        if 1.0 <= keyword_density <= 3.0:
            score += 40
        elif 0.5 <= keyword_density < 1.0 or 3.0 < keyword_density <= 4.0:
            score += 25
        elif keyword_density > 0:
            score += 10
        
        # 見出し構造スコア（30点）
        if 3 <= h2_count <= 8:
            score += 30
        elif 2 <= h2_count < 3 or 8 < h2_count <= 10:
            score += 20
        elif h2_count > 0:
            score += 10
        
        return score
    
    def _generate_recommendations(self, word_count: int, keyword_density: float, h2_count: int) -> List[str]:
        """改善提案を生成"""
        recommendations = []
        
        if word_count < 1500:
            recommendations.append("文字数を1500文字以上に増やしてください")
        elif word_count > 4000:
            recommendations.append("文字数を4000文字以下に調整してください")
        
        if keyword_density < 1.0:
            recommendations.append("メインキーワードの使用頻度を増やしてください")
        elif keyword_density > 3.0:
            recommendations.append("メインキーワードの使用頻度を減らしてください")
        
        if h2_count < 3:
            recommendations.append("H2見出しを3つ以上追加してください")
        elif h2_count > 8:
            recommendations.append("H2見出しの数を8つ以下に調整してください")
        
        return recommendations


def main():
    """テスト用メイン関数"""
    optimizer = SEOContentOptimizer()
    
    # キーワードセット（例）
    keywords = {
        "primary": ["Suno AI", "スーノ"],
        "semantic": ["音楽制作", "AI作曲", "音楽生成"],
        "intent": ["使い方", "始め方", "方法"],
        "seasonal": ["2024年", "最新"]
    }
    
    # 記事構造最適化テスト
    structure = optimizer.optimize_article_structure(
        "beginner_guide",
        "Suno AIで音楽制作を始める方法",
        keywords
    )
    
    print("🎯 最適化された記事構造:")
    for section in structure["sections"]:
        print(f"  {section['heading']}")
        print(f"    目標文字数: {section['target_length']}")
        print(f"    キーワード: {section['keywords_to_include']}")
        print()
    
    # プロンプト生成テスト
    prompts = optimizer.generate_optimized_prompts(structure, keywords, "beginner_guide")
    
    print("📝 生成されたプロンプト:")
    print(prompts["main_content"][:500] + "...")


if __name__ == "__main__":
    main()