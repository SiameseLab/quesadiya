
$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
    var actions = $("table td:last-child").html();
    // Append table with add row form on add new button click
    // $(".add-new").click(function () {
    //     $(this).attr("disabled", "disabled");
    //     var index = $("table tbody tr:last-child").index();
    //     var row = '<tr>' +
    //         '<td><input type="text" class="form-control" name="name" id="name"></td>' +
    //         '<td><input type="text" class="form-control" name="department" id="department"></td>' +
    //         '<td><input type="text" class="form-control" name="phone" id="phone"></td>' +
    //         '<td>' + actions + '</td>' +
    //         '</tr>';
    //     $("table").append(row);
    //     $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
    //     $('[data-toggle="tooltip"]').tooltip();
    // });
    // Add row on add button click
    // $(document).on("click", ".add", function () {
    //     var empty = false;
    //     var input = $(this).parents("tr").find('input[type="text"]');
    //     var anchor_id = $(this).parents("tr").find("td:eq(0)").text()
    //     input.each(function () {
    //         if (!$(this).val()) {
    //             $(this).addClass("error");
    //             empty = true;
    //         } else {
    //             $(this).removeClass("error");
    //         }
    //     });
    //     $(this).parents("tr").find(".error").first().focus();
    //     if (!empty) {
    //         input.each(function () {
    //             // var anchor_id = document.getElementsByClassName("card-title anchor-id")[0].innerText;
    //             var data = { 'anchor_id': anchor_id, 'cooperator': $(this).val() };
    //             console.log(data)
    //             $.ajax({
    //                 data: data,
    //                 url: '/updateCooperator/',
    //                 method: 'POST',
    //                 success: function (data) {
    //                     // location.reload(true)

    //                 }
    //             });
    //             $(this).parent("td").html($(this).val());
    //             // $(this).parent("td").html($(this).val());
    //         });
    //         $(this).parents("tr").find(".add, .edit").toggle();
    //         $(".add-new").removeAttr("disabled");
    //     }
    // });
    // Edit row on edit button click
    $(document).on("click", ".edit", function () {
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
    // Delete row on delete button click
    // $(document).on("click", ".delete", function () {
    //     $(this).parents("tr").remove();
    //     $(".add-new").removeAttr("disabled");
    // });
});
