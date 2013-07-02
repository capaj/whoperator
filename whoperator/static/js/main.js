/* Quick scroll to anchor fix */
window.addEventListener("hashchange", function() { scrollBy(0, -60) })

function jsontpl(json, tpl, where) {
    var tpl_return = [], json_return = [], template;

    $.when(
        $.ajax({
            dataType: "json",
            url: json,
            success: function(data) {
                json_return = data;
            }
        }), $.ajax({
            dataType: "text",
            url: tpl,
            success: function(data) {
                template = Handlebars.compile(data);
            }
        })
    ).done(function(){
        html = template(json_return);
        $(where).html(html);        
    });
}

$('#section_tabs a[data-toggle="tab"]').on('shown', function(e) {
    jsontpl('/log', '/static/tpl/' + $(this).attr('data-template') + '.handlebars', '#' + $(this).attr('data-template'));
});

$('#section_tabs a[data-template="dashboard"]').on('shown', function(e) { });

$('#dashboard').on('shown', function (e) { });

$('#section_tabs a:first').tab('show');

$('a[href="#logModal"]').on('click', jsontpl('/log', '/static/tpl/log.handlebars','#logModal .modal-body'));