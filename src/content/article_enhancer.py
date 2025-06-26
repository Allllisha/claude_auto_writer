"""
Article Enhancer for AI Melody Kobo
記事に画像やリッチコンテンツを追加
"""

import re
import logging
from typing import Dict, List, Optional
from src.media.stock_images import StockImageManager
from src.wordpress.api_client import WordPressClient

logger = logging.getLogger(__name__)


class ArticleEnhancer:
    """記事を強化するクラス"""
    
    def __init__(self):
        """エンハンサーの初期化"""
        self.image_manager = StockImageManager()
        self.wp_client = WordPressClient()
    
    def enhance_article_with_images(self, 
                                  markdown_content: str,
                                  title: str,
                                  keywords: List[str] = None) -> Dict[str, any]:
        """
        記事に画像を追加して強化
        
        Args:
            markdown_content: 元のMarkdown記事
            title: 記事タイトル
            keywords: キーワードリスト
            
        Returns:
            強化された記事データ
        """
        # 画像プレースホルダーを探す
        placeholders = self._find_image_placeholders(markdown_content)
        
        # 必要な画像を取得
        topics = self._extract_topics_from_content(markdown_content, title)
        images = self.image_manager.get_multiple_images(topics, count=len(placeholders))
        
        # 画像をWordPressにアップロード
        uploaded_images = []
        for i, image_data in enumerate(images):
            try:
                # 画像をダウンロード
                local_path = self.image_manager.download_image(
                    image_data['url'],
                    filename=f"article_image_{i+1}.jpg"
                )
                
                # WordPressにアップロード
                with open(local_path, 'rb') as f:
                    media_result = self.wp_client.upload_media(
                        file_data=f.read(),
                        filename=f"ai_music_{i+1}.jpg",
                        title=image_data['alt'],
                        alt_text=image_data['alt'],
                        mime_type='image/jpeg'
                    )
                
                uploaded_images.append({
                    'url': media_result['source_url'],
                    'id': media_result['id'],
                    'alt': image_data['alt'],
                    'description': image_data['description']
                })
                
                logger.info(f"Uploaded image {i+1}: ID {media_result['id']}")
                
            except Exception as e:
                logger.error(f"Failed to upload image {i+1}: {str(e)}")
                # フォールバック: 元のURLを使用
                uploaded_images.append({
                    'url': image_data['url'],
                    'alt': image_data['alt'],
                    'description': image_data['description']
                })
        
        # Markdownの画像プレースホルダーを実際の画像に置換
        enhanced_content = self._replace_placeholders(markdown_content, uploaded_images)
        
        return {
            'content': enhanced_content,
            'images': uploaded_images,
            'image_count': len(uploaded_images)
        }
    
    def _find_image_placeholders(self, content: str) -> List[str]:
        """画像プレースホルダーを検索"""
        # Markdownの画像記法を探す
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        matches = re.findall(pattern, content)
        return matches
    
    def _extract_topics_from_content(self, content: str, title: str) -> List[str]:
        """コンテンツからトピックを抽出"""
        topics = []
        
        # タイトルから
        topics.append(title)
        
        # セクションヘッダーから
        headers = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        topics.extend(headers[:3])  # 最初の3つのヘッダー
        
        # 特定のキーワードから
        if 'Suno' in content:
            topics.append('Suno AI music production')
        if 'Udio' in content:
            topics.append('Udio music creation')
        if 'J-POP' in content or 'j-pop' in content.lower():
            topics.append('Japanese pop music production')
        
        return topics
    
    def _replace_placeholders(self, content: str, images: List[Dict]) -> str:
        """プレースホルダーを実際の画像URLに置換"""
        # 画像プレースホルダーのパターン
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        
        def replace_image(match):
            if images:
                image = images.pop(0)
                alt_text = image['alt']
                url = image['url']
                
                # 画像のみ（説明文なし）
                return f"<img src=\"{url}\" alt=\"{alt_text}\" style=\"max-width: 100%; height: auto; display: block; margin: 20px auto;\">"
            return match.group(0)
        
        # 置換を実行
        enhanced_content = re.sub(pattern, replace_image, content)
        
        return enhanced_content
    
    def add_images_to_sections(self, content: str, title: str) -> str:
        """
        セクションに自動的に画像を追加
        
        Args:
            content: Markdown記事
            title: 記事タイトル
            
        Returns:
            画像が追加された記事
        """
        # 主要なセクションを検出
        sections = self._detect_sections(content)
        
        # 各セクションに適した画像を取得
        section_images = []
        for section in sections[:3]:  # 最初の3セクションに画像を追加
            topic = section['title']
            image_data = self.image_manager.get_image_for_topic(topic, section.get('keywords', []))
            section_images.append({
                'section': section['title'],
                'image': image_data,
                'position': section['position']
            })
        
        # 画像をアップロードして記事に挿入
        enhanced_content = content
        # 画像挿入位置を調整するため、位置情報を更新
        offset = 0
        for i, section_data in enumerate(reversed(section_images)):  # 後ろから処理
            try:
                # 画像をダウンロード
                local_path = self.image_manager.download_image(
                    section_data['image']['url'],
                    filename=f"section_image_{i+1}.jpg"
                )
                
                # WordPressにアップロード
                with open(local_path, 'rb') as f:
                    media_result = self.wp_client.upload_media(
                        file_data=f.read(),
                        filename=f"section_{i+1}.jpg",
                        title=section_data['image']['alt'],
                        alt_text=section_data['image']['alt'],
                        mime_type='image/jpeg'
                    )
                
                # 記事に画像を挿入（説明文なし、画像サイズ指定）
                image_markdown = f"\n\n<img src=\"{media_result['source_url']}\" alt=\"{section_data['image']['alt']}\" style=\"max-width: 100%; height: auto; display: block; margin: 20px auto;\">\n\n"
                
                # セクションタイトルの後の改行を探して、その後に画像を挿入
                newline_pos = enhanced_content.find('\n', section_data['position'])
                if newline_pos != -1:
                    insert_pos = newline_pos + 1
                else:
                    insert_pos = section_data['position']
                
                enhanced_content = (
                    enhanced_content[:insert_pos + offset] +
                    image_markdown +
                    enhanced_content[insert_pos + offset:]
                )
                offset += len(image_markdown)
                
            except Exception as e:
                logger.error(f"Failed to add image to section: {str(e)}")
        
        return enhanced_content
    
    def _detect_sections(self, content: str) -> List[Dict]:
        """記事のセクションを検出"""
        sections = []
        
        # セクションヘッダーのパターン
        pattern = r'^(#{2,3})\s+(.+)$'
        
        for match in re.finditer(pattern, content, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2)
            position = match.end()
            
            # セクションタイトルからキーワードを抽出
            keywords = []
            if 'Suno' in title:
                keywords.append('Suno')
            if 'Udio' in title:
                keywords.append('Udio')
            if 'J-POP' in title:
                keywords.append('J-POP')
            
            sections.append({
                'level': level,
                'title': title,
                'position': position,
                'keywords': keywords
            })
        
        return sections