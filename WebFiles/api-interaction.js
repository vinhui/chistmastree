$(".alert").hide();
updateSequences();
setInterval(updateSequences, 5000);

$("#sequences").on('click', 'button', function () {
    url = "/set/" + $(this).text();
    if($(this).hasClass("btn-primary")) {
        url = "/stop/";
    }
    $.get(url, function (data, status) {
        updateSequences();
        connectionSuccess();
    })
    .fail(connectionFailed);
});

$(".row").on('click', '#run-sequence-remote', function () {
    $.ajax({
        type: "POST",
        url: "/set/",
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
    $.get("/get/sequences/html", function (data, status) {
        $("#sequences").html(data);
        connectionSuccess();
    })
    .fail(connectionFailed);
}