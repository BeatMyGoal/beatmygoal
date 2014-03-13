$(document).ready(function() {
 });


$('#edit_goal_button').click(function() {
  window.location = window.location.href+"edit"
  return false;
});
$('#delete_goal_button').click(function() {
	var goal_id = window.location.pathname.split("/")[2];
	var data = {
		goal_id: goal_id,
	}
	$.ajax({
			type: "POST",
			url: "/goals/remove",
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
			console.log(data);
			if (data.hasOwnProperty("success")) {
				window.location.href = data.redirect;
			} 

		}).fail(function(data) {
			console.log(data);
			alert("failure");
		});

});
$('#join_goal_button').click(function() {
	var goal_id = window.location.pathname.split("/")[2];
	console.log(goal_id)
	var data = {
		goal_id: goal_id,
	}
	$.ajax({
			type: "POST",
			url: "/goals/join",
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
			console.log(data);
			if (data.hasOwnProperty("success")) {
				window.location.href = data.redirect;
			} 

		}).fail(function(data) {
			console.log(data);
			alert("failure");
		});

});