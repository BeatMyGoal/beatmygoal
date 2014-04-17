$(document).ready(function() {

	var page = 0;
    var query = "";
	var scroll_activated = false;

    get_goals_ajax(page, query);
    $('#dashboard_search').keyup(function() {
        query = $('#dashboard_search').val();
        console.log(query);
        page = 0;
        $(".dashcard-container").empty();
        get_goals_ajax();
    });
	$(window).scroll(function() {
	   if($(window).scrollTop() + $(window).height() == $(document).height() && !scroll_activated) {
	        scroll_activated = true;
            get_goals_ajax();
			scroll_activated = false;
	   }
	});
    $(".dashcard-container").on({
        mouseenter: function () {
            var currid = $(this).attr('id');
            console.log(currid);
            $('#'+currid+'.dashcard-overlay').css("background-color","rgba(100,100,100,0.8)");
            $('#'+currid+'.join-button').css("display","inline");
        },
        mouseleave: function () {
            var currid = $(this).attr('id');
            console.log(currid);
            $('#'+currid+'.dashcard-overlay').css("background-color","rgba(100,100,100,0.1)");
            $('#'+currid+'.join-button').css("display","none");
        }
    }, ".dashcard-overlay");

    function get_goals_ajax(){
        var data = {
            page: page,
            query: query,
        };
        $.ajax({
            type: "POST",
            url: "/dashboard",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
        }).done(function(data) {
            goals = jQuery.parseJSON(data['goals']);
            goals.forEach(function(entry) {
                //console.log(entry);
                fields = entry['fields'];
                user = $(".users>#id"+fields['creator']);
                //console.log(user);
                $(".dashcard-container").append('<li><div class="dashcard-holder" id="'+entry['pk']+'"></div></li>');
                $(".dashcard-holder#"+entry['pk']).empty();
                $(".dashcard-holder#"+entry['pk']).append('<div class="dashcard" id="'+entry['pk']+'"></div>');
                $("#"+entry['pk']+".dashcard").append('<div class=dashcard-img></div>');
                $("#"+entry['pk']+".dashcard").append('<div class=dashcard-title><a href="/goals/'+entry['pk']+'">'+fields['title']+'</a></div>');
                $("#"+entry['pk']+".dashcard").append('<div class=dashcard-creator><b>Creator:</b> <a href="/users/'+fields['creator']+'">'+user.text()+'</a></div>');
                $("#"+entry['pk']+".dashcard").append('<div class=dashcard-prize><b>Prize:</b> '+fields['prize']+'</div>');
                $("#"+entry['pk']+".dashcard").append('<div class=dashcard-description>'+fields['description']+'</div>');
                $("#"+entry['pk']+".dashcard-holder").append('<div class="dashcard-overlay" id="'+entry['pk']+'"></div>');
                $("#"+entry['pk']+".dashcard-overlay").append('<a href="/goals/'+entry['pk']+'" class="button join-button" id="'+entry['pk']+'">Join Goal</a>');
            });
        }).fail(function(data) {
            console.log(data);
            alert("failure");
        });
        page = page + 1;
    }
});
