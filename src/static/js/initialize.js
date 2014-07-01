/**
 * INITIALIZATION
 * ==============
 */

+function ($) { "use strict"; 
        var isRTL = !!$('html').is('[dir=rtl]');
        
        /*
         * Carousel Caption Animation
         * ==========================
         */
        new $.CarouselAnimation('#carousel-large');
        new $.CarouselAnimation('#carousel-medium');
        
        /*
         * Slider Tabs
         * ===========
         */
        new $.Slider({
                widget  : '#slider-tabs',       // The widget ID
                tab     : '#popular'            // The tab ID
        });
        new $.Slider({
                widget  : '#slider-tabs',       // The widget ID
                tab     : '#recent'             // The tab ID
        });
        new $.Slider({
                widget  : '#slider-tabs',       // The widget ID
                tab     : '#gallery'            // The tab ID
        });
        
        /*
         * Nivo Lightbox 
         * =============
         */
        $(
                '.image a:has(.fa-search-plus), ' + 
                '#main-content :not(.widget) .frame > a:has(img), ' +
                '.da-thumbs a'
        ).nivoLightbox({ 
                effect  : 'fadeScale'
        });

        /*
         * jQuery Marquee 
         * ==============
         */
         $('.breaking-news .content').marquee({   
                duplicated      : true,                 
                duration        : 20000,     
                pauseOnHover    : true,
                direction       : isRTL ? 'right' : 'left'
         });
         
        /*
         * HOVER DIRECTION AWARE
         * =====================
         */
        $('.da-thumbs > li').each(function() { 
                $(this).hoverdir({
                        hoverDelay : 75
                }); 
        });
        
        /**
         * RateIt
         * --------------------------------------------------------------
         */
         $(".rateit").rateit({
                step        : .5,
                resetable   : false
         }).on('over', function (event,value) { 
                $(this).attr('title', value ? parseFloat(value).toFixed(1) : 0 ); 
         }).on('rated', function (event,value) {
                $(this)
                        .rateit( 'readonly', true )
                        .attr('title', value ? parseFloat(value).toFixed(1) : 0 )
                        .next('.after-vote').css('display', 'block');
         });

        /*
         * Flickr Feed
         * ===========
         */
        new $.FlickrFeed({
                element : '#flickr-feed-aside', // The element id to place the photos.
                items   : 8,                    // How many items do you want to show.
                id      : '112356465@N05',      // A single user ID. This specifies a user to fetch for. eg: '685365@N25'.
                ids     : '',                   // A comma delimited list of user IDs. This specifies a list of users to fetch for.
                tags    : '',                   // A comma delimited list of tags to filter the feed by.
                tagmode : ''                    // Control whether items must have ALL the tags (tagmode=all), or ANY (tagmode=any) of the tags. Default is ALL.
        });
        new $.FlickrFeed({
                element : '#flickr-feed-footer',// The element id to place the photos.
                items   : 9,                    // How many items do you want to show.
                id      : '112356465@N05',      // A single user ID. This specifies a user to fetch for. eg: '685365@N25'.
                ids     : '',                   // A comma delimited list of user IDs. This specifies a list of users to fetch for.
                tags    : '',                   // A comma delimited list of tags to filter the feed by.
                tagmode : ''                    // Control whether items must have ALL the tags (tagmode=all), or ANY (tagmode=any) of the tags. Default is ALL.
        });
        
        /**
         * Twittie
         * =======
         */                        
        $('#content .twitter-feed').each(function() {
                var $this = $(this);
                $this.twittie({
                        apiPath      : 'php/tweetie/tweet.php',
                        template     : $this.find('script[type="text/template"]').html(),
                        dateFormat   : '%B %d, %Y',
                        count        : 5
                 });
        });  
        $('#footer-main .twitter-feed').each(function() {
                var $this = $(this);
                $this.twittie({
                        apiPath      : 'php/tweetie/tweet.php',
                        template     : $this.find('script').html(),
                        dateFormat   : '%B %d, %Y',
                        count        : 3
                });
        }); 

        if( $(window).width() >= 768 ) {                
                /*
                 * JQUERY ZOOM
                 * ===========
                 */
                $('.article-large .frame [data-zoom]').each(function () {
                        var $this = $(this);
                        $this.zoom({
                                url: $this.attr('href')
                        });
                });
                
                /**
                 * ========
                 * ZOOM IMG
                 * ========
                 */
                $('#content .image img').zoomImg();
        }
        
        if(!!$('#map').length) {
               /*
                * gmaps.js 
                * ========
                */
                $('#map').height( $(window).height() / 2 ); // set the map container's height
                
                new GMaps({
                        div             : '#map',
                        lat             : -6.1753500, 
                        lng             : 106.8271667,
                        scrollwheel     : false
                }).addMarker({
                        lat     : -6.1753500, 
                        lng     : 106.8271667,
                        title   : 'FriskaMax Headquarters'
                });
        }
} (jQuery);