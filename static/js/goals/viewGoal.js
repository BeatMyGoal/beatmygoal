$(document).ready(function() {



    $('#edit_goal_button').click(function() {
      window.location = window.location.href+"edit";
      return false;
    });

    $('#favorite_button').click(function() {
        console.log('favorite button pushed');
        $(this).toggleClass('alert');
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
                    
                }
            }).fail(function(data) {
                console.log(data);
                alert("failure");
        });

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

