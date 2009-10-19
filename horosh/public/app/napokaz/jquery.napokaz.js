(function ($) {
	$.fn.napokaz = function (options) {
		
		var opts = $.extend({}, $.fn.napokaz.defaults, options);
        
        return this.each(function(){
        	var obj = $(this);
        	
        	display();
        	
        	function display() {
	        	var items = obj.find(opts.span_items).find('a');
	        	var pages = preparePages(items);
        		var container = $('<div class="gallery-container" />');
            	container.css('position', 'relative');
            	
        		var page_tmpl = $('<div class="gallery-page" />');
        		
        		for (i=0; i<pages.length; i++) {
					var page = page_tmpl.clone();
					page.css({
						position: 'absolute', 
						top:0, 
						left:0
					});
					
					var photos = [];
					for (j=0; j<pages[i].length; j++ ) {
						var photo = $(pages[i][j]);
						var img = photo.find('img');
						photo.css({
	                        backgroundImage: 'url(' + img.attr('src') + ')',
	                        backgroundPosition: 'center',
	        				width: opts.img_min,
	        				height: opts.img_min,
	        				display: 'block',
	        				float: 'left'
	                    });
						photo.html('');
						page.append(photo);
					}
					container.append(page);
				}
	        	obj.append(container);
	        	
	        	if (1 < pages.length) {
	        		if (opts.show_controls) {
		        		var controls = getControls();
		        		obj.append(controls);
		        		obj.css('padding-bottom', controls.outerHeight());
	        		}
	        		cycle(container);
	        		
	        	} else {
	        		reshape(container);
	        	}
	        	
	        	obj.find(opts.span_items).remove();
	        	
	        	obj.css({
	        		width: container.width(),
	        		height: container.height(),
	        		position: 'relative'
	        	});
        		
        		return container;
        	}
        	
        	function getControls() {
        		var container = $('<div class="gallery-controls" />');
        		var buttons = $('<div class="gallery-controls-buttons" />');
        		buttons.append('<div class="control-prev">prev</div>');
        		buttons.append('<div class="control-next">next</div>');
        		container.append(buttons);
        		container.append('<div class="gallery-controls-pager"></div>');
        		
        		//container.append('<div class="gallery-controls-pages"></div>');
        		return container;
			}
        	
        	function cycle(container) {
        		var options = {
                    fx:     'scrollHorz', 
                    //pause:   1,
                    timeout: 0,
                    speed:  'fast'
        		};
        		if (opts.show_controls) {
        			$.extend(options, {
        				slideExpr: '.gallery-page',
                        next: obj.find('.control-next'),
                        prev: obj.find('.control-prev'),
                        after: function(curr, next, opts) {
                            obj.find('.gallery-controls-pager').html(
                            	(opts.currSlide + 1) + ' из ' + opts.slideCount
                            );
                        }
        				//pager: obj.find('.gallery-controls-pages')
        			});
        		}
        		container.cycle(options);
        	}
        	
        	function reshape(container) {
        		var els = container.children();
        		var maxw = 0, maxh = 0;
        		for(var j=0; j < els.length; j++) {
        			var $e = $(els[j]), e = $e[0], w = $e.outerWidth(), h = $e.outerHeight();
        			if (!w) w = e.offsetWidth;
        			if (!h) h = e.offsetHeight;
        			maxw = w > maxw ? w : maxw;
        			maxh = h > maxh ? h : maxh;
        		}
        		if (maxw > 0 && maxh > 0)
        			container.css({width: maxw+'px',height: maxh+'px'});
			}
        	
        	function preparePages(items) {
        		var pages = [];
            	var items_count = items.size();
            	var pages_count = Math.floor(items_count / opts.count_per_page);
            	if (pages_count * opts.count_per_page != items_count) {
            		pages_count++;
            	}
            	for (i=0; i<pages_count; i++) {
            		pages[i] = items.splice(0, opts.count_per_page);
            	}
            	return pages;
			}
        });
        
        function debug(msg) {
            if (window.console && window.console.log && opts.debug) {
                window.console.log(msg);
            }
        }
	};
	$.fn.napokaz.defaults = {
		debug: true,
		span_items: '.gallery-items',
		count_per_page: 5,
		show_controls: true,
		img_min: '108px'
	};
}(jQuery));