$(document).ready(function() {

	$('#payment').click(function(e){
		var giver = document.getElementById("giver").value;
		var receiver = document.getElementById("receiver").value;
		var amount = document.getElementById("amount").value;

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
			alert("payment failure : make_payments in view");
		});
	});

	$('#get_vm_token').click(function(e){
		venmo()
	});
	
	function venmo(){
		var url = "https://api.venmo.com/v1/oauth/authorize?client_id=1700&scope=make_payments%20access_profile%20access_email%20access_phone%20access_balance&response_type=code";
		var popOption = "width=400, height=500, left=200, top=200 resizable=no, scrollbars=no, status=no;";
		popupWindow = window.open(url,"",popOption);
	}
	
	$('#vm_logout').click(function(e){
		$.ajax({
			type: "GET",
			url: '/venmo_logout',
			contentType: "application/json",
			dataType: "json",
		}).done(function(data) {
			if (data.errors.length === 0) {
				alert("success : logout from Venmo")
				window.parent.document.getElementById('venmoWindow').contentDocument.location.reload(true);
			}
		}).fail(function(data) {
			alert("failed : logout from Venmo");
		});
		
	});
	


});