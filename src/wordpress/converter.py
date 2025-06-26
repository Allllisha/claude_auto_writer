"""
Markdown to HTML Converter
AI Melody Kobo - Markdown記事をWordPress用HTMLに変換
"""

import re
import markdown
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ArticleConverter:
    """Markdown記事をWordPress用に変換するクラス"""
    
    def __init__(self):
        """コンバーターの初期化"""
        # Markdown拡張機能の設定
        self.md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.tables',
                'markdown.extensions.toc',
                'markdown.extensions.meta',
                'markdown.extensions.md_in_html'
            ],
            extension_configs={
                'markdown.extensions.codehilite': {'css_class': 'highlight'},
                'markdown.extensions.extra': {'markdown_in_html_blocks': True}
            }
        )
        
    def parse_article(self, markdown_content: str) -> Dict:
        """
        Markdown記事を解析してWordPress用のデータに変換
        
        Args:
            markdown_content: Markdown形式の記事内容
            
        Returns:
            パースされた記事データ
        """
        # タイトルを抽出（最初のH1）
        title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
        title = title_match.group(1) if title_match else "無題"
        
        # タイトル以降のコンテンツを取得
        content_without_title = re.sub(r'^#\s+.+$', '', markdown_content, count=1, flags=re.MULTILINE).strip()
        
        # WordPressタグとメタディスクリプションを本文から除去
        content_without_meta = self._remove_meta_information(content_without_title)
        
        # HTMLに変換
        html_content = self.md.convert(content_without_meta)
        
        # 画像・動画挿入指示を処理
        html_content = self._process_media_instructions(html_content)
        
        # リンク指示を処理
        html_content = self._process_link_instructions(html_content)
        
        # CTAブロックを装飾
        html_content = self._enhance_cta_blocks(html_content)
        
        # メタ情報の抽出
        tags = self._extract_tags(markdown_content)
        meta_description = self._extract_meta_description(markdown_content)
        
        # 抜粋の生成
        excerpt = self._generate_excerpt(content_without_meta)
        
        return {
            'title': title,
            'content': html_content,
            'tags': tags,
            'meta_description': meta_description,
            'excerpt': excerpt,
            'original_markdown': markdown_content
        }
    
    def _process_media_instructions(self, html_content: str) -> str:
        """画像・動画挿入指示を処理"""
        # [画像挿入指示: description] をプレースホルダーに変換
        pattern = r'\[画像挿入指示:\s*([^\]]+)\]'
        replacement = r'<!-- IMAGE_PLACEHOLDER: \1 -->\n<div class="image-placeholder" style="background: #f0f0f0; padding: 20px; text-align: center; margin: 20px 0;">📷 画像: \1</div>'
        html_content = re.sub(pattern, replacement, html_content)
        
        # [動画挿入指示: description] をプレースホルダーに変換
        pattern = r'\[動画挿入指示:\s*([^\]]+)\]'
        replacement = r'<!-- VIDEO_PLACEHOLDER: \1 -->\n<div class="video-placeholder" style="background: #f0f0f0; padding: 20px; text-align: center; margin: 20px 0;">🎥 動画: \1</div>'
        html_content = re.sub(pattern, replacement, html_content)
        
        return html_content
    
    def _process_link_instructions(self, html_content: str) -> str:
        """リンク指示を処理"""
        # [内部リンク: title] を処理
        pattern = r'\[内部リンク:\s*([^\]]+)\]'
        replacement = r'<a href="#" class="internal-link-placeholder" data-link-title="\1">\1</a>'
        html_content = re.sub(pattern, replacement, html_content)
        
        # [外部リンク: site name] を処理
        pattern = r'\[外部リンク:\s*([^\]]+)\]'
        replacement = r'<a href="#" class="external-link-placeholder" data-site-name="\1" target="_blank" rel="noopener noreferrer">\1</a>'
        html_content = re.sub(pattern, replacement, html_content)
        
        return html_content
    
    def _enhance_cta_blocks(self, html_content: str) -> str:
        """CTAブロックを装飾"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # HR要素で囲まれたCTAセクションを検出
        hrs = soup.find_all('hr')
        for i in range(0, len(hrs) - 1, 2):
            cta_content = []
            current = hrs[i].next_sibling
            
            while current and current != hrs[i + 1]:
                if hasattr(current, 'name'):
                    cta_content.append(str(current))
                current = current.next_sibling
            
            if cta_content and 'AI Melody Kobo' in ' '.join(cta_content):
                # CTAブロックをdivで囲む
                cta_div = soup.new_tag('div', attrs={
                    'class': 'cta-block',
                    'style': 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; margin: 40px 0; border-radius: 10px; text-align: center;'
                })
                
                # CTAコンテンツを新しいdivに移動
                for elem_str in cta_content:
                    elem_soup = BeautifulSoup(elem_str, 'html.parser')
                    for elem in elem_soup:
                        if hasattr(elem, 'name'):
                            # スタイルを調整
                            if elem.name == 'h3':
                                elem['style'] = 'color: white; margin-bottom: 15px;'
                            elif elem.name == 'p':
                                elem['style'] = 'color: white; margin-bottom: 20px;'
                            elif elem.name == 'a':
                                elem['style'] = 'background: white; color: #667eea; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold; margin-top: 10px;'
                            cta_div.append(elem)
                
                # 元のコンテンツを削除してCTAブロックを挿入
                current = hrs[i].next_sibling
                while current and current != hrs[i + 1]:
                    next_sibling = current.next_sibling
                    if hasattr(current, 'extract'):
                        current.extract()
                    current = next_sibling
                
                hrs[i].replace_with(cta_div)
                hrs[i + 1].extract()
        
        return str(soup)
    
    def _extract_tags(self, markdown_content: str) -> List[str]:
        """記事からWordPressタグを抽出"""
        # **WordPressタグ:** セクションを探す
        tag_match = re.search(r'\*\*WordPressタグ:\*\*\s*(.+)$', markdown_content, re.MULTILINE)
        if tag_match:
            tags_text = tag_match.group(1)
            # #を削除してタグのリストを作成
            tags = [tag.strip().replace('#', '') for tag in tags_text.split() if tag.strip()]
            return tags
        return []
    
    def _extract_meta_description(self, markdown_content: str) -> Optional[str]:
        """メタディスクリプションを抽出"""
        meta_match = re.search(r'\*\*メタディスクリプション:\*\*\s*(.+)$', markdown_content, re.MULTILINE)
        if meta_match:
            return meta_match.group(1).strip()
        return None
    
    def _generate_excerpt(self, content: str) -> str:
        """記事の抜粋を生成"""
        # Markdownを一時的にHTMLに変換してテキストを抽出
        html = self.md.convert(content)
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        
        # 最初の200文字を抜粋として使用
        excerpt = text[:200].strip()
        if len(text) > 200:
            excerpt += '...'
        
        return excerpt
    
    def _remove_meta_information(self, content: str) -> str:
        """WordPressタグとメタディスクリプションを本文から除去"""
        # WordPressタグセクションを除去
        content = re.sub(r'\*\*WordPressタグ:\*\*.*?(?=\n\n|\n\*\*|\Z)', '', content, flags=re.DOTALL)
        
        # メタディスクリプションセクションを除去
        content = re.sub(r'\*\*メタディスクリプション:\*\*.*?(?=\n\n|\n\*\*|\Z)', '', content, flags=re.DOTALL)
        
        # 連続する改行を整理
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()
    
    def convert_to_wordpress_html(self, markdown_content: str) -> Dict:
        """
        Markdown記事をWordPress投稿用のデータに変換
        
        Args:
            markdown_content: Markdown形式の記事
            
        Returns:
            WordPress投稿用のデータ辞書
        """
        try:
            article_data = self.parse_article(markdown_content)
            
            # WordPress用にHTMLを最適化
            article_data['content'] = self._optimize_for_wordpress(article_data['content'])
            
            return article_data
            
        except Exception as e:
            logger.error(f"記事変換エラー: {str(e)}")
            raise
    
    def _optimize_for_wordpress(self, html_content: str) -> str:
        """WordPress用にHTMLを最適化"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # コードブロックにWordPressのクラスを追加
        for pre in soup.find_all('pre'):
            pre['class'] = pre.get('class', []) + ['wp-block-code']
        
        # テーブルにWordPressのクラスを追加
        for table in soup.find_all('table'):
            table['class'] = table.get('class', []) + ['wp-block-table']
        
        # 画像プレースホルダーにWordPressのクラスを追加
        for div in soup.find_all('div', class_='image-placeholder'):
            div['class'] = div.get('class', []) + ['wp-block-image']
        
        # 画像のサイズを最適化（最大幅を設定）
        for img in soup.find_all('img'):
            # 既存のstyle属性を保持しつつ、max-widthを設定
            current_style = img.get('style', '')
            if 'max-width' not in current_style:
                img['style'] = 'max-width: 800px; height: auto; display: block; margin: 20px auto;'
            # WordPressのレスポンシブクラスを追加
            img['class'] = img.get('class', []) + ['aligncenter', 'size-large']
        
        return str(soup)