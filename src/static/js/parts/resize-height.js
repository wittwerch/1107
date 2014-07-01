/*
 * RESIZE HEIGHT 
 * =============================================================================
 */
+function ($) { "use strict";
    
    /**
     * Adjust container image height
     * =========================================================================
     * @param {string} parent
     * @returns {$}
     */
    $.fn.resizeHeight = function ( parent ) {                 
        var $this = $( this ); 
        
        $this.each( function () {
            var $this       = $(this),
                container   = $this.closest( parent );    
                
            $(this).imagesLoaded(function () {                
                setTimeout(function () {
                    var newH = container.width() * $this[0].height / $this[0].width;                
                    container.height( newH );
                }, 400);  
            });
        } );
        
        return $( this );        
    };
    
    /*
     * Initialize
     * -------------------------------------------------------------------------
     */
    var resizeTimer;
    
    function init() {
        $( '.article-medium .image img' ).resizeHeight( '.image' );
        $( '.article-small .image img' ).resizeHeight( '.image' );
        $( '.carousel-small .carousel-inner .item.active img' ).resizeHeight( '.carousel-inner' );
    }
    init();
    
    $(window).on( 'resize', function () { 
        clearTimeout(resizeTimer); 
        resizeTimer = setTimeout(init, 300);
    });     
        
} ( jQuery );