$(document).ready(function(){
	placeFooter();

	function placeFooter(){		
		console.log("Welcome in the function about the footer !");
		console.log($('#root').height());
		var header = $('header .jumbotron');
		var footer = $("#footer");
		var body = $('body');
		var root = $("#root");

		if(root.height() < body.height()){
			console.log("First if validated");
			var margin = body.outerHeight() - root.outerHeight() - header.outerHeight() - 10;
			if (margin > 0){
				console.log("Changed");
				footer.css('margin-top',margin);
			}			
		}
	}
});