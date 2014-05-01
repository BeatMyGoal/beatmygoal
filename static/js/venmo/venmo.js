$(document).ready(function() {
	var tt;
	

	$('#payment').click(function(e){
		var giver = document.getElementById("giver").value;
		var receiver = document.getElementById("receiver").value;
		var amount = document.getElementById("amount").value;

		alert("Processing Payment");

		var data = {
					giver : giver,
					receiver : receiver,
					amount : amount,
		};

		$.ajax({
			type: "POST",
			url: '/payment',
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
			alert("payment completed")
		}).fail(function(data) {
			alert("payment failure");
		});
	});




});
