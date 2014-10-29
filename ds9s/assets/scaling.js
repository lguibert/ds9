$(document).ready(function(){
	$("#scaling").unbind().change(function(){
		$("#valScaling").val($(this).val());
		scaling($(this).val(), $("#colors").val());			
	});

	$("#valScaling").unbind().change(function(){
		$("#scaling").val($(this).val());
		scaling($(this).val(), $("#colors").val());	
	})

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
		    }).error(function(xhr, err){
		    	//alert("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
		    	alert("responseText: "+xhr.responseText);
		    });
	}

	$("#colors").unbind().change(function(){
		scaling($("#scaling").val(), $(this).val());	
	})

	$("#default").unbind().click(function(){
		if($("#scaling").val() != 100 || $("#colors").val() != "Greys-9"){
			$("#scaling").val("100");
			$("#valScaling").val("100");
			$("#colors option[value='Greys-9']").attr("selected",true);
			scaling($("#scaling").val(), $("#colors").val());
		}else{
			alert("Values already at default value");
		}
	})


});