"""
Image Generator for AI Melody Kobo
記事のアイキャッチ画像を自動生成
"""

import os
import requests
import logging
from typing import Dict, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
from pathlib import Path
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)


class ThumbnailGenerator:
    """記事のサムネイル画像を生成するクラス"""
    
    def __init__(self, assets_dir: Optional[str] = None):
        """
        画像生成器の初期化
        
        Args:
            assets_dir: アセット（フォント、背景画像等）のディレクトリ
        """
        self.assets_dir = Path(assets_dir or "assets")
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # デフォルトの画像サイズ（WordPress推奨）
        # 16:9の比率が一般的
        self.default_size = (1200, 675)  # 16:9比率
        
        # その他の一般的なサイズオプション
        self.size_presets = {
            'wordpress_default': (1200, 675),  # 16:9
            'og_image': (1200, 630),  # Open Graph推奨
            'twitter_card': (1200, 600),  # Twitter Card
            'square': (1200, 1200),  # 正方形
            'wordpress_featured': (1920, 1080)  # フルHD
        }
        
        # カラーパレット（AI音楽をイメージ）
        self.color_schemes = {
            'suno': {
                'primary': '#FF6B6B',
                'secondary': '#4ECDC4',
                'background': '#1A1D23',
                'text': '#FFFFFF'
            },
            'udio': {
                'primary': '#7B68EE',
                'secondary': '#FF69B4',
                'background': '#2D2D3F',
                'text': '#FFFFFF'
            },
            'musicgen': {
                'primary': '#00D9FF',
                'secondary': '#FF00FF',
                'background': '#0A0E27',
                'text': '#FFFFFF'
            },
            'general': {
                'primary': '#667EEA',
                'secondary': '#764BA2',
                'background': '#1A202C',
                'text': '#FFFFFF'
            },
            'comparison': {
                'primary': '#F56565',
                'secondary': '#48BB78',
                'background': '#2D3748',
                'text': '#FFFFFF'
            }
        }
    
    def generate_thumbnail(self, 
                          title: str,
                          subtitle: Optional[str] = None,
                          theme: str = 'general',
                          keywords: Optional[list] = None,
                          size_preset: str = 'wordpress_default') -> bytes:
        """
        記事のサムネイル画像を生成
        
        Args:
            title: 記事タイトル
            subtitle: サブタイトル
            theme: カラーテーマ
            keywords: キーワード（ツール名等）
            
        Returns:
            画像データ（bytes）
        """
        # カラースキームを選択
        colors = self._select_color_scheme(theme, keywords)
        
        # サイズを選択
        size = self.size_presets.get(size_preset, self.default_size)
        
        # 画像を作成
        img = Image.new('RGB', size, color=colors['background'])
        draw = ImageDraw.Draw(img)
        
        # グラデーション背景を追加
        self._add_gradient_background(img, colors)
        
        # 装飾要素を追加
        self._add_decorative_elements(img, draw, colors)
        
        # AI音楽をイメージしたパターンを追加
        self._add_music_pattern(img, draw, colors)
        
        # テキストを追加
        self._add_text(img, draw, title, subtitle, colors)
        
        # ロゴやブランディングを追加
        self._add_branding(img, draw, colors)
        
        # バイトデータに変換
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG', optimize=True, quality=95)
        img_bytes.seek(0)
        
        return img_bytes.getvalue()
    
    def _select_color_scheme(self, theme: str, keywords: Optional[list]) -> Dict[str, str]:
        """キーワードに基づいてカラースキームを選択"""
        if keywords:
            keywords_lower = [k.lower() for k in keywords]
            if 'suno' in keywords_lower:
                return self.color_schemes['suno']
            elif 'udio' in keywords_lower:
                return self.color_schemes['udio']
            elif 'musicgen' in keywords_lower:
                return self.color_schemes['musicgen']
            elif '比較' in keywords_lower or 'comparison' in keywords_lower:
                return self.color_schemes['comparison']
        
        return self.color_schemes.get(theme, self.color_schemes['general'])
    
    def _add_gradient_background(self, img: Image.Image, colors: Dict[str, str]):
        """グラデーション背景を追加"""
        width, height = img.size
        
        # グラデーションを作成
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)
        
        # 縦方向のグラデーション
        for y in range(height):
            # 背景色から primary color への遷移
            ratio = y / height
            r1, g1, b1 = self._hex_to_rgb(colors['background'])
            r2, g2, b2 = self._hex_to_rgb(colors['primary'])
            
            r = int(r1 + (r2 - r1) * ratio * 0.3)  # 30%の強度
            g = int(g1 + (g2 - g1) * ratio * 0.3)
            b = int(b1 + (b2 - b1) * ratio * 0.3)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # 元の画像に合成
        img.paste(gradient, (0, 0))
    
    def _add_decorative_elements(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """装飾要素を追加（円、波形など）"""
        width, height = img.size
        
        # 半透明の円を追加
        for i in range(5):
            x = width * (0.1 + i * 0.2)
            y = height * (0.7 + (i % 2) * 0.1)
            radius = 50 + i * 20
            
            # 半透明の円を描画
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            color_with_alpha = self._hex_to_rgb(colors['secondary']) + (50,)  # アルファ値50
            overlay_draw.ellipse(
                [(x - radius, y - radius), (x + radius, y + radius)],
                fill=color_with_alpha
            )
            
            # ブラー効果
            overlay = overlay.filter(ImageFilter.GaussianBlur(radius=10))
            img.paste(overlay, (0, 0), overlay)
    
    def _add_music_pattern(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """音楽をイメージしたパターンを追加（波形、音符など）"""
        width, height = img.size
        
        # 波形パターン
        wave_height = height // 3
        wave_y = height // 2
        
        for x in range(0, width, 4):
            # サイン波で音波を表現
            import math
            y_offset = int(math.sin(x * 0.02) * 30)
            bar_height = abs(y_offset) + 10
            
            # 波形バーを描画
            color = colors['primary'] if x % 8 < 4 else colors['secondary']
            alpha = 100
            
            draw.rectangle(
                [(x, wave_y - bar_height), (x + 2, wave_y + bar_height)],
                fill=self._hex_to_rgb(color)
            )
    
    def _add_text(self, img: Image.Image, draw: ImageDraw.Draw, 
                  title: str, subtitle: Optional[str], colors: Dict[str, str]):
        """テキストを追加"""
        width, height = img.size
        
        # フォントの設定（システムフォントを使用）
        try:
            # 日本語フォントを優先
            # フォントサイズを調整
            date_font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 32)
            title_font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 48)
            blog_font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 24)
        except:
            # フォールバック
            date_font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            blog_font = ImageFont.load_default()
        
        # 日時を抽出（タイトルから【】内の日時を取得）
        import re
        date_match = re.search(r'【(.+?)】', title)
        if date_match:
            date_text = date_match.group(1)
            # タイトルから日時を除去
            title_text = re.sub(r'【.+?】', '', title).strip()
        else:
            date_text = datetime.now().strftime('%Y年%m月')
            title_text = title
        
        # 各テキスト要素の高さを計算
        date_lines = [date_text]  # 日時は1行
        title_lines = self._wrap_text(title_text, title_font, width - 200)
        blog_name = "AI Melody Kobo"
        
        # 行間設定
        date_height = 40
        title_line_height = 80
        blog_height = 30
        spacing_between_elements = 30  # 要素間の余白
        
        # 全体の高さを計算
        total_height = (
            date_height +  # 日時
            spacing_between_elements + 
            (len(title_lines) * title_line_height) +  # タイトル
            spacing_between_elements + 
            blog_height  # ブログ名
        )
        
        # 縦方向の中央に配置するための開始位置
        y_offset = (height - total_height) // 2
        
        # 1. 日時を描画（中央揃え）
        date_bbox = date_font.getbbox(date_text)
        date_width = date_bbox[2] - date_bbox[0]
        x_position = (width - date_width) // 2
        
        # 影を描画
        draw.text((x_position + 2, y_offset + 2), date_text, font=date_font, fill=(0, 0, 0, 128))
        # 本文を描画
        draw.text((x_position, y_offset), date_text, font=date_font, fill=colors['text'])
        
        y_offset += date_height + spacing_between_elements
        
        # 2. タイトルを描画（中央揃え、複数行対応）
        for line in title_lines:
            # テキストの幅を取得して中央揃え
            bbox = title_font.getbbox(line)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) // 2
            
            # 影を描画
            draw.text((x_position + 2, y_offset + 2), line, font=title_font, fill=(0, 0, 0, 128))
            # 本文を描画
            draw.text((x_position, y_offset), line, font=title_font, fill=colors['text'])
            y_offset += title_line_height
        
        y_offset += spacing_between_elements
        
        # 3. ブログ名を描画（中央揃え）
        blog_bbox = blog_font.getbbox(blog_name)
        blog_width = blog_bbox[2] - blog_bbox[0]
        x_position = (width - blog_width) // 2
        
        # 少し薄い色で描画
        blog_color = colors['text'] + 'CC'  # アルファ値を追加
        draw.text((x_position, y_offset), blog_name, font=blog_font, fill=colors['text'])
    
    def _add_branding(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """ブランディング要素を追加"""
        width, height = img.size
        
        # AI Melody Kobo のロゴテキスト
        try:
            brand_font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 20)
        except:
            brand_font = ImageFont.load_default()
        
        brand_text = "AI Melody Kobo"
        draw.text((width - 200, height - 40), brand_text, font=brand_font, fill=colors['text'])
    
    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> list:
        """テキストを折り返し（日本語対応・自然な改行）"""
        lines = []
        
        # まず句読点、助詞、記号で区切れる位置を探す
        import re
        
        # 改行候補となる区切り文字
        delimiters = ['：', '、', '。', '！', '？', 'ー', '・', '／', '（', '）', '「', '」', ' ']
        
        # 助詞での区切り（後に続く文字がある場合のみ）
        particles = ['の', 'を', 'に', 'で', 'と', 'は', 'が', 'から', 'まで', 'より']
        
        # タイトルが短い場合はそのまま返す
        bbox = font.getbbox(text)
        if bbox[2] - bbox[0] <= max_width:
            return [text]
        
        # 単語や句で分割を試みる
        current_line = ""
        i = 0
        
        while i < len(text):
            char = text[i]
            test_line = current_line + char
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                current_line = test_line
                i += 1
            else:
                # 改行位置を探す
                best_break = len(current_line)
                found_break = False
                
                # 句読点や記号での改行を優先
                for delimiter in delimiters:
                    pos = current_line.rfind(delimiter)
                    if pos > 0:
                        best_break = pos + len(delimiter)
                        found_break = True
                        break
                
                # 句読点がない場合は助詞での改行を試みる
                if not found_break:
                    for particle in particles:
                        pos = current_line.rfind(particle)
                        # 助詞の後に文字が続く場合のみ改行
                        if pos > 0 and pos + len(particle) < len(current_line):
                            best_break = pos + len(particle)
                            found_break = True
                            break
                
                # それでも見つからない場合は、なるべく長い位置で改行
                if not found_break and len(current_line) > 10:
                    # カタカナ・ひらがなの境界を探す
                    for j in range(len(current_line) - 1, max(0, len(current_line) - 10), -1):
                        if (self._is_katakana(current_line[j-1]) and not self._is_katakana(current_line[j])) or \
                           (not self._is_katakana(current_line[j-1]) and self._is_katakana(current_line[j])):
                            best_break = j
                            break
                
                # 改行を実行
                if best_break > 0:
                    lines.append(current_line[:best_break])
                    current_line = current_line[best_break:]
                else:
                    # どうしても改行位置が見つからない場合は現在の位置で改行
                    lines.append(current_line)
                    current_line = char
                    i += 1
        
        if current_line:
            lines.append(current_line)
        
        # 最大3行に制限
        if len(lines) > 3:
            # 3行目を短くして「...」を追加
            third_line = lines[2]
            while len(third_line) > 1:
                test_line = third_line + "..."
                bbox = font.getbbox(test_line)
                if bbox[2] - bbox[0] <= max_width:
                    lines = lines[:2] + [test_line]
                    break
                third_line = third_line[:-1]
        
        return lines
    
    def _is_katakana(self, char: str) -> bool:
        """カタカナかどうかを判定"""
        return '\u30A0' <= char <= '\u30FF'
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """16進数カラーをRGBに変換"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def generate_from_article_data(self, article_data: Dict) -> bytes:
        """記事データから自動的に画像を生成"""
        title = article_data.get('title', 'AI Music Article')
        tags = article_data.get('tags', [])
        
        # テーマを自動判定
        theme = 'general'
        if any('比較' in tag for tag in tags):
            theme = 'comparison'
        
        # サブタイトルは使用しない（新しいレイアウトでは不要）
        subtitle = None
        
        return self.generate_thumbnail(
            title=title,
            subtitle=subtitle,
            theme=theme,
            keywords=tags
        )