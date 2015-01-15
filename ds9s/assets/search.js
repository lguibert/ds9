$(document).ready(function(){

	function removeHidden(){
		$('.hidden').each(function(){
			$(this).removeClass('hidden');
		});
	}

	function selectCheckBox(checkbox, actual){
		if(checkbox.prop("checked")){
			checkbox.prop("checked",false);
			actual.removeClass('background-selected');
		}else{
			checkbox.prop("checked",true);
			actual.addClass('background-selected');
		}
	}

	$('#removeAllFilters').click(function(){
		removeHidden();
		$('.searchController').val('');
		$('#selectGal option[value="base"]').prop('selected',true);
	});

	//-------------------------------------- EXPORT --------------------------------------
	/*$('.exportSelection').click(function(){
		$('.selectExport:checked').each(function(){
			alert($(this).parent().parent().attr("name"));			
		});
	});*/

	$('#galaxySelectioner').submit(function(){
		$('.selectExport:checked').each(function(){
			$('<input />').attr('type', 'hidden')
		        .attr('value', $(this).parent().parent().attr("value"))
		        .attr('name', 'selectedGalaxy')
		        .appendTo('#galaxySelectioner');
		});
		
		return true;
	});

	//-------------------------------------- CHECK -- ------------------------------------
	$('tbody').on('click', '.lines', function(){
		var checkbox = $(this).find('.selectExport');
		var that = $(this);
		selectCheckBox(checkbox, that);
	});

	$('tbody').on('click', '.selectExport', function(){
		var that = $(this);
		if(that.prop("checked")){
			that.prop("checked",false);
			that.parent().parent().removeClass('background-selected');
		}else{
			that.prop("checked",true);
			that.parent().parent().addClass('background-selected');
		}
	});


	//-------------------------------------- REDSHIFT --------------------------------------

	$('#submitIntervalRedshift').click(function(){
		var min = $('#minRedshift').val();
		var max = $('#maxRedshift').val();
		removeHidden();

		$('.hutRedshift').each(function(){
			var value = $(this).html();

			if(value< min || value >max){
				$(this).parent().addClass("hidden");
			}
		});
	});

	//-------------------------------------- X --------------------------------------

	$('#submitIntervalX').click(function(){
		var min = $('#minX').val();
		var max = $('#maxX').val();
		removeHidden();

		$('.hutX').each(function(){
			var value = $(this).html();

			if(value< min || value >max){
				$(this).parent().addClass("hidden");
			}
		});
	});


	//-------------------------------------- Y --------------------------------------

	$('#submitIntervalY').click(function(){
		var min = $('#minY').val();
		var max = $('#maxY').val();
		removeHidden();

		$('.hutY').each(function(){
			var value = $(this).html();

			if(value< min || value >max){
				$(this).parent().addClass("hidden");
			}
		});
	});

	//-------------------------------------- headerSelector --------------------------------------
	$("#headerSelector").click(function(){
		var that = $(this);
		var type = $(this).attr('type');

		if(type == 'undone'){
			that.html('Unselect everything');
			$('.selectExport').each(function(){
				$(this).prop("checked",true);
				$(this).parent().parent().addClass('background-selected');
			});

			that.attr("type",'done');
		}else{
			that.html('Select everything');
			$('.selectExport').each(function(){
				$(this).prop("checked",false);
				$(this).parent().parent().removeClass('background-selected');
			});
			that.attr("type",'undone');
		}
	});

	//-------------------------------------- SELECT PRECISE --------------------------------------
	$("#submitSelectGalPerso").click(function(){
		var galId = $('#galId').val();
		var fieldId = $('#fieldId').val();

		if(galId == null || fieldId == null){
			alert('Both fields are required.');
		}else{
			$('tbody').find(".lines .galsids[value='"+galId+"'] + .fieldsids[value='"+fieldId+"']").each(function(){
				selectCheckBox($(this).parent().find('.selectExport'),$(this).parent());
			});
		}
	});

	$("#submitSelectGal").click(function(){
			var ids = $('#selectGal').val();
			var splited = ids.split('-');

			var galId = splited[0];
			var fieldId = splited[1];

			$('tbody').find(".lines .galsids[value='"+galId+"'] + .fieldsids[value='"+fieldId+"']").each(function(){
				selectCheckBox($(this).parent().find('.selectExport'),$(this).parent());
			});
		});
});