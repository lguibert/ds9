$(document).ready(function(){
	$("input[name='typeObject']").unbind().click(function(){
		var selecChecked = "input[name='typeObject']:checked"
		var value = $(selecChecked).val();

		if(value == "quasar"){
			$("#divCheckRef").html("<h1>"+value.toUpperCase()+"</h1>");
		} 
		else if(value == "galaxyLines"){
			$("#divCheckRef").html("<h1>"+value.toUpperCase()+"</h1>");
		}else if(value == "oneLine"){
			$("#divCheckRef").html("<h3>We selected Halpha by default. But you can change it below.</h3>");
			oneLining();
		}else{
			$("#divCheckRef").html('');
		}


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

	function deleteStyle(){
		$('*[style*="cursor: progress;"]').each(function() {
			var style = $(this).attr("style");
			style = style.replace("cursor: progress;", "");
			$(this).attr("style",style);
		});		
	}

	function oneLining(){
		var csrftoken = getCookie('csrftoken');

		$.ajax({
			url : "/ds9s/oneLining/",
			type: "POST",
			cache: true,
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		        
		        $(".disableCharge").prop("disabled",true);
		        $("*").css("cursor","progress");
		    }
		    })
			.success(function(data){
				data = $.parseJSON(data)
				
				$("#divCheckRef").append(data);		
		    }).complete(function(){
		    	$(".disableCharge").prop("disabled",false);
		    	deleteStyle();
		    });
	} 
});