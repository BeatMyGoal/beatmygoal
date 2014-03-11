$(document).ready(function() {

	$("#register-submit").click(function(e) {

		var data = {
			username: $("#register-username").val(),
			password: $("#register-password").val(),
			email: $("#register-email").val(),
		};

		$.ajax({
			type: "POST",
			url: "/users/create",
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
			console.log(data);
			if (data.hasOwnProperty("success")) {
				window.location.href = data.redirect;
			} else {
				if ('errors' in data) {
					var errors = data.errors;
					if ('username' in errors) {
						$('#username-error').text(data.errors.username).css("display", "block");

					}
					if ('email' in errors) {
						$('#email-error').text(data.errors.email).css("display", "block");

					}
					if ('password' in errors) {
						$('#password-error').text(data.errors.password).css("display", "block");

					}
				}
			}

		}).fail(function(data) {
			alert("failure");
		});
	});

});