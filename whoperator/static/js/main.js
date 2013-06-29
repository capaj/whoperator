/* Quick scroll to anchor fix */
window.addEventListener("hashchange", function() { scrollBy(0, -60) })


/* Show Playlist */
$(".nav .current-song").click(function () {
    $("#now-playing").fadeToggle(600);
});


/* Import Template */
function fetch_tpl(path, callback) {
    var source;
    var template;

    $.ajax({
        url: path,
        success: function(data) {
            source    = data;
            template  = Handlebars.compile(source);

            if (callback) {
                callback(template);
            } else {
                $('#content').html(template);
            }
        }
    });
}

//run our template loader with callback

$('#sections a[data-toggle="tab"]').on('shown', function (e) {
    fetch_tpl('/static/tpl/' + $(e.target).attr('data-template') + '.handlebars');
});

$('#sections a:first').tab('show');