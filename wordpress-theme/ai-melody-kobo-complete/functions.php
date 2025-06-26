<?php
/**
 * AI Melody Kobo Complete Theme Functions
 * 
 * @package AI_Melody_Kobo
 * @version 2.0.0
 */

if ( !defined( 'ABSPATH' ) ) exit;

// テーマのセットアップ
add_action( 'after_setup_theme', 'ai_melody_kobo_setup' );
function ai_melody_kobo_setup() {
    // カスタムロゴサポート
    add_theme_support( 'custom-logo' );
    
    // アイキャッチ画像サポート
    add_theme_support( 'post-thumbnails' );
    
    // カスタムメニュー
    register_nav_menus( array(
        'primary' => 'メインメニュー',
    ) );
}

// スタイルとスクリプトの読み込み
add_action( 'wp_enqueue_scripts', 'ai_melody_kobo_scripts' );
function ai_melody_kobo_scripts() {
    // 親テーマのスタイル
    wp_enqueue_style( 'parent-style', get_template_directory_uri() . '/style.css' );
    
    // 子テーマのスタイル
    wp_enqueue_style( 'child-style',
        get_stylesheet_directory_uri() . '/style.css',
        array('parent-style'),
        '2.0.0'
    );
    
    // Google Fonts
    wp_enqueue_style( 'google-fonts', 'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap' );
    
    // カスタムJavaScript（jQueryに依存）
    if ( file_exists( get_stylesheet_directory() . '/assets/js/scripts.js' ) ) {
        wp_enqueue_script( 'ai-melody-scripts',
            get_stylesheet_directory_uri() . '/assets/js/scripts.js',
            array('jquery'),
            '2.0.0',
            true
        );
    }
}

// カスタムCSSの追加
add_action( 'wp_head', 'ai_melody_kobo_custom_styles' );
function ai_melody_kobo_custom_styles() {
    ?>
    <style>
        /* AI Melody Koboカスタムスタイル */
        :root {
            --primary-color: #1e3a8a;
            --primary-dark: #1e293b;
            --secondary-color: #10b981;
            --secondary-dark: #059669;
            --accent-color: #8b5cf6;
            --accent-light: #a78bfa;
            --info-color: #3b82f6;
            --cyan-color: #06b6d4;
            --bg-white: #ffffff;
            --bg-gray: #f9fafb;
            --border-gray: #e5e7eb;
            --text-heading: #111827;
            --text-body: #374151;
            --text-muted: #6b7280;
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.16);
            --transition: all 0.3s ease;
        }

        /* ベーススタイル */
        body {
            font-family: "Noto Sans JP", "Hiragino Sans", Meiryo, sans-serif;
            color: var(--text-body);
            line-height: 1.8;
            background-color: var(--bg-gray);
        }

        /* ヘッダー */
        .header {
            background-color: var(--primary-color) !important;
            box-shadow: var(--shadow-sm);
        }

        .header .site-name-text {
            color: var(--bg-white) !important;
            font-size: 28px;
            letter-spacing: 0.05em;
        }

        .header .tagline {
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
        }

        /* ナビゲーション */
        .navi-in > ul > li > a {
            color: var(--bg-white) !important;
            font-weight: 500;
            padding: 0 20px;
            transition: var(--transition);
        }

        .navi-in > ul > li > a:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }

        /* 記事見出し */
        .article h2 {
            position: relative;
            margin: 48px 0 24px;
            padding: 16px 24px;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--info-color) 100%);
            color: var(--bg-white);
            border-radius: 8px;
            font-size: 28px;
            box-shadow: var(--shadow-sm);
        }

        .article h2::before {
            content: "♪";
            margin-right: 12px;
            opacity: 0.8;
        }

        .article h3 {
            margin: 36px 0 18px;
            padding-left: 20px;
            border-left: 5px solid var(--secondary-color);
            font-size: 22px;
            color: var(--primary-color);
        }

        /* ボタン */
        .btn-primary,
        .wp-block-button__link,
        input[type="submit"],
        .go-to-top-button {
            background: linear-gradient(135deg, var(--secondary-color) 0%, var(--secondary-dark) 100%) !important;
            color: var(--bg-white) !important;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2);
            transition: var(--transition);
            display: inline-block;
            text-decoration: none !important;
            cursor: pointer;
        }

        .btn-primary:hover,
        input[type="submit"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(16, 185, 129, 0.3);
        }

        /* カード */
        .entry-card-wrap,
        .related-entry-card-wrap {
            background: var(--bg-white);
            border-radius: 12px;
            box-shadow: var(--shadow-sm);
            transition: var(--transition);
            overflow: hidden;
        }

        .entry-card-wrap:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-4px);
        }

        /* サイドバー */
        .sidebar .widget {
            background: var(--bg-white);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-sm);
        }

        .sidebar .widget-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--border-gray);
        }

        /* 検索ボックス */
        .search-box input[type="text"] {
            border: 2px solid var(--border-gray);
            border-radius: 6px;
            padding: 10px 16px;
            transition: var(--transition);
        }

        .search-box input[type="text"]:focus {
            border-color: var(--primary-color);
            outline: none;
            box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1);
        }

        /* 目次 */
        #toc {
            background-color: var(--bg-white);
            border: 2px solid var(--border-gray);
            border-radius: 12px;
            padding: 24px;
            margin: 32px 0;
            box-shadow: var(--shadow-sm);
        }

        #toc_title::before {
            content: "📑";
            margin-right: 8px;
        }
        
        /* 目次の固定表示を修正 */
        #toc.toc-fixed,
        #toc-fixed {
            display: none !important;
        }
        
        /* Cocoonの目次ウィジェットを記事内のみに制限 */
        .article #toc {
            display: block;
        }
        
        /* 目次が記事外に表示されないように */
        body > #toc,
        .footer #toc,
        .footer ~ #toc {
            display: none !important;
        }

        /* フッター */
        .footer {
            background-color: var(--primary-dark);
            color: var(--bg-white);
            padding: 48px 0 24px;
        }

        .footer a {
            color: rgba(255, 255, 255, 0.8);
        }

        .footer a:hover {
            color: var(--bg-white);
        }

        /* レスポンシブ */
        @media (max-width: 767px) {
            .article h2 {
                font-size: 20px;
                padding: 12px 16px;
            }
            
            .article h3 {
                font-size: 18px;
            }
            
            .sidebar .widget {
                padding: 20px;
            }
        }
        /* 目次の強制的な修正 */
        .toc-widget-box,
        .sidebar-scroll #toc,
        .sidebar-scroll .toc-widget-box,
        #sidebar #toc,
        #sidebar .toc-widget-box {
            position: relative !important;
            top: auto !important;
            bottom: auto !important;
            left: auto !important;
            right: auto !important;
        }
        
        /* スクロール追従する目次を完全に無効化 */
        .sidebar-scroll,
        .sidebar-scroll-fixed,
        .toc-fixed,
        .toc-widget-box.sticky,
        .toc-widget-box.fixed,
        #toc.sticky,
        #toc.fixed {
            position: relative !important;
            display: none !important;
        }
        
        /* 記事の外側にある目次を強制非表示 */
        body > .toc-widget-box,
        body > #toc,
        .footer ~ .toc-widget-box,
        .footer ~ #toc,
        #container ~ .toc-widget-box,
        #container ~ #toc {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
        }
    </style>
    <?php
}

// Cocoonの目次設定を上書き
add_action( 'init', 'ai_melody_kobo_disable_toc_widget' );
function ai_melody_kobo_disable_toc_widget() {
    // 目次ウィジェットの追従を無効化
    add_filter( 'cocoon_is_toc_widget_sticky', '__return_false' );
    
    // サイドバーの固定スクロールを無効化
    add_filter( 'cocoon_is_sidebar_scroll', '__return_false' );
}

// 目次の表示位置を記事内に限定
add_filter( 'the_content', 'ai_melody_kobo_fix_toc_position', 99 );
function ai_melody_kobo_fix_toc_position( $content ) {
    if ( is_single() && has_shortcode( $content, 'toc' ) ) {
        // 目次が適切な位置にある場合はそのまま
        return $content;
    }
    return $content;
}

// 個別記事ページで目次ウィジェットを完全に無効化
add_action( 'wp', 'ai_melody_kobo_disable_toc_on_single' );
function ai_melody_kobo_disable_toc_on_single() {
    if ( is_single() ) {
        // 目次ウィジェットを削除
        remove_action( 'wp_footer', 'cocoon_toc_widget' );
        remove_action( 'cocoon_after_footer', 'cocoon_toc_widget' );
        
        // 目次の追従表示を無効化
        add_filter( 'cocoon_is_toc_visible', '__return_false' );
    }
}

// フッター後のフックをクリア
add_action( 'wp_footer', 'ai_melody_kobo_clean_footer', 1 );
function ai_melody_kobo_clean_footer() {
    if ( is_single() ) {
        ?>
        <script>
        // 目次要素を即座に削除
        document.addEventListener('DOMContentLoaded', function() {
            var tocElements = document.querySelectorAll('.footer ~ #toc, .footer ~ .toc-widget-box, #container ~ #toc, #container ~ .toc-widget-box');
            tocElements.forEach(function(element) {
                element.remove();
            });
        });
        </script>
        <style>
        /* 個別記事ページでの目次非表示を強化 */
        .single .footer ~ #toc,
        .single .footer ~ .toc-widget-box,
        .single #container ~ #toc,
        .single #container ~ .toc-widget-box,
        .single .toc-widget-box.sidebar-scroll-fixed {
            display: none !important;
            visibility: hidden !important;
            position: absolute !important;
            left: -9999px !important;
        }
        </style>
        <?php
    }
}

// カスタムウィジェット（メルマガCTA）
class AI_Melody_Newsletter_Widget extends WP_Widget {
    
    public function __construct() {
        parent::__construct(
            'ai_melody_newsletter',
            'AI Melody Kobo ニュースレター',
            array( 'description' => 'メルマガ登録フォーム' )
        );
    }
    
    public function widget( $args, $instance ) {
        echo $args['before_widget'];
        ?>
        <div class="newsletter-widget" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%); border: 2px solid var(--primary-color); border-radius: 16px; padding: 32px; text-align: center;">
            <h3 style="font-size: 24px; color: var(--primary-color); margin-bottom: 16px;">📧 無料メルマガ登録</h3>
            <p style="margin-bottom: 24px;">AI音楽制作の最新情報をお届け！</p>
            <ul style="text-align: left; margin: 20px 0; list-style: none;">
                <li style="margin: 8px 0;">✓ Sunoの新機能情報</li>
                <li style="margin: 8px 0;">✓ プロ級テクニック</li>
                <li style="margin: 8px 0;">✓ 限定プロンプト集</li>
            </ul>
            <form action="#" method="post" target="_blank">
                <input type="email" name="EMAIL" placeholder="メールアドレス" required style="width: 100%; padding: 12px 16px; border: 2px solid var(--border-gray); border-radius: 8px; margin-bottom: 16px;">
                <button type="submit" class="btn-primary" style="width: 100%; font-size: 18px;">今すぐ無料登録</button>
            </form>
            <small style="display: block; margin-top: 12px; color: var(--text-muted);">✓ いつでも解除可能</small>
        </div>
        <?php
        echo $args['after_widget'];
    }
    
    public function form( $instance ) {
        // ウィジェット設定フォーム
        ?>
        <p>メルマガ登録フォームを表示します。</p>
        <?php
    }
}

// ウィジェットを登録
add_action( 'widgets_init', function() {
    register_widget( 'AI_Melody_Newsletter_Widget' );
    
    // カスタムウィジェットエリア
    register_sidebar( array(
        'name'          => 'ニュースレターCTA',
        'id'            => 'newsletter-cta',
        'description'   => 'メルマガ登録CTAエリア',
        'before_widget' => '<div class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ) );
});