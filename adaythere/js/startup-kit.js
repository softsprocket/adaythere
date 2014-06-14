/**
 * JavaScript code for all ui-kit components.
 * Use namespaces.
 */
window.isRetina = (function() {
	var root = ( typeof exports == 'undefined' ? window : exports);
	var mediaQuery = "(-webkit-min-device-pixel-ratio: 1.5),(min--moz-device-pixel-ratio: 1.5),(-o-min-device-pixel-ratio: 3/2),(min-resolution: 1.5dppx)";
	if (root.devicePixelRatio > 1)
		return true;
	if (root.matchMedia && root.matchMedia(mediaQuery).matches)
		return true;
	return false;
})();
//nextOrFirst? prevOrLast?
jQuery.fn.nextOrFirst = function(selector) { var next = this.next(selector); return (next.length) ? next : this.prevAll(selector).last(); }
jQuery.fn.prevOrLast = function(selector){ var prev = this.prev(selector); return (prev.length) ? prev : this.nextAll(selector).last(); }

//preload images
$.fn.preload=function(){this.each(function(){$("<img/>")[0].src=this})}

var isMobile = {
	Android: function() {
		return navigator.userAgent.match(/Android/i);
	},
	BlackBerry: function() {
		return navigator.userAgent.match(/BlackBerry/i);
	},
	iOS: function() {
		return navigator.userAgent.match(/iPhone|iPad|iPod/i);
	},
	Opera: function() {
		return navigator.userAgent.match(/Opera Mini/i);
	},
	Windows: function() {
		return navigator.userAgent.match(/IEMobile/i);
	},
	any: function() {
		return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
	}
};

/** 
 * Global part of startup-kit
 * */
(function($) {
	$(function() {
		/* function on load */
		$(window).load(function() {
			$('html').addClass('loaded');
			$(window).resize();
		});

		/* ie fix images */
		if (/msie/i.test(navigator.userAgent)) {
			$('img').each(function() {
				$(this).css({
					width : $(this).attr('width') + 'px',
					height : 'auto'
				});
			});
		}
		// Focus state for append/prepend inputs
		$('.input-prepend, .input-append').on('focus', 'input', function() {
			$(this).closest('.control-group, form').addClass('focus');
		}).on('blur', 'input', function() {
			$(this).closest('.control-group, form').removeClass('focus');
		});
	});
})(jQuery);
//swipe
(function($){$.fn.touchwipe=function(settings){var config={min_move_x:20,min_move_y:20,wipeLeft:function(){},wipeRight:function(){},wipeUp:function(){},wipeDown:function(){},preventDefaultEvents:true};if(settings)$.extend(config,settings);this.each(function(){var startX;var startY;var isMoving=false;function cancelTouch(){this.removeEventListener('touchmove',onTouchMove);startX=null;isMoving=false}function onTouchMove(e){if(config.preventDefaultEvents){e.preventDefault()}if(isMoving){var x=e.touches[0].pageX;var y=e.touches[0].pageY;var dx=startX-x;var dy=startY-y;if(Math.abs(dx)>=config.min_move_x){cancelTouch();if(dx>0){config.wipeLeft();e.preventDefault()}else{config.wipeRight();e.preventDefault()}}else if(Math.abs(dy)>=config.min_move_y){cancelTouch();if(dy>0){config.wipeDown()}else{config.wipeUp()}}}}function onTouchStart(e){if(e.touches.length==1){startX=e.touches[0].pageX;startY=e.touches[0].pageY;isMoving=true;this.addEventListener('touchmove',onTouchMove,false)}}if('ontouchstart'in document.documentElement){this.addEventListener('touchstart',onTouchStart,false)}});return this}})(jQuery);
