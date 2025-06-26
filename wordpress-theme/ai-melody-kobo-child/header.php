<?php
/**
 * Header Template
 *
 * @package AI_Melody_Kobo
 */
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div id="page" class="site">
    <a class="skip-link screen-reader-text" href="#primary">
        <?php esc_html_e( 'コンテンツへスキップ', 'ai-melody-kobo' ); ?>
    </a>

    <header id="masthead" class="site-header">
        <div class="header-inner">
            <div class="container">
                <div class="header-content">
                    <!-- サイトロゴ/タイトル -->
                    <div class="site-branding">
                        <?php if ( has_custom_logo() ) : ?>
                            <div class="site-logo">
                                <?php the_custom_logo(); ?>
                            </div>
                        <?php else : ?>
                            <h1 class="site-title">
                                <a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home">
                                    AI Melody Kobo
                                </a>
                            </h1>
                            <p class="site-description">
                                <?php bloginfo( 'description' ); ?>
                            </p>
                        <?php endif; ?>
                    </div>

                    <!-- デスクトップナビゲーション -->
                    <nav id="site-navigation" class="main-navigation desktop-navigation">
                        <?php
                        wp_nav_menu( array(
                            'theme_location' => 'primary',
                            'menu_id'        => 'primary-menu',
                            'menu_class'     => 'nav-menu',
                            'container'      => 'div',
                            'container_class' => 'nav-menu-container',
                            'fallback_cb'    => function() {
                                ?>
                                <div class="nav-menu-container">
                                    <ul class="nav-menu">
                                        <li><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a></li>
                                        <li class="menu-item-has-children">
                                            <a href="#">Sunoノウハウ</a>
                                            <ul class="sub-menu">
                                                <li><a href="#">基本操作</a></li>
                                                <li><a href="#">プロンプトテクニック</a></li>
                                                <li><a href="#">ジャンル別ガイド</a></li>
                                                <li><a href="#">商用利用ガイド</a></li>
                                            </ul>
                                        </li>
                                        <li><a href="#">AI音楽ニュース</a></li>
                                        <li><a href="#">コラム</a></li>
                                        <li><a href="#">About</a></li>
                                    </ul>
                                </div>
                                <?php
                            }
                        ) );
                        ?>

                        <!-- 検索アイコン -->
                        <button class="search-toggle" aria-label="検索">
                            <span class="search-icon">🔍</span>
                        </button>
                    </nav>

                    <!-- モバイルメニューボタン -->
                    <button class="mobile-menu-toggle" aria-label="メニュー">
                        <span class="hamburger">
                            <span></span>
                            <span></span>
                            <span></span>
                        </span>
                    </button>
                </div>
            </div>
        </div>

        <!-- 検索フォーム（ドロップダウン） -->
        <div class="header-search-form">
            <div class="container">
                <form role="search" method="get" action="<?php echo esc_url( home_url( '/' ) ); ?>">
                    <input type="search" placeholder="検索..." value="<?php echo get_search_query(); ?>" name="s">
                    <button type="submit">検索</button>
                </form>
                <button class="search-close">✕</button>
            </div>
        </div>
    </header>

    <!-- モバイルナビゲーション -->
    <nav id="mobile-navigation" class="mobile-navigation">
        <div class="mobile-menu-header">
            <span class="mobile-menu-title">メニュー</span>
            <button class="mobile-menu-close">✕</button>
        </div>
        
        <?php
        wp_nav_menu( array(
            'theme_location' => 'primary',
            'menu_id'        => 'mobile-menu',
            'menu_class'     => 'mobile-nav-menu',
            'container'      => 'div',
            'container_class' => 'mobile-nav-container',
            'fallback_cb'    => function() {
                ?>
                <div class="mobile-nav-container">
                    <ul class="mobile-nav-menu">
                        <li><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a></li>
                        <li class="menu-item-has-children">
                            <a href="#">Sunoノウハウ</a>
                            <span class="submenu-toggle">▼</span>
                            <ul class="sub-menu">
                                <li><a href="#">基本操作</a></li>
                                <li><a href="#">プロンプトテクニック</a></li>
                                <li><a href="#">ジャンル別ガイド</a></li>
                                <li><a href="#">商用利用ガイド</a></li>
                            </ul>
                        </li>
                        <li><a href="#">AI音楽ニュース</a></li>
                        <li><a href="#">コラム</a></li>
                        <li><a href="#">About</a></li>
                    </ul>
                </div>
                <?php
            }
        ) );
        ?>
        
        <!-- モバイルメニュー内のメルマガCTA -->
        <div class="mobile-newsletter-cta">
            <h3>📧 メルマガ登録</h3>
            <p>AI音楽制作の最新情報をお届け！</p>
            <a href="#newsletter" class="btn-primary">無料登録</a>
        </div>
    </nav>

    <!-- パンくずリスト -->
    <?php if ( ! is_front_page() && function_exists( 'cocoon_breadcrumb' ) ) : ?>
        <div class="breadcrumb-wrapper">
            <div class="container">
                <?php cocoon_breadcrumb(); ?>
            </div>
        </div>
    <?php elseif ( ! is_front_page() ) : ?>
        <div class="breadcrumb-wrapper">
            <div class="container">
                <nav class="breadcrumb">
                    <a href="<?php echo esc_url( home_url( '/' ) ); ?>">ホーム</a>
                    <?php if ( is_single() ) : ?>
                        <span class="separator">›</span>
                        <?php
                        $categories = get_the_category();
                        if ( ! empty( $categories ) ) :
                            $category = $categories[0];
                        ?>
                            <a href="<?php echo get_category_link( $category->term_id ); ?>">
                                <?php echo $category->name; ?>
                            </a>
                            <span class="separator">›</span>
                        <?php endif; ?>
                        <span class="current"><?php the_title(); ?></span>
                    <?php elseif ( is_page() ) : ?>
                        <span class="separator">›</span>
                        <span class="current"><?php the_title(); ?></span>
                    <?php elseif ( is_category() ) : ?>
                        <span class="separator">›</span>
                        <span class="current"><?php single_cat_title(); ?></span>
                    <?php elseif ( is_tag() ) : ?>
                        <span class="separator">›</span>
                        <span class="current">タグ: <?php single_tag_title(); ?></span>
                    <?php elseif ( is_search() ) : ?>
                        <span class="separator">›</span>
                        <span class="current">検索結果: <?php echo get_search_query(); ?></span>
                    <?php endif; ?>
                </nav>
            </div>
        </div>
    <?php endif; ?>

    <div id="content" class="site-content">
        <div class="container">

<script>
// ヘッダー検索フォームの開閉
document.addEventListener('DOMContentLoaded', function() {
    const searchToggle = document.querySelector('.search-toggle');
    const searchForm = document.querySelector('.header-search-form');
    const searchClose = document.querySelector('.search-close');
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-navigation');
    const mobileClose = document.querySelector('.mobile-menu-close');
    const body = document.body;

    // 検索フォームの開閉
    if (searchToggle && searchForm) {
        searchToggle.addEventListener('click', function() {
            searchForm.classList.add('active');
            searchForm.querySelector('input[type="search"]').focus();
        });

        searchClose.addEventListener('click', function() {
            searchForm.classList.remove('active');
        });
    }

    // モバイルメニューの開閉
    if (mobileToggle && mobileNav) {
        mobileToggle.addEventListener('click', function() {
            mobileNav.classList.add('active');
            body.classList.add('mobile-menu-open');
        });

        mobileClose.addEventListener('click', function() {
            mobileNav.classList.remove('active');
            body.classList.remove('mobile-menu-open');
        });

        // サブメニューの開閉
        const submenuToggles = document.querySelectorAll('.submenu-toggle');
        submenuToggles.forEach(function(toggle) {
            toggle.addEventListener('click', function() {
                const parent = this.parentElement;
                parent.classList.toggle('open');
            });
        });
    }

    // スクロール時のヘッダー固定
    let lastScrollTop = 0;
    const header = document.getElementById('masthead');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.classList.add('fixed');
            
            if (scrollTop > lastScrollTop) {
                header.classList.add('hidden');
            } else {
                header.classList.remove('hidden');
            }
        } else {
            header.classList.remove('fixed', 'hidden');
        }
        
        lastScrollTop = scrollTop;
    });
});
</script>