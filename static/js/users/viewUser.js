function showfileButton(){
    $('#dummyContainer').show();
}
function hidefileButton(){
    $('#dummyContainer').hide();
}
function submitimage(){
    $('#imagesubmitbutton').click();
}
$(document).ready(function() {
    $("#imdummy").click(function(event) {
        $("#imagebutton").click();
    });

    $("#Edit_User_button").click(function(e) {
        window.location = window.location.href+"edit";
    })
});


