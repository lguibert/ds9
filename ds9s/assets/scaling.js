$(document).ready(function(){
	$(".unsubmitable").submit(function(e){
		return false;
	});

	$("#scaling").unbind().change(function(){
		$("#valScaling").val($(this).val());
		scaling($(this).val(), $("#colors").val());			
	});

	$("#valScaling").unbind().change(function(){
		$("#scaling").val($(this).val());
		scaling($(this).val(), $("#colors").val());	
	});

	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
		return cookieValue;
	}

	function csrfSafeMethod(method) {
    	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}


	function scaling(val,color){
		var csrftoken = getCookie('csrftoken');

		url = document.location.href;
		id = url.split("/")[6];

		$.ajax({
			url : "/ds9s/fits/scaling/"+id+"/"+val+"/"+color+"/",
			type: "POST",
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		        $(".disableCharge").prop("disabled",true);
		    }
		    })
			.success(function(data){
				data = $.parseJSON(data)
				var f110script = data[0];
				var f110div = data[1];
				var f160script = data[2];
				var f160div = data[3];

				$("#f110").html(f110div);
				$("#f160140").html(f160div);
				$("#scrF110").html(f110script);
				$("#scrf160140").html(f160script);
		    }).complete(function(){
		    	$(".disableCharge").prop("disabled",false);
		    }).error(function(xhr, err){
		    	//alert("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
		    	alert("responseText: "+xhr.responseText);
		    });
	}

	$("#colors").unbind().change(function(){
		scaling($("#scaling").val(), $(this).val());	
	})

	$("#default").unbind().click(function(){
		if($("#scaling").val() != 150 || $("#colors").val() != "Greys-9"){
			$("#scaling").val("150");
			$("#valScaling").val("150");
			$("#colors option[value='Greys-9']").attr("selected",true);
			scaling($("#scaling").val(), $("#colors").val());
		}else{
			alert("Values already at default value");
		}
	})
// --------------------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------------------

	$(".wavelengh").unbind().change(function(){
		$(".valWavelengh").val($(this).val());
		$(".wavelengh").val($(this).val());
		wavelenghing($(this).val());			
	});

	$(".valWavelengh").unbind().change(function(){
		var val = $(this).val();
		$(".wavelengh").val(val);
		$(".valWavelengh").val(val);

		wavelenghing(val);		
	});

	function wavelenghing(redshift){
		var csrftoken = getCookie('csrftoken');

		url = document.location.href;
		id = url.split("/")[6];

		$.ajax({
			url : "/ds9s/fits/wavelenghing/"+id+"/"+redshift+"/",
			type: "POST",
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		        $(".disableCharge").prop("disabled",true);
		    }
		    })
			.success(function(data){
				data = $.parseJSON(data)
				var g1script = data[0];
				var g1div = data[1];
				var g2script = data[2];
				var g2div = data[3];
				var srcDat102 = data[4];
				var divDat102 = data[5];
				var srcDat141 = data[6];
				var divDat141 = data[7];

				$("#g102").html(g1div);
				$("#g141").html(g2div);
				$("#datG102").html(divDat102);
				$("#datG141").html(divDat141);


				$("#scrG102").html(g1script);
				$("#scrG141").html(g2script);
				$("#scrG102Dat").html(srcDat102);
				$("#scrG141Dat").html(srcDat141);
		    }).complete(function(){
		    	$(".disableCharge").prop("disabled",false);
		    });/*.error(function(xhr, err){
		    	//alert("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
		    	alert("responseText: "+xhr.responseText);
		    });*/
	}

	$(".defaultWave").unbind().click(function(){
		if($(".valWavelengh").val() != 1 || $(".wavelengh").val() != 1){
			$(".valWavelengh").val("1");
			$(".wavelengh").val("1");
			wavelenghing($(".wavelengh").val());
		}else{
			alert("Value already at default value");
		}
	})



});


