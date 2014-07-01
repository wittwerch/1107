/* 
 * NAVBAR
 * -----------------------------------------------------------------------------
 * Set navbar collapse margin, so it will always be next to logo, even when 
 * there's no room
 * =============================================================================
 */
+function ($) { "use strict";
        
        var     $window = $(window),
                Navbar  = function() {
                        this.isRtl              = !! $('html[dir=rtl]').length;
                        this.logoW              = $('#main-nav .navbar-brand').width();
                        this.property           = this.isRtl ? 'margin-right' : 'margin-left';
                        this.navbarCollapse     = $('#main-nav .navbar-collapse');

                        this.init();
                };
        
        Navbar.prototype.init = function() {
                if($window.width() > 992)
                        this.navbarCollapse.css(this.property, this.logoW + 15);
                else
                        this.navbarCollapse.css(this.property, -15);
        };
        
        /**
         * Initialize
         * ---------------------------------------------------------------------
         */
        var     resizeTimer,
                navbar = new Navbar();                
        $(window).on( 'resize', function () { 
                clearTimeout(resizeTimer); 
                resizeTimer = setTimeout(function() {
                        navbar.init();
                }, 400);
        }); 
    
} (jQuery);