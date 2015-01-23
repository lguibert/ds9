$(document).ready(function(){
	$(".controllerCheckboxs").click(function(){
		$('+ .checkboxsSelect input[type="checkbox"]',this).each(function(){
			if($(this).prop("checked") == true){
				$(this).prop("checked",false);
			}else{
				$(this).prop("checked",true);
			}			
		});
	});
});