"""
Content Image Generator for AI Melody Kobo
記事内の画像を自動生成
"""

import os
import logging
from typing import Dict, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
from pathlib import Path
import random

logger = logging.getLogger(__name__)


class ContentImageGenerator:
    """記事内コンテンツ画像を生成するクラス"""
    
    def __init__(self):
        """画像生成器の初期化"""
        # デフォルトの画像サイズ
        self.default_size = (800, 450)  # 16:9比率
        
        # カラーテーマ
        self.color_themes = {
            'modern': {
                'background': '#0A0A0F',
                'primary': '#00D4FF',
                'secondary': '#FF0080',
                'accent': '#00FF88',
                'text': '#FFFFFF'
            },
            'tech': {
                'background': '#0D1117',
                'primary': '#00FF41',
                'secondary': '#FF1744',
                'accent': '#FFEA00',
                'text': '#FFFFFF'
            },
            'creative': {
                'background': '#1A0E0A',
                'primary': '#FF6B35',
                'secondary': '#F7931E',
                'accent': '#FF006E',
                'text': '#FFFFFF'
            }
        }
    
    def generate_content_image(self, 
                             description: str,
                             style: str = 'modern',
                             article_context: Optional[str] = None) -> bytes:
        """
        記事内容に応じた画像を生成
        
        Args:
            description: 画像の説明（例：「AIが音楽を生成している様子」）
            style: 画像スタイル
            article_context: 記事のコンテキスト
            
        Returns:
            画像データ（bytes）
        """
        # カラーテーマを選択
        colors = self.color_themes.get(style, self.color_themes['modern'])
        
        # 画像を作成
        img = Image.new('RGB', self.default_size, colors['background'])
        draw = ImageDraw.Draw(img)
        
        # 背景にグラデーション効果
        self._add_gradient_background(img, draw, colors)
        
        # コンテンツに応じたビジュアル要素を追加
        if 'インターフェース' in description or 'UI' in description:
            self._draw_interface_mockup(img, draw, colors)
        elif 'グラフ' in description or 'チャート' in description:
            self._draw_chart(img, draw, colors)
        elif '波形' in description or 'ウェーブ' in description:
            self._draw_waveform(img, draw, colors)
        elif 'アイコン' in description or 'ボタン' in description:
            self._draw_icons(img, draw, colors)
        else:
            # デフォルト：幾何学的パターン
            self._draw_geometric_pattern(img, draw, colors)
        
        # 説明テキストを追加
        self._add_description_text(img, draw, description, colors)
        
        # バイトデータに変換
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG', optimize=True, quality=95)
        img_bytes.seek(0)
        
        return img_bytes.getvalue()
    
    def _add_gradient_background(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict):
        """グラデーション背景を追加"""
        width, height = img.size
        
        # 縦方向のグラデーション
        for y in range(height):
            ratio = y / height
            # 背景色を少し明るくする
            r = int(int(colors['background'][1:3], 16) * (1 + ratio * 0.3))
            g = int(int(colors['background'][3:5], 16) * (1 + ratio * 0.3))
            b = int(int(colors['background'][5:7], 16) * (1 + ratio * 0.3))
            
            r = min(255, r)
            g = min(255, g)
            b = min(255, b)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    def _draw_interface_mockup(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict):
        """インターフェースモックアップを描画"""
        width, height = img.size
        
        # ウィンドウ枠
        window_x = width // 4
        window_y = height // 4
        window_w = width // 2
        window_h = height // 2
        
        # ウィンドウ背景
        draw.rectangle(
            [(window_x, window_y), (window_x + window_w, window_y + window_h)],
            fill=(20, 20, 30),
            outline=colors['primary']
        )
        
        # タイトルバー
        draw.rectangle(
            [(window_x, window_y), (window_x + window_w, window_y + 30)],
            fill=colors['primary']
        )
        
        # ボタンを配置
        button_y = window_y + window_h // 2
        for i in range(3):
            button_x = window_x + 20 + i * 120
            draw.rectangle(
                [(button_x, button_y), (button_x + 100, button_y + 40)],
                fill=colors['accent'],
                outline=colors['primary']
            )
    
    def _draw_chart(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict):
        """チャートを描画"""
        width, height = img.size
        
        # 棒グラフ
        bar_count = 8
        bar_width = width // (bar_count * 2)
        max_height = height * 0.6
        
        for i in range(bar_count):
            bar_height = random.randint(int(max_height * 0.3), int(max_height))
            x = width // 4 + i * bar_width * 1.5
            y = height * 0.7
            
            # バーを描画
            draw.rectangle(
                [(x, y - bar_height), (x + bar_width, y)],
                fill=colors['primary'] if i % 2 == 0 else colors['secondary']
            )
    
    def _draw_waveform(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict):
        """波形を描画"""
        width, height = img.size
        center_y = height // 2
        
        # 波形データを生成
        points = []
        for x in range(0, width, 2):
            # 複数の周波数を組み合わせ
            y = center_y + int(
                30 * random.random() * (1 + 0.5 * random.random()) +
                20 * random.random() * (1 + 0.3 * random.random())
            )
            points.append((x, y))
        
        # 上下対称の波形
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            # 上側
            draw.line([(x1, y1), (x2, y2)], fill=colors['primary'], width=2)
            # 下側（対称）
            draw.line(
                [(x1, center_y - (y1 - center_y)), 
                 (x2, center_y - (y2 - center_y))],
                fill=colors['secondary'], width=2
            )
    
    def _draw_icons(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict):
        """アイコンを描画"""
        width, height = img.size
        
        # 3x3のグリッドでアイコンを配置
        icon_size = 60
        spacing = 80
        start_x = (width - spacing * 2) // 2
        start_y = (height - spacing * 2) // 2
        
        for i in range(3):
            for j in range(3):
                x = start_x + j * spacing
                y = start_y + i * spacing
                
                # ランダムな形状
                shape = random.choice(['circle', 'square', 'triangle'])
                color = random.choice([colors['primary'], colors['secondary'], colors['accent']])
                
                if shape == 'circle':
                    draw.ellipse(
                        [(x, y), (x + icon_size, y + icon_size)],
                        fill=color
                    )
                elif shape == 'square':
                    draw.rectangle(
                        [(x, y), (x + icon_size, y + icon_size)],
                        fill=color
                    )
                else:  # triangle
                    points = [
                        (x + icon_size // 2, y),
                        (x, y + icon_size),
                        (x + icon_size, y + icon_size)
                    ]
                    draw.polygon(points, fill=color)
    
    def _draw_geometric_pattern(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict):
        """幾何学的パターンを描画"""
        width, height = img.size
        
        # ランダムな円を配置
        for _ in range(15):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(20, 100)
            alpha = random.randint(30, 150)
            
            # 半透明の円を描画
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            color = random.choice([colors['primary'], colors['secondary'], colors['accent']])
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            
            overlay_draw.ellipse(
                [(x - radius, y - radius), (x + radius, y + radius)],
                fill=rgb + (alpha,)
            )
            
            # 元画像に合成
            img.paste(overlay, (0, 0), overlay)
    
    def _add_description_text(self, img: Image.Image, draw: ImageDraw.Draw, 
                            description: str, colors: Dict):
        """説明テキストを追加"""
        width, height = img.size
        
        # フォント設定
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        except:
            font = ImageFont.load_default()
        
        # テキストボックスの背景
        text_height = 40
        draw.rectangle(
            [(0, height - text_height), (width, height)],
            fill=(0, 0, 0, 180)
        )
        
        # テキストを中央に配置
        bbox = font.getbbox(description)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        text_y = height - text_height + 10
        
        draw.text((text_x, text_y), description, font=font, fill=colors['text'])