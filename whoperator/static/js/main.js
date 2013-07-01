/* Quick scroll to anchor fix */
window.addEventListener("hashchange", function() { scrollBy(0, -60) })

$('a[href="#logModal"]').on('click', showLog);

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
                callback(template, data);
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
function showLog() {
    $.getJSON('/log',
        function(data) {
            var json_log = data;
            $.ajax({
                url: '/static/tpl/log.handlebars',
                success: function(data) {
                    template  = Handlebars.compile(data);
                    var html = template(json_log);
                    $('#logModal .modal-body ul').html(html);
                }
            });
        }
    );
}