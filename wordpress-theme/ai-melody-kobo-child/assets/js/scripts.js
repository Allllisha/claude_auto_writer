/**
 * AI Melody Kobo Custom Scripts
 */

(function($) {
    'use strict';

    // Document ready
    $(document).ready(function() {
        
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

        // フェードインアニメーション
        function checkScroll() {
            $('.fade-in').each(function() {
                var elementTop = $(this).offset().top;
                var elementBottom = elementTop + $(this).outerHeight();
                var viewportTop = $(window).scrollTop();
                var viewportBottom = viewportTop + $(window).height();

                if (elementBottom > viewportTop && elementTop < viewportBottom) {
                    $(this).addClass('visible');
                }
            });
        }

        // 初回チェック
        checkScroll();

        // スクロール時にチェック
        $(window).scroll(function() {
            checkScroll();
        });

        // 目次の固定表示
        var toc = $('#toc');
        if (toc.length) {
            var tocOffset = toc.offset().top;
            var tocClone = toc.clone().attr('id', 'toc-fixed').addClass('toc-fixed').hide();
            $('body').append(tocClone);

            $(window).scroll(function() {
                if ($(window).scrollTop() > tocOffset + 100) {
                    tocClone.fadeIn();
                } else {
                    tocClone.fadeOut();
                }
            });

            // 目次内のリンククリック
            tocClone.find('a').on('click', function(e) {
                e.preventDefault();
                var target = $(this.getAttribute('href'));
                if (target.length) {
                    $('html, body').animate({
                        scrollTop: target.offset().top - 20
                    }, 500);
                }
            });
        }

        // 記事カードのホバーエフェクト
        $('.article-card, .entry-card-wrap').hover(
            function() {
                $(this).find('img').css('transform', 'scale(1.05)');
            },
            function() {
                $(this).find('img').css('transform', 'scale(1)');
            }
        );

        // メールフォームのバリデーション
        $('.newsletter-form').on('submit', function(e) {
            var emailInput = $(this).find('input[type="email"]');
            var email = emailInput.val();
            
            if (!isValidEmail(email)) {
                e.preventDefault();
                emailInput.addClass('error');
                showMessage('有効なメールアドレスを入力してください。', 'error');
                return false;
            }
            
            // 成功メッセージ（実際の送信はフォームのactionに依存）
            showMessage('登録ありがとうございます！', 'success');
        });

        // メールアドレスの検証
        function isValidEmail(email) {
            var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            return regex.test(email);
        }

        // メッセージ表示
        function showMessage(message, type) {
            var messageBox = $('<div class="message-box ' + type + '">' + message + '</div>');
            $('body').append(messageBox);
            messageBox.fadeIn().delay(3000).fadeOut(function() {
                $(this).remove();
            });
        }

        // モバイルメニューの改善
        $('.mobile-menu-button').on('click', function() {
            $('body').toggleClass('menu-open');
        });

        // 検索ボックスのフォーカス効果
        $('.search-box input[type="text"]').on('focus', function() {
            $(this).parent().addClass('focused');
        }).on('blur', function() {
            $(this).parent().removeClass('focused');
        });

        // 人気記事のランキング番号スタイル
        $('.popular-post-item').each(function(index) {
            var rank = index + 1;
            if (rank <= 3) {
                $(this).find('.rank-number').addClass('top-' + rank);
            }
        });

        // タグクラウドのホバーエフェクト
        $('.tagcloud a').hover(
            function() {
                $(this).css({
                    'transform': 'translateY(-2px)',
                    'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'
                });
            },
            function() {
                $(this).css({
                    'transform': 'translateY(0)',
                    'box-shadow': 'none'
                });
            }
        );

        // 記事内の画像にライトボックス効果を追加
        $('.article img').each(function() {
            if (!$(this).parent().is('a')) {
                $(this).wrap('<a href="' + $(this).attr('src') + '" class="image-lightbox"></a>');
            }
        });

        // シェアボタンの動的配置
        var shareButtons = $('.sns-share-buttons');
        if (shareButtons.length) {
            var shareClone = shareButtons.clone().addClass('floating-share');
            $('body').append(shareClone);
            
            $(window).scroll(function() {
                var scrollTop = $(window).scrollTop();
                var articleTop = $('.article').offset().top;
                var articleBottom = articleTop + $('.article').height();
                
                if (scrollTop > articleTop && scrollTop < articleBottom - 500) {
                    shareClone.fadeIn();
                } else {
                    shareClone.fadeOut();
                }
            });
        }

        // コードブロックにコピーボタンを追加
        $('pre code').each(function() {
            var code = $(this);
            var copyButton = $('<button class="copy-code-button">コピー</button>');
            
            code.parent().css('position', 'relative');
            code.parent().append(copyButton);
            
            copyButton.on('click', function() {
                var textToCopy = code.text();
                copyToClipboard(textToCopy);
                $(this).text('コピーしました！');
                setTimeout(function() {
                    copyButton.text('コピー');
                }, 2000);
            });
        });

        // クリップボードにコピー
        function copyToClipboard(text) {
            var textarea = $('<textarea>').val(text).css({
                position: 'fixed',
                opacity: 0
            });
            $('body').append(textarea);
            textarea[0].select();
            document.execCommand('copy');
            textarea.remove();
        }

        // パララックス効果（ヒーローセクション）
        if ($('.hero-section').length) {
            $(window).scroll(function() {
                var scrolled = $(window).scrollTop();
                $('.hero-bg').css('transform', 'translateY(' + (scrolled * 0.5) + 'px)');
                $('.hero-content').css('transform', 'translateY(' + (scrolled * 0.2) + 'px)');
            });
        }

        // アコーディオン（FAQ等で使用）
        $('.accordion-item').each(function() {
            var item = $(this);
            var header = item.find('.accordion-header');
            var content = item.find('.accordion-content');
            
            header.on('click', function() {
                item.toggleClass('active');
                content.slideToggle(300);
                
                // 他のアコーディオンを閉じる
                item.siblings('.accordion-item').removeClass('active');
                item.siblings('.accordion-item').find('.accordion-content').slideUp(300);
            });
        });

        // 読了時間の計算と表示
        if ($('.article').length) {
            var articleText = $('.article').text();
            var wordsPerMinute = 400; // 日本語の平均読書速度
            var textLength = articleText.length;
            var readingTime = Math.ceil(textLength / wordsPerMinute);
            
            $('.reading-time').text(readingTime + '分で読めます');
        }

        // スクロールプログレスバー
        var progressBar = $('<div class="scroll-progress"></div>');
        $('body').append(progressBar);
        
        $(window).scroll(function() {
            var scrollTop = $(window).scrollTop();
            var docHeight = $(document).height() - $(window).height();
            var scrollPercent = (scrollTop / docHeight) * 100;
            
            progressBar.css('width', scrollPercent + '%');
        });

    });

    // Window load
    $(window).on('load', function() {
        // ローディング画面を非表示
        $('.loading-screen').fadeOut();
        
        // 画像の遅延読み込み
        $('img[data-src]').each(function() {
            $(this).attr('src', $(this).data('src'));
        });
    });

})(jQuery);