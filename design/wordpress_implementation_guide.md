# AI Melody Kobo - WordPress実装ガイド

## 🚀 実装手順（ステップバイステップ）

### Phase 1: 基本セットアップ（Day 1）

#### 1. WordPress インストール
```bash
# MixHostでの手順
1. コントロールパネルにログイン
2. 「WordPress簡単インストール」を選択
3. ドメイン選択: ai-melody-kobo.com
4. 管理者情報入力
```

#### 2. 初期設定
- **サイトタイトル**: AI Melody Kobo
- **キャッチフレーズ**: AIクリエイター アリサが探求する、未来の音作り
- **タイムゾーン**: 東京
- **日付形式**: Y年n月j日
- **パーマリンク設定**: /%category%/%postname%/

#### 3. セキュリティ設定（最優先）
```
1. SiteGuard WP Plugin インストール
2. ログインページURL変更
3. 画像認証有効化
4. ログインアラート設定
5. .htaccessに以下を追加:

# XMLRPCアクセス制限
<Files xmlrpc.php>
Order Deny,Allow
Deny from all
</Files>
```

### Phase 2: テーマ設定（Day 1-2）

#### 1. Cocoonテーマインストール
```
外観 > テーマ > 新規追加 > 「Cocoon」検索
親テーマ・子テーマ両方インストール
子テーマを有効化
```

#### 2. Cocoon基本設定
```
Cocoon設定 > 全体
├─ サイトフォント: Noto Sans JP
├─ モバイルメニュー: スライドインタイプ
└─ サイドバー位置: 右

Cocoon設定 > ヘッダー
├─ ヘッダーレイアウト: センターロゴ
├─ 高さ: 80px
└─ 背景色: #1e3a8a

Cocoon設定 > 投稿
├─ 関連記事表示: 有効（6記事）
├─ 目次表示: 有効（H2, H3）
└─ SNSシェアボタン: 上下表示
```

#### 3. カスタムCSS追加
```css
/* 子テーマのstyle.cssに追加 */

/* カラーパレット適用 */
:root {
  --primary-color: #1e3a8a;
  --secondary-color: #10b981;
  --accent-color: #8b5cf6;
  --bg-color: #f9fafb;
  --text-color: #374151;
}

/* 見出しカスタマイズ */
.article h2 {
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  color: #ffffff;
  padding: 16px 24px;
  border-radius: 8px;
  margin: 40px 0 24px;
}

.article h2::before {
  content: "♪";
  margin-right: 12px;
}

/* CTAボタン */
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

### Phase 3: プラグイン設定（Day 2-3）

#### インストール順序と設定

1. **UpdraftPlus**（バックアップ）
   - 週次自動バックアップ設定
   - Google Drive連携

2. **SEO SIMPLE PACK**
   - 基本設定完了
   - OGP設定
   - Google Analytics/Search Console連携

3. **LiteSpeed Cache**
   - MixHost推奨設定適用
   - 画像最適化有効化
   - CSS/JS圧縮

4. **Contact Form 7**
   - お問い合わせフォーム作成
   - スパム対策設定

5. **Table of Contents Plus**
   - 目次自動生成設定
   - デザインカスタマイズ

### Phase 4: コンテンツ構造（Day 3-4）

#### カテゴリ作成
```
メインカテゴリ:
├─ Sunoノウハウ
│  ├─ 基本操作
│  ├─ プロンプトテクニック
│  ├─ ジャンル別ガイド
│  └─ 商用利用ガイド
├─ AI音楽ニュース
├─ ツールレビュー
└─ コラム
```

#### 固定ページ作成
- トップページ（カスタムレイアウト）
- About（アリサのプロフィール）
- プライバシーポリシー
- お問い合わせ

### Phase 5: ウィジェット設定（Day 4）

#### サイドバーウィジェット配置
1. 検索ボックス
2. カスタムHTML（メルマガCTA）
3. 人気記事（WordPress Popular Posts）
4. カテゴリー一覧
5. 最新記事
6. タグクラウド

#### メルマガCTAウィジェット
```html
<div class="newsletter-widget">
  <h3>📧 無料メルマガ登録</h3>
  <p>AI音楽制作の最新情報をお届け！</p>
  <form action="[MailChimp URL]" method="post">
    <input type="email" placeholder="メールアドレス" required>
    <button type="submit" class="btn-primary">今すぐ無料登録</button>
  </form>
  <small>✓ いつでも解除可能</small>
</div>
```

### Phase 6: パフォーマンス最適化（Day 5）

#### 速度測定と改善
1. **GTmetrix**で初期測定
2. 画像最適化（WebP変換）
3. 不要プラグイン削除
4. CDN設定（Cloudflare）
5. データベース最適化

#### 目標数値
- PageSpeed Insights: 90以上
- GTmetrix: Aグレード
- 読み込み時間: 3秒以内

### Phase 7: セキュリティ強化（Day 5）

#### 追加セキュリティ対策
```
1. SSL証明書確認
2. wp-config.php保護
3. ファイルパーミッション設定
4. 定期的なマルウェアスキャン設定
5. 2段階認証の導入検討
```

## 📋 チェックリスト

### 公開前の最終確認
- [ ] 全ページのモバイル表示確認
- [ ] 404ページのカスタマイズ
- [ ] robots.txt設定
- [ ] XMLサイトマップ生成
- [ ] Google Analytics設置
- [ ] Search Console登録
- [ ] OGP画像設定
- [ ] ファビコン設定
- [ ] お問い合わせフォームテスト
- [ ] メルマガ登録テスト
- [ ] バックアップ動作確認
- [ ] 表示速度測定（3秒以内）

## 🔧 トラブルシューティング

### よくある問題と解決策

1. **表示が崩れる**
   - キャッシュクリア
   - プラグイン競合確認
   - 子テーマのCSS確認

2. **速度が遅い**
   - 画像サイズ確認
   - プラグイン数見直し
   - キャッシュ設定確認

3. **エラーが出る**
   - デバッグモード有効化
   - エラーログ確認
   - プラグイン一時無効化

## 📚 参考リソース

- [Cocoon公式マニュアル](https://wp-cocoon.com/)
- [MixHostサポート](https://mixhost.jp/support/)
- [WordPress Codex日本語版](https://wpdocs.osdn.jp/)

## 🎯 運用開始後のタスク

1. **週次タスク**
   - プラグイン更新確認
   - バックアップ確認
   - アクセス解析レビュー

2. **月次タスク**
   - セキュリティスキャン
   - 表示速度測定
   - 不要データ削除
   - SEO順位確認

3. **四半期タスク**
   - デザイン見直し
   - プラグイン棚卸し
   - コンテンツ戦略見直し