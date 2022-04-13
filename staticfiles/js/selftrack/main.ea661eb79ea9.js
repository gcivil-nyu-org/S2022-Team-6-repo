(function($) {

	"use strict";

	 $('.label.ui.dropdown')
  .dropdown();

		$('.no.label.ui.dropdown')
		  .dropdown({
		  useLabels: false
		});

		$('.ui.button').on('click', function () {
		  $('.ui.dropdown')
		    .dropdown('restore defaults')
		})

	 
})(jQuery);
