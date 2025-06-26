# AI Melody Kobo - WordPress Child Theme

AI音楽制作情報サイト「AI Melody Kobo」のためのCocoon子テーマです。

## 概要

このテーマは、AI音楽ツール（特にSuno）に関する情報を発信するブログサイト向けに最適化されています。

### 主な特徴

- **Cocoon親テーマベース**: 高機能な日本製テーマCocoonの子テーマとして開発
- **AI音楽特化デザイン**: ディープブルー×エレクトリックグリーンの配色
- **SEO最適化**: 構造化データ、適切な見出し階層、高速表示
- **メルマガCTA**: 目立つ位置に配置されたニュースレター登録フォーム
- **レスポンシブ対応**: モバイル、タブレット、デスクトップで最適表示

## インストール方法

1. **親テーマのインストール**
   - WordPress管理画面から「Cocoon」テーマをインストール
   - [Cocoon公式サイト](https://wp-cocoon.com/)からダウンロード可能

2. **子テーマのアップロード**
   - `ai-melody-kobo-child`フォルダをZIP圧縮
   - WordPress管理画面 > 外観 > テーマ > 新規追加
   - テーマのアップロードからZIPファイルを選択

3. **有効化**
   - インストール後、子テーマを有効化

## ファイル構成

```
ai-melody-kobo-child/
├── style.css           # メインスタイルシート
├── functions.php       # テーマ機能とカスタマイズ
├── front-page.php      # トップページテンプレート
├── header.php          # ヘッダーテンプレート
├── sidebar.php         # サイドバーテンプレート
├── assets/
│   ├── js/
│   │   └── scripts.js  # カスタムJavaScript
│   ├── images/         # テーマ画像
│   └── css/           # 追加CSS（必要に応じて）
└── README.md          # このファイル
```

## カスタマイズ

### カラーパレット

CSSカスタムプロパティで定義されているため、簡単に変更可能：

```css
:root {
  --primary-color: #1e3a8a;      /* ディープブルー */
  --secondary-color: #10b981;    /* エレクトリックグリーン */
  --accent-color: #8b5cf6;       /* パープル */
}
```

### ウィジェットエリア

- **newsletter-cta**: メルマガ登録専用エリア
- **sidebar-1**: 標準サイドバー（Cocoon継承）

### カスタムショートコード

```
[ai_cta text="ボタンテキスト" url="リンク先"]
[ai_point]ポイントボックスの内容[/ai_point]
[ai_warning]注意ボックスの内容[/ai_warning]
```

## 推奨プラグイン

1. **セキュリティ**: SiteGuard WP Plugin
2. **バックアップ**: UpdraftPlus
3. **SEO**: SEO SIMPLE PACK
4. **高速化**: LiteSpeed Cache（MixHost推奨）
5. **フォーム**: Contact Form 7
6. **人気記事**: WordPress Popular Posts

## メンテナンス

### 定期的な更新

- 親テーマ（Cocoon）の更新確認
- WordPress本体の更新
- プラグインの更新

### パフォーマンス最適化

- 画像の最適化（WebP変換推奨）
- 不要なプラグインの削除
- データベース最適化（月1回）

## ライセンス

GPL v2 or later

## サポート

質問や問題がある場合は、[AI Melody Kobo](https://ai-melody-kobo.com)までお問い合わせください。

## 更新履歴

- **v1.0.0** (2024-06-25): 初回リリース