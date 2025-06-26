"""
コンテンツ戦略モジュール
タイトルと内容の一貫性を確保するための戦略
"""

from typing import Dict, List, Tuple
import re

class ContentStrategy:
    """タイトルに基づいて適切なコンテンツ戦略を決定"""
    
    @staticmethod
    def analyze_title(title: str) -> Dict[str, any]:
        """タイトルを分析して、記事の方向性を決定"""
        
        # タイトルから年を抽出
        year_match = re.search(r'(\d{4})年', title)
        year = year_match.group(1) if year_match else "2025"
        
        # メインタイトルを抽出（】の後の部分）
        main_title_match = re.search(r'】(.+)$', title)
        main_title = main_title_match.group(1) if main_title_match else title
        
        # キーワード分析
        analysis = {
            'year': year,
            'main_title': main_title,
            'content_type': ContentStrategy._determine_content_type(main_title),
            'main_focus': ContentStrategy._determine_main_focus(main_title),
            'target_audience': ContentStrategy._determine_target_audience(main_title),
            'key_topics': ContentStrategy._extract_key_topics(main_title)
        }
        
        return analysis
    
    @staticmethod
    def _determine_content_type(title: str) -> str:
        """コンテンツタイプを決定"""
        
        # チュートリアル系
        if any(word in title for word in ['使い方', '始め方', '入門', 'ガイド', '方法', '手順']):
            return 'tutorial'
        
        # 比較・レビュー系
        elif any(word in title for word in ['比較', 'vs', 'VS', 'どっち', 'おすすめ', 'ランキング', 'TOP']):
            return 'comparison'
        
        # 技術解説系
        elif any(word in title for word in ['仕組み', 'アルゴリズム', '技術', '理論', 'API', '実装']):
            return 'technical'
        
        # ニュース・トレンド系
        elif any(word in title for word in ['最新', '新機能', 'アップデート', 'リリース', '発表']):
            return 'news'
        
        # 実践・活用系
        elif any(word in title for word in ['活用', '実例', '事例', 'プロ', '収益化', '稼ぐ']):
            return 'practical'
        
        # 開発系
        elif any(word in title for word in ['作る', '開発', 'React', 'Python', 'JavaScript', 'アプリ']):
            return 'development'
        
        else:
            return 'general'
    
    @staticmethod
    def _determine_main_focus(title: str) -> str:
        """メインフォーカスを決定"""
        
        # 特定のツール名が含まれているか
        tools = {
            'suno': ['Suno', 'suno', 'スーノ'],
            'udio': ['Udio', 'udio', 'ウディオ'],
            'stable_audio': ['Stable Audio', 'StableAudio'],
            'musicgen': ['MusicGen', 'musicgen'],
            'aiva': ['AIVA', 'Aiva'],
            'musiclm': ['MusicLM', 'musiclm'],
            'riffusion': ['Riffusion', 'riffusion']
        }
        
        for tool_key, tool_names in tools.items():
            if any(name in title for name in tool_names):
                return tool_key
        
        # 技術カテゴリー
        if any(word in title for word in ['音声合成', 'TTS', 'ボイス', '音声']):
            return 'voice_synthesis'
        elif any(word in title for word in ['作曲', 'メロディ', 'ビート', 'リズム']):
            return 'composition'
        elif any(word in title for word in ['歌詞', 'リリック', '作詞']):
            return 'lyrics'
        elif any(word in title for word in ['ミックス', 'マスタリング', 'エフェクト']):
            return 'audio_processing'
        else:
            return 'ai_music_general'
    
    @staticmethod
    def _determine_target_audience(title: str) -> str:
        """ターゲットオーディエンスを決定"""
        
        if any(word in title for word in ['初心者', '入門', '始め方', '基本']):
            return 'beginner'
        elif any(word in title for word in ['プロ', '上級', 'advanced', '収益化']):
            return 'professional'
        elif any(word in title for word in ['開発', 'API', 'React', 'Python', 'コード']):
            return 'developer'
        else:
            return 'general'
    
    @staticmethod
    def _extract_key_topics(title: str) -> List[str]:
        """キートピックを抽出"""
        topics = []
        
        # ツール名
        tool_names = ['Suno', 'Udio', 'Stable Audio', 'MusicGen', 'AIVA', 'MusicLM', 'Riffusion']
        for tool in tool_names:
            if tool.lower() in title.lower():
                topics.append(tool)
        
        # 技術用語
        tech_terms = ['AI', '音楽生成', '作曲', 'API', '音声合成', 'TTS', 'React', 'Python', 
                      'JavaScript', 'TypeScript', 'Transformer', '深層学習', '機械学習']
        for term in tech_terms:
            if term in title:
                topics.append(term)
        
        # アクション
        actions = ['作る', '使う', '始める', '学ぶ', '比較', '選ぶ', '活用', '収益化']
        for action in actions:
            if action in title:
                topics.append(action)
        
        return topics
    
    @staticmethod
    def generate_content_outline(title_analysis: Dict[str, any]) -> Dict[str, any]:
        """タイトル分析に基づいてコンテンツアウトラインを生成"""
        
        content_type = title_analysis['content_type']
        main_focus = title_analysis['main_focus']
        
        # コンテンツタイプに応じたアウトライン
        if content_type == 'tutorial':
            return ContentStrategy._generate_tutorial_outline(title_analysis)
        elif content_type == 'comparison':
            return ContentStrategy._generate_comparison_outline(title_analysis)
        elif content_type == 'technical':
            return ContentStrategy._generate_technical_outline(title_analysis)
        elif content_type == 'development':
            return ContentStrategy._generate_development_outline(title_analysis)
        elif content_type == 'practical':
            return ContentStrategy._generate_practical_outline(title_analysis)
        else:
            return ContentStrategy._generate_general_outline(title_analysis)
    
    @staticmethod
    def _generate_tutorial_outline(analysis: Dict) -> Dict:
        """チュートリアル記事のアウトライン"""
        main_focus = analysis['main_focus']
        
        # ツール固有のチュートリアル
        if main_focus in ['suno', 'udio', 'stable_audio', 'musicgen', 'aiva']:
            tool_name = main_focus.replace('_', ' ').title()
            return {
                'sections': [
                    f'{tool_name}とは？基本概要',
                    'アカウント作成と初期設定',
                    '基本的な使い方（ステップバイステップ）',
                    '高度な機能と設定',
                    'よくあるトラブルと解決方法',
                    '作品例とインスピレーション',
                    'まとめと次のステップ'
                ],
                'focus_points': [
                    '具体的な操作手順',
                    'スクリーンショット指示',
                    '初心者向けの説明',
                    '実践的なTips'
                ]
            }
        else:
            return {
                'sections': [
                    '概要と背景',
                    '必要な準備',
                    '基本ステップ',
                    '応用テクニック',
                    'トラブルシューティング',
                    'まとめ'
                ],
                'focus_points': [
                    '分かりやすい説明',
                    '実践的な例',
                    '段階的な学習'
                ]
            }
    
    @staticmethod
    def _generate_comparison_outline(analysis: Dict) -> Dict:
        """比較記事のアウトライン"""
        return {
            'sections': [
                '比較対象の概要',
                '機能比較表',
                '料金プラン比較',
                '使いやすさの比較',
                'クオリティ比較（実例付き）',
                'どんな人におすすめ？',
                '総合評価とまとめ'
            ],
            'focus_points': [
                '客観的な比較',
                '具体的な数値や例',
                '用途別の推奨',
                '比較表の活用'
            ]
        }
    
    @staticmethod
    def _generate_technical_outline(analysis: Dict) -> Dict:
        """技術解説記事のアウトライン"""
        return {
            'sections': [
                '技術の背景と重要性',
                '基本的な仕組み',
                'アーキテクチャ解説',
                '実装例とコード',
                '性能と制限',
                '今後の展望',
                'まとめ'
            ],
            'focus_points': [
                '技術的な正確性',
                'ダイアグラムや図表',
                'コード例',
                '理論と実践のバランス'
            ]
        }
    
    @staticmethod
    def _generate_development_outline(analysis: Dict) -> Dict:
        """開発記事のアウトライン"""
        return {
            'sections': [
                'プロジェクト概要',
                '開発環境のセットアップ',
                '基本実装',
                '機能追加と拡張',
                'テストとデバッグ',
                'デプロイと公開',
                'まとめと改善点'
            ],
            'focus_points': [
                '実際に動くコード',
                'ステップバイステップの説明',
                'エラー対処法',
                'ベストプラクティス'
            ]
        }
    
    @staticmethod
    def _generate_practical_outline(analysis: Dict) -> Dict:
        """実践・活用記事のアウトライン"""
        return {
            'sections': [
                '実践の背景と目的',
                '成功事例の紹介',
                '具体的な活用方法',
                '収益化の戦略',
                '注意点とリスク',
                'ケーススタディ',
                'まとめと行動計画'
            ],
            'focus_points': [
                '実際の成功例',
                '具体的な数値',
                '再現可能な方法',
                '実践的なアドバイス'
            ]
        }
    
    @staticmethod
    def _generate_general_outline(analysis: Dict) -> Dict:
        """一般記事のアウトライン"""
        return {
            'sections': [
                '導入と背景',
                'メインコンテンツ1',
                'メインコンテンツ2',
                'メインコンテンツ3',
                '実例と応用',
                'まとめと展望'
            ],
            'focus_points': [
                'バランスの取れた内容',
                '読者の興味を引く構成',
                '実用的な情報'
            ]
        }