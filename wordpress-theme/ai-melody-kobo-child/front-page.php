<?php
/**
 * Front Page Template
 *
 * @package AI_Melody_Kobo
 */

get_header(); ?>

<!-- ヒーローセクション -->
<section class="hero-section">
    <div class="hero-bg">
        <div class="hero-overlay"></div>
    </div>
    <div class="hero-content">
        <div class="container">
            <h1 class="hero-title fade-in">
                🎵 AIクリエイター アリサが探求する<br>
                <span class="hero-subtitle">未来の音作り</span>
            </h1>
            <p class="hero-description fade-in">
                Sunoを使った最新のAI作曲テクニックと情報をお届け
            </p>
            <div class="hero-buttons fade-in">
                <a href="#latest-articles" class="btn-primary">最新記事を読む</a>
                <a href="#newsletter" class="btn-secondary">メルマガ登録</a>
            </div>
        </div>
    </div>
    <div class="hero-wave">
        <svg viewBox="0 0 1200 120" preserveAspectRatio="none">
            <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" fill="#f9fafb"></path>
        </svg>
    </div>
</section>

<!-- 最新記事セクション -->
<section id="latest-articles" class="latest-articles-section">
    <div class="container">
        <h2 class="section-title">
            <span class="section-icon">📰</span>
            最新記事
        </h2>
        
        <div class="articles-grid">
            <?php
            $latest_posts = new WP_Query( array(
                'posts_per_page' => 6,
                'post_status' => 'publish'
            ) );
            
            if ( $latest_posts->have_posts() ) :
                while ( $latest_posts->have_posts() ) : $latest_posts->the_post();
            ?>
                <article class="article-card fade-in">
                    <a href="<?php the_permalink(); ?>" class="article-card-link">
                        <div class="article-thumb">
                            <?php if ( has_post_thumbnail() ) : ?>
                                <?php the_post_thumbnail( 'medium_large' ); ?>
                            <?php else : ?>
                                <img src="<?php echo get_stylesheet_directory_uri(); ?>/assets/images/default-thumb.jpg" alt="<?php the_title(); ?>">
                            <?php endif; ?>
                            <div class="article-category">
                                <?php
                                $categories = get_the_category();
                                if ( ! empty( $categories ) ) {
                                    echo esc_html( $categories[0]->name );
                                }
                                ?>
                            </div>
                        </div>
                        <div class="article-content">
                            <h3 class="article-title"><?php the_title(); ?></h3>
                            <div class="article-meta">
                                <time datetime="<?php echo get_the_date( 'c' ); ?>">
                                    <?php echo get_the_date(); ?>
                                </time>
                            </div>
                            <p class="article-excerpt">
                                <?php echo wp_trim_words( get_the_excerpt(), 50, '...' ); ?>
                            </p>
                        </div>
                    </a>
                </article>
            <?php
                endwhile;
                wp_reset_postdata();
            endif;
            ?>
        </div>
        
        <div class="section-more">
            <a href="<?php echo get_permalink( get_option( 'page_for_posts' ) ); ?>" class="btn-secondary">
                すべての記事を見る →
            </a>
        </div>
    </div>
</section>

<!-- Sunoカテゴリ特集 -->
<section class="suno-feature-section">
    <div class="container">
        <div class="feature-wrapper">
            <div class="feature-image">
                <img src="<?php echo get_stylesheet_directory_uri(); ?>/assets/images/suno-feature.jpg" alt="Sunoマスターガイド">
            </div>
            <div class="feature-content">
                <h2 class="section-title">
                    <span class="section-icon">🎸</span>
                    Sunoマスターガイド
                </h2>
                <p class="feature-description">
                    AI作曲ツール「Suno」を使いこなすための完全ガイド。初心者から上級者まで、レベルに合わせた情報をお届けします。
                </p>
                <ul class="feature-list">
                    <li><a href="#">Suno基本操作完全ガイド</a></li>
                    <li><a href="#">プロンプトテクニック集</a></li>
                    <li><a href="#">ジャンル別作曲のコツ</a></li>
                    <li><a href="#">商用利用と著作権について</a></li>
                </ul>
                <a href="<?php echo get_category_link( get_cat_ID( 'Sunoノウハウ' ) ); ?>" class="btn-primary">
                    もっと見る →
                </a>
            </div>
        </div>
    </div>
</section>

<!-- 人気記事ランキング -->
<section class="popular-articles-section">
    <div class="container">
        <h2 class="section-title">
            <span class="section-icon">🏆</span>
            人気記事TOP5
        </h2>
        
        <div class="popular-articles-list">
            <?php
            // WordPress Popular Postsプラグインがある場合
            if ( function_exists( 'wpp_get_mostpopular' ) ) {
                $args = array(
                    'limit' => 5,
                    'range' => 'monthly',
                    'post_type' => 'post',
                    'stats_views' => 1,
                    'thumbnail_width' => 100,
                    'thumbnail_height' => 100,
                    'wpp_start' => '<div class="popular-posts">',
                    'wpp_end' => '</div>',
                    'post_html' => '<article class="popular-post-item">
                        <span class="rank-number">{item_position}</span>
                        <div class="post-thumb">{thumb}</div>
                        <div class="post-content">
                            <h3 class="post-title">{title}</h3>
                            <span class="post-views">{views} views</span>
                        </div>
                    </article>'
                );
                wpp_get_mostpopular( $args );
            } else {
                // フォールバック: 最新記事を表示
                $popular_posts = new WP_Query( array(
                    'posts_per_page' => 5,
                    'orderby' => 'comment_count',
                    'order' => 'DESC'
                ) );
                
                if ( $popular_posts->have_posts() ) :
                    $rank = 1;
                    echo '<div class="popular-posts">';
                    while ( $popular_posts->have_posts() ) : $popular_posts->the_post();
                ?>
                    <article class="popular-post-item">
                        <span class="rank-number"><?php echo $rank; ?></span>
                        <div class="post-thumb">
                            <?php if ( has_post_thumbnail() ) : ?>
                                <?php the_post_thumbnail( 'thumbnail' ); ?>
                            <?php else : ?>
                                <img src="<?php echo get_stylesheet_directory_uri(); ?>/assets/images/default-thumb-small.jpg" alt="<?php the_title(); ?>">
                            <?php endif; ?>
                        </div>
                        <div class="post-content">
                            <h3 class="post-title">
                                <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                            </h3>
                            <span class="post-views"><?php echo get_comments_number(); ?> comments</span>
                        </div>
                    </article>
                <?php
                    $rank++;
                    endwhile;
                    echo '</div>';
                    wp_reset_postdata();
                endif;
            }
            ?>
        </div>
    </div>
</section>

<!-- ニュースレターCTA -->
<section id="newsletter" class="newsletter-cta-section">
    <div class="container">
        <div class="newsletter-cta-box">
            <div class="newsletter-cta-content">
                <h2 class="newsletter-title">
                    📧 AI音楽制作の最新情報をお届け！
                </h2>
                <p class="newsletter-description">
                    毎週金曜日、Sunoの新機能やテクニックを配信
                </p>
                <form action="#" method="post" class="newsletter-form">
                    <input type="email" name="EMAIL" placeholder="メールアドレスを入力" required>
                    <button type="submit" class="btn-primary">無料登録</button>
                </form>
                <p class="newsletter-note">
                    ✓ 無料で購読　✓ いつでも解除可能
                </p>
            </div>
            <div class="newsletter-cta-image">
                <img src="<?php echo get_stylesheet_directory_uri(); ?>/assets/images/newsletter-illustration.svg" alt="ニュースレター">
            </div>
        </div>
    </div>
</section>

<!-- カテゴリナビゲーション -->
<section class="category-navigation-section">
    <div class="container">
        <h2 class="section-title">
            <span class="section-icon">📚</span>
            カテゴリから探す
        </h2>
        
        <div class="category-grid">
            <?php
            $categories = array(
                array(
                    'name' => 'Suno基本',
                    'slug' => 'suno-basic',
                    'icon' => '🎵',
                    'color' => '#1e3a8a'
                ),
                array(
                    'name' => 'テクニック',
                    'slug' => 'techniques',
                    'icon' => '💡',
                    'color' => '#10b981'
                ),
                array(
                    'name' => 'ニュース',
                    'slug' => 'news',
                    'icon' => '📰',
                    'color' => '#8b5cf6'
                ),
                array(
                    'name' => 'ツールレビュー',
                    'slug' => 'tool-review',
                    'icon' => '🛠️',
                    'color' => '#f59e0b'
                )
            );
            
            foreach ( $categories as $cat ) :
                $category = get_category_by_slug( $cat['slug'] );
                if ( $category ) :
            ?>
                <a href="<?php echo get_category_link( $category->term_id ); ?>" class="category-card" style="--cat-color: <?php echo $cat['color']; ?>">
                    <span class="category-icon"><?php echo $cat['icon']; ?></span>
                    <h3 class="category-name"><?php echo $cat['name']; ?></h3>
                    <span class="category-count"><?php echo $category->count; ?> 記事</span>
                </a>
            <?php
                endif;
            endforeach;
            ?>
        </div>
    </div>
</section>

<!-- カスタムスタイル（このページ専用） -->
<style>
/* ヒーローセクション */
.hero-section {
    position: relative;
    min-height: 70vh;
    display: flex;
    align-items: center;
    overflow: hidden;
}

.hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--accent-color) 100%);
    z-index: -1;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('<?php echo get_stylesheet_directory_uri(); ?>/assets/images/hero-pattern.svg') repeat;
    opacity: 0.1;
}

.hero-content {
    text-align: center;
    color: white;
    padding: 80px 0;
}

.hero-title {
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 16px;
    line-height: 1.3;
}

.hero-subtitle {
    display: block;
    font-size: 56px;
    margin-top: 16px;
}

.hero-description {
    font-size: 20px;
    margin-bottom: 32px;
    opacity: 0.9;
}

.hero-buttons {
    display: flex;
    gap: 16px;
    justify-content: center;
}

.hero-wave {
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 100%;
    height: 120px;
}

/* セクション共通 */
.section-title {
    font-size: 36px;
    text-align: center;
    margin-bottom: 48px;
    color: var(--primary-color);
}

.section-icon {
    font-size: 42px;
    margin-right: 12px;
}

/* 最新記事グリッド */
.articles-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
    margin-bottom: 48px;
}

/* Suno特集セクション */
.suno-feature-section {
    background-color: var(--bg-white);
    padding: 80px 0;
}

.feature-wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 64px;
    align-items: center;
}

.feature-list {
    list-style: none;
    margin: 24px 0 32px;
}

.feature-list li {
    padding: 12px 0;
    border-bottom: 1px solid var(--border-gray);
}

.feature-list li:before {
    content: "●";
    color: var(--secondary-color);
    margin-right: 12px;
}

/* カテゴリグリッド */
.category-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
}

.category-card {
    background: var(--bg-white);
    border-radius: 12px;
    padding: 32px;
    text-align: center;
    transition: var(--transition);
    box-shadow: var(--shadow-sm);
    text-decoration: none;
    color: var(--text-body);
}

.category-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
    border-color: var(--cat-color);
}

.category-icon {
    font-size: 48px;
    display: block;
    margin-bottom: 16px;
}

/* ニュースレターCTA */
.newsletter-cta-section {
    background: linear-gradient(135deg, rgba(30, 58, 138, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
    padding: 80px 0;
}

.newsletter-cta-box {
    background: var(--bg-white);
    border-radius: 24px;
    padding: 64px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: center;
    box-shadow: var(--shadow-lg);
}

.newsletter-form {
    display: flex;
    gap: 16px;
    margin: 24px 0;
}

.newsletter-form input[type="email"] {
    flex: 1;
    padding: 16px 20px;
    border: 2px solid var(--border-gray);
    border-radius: 8px;
    font-size: 16px;
}

/* レスポンシブ */
@media (max-width: 1023px) {
    .articles-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .category-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 767px) {
    .hero-title {
        font-size: 32px;
    }
    
    .hero-subtitle {
        font-size: 36px;
    }
    
    .hero-buttons {
        flex-direction: column;
    }
    
    .articles-grid {
        grid-template-columns: 1fr;
    }
    
    .feature-wrapper,
    .newsletter-cta-box {
        grid-template-columns: 1fr;
    }
    
    .category-grid {
        grid-template-columns: 1fr;
    }
    
    .newsletter-form {
        flex-direction: column;
    }
}
</style>

<?php get_footer(); ?>