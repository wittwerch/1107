/*
 * IFRAME
 * =============================================================================
 */
+function ($) { "use strict";
    
    /*
     * Fix z-index youtube video embedding
     * -------------------------------------------------------------------------
     */
    $('iframe').each(function () {        
        var $this   = $(this),
            src     = $this.attr('src');
        
        if(src && src.search(/youtube/i) >= 0) {
            $this.attr('src', src + '?wmode=transparent');
        }
    });
    
} (jQuery);