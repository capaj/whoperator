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






































/*(function(){
    window.Whop = { Models: {}, Collections: {}, Views: {} };
    window.template = function(id){ return _.template( $('#' + id).html()); };

    Whop.Models.Artist = Backbone.Model.extend({
        defaults: {
            name: 'Artist Name',
            wid: 0,
            founded: 'Unknown'
        },
        founded: function(){
            return this.get('name') + ' was founded in ' + this.get('founded');
        }
    });

    Whop.Collections.Artists = Backbone.Collection.extend({
        model: Whop.Models.Artist
    });

    Whop.Views.Artists = Backbone.View.extend({
        tagName: 'ul',
        render: function(){
            this.collection.each(function(artist){
                var artistView = new Whop.Views.Artist({ model: artist });
                this.$el.append(artistView.render().el);
            }, this);
            return this;
        }
    });

    Whop.Views.Person = Backbone.View.extend({
        tagName: 'li',
        template: template('artistTemplate'),
        render: function(){
            this.$el.html( this.template(this.model.toJSON()));
            return this;
        }
    });

    var artistsCollection = new Whop.Collections.Artists([
        {
            name: 'Metallica',
            wid: 123,
            founded: '1981'
        },
        {
            name: 'Megadeth',
            wid: 456
        },
        {
            name: 'Pantera',
            wid: 789,
            founded: '1988'
        }
    ]);

    var artistsView = new Whop.Views.Artist({ collection: artistsCollection });
    $(document.body).append(artistsView.render().el);
})();*/