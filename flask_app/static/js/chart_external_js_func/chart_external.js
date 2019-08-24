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
    if ("content" in document.createElement("template")) {
        var t = document.querySelector("#author_docs").content;
        t.querySelector('tr').id = doc.val(); //This is not doc_id 

        td = t.querySelectorAll("td");
        td[0].textContent = author.html();
        td[1].textContent = doc.html();

        td[2].innerHTML = '<button type="button" class="btn btn-success" data-toggle="modal" data-target="#doc_modal" ' +
            'onclick="get_content_by_id(' + doc.val() + ')"><span class="glyphicon glyphicon-folder-open"></span></button>';

        td[3].innerHTML = '<input checked="" type="checkbox" class="doc_list" name="doc_list" value="' + doc.val() + '" style="display: none;">' +
            '<button type="button" class="btn btn-warning" onclick="remove_row_from_table(' + doc.val() + ')">' +
            '<span class="glyphicon glyphicon-trash"></span></button>';

        var tb = document.getElementsByTagName("tbody");
        var clone = document.importNode(t, true);
        tb[0].appendChild(clone);
    }
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
            .val(val[0]) //Change key to val[0]
            .html(val[1]));
}


$("#author_select").on("change", function () {

    if (!this.value) {
        alert("Please select a valid author, dude!");
        return false;
    }

    hide_author_doc_elements();

    $.ajax({
        type: "POST",
        url: "/stylometry/getdoclist",
        data: "author_id=" + this.value,
        dataType: "json",
        success: function (result) {
            add_options("doc_select", "", ["", "-- Choose a document written by this author --"]);

            $.each(result, function (key, value) {
                add_options("doc_select", key, value);
            });

            show_author_doc_elements();
        }
    });
});