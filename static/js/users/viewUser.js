$(document).ready(function() {
	var uid = window.location.pathname.split("/")[2];

	$("#delete_user_button").click(function(event) {
		$.ajax({
			type: "POST",
			url: "/users/" + uid + "/delete",
			contentType: "application/json",
			dataType: "json"
		}).done(function(data) {
			if (data.errCode >= 0) {
				window.location.href = data.redirect;
				consol.log(url)
			}
		}).fail(function(data) {
			alert("data.errCode");
		})
	});
});

