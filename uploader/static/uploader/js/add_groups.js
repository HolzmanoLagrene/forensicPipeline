$('ul.dropdown-menu.reddy').on('click', function (event) {
    event.stopPropagation();
});

$("#createnew").on("click", function () {
    var $dropdown = $(".dropdown-menu.reddy");

    var $listingName = $("#listingname");
    var listingNameLabel = $listingName.val();
    $.ajax({
        type: "POST",
        url: "add_group",
        async: true,
        data: listingNameLabel
    });
});