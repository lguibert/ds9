$(document).ready(function(){
	$(".unbindClick").click(function(){
		if ($(this).prop('disabled')){
			return false;
		}else{
			$(this).prop('disabled',true);
		}		
	});
});