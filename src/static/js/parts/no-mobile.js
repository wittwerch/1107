/* 
 * NO MOBILE
 * -----------------------------------------------------------------------------
 * Only display images on medium and large devices.
 * Remove element on small devices.
 * =============================================================================
 */
+function ($) { "use strict";
    
        var noMobile        = $('.no-mobile'),
            images          = noMobile.find('[data-src], [data-alt], [data-small], [data-medium], [data-large]');

        if( $(window).width() >= 768 ) {
                if( images.length > 0 ) {            
                        images.each(function () {
                                var $this = $(this);
                                $('<img>', {
                                        src             : $this.data('src'),
                                        alt             : $this.data('alt'),
                                        'data-small'    : $this.data('small'),
                                        'data-medium'   : $this.data('medium'),
                                        'data-large'    : $this.data('large')
                                }).replaceAll( $this ).imagesLoaded(function () {
                                        noMobile.css('display', 'block');
                                });
                        });
                } else {
                        noMobile.css('display', 'block');
                }
        } else {
            noMobile.remove();
        }
    
} (jQuery);