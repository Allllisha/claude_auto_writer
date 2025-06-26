<?php
/**
 * AI Melody Kobo Child Theme Functions
 *
 * @package AI_Melody_Kobo
 * @since 1.0.0
 */

// 子テーマのセットアップ
if ( !defined( 'ABSPATH' ) ) exit;

// 親テーマと子テーマのスタイルシートを正しく読み込む
add_action( 'wp_enqueue_scripts', 'ai_melody_kobo_enqueue_styles' );
function ai_melody_kobo_enqueue_styles() {
    // 親テーマのスタイル
    wp_enqueue_style( 'parent-style', get_template_directory_uri() . '/style.css' );
    
    // 子テーマのスタイル（親テーマの後に読み込む）
    wp_enqueue_style( 'child-style',
        get_stylesheet_directory_uri() . '/style.css',
        array('parent-style'),
        wp_get_theme()->get('Version')
    );
    
    // カスタムJavaScript（jQueryが読み込まれた後）
    wp_enqueue_script( 'ai-melody-kobo-scripts',
        get_stylesheet_directory_uri() . '/assets/js/scripts.js',
        array( 'jquery' ),
        wp_get_theme()->get('Version'),
        true
    );
}

// Cocoonが要求するjavascript.jsに対応
add_action( 'wp_enqueue_scripts', 'ai_melody_kobo_handle_javascript_js', 20 );
function ai_melody_kobo_handle_javascript_js() {
    // Cocoonのjavascript.jsリクエストを処理
    if ( file_exists( get_stylesheet_directory() . '/javascript.js' ) ) {
        wp_enqueue_script( 'child-javascript',
            get_stylesheet_directory_uri() . '/javascript.js',
            array( 'jquery' ),
            wp_get_theme()->get('Version'),
            true
        );
    }
}

// Google Fontsの追加
add_action( 'wp_head', 'ai_melody_kobo_add_google_fonts' );
function ai_melody_kobo_add_google_fonts() {
    ?>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
    <?php
}

// カスタムウィジェットエリアの登録
add_action( 'widgets_init', 'ai_melody_kobo_widgets_init' );
function ai_melody_kobo_widgets_init() {
    // ニュースレターCTAエリア
    register_sidebar( array(
        'name'          => __( 'ニュースレターCTA', 'ai-melody-kobo' ),
        'id'            => 'newsletter-cta',
        'description'   => __( 'メルマガ登録CTAを表示するエリア', 'ai-melody-kobo' ),
        'before_widget' => '<div id="%1$s" class="widget newsletter-widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ) );
}

// カスタムニュースレターウィジェット
class AI_Melody_Kobo_Newsletter_Widget extends WP_Widget {
    
    public function __construct() {
        parent::__construct(
            'ai_melody_kobo_newsletter',
            __( 'AI Melody Kobo ニュースレター', 'ai-melody-kobo' ),
            array(
                'description' => __( 'メルマガ登録フォームウィジェット', 'ai-melody-kobo' ),
            )
        );
    }
    
    public function widget( $args, $instance ) {
        echo $args['before_widget'];
        
        $title = ! empty( $instance['title'] ) ? $instance['title'] : __( '📧 無料メルマガ登録', 'ai-melody-kobo' );
        $description = ! empty( $instance['description'] ) ? $instance['description'] : __( 'AI音楽制作の最新情報をお届け！', 'ai-melody-kobo' );
        $mailchimp_url = ! empty( $instance['mailchimp_url'] ) ? $instance['mailchimp_url'] : '#';
        
        ?>
        <div class="newsletter-widget-inner">
            <h3><?php echo esc_html( $title ); ?></h3>
            <p><?php echo esc_html( $description ); ?></p>
            
            <ul class="newsletter-benefits">
                <li>Sunoの新機能情報</li>
                <li>プロ級テクニック</li>
                <li>限定プロンプト集</li>
            </ul>
            
            <form action="<?php echo esc_url( $mailchimp_url ); ?>" method="post" target="_blank">
                <input type="email" name="EMAIL" placeholder="メールアドレス" required>
                <button type="submit" class="btn-primary">今すぐ無料登録</button>
            </form>
            
            <small>✓ いつでも解除可能</small>
        </div>
        <?php
        
        echo $args['after_widget'];
    }
    
    public function form( $instance ) {
        $title = ! empty( $instance['title'] ) ? $instance['title'] : __( '📧 無料メルマガ登録', 'ai-melody-kobo' );
        $description = ! empty( $instance['description'] ) ? $instance['description'] : __( 'AI音楽制作の最新情報をお届け！', 'ai-melody-kobo' );
        $mailchimp_url = ! empty( $instance['mailchimp_url'] ) ? $instance['mailchimp_url'] : '';
        ?>
        <p>
            <label for="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>"><?php esc_attr_e( 'タイトル:', 'ai-melody-kobo' ); ?></label>
            <input class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'title' ) ); ?>" type="text" value="<?php echo esc_attr( $title ); ?>">
        </p>
        <p>
            <label for="<?php echo esc_attr( $this->get_field_id( 'description' ) ); ?>"><?php esc_attr_e( '説明文:', 'ai-melody-kobo' ); ?></label>
            <textarea class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'description' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'description' ) ); ?>"><?php echo esc_textarea( $description ); ?></textarea>
        </p>
        <p>
            <label for="<?php echo esc_attr( $this->get_field_id( 'mailchimp_url' ) ); ?>"><?php esc_attr_e( 'MailChimp URL:', 'ai-melody-kobo' ); ?></label>
            <input class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'mailchimp_url' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'mailchimp_url' ) ); ?>" type="url" value="<?php echo esc_attr( $mailchimp_url ); ?>">
        </p>
        <?php
    }
    
    public function update( $new_instance, $old_instance ) {
        $instance = array();
        $instance['title'] = ( ! empty( $new_instance['title'] ) ) ? sanitize_text_field( $new_instance['title'] ) : '';
        $instance['description'] = ( ! empty( $new_instance['description'] ) ) ? sanitize_textarea_field( $new_instance['description'] ) : '';
        $instance['mailchimp_url'] = ( ! empty( $new_instance['mailchimp_url'] ) ) ? esc_url_raw( $new_instance['mailchimp_url'] ) : '';
        return $instance;
    }
}

// ウィジェットの登録
add_action( 'widgets_init', function() {
    register_widget( 'AI_Melody_Kobo_Newsletter_Widget' );
});

// カスタムショートコード
// [ai_cta] ショートコード
add_shortcode( 'ai_cta', 'ai_melody_kobo_cta_shortcode' );
function ai_melody_kobo_cta_shortcode( $atts ) {
    $atts = shortcode_atts( array(
        'text' => '今すぐSunoを始める',
        'url' => 'https://suno.ai',
        'class' => 'btn-primary',
        'target' => '_blank'
    ), $atts );
    
    return sprintf(
        '<a href="%s" class="%s" target="%s">%s →</a>',
        esc_url( $atts['url'] ),
        esc_attr( $atts['class'] ),
        esc_attr( $atts['target'] ),
        esc_html( $atts['text'] )
    );
}

// [ai_point] ショートコード（ポイントボックス）
add_shortcode( 'ai_point', 'ai_melody_kobo_point_shortcode' );
function ai_melody_kobo_point_shortcode( $atts, $content = null ) {
    return '<div class="point-box">' . do_shortcode( $content ) . '</div>';
}

// [ai_warning] ショートコード（注意ボックス）
add_shortcode( 'ai_warning', 'ai_melody_kobo_warning_shortcode' );
function ai_melody_kobo_warning_shortcode( $atts, $content = null ) {
    return '<div class="warning-box">' . do_shortcode( $content ) . '</div>';
}

// 記事内に自動でニュースレターCTAを挿入
add_filter( 'the_content', 'ai_melody_kobo_insert_newsletter_cta' );
function ai_melody_kobo_insert_newsletter_cta( $content ) {
    if ( ! is_single() ) {
        return $content;
    }
    
    // 記事の中間にCTAを挿入
    $newsletter_cta = '
    <div class="article-newsletter-cta">
        <div class="newsletter-widget">
            <h3>📧 ニュースレター登録CTA</h3>
            <p>AI音楽制作の最新情報を毎週お届け！</p>
            <form action="#" method="post" target="_blank">
                <input type="email" name="EMAIL" placeholder="メールアドレスを入力" required>
                <button type="submit" class="btn-primary">無料で登録</button>
            </form>
        </div>
    </div>
    ';
    
    // H2タグの前にCTAを挿入（3番目のH2の前）
    $h2_count = 0;
    $content = preg_replace_callback( '/<h2/i', function( $matches ) use ( &$h2_count, $newsletter_cta ) {
        $h2_count++;
        if ( $h2_count == 3 ) {
            return $newsletter_cta . $matches[0];
        }
        return $matches[0];
    }, $content );
    
    return $content;
}

// Cocoonの設定をカスタマイズ
add_filter( 'cocoon_setting_funcs', 'ai_melody_kobo_customize_cocoon_settings' );
function ai_melody_kobo_customize_cocoon_settings( $settings ) {
    // サイトフォントをNoto Sans JPに設定
    $settings['site_font_family'] = 'noto_sans_jp';
    
    // ヘッダーロゴを中央配置
    $settings['header_layout_type'] = 'center_logo';
    
    // 目次を自動表示
    $settings['toc_display_toggle'] = 1;
    $settings['toc_depth'] = 3;
    
    return $settings;
}

// 人気記事ウィジェットのカスタマイズ
add_filter( 'wpp_custom_html', 'ai_melody_kobo_customize_popular_posts', 10, 2 );
function ai_melody_kobo_customize_popular_posts( $popular_posts, $instance ) {
    // カスタムHTMLで人気記事を表示
    $output = '<div class="popular-posts-widget">';
    
    // ここでカスタムレイアウトを実装
    
    $output .= '</div>';
    
    return $output;
}

// カテゴリーウィジェットに記事数を表示
add_filter( 'wp_list_categories', 'ai_melody_kobo_cat_count_span' );
function ai_melody_kobo_cat_count_span( $output ) {
    $output = str_replace( '</a> (', '</a> <span class="cat-count">(', $output );
    $output = str_replace( ')', ')</span>', $output );
    return $output;
}

// パンくずリストのカスタマイズ
add_filter( 'cocoon_breadcrumbs', 'ai_melody_kobo_customize_breadcrumbs' );
function ai_melody_kobo_customize_breadcrumbs( $breadcrumbs ) {
    // ホームアイコンを追加
    $breadcrumbs = str_replace( 'ホーム', '🏠 ホーム', $breadcrumbs );
    return $breadcrumbs;
}

// 投稿者情報のカスタマイズ
add_filter( 'cocoon_author_box', 'ai_melody_kobo_customize_author_box' );
function ai_melody_kobo_customize_author_box( $author_box ) {
    // AIクリエイター アリサの情報を追加
    $custom_author = '
    <div class="author-box">
        <div class="author-thumb">
            <img src="' . get_stylesheet_directory_uri() . '/assets/images/alisa-avatar.png" alt="AIクリエイター アリサ">
        </div>
        <div class="author-content">
            <h4 class="author-name">AIクリエイター アリサ</h4>
            <p class="author-description">AI音楽制作の魅力を日々探求中。Sunoを使った作曲テクニックや最新情報をお届けします。</p>
            <div class="author-social">
                <a href="#" target="_blank" rel="noopener">Twitter</a>
                <a href="#" target="_blank" rel="noopener">YouTube</a>
            </div>
        </div>
    </div>
    ';
    
    return $custom_author;
}

// 管理画面にカスタムスタイルを追加
add_action( 'admin_head', 'ai_melody_kobo_admin_styles' );
function ai_melody_kobo_admin_styles() {
    ?>
    <style>
        /* 管理画面のカスタマイズ */
        .wp-admin #wpadminbar {
            background: #1e3a8a;
        }
    </style>
    <?php
}