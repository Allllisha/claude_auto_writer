// AI Melody Kobo カスタムスクリプト
jQuery(document).ready(function($) {
    // スムーズスクロール
    $('a[href^="#"]').on('click', function(e) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            e.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top - 100
            }, 800);
        }
    });

    // ヘッダー固定時の処理
    var header = $('.header');
    var headerHeight = header.outerHeight();
    
    $(window).scroll(function() {
        if ($(this).scrollTop() > headerHeight) {
            header.addClass('fixed-header');
            $('body').css('padding-top', headerHeight);
        } else {
            header.removeClass('fixed-header');
            $('body').css('padding-top', 0);
        }
    });
    
    // 目次の位置を修正
    var toc = $('#toc');
    if (toc.length && !toc.closest('.article').length) {
        // 目次が記事外にある場合は非表示
        toc.hide();
    }
    
    // フッター下の不要な要素を削除
    $('.footer').nextAll('#toc, #toc-fixed, .toc-widget-box').remove();
    
    // 目次ウィジェットが変な位置にある場合は強制削除
    setTimeout(function() {
        // フッター後のすべての目次関連要素を削除
        var footer = $('.footer');
        if (footer.length) {
            footer.nextAll().filter('#toc, .toc-widget-box, .sidebar-scroll').remove();
            
            // body直下の目次も削除
            $('body > #toc, body > .toc-widget-box').remove();
        }
        
        // 固定/スティッキー目次を無効化
        $('.toc-widget-box, #toc').removeClass('sticky fixed sidebar-scroll-fixed');
        
        // z-indexが高い目次要素を修正
        $('.toc-widget-box, #toc').css({
            'position': 'relative',
            'z-index': '1',
            'top': 'auto',
            'bottom': 'auto'
        });
    }, 1000);
});