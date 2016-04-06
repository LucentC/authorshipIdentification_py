function get_content_by_id(e) {

    $.ajax({
        type: "POST",
        url: "/doccontent",
        data: "doc_id=" + $(e.target).data("id"),
        success: function (result) {

            $.each(result, function(key, value){
                if (key == "doc_title")
                    $("#h4_tag").text(value);
                else
                    $("#pre_tag").text(value);
            });

        }
    });
}
