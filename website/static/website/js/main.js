(function(jQuery){
	var parents;

	jQuery(window).ready(function(){ 
		parents = jQuery('.action-banner-container, header.large-view, header.small-view'); 
		jQuery(window).trigger('resize');
		applyStyle();
	});

	jQuery(window).load(function(){ jQuery(window).trigger('resize'); });

	jQuery('button.search').on('click', function(){
		var target = jQuery('.search-box');
		if(!target.is(':visible')){
			target.css({ display : 'block' });
			jQuery(target).animate({ top : '65px' }, 400, function(){
				jQuery(this).find('input[type="text"]').focus();
			});
		} else {
			jQuery(target).animate({ top : '0px' }, 400, function(){
				target.css({ display : 'none' });
			});
		}
	});

	jQuery(window).on('resize', function(){
		if(typeof parents === 'undefined'){ return; }
		jQuery(parents).find('figure > img').removeClass('landscape portrait');
		var _this;
		var orientation = calcHeaderOrientation();
		jQuery(orientation).each(function(index, orientation){
			_this = jQuery(orientation[0]);
			_this.removeClass('portrait landscape');
			_this.addClass(orientation[1]);
		});
	});

	function calcHeaderOrientation(){
		var orientations = Array();
		parents.each(function() {
			var target = jQuery(this).find('figure > img');
			var parent = { width : jQuery(this).outerWidth(), height : jQuery(this).outerHeight() };
			var size = { 
				original : { width : jQuery(target).outerWidth(), height : jQuery(target).outerHeight()}, 
				portrait : {}, 
				landscape : {} 
			};

			var ratio = { 
				width : parent.width / size.original.width,
				height : parent.height / size.original.height,
				aspect : size.original.width / size.original.height
			}

			size.landscape.width = Math.ceil(size.original.width * ratio.width);
			size.landscape.height = size.landscape.width / ratio.aspect;
			size.portrait.height = Math.ceil(size.original.height * ratio.height);
			size.portrait.width = size.portrait.height * ratio.aspect;
			
			if(size.portrait.height === parent.height && size.portrait.width >= parent.width){
				orientations.push(Array(target, 'portrait'));
			} else {
				orientations.push(Array(target, 'landscape'));
			}
		});
		return orientations;
	}


	function testStyle(){
        if(jQuery(".sidebar.twitter iframe").contents().find(".timeline-Widget").css("backgroundColor") == 'rgba(0, 0, 0, 0)'){
            return true;
        } return false;
    }

    function applyStyle(){
        var content = jQuery(".sidebar.twitter iframe").contents();
        jQuery(".sidebar.twitter").css({float:'right', width:'100%'});
        jQuery(content).find("a, a:visited, a:hover, a:active").css("color", '#ffffff');
        jQuery(content).find(".TweetAuthor > a").css("color", '#ffffff !important');
        jQuery(content).find(".timeline-Widget").css("backgroundColor", 'transparent');
        jQuery(content).find(".timeline-Tweet:hover").css("backgroundColor", 'transparent');
        jQuery(content).find(".timeline-Tweet-media").css("display", 'none');
        jQuery(content).find(".timeline-Header").css("display", 'none');
        jQuery(content).find(".timeline-Tweet-retweetCredit").css("color", '#fff !important');
        if(!testStyle()) {
            jQuery(".sidebar.twitter").fadeOut(0);
            setTimeout(applyStyle, 300);
        } else { jQuery(".sidebar.twitter").fadeIn(100); }
    }
}(jQuery));