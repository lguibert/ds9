$(document).ready(function(){
	$('#formSelection').submit(function(){
		//getState();
	});	
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

function getState(){
	var csrftoken = getCookie('csrftoken');

	$.ajax({
		url : "/ds9s/reviews/getStateDownload/",
		type: "POST",
		cache: true,
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	        
	        //$(".disableCharge").prop("disabled",true);
	        //$("*").css("cursor","progress");
	    }
	    })
		.success(function(data){
			state = $.parseJSON(data)

			if (state == false){
				$("#btnExport").prop('disabled', true);
				$("body").css('background-color','red');
			}else{
				$("#btnExport").prop('disabled', false);
				$("body").css('background-color','yellow');
			}
				
	    }).complete(function(){
	    	//$(".disableCharge").prop("disabled",false);
	    	//deleteStyle();
	    	//clearTimeout(tOut);
	    });

	var tOut = setTimeout(getState,10);
} 