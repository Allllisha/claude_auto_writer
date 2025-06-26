"""
Modern Thumbnail Generator for AI Melody Kobo
近未来的でAI感のあるサムネイル画像を自動生成
"""

import os
import random
import math
import logging
from typing import Dict, Optional, Tuple, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import io
from pathlib import Path
from datetime import datetime
import colorsys

logger = logging.getLogger(__name__)


class ModernThumbnailGenerator:
    """モダンで近未来的なサムネイル画像を生成するクラス"""
    
    def __init__(self, assets_dir: Optional[str] = None):
        """
        画像生成器の初期化
        
        Args:
            assets_dir: アセット（フォント、背景画像等）のディレクトリ
        """
        self.assets_dir = Path(assets_dir or "assets")
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # デフォルトの画像サイズ（WordPress推奨）
        self.default_size = (1200, 675)  # 16:9比率
        
        # モダンなカラーテーマ（ネオン・サイバーパンク風）
        self.color_themes = {
            'neon_purple': {
                'primary': '#FF00FF',
                'secondary': '#00FFFF',
                'accent': '#FF00AA',
                'glow': '#FF00FF',
                'background': '#0A0A0F',
                'text': '#FFFFFF',
                'gradient_start': '#1A0033',
                'gradient_end': '#000511'
            },
            'cyber_blue': {
                'primary': '#00D4FF',
                'secondary': '#FF0080',
                'accent': '#00FF88',
                'glow': '#00D4FF',
                'background': '#000814',
                'text': '#FFFFFF',
                'gradient_start': '#001D3D',
                'gradient_end': '#000814'
            },
            'ai_green': {
                'primary': '#00FF41',
                'secondary': '#FF1744',
                'accent': '#FFEA00',
                'glow': '#00FF41',
                'background': '#0D1117',
                'text': '#FFFFFF',
                'gradient_start': '#001A00',
                'gradient_end': '#0D1117'
            },
            'synth_orange': {
                'primary': '#FF6B35',
                'secondary': '#F7931E',
                'accent': '#FF006E',
                'glow': '#FF6B35',
                'background': '#1A0E0A',
                'text': '#FFFFFF',
                'gradient_start': '#2D1810',
                'gradient_end': '#1A0E0A'
            },
            'hologram': {
                'primary': '#B388FF',
                'secondary': '#00E5FF',
                'accent': '#FF4081',
                'glow': '#B388FF',
                'background': '#0F0F23',
                'text': '#FFFFFF',
                'gradient_start': '#1A1A3E',
                'gradient_end': '#0F0F23'
            },
            'matrix': {
                'primary': '#00FF00',
                'secondary': '#00AA00',
                'accent': '#00FF00',
                'glow': '#00FF00',
                'background': '#000000',
                'text': '#00FF00',
                'gradient_start': '#001100',
                'gradient_end': '#000000'
            }
        }
        
        # 記事タイプ別のビジュアルスタイル
        self.visual_styles = {
            'music_generation': ['sound_waves', 'frequency_bars', 'circular_visualizer'],
            'voice_synthesis': ['voice_pattern', 'waveform_circle', 'digital_voice'],
            'tutorial': ['code_blocks', 'geometric_grid', 'tech_circuit'],
            'news': ['data_stream', 'hologram_effect', 'glitch_art'],
            'comparison': ['split_design', 'versus_style', 'dual_gradient'],
            'development': ['code_rain', 'binary_pattern', 'circuit_board']
        }
    
    def generate_thumbnail(self, 
                          title: str,
                          article_type: str = 'general',
                          tool_name: Optional[str] = None,
                          keywords: Optional[List[str]] = None,
                          theme_override: Optional[str] = None) -> bytes:
        """
        モダンなサムネイル画像を生成
        
        Args:
            title: 記事タイトル
            article_type: 記事タイプ
            tool_name: ツール名（Suno、Udio等）
            keywords: キーワードリスト
            theme_override: カラーテーマの上書き
            
        Returns:
            画像データ（bytes）
        """
        # カラーテーマを選択
        theme = self._select_theme(article_type, tool_name, keywords, theme_override)
        colors = self.color_themes[theme]
        
        # 画像を作成
        img = Image.new('RGBA', self.default_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 1. グラデーション背景
        self._create_gradient_background(img, colors)
        
        # 2. 記事タイプに応じたビジュアル要素を追加
        visual_style = self._select_visual_style(article_type)
        self._add_visual_element(img, draw, visual_style, colors)
        
        # 3. ネオン効果のある幾何学模様
        self._add_geometric_patterns(img, draw, colors)
        
        # 4. グロウ効果
        img = self._add_glow_effect(img, colors)
        
        # 5. 装飾的なアクセント（背景）
        self._add_decorative_accents(img, draw, colors)
        
        # 6. タイトルとテキスト要素（最前面に描画）
        draw = ImageDraw.Draw(img)  # drawオブジェクトを再取得
        self._add_modern_text(img, draw, title, colors, tool_name)
        
        # RGBに変換（透過を除去）
        final_img = Image.new('RGB', self.default_size, colors['background'])
        final_img.paste(img, (0, 0), img)
        
        # バイトデータに変換
        img_bytes = io.BytesIO()
        final_img.save(img_bytes, format='PNG', optimize=True, quality=95)
        img_bytes.seek(0)
        
        return img_bytes.getvalue()
    
    def _select_theme(self, article_type: str, tool_name: Optional[str], 
                     keywords: Optional[List[str]], theme_override: Optional[str]) -> str:
        """記事内容に基づいてカラーテーマを選択"""
        if theme_override and theme_override in self.color_themes:
            return theme_override
        
        # ツール別のテーマ
        tool_themes = {
            'suno': 'neon_purple',
            'udio': 'cyber_blue',
            'musicgen': 'ai_green',
            'stable audio': 'synth_orange',
            'aiva': 'hologram'
        }
        
        if tool_name and tool_name.lower() in tool_themes:
            return tool_themes[tool_name.lower()]
        
        # 記事タイプ別のテーマ
        type_themes = {
            'voice_synthesis': 'cyber_blue',
            'singing_synthesis': 'neon_purple',
            'programming': 'matrix',
            'app_development': 'ai_green',
            'music_analysis': 'hologram'
        }
        
        if article_type in type_themes:
            return type_themes[article_type]
        
        # ランダムに選択（matrix以外）
        themes = [t for t in self.color_themes.keys() if t != 'matrix']
        return random.choice(themes)
    
    def _select_visual_style(self, article_type: str) -> str:
        """記事タイプに応じたビジュアルスタイルを選択"""
        # 記事タイプのマッピング
        type_mapping = {
            'suno_specific': 'music_generation',
            'udio_specific': 'music_generation',
            'musicgen_specific': 'music_generation',
            'voice_synthesis': 'voice_synthesis',
            'singing_synthesis': 'voice_synthesis',
            'tutorial': 'tutorial',
            'beginner_guide': 'tutorial',
            'tool_update': 'news',
            'industry_news': 'news',
            'tool_comparison': 'comparison',
            'programming': 'development',
            'app_development': 'development'
        }
        
        style_category = type_mapping.get(article_type, 'music_generation')
        styles = self.visual_styles.get(style_category, self.visual_styles['music_generation'])
        return random.choice(styles)
    
    def _create_gradient_background(self, img: Image.Image, colors: Dict[str, str]):
        """高度なグラデーション背景を作成"""
        width, height = img.size
        draw = ImageDraw.Draw(img)
        
        # 放射状グラデーション
        center_x, center_y = width // 2, height // 2
        max_radius = math.sqrt(center_x**2 + center_y**2)
        
        # グラデーション用の一時画像
        gradient = Image.new('RGB', (width, height))
        grad_draw = ImageDraw.Draw(gradient)
        
        start_color = self._hex_to_rgb(colors['gradient_start'])
        end_color = self._hex_to_rgb(colors['gradient_end'])
        
        # 円形グラデーション
        for i in range(int(max_radius)):
            ratio = i / max_radius
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            grad_draw.ellipse(
                [(center_x - i, center_y - i), (center_x + i, center_y + i)],
                outline=(r, g, b)
            )
        
        # ノイズテクスチャを追加
        noise = Image.new('RGB', (width, height))
        noise_draw = ImageDraw.Draw(noise)
        for _ in range(1000):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            brightness = random.randint(0, 30)
            noise_draw.point((x, y), fill=(brightness, brightness, brightness))
        
        # ブレンド
        gradient = Image.blend(gradient, noise, 0.1)
        img.paste(gradient, (0, 0))
    
    def _add_visual_element(self, img: Image.Image, draw: ImageDraw.Draw, 
                           style: str, colors: Dict[str, str]):
        """記事タイプに応じたメインビジュアル要素を追加"""
        width, height = img.size
        
        if style == 'sound_waves':
            self._draw_sound_waves(img, draw, colors)
        elif style == 'frequency_bars':
            self._draw_frequency_bars(img, draw, colors)
        elif style == 'circular_visualizer':
            self._draw_circular_visualizer(img, draw, colors)
        elif style == 'voice_pattern':
            self._draw_voice_pattern(img, draw, colors)
        elif style == 'code_blocks':
            self._draw_code_blocks(img, draw, colors)
        elif style == 'data_stream':
            self._draw_data_stream(img, draw, colors)
        elif style == 'split_design':
            self._draw_split_design(img, draw, colors)
        elif style == 'circuit_board':
            self._draw_circuit_pattern(img, draw, colors)
    
    def _draw_sound_waves(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """音波パターンを描画"""
        width, height = img.size
        wave_count = 5
        
        for i in range(wave_count):
            wave_y = height * (0.3 + i * 0.1)
            amplitude = 30 + i * 10
            frequency = 0.02 - i * 0.002
            
            points = []
            for x in range(0, width, 2):
                y = wave_y + math.sin(x * frequency) * amplitude
                points.append((x, y))
            
            # グロウ効果のために複数回描画
            for offset in range(3, 0, -1):
                alpha = 50 + offset * 30
                draw.line(points, fill=self._hex_to_rgb(colors['primary']) + (alpha,), width=offset*2)
    
    def _draw_frequency_bars(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """周波数バーを描画"""
        width, height = img.size
        bar_count = 60
        bar_width = width // bar_count
        
        for i in range(bar_count):
            # ランダムな高さ（音楽のビジュアライザー風）
            bar_height = random.randint(50, 300)
            x = i * bar_width
            y = height // 2
            
            # グラデーションカラー
            color_ratio = i / bar_count
            color = self._interpolate_colors(colors['primary'], colors['secondary'], color_ratio)
            
            # バーを描画（上下対称）
            draw.rectangle(
                [(x, y - bar_height//2), (x + bar_width - 2, y + bar_height//2)],
                fill=self._hex_to_rgb(color) + (180,)
            )
    
    def _draw_circular_visualizer(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """円形ビジュアライザーを描画"""
        width, height = img.size
        center_x, center_y = width // 2, height // 2
        
        # 同心円を描画
        for i in range(10):
            radius = 50 + i * 30
            alpha = 150 - i * 10
            
            # 円を描画
            draw.ellipse(
                [(center_x - radius, center_y - radius), 
                 (center_x + radius, center_y + radius)],
                outline=self._hex_to_rgb(colors['primary']) + (alpha,),
                width=2
            )
            
            # 放射状の線
            if i % 2 == 0:
                for angle in range(0, 360, 30):
                    rad = math.radians(angle)
                    x1 = center_x + radius * math.cos(rad)
                    y1 = center_y + radius * math.sin(rad)
                    x2 = center_x + (radius + 20) * math.cos(rad)
                    y2 = center_y + (radius + 20) * math.sin(rad)
                    
                    draw.line(
                        [(x1, y1), (x2, y2)],
                        fill=self._hex_to_rgb(colors['accent']) + (alpha,),
                        width=2
                    )
    
    def _draw_voice_pattern(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """音声パターンを描画"""
        width, height = img.size
        
        # 中央に大きな波形
        center_y = height // 2
        
        for x in range(0, width, 3):
            # 複数の周波数を重ねる
            y1 = math.sin(x * 0.01) * 50
            y2 = math.sin(x * 0.02) * 30
            y3 = math.sin(x * 0.03) * 20
            
            y_total = center_y + y1 + y2 + y3
            
            # 垂直線で波形を表現
            draw.line(
                [(x, center_y), (x, y_total)],
                fill=self._hex_to_rgb(colors['primary']) + (150,),
                width=2
            )
    
    def _draw_code_blocks(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """コードブロック風のデザイン"""
        width, height = img.size
        
        # コードライン風の要素
        line_height = 30
        indent_levels = [0, 20, 40, 60]
        
        for i in range(height // line_height):
            y = i * line_height + 20
            indent = random.choice(indent_levels)
            line_length = random.randint(100, 400)
            
            # コードライン
            draw.rectangle(
                [(50 + indent, y), (50 + indent + line_length, y + 15)],
                fill=self._hex_to_rgb(colors['primary']) + (100,)
            )
            
            # シンタックスハイライト風
            if random.random() > 0.7:
                highlight_start = 50 + indent + random.randint(0, line_length // 2)
                highlight_length = random.randint(30, 100)
                draw.rectangle(
                    [(highlight_start, y), (highlight_start + highlight_length, y + 15)],
                    fill=self._hex_to_rgb(colors['accent']) + (150,)
                )
    
    def _draw_data_stream(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """データストリーム効果"""
        width, height = img.size
        
        # 垂直に流れるデータ
        for x in range(0, width, 40):
            stream_length = random.randint(100, 400)
            start_y = random.randint(-200, height)
            
            for y in range(start_y, start_y + stream_length, 20):
                if 0 <= y < height:
                    # バイナリ風テキスト
                    text = random.choice(['01', '10', '11', '00'])
                    alpha = 255 - abs(y - start_y - stream_length//2) * 2
                    
                    try:
                        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
                    except:
                        font = ImageFont.load_default()
                    
                    draw.text(
                        (x, y), text, 
                        font=font,
                        fill=self._hex_to_rgb(colors['primary']) + (max(0, alpha),)
                    )
    
    def _draw_split_design(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """分割デザイン（比較記事用）"""
        width, height = img.size
        
        # 斜めの分割線
        points = [(width//2 - 50, 0), (width//2 + 50, height)]
        draw.polygon(
            [(0, 0), points[0], points[1], (0, height)],
            fill=self._hex_to_rgb(colors['primary']) + (50,)
        )
        draw.polygon(
            [points[0], (width, 0), (width, height), points[1]],
            fill=self._hex_to_rgb(colors['secondary']) + (50,)
        )
        
        # 中央の光る線
        for offset in range(-2, 3):
            draw.line(
                [(width//2 + offset - 50, 0), (width//2 + offset + 50, height)],
                fill=self._hex_to_rgb(colors['glow']) + (200 - abs(offset) * 40,),
                width=3
            )
    
    def _draw_circuit_pattern(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """回路基板パターン"""
        width, height = img.size
        
        # グリッド上にノードを配置
        grid_size = 80
        nodes = []
        
        for x in range(grid_size, width - grid_size, grid_size):
            for y in range(grid_size, height - grid_size, grid_size):
                if random.random() > 0.3:
                    nodes.append((x, y))
        
        # ノード間を接続
        for i, node1 in enumerate(nodes):
            # 近くのノードと接続
            for node2 in nodes[i+1:]:
                distance = math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)
                if distance < grid_size * 1.5 and random.random() > 0.5:
                    # 直角の経路
                    mid_x = node1[0]
                    mid_y = node2[1]
                    
                    draw.line([node1, (mid_x, mid_y)], 
                             fill=self._hex_to_rgb(colors['primary']) + (100,), width=2)
                    draw.line([(mid_x, mid_y), node2], 
                             fill=self._hex_to_rgb(colors['primary']) + (100,), width=2)
        
        # ノードを描画
        for node in nodes:
            draw.ellipse(
                [(node[0] - 5, node[1] - 5), (node[0] + 5, node[1] + 5)],
                fill=self._hex_to_rgb(colors['accent']),
                outline=self._hex_to_rgb(colors['glow'])
            )
    
    def _add_geometric_patterns(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """幾何学的なパターンを追加"""
        width, height = img.size
        
        # 六角形パターン
        hex_size = 30
        for x in range(0, width, hex_size * 3):
            for y in range(0, height, hex_size * 2):
                if random.random() > 0.7:
                    self._draw_hexagon(
                        draw, x + (hex_size * 1.5 if y % (hex_size * 4) else 0), 
                        y, hex_size,
                        self._hex_to_rgb(colors['accent']) + (50,)
                    )
        
        # 三角形の装飾
        for _ in range(5):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(20, 60)
            
            points = [
                (x, y - size),
                (x - size * 0.866, y + size * 0.5),
                (x + size * 0.866, y + size * 0.5)
            ]
            
            draw.polygon(points, outline=self._hex_to_rgb(colors['primary']) + (100,), width=2)
    
    def _draw_hexagon(self, draw: ImageDraw.Draw, x: float, y: float, size: float, color: Tuple):
        """六角形を描画"""
        angles = [60 * i for i in range(6)]
        points = []
        
        for angle in angles:
            rad = math.radians(angle)
            px = x + size * math.cos(rad)
            py = y + size * math.sin(rad)
            points.append((px, py))
        
        draw.polygon(points, outline=color, width=1)
    
    def _add_glow_effect(self, img: Image.Image, colors: Dict[str, str]) -> Image.Image:
        """グロウ効果を追加"""
        # 明るい部分を抽出
        bright = img.copy()
        enhancer = ImageEnhance.Brightness(bright)
        bright = enhancer.enhance(2.0)
        
        # ブラー効果
        glow = bright.filter(ImageFilter.GaussianBlur(radius=10))
        
        # 元画像と合成
        return Image.blend(img, glow, 0.3)
    
    def _add_modern_text(self, img: Image.Image, draw: ImageDraw.Draw, 
                        title: str, colors: Dict[str, str], tool_name: Optional[str]):
        """確実に見えるテキストレイアウト"""
        width, height = img.size
        
        # フォント設定
        try:
            # タイトル用フォント（太め）
            title_font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 52)
            tag_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
            logger.info("日本語フォントを読み込みました")
        except Exception as e:
            logger.warning(f"日本語フォント読み込み失敗: {e}")
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 52)
                tag_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 20)
                logger.info("代替フォント(Arial)を読み込みました")
            except:
                title_font = ImageFont.load_default()
                tag_font = ImageFont.load_default()
                logger.warning("デフォルトフォントを使用します")
        
        # タイトルの処理（日付除去）
        import re
        title_text = re.sub(r'【.+?】', '', title).strip()
        
        # タイトルを折り返し
        title_lines = self._wrap_text(title_text, title_font, width - 120)
        logger.info(f"タイトル行数: {len(title_lines)}, 行: {title_lines}")
        
        # テキストエリアの背景矩形を描画（可読性確保）
        line_height = 70
        total_height = len(title_lines) * line_height
        y_start = (height - total_height) // 2
        
        # 背景矩形の計算
        max_width = 0
        for line in title_lines:
            bbox = title_font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            max_width = max(max_width, line_width)
        
        # 半透明の黒い背景矩形
        padding = 30
        bg_x1 = (width - max_width) // 2 - padding
        bg_y1 = y_start - padding
        bg_x2 = (width + max_width) // 2 + padding
        bg_y2 = y_start + total_height + padding
        
        # 背景矩形を描画
        draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], 
                      fill=(0, 0, 0, 200), 
                      outline=self._hex_to_rgb(colors['primary']) + (150,), 
                      width=3)
        
        logger.info(f"背景矩形描画: ({bg_x1},{bg_y1}) to ({bg_x2},{bg_y2})")
        
        # タイトルテキストを描画
        y_offset = y_start
        for i, line in enumerate(title_lines):
            if not line.strip():
                continue
                
            try:
                bbox = title_font.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x_position = (width - text_width) // 2
                
                logger.info(f"行{i+1}: '{line}', x={x_position}, y={y_offset}")
                
                # ネオングロウ効果
                for glow_size in [8, 6, 4, 2]:
                    glow_color = self._hex_to_rgb(colors['glow']) + (50,)
                    for dx in range(-glow_size, glow_size+1):
                        for dy in range(-glow_size, glow_size+1):
                            if dx*dx + dy*dy <= glow_size*glow_size:
                                draw.text((x_position + dx, y_offset + dy), line, 
                                        font=title_font, fill=glow_color)
                
                # メインテキスト（明るい白）
                draw.text((x_position, y_offset), line, font=title_font, fill=(255, 255, 255, 255))
                
                y_offset += line_height
                
            except Exception as e:
                logger.error(f"テキスト描画エラー: {e}")
                continue
        
        # ツール名タグ（左上）
        if tool_name:
            tag_text = f"#{tool_name.upper()}"
            tag_x, tag_y = 40, 40
            
            # タグ背景
            bbox = tag_font.getbbox(tag_text)
            tag_width = bbox[2] - bbox[0] + 20
            tag_height = bbox[3] - bbox[1] + 10
            
            draw.rectangle(
                [(tag_x - 10, tag_y - 5), (tag_x + tag_width, tag_y + tag_height)],
                fill=self._hex_to_rgb(colors['primary']) + (100,),
                outline=self._hex_to_rgb(colors['glow']),
                width=2
            )
            
            draw.text((tag_x, tag_y), tag_text, font=tag_font, fill=colors['text'])
        
        # AI MELODY KOBO（右下）
        brand_text = "AI MELODY KOBO"
        bbox = tag_font.getbbox(brand_text)
        brand_width = bbox[2] - bbox[0]
        
        brand_x = width - brand_width - 40
        brand_y = height - 60
        
        # ブランド名にもグロウ効果
        for offset in range(3, 0, -1):
            glow_alpha = 20 + offset * 10
            draw.text(
                (brand_x, brand_y), brand_text, 
                font=tag_font, 
                fill=self._hex_to_rgb(colors['secondary']) + (glow_alpha,)
            )
        
        draw.text((brand_x, brand_y), brand_text, font=tag_font, fill=colors['text'])
    
    def _add_decorative_accents(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """装飾的なアクセントを追加"""
        width, height = img.size
        
        # コーナーの装飾
        corner_size = 100
        corner_width = 3
        
        # 左上
        draw.line([(0, corner_size), (0, 0), (corner_size, 0)], 
                 fill=self._hex_to_rgb(colors['accent']), width=corner_width)
        
        # 右上
        draw.line([(width - corner_size, 0), (width, 0), (width, corner_size)], 
                 fill=self._hex_to_rgb(colors['accent']), width=corner_width)
        
        # 左下
        draw.line([(0, height - corner_size), (0, height), (corner_size, height)], 
                 fill=self._hex_to_rgb(colors['accent']), width=corner_width)
        
        # 右下
        draw.line([(width - corner_size, height), (width, height), (width, height - corner_size)], 
                 fill=self._hex_to_rgb(colors['accent']), width=corner_width)
        
        # ランダムな光の粒子
        for _ in range(20):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            alpha = random.randint(100, 255)
            
            draw.ellipse(
                [(x - size, y - size), (x + size, y + size)],
                fill=self._hex_to_rgb(colors['glow']) + (alpha,)
            )
    
    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> List[str]:
        """テキストを折り返し"""
        lines = []
        
        # 特定の区切り文字で優先的に改行
        preferred_breaks = ['ガイド - ', 'ガイド-', 'ガイド ']
        
        # 優先改行ポイントをチェック
        for break_point in preferred_breaks:
            if break_point in text:
                parts = text.split(break_point, 1)
                if len(parts) == 2:
                    first_part = parts[0] + break_point.strip(' -')
                    second_part = parts[1]
                    
                    # 両方が適切な長さかチェック
                    bbox1 = font.getbbox(first_part)
                    bbox2 = font.getbbox(second_part)
                    
                    if (bbox1[2] - bbox1[0] <= max_width and 
                        bbox2[2] - bbox2[0] <= max_width):
                        return [first_part, second_part]
        
        # 通常の文字単位折り返し
        current_line = ""
        for char in text:
            test_line = current_line + char
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
        
        if current_line:
            lines.append(current_line)
        
        # 最大2行に制限
        if len(lines) > 2:
            lines = lines[:2]
            lines[1] = lines[1][:-3] + "..."
        
        return lines
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """16進数カラーをRGBに変換"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _interpolate_colors(self, color1: str, color2: str, ratio: float) -> str:
        """2つの色を補間"""
        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)
        
        r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * ratio)
        g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * ratio)
        b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * ratio)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def generate_from_article_data(self, article_data: Dict, 
                                  article_type: str = 'general',
                                  tool_name: Optional[str] = None) -> bytes:
        """記事データから自動的に画像を生成"""
        title = article_data.get('title', 'AI Music Article')
        tags = article_data.get('tags', [])
        
        return self.generate_thumbnail(
            title=title,
            article_type=article_type,
            tool_name=tool_name,
            keywords=tags
        )