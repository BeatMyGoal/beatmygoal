$(document).ready(function() {
	$fname = $("#editForm #fname");
	$lname = $("#editForm #lname");
	$username = $("#editForm #username");
	$email = $("#editForm #email");

	uid = window.location.pathname.split("/")[2];
	
	$("#save").click(function(event) {
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
			console.log(data.redirect);
			if (data.errCode >= 0) {
				window.location.href = data.redirect;
			}
		}).fail(function(data) {
			alert("failure");
		});
	});

	$("#cancel").click(function(event) {
		/* Act on the event */
	});
});