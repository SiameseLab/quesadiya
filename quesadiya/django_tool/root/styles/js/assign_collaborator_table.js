
$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
    var actions = $("table td:last-child").html();
    $(document).on("click", ".edit", function () {
        $(this).tooltip('hide')
        var anchor_id = $(this).parents("tr").find("td:eq(0)").text()
        var data = { 'anchor_id': anchor_id, 'cooperator': $(this).val() };
        console.log(data)
        $.ajax({
            data: data,
            url: '/reviewDiscarded/',
            method: 'POST',
            success: function (data) {
                // location.reload(true)

            }
        });
        $(this).parents("tr").remove();
        $(".add-new").attr("disabled", "disabled");
    });
});
