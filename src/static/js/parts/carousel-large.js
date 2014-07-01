/*
 * CAROUSEL LARGE 
 * =============================================================================
 */
+function ($) { "use strict"; 
    
    var $window     = $(window),
        container   = $('.carousel-large'); 
            
    var CarouselLarge = function () {  
        this.images     = container.find('.carousel-inner img');

        this.init();
    };

    /**
     * Change images accourding to window width.
     * ---------------------------------------------------------------------
     */
    CarouselLarge.prototype.changeImages = function () {           
        this.images.each(function () {
            var $this   = $(this),
                src     = $this.attr('src'),
                small   = $this.data('small'),
                medium  = $this.data('medium'),
                large   = $this.data('large'),
                windowW = $window.width();

            if      (small && windowW <= 768 && src !== small)      $this.attr('src', small);
            else if (medium && windowW <= 1366 && src !== medium)   $this.attr('src', medium);
            else if (large && windowW > 1366 && src !== large)      $this.attr('src', large);
        });
    };

    /*
     * Define maximum container height.
     * ---------------------------------------------------------------------
     */
    CarouselLarge.prototype.defineMaxHeight = function () {        
        if( $window.width() < 992 ) {
            this.containerHeight = $window.height() - 60; // Without #top-nav.
        } else {
            this.containerHeight = $window.height() - 90; // With #top-nav.                    
        }
    };

    /*
     * Adjust vertical image position to middle.
     * 
     * @param int imgHeight
     * @param int containerHeight
     * ---------------------------------------------------------------------
     */
    CarouselLarge.prototype.setImagePosition = function (imgHeight, containerHeight) {        
        $(this).css('top', (imgHeight - containerHeight) / 2 * -1 + 'px');
    };

    /*
     * Set the container height.
     * ---------------------------------------------------------------------
     */
    CarouselLarge.prototype.setContainerHeight = function () {
        var self = this;

        container.imagesLoaded(function () {
            self.images.each(function () {            
                var w       = this.width,
                    h       = this.height,
                    newH    = ( container.width() / w ) * h; 

                if( newH < self.containerHeight ) self.containerHeight = newH;

                self.setImagePosition.call(this, newH, self.containerHeight);
            });  

            container.height(self.containerHeight);
            container.find('.item').height(self.containerHeight);
        });
    };

    /*
     * Initialize
     * ---------------------------------------------------------------------
     */
    CarouselLarge.prototype.init = function () {
        this.changeImages();
        this.defineMaxHeight();
        this.setContainerHeight();
    };

    $.CarouselLarge = new CarouselLarge();
    var resizeTimer;

    $window.on('resize', function () { 
        /*
         * On resize, reset the timeout, so the function won't run if window  
         * hasn't finish resizing. This can dramatically increase performance.
         */
        clearTimeout(resizeTimer); 

        resizeTimer = setTimeout(function () { 
             $.CarouselLarge.init();
        }, 100);
    }); 
    
} (jQuery);