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
        	$(this).html('See less information about this galaxy');
        }else{
          hideSelector('#dataCatContainer', "slow");
          $(this).attr('type','0');
          $(this).html('See more information about this galaxy');
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
        	$("#refSpectra").css("display","inline-block");
        	//showSelector('#refSpectra', "slow");
        }else{
        	$(this).attr('type','0');
        	$(this).html('Show reference');
        	$("#refSpectra").css("display","none");
        	//hideSelector('#refSpectra', "slow");
        	$("input[name='choiseRef']:checked").prop("checked",false);
        }
	});

	function hideLegend(selector){
		if ($(selector).attr('type') == 0){
        	$(selector).attr('type','1');
        	$(selector).html('Hide legend');
        	showSelector('.legendsLines', "slow");
        }else{
        	$(selector).attr('type','0');
        	$(selector).html('Show legend');
        	hideSelector('.legendsLines', "slow");
        }
	}

	$(".legendLine").unbind().click(function(){
		hideLegend(this);
	});

	$("#removeSelec").unbind().click(function(){
		if($("input[name='choiseRef']").is(':checked')){
			$("input[name='choiseRef']:checked").prop("checked",false);
			$("#divRef102").html("");
			$("#divRef141").html("");
			$('#removeSelec .removeImage').hide();
		}
	});

	$(".speWaveTitle").unbind().click(function(){
		if ($(this).attr('type') == 0){
			$(this).attr('type','1');
        	$("+ .speWaveValues", this).show("slow");
        }else{
        	$(this).attr('type','0');
        	$("+ .speWaveValues", this).hide("slow");        	
        }
	});

	$("#scrollToViewAll").unbind().click(function(){
		$(".legendLine").attr('type','1');
		hideLegend($('.legendLine'));
		$(document).scrollTop(300);
	});
})