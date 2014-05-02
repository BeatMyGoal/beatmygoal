$(document).ready(function() {
	$fname = $("#editForm #fname");
	$lname = $("#editForm #lname");
	$username = $("#editForm #username");
	$email = $("#editForm #email");
	$password = $("#editForm #password");

	uid = window.location.pathname.split("/")[2];
	
	var saveAction = function(e) {
		e.preventDefault();
  
		var invalid_fields = $("#editForm").find('[data-invalid]');
		if (invalid_fields.length > 0) {
			return;
		}

		var fname = $fname.val();
		var lname = $lname.val();
		var username = $username.val();
		var email = $email.val();

		var data = {
			username: username,
			email: email,
			fname: fname,
			lname: lname,
		};

		$.ajax({
			type: "POST",
			url: "",
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
			console.log(data);
			if (data.errors.length === 0) {
				window.location.href = data.redirect;
			} else {
                if (data.errors.length >= 0) {
                    var errors = data.errors;
                    if (errors.indexOf(ERRCODES.CODE_DUPLICATE_USERNAME) >= 0) {
                        $("#username-error").text("Sorry, that username has already been used");
                        $('label[for="username"]').addClass("error");
                    
                    }
                    if (errors.indexOf(ERRCODES.CODE_DUPLICATE_EMAIL) >= 0) {
                        $("#email-error").text("Sorry, that email has already been used");
                        $('label[for="email"]').addClass('error');
                    }
                }
            }
		}).fail(function(data) {
			// alert("failure");
		});
	};

	var deleteAction = function(e) {
		console.log(uid);
		$.ajax({
			type: "POST",
			url: "/users/" + uid + "/delete",
			contentType: "application/json",
			dataType: "json"
		}).done(function(data) {
			window.location.href = data.redirect;
		}).fail(function(){
			// alert("failed to delete");
		});
	};

	$("#cancel").click(function(e) {
		window.location.href = "/users/" + uid;
	});

	$("#reveal_save #Back_button").click(function(e) {
        $('#reveal_save').foundation('reveal', 'close');
    });


    $("#reveal_save #Confirm_button").click(function(e) {
        var password = $('#reveal_save #password').val();
        var data = {
            password: password
        };

        $.ajax({
            type: "POST",
            url: "/confirm/",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
        }).done(function(data) {

            console.log(data);
            if (data.errors.length === 0) {
                saveAction(e);
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
            // alert("failure");
        });
    });

    $("#firstModal #No_button").click(function(e) {
	$('#firstModal').foundation('reveal', 'close');
	});
	
    $("#firstModal #Yes_button").click(function(e) {
        var password = $('#firstModal #password').val();
        var data = {
            password: password
        };

        $.ajax({
            type: "POST",
            url: "/confirm/",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
        }).done(function(data) {

            console.log(data);
            if (data.errors.length === 0) {
                deleteAction(e);
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
            // alert("failure");
        });
    });

});
