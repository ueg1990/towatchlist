$('document').ready(function(){
	//var checkboxes = $("input[type='checkbox']")
	// checkboxes.click(function() {
	// 	$('#seen').prop('disabled', !$(this).is(":checked"));
	// 	$('#delete').prop('disabled', !$(this).is(":checked"));
	// });

    $("#links"/*use rather a static parent ID here*/).on("click", "[name=link]", function() {

  var checkboxes = $("[name=link]"); // get all
  $('#seen').prop('disabled', !checkboxes.is(":checked"));
  $('#delete').prop('disabled', !checkboxes.is(":checked"));

});

	user = $(location).attr('href').split('/').slice(-1)[0];
    $.ajax({
    url: '/userdata/' + user,
    type: 'GET',
    success: function (response) {
        var trHTML = '';
  		var is_user = response.is_user;
		if (is_user === true) {
        $.each(response.links, function (i, item) {
            trHTML += '<tr><td style="text-align:center;" class="col-md-2"><input type="checkbox" value='+item.id+' name="link"/></td>' + 
                      '<td class="col-md-8"><a href="'+item.url+'">'+item.name+'</a></td><td style="text-align:center;" class="col-md-2">'+item.date+'</td></tr>';
        });
        $('.todolist').append(trHTML);
    	}
    	else {
    		$.each(response.links, function (i, item) {
            trHTML += '<tr>' + 
                      '<td class="col-md-8"><a href="'+item.url+'">'+item.name+'</a></td><td style="text-align:center;" class="col-md-2">'+item.date+'</td></tr>';
        });
    		 $('.todolist').append(trHTML);
    	}
    }
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