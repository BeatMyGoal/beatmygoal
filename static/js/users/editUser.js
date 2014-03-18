$(document).ready(function() {
	$fname = $("#editForm #fname");
	$lname = $("#editForm #lname");
	$username = $("#editForm #username");
	$email = $("#editForm #email");

	uid = window.location.pathname.split("/")[2];
	
	$("#editForm #save").click(function(e) {
		e.preventDefault();

		var invalid_fields = $("#editForm").find('[data-invalid]');
		console.log(invalid_fields);
		if (invalid_fields.length > 0) {
			return;
		}

		console.log("test");
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
		console.log(data);

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
			alert("failure");
		});
	});

	$("#editForm #delete").click(function(e) {
		console.log(uid);
		$.ajax({
			type: "POST",
			url: "/users/" + uid + "/delete",
			contentType: "application/json",
			dataType: "json"
		}).done(function(data) {
			window.location.href = data.redirect;
		}).fail(function(){
			alert("failed to delete");
		});
	});

	$("#editForm #cancel").click(function(e) {
		window.location.href = "/users/" + uid;
	});
});
