/*
 * ACCORDION 
 * =============================================================================
 */
+function ($) { "use strict"; 
    
    var Accordion = function () {
        this.container  = $('.accordion');
        this.header     = this.container.find('.header');
        this.content    = this.container.find('.content');
        
        this.hide();
        this.click();
    };
    
    /*
     * Hide contents except the active one.
     * -------------------------------------------------------------------------
     */
    Accordion.prototype.hide = function () {
        this.content.hide();
        this.header.filter('.active').next().show();
    };
    
    /*
     * Show clicked content.
     * -------------------------------------------------------------------------
     */
    Accordion.prototype.click = function () {
        var self = this;
        
        this.header.click(function () {      
                var $this = $(this);
                
                if( !$this.hasClass('active') ) {
                        self.header
                                .filter('.active').removeClass('active')
                                .next().stop().slideUp();
                }

                $(this)
                        .toggleClass('active')
                        .next().stop().slideToggle();
        });
    };
    
    new Accordion();
    
} (jQuery);