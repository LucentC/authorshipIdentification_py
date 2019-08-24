var data_arr = [];

function get_csv_by_doc_list() {

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
                data_arr.push(new Array(parseFloat(line[0]), parseFloat(line[1]), parseFloat(line[2]), parseFloat(line[3])));
            }

            draw3dGraph(craft_series_json(data_arr, "ss"), true);
            draw3dGraph(craft_series_json(data_arr, "ss"), true);

            $("#dimenison_select").show();
        }
    });
}

function get_distance() {
    $.ajax({
        type: "POST",
        url: "/stylometry/gethausdis",
        data: $(".doc_list:checked").serialize(),
        cache: false,
        dataType: "json",
        success: function (result) {
            $("#distance_table").show();
            $.each(result, function (key, value) {
                $("#distance_table > tbody:last").append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");
            })
        }
    });
}

$("#select_dimensions").on('change', function () {

    if (!this.value) {
        alert("Honestly, I have no idea how you did that.");
        return false;
    }

    if (!data_arr) {
        alert("Again, I have no idea how you did that.");
        return false;
    }

    if (this.value == "ss")
        draw3dGraph(craft_series_json(data_arr, "ss"), true);
    else
        draw3dGraph(craft_series_json(data_arr, this.value), false);
});