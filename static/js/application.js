'use strict';

// Highlight current nav item
$('.nav a[href="'+window.location.pathname+'"]').parents('li').addClass('active');

$('.js-tooltip').tooltip();

$('#liame').hover(function () {
	this.href = '\x6D\x61\x69\x6C\x74\x6F\x3A\x6D\x61\x78\x40\x6D\x61\x78\x66\x69\x65\x72\x6B\x65\x2E\x63\x6F\x6D'
})

$("#all").click(function() {
	$("#all").addClass("btn-primary");
	$(".js-filter").removeClass("btn-primary").addClass("btn-default");
	$(".panel-project").show({ easing: "swing", duration: 400 });
	return false;
});
$(".js-filter").click(function() {
	var filterClass = $(this).attr('id');
	$("#js-project-filter a").removeClass("btn-primary").addClass("btn-default");
	$(".panel-project").not("."+filterClass).hide({ easing: "swing", duration: 400 });
	$("." + filterClass).show({ easing: "swing", duration: 400 });
	$(this).removeClass("btn-default").addClass("btn-primary");
	return false;
});
