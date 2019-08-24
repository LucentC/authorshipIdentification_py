function get_content_by_id(doc_id) {

    $.ajax({
        type: "POST",
        url: "/sytlometry/doccontent",
        data: "doc_id=" + doc_id,
        success: function (result) {

            $.each(result, function (key, value) {
                if (key == "doc_title")
                    $("#h4_tag").text(value);
                else
                    $("#pre_tag").text(value);
            });

        }
    });
}

function get_stylometric_csv(doc_id) {
    window.location = '/stylometry/getstylocsv?doc_id=' + doc_id
}