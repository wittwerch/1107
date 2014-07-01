/*
 * TABS 
 * =============================================================================
 */
+function ($) { "use strict";
    
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        /*
         * Resize image height. 
         * ---------------------------------------------------------------------
         */
        $( $(this).attr('href') ).find('img').resizeHeight( '.image' );               
    });
    
} (jQuery);