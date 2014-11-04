$(document).ready(function(){

	function showSelector(selector, speed){
		if(speed){
			$(selector).show(speed);
		}else{
			$(selector).show();
		}		
	}

	function hideSelector(selector, speed){
		if(speed){
			$(selector).hide(speed);
		}else{
			$(selector).hide();
		}
	}

	$('#displayCatData').unbind().click(function(){
        if ($(this).attr('type') == 0){
        	showSelector('#dataCatContainer', "slow");
        	$(this).attr('type','1');
        	$(this).html('See less');
        }else{
          hideSelector('#dataCatContainer', "slow");
          $(this).attr('type','0');
          $(this).html('See more');
        }
    })    

	$('#id_showPass').on("click",function(){
		if ($(this).prop("checked")){
			showSelector('#id_password');
			showSelector('#id_passwordCheck');
			showSelector("label[for='id_password']");
			showSelector("label[for='id_passwordCheck']");
		}else{
			hideSelector('#id_password');
			hideSelector('#id_passwordCheck');
			hideSelector("label[for='id_password']");
			hideSelector("label[for='id_passwordCheck']");
		}
	})

	if($('#id_showPass').is(':checked')){
		showSelector('#id_password');
		showSelector('#id_passwordCheck');
		showSelector("label[for='id_password']");
		showSelector("label[for='id_passwordCheck']");
	}


	$("#btnDisplayRef").unbind().click(function(){
		if ($(this).attr('type') == 0){
        	$(this).attr('type','1');
        	$(this).html('Hide reference');
        	showSelector('#refSpectra', "slow");
        }else{
        	$(this).attr('type','0');
        	$(this).html('Show reference');
        	hideSelector('#refSpectra', "slow");
        	$("input[name='choiseRef']:checked").prop("checked",false);
        }
	});
})