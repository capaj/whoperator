/* Quick scroll to anchor fix */
window.addEventListener("hashchange", function() { scrollBy(0, -60) })

$(".nav .current-song").click(function () {
    $("#now-playing").fadeToggle(600);
});