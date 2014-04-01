$(document).ready(function() {

	$("#register-submit").click(function(e) {
		var goal_type;
		var ending_date;

		if ($('#deadline').is(":checked")) {
			goal_type = "Time-based";
			ending_date = $('#datepicker').val();
		} else {
			goal_type = "Value-based";
			ending_date = null;
		}
		
		var data = {
			title: $("#register-title").val(),
			description: $("#register-description").val(),
			creator: "come back to this",
			prize: $("#register-prize").val(),
			private_setting: 1.0,
			goal_type: goal_type,
			ending_value: $("#register-end-value").val(),
			unit: $("#register-value-unit").val(),
			ending_date : ending_date
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

	$('.end-time-label').hide();

	
	$('#deadline').change(function() {
		$('.end-time-label').hide();

        if($(this).is(":checked")) {
        	$('.end-time-label').fadeIn();
        }

    });

});


