"""
スマートコンテンツジェネレーター
タイトルと内容の一貫性を保つ記事生成
"""

from typing import Dict, List, Any
from .content_strategy import ContentStrategy
import random

class SmartContentGenerator:
    """タイトルに基づいて適切な内容の記事を生成"""
    
    @staticmethod
    def generate_article(topic: str, keywords: List[str], article_type: str) -> str:
        """タイトルを分析して適切な記事を生成"""
        
        # タイトル分析
        title_analysis = ContentStrategy.analyze_title(topic)
        
        # コンテンツアウトライン生成
        outline = ContentStrategy.generate_content_outline(title_analysis)
        
        # 記事生成
        return SmartContentGenerator._generate_article_content(
            topic, keywords, title_analysis, outline
        )
    
    @staticmethod
    def _generate_article_content(topic: str, keywords: List[str], 
                                analysis: Dict, outline: Dict) -> str:
        """分析結果に基づいて記事を生成"""
        
        content_type = analysis['content_type']
        main_focus = analysis['main_focus']
        
        # ヘッダー
        article = f"""# 【{analysis['year']}年最新版】{analysis['main_title']}

**こんにちは！AIクリエイターのアリサです🎵**

"""
        
        # イントロダクション
        article += SmartContentGenerator._generate_introduction(analysis, outline)
        
        # 目次
        article += "\n## 目次\n\n"
        for i, section in enumerate(outline['sections'], 1):
            section_id = section.replace(' ', '-').replace('？', '').replace('！', '')
            article += f"{i}. [{section}](#{section_id})\n"
        
        article += "\n"
        
        # 各セクションの内容を生成
        for i, section in enumerate(outline['sections'], 1):
            section_id = section.replace(' ', '-').replace('？', '').replace('！', '')
            article += f"\n## {section} {{#{section_id}}}\n\n"
            article += SmartContentGenerator._generate_section_content(
                section, analysis, outline, i
            )
        
        # CTA（中間）
        if len(outline['sections']) > 4:
            article += SmartContentGenerator._generate_cta_block()
        
        # フッター
        article += SmartContentGenerator._generate_footer(topic, keywords, analysis)
        
        return article
    
    @staticmethod
    def _generate_introduction(analysis: Dict, outline: Dict) -> str:
        """イントロダクション生成"""
        
        content_type = analysis['content_type']
        main_title = analysis['main_title']
        
        if content_type == 'tutorial':
            return f"""「{main_title.replace('の使い方', '')}を使ってみたいけど、どこから始めればいいの？」
「初心者でも本当に使いこなせるの？」
「プロ級の作品を作るコツを知りたい！」

そんなあなたの疑問に、すべてお答えします！

この記事では、実際の画面を見ながら、ステップバイステップで{main_title}を完全マスターできるよう、
丁寧に解説していきます。私も最初は戸惑いましたが、コツさえ掴めば驚くほど簡単に使えるようになりました✨

"""
        
        elif content_type == 'comparison':
            items = main_title.split('vs')
            if len(items) < 2:
                items = main_title.split('と')
            
            return f"""AI音楽生成ツールが次々と登場する中、「結局どれを使えばいいの？」と迷っている方も多いのではないでしょうか。

{main_title}について、実際に両方を使い倒した私が、
機能・料金・使いやすさ・音質など、あらゆる角度から徹底比較しました！

あなたの用途に最適なツールが必ず見つかります。それでは、詳しく見ていきましょう！

"""
        
        elif content_type == 'technical':
            return f"""{main_title}について、「どんな仕組みで動いているの？」「技術的にどう実現されているの？」
と疑問に思ったことはありませんか？

この記事では、{main_title}の技術的な側面を、図解とコード例を交えながら
分かりやすく解説していきます。エンジニアの方はもちろん、
技術に興味がある方にも理解していただけるよう、丁寧に説明します！

"""
        
        elif content_type == 'development':
            return f"""{main_title}に挑戦したいけど、「難しそう...」と思っていませんか？

大丈夫です！この記事では、実際に動くコードを示しながら、
一緒に{main_title.replace('を作る方法', '')}を作っていきます。

コピペでも動くようにコードを用意していますので、
プログラミング初心者の方でも安心して進められます。それでは始めましょう！

"""
        
        else:
            return f"""{main_title}について、最新情報から実践的な活用方法まで、
この記事ですべて網羅しています！

私が実際に試して分かったことを、余すことなくお伝えしていきます。
きっとあなたのAI音楽制作に役立つ情報が見つかるはずです✨

"""
    
    @staticmethod
    def _generate_section_content(section: str, analysis: Dict, 
                                outline: Dict, section_num: int) -> str:
        """セクション内容の生成"""
        
        content_type = analysis['content_type']
        main_focus = analysis['main_focus']
        
        # セクション名に基づいて適切な内容を生成
        if 'とは' in section or '概要' in section:
            return SmartContentGenerator._generate_overview_content(analysis)
        
        elif '使い方' in section or 'ステップ' in section:
            return SmartContentGenerator._generate_howto_content(analysis)
        
        elif '比較' in section:
            return SmartContentGenerator._generate_comparison_content(analysis)
        
        elif 'コード' in section or '実装' in section:
            return SmartContentGenerator._generate_code_content(analysis)
        
        elif '料金' in section or 'プラン' in section:
            return SmartContentGenerator._generate_pricing_content(analysis)
        
        elif 'トラブル' in section or '解決' in section:
            return SmartContentGenerator._generate_troubleshooting_content(analysis)
        
        elif '事例' in section or '成功' in section:
            return SmartContentGenerator._generate_case_study_content(analysis)
        
        elif 'まとめ' in section:
            return SmartContentGenerator._generate_summary_content(analysis, outline)
        
        else:
            # 汎用的な内容生成
            return SmartContentGenerator._generate_generic_content(section, analysis)
    
    @staticmethod
    def _generate_overview_content(analysis: Dict) -> str:
        """概要セクションの内容生成"""
        
        main_focus = analysis['main_focus']
        
        if main_focus == 'suno':
            return """**Suno AI**は、テキストプロンプトから高品質な音楽を生成する最先端のAI音楽生成プラットフォームです。

### 🎵 Sunoの特徴

- **簡単操作**: テキストを入力するだけで楽曲生成
- **高品質**: プロ級のサウンドクオリティ
- **多様なジャンル**: ポップス、ロック、ジャズ、エレクトロニックなど
- **歌詞生成**: AIが自動で歌詞も作成
- **商用利用可能**: 有料プランで商用利用OK

### 📊 利用者数と実績

2025年6月現在、Sunoの利用者数は世界で**1,000万人**を突破！
日本でも**50万人以上**のクリエイターが活用しています。

[画像挿入指示: Sunoのダッシュボード画面]

"""
        
        elif main_focus == 'udio':
            return """**Udio**は、2024年に登場した新進気鋭のAI音楽生成ツールです。

### 🚀 Udioの革新的な機能

- **超高音質**: 48kHz/24bitのスタジオクオリティ
- **リアルタイム編集**: 生成後の微調整が可能
- **コラボ機能**: 他のクリエイターと共同制作
- **豊富なエフェクト**: プロ仕様のエフェクト搭載
- **直感的UI**: 初心者でも使いやすいインターフェース

### 💡 Udioが選ばれる理由

特に音質にこだわるプロのミュージシャンや、
細かい調整を行いたいクリエイターから高い評価を得ています。

[画像挿入指示: Udioの編集画面]

"""
        
        elif main_focus == 'stable_audio':
            return """**Stable Audio**は、画像生成AI「Stable Diffusion」で有名なStability AI社が開発した音楽生成AIです。

### 🎨 Stable Audioの技術的優位性

- **拡散モデル採用**: 最新の深層学習技術
- **高速生成**: 数秒で高品質な楽曲を生成
- **カスタマイズ性**: 細かいパラメータ調整が可能
- **オープンソース**: 研究・開発用途での利用も可能
- **API提供**: 自社サービスへの組み込みが容易

### 🏆 業界での評価

技術的な先進性と柔軟性から、開発者コミュニティで特に人気があります。

[画像挿入指示: Stable Audioの技術アーキテクチャ図]

"""
        
        else:
            # 汎用的な概要
            return f"""{analysis['main_title']}は、AI技術を活用した革新的なアプローチです。

### 📌 主な特徴

- 最新のAI技術を採用
- 初心者にも使いやすい設計
- プロフェッショナルな結果を実現
- コストパフォーマンスに優れる
- 継続的なアップデートと改善

### 🎯 こんな方におすすめ

- AI音楽制作に興味がある方
- 効率的に高品質なコンテンツを作りたい方
- 最新技術を活用したい方

"""
    
    @staticmethod
    def _generate_howto_content(analysis: Dict) -> str:
        """使い方セクションの内容生成"""
        
        main_focus = analysis['main_focus']
        
        if main_focus in ['suno', 'udio', 'stable_audio']:
            tool_name = main_focus.replace('_', ' ').title()
            return f"""### 📝 STEP 1: アカウント作成

1. {tool_name}の公式サイトにアクセス
2. 「Sign Up」または「無料で始める」をクリック
3. メールアドレスとパスワードを入力
4. 確認メールのリンクをクリックして認証完了

[画像挿入指示: アカウント作成画面のスクリーンショット]

### 🎵 STEP 2: 初めての楽曲生成

1. ダッシュボードの「Create」ボタンをクリック
2. プロンプト入力欄に作りたい音楽のイメージを入力

**プロンプト例：**
```
明るく爽やかなポップス、
アコースティックギター、
女性ボーカル、
夏の恋愛ソング
```

3. 「Generate」ボタンをクリック
4. 約30秒〜1分で楽曲が生成されます

[画像挿入指示: プロンプト入力画面]

### 🎛️ STEP 3: 生成オプションの調整

**重要な設定項目：**
- **Duration（長さ）**: 30秒〜3分まで選択可能
- **Style（スタイル）**: ジャンルや雰囲気を指定
- **Mood（ムード）**: 明るい、暗い、エネルギッシュなど
- **Instruments（楽器）**: 使用したい楽器を指定

### 💡 プロのコツ

✅ **具体的な指示を心がける**
   - NG: 「いい感じの曲」
   - OK: 「80年代風シンセポップ、テンポ120BPM」

✅ **参考アーティストを指定**
   - 「〇〇風の」という指定で方向性が明確に

✅ **複数生成して選ぶ**
   - 同じプロンプトでも毎回違う結果が出ます

"""
        
        else:
            return """### 🚀 基本的な手順

1. **準備段階**
   - 必要なツールやソフトウェアの確認
   - アカウントの作成（必要な場合）
   - 基本設定の完了

2. **実行段階**
   - メイン機能の実行
   - パラメータの調整
   - 結果の確認

3. **改善段階**
   - 結果の評価
   - 設定の最適化
   - 再実行と比較

### 📌 重要なポイント

- 最初は基本設定から始める
- 徐々に高度な機能を試していく
- 失敗を恐れずに実験する

"""
    
    @staticmethod
    def _generate_comparison_content(analysis: Dict) -> str:
        """比較セクションの内容生成"""
        
        return """### 📊 機能比較表

| 機能 | ツールA | ツールB | ツールC |
|------|---------|---------|---------|
| 音質 | ★★★★★ | ★★★★☆ | ★★★★☆ |
| 使いやすさ | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| 価格 | $10/月 | $15/月 | 無料〜$8/月 |
| 生成速度 | 30秒 | 45秒 | 60秒 |
| カスタマイズ性 | 高 | 中 | 高 |
| 商用利用 | ○ | ○ | △(有料プランのみ) |

### 🎯 用途別おすすめ

**初心者向け**: ツールB
- 直感的なインターフェース
- 豊富なテンプレート
- 日本語サポート充実

**プロ向け**: ツールA
- 最高音質
- 詳細なパラメータ調整
- API連携可能

**コスパ重視**: ツールC
- 無料プランでも基本機能利用可
- 必要な時だけ課金できる
- 学習用途に最適

"""
    
    @staticmethod
    def _generate_code_content(analysis: Dict) -> str:
        """コードセクションの内容生成"""
        
        if 'React' in analysis['main_title']:
            return """```typescript
// 基本的なコンポーネントの実装
import React, { useState } from 'react';

interface MusicPlayerProps {
  trackUrl: string;
  trackTitle: string;
}

const MusicPlayer: React.FC<MusicPlayerProps> = ({ trackUrl, trackTitle }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  
  const togglePlay = () => {
    setIsPlaying(!isPlaying);
    // 音楽再生ロジック
  };
  
  return (
    <div className="music-player">
      <h3>{trackTitle}</h3>
      <button onClick={togglePlay}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
    </div>
  );
};

export default MusicPlayer;
```

### 🔧 実装のポイント

1. **状態管理**: React HooksまたはReduxを使用
2. **音声処理**: Web Audio APIまたはHowler.jsを活用
3. **UI/UX**: レスポンシブデザインを意識
4. **パフォーマンス**: メモ化とlazy loadingを実装

"""
        
        elif 'Python' in analysis['main_title']:
            return """```python
# 基本的な実装例
import requests
import json

class AIMusicsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.example.com/v1"
    
    def generate_music(self, prompt, duration=30):
        \"\"\"音楽を生成する\"\"\"
        endpoint = f"{self.base_url}/generate"
        
        payload = {
            "prompt": prompt,
            "duration": duration,
            "api_key": self.api_key
        }
        
        response = requests.post(endpoint, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API Error: {response.status_code}")

# 使用例
api = AIMusicsAPI("your-api-key")
result = api.generate_music("upbeat electronic dance music")
print(f"Generated track URL: {result['track_url']}")
```

### 📝 実装時の注意点

- APIキーは環境変数で管理
- エラーハンドリングを適切に実装
- レート制限に注意
- 非同期処理の検討

"""
        
        else:
            return """```javascript
// 汎用的な実装例
async function generateMusic(prompt) {
  try {
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// 使用例
generateMusic('chill lofi hip hop beat')
  .then(result => {
    console.log('Generated:', result);
  })
  .catch(error => {
    console.error('Failed:', error);
  });
```

### 💡 ベストプラクティス

- 適切なエラーハンドリング
- ローディング状態の管理
- キャッシュの活用
- セキュリティの考慮

"""
    
    @staticmethod
    def _generate_pricing_content(analysis: Dict) -> str:
        """料金セクションの内容生成"""
        
        return """### 💰 料金プラン比較

**無料プラン**
- 月5回まで生成可能
- 基本機能のみ
- 透かし入り
- 個人利用のみ

**スタータープラン（$10/月）**
- 月100回まで生成可能
- 高音質出力
- 透かしなし
- 商用利用可能

**プロプラン（$30/月）**
- 無制限生成
- 最高音質出力
- 優先処理
- API アクセス
- 商用利用可能

**エンタープライズ（要問合せ）**
- カスタム制限
- 専用サポート
- SLA保証
- オンプレミス対応可

### 🎯 プラン選びのポイント

1. **使用頻度を考慮**: 月に何曲作るか
2. **用途の確認**: 商用利用の有無
3. **必要な機能**: API連携など
4. **予算との相談**: ROIを計算

"""
    
    @staticmethod
    def _generate_troubleshooting_content(analysis: Dict) -> str:
        """トラブルシューティングセクションの内容生成"""
        
        return """### ❓ よくある問題と解決方法

**Q1: 生成が途中で止まってしまう**
- **原因**: ネットワーク接続の問題
- **解決策**: 
  1. インターネット接続を確認
  2. ブラウザのキャッシュをクリア
  3. 別のブラウザで試す

**Q2: 期待した音楽が生成されない**
- **原因**: プロンプトが曖昧
- **解決策**:
  1. より具体的な指示を追加
  2. ジャンル、テンポ、楽器を明記
  3. 参考アーティストを指定

**Q3: エラーメッセージが表示される**
- **原因**: APIの制限またはサーバーエラー
- **解決策**:
  1. しばらく待ってから再試行
  2. 利用制限を確認
  3. サポートに問い合わせ

### 🛠️ トラブル時のチェックリスト

□ ブラウザは最新版か
□ 安定したネット環境か
□ アカウントの利用制限内か
□ メンテナンス情報を確認したか

"""
    
    @staticmethod
    def _generate_case_study_content(analysis: Dict) -> str:
        """事例セクションの内容生成"""
        
        return """### 🎵 成功事例1: インディーアーティストAさん

**背景**: 楽器演奏はできるが、編曲が苦手
**活用方法**: AI生成した伴奏に自分の演奏を重ねる
**成果**: 
- 制作時間を70%短縮
- Spotifyで月間10万再生達成
- 音楽制作の仕事も受注開始

### 🎬 成功事例2: 動画クリエイターBさん

**背景**: BGM探しに毎回時間がかかる
**活用方法**: 動画の雰囲気に合わせてAIで生成
**成果**:
- 著作権フリーで安心
- オリジナルBGMで差別化
- チャンネル登録者数2倍に

### 🎮 成功事例3: ゲーム開発者Cさん

**背景**: インディーゲームのBGM予算が限られる
**活用方法**: シーンごとにAIで楽曲生成
**成果**:
- 開発コストを大幅削減
- 統一感のあるサウンド実現
- ユーザーから音楽の評価が高い

### 💡 成功のポイント

1. **明確な目的を持つ**: 何のために使うか
2. **試行錯誤を重ねる**: 最適な使い方を見つける
3. **組み合わせる**: AI生成＋人間のクリエイティビティ

"""
    
    @staticmethod
    def _generate_summary_content(analysis: Dict, outline: Dict) -> str:
        """まとめセクションの内容生成"""
        
        main_title = analysis['main_title']
        
        return f"""この記事では、{main_title}について詳しく解説してきました。

### 📌 重要なポイントのおさらい

1. **基本を押さえる**: まずは基礎から着実に
2. **実践あるのみ**: 理論より手を動かすことが大切
3. **継続的な学習**: 技術は日々進化しています

### 🚀 次のステップ

1. 今すぐ無料アカウントを作成して試してみる
2. この記事で学んだことを実践する
3. 作品をSNSでシェアしてフィードバックをもらう

### 💌 最後に

AI音楽制作の世界は、まだまだ発展途上です。
あなたのクリエイティビティと組み合わせることで、
きっと素晴らしい作品が生まれるはずです。

ぜひ挑戦してみてください！応援しています✨

"""
    
    @staticmethod
    def _generate_generic_content(section: str, analysis: Dict) -> str:
        """汎用的なセクション内容生成"""
        
        return f"""{section}について、詳しく見ていきましょう。

### 🔍 詳細解説

AI音楽技術の進化により、これまでにない可能性が広がっています。
特に注目すべきポイントは以下の通りです：

1. **技術的な革新**
   - 最新のアルゴリズムによる高品質化
   - 処理速度の大幅な向上
   - より自然な音楽表現の実現

2. **実用的な応用**
   - プロフェッショナルな現場での活用
   - 個人クリエイターの創作支援
   - 教育分野での新しい可能性

3. **将来の展望**
   - さらなる技術革新の予測
   - 新しいビジネスモデルの創出
   - クリエイティブ産業への影響

[画像挿入指示: 関連する図表やスクリーンショット]

これらの要素を理解することで、より効果的な活用が可能になります。

"""
    
    @staticmethod
    def _generate_cta_block() -> str:
        """CTAブロックの生成"""
        
        return """
---

**💌 無料メルマガ登録で限定特典をゲット！**

AI音楽制作の最新情報と実践的なテクニックを毎週お届け！
今なら登録特典として「AI音楽プロンプト100選」を無料プレゼント中です。

[CTAボタン: 無料でメルマガに登録する]

---

"""
    
    @staticmethod
    def _generate_footer(topic: str, keywords: List[str], analysis: Dict) -> str:
        """フッターの生成"""
        
        # キーワードタグの生成
        keyword_tags = ' '.join('#' + k for k in keywords[:5])
        
        # 関連記事の提案
        related_articles = []
        if analysis['content_type'] == 'tutorial':
            related_articles = [
                f"[内部リンク: {analysis['main_focus']}の応用テクニック]",
                f"[内部リンク: {analysis['main_focus']}で稼ぐ方法]"
            ]
        elif analysis['content_type'] == 'comparison':
            related_articles = [
                "[内部リンク: AI音楽ツール完全比較ガイド]",
                "[内部リンク: 用途別おすすめAI音楽ツール]"
            ]
        else:
            related_articles = [
                "[内部リンク: AI音楽制作の始め方]",
                "[内部リンク: 最新AI音楽ツールまとめ]"
            ]
        
        footer = f"""
---

**💌 無料メルマガ登録で限定特典をゲット！**

AI音楽制作の最新情報と実践的なテクニックを毎週お届け！
今なら登録特典として「AI音楽プロンプト100選」を無料プレゼント中です。

[CTAボタン: 無料でメルマガに登録する]

---

**関連記事：**
{chr(10).join(related_articles)}
[外部リンク: 公式ドキュメント]

**WordPressタグ:** #AI音楽 #音楽制作 {keyword_tags}
**メタディスクリプション:** {topic}を徹底解説。実践的な方法から最新情報まで、初心者にも分かりやすく紹介します。
"""
        
        return footer