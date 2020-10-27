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
    $(".clickable-row").click(function() {
        var anchor_id = $(this).children(".anchor-id").text()
        console.log(anchor_id)
        var data = { 'anchor_id': anchor_id };
        console.log(data)
        $.ajax({
            data: data,
            url: 'ReviewDiscarded',
            method: 'POST',
            success: function(data) { location.reload(true) }
        });
    });
});
$(document).ready(function() {
    selected_sample_anchor = $(".selected-sample-anchor").text();
    table = $(".table").find("td#" + selected_sample_anchor).closest('tr').css({ 'font-weight': 'bold', 'color': '#ff1744' })
        // $('.card-text').each(function() {
        //     console.log($(this).html())
        // });
        // collpse
    var showChar = 250;
    var ellipsestext = "...";
    var moretext = "more";
    var lesstext = "less";
    $('.card-text').each(function() {
        var content = $(this).html();
        var child = $(this).children('p')
            // var html = '&nbsp;&nbsp;<a href="" class="morelink">See More</a>'
        var html = '<span class="moreelipses"><a class="morelink less">+&nbsp;' + moretext + '</a></span>';
        // console.log(child.length)
        if (child.length > 1) {
            $(this).append(html)
            for (var i = 1; i < child.length; i++) {
                var a = child[i];
                a.style.display = 'none';
            }
            // var c = content.substr(0, showChar);
            // var h = content.substr(showChar - 1, content.length - showChar);

            // var html = c + '<span class="moreelipses">' + ellipsestext + '</span>&nbsp;<span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';
            // console.log(html)
        }

    });
    $(".morelink").click(function() {
        console.log("more click")
        var child = $(this).parent().siblings('p')
        console.log($(this).text())
            // $(this).removeClass("morelink");
        if ($(this).hasClass("less")) {
            $(this).text("- less");
            if (child.length > 1) {
                for (var i = 1; i < child.length; i++) {
                    var a = child[i];
                    a.style.display = 'block';
                }
            }
            $(this).removeClass("less");
        } else {
            $(this).addClass("less");
            $(this).text("+ more");
            if (child.length > 1) {
                for (var i = 1; i < child.length; i++) {
                    var a = child[i];
                    a.style.display = 'none';
                }
            }
        }
    });
    // $(".morelink").click(function() {
    //     if ($(this).hasClass("less")) {
    //         $(this).removeClass("less");
    //         $(this).html(moretext);
    //     } else {
    //         $(this).addClass("less");
    //         $(this).html(lesstext);
    //     }
    //     $(this).parent().prev().toggle();
    //     $(this).prev().toggle();
    //     return false;
    // });
});