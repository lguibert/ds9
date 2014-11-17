$(document).ready(function(){
	$("input[name='typeObject']").unbind().click(function(){
		var selecChecked = "input[name='typeObject']:checked"
		if($(selecChecked).val() == "quasar" || $(selecChecked).val() == "galaxyLines"){
			$("#divCheckRef").html("<h1>"+$(this).val().toUpperCase()+"</h1>");
		}else{
			$("#divCheckRef").html('');
		}
	});
});