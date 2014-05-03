$(document).ready(function() {

	$("#login-page #login").click(function(e) {

		var data = {
			username: $("#login-page #username").val(),
			password: $("#login-page #password").val(),
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
			} else if (data.errors.length >= 0) {
                $('#login-page').addClass("error");
            }
		}).fail(function(data) {
			// alert("fail to login");
		});
	});

        $("#register").click(function(e){
            window.location.href = "/users/create";
        });

});