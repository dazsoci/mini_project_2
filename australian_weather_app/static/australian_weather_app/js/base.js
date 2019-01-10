$(document).ready(() => {
    var path = window.location.pathname;
    $('a[href="'+ path +'"].nav-link')
    .parent().addClass('active');
    $('a.nav-link').filter(() => {
         return this.href == path;
    }).parent().addClass('active');
});