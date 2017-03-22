function viewGames() {
    if($("#gametable").is(":visible")) {
        $("#gametable").slideUp(400);
    } else {
        $("#gametable").slideDown(400);
        $("#usertable").hide(400);
    }
}

function viewUsers() {
    if($("#usertable").is(":visible")) {
        $("#usertable").slideUp(400);
    } else {
        $("#gametable").hide(400);
        $("#usertable").slideDown(400);
    }
}
