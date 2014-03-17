$(document).ready(function() {
 });


$('#edit_goal_button').click(function() {
  window.location = window.location.href+"edit"
  return false;
});

$('#favorite_button').click(function() {
	console.log('favorite button pushed');
	$(this).toggleClass('alert');
})
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
			console.log(data.redirect);
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
	}
	console.log(goal_id);
	$.ajax({
			type: "POST",
			url: "/goals/leave",
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
			console.log(data);
			if (data.hasOwnProperty("success")) {
				console.log(data);
				window.location.href = data.redirect;
			} 

		}).fail(function(data) {
			console.log(data);
			alert("failure");
		});

});