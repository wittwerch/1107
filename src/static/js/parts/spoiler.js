/**
 * Created on : Mar 31, 2014, 10:56:33 AM
 * Author     : Fahri
 */
+function( $ ) { 'use strict';
        
        $('.spoiler')
                .hide()
                .each(function() {
                        var     spoiler = $(this),
                                button  = $('<button></button>', {  
                                                text    : spoiler.data('show-text'),
                                                class   : spoiler.data('button-class') || 'btn btn-primary btn-xs',
                                        }),
                                pPrev   = spoiler.prev('p');
                                
                        if(spoiler.data('button-type') === 'inline' && !!pPrev.length) {
                                button.appendTo(pPrev.css('margin-bottom', 4));
                        } else {
                                button.insertBefore(spoiler);
                        }
                                                                                        
                        button.click(function() {
                                var $this = $(this);

                                if(spoiler.data('type') === 'inline') {
                                        $this.hide();
                                        spoiler.fadeIn();
                                } else {
                                        spoiler.stop().slideToggle('_default', function() {                                                                                                                
                                                $this.text( spoiler.data( spoiler.is(':visible') ? 'hide-text' : 'show-text' ) );
                                        });            
                                }
                        }); 
                });
                
        
}( jQuery );