$(document).ready(function() {

	$("#register-submit").click(function(e) {
		var sel = document.getElementById('types');
		var data = {
			title: $("#register-title").val(),
			description: $("#register-description").val(),
			creator: "come back to this",
			prize: $("#register-prize").val(),
			private_setting: 1.0,
			goal_type: sel.options[sel.selectedIndex].value
		};

		$.ajax({
			type: "POST",
			url: "/goals/create",
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
			if (data.hasOwnProperty("success")) {
				window.location.href = data.redirect;
			} else {
				if ('errors' in data) {
					var errors = data.errors;
					if ('title' in errors) {
						$('#title-error').text("Title is required and can't be too long").css("display", "block");

					}
					if ('description' in errors) {
						$('#description-error').text("Description is required and can't be so damn long").css("display", "block");

					}
					if ('prize' in errors) {
						$('#prize-error').text("Prize description must exsit and not so damn long").css("display", "block");

					}
				}
			}

		}).fail(function(data) {
			alert("failure");
		});
	});

});