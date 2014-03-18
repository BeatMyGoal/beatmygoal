$(document).ready(function() {
    //$('#loginMessage').html("Enter your credentials");
	$("#login-form #login").click(function(e) {
		e.preventDefault();

		var invalid_fields = $("#editForm").find('[data-invalid]');
		console.log(invalid_fields);
		if (invalid_fields.length > 0) {
			return;
		}
		
		var data = {
			username: $("#username").val(),
			password: $("#password").val(),
		};

		$.ajax({
			type: "POST",
			url: "/users/login",
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
					$('#login-form').addClass("error");
				}
			}
		}).fail(function(data) {
			alert("fail to login");
		});
	});


});