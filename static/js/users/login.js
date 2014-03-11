$(document).ready(function() {

	$("#login-form #login").click(function(e) {

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
			if (data.errCode >= 0) {
				window.location.href = data.redirect;
			} 
		}).fail(function(data) {
			alert("fail to login");
		});
	});

        $("#register").click(function(e){
        	window.location.href = "/users/create";
        });

});