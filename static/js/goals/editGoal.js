$(document).ready(function() {

	$title = $('#editForm #title');
	$description = $('#editForm #description');
	$password = $('#editForm #password');
	$prize = $('#editForm #prize');
	$ending_value = $('#editForm #ending_value');
	$unit = $('#editForm #unit');

	gid = window.location.pathname.split("/")[2];


	var deleteAction = function() {
        var goal_id = window.location.pathname.split("/")[2];
        var data = {
           goal_id: goal_id,
        };
        $.ajax({
                type: "POST",
                url: "/goals/remove",
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: "json",
            }).done(function(data) {
                console.log(data);
                console.log(data.redirect);
                if (data.errors.length === 0) {
                    window.location.href = data.redirect;
                } 
            }).fail(function(data) {
                console.log(data);
//                alert("failure");
        });

    };

	var saveAction = function(event) {
        event.preventDefault();
  
        var invalid_fields = $("#editForm").find('[data-invalid]');
        if (invalid_fields.length > 0) {
            return;
        }
        
		var title = $title.val();
		var description = $description.val();
		var prize = $prize.val();
		var ending_value = $ending_value.val();
		var unit = $unit.val();

		var data = {
			title: title,
			description: description,
			prize: prize,
			ending_value: ending_value,
			unit: unit
		};

		$.ajax({
			type: "POST",
			url: "",
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
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
                    if (errors.indexOf(ERRCODES.CODE_BAD_ENDING_VALUE) >= 0) {
                        console.log("here");
                        $('#end-value-error').text("Ending value must be specified with number");
                        $("label[for='ending_value']").addClass("error");
                    }

				}
			}
		}).fail(function(data) {
//			alert("failure");
		});
	};

	$("#cancel").click(function(event) {
		window.location.href = "/goals/" + gid;
	});

	$("#firstModal #No_button").click(function(e) {
	$('#firstModal').foundation('reveal', 'close');
	});


	$("#reveal_save #Back_button").click(function(e) {
        $('#reveal_save').foundation('reveal', 'close');
    });

    $("#save").click(function(e){
        e.preventDefault();
        var invalid_fields = $("#editForm").find('[data-invalid]');
        if (invalid_fields.length > 0) {
            return;
        } else {
            $('#reveal_save').foundation('reveal', 'open');
        }
    });


    $("#reveal_save #Confirm_button").click(function(e) {
        var password = $('#reveal_save #password').val();
        var data = {
            password: password
        };

        var invalid_fields = $("#editForm").find('[data-invalid]');
        if (invalid_fields.length > 0) {
            $('#reveal_save').foundation('reveal', 'close');
            return;
        }

        $.ajax({
            type: "POST",
            url: "/confirm/",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
        }).done(function(data) {

            console.log(data);
            if (data.errors.length === 0) {
                saveAction(e);
            } else {
                if (data.errors.length >= 0) {
                    var errors = data.errors;
                    if (errors.indexOf(ERRCODES.CODE_BAD_PASSWORD) >= 0) {
                            $('#password-error').text('Validation failed');
                            $("label[for='password']").addClass("error");
                        }
                }
            }
        }).fail(function(data) {
//            alert("failure");
        });
    });

    $("#firstModal #Yes_button").click(function(e) {
        var password = $('#firstModal #password').val();
        var data = {
            password: password
        };

        $.ajax({
            type: "POST",
            url: "/confirm/",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
        }).done(function(data) {

            console.log(data);
            if (data.errors.length === 0) {
                deleteAction(e);
            } else {
                if (data.errors.length >= 0) {
                    var errors = data.errors;
                    if (errors.indexOf(ERRCODES.CODE_BAD_PASSWORD) >= 0) {
                            $('#password-error').text('Validation failed');
                            $("label[for='password']").addClass("error");
                        }
                }
            }
        }).fail(function(data) {
//            alert("failure");
        });
    });
});




