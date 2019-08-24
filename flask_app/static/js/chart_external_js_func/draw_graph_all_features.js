var data_arr = [];

function get_csv_of_all_features_by_doc_list() {

    $("#author_doc_form").hide();

    $.ajax({
        type: "POST",
        url: "/stylometry/getcsv",
        data: $(".doc_list:checked").serialize(),
        cache: false,
        dataType: "text",
        success: function (result) {
            var val = result.split("\n");
            var line = "";

            for (var i = 0; i < val.length - 1; i++) {
                line = val[i].split(",");
                data_arr.push(new Array(Number(line[0]), Number(line[1]), Number(line[2]), Number(line[3])));
            }

            draw3dGraph(data_arr, true, "ss");

            $("#dimenison_select").show();
        }
    });
}
