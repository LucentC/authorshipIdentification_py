var data_arr = [];

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
            var line = "";

            for (var i = 0; i < val.length - 1; i++) {
                line = val[i].split(",");
                data_arr.push(new Array(parseFloat(line[0]), parseFloat(line[1]), parseFloat(line[2]), parseFloat(line[3])));
            }

            draw3dGraph(data_arr, true, "ss");

            $("#dimenison_select").show();
        }
    });
}

$("#select_dimensions").on('change', function(){

    if (!this.value) {
        alert("Honestly, I have no idea how you did that.");
        return false;
    }

    if (!data_arr) {
        alert("Again, I have no idea how you did that.");
        return false;
    }

    if (this.value == "ss")
        draw3dGraph(data_arr, true, "ss");
    else
        draw3dGraph(data_arr, false, this.value);
});