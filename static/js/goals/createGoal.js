$(document).ready(function() {

	$("#register-submit").click(function(e) {
		var sel = document.getElementById('types');
		var data = {
			title: $("#register-title").val(),
			description: $("#register-description").val(),
			creator: "come back to this",
			prize: $("#register-prize").val(),
			private_setting: 1.0,
			goal_type: sel.options[sel.selectedIndex].value,
			unit: $("#register-value-unit").val()
		};

		$.ajax({
			type: "POST",
			url: "/goals/create",
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
			if (data.errors.length === 0) {
				window.location.href = data.redirect;
			} else {
				if ('errors' in data) {
					var errors = data.errors;
					if (errors.indexOf(ERRCODES.CODE_BAD_TITLE) >= 0) {
						$('#title-error').text("Title is required and can't be too long");
                        $("label[for='title']").addClass("error");

					}
					if (errors.indexOf(ERRCODES.CODE_BAD_DESCRIPTION) >= 0) {
						$('#description-error').text("Description is required and can't be too long");
                        $("label[for='description']").addClass("error");
					}
					if (errors.indexOf(ERRCODES.CODE_BAD_PRIZE) >= 0) {
						$('#prize-error').text("Prize description must exsit and not too long");
                        $("label[for='prize']").addClass("error");
					}
				}
			}

		}).fail(function(data) {
			alert("failure");
		});
	});


	$('.value-unit-label').hide();

	$('#types').change(function(e) {
	e.preventDefault();
	var sel = document.getElementById('types');
	if (sel.options[sel.selectedIndex].value == "Value-based") {
		$('.Time-unit-label').hide();
		$('.value-unit-label').fadeIn();
		
	} else if (sel.options[sel.selectedIndex].value == "Time-based") {
		$('.value-unit-label').hide();
		$('.Time-unit-label').fadeIn();
	} else {
		
	}
	
	console.log("type changed");
})

});


