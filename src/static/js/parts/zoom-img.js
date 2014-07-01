/*
 * ZOOM IMAGE EFFECT 
 * =============================================================================
 */

+function ($) { "use strict";
    
    // Only run on medium and large device.
    if( $(window).width() >= 768 ) {
        /**
         * Zoom an image.
         * -------------------------------------------------------------------------
         * @param {int} duration
         * @param {string} parent
         * @returns {$}
         */
        $.fn.zoomImg = function (duration, parent) {   
            
            var $this = $(this);
            
            $this.imagesLoaded(function () {
                $this.closest(parent || '.image').hover(function () {
                        var img     = $(this).find('img'),            
                            h       = img.height(),
                            w       = img.width(),
                            newW    = w * 2,
                            newH    = newW * h / w;

                        img
                                .css({
                                                maxWidth        : 'none',
                                                maxHeight       : 'none'
                                        })
                                .stop()
                                .animate({
                                                height  : newH,
                                                width   : newW,
                                                top     : -(h/2),
                                                left    : -(w/2)
                                        }, 
                                        duration || 300);
                }, function (e) {
                    $(this).find('img').stop().animate({
                        height  : '100%',
                        width   : '100%',
                        top     : 0,
                        left    : 0
                    }, duration || 300);
                });
            });                

            return $(this);
        };
    }   
    
} (jQuery);