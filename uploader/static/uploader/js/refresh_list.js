$(document).ready(function () {
    $.ajaxSetup({cache: false}); // This part addresses an IE bug.  without it, IE will only load the first number and will never refresh
    var my_refresh = setInterval(function () {
        $('td[id^="status_"]').each(function () {
            $(this).load(" #"+$(this).attr("id"))
        });
    }, 3000);
});

