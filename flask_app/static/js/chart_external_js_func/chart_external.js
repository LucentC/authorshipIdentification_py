function add_rows_to_table() {
    var author = $("#author_select option:selected");
    var doc = $("#doc_select option:selected");

    if (!author.val() || !doc.val()) {
        alert("Please select a valid document, dude!");
        return false;
    }

    $("#display_doc_form").show();

    add_a_row(author, doc);
    check_confirm_table()

    $("#author_select").prop('selectedIndex', 0);
    $("#doc_select option").remove();
    hide_author_doc_elements();
}

function add_a_row(author, doc) {
    $("#confirm_table > tbody")
        .append($("<tr></tr>")
            .attr("id", "doc_" + doc.val())
            .append($("<td></td>")
                .html(author.html()))
            .append($("<td></td>")
                .html(doc.html()))
            .append($("<td></td>")
                .append($("<button></button>")
                    .attr("type", "button")
                    .attr("class", "btn btn-success")
                    .attr("data-toggle", "modal")
                    .attr("data-target", "#doc_modal")
                    .attr("onclick", "get_content_by_id(" + doc.val() + ")")
                    .append($("<span></span>")
                        .attr("class", "glyphicon glyphicon-folder-open"))))
            .append($("<td></td>")
                .append($("<input checked/>")
                    .attr("type", "checkbox")
                    .attr("class", "doc_list")
                    .attr("name", "doc_list")
                    .attr("value", doc.val())
                    .attr("style", "display: none;"))
                .append($("<button></button>")
                    .attr("type", "button")
                    .attr("class", "btn btn-warning")
                    .attr("onclick", "remove_row_from_table(\"doc_" + doc.val() + "\")")
                    .append($("<span></span>")
                        .attr("class", "glyphicon glyphicon-trash"))
                )));
}

function remove_row_from_table(doc_id) {
    $("#" + doc_id).remove();
    check_confirm_table()
}

function check_confirm_table() {
    var tds = $("#confirm_table").children("tbody").children("tr").length;

    if (tds == 0) {
        $("#warning_banner").hide();
        $("#display_doc_form").hide();
        $("#author_doc_form").show();
        return true;
    }

    if (tds == 1) {
        $("#warning_banner").show();
        $("#author_doc_form").show();
        $("#display_form_confirm").hide();
        return true;
    }

    if (tds == 3) {
        $("#warning_banner i").text("The system at most supports the comparison of 3 documents");
        $("#warning_banner").show();
        $("#author_doc_form").hide();
    }
    else {
        $("#warning_banner").hide();
        $("#author_doc_form").show();
    }

    $("#display_form_confirm").show();
    return true;
}

function hide_author_doc_elements() {
    $("#document_form").hide();
    $("#submit").hide();
}

function show_author_doc_elements() {
    $("#document_form").show();
    $("#submit").show();
}

function add_options(id, key, val) {
    $("#" + id)
        .append($("<option></option>")
            .val(key)
            .html(val));
}

function get_csv_by_doc_list() {

    $("#author_doc_form").hide();

    $.ajax({
        type: "POST",
        url: "/getcsv",
        data: $(".doc_list:checked").serialize(),
        cache: false,
        dataType: "text",
        success: function (result) {
            var val = result.split("\n");
            var line = ""
            var data_arr = []
            for (var i = 0; i < val.length - 1; i++) {
                line = val[i].split(",");
                data_arr.push(new Array(parseFloat(line[0]), parseFloat(line[1]), parseFloat(line[2]), parseFloat(line[3])));
            }
            draw3dGraph(data_arr)
        }
    });
}


$("#author_select").on("change", function () {

    if (!this.value) {
        alert("Please select a valid author, dude!");
        return false;
    }

    hide_author_doc_elements();

    $.ajax({
        type: "POST",
        url: "/getdoclist",
        data: "author_id=" + this.value,
        dataType: "json",
        success: function (result) {
            add_options("doc_select", "", "-- Choose a document written by this author --");

            $.each(result, function (key, value) {
                add_options("doc_select", key, value);
            });

            show_author_doc_elements();
        }
    });
});