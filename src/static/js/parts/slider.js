/*
 * SLIDER 
 * =============================================================================
 */
+function ($) { "use strict";
        
    var isRtl = $('[dir=rtl]').length > 0;
  
    $.Slider = function (config) { 
        var self = this,
            resizeTimer;
        
        $.extend(this, config);
                
        this.activateControl();
        this.init();
        
        $(window).on('resize', function () {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () {
                self.init();
            }, 500);
        });
    };
    
    /*
     * Show the current tab controls.
     * -------------------------------------------------------------------------
     */
    $.Slider.prototype.activateControl = function () { 
        var self = this;
        
        $(this.widget).find('a[data-toggle="tab"]').off('show.bs.tab').on('show.bs.tab', function (e) {
            var control = $(self.widget).find('li.control'),
                target  = $(e.target).attr('href');

            control.removeClass('current');
            control.has('a[href=' + target + ']').addClass('current');
        });
    };
    
    /*
     * Resize div.container-carousel to make all items stack horizontal.
     * -------------------------------------------------------------------------
     */
    $.Slider.prototype.resizeContent = function () {
        var ulWidth = (100 / this.maxItems) * this.totalItems,
            liWidth = 100 / this.totalItems;

        this.ul.css('width', ulWidth + '%');
        this.li.css('width', liWidth + '%');

    };
    
    /*
     * Adding sliding control.
     * -------------------------------------------------------------------------
     */
    $.Slider.prototype.slideControl = function () {
        var     self            = this,
                direction       = isRtl ? 'right' : 'left',
                maxPos  = Math.ceil( this.totalItems / this.maxItems ) - 1,
                mod     = (this.totalItems % this.maxItems),
                maxMove = mod 
                        ? -( (maxPos - 1) * 100 + mod * 100 / this.maxItems )
                        : -( maxPos * 100 + mod * 100 / this.maxItems );
                    
                // Reset position.
                this.position = 0;
                this.ul.css(direction, 0);
        
                this.control.off('click').on('click', function () {    
                        if( isRtl ) {
                                $(this).data('slide') === 'next' ? self.position-- : self.position++;
                        } else {
                                $(this).data('slide') === 'next' ? self.position++ : self.position--;
                        }

                        var     newMove = -self.position * 100,
                                obj     = {};

                        if( self.position === maxPos || self.position < 0  ) {
                                newMove         = maxMove;
                                self.position   = maxPos;
                        } else if( self.position > maxPos ) {
                                newMove         = 0;
                                self.position   = 0;
                        }    
                        
                        obj[direction] = newMove + '%';
                        self.ul.animate( obj, 1000, 'easeOutExpo');
                });
    };
    
    /*
     * Initialize.
     * -------------------------------------------------------------------------
     */
    $.Slider.prototype.init = function () {
        var widgetWidth     = $(this.widget).width();
           
        this.ul             = $(this.tab).find('ul');
        this.li             = this.ul.find('li');
        this.totalItems     = this.li.length;
        this.control        = $(this.widget).find('.control a').filter('[href=' + this.tab + ']');  
                        
        if(widgetWidth < 570)       this.maxItems = 2;
        else if(widgetWidth < 720)  this.maxItems = 3;
        else if(widgetWidth < 950)  this.maxItems = 4;
        else                        this.maxItems = 6;

        this.resizeContent();
        this.slideControl();
    };

    
} (jQuery);