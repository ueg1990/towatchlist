$('document').ready(function(){
	var checkboxes = $("input[type='checkbox']")
	checkboxes.click(function() {
		$('#seen').prop('disabled', !checkboxes.is(":checked"));
		$('#delete').prop('disabled', !checkboxes.is(":checked"));
	});

});


function onClickSeen() {
	/* declare an checkbox array */
	var chkArray = [];
	
	/* look for all checkboes that have a class 'chk' attached to it and check if it was checked */
	$( 'input[name="link"]:checked' ).each(function() {
		chkArray.push($(this).val());
	});
	
	/* we join the array separated by the comma */
	var selected;
	selected = chkArray.join(',');

	//alert("You have selected " + selected)

	$.ajax({type: "POST",
                url: "/set-seen",
                data: { 'selected': selected },
                success:function(result){
         			location.reload(true);
        	}});
}

function onClickDelete() {
	/* declare an checkbox array */
	var chkArray = [];
	
	/* look for all checkboes that have a class 'chk' attached to it and check if it was checked */
	$( 'input[name="link"]:checked' ).each(function() {
		chkArray.push($(this).val());
	});
	
	/* we join the array separated by the comma */
	var selected;
	selected = chkArray.join(',');

	//alert("You have selected " + selected)

	$.ajax({type: "POST",
                url: "/delete-links",
                data: { 'selected': selected },
                success:function(result){
         			location.reload(true);
        	}});
}