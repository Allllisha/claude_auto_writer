<?php
/**
 * Sidebar Template
 *
 * @package AI_Melody_Kobo
 */

// サイドバーが有効でない場合は表示しない
if ( ! is_active_sidebar( 'sidebar-1' ) && ! is_active_sidebar( 'newsletter-cta' ) ) {
    return;
}
?>

<aside id="sidebar" class="sidebar">
    
    <!-- 検索ウィジェット -->
    <div class="widget search-widget">
        <h3 class="widget-title">
            <span class="widget-icon">🔍</span>
            サイト内検索
        </h3>
        <form role="search" method="get" class="search-form" action="<?php echo esc_url( home_url( '/' ) ); ?>">
            <div class="search-box">
                <input type="text" class="search-field" placeholder="検索キーワード入力..." value="<?php echo get_search_query(); ?>" name="s" />
                <button type="submit" class="search-submit btn-primary">検索</button>
            </div>
        </form>
        <div class="popular-searches">
            <p class="popular-searches-label">人気の検索:</p>
            <a href="<?php echo esc_url( home_url( '/?s=Suno' ) ); ?>">Suno</a>
            <a href="<?php echo esc_url( home_url( '/?s=プロンプト' ) ); ?>">プロンプト</a>
            <a href="<?php echo esc_url( home_url( '/?s=商用利用' ) ); ?>">商用利用</a>
            <a href="<?php echo esc_url( home_url( '/?s=初心者' ) ); ?>">初心者</a>
        </div>
    </div>

    <!-- メルマガCTAウィジェット（最重要） -->
    <?php if ( is_active_sidebar( 'newsletter-cta' ) ) : ?>
        <?php dynamic_sidebar( 'newsletter-cta' ); ?>
    <?php else : ?>
        <div class="widget newsletter-widget">
            <h3 class="widget-title">
                <span class="widget-icon">📧</span>
                無料メルマガ登録
            </h3>
            <div class="newsletter-widget-inner">
                <p class="newsletter-lead">🎵 AI音楽制作の最新情報をお届け！</p>
                <ul class="newsletter-benefits">
                    <li>Sunoの新機能情報</li>
                    <li>プロ級テクニック</li>
                    <li>限定プロンプト集</li>
                </ul>
                <form action="#" method="post" target="_blank" class="newsletter-form">
                    <input type="email" name="EMAIL" placeholder="メールアドレス" required>
                    <button type="submit" class="btn-primary">今すぐ無料登録</button>
                </form>
                <small>✓ いつでも解除可能</small>
            </div>
        </div>
    <?php endif; ?>

    <!-- 人気記事ランキング -->
    <div class="widget popular-posts-widget">
        <h3 class="widget-title">
            <span class="widget-icon">🏆</span>
            人気記事TOP5
        </h3>
        <?php
        // WordPress Popular Postsプラグインがインストールされている場合
        if ( function_exists( 'wpp_get_mostpopular' ) ) {
            $wpp_args = array(
                'limit' => 5,
                'range' => 'monthly',
                'post_type' => 'post',
                'thumbnail_width' => 80,
                'thumbnail_height' => 80,
                'stats_views' => 1,
                'wpp_start' => '<div class="popular-posts-list">',
                'wpp_end' => '</div>',
                'post_html' => '
                <div class="popular-post-item">
                    <span class="rank-number">{item_position}</span>
                    <div class="post-thumb">{thumb}</div>
                    <div class="post-content">
                        <h4 class="post-title"><a href="{url}">{text_title}</a></h4>
                        <span class="post-views">{views} views</span>
                    </div>
                </div>'
            );
            wpp_get_mostpopular( $wpp_args );
        } else {
            // フォールバック: 最新のコメントが多い記事を表示
            $popular_posts = new WP_Query( array(
                'posts_per_page' => 5,
                'meta_key' => 'post_views_count',
                'orderby' => 'meta_value_num',
                'order' => 'DESC'
            ) );
            
            if ( $popular_posts->have_posts() ) :
                echo '<div class="popular-posts-list">';
                $rank = 1;
                while ( $popular_posts->have_posts() ) : $popular_posts->the_post();
            ?>
                <div class="popular-post-item">
                    <span class="rank-number"><?php echo $rank; ?></span>
                    <div class="post-thumb">
                        <?php if ( has_post_thumbnail() ) : ?>
                            <?php the_post_thumbnail( 'thumbnail' ); ?>
                        <?php else : ?>
                            <img src="<?php echo get_stylesheet_directory_uri(); ?>/assets/images/default-thumb-small.jpg" alt="<?php the_title(); ?>">
                        <?php endif; ?>
                    </div>
                    <div class="post-content">
                        <h4 class="post-title">
                            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                        </h4>
                        <span class="post-views"><?php echo get_post_meta( get_the_ID(), 'post_views_count', true ) ?: 0; ?> views</span>
                    </div>
                </div>
            <?php
                $rank++;
                endwhile;
                echo '</div>';
                wp_reset_postdata();
            endif;
        }
        ?>
    </div>

    <!-- カテゴリ一覧 -->
    <div class="widget category-widget">
        <h3 class="widget-title">
            <span class="widget-icon">📚</span>
            カテゴリ
        </h3>
        <ul class="category-list">
            <?php
            $categories = get_categories( array(
                'orderby' => 'count',
                'order' => 'DESC',
                'hide_empty' => true,
            ) );
            
            foreach ( $categories as $category ) :
            ?>
                <li class="category-item">
                    <a href="<?php echo get_category_link( $category->term_id ); ?>">
                        <span class="category-icon">📁</span>
                        <?php echo $category->name; ?>
                        <span class="category-count">(<?php echo $category->count; ?>)</span>
                    </a>
                </li>
            <?php endforeach; ?>
        </ul>
    </div>

    <!-- 最新記事 -->
    <div class="widget recent-posts-widget">
        <h3 class="widget-title">
            <span class="widget-icon">📰</span>
            最新記事
        </h3>
        <ul class="recent-posts-list">
            <?php
            $recent_posts = new WP_Query( array(
                'posts_per_page' => 5,
                'post_status' => 'publish'
            ) );
            
            if ( $recent_posts->have_posts() ) :
                while ( $recent_posts->have_posts() ) : $recent_posts->the_post();
            ?>
                <li class="recent-post-item">
                    <a href="<?php the_permalink(); ?>">
                        <?php the_title(); ?>
                    </a>
                    <time datetime="<?php echo get_the_date( 'c' ); ?>" class="post-date">
                        <?php echo get_the_date(); ?>
                    </time>
                </li>
            <?php
                endwhile;
                wp_reset_postdata();
            endif;
            ?>
        </ul>
    </div>

    <!-- タグクラウド -->
    <div class="widget tag-widget">
        <h3 class="widget-title">
            <span class="widget-icon">🏷️</span>
            人気のタグ
        </h3>
        <div class="tagcloud">
            <?php
            $tags = get_tags( array(
                'orderby' => 'count',
                'order' => 'DESC',
                'number' => 20
            ) );
            
            foreach ( $tags as $tag ) :
                $tag_link = get_tag_link( $tag->term_id );
                $tag_size = ( $tag->count > 10 ) ? 'large' : ( ( $tag->count > 5 ) ? 'medium' : 'small' );
            ?>
                <a href="<?php echo $tag_link; ?>" class="tag-link tag-<?php echo $tag_size; ?>">
                    <?php echo $tag->name; ?>
                </a>
            <?php endforeach; ?>
        </div>
    </div>

    <!-- プロフィール（シングルページのみ） -->
    <?php if ( is_single() ) : ?>
    <div class="widget author-widget">
        <h3 class="widget-title">
            <span class="widget-icon">👤</span>
            AIクリエイター アリサ
        </h3>
        <div class="author-widget-content">
            <div class="author-avatar">
                <img src="<?php echo get_stylesheet_directory_uri(); ?>/assets/images/alisa-avatar.png" alt="AIクリエイター アリサ">
            </div>
            <p class="author-bio">
                AI音楽制作の魅力を日々探求中。<br>
                Sunoを使った作曲テクニックや最新情報をお届けします。
            </p>
            <div class="author-social">
                <a href="#" target="_blank" rel="noopener" class="social-link twitter">
                    <span>Twitter</span>
                </a>
                <a href="#" target="_blank" rel="noopener" class="social-link youtube">
                    <span>YouTube</span>
                </a>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <!-- アーカイブ -->
    <div class="widget archive-widget">
        <h3 class="widget-title">
            <span class="widget-icon">📅</span>
            アーカイブ
        </h3>
        <ul class="archive-list">
            <?php
            wp_get_archives( array(
                'type' => 'monthly',
                'limit' => 12,
                'show_post_count' => true,
                'before' => '<li class="archive-item">',
                'after' => '</li>'
            ) );
            ?>
        </ul>
    </div>

    <!-- 標準のサイドバーウィジェット -->
    <?php if ( is_active_sidebar( 'sidebar-1' ) ) : ?>
        <?php dynamic_sidebar( 'sidebar-1' ); ?>
    <?php endif; ?>

</aside><!-- #sidebar -->