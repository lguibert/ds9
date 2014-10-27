$(document).ready(function(){
	$("#scaling").change(function(){
		if(!$.cookie("done")){
			$("#valScaling").val($(this).val());
			scaling($(this).val());	
			$.cookie("done","true");
		}		
	});

	/*$("#valScaling").on("change",function(){
		$("#scaling").val($(this).val());
	})*/

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


	function scaling(val){
		var csrftoken = getCookie('csrftoken');

		url = document.location.href;
		id = url.split("/")[6];

		$.ajax({
			url : "/ds9s/fits/view/"+id+"/?value="+val,
			type: "GET",
			data: {value:val},
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    }
		    })
			.success(function(data){
		    	location.reload();
		    });



	}

	


});
