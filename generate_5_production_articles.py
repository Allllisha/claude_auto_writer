#!/usr/bin/env python3
"""
本番用の5記事を生成し、サムネイルと記事内画像付きでWordPressに投稿
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import requests
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.article_generator.smart_content_generator import SmartContentGenerator
from src.media.modern_thumbnail_generator import ModernThumbnailGenerator
from src.media.content_image_generator import ContentImageGenerator
from convert_markdown_to_html import convert_markdown_to_html

# WordPress設定
WP_USERNAME = os.getenv('WORDPRESS_USERNAME')
WP_PASSWORD = os.getenv('WORDPRESS_APP_PASSWORD')
WP_URL = 'https://aimelodykobo.com'

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 本番用の5記事トピック
PRODUCTION_TOPICS = [
    {
        'topic': 'AI音楽生成の基礎知識：初心者が知るべき10のポイント',
        'keywords': ['AI音楽', '初心者', '基礎知識', '音楽生成', 'Suno', 'Udio'],
        'article_type': 'beginner_guide'
    },
    {
        'topic': 'Suno V4の新機能徹底解説！従来版との違いと活用法',
        'keywords': ['Suno', 'V4', '新機能', 'アップデート', '音楽生成'],
        'article_type': 'tool_update'
    },
    {
        'topic': 'AI音楽で月10万円稼ぐ！実践的な収益化戦略',
        'keywords': ['AI音楽', '収益化', '副業', 'マネタイズ', 'ビジネス'],
        'article_type': 'business'
    },
    {
        'topic': 'MusicGenとAudioCraftで作る高品質BGM制作ガイド',
        'keywords': ['MusicGen', 'AudioCraft', 'BGM', '音楽制作', 'Meta'],
        'article_type': 'tutorial'
    },
    {
        'topic': '2025年注目のAI音楽スタートアップ企業10選',
        'keywords': ['AI音楽', 'スタートアップ', '2025年', 'トレンド', '企業'],
        'article_type': 'industry_news'
    }
]

def add_newsletter_cta(content: str) -> str:
    """ニュースレターCTAを追加"""
    
    # CTAのフォーマット（記事中用）
    mid_cta = """
---

**💌 無料メルマガ登録で限定特典をゲット！**

AI音楽制作の最新情報や、プロ級のテクニックを無料でお届け！今すぐ登録して、AI音楽制作マスターへの第一歩を踏み出しましょう。

[CTAボタン: 無料メルマガに登録する]

---
"""
    
    # CTAのフォーマット（記事末尾用）
    final_cta = """
---

**💌 無料メルマガ登録で限定特典をゲット！**

AI Melody Koboの無料メルマガで、AI音楽制作の最新トレンドをいち早くキャッチ！実践的なノウハウも満載です。

[CTAボタン: 無料メルマガに登録する]

---
"""
    
    # 記事を行単位で分割
    lines = content.split('\n')
    new_lines = []
    cta_added_mid = False
    section_count = 0
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # H2セクションをカウント
        if line.startswith('## ') and not line.startswith('## 目次') and not line.startswith('## まとめ'):
            section_count += 1
            
            # 3つ目のセクションの後にCTAを挿入
            if section_count == 3 and not cta_added_mid:
                # 次の空行を探す
                for j in range(i + 1, min(i + 10, len(lines))):
                    if j < len(lines) and lines[j].strip() == '':
                        new_lines.append(mid_cta)
                        cta_added_mid = True
                        break
    
    # 記事を再結合
    content = '\n'.join(new_lines)
    
    # 記事末尾のCTAを追加
    if "**WordPressタグ:" in content:
        content = content.replace("**WordPressタグ:", final_cta + "\n**WordPressタグ:")
    
    return content

def convert_cta_to_html(content: str) -> str:
    """CTAボタンをHTML形式に変換"""
    cta_button_html = '''<div class="wp-block-buttons is-content-justification-center is-layout-flex wp-container-core-buttons-layout-1 wp-block-buttons-is-layout-flex">
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="/newsletter" style="background-color:#ff6b35;color:#ffffff;">無料メルマガに登録する</a></div>
</div>'''
    
    content = content.replace('[CTAボタン: 無料メルマガに登録する]', cta_button_html)
    content = content.replace('**💌 無料メルマガ登録で限定特典をゲット！**', 
                            '<h3 style="text-align: center; color: #ff6b35;">💌 無料メルマガ登録で限定特典をゲット！</h3>')
    
    return content

def upload_image_to_wordpress(image_data, filename, alt_text="AI音楽関連画像"):
    """画像をWordPressにアップロード"""
    
    files = {'file': (filename, image_data, 'image/png')}
    
    response = requests.post(
        f"{WP_URL}/index.php?rest_route=/wp/v2/media",
        files=files,
        auth=(WP_USERNAME, WP_PASSWORD),
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    
    if response.status_code == 201:
        media_id = response.json()['id']
        media_url = response.json()['source_url']
        logger.info(f"   ✅ 画像アップロード成功: {filename} (ID={media_id})")
        return media_id, media_url
    else:
        logger.error(f"   ❌ 画像アップロード失敗: {response.status_code}")
        return None, None

def add_images_to_content(content: str, article_title: str, image_generator: ContentImageGenerator) -> str:
    """記事内の画像挿入指示を実際の画像に置換"""
    
    import re
    
    # 画像挿入指示のパターン
    image_pattern = r'\[画像挿入指示: ([^\]]+)\]'
    
    # すべての画像挿入指示を検索
    matches = list(re.finditer(image_pattern, content))
    
    # 後ろから置換（インデックスがずれないように）
    for i, match in enumerate(reversed(matches)):
        instruction = match.group(1)
        logger.info(f"   🎨 画像生成中: {instruction}")
        
        # 画像を生成
        try:
            image_data = image_generator.generate_content_image(
                description=instruction,
                style='modern',
                article_context=article_title
            )
            
            # WordPressにアップロード
            filename = f"content_image_{i+1}.png"
            media_id, media_url = upload_image_to_wordpress(image_data, filename, instruction)
            
            if media_url:
                # HTML形式の画像に置換
                image_html = f'''
<figure class="wp-block-image size-large">
<img src="{media_url}" alt="{instruction}" class="ai-music-image"/>
<figcaption>{instruction}</figcaption>
</figure>'''
                
                content = content[:match.start()] + image_html + content[match.end():]
            
        except Exception as e:
            logger.error(f"   ❌ 画像生成エラー: {str(e)}")
            # エラーの場合はプレースホルダー画像を使用
            placeholder_html = f'''
<figure class="wp-block-image size-large">
<img src="https://via.placeholder.com/800x450/1a1a1a/00ff00?text=AI+Music+Image" alt="{instruction}" class="ai-music-image"/>
<figcaption>{instruction}</figcaption>
</figure>'''
            content = content[:match.start()] + placeholder_html + content[match.end():]
    
    return content

def post_article_with_images(title, content, thumbnail_data, image_generator, status='draft'):
    """サムネイルと記事内画像付きで投稿"""
    
    # サムネイルをアップロード
    thumbnail_id = None
    if thumbnail_data:
        # ASCII文字のみのファイル名を生成
        import hashlib
        title_hash = hashlib.md5(title.encode('utf-8')).hexdigest()[:8]
        thumbnail_filename = f"thumbnail_{title_hash}.png"
        thumbnail_id, _ = upload_image_to_wordpress(thumbnail_data, thumbnail_filename, f"{title}のサムネイル")
    
    # MarkdownをHTMLに変換
    html_content = convert_markdown_to_html(content)
    
    # CTAをHTML形式に変換
    html_content = convert_cta_to_html(html_content)
    
    # 記事内画像を追加
    html_content = add_images_to_content(html_content, title, image_generator)
    
    logger.info("   📝 記事の準備完了（HTML + 画像）")
    
    # WordPress投稿データ
    post_data = {
        'title': title,
        'content': html_content,
        'status': status,
        'categories': [27, 29, 31],  # AI音楽ツール、使い方・始め方、最新情報
        'tags': [],
    }
    
    if thumbnail_id:
        post_data['featured_media'] = thumbnail_id
    
    # 投稿
    try:
        response = requests.post(
            f"{WP_URL}/index.php?rest_route=/wp/v2/posts",
            json=post_data,
            auth=(WP_USERNAME, WP_PASSWORD)
        )
        
        if response.status_code == 201:
            post_id = response.json()['id']
            post_link = response.json()['link']
            logger.info(f"✅ 投稿成功: {title}")
            logger.info(f"   ID: {post_id}")
            logger.info(f"   URL: {post_link}")
            return True
        else:
            logger.error(f"❌ 投稿失敗: {response.status_code}")
            logger.error(f"   エラー: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 投稿エラー: {str(e)}")
        return False

def main():
    """メイン処理"""
    
    logger.info("🚀 本番用5記事の生成と投稿を開始します...")
    
    # ジェネレーター初期化
    thumbnail_generator = ModernThumbnailGenerator()
    image_generator = ContentImageGenerator()
    
    # 出力ディレクトリ
    output_dir = Path("production_articles")
    output_dir.mkdir(exist_ok=True)
    
    success_count = 0
    
    for i, article_config in enumerate(PRODUCTION_TOPICS, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"処理中 {i}/{len(PRODUCTION_TOPICS)}: {article_config['topic']}")
        
        try:
            # 記事を生成
            content = SmartContentGenerator.generate_article(
                topic=article_config['topic'],
                keywords=article_config['keywords'],
                article_type=article_config['article_type']
            )
            
            # ニュースレターCTAを追加
            content = add_newsletter_cta(content)
            
            # ファイルに保存（バックアップ用）
            # 日本語文字を含むファイル名を安全に処理
            import unicodedata
            topic_ascii = unicodedata.normalize('NFKD', article_config['topic'])
            topic_ascii = ''.join([c for c in topic_ascii if ord(c) < 128])
            if not topic_ascii:
                topic_ascii = f"article_{i}"
            safe_filename = f"{i:02d}_{topic_ascii[:30].replace(' ', '_')}.md"
            output_path = output_dir / safe_filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"   📄 記事生成完了: {len(content)}文字")
            
            # タイトルを抽出
            lines = content.split('\n')
            full_title = lines[0].replace('# ', '').strip()
            clean_title = full_title.replace('【2025年最新版】', '').strip()
            
            # ツール名を判定
            tool_name = 'AI音楽'
            for tool in ['Suno', 'Udio', 'MusicGen', 'AudioCraft', 'Stable Audio', 'AIVA']:
                if tool in full_title:
                    tool_name = tool
                    break
            
            # サムネイル生成
            logger.info("   🖼️ サムネイル生成中...")
            thumbnail_data = thumbnail_generator.generate_thumbnail(
                title=clean_title,
                article_type=article_config['article_type'],
                tool_name=tool_name,
                keywords=article_config['keywords']
            )
            
            # 投稿
            if post_article_with_images(full_title, content, thumbnail_data, image_generator):
                success_count += 1
            
        except Exception as e:
            logger.error(f"❌ エラー: {str(e)}")
            continue
    
    # 最終結果
    logger.info(f"\n{'='*60}")
    logger.info("🎉 処理完了！")
    logger.info(f"✅ 成功: {success_count}件")
    logger.info(f"📊 成功率: {success_count/len(PRODUCTION_TOPICS)*100:.1f}%")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️ ユーザーによって中断されました")
    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}", exc_info=True)