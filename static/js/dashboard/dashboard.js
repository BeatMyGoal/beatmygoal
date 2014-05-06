$(document).ready(function() {
    var delay = (function(){
      var timer = 0;
      return function(callback, ms){
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
      };
    })();

	var page = 0;
    var query = "";
    var filter = "all"; 
	var scroll_activated = false;
    var is_searching = false;

    get_goals_ajax();
    $('#dashboard_search').keyup(function() {
        delay(function(){
            is_searching = true;
            query = $('#dashboard_search').val();
            // console.log(query);
            page = 0;
            $(".dashcard-container").empty();
            get_goals_ajax();
            is_searching = false;
        }, 200 );
    });
	$(window).scroll(function() {
	   if($(window).scrollTop() + $(window).height() == $(document).height() && !is_searching && !scroll_activated) {
	        scroll_activated = true;
            get_goals_ajax();
			scroll_activated = false;
	   }
	});
    $(".dashcard-container").on({
        click: function () {
            var goal_id = $(this).attr('id');
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
                // console.log(data);
                if (data.errors.length === 0) {
                    // console.log(data);
                    window.location.href = data.redirect;
                } 
            }).fail(function(data) {
                // console.log(data);
//                alert("failure");
            });
        }
    }, ".join-button");
    $(".filter-choice").click(function(){
        filter = $(this).attr('id');
        page = 0;
        $(".dashcard-container").empty();
        get_goals_ajax();
        $(".current").removeClass('current');
        $(this).addClass('current');
    });

    $(".dashcard-container").on({
        mouseenter: function () {
            var currid = $(this).attr('id');
            // console.log(currid);
            $('#'+currid+'.dashcard-overlay').css("background-color","rgba(100,100,100,0.8)");
            $('#'+currid+'.join-button').css("display","inline");
            $('#'+currid+'.view-button').css("display","inline");
        },
        mouseleave: function () {
            var currid = $(this).attr('id');
            // console.log(currid);
            $('#'+currid+'.dashcard-overlay').css("background-color","rgba(100,100,100,0.0)");
            $('#'+currid+'.join-button').css("display","none");
            $('#'+currid+'.view-button').css("display","none");
        }
    }, ".dashcard-holder");

    $(".dashcard-container").on({
        click: function () {
            var currid = $(this).attr('id');
            window.location.replace("/goals/"+currid); 
        }
    }, ".dashcard-overlay");

    function get_goals_ajax(){
        var data = {
            page: page,
            query: query,
            filter: filter,
        };
        $.ajax({
            type: "POST",
            url: "/dashboard",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
        }).done(function(data) {
            goals = jQuery.parseJSON(data['goals']);
            if (goals.length===0){
                // $(".dashcard-container").empty();
            }
            else{
                goals.forEach(function(entry) {
                    //console.log(entry);
                    fields = entry['fields'];
                    user = $(".users>#id"+fields['creator']);
                    // console.log(fields) 
                    //console.log(user);
                    $(".dashcard-container").append('<li><div class="dashcard-holder card" id="'+entry['pk']+'"></div></li>');
                    $(".dashcard-holder#"+entry['pk']).empty();
                    $(".dashcard-holder#"+entry['pk']).append('<div class="dashcard" id="'+entry['pk']+'"></div>');
                    $("#"+entry['pk']+".dashcard").append('<div class=dashcard-img id="'+entry['pk']+'"></div>');
                    if (fields['image'] != ""){
                        $("#"+entry['pk']+".dashcard-img").append('<img src="' + window.MEDIA_URL + fields['image']+'" class="goal-image"/>');
                        // hide the trophy
                        $("#"+entry['pk']+".dashcard-img").css("background-image", "none");
                    }
                    $("#"+entry['pk']+".dashcard").append('<div class=dashcard-title><a href="/goals/'+entry['pk']+'">'+fields['title']+'</a></div>');
                    $("#"+entry['pk']+".dashcard").append('<div class=dashcard-creator><b>Creator:</b> <a href="/users/'+fields['creator']+'">'+user.text()+'</a></div>');
                    $("#"+entry['pk']+".dashcard").append('<div class=dashcard-prize><b>Prize:</b> '+fields['prize']+'</div>');
                    $("#"+entry['pk']+".dashcard").append('<div class=dashcard-description>'+fields['description']+'</div>');
                    $("#"+entry['pk']+".dashcard-holder").append('<div class="dashcard-overlay" id="'+entry['pk']+'"></div>');
                    $("#"+entry['pk']+".dashcard-overlay").append('<a href="#" class="button join-button" id="'+entry['pk']+'">Join Goal</a>');
                    $("#"+entry['pk']+".dashcard-overlay").append('<a href="/goals/'+entry['pk']+'" class="button view-button" id="'+entry['pk']+'">View Goal</a>');
                });
            }
        }).fail(function(data) {
            // console.log(data);
//            alert("failure");
        });
        page = page + 1;
    }
});
