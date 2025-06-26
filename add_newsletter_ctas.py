#!/usr/bin/env python3
"""
既存の記事にニュースレターCTAを追加するスクリプト
"""

import os
import glob
import logging
from pathlib import Path

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def add_newsletter_cta(content: str, article_title: str) -> str:
    """記事にニュースレターCTAを追加"""
    
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
    
    # 記事末尾のCTAを追加（WordPressタグの前）
    if "**WordPressタグ:" in content:
        content = content.replace("**WordPressタグ:", final_cta + "\n**WordPressタグ:")
    else:
        # WordPressタグがない場合は最後に追加
        content += "\n" + final_cta
    
    return content

def process_articles():
    """記事を処理"""
    
    logger.info("📝 既存記事にニュースレターCTAを追加します...")
    
    # 入力ディレクトリ
    input_dir = Path("generated_articles")
    output_dir = Path("generated_articles_with_cta")
    output_dir.mkdir(exist_ok=True)
    
    # 記事ファイルを取得
    article_files = sorted(glob.glob(str(input_dir / "*.md")))
    
    if not article_files:
        logger.error("記事ファイルが見つかりません")
        return
    
    logger.info(f"📊 {len(article_files)}件の記事が見つかりました")
    
    success_count = 0
    
    for filepath in article_files:
        filename = os.path.basename(filepath)
        logger.info(f"処理中: {filename}")
        
        try:
            # ファイルを読み込み
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # タイトルを抽出
            lines = content.split('\n')
            title = lines[0].replace('# ', '').strip() if lines else ""
            
            # CTAを追加
            updated_content = add_newsletter_cta(content, title)
            
            # 保存
            output_path = output_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            logger.info(f"   ✅ CTA追加完了: {output_path}")
            success_count += 1
            
        except Exception as e:
            logger.error(f"   ❌ エラー: {str(e)}")
            continue
    
    logger.info(f"\n{'='*60}")
    logger.info("🎉 処理完了！")
    logger.info(f"✅ 成功: {success_count}件")
    logger.info(f"📂 出力先: {output_dir.absolute()}")

if __name__ == "__main__":
    try:
        process_articles()
    except KeyboardInterrupt:
        logger.info("\n⚠️ ユーザーによって中断されました")
    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}", exc_info=True)