$(document).ready(function() {
        $('#loginMessage').html("Enter your credentials");
	$("#Login").click(function(e) {

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
			if (data.hasOwnProperty("success")) {
				window.location.href = data.redirect;
			} else {
			    if ('errors' in data) {
				var errors = data.errors;
				if ('username' in errors){
				    $('#loginMessage').html("Invalid Username");
				}
				if ('password' in errors){
				   $('#loginMessage').html("Invalid Password");
				}
			    }
			}
		}).fail(function(data) {
			alert("fail to login");
		});
	});


});