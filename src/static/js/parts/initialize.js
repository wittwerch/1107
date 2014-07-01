/*
 * INITIALIZE
 * =============================================================================
 */
+function ($) { "use strict";
    
    /*
     * HTML5 PLACEHOLDER
     * -------------------------------------------------------------------------
     */
    $('input, textarea').placeholder(); 
    
    
    // Disable .fa-flip-horizontal on IE9 and older
    if( ! Modernizr.csstransitions ) {               
                $('.fa-flip-horizontal').removeClass('fa-flip-horizontal'); 
    }
        
} (jQuery);