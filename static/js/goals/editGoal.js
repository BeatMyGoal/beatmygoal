$(document).ready(function() {

	$title = $('#editForm #title');
	$description = $('#editForm #description')
	gid = window.location.pathname.split("/")[2];

	$("#save").click(function(event) {
		var title = $title.val();
		var description = $description.val();
		var data = {
			title: title,
			description: description
		};

		$.ajax({
			type: "POST",
			url: "",
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
			console.log(data)
			if (data['success']) {
				window.location.href = data.redirect;
			} else {
				if ('errors' in data) {
					var errors = data.errors;
					if ('title' in errors) {
						$('#title-error').text('Invalid title').css("display", "block");
					}
					if ('description' in errors) {
						$('#description-error').text('Invalid description').css("display", "block")
					}
				}
			}
		}).fail(function(data) {
			alert("failure");
		});
	});

	$("#cancel").click(function(event) {
		window.location.href = "/goals/" + gid;
	});


});