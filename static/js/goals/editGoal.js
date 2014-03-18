$(document).ready(function() {

	$title = $('#editForm #title');
	$description = $('#editForm #description');
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
			console.log(data);
			console.log(data.goals);
			if (data.errors.length === 0) {
				window.location.href = data.redirect;
			} else {
				if (data.errors.length >= 0) {
					var errors = data.errors;
					if (errors.indexOf(ERRCODES.CODE_BAD_TITLE) >= 0) {
						$('#title-error').text('Invalid title');
						$("label[for='title']").addClass("error");
					}
					if (errors.indexOf(ERRCODES.CODE_BAD_DESCRIPTION) >= 0) {
						$('#description-error').text('Invalid description');
						$("label[for='description']").addClass("error");
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