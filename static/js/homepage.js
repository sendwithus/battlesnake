//STICKY TABS
function sticky_relocate() {
    var window_top = $(window).scrollTop();
    var div_top = $('#sticky-anchor').offset().top;
    if (window_top > div_top) {
        $('#top-bar').addClass('sticky');
        $('#sticky-fix').addClass('active');
    } else {
        $('#top-bar').removeClass('sticky');
        $('#sticky-fix').removeClass('active');
    }
}

$(function () {
    $(window).scroll(sticky_relocate);
    sticky_relocate();
});
