$(document).ready(function() {
    $(document).on("click", "#anchor_redo", function() {
        console.log($(this))
        var anchor_id = $(this).siblings(".anchor-id").text()
        var data = { 'anchor_id': anchor_id };
        console.log(data)
        $.ajax({
            data: data,
            url: '/reviewDiscarded/',
            method: 'POST',
            success: function(data) { location.reload(true) }
        });
        $(this).parents("tr").remove();
        $(".add-new").attr("disabled", "disabled");
    });
});
$(document).ready(function() {
    $(document).on("click", "#anchor_next", function() {
        location.reload(true)
    });
});