$(document).ready(function() {


    $('#add_favorite_button').click(function() {
        var goal_id = window.location.pathname.split("/")[2];
        var data = {
            goal_id: goal_id,
        };
        $.ajax({
            type:"POST",
            url: "/goals/goal_add_favorite",
            data: JSON.stringify(data),
            contentType: "json",
        }).done(function(data) {
            console.log(data.errors);
            if (data.errors.length === 0) {
                window.location.href = data.redirect;
            }
            console.log(data.errors);
        }).fail(function(data) {
            alert("failure");
        });

    });

    $('#remove_favorite_button').click(function() {
        var goal_id = window.location.pathname.split("/")[2];
        var data = {
            goal_id: goal_id,
        };
        $.ajax({
            type:"POST",
            url: "/goals/goal_remove_favorite",
            data: JSON.stringify(data),
            contentType: "json",
        }).done(function(data) {
            console.log(data.errors);
            if (data.errors.length === 0) {
                window.location.href = data.redirect;
            }
            console.log(data.errors);
        }).fail(function(data) {
            alert("failure");
        });
    });


    $('#edit_goal_button').click(function() {
      window.location = window.location.href+"edit";
      return false;
    });


    $('#join_goal_button').click(function() {
        var goal_id = window.location.pathname.split("/")[2];
        var data = {
            goal_id: goal_id,
        };
        $.ajax({
                type: "POST",
                url: "/goals/join",
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: "json",
            }).done(function(data) {
                console.log(data);
                if (data.errors.length === 0) {
                    console.log(data);
                    window.location.href = data.redirect;
                } 

            }).fail(function(data) {
                console.log(data);
                alert("failure");
            });

    });

    $('#leave_goal_button').click(function() {
        var goal_id = window.location.pathname.split("/")[2];
        var data = {
            goal_id: goal_id,
        };
        console.log(goal_id);
        $.ajax({
                type: "POST",
                url: "/goals/leave",
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: "json",
            }).done(function(data) {
                console.log(data);
                if (data.errors.length === 0) {
                    console.log(data);
                    window.location.href = data.redirect;
                } 

            }).fail(function(data) {
                console.log(data);
                alert("failure");
            });

    });

    $('#log_progress_form #submit_log_button').click(function(e) {
        e.preventDefault();

        var invalid_fields = $("#log_progress_form").find('[data-invalid]');
        console.log(invalid_fields);
        if (invalid_fields.length > 0) {
            return;
        }
        
        var goal_id = window.location.pathname.split("/")[2];
        var data = {
            amount : $('#log_progress_form #log_amount').val(),
            comment : $('#log_progress_form #log_comment').val(),
        };
        $.ajax({
        type: "POST",
            url: "/goals/" + goal_id + "/log",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            }).done(function(data) {
                console.log(data);
                console.log(data.redirect);
                if (data.errors.length === 0) {
                    window.location.href = data.redirect;
                } else if (data.errors.length > 0) {
                    $("#log-comment-error").text("Invalid comment.");
		    $("#log-comment-error").show();
                }
            }).fail(function(data) {
                console.log(data);
                alert("failure");
        });

    });


    $("#reveal_edit #Back_button").click(function(e) {
        $('#reveal_edit').foundation('reveal', 'close');
    });



    $("#reveal_edit #Confirm_button").click(function(e) {
        var password = $('#reveal_edit #password').val();
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
                window.location = window.location.href+"edit";
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
            alert("failure");
        });
    });


    $("#reveal_email #cancle_button").click(function(e) {
        $('#reveal_email').foundation('reveal', 'close');
    });

    $("#reveal_email #send_button").click(function(e) {
        var to = $('#reveal_email #to').val();
        var goal_id = window.location.pathname.split("/")[2];
        var data = {
            to: to,
            goal_id: goal_id,
        }
        console.log(data);

        $.ajax({
            type: "POST",
            url: "/email/",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
        }).done(function(data) {
            console.log(data.errors);
            if (data.errors.length === 0) {
                window.location = data.redirect;
            }
        }).fail(function(data) {
            alert("failure");
        });
    });



    $("#register-form #back_button").click(function(e) {
        console.log("back")
        $('#reveal_register').foundation('reveal', 'close');
    });



    $("#register-form").submit(function(e) {
        var invalid_fields = $("#register-form").find('[data-invalid]');
        console.log(invalid_fields);
        if (invalid_fields.length > 0) {
            return;
        }
        e.preventDefault();
        e.stopPropagation();
        var goal_id = window.location.pathname.split("/")[2];
        var data = {
            username: $("#register-username").val(),
            password: $("#register-password").val(),
            email: $("#register-email").val(),
            goal: goal_id,
        };
        console.log("pushed");
        $.ajax({
            type: "POST",
            url: "/users/create",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
        }).done(function(data) {
            if (data.errors.length === 0) {
                window.location.href = data.redirect;
            } else {
                if (data.errors.length > 0) {
                    var errors = data.errors;
                    if (errors.indexOf(ERRCODES.CODE_DUPLICATE_USERNAME) >= 0) {
                        $('#register-form #username-error').text("Sorry, that username has already been used");
                        $('#register-form label[for="username"]').addClass('error');

                    }
                    if (errors.indexOf(ERRCODES.CODE_DUPLICATE_EMAIL) >= 0) {
                        $('#register-form #email-error').text("Sorry, that email has already been used");
                        $('#register-form label[for="email"]').addClass('error');
                    }
                    if (errors.indexOf(ERRCODES.CODE_BAD_PASSWORD) >= 0) {
                        $('#register-form #password-error').text("Invalid password");
                        $('#register-form label[for="email"]').addClass('error');
                    }
                }
            }

        }).fail(function(data) {
            alert("failure");
        });
});


});














