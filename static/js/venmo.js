$(document).ready(function() {
	var tt;
	$('#button').click(function(e){
		var url = 'https://api.venmo.com/v1/me?access_token=';
		var token = document.getElementById("userinfo").value;
		var url = url.concat(token);
		alert(token);
		$.ajax({
			type: "GET",
			url: 'https://sandbox-api.venmo.com/payments?user_id=145434160922624933&amount=0.20&note=beatmygoal&audience=private&access_token=ZzujwuryWUqwhKQ6R9rB2xXbvWRhgc8Q',
			dataType: "json",
		}).done(function(data) {
			document.getElementById("userinfo").innerHTML = data;
			tt = data.refresh_token;
		}).fail(function(data) {
			alert("failure");
		});
	});



	$('#second').click(function(e){
		var token = document.getElementById("userinfo").value;
		alert(document.getElementById("userinfo").value);
		var data = {
					access_token : token,
					email : "venmo@venmo.com",
					note : "A message to accompany the payment.",
					amount : 0.10,
		};
		$.ajax({
			type: "POST",
			url: 'https://sandbox-api.venmo.com/v1/payments',
			data: data,
			dataType: "json",
		}).done(function(data) {
			document.getElementById("userinfo").innerHTML = data;
		}).fail(function(data) {
			alert("failure");
		});
	});


});
