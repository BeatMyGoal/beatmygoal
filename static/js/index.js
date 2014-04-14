$(document).ready(function() {
	console.log(request)
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
			if (data.errors.length === 0) {
				window.location.href = data.redirect;
			} else {
				if (data.errors.length > 0) {
					var errors = data.errors;
					if (errors.indexOf(ERRCODES.CODE_DUPLICATE_USERNAME) >= 0) {
						$('#register-form #username-error').text("Sorry, that username has already been used");
						$('#register-form label[for="username"]').addClass('error');

					}
					if (errors.indexOf(ERRCODES.CODE_DUPLICATE_EMAIL) >= 0) {
						$('#register-form #email-error').text("Sorry, that email has already been used");
						$('#register-form label[for="email"]').addClass('error');

					}
					if (errors.indexOf(ERRCODES.CODE_BAD_PASSWORD) >= 0) {
						$('#register-form #password-error').text("Invalid password");
						$('#register-form label[for="email"]').addClass('error');
					}
				}
			}

		}).fail(function(data) {
			alert("failure");
		});
	});

});
