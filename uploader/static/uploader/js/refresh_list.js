$(document).ready(function () {
    $.ajaxSetup({cache: false}); // This part addresses an IE bug.  without it, IE will only load the first number and will never refresh
    var my_refresh = setInterval(function () {
        $('#status_').load(' #status_', function () {
            $(this).children().unwrap()
        })
    }, 3000);
});

