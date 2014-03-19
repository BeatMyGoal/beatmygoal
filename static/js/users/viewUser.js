$(document).ready(function() {
	var uid = window.location.pathname.split("/")[2];

	$("#delete_user_button").click(function(event) {
		$.ajax({
			type: "POST",
			url: "/users/" + uid + "/delete",
			contentType: "application/json",
			dataType: "json"
		}).done(function(data) {
			window.location.href = data.redirect;
		}).fail(function(data) {
			alert("Delete User Fail");
		});
	});
});

$("#firstModal #No_button").click(function(e) {
	$('#firstModal').foundation('reveal', 'close');
});

