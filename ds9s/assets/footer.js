$(document).ready(function(){
	var bumpIt = function(){
		var main = $("#main");

		if (main.height() < $(window).height()){
			var margin = $("body").height() - ($("header").height() + 2 *$("footer").height() + main.height());
			main.css("margin-bottom",margin);
		}
	}, didResize = false;
	
	bumpIt();


	$(window).resize(function() {
	  didResize = true;
	});
	
	setInterval(function() {  
	  if(didResize) {
	    didResize = false;
	    bumpIt();
	  }
	}, 250);
})