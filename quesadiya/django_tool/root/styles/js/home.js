feather.replace()
var header = document.getElementById("sample_cards");
var btns = header.getElementsByClassName("btn btn-primary");
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
        var current = header.getElementsByClassName("btn-success");
        var current_header = header.getElementsByClassName("card-header");
        if (current[0] != undefined) {
            current[0].className = current[0].className.replace(" btn-success", " btn-primary");
            current_header[0].className = current_header[0].className.replace("card-header positive-anchor-id", "card-header");
        }

        var parent = $(this).parent().parent();

        var current_header = parent.children(".card-header");
        console.log(current_header)
        current_header[0].className = current_header[0].className.replace("card-header", "card-header positive-anchor-id");

        this.className = this.className.replace("btn btn-primary", "btn btn-success");
        var element = document.getElementById("anchor_submit");
        element.classList.remove("disabled");
    });
}
$('#anchor_submit').click(function() {
    var positive_anchor_id = document.getElementsByClassName("card-header positive-anchor-id")[0].innerText;
    var anchor_id = document.getElementsByClassName("card-title anchor-id")[0].innerText;
    var data = { anchor_id: anchor_id, positive_anchor_id: positive_anchor_id };
    $.ajax({
        data: data,
        url: 'updateAnchor/',
        method: 'POST',
        success: function(data) {
            location.reload(true)
        }
    });
});
$('#anchor_next').click(function() {
    var anchor_id = document.getElementsByClassName("card-title anchor-id")[0].innerText;
    var data = { anchor_id: anchor_id };
    var txt;
    var r = confirm("Are you sure to go next anchor and discarded this?");
    if (r == true) {
        $.ajax({
            data: data,
            url: 'nextAnchor/',
            method: 'POST',
            success: function(data) {
                location.reload(true)
            }
        });
    } else {}

});
$(document).ready(function() {

    var showChar = 250;
    var ellipsestext = "...";
    var moretext = "more";
    var lesstext = "less";
    $('.card-text').each(function() {
        var content = $(this).html();
        var child = $(this).children('p')
        var html = '<span class="moreelipses"><a class="morelink less">+&nbsp; more</a></span > ';

        if (child.length > 1) {
            $(this).append(html)
            for (var i = 1; i < child.length; i++) {
                var a = child[i];
                a.style.display = 'none';
            }
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
});