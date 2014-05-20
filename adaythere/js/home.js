(function($) {


		// PageTransitions

		$(window).resize(function() {
			var maxH = 0;
			$('.about-sections .pt-page').css('height', 'auto').each(function() {
				var h = $(this).outerHeight();
				if (h > maxH)
					maxH = h;
			}).css('height', maxH + 'px');
			$('.about-sections .page-transitions').css('height', maxH + 'px');
		});

		var pt2 = PageTransitions();
		pt2.init('#pt-2');

		$('#pt-2 .pt-control-prev').on('click', function() {
			pt2.gotoPage(2, 'prev');
			return false;
		});

		$('#pt-2 .pt-control-next').on('click', function() {
			pt2.gotoPage(1, 'next');
			return false;
		});

		$(window).resize().scroll();
		// add class "loaded" here to force ani start
		setTimeout(function() {
			$('html').addClass('loaded');
		}, 500);


	$(window).load(function() {
		$(window).resize().scroll();
	});
})(jQuery);