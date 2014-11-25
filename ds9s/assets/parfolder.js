$(document).ready(function(){
	$(".parfolderList").click(function(){
		$("#id_name").val($(this).val());
	});

	$("#uploadParForm").submit(function(){
		$("#btnUploadPar").prop("disabled",true);
		$("*").css("cursor","progress");
		return true;
	});
});