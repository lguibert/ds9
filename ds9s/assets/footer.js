$(document).ready(function(){
	placeFooter();

	function placeFooter(){
		var header = $('header .jumbotron');
		var footer = $("#footer");
		var body = $('body');
		var root = $("#root");

		if(root.height() < body.height()){
			console.log("First if validated");
			var margin = body.outerHeight() - root.outerHeight() - header.outerHeight() - 10;
			if (margin > 0){
				footer.css('margin-top',margin);
			}			
		}
	}
});