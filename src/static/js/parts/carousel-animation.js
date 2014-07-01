/**
 * ==================
 * CAROUSEL ANIMATION 
 * ==================
 */
+function ($) { "use strict"; 
        
        $.CarouselAnimation = function (container) {        
                this.container = container;

                this.attachEventHandler();
        };
    
        /*
         * Hide the caption.
         */
        $.CarouselAnimation.prototype.hide = function () {
                var container = $(this);

                container.find('.carousel-caption').each(function () {
                        var elements    = $(this).find('div').find('h1, p').css('position', 'relative'),
                            containerW  = container.width(),
                            containerH  = container.height(),
                            animation   = $(this).data('animation');

                        switch (animation) {
                                case 'fade':
                                        elements.stop().animate({ opacity : 0 });
                                        break;

                                case 'bounce':
                                        elements.stop().animate({
                                            opacity : 0,
                                            top     : '-' + (containerH)                                    
                                        });
                                        break;
                                                       
                                case 'slide':
                                default: 
                                        var config  = { opacity: 0 },
                                            right   = containerW / 2,
                                            left    = -1 * containerW / 2;

                                        elements.each(function (i) {
                                                switch (Math.round(Math.random())) {
                                                        case 0:                                    
                                                                config.left = right;
                                                                break;
                                                        case 1:
                                                                config.left = left;
                                                                break;
                                                }

                                                $(this).stop().animate(config);
                                        });

                        }

                });

        };    
    
        /**
         * Show the caption.
         */
        $.CarouselAnimation.prototype.show = function () {
                var     container   = $(this),
                        caption     = container.find('.active .carousel-caption'),
                        elements    = caption.find('h1:visible, p:visible'),
                        animation   = caption.data('animation'),
                        speed       = caption.data('speed') || 1000;

                switch (animation) {
                        case 'fade':                    
                                elements.each(function (i) {
                                        $(this).stop().delay(Math.random() * speed / 2).animate({
                                                opacity: 1
                                        });
                                });
                                break;
                        case 'bounce':                    
                                elements.each(function (i) {
                                        $(this).stop().delay(Math.random() * speed / 2).animate({
                                                opacity: 1,
                                                top: 0
                                        }, speed, 'easeOutBounce');
                                });
                                break;
                        case 'slide':
                        default:
                                elements.each(function (i) {
                                        $(this)
                                                .stop()
                                                .delay(Math.random() * speed / 2)
                                                .animate({
                                                        opacity : 1,
                                                        top     : 0,
                                                        left    : 0
                                                }, speed, 'easeOutExpo');                        
                                });
                                break;
                }

        };
    
        /*
         * Attach event handler to automatically animate the caption.
         */
        $.CarouselAnimation.prototype.attachEventHandler = function () {
                var self = this;

                $(this.container).off('slid.bs.carousel').on('slid.bs.carousel', function () {
                        self.show.call(this);
                });

                $(this.container).off('slide.bs.carousel').on('slide.bs.carousel', function () {
                        self.hide.call(this);
                });
        };
    
}(jQuery);

