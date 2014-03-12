$(document).ready(function() {

	$title = $('#editForm #title');
	$description = $('#editForm #description')
	gid = window.location.pathname.split("/")[2];

	$("#save").click(function(event) {
		console.log("test");
		var title = $title.val();
		var description = $description.val();
		var data = {
			title: title,
			description: description
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
		window.location.href = "/goals/" + gid;
	});


});