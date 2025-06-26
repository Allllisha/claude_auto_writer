# AI Melody Kobo - WordPress Article Generator

AI音楽に関する記事を自動生成し、WordPressに投稿するシステム

## 概要

このプロジェクトは、AI音楽ツール（Suno、Udio、MusicGen、Stable Audio、AIVA等）に関する高品質な日本語記事を自動生成し、WordPress REST APIを使用して投稿するPythonアプリケーションです。

## 主な機能

- **記事自動生成**: AI音楽に関する様々なトピックの記事を自動生成
- **タイトルと内容の一貫性**: ContentStrategyパターンでタイトルに応じた適切な内容を生成
- **SEO最適化**: キーワード自然統合、適切な見出し構造
- **サムネイル自動生成**: 記事ごとにモダンなAIテーマのサムネイルを生成
- **記事内画像**: 記事内容に応じた説明画像を自動生成・挿入
- **ニュースレターCTA**: 記事内に効果的なCTAボタンを配置
- **WordPress連携**: REST APIを使用した自動投稿

## プロジェクト構造

```
claude_writer/
├── src/
│   ├── article_generator/
│   │   ├── ai_client.py          # AI API統合
│   │   ├── content_strategy.py   # コンテンツ戦略
│   │   └── smart_content_generator.py # 記事生成
│   ├── wordpress/
│   │   └── api_client.py         # WordPress API
│   └── media/
│       ├── modern_thumbnail_generator.py  # サムネイル生成
│       └── content_image_generator.py     # 記事内画像生成
├── config/
│   └── settings.py               # 設定管理
├── scripts/
│   ├── generate_5_production_articles.py  # 本番記事生成
│   └── post_articles_with_cta_html.py    # CTA付き投稿
└── CLAUDE.md                     # AIアシスタント向けガイド
```

## セットアップ

1. **環境変数の設定**

`.env`ファイルを作成し、以下の変数を設定：

```env
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_app_password
ANTHROPIC_API_KEY=your_api_key  # オプション
```

2. **依存関係のインストール**

```bash
pip install -r requirements.txt
```

## 使用方法

### 5記事の本番投稿

```bash
python generate_5_production_articles.py
```

これにより、以下が実行されます：
- 5つの異なるトピックの記事を生成
- 各記事にサムネイルと記事内画像を追加
- ニュースレターCTAを挿入
- WordPress下書きとして投稿

### 個別の記事生成

```python
from src.article_generator.smart_content_generator import SmartContentGenerator

content = SmartContentGenerator.generate_article(
    topic="Suno AIの使い方完全ガイド",
    keywords=["Suno", "AI音楽", "使い方"],
    article_type="tutorial"
)
```

## 記事タイプ

- `beginner_guide`: 初心者向けガイド
- `tool_update`: ツールアップデート情報
- `business`: ビジネス・収益化
- `tutorial`: チュートリアル
- `industry_news`: 業界ニュース
- `comparison`: ツール比較

## 生成される記事の特徴

- **文字数**: 3000〜5000文字
- **構成**: 導入→目次→本文（5-8セクション）→まとめ
- **画像**: サムネイル1枚 + 記事内画像5-8枚
- **CTA**: メルマガ登録ボタン2箇所
- **SEO**: 適切なH2/H3構造、キーワード自然配置

## 注意事項

- WordPress REST APIの有効化が必要
- アプリケーションパスワードの設定が必要
- 画像生成には適切なフォントのインストールが必要

## ライセンス

このプロジェクトは内部使用を目的としています。

## 作成者

AI Melody Kobo開発チーム

---

🤖 Powered by Claude Code