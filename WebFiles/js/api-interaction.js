$(document).ready(function() {
    $(".alert").hide();
    updateSequences();
    updatePlaylists();
    setInterval(updateSequences, 5000);
    setInterval(updatePlaylists, 5000);

    $("#sequences").on('click', 'button', function () {
        url = "/set/sequence/" + $(this).text();
        if($(this).hasClass("btn-primary")) {
            url = "/stop/";
        }
        $.get(url, function (data, status) {
            updateSequences();
            updatePlaylists();
            connectionSuccess();
        })
        .fail(connectionFailed);
    });

    $("#playlists").on('click', 'button', function () {
        url = "/set/playlist/" + $(this).text();
        if($(this).hasClass("btn-primary")) {
            url = "/stop/";
        }
        $.get(url, function (data, status) {
            updatePlaylists();
            updateSequences();
            connectionSuccess();
        })
        .fail(connectionFailed);
    });

    $(".row").on('click', '#run-sequence-remote', function () {
        $.ajax({
            type: "POST",
            url: "/set/sequence/",
            data: $("textarea[name='sequence-data']").val()
        }, function(){
            connectionSuccess();
        })
        .fail(connectionFailed);
    });

    function connectionFailed() {
        $(".alert").show();
    }

    function connectionSuccess() {
        $(".alert").hide();
    }

    function updateSequences() {
        $.get("/get/sequences/html/", function (data, status) {
            $("#sequences").html(data);
            connectionSuccess();
        })
        .fail(connectionFailed);
    }

    function updatePlaylists() {
        $.get("/get/playlists/html/", function (data, status) {
            $("#playlists").html(data);
            connectionSuccess();
        })
        .fail(connectionFailed);
    }
});