$(document).ready(function() {
    $(document).on("click", "#anchor_redo", function() {
        console.log($(this))
        var anchor_id = $(this).siblings(".anchor-id").text()
        var data = { 'anchor_id': anchor_id };
        console.log(data)
        $.ajax({
            data: data,
            url: '/updateReviewDiscarded/',
            method: 'POST',
            success: function(data) { location.reload(true) }
        });
        // $(this).parents("tr").remove();

    });
});
$(document).ready(function() {
    $(document).on("click", "#anchor_next", function() {
        location.reload(true)
    });
    $(".clickable-row").click(function() {
        var anchor_id = $(this).children(".anchor-id").text()
        console.log(anchor_id)
        var data = { 'anchor_id': anchor_id };
        console.log(data)
        $.ajax({
            data: data,
            url: '/getReviewDiscarded/',
            method: 'POST',
            success: function(data) { location.reload(true) }
        });
    });
});
$(document).ready(function() {
    selected_sample_anchor = $(".selected-sample-anchor").text();
    console.log(selected_sample_anchor)
        // table = $(".table table-striped").find("td").attr("id", selected_sample_anchor);
    table = $(".table").find("td#" + selected_sample_anchor).closest('tr').css({ 'font-weight': 'bold', 'color': '#ff1744' })
    console.log(table)
});