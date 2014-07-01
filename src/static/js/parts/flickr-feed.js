/*
 * FLICKR FEED 
 * =============================================================================
 */
+function ($) { "use strict";
    
    $.FlickrFeed = function (config) {
        var self = this,
            resizeTimer;
            
        $.extend(this, config);
        
        // Return if element not found
        if(!$(this.element).length) {
            return;
        }
        
        this.getImgs(); 
                
        $(window).on( 'resize', function () { 
            clearTimeout(resizeTimer); 

            resizeTimer = setTimeout(function () { 
                self.resizeAs(); 
                self.resizeImgs();
            }, 200);
        }); 
    };
    
    /*
     * Get flickr images.
     * -------------------------------------------------------------------------
     */
    $.FlickrFeed.prototype.getImgs = function () {
        var self        = this,
            flickerAPI  = "http://api.flickr.com/services/feeds/photos_public.gne?jsoncallback=?",
            template    = $(this.element).find('script').html(),
            frag        = '';

        $.getJSON( flickerAPI, {
            id      : this.id,
            ids     : this.ids,
            tags    : this.tags,
            tagmode : this.tagmode,
            format  : "json"
        }, function (data) {
            $.each( data.items, function( i, item ) {   
                if ( i === ( self.items || 9 ) ) return false;
                
                frag += template.replace(/{{link}}/ig, item.link)
                                .replace(/{{thumbnail}}/ig, item.media.m)
                                .replace(/{{title}}/ig, item.title);                
            });
            
            $(self.element).html(frag);
        }).done(function() {
            self.resizeAs();
            self.resizeImgs();
        });
    };
    
    /*
     * Resize the anchor height to be equal the width.
     * -------------------------------------------------------------------------
     */
    $.FlickrFeed.prototype.resizeAs = function () {
        this.a = $(this.element).find('a');
        this.a.height( this.a.width() ); 
    };
    
    /*
     * Resize the images to fit the container.
     * -------------------------------------------------------------------------
     */
    $.FlickrFeed.prototype.resizeImgs = function () {
        var self    = this,
            aW      = this.a.width();
        
        $(this.element).imagesLoaded(function () {
            self.a.find('img').each(function () {
                var h = this.height,
                    w = this.width;

                if(h < w)   $(this).height(aW).css('left', ( aW - $(this).width() ) / 2 );
                else        $(this).width(aW).css('top', ( aW - $(this).height() ) / 2 );
            });
        });
    };    
    
} (jQuery);