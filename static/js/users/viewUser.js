$(document).ready(function() {
	
});

$("#reconfirom_delete_user #Yes_button").click(function(event) {
	var uid = window.location.pathname.split("/")[2];
	$.ajax({
		type: "POST",
		url: "/users/" + uid + "/delete",
		contentType: "application/json",
		dataType: "json"
	}).done(function(data) {
		window.location.href = data.redirect;
	}).fail(function(data) {
		alert("Delete User Fail");
	});

});

$("#reconfirom_delete_user #No_button").click(function(e) {
	$('#reconfirom_delete_user').foundation('reveal', 'close');
});


$("#reveal_edit #Confirm_button").click(function(e) {
    //window.location = window.location.href+"edit";
    //return false;
    var password = $('#reveal_edit #password').val();
    var data = { password: password }

    $.ajax({
        type: "POST",
        url: "/confirm",
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: "json",
    }).done(function(data) {


        if (data.errors.length === 0) {
            window.location = window.location.href+"edit";
        } else {
            if (data.errors.length >= 0) {
                var errors = data.errors;
                if (errors.indexOf(ERRCODES.CODE_BAD_PASSWORD) >= 0) {
                        $('#password-error').text('Validation failed');
                        $("label[for='password']").addClass("error");
                    }
            }
        }
    }).fail(function(data) {
        alert(data);
    });
});

$("#reveal_edit #Back_button").click(function(e) {

    $('#reveal_edit').foundation('reveal', 'close');
    
});
