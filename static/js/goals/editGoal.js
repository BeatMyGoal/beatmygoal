$(document).ready(function() {

	$title = $('#editForm #title');
	$description = $('#editForm #description');
	$password = $('#editForm #password');
	$prize = $('#editForm #prize');
	$ending_value = $('#editForm #ending_value');
	$unit = $('#editForm #unit');

	gid = window.location.pathname.split("/")[2];


	$('#delete_goal_button').click(function() {
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
                alert("failure");
        });

    });



	$("#save").click(function(event) {
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

				}
			}
		}).fail(function(data) {
			alert("failure");
		});
	});

	$("#cancel").click(function(event) {
		window.location.href = "/goals/" + gid;
	});

	$("#firstModal #No_button").click(function(e) {
	$('#firstModal').foundation('reveal', 'close');
});
});




