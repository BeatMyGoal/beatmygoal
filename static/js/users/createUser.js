$(document).ready(function() {
    
    $("#register-submit").click(function(e) {
	console.log("clicked!");
        //e.preventDefault();
        //e.stopPropagation();

	var data = {
	    username : $("#register-username").val(),
	    password : $("#register-password").val(),
	    email: $("#register-email").val(),
	};

	$.ajax({
	    type: "POST",
	    url: "",
	    data: JSON.stringify(data),
	    contentType: "application/json",
	    dataType: "json",
	}).done(function(data) {
		console.log(data);
	    if (data.hasOwnProperty("success")) {
			console.log(data.redirect);
			window.location.href = data.redirect;   
	    } else {
		// show the errors
	    }
	    
	}).fail(function(data) {
	    alert("failure");
	});
    });
    
});
