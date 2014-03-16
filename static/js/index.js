$(document).ready(function() {

	$("#register-form").submit(function(e) {
	    var invalid_fields = $("#register-form").find('[data-invalid]');
	    console.log(invalid_fields);
	    if (invalid_fields.length > 0) {
		return;
	    }


	    e.preventDefault();
            e.stopPropagation();

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
						$('#register-form #username-error').text(data.errors.username);
						$('#register-form label[for="username"]').addClass('error');

					}
					if ('email' in errors) {
						$('#register-form #email-error').text(data.errors.email);
						$('#register-form label[for="email"]').addClass('error');

					}
					if ('password' in errors) {
						$('#register-form #password-error').text(data.errors.password);
						$('#register-form label[for="email"]').addClass('error');
					}
				}
			}

		}).fail(function(data) {
			alert("failure");
		});
	});

});
