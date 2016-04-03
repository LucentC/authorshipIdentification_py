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

            console.log(data_arr)
        }
    });
}

function outf(text) {
    var mypre = document.getElementById("output");
    mypre.innerHTML = mypre.innerHTML + text;
}

function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
        throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
}

function runit() {
    var prog = editor.getValue();
    var mypre = document.getElementById("output");

    mypre.innerHTML = '';
    Sk.pre = "output";

    Sk.configure({output: outf, read: builtinRead});
    (Sk.TurtleGraphics || (Sk.TurtleGraphics = {})).target = 'mycanvas';

    var myPromise = Sk.misceval.asyncToPromise(function () {
        return Sk.importMainWithBody("<stdin>", false, prog, true);
    });

    myPromise.then(
        function (mod) {
            $("#error_message").hide();
        },
        function (err) {
            $("#error_message i").text(err.toString());
            $("#error_message").show();
        });
}
