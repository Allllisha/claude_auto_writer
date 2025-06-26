# AI Melody Kobo - Visual Style Guide

## 🎨 カラーパレット

### プライマリカラー
- **ディープブルー**: `#1e3a8a` - メインブランドカラー
- **ネイビー**: `#1e293b` - 代替プライマリカラー

### セカンダリカラー
- **エレクトリックグリーン**: `#10b981` - CTAボタン、成功メッセージ
- **ライトブルー**: `#3b82f6` - リンク、アクセント

### アクセントカラー
- **パープル**: `#8b5cf6` - 特別な要素、AIを表現
- **シアン**: `#06b6d4` - 新着・注目マーク

### ベースカラー
- **背景白**: `#ffffff`
- **背景グレー**: `#f9fafb`
- **ボーダーグレー**: `#e5e7eb`

### テキストカラー
- **見出し**: `#111827`
- **本文**: `#374151`
- **補助テキスト**: `#6b7280`

## 🔤 タイポグラフィ

### フォントファミリー
```css
/* 見出し用 */
font-family: "Noto Sans JP", "Hiragino Kaku Gothic ProN", sans-serif;
font-weight: 700;

/* 本文用 */
font-family: "Noto Sans JP", "Hiragino Sans", Meiryo, sans-serif;
font-weight: 400;

/* コード・技術用語 */
font-family: "Source Code Pro", "Consolas", monospace;
```

### フォントサイズ
- **H1**: 32px (2rem) - ページタイトル
- **H2**: 28px (1.75rem) - 大見出し
- **H3**: 24px (1.5rem) - 中見出し
- **H4**: 20px (1.25rem) - 小見出し
- **本文**: 16px (1rem)
- **キャプション**: 14px (0.875rem)

### 行間・余白
- **本文行間**: 1.8
- **見出し行間**: 1.4
- **段落間**: 24px
- **セクション間**: 48px

## 🎯 UI要素デザイン

### ボタンスタイル

#### プライマリボタン（CTA用）
```css
.btn-primary {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #ffffff;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(16, 185, 129, 0.3);
}
```

#### セカンダリボタン
```css
.btn-secondary {
  background: #ffffff;
  color: #1e3a8a;
  border: 2px solid #1e3a8a;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
}
```

### カードデザイン
```css
.article-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  overflow: hidden;
}

.article-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
}
```

### 見出しデザイン

#### H2見出し（記事内）
```css
.article h2 {
  position: relative;
  padding: 16px 20px;
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  color: #ffffff;
  border-radius: 8px;
  margin: 40px 0 24px;
}

.article h2::before {
  content: "♪";
  margin-right: 8px;
  opacity: 0.8;
}
```

#### H3見出し（記事内）
```css
.article h3 {
  padding-left: 16px;
  border-left: 4px solid #10b981;
  color: #1e3a8a;
  margin: 32px 0 16px;
}
```

## 📱 レスポンシブブレークポイント

- **モバイル**: 320px - 767px
- **タブレット**: 768px - 1023px
- **デスクトップ**: 1024px - 1279px
- **ワイドスクリーン**: 1280px以上

## 🎭 アニメーション

### ホバーエフェクト
- **duration**: 0.3s
- **easing**: ease-in-out
- **transform**: translateY(-2px) または scale(1.02)

### ページ遷移
- **fade-in duration**: 0.5s
- **slide-up duration**: 0.6s

### スクロールアニメーション
- **要素の出現**: opacity 0→1, translateY 20px→0

## 🖼️ ビジュアル要素

### アイコン使用
- **Font Awesome 6**: 基本アイコンセット
- **カスタムSVG**: AI・音楽関連の特別なアイコン

### 画像処理
- **サムネイル比率**: 16:9
- **圧縮形式**: WebP（フォールバックでJPEG）
- **遅延読み込み**: loading="lazy"属性を使用

### グラデーション使用例
```css
/* AIをイメージしたグラデーション */
.ai-gradient {
  background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 50%, #10b981 100%);
}

/* 音楽をイメージしたグラデーション */
.music-gradient {
  background: linear-gradient(45deg, #1e3a8a 0%, #8b5cf6 100%);
}
```

## 📐 レイアウトグリッド

### デスクトップ
- **コンテナ最大幅**: 1200px
- **メインコンテンツ**: 8/12 (66.67%)
- **サイドバー**: 4/12 (33.33%)
- **ガター**: 32px

### モバイル
- **パディング**: 左右16px
- **単一カラムレイアウト**

## 🎪 特別な装飾要素

### ニューモーフィズム風CTAボックス
```css
.cta-box {
  background: #f9fafb;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 
    8px 8px 16px rgba(0, 0, 0, 0.08),
    -8px -8px 16px rgba(255, 255, 255, 0.9);
}
```

### AIメロディ工房らしさの表現
- 音符やウェーブフォームのSVGパターン背景
- AIをイメージした幾何学模様
- グロー効果を使った未来的な表現