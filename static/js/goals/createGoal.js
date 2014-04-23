$(document).ready(function() {
	$('#hidden_tabs').hide();

	$("#register-submit").click(function(e) {
		$('#step4_check').fadeIn();
		$("label[for='prize']").removeClass("error");
		$("label[for='ending']").removeClass("error");
		$("label[for='description']").removeClass("error");
		$("label[for='title']").removeClass("error");
		$("label[for='ending_value']").removeClass("error");
		$("label[for='value_unit']").removeClass("error");

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
					console.log(errors);
					
					if (errors.indexOf(ERRCODES.CODE_BAD_PRIZE) >= 0) {
						$('#prize-error').text("Prize description must exsit and not too long");
                        $("label[for='prize']").addClass("error");
                        $('#step4_check').hide();
                        document.getElementById('step4').click();
					}
					if (errors.indexOf(ERRCODES.CODE_BAD_DEADLINE) >= 0) {
						$('#ending-error').text("Date must be a future value");
                        $("label[for='ending']").addClass("error");
                        $('#step3_check').hide();
                        document.getElementById('step3').click();
					}
					if (errors.indexOf(ERRCODES.CODE_BAD_DESCRIPTION) >= 0) {
						$('#description-error').text("Description is required and can't be too long");
                        $("label[for='description']").addClass("error");
                        $('#step2_check').hide();
                        document.getElementById('step2').click();
					}
					if (errors.indexOf(ERRCODES.CODE_BAD_TITLE) >= 0) {
						$('#title-error').text("Title is required and can't be too long");
                        $("label[for='title']").addClass("error");
						$('#step2_check').hide();
						document.getElementById('step2').click();
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
	
	$('#Collaborative').hide();
	$('#Competitive').hide();
	$('#goal_type').change(function() {
		if (document.getElementById('goal_type').value === "Collaborative") {
			$("label[for='GoalType']").removeClass("error");
			$('#Collaborative').fadeIn();
			$('#Competitive').hide();
		}
		else if (document.getElementById('goal_type').value === "Competitive") {
			$("label[for='GoalType']").removeClass("error");
			$('#Collaborative').hide();
			$('#Competitive').fadeIn();
		} else {
			$('#Collaborative').hide();
			$('#Competitive').hide();
		}

    });
	
	//Check icons
	$('#step1_check').hide();
	$('#step2_check').hide();
	$('#step3_check').hide();
	$('#step4_check').hide();
	
	//previous buttons
	$('#prev_button_step2').click(function(e){
		document.getElementById('step1').click();
		$('#step2_check').hide();
	});
	$('#prev_button_step3').click(function(e){
		document.getElementById('step2').click();
		$('#step3_check').hide();
	});
	$('#prev_button_step4').click(function(e){
		document.getElementById('step3').click();
		$('#step4_check').hide();
	});

	//next buttons
	$('#next_button_step1').click(function(e){
		if (document.getElementById('goal_type').value ==="default") {
			$("label[for='GoalType']").addClass("error");
		} else {
			document.getElementById('step2').click();
			$('#step1_check').fadeIn();
			document.getElementById("selected_goal_type").innerHTML = document.getElementById('goal_type').value;
		}
	});
	$('#next_button_step2').click(function(e){
		if ($("#register-title").val() && $("#register-description").val() 
			&& $("#register-end-value").val() && $("#register-value-unit").val()) {
			document.getElementById('step3').click();
			$('#step2_check').fadeIn();
		}
		if ($("#register-title").val() === "") {
			$("label[for='title']").addClass("error");
		}
		if ($("#register-description").val() === "") {
			$("label[for='description']").addClass("error");
		}
		if ($("#register-end-value").val() === "") {
			$("label[for='ending_value']").addClass("error");
		}
		if ($("#register-value-unit").val() === "") {
			$("label[for='value_unit']").addClass("error");
		}

	});
	$('#next_button_step3').click(function(e){
		if ($('#deadline').is(":checked") && $('#datepicker').val() === "") {
			$("label[for='ending']").addClass("error");
		} else {
			document.getElementById('step4').click();
			$('#step3_check').fadeIn();
		}
	});


});


