function draw3dGraph(dataPoints) {

    var view = $("#viewSelect").val();
    var is3D = true;
    if (view=="ss")
            is3D = true;
    else is3D = false;

    Highcharts.getOptions().colors = $.map(Highcharts.getOptions().colors, function (color) {
        return {
            radialGradient: {
                cx: 0.4,
                cy: 0.3,
                r: 0.5

            },
            stops: [
                [0, color],
                [1, Highcharts.Color(color).brighten(-0.2).get('rgb')]
            ]
        };
    });

  var dPoint = [];


    for (var i=0; i<dataPoints.length; i++) {
        var ncolor = '#000';
        if (dataPoints[i][3] == 1)
            ncolor = '#000';
        else if (dataPoints[i][3] == 2)
            ncolor = '#595';
        else
            ncolor = '#CB3';

         if (view=="s1")
             dPoint[dPoint.length] = {x: dataPoints[i][0], y: Number(dataPoints[i][1]), z: dataPoints[i][2], color: ncolor};
         else if (view=="s2")
             dPoint[dPoint.length] = {x: dataPoints[i][1], y: Number(dataPoints[i][2]), z: dataPoints[i][0], color: ncolor};
         else if (view=="s3")
             dPoint[dPoint.length] = {x: dataPoints[i][2], y: Number(dataPoints[i][0]), z:dataPoints[i][1] , color: ncolor};
         else
            dPoint[dPoint.length] = {x: dataPoints[i][0], y: Number(dataPoints[i][1]), z: dataPoints[i][2], color: ncolor};

    }

    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            margin: 100,
            type: 'scatter',
            options3d: {
                enabled: is3D,
                alpha: 10,
                beta: 30,
                depth: 250,
                viewDistance: 5,

                frame: {
                    bottom: { size: 1, color: 'rgba(0,0,0,0.02)' },
                    back: { size: 1, color: 'rgba(0,0,0,0.04)' },
                    side: { size: 1, color: 'rgba(0,0,0,0.06)' }
                }
            }
        },
        title: {
            text: 'Draggable box'
        },
        subtitle: {
            text: 'Click and drag the plot area to rotate in space'
        },
        plotOptions: {
            scatter: {
                width: 10,
                height: 10,
                depth: 10
            }
        },
        yAxis: {
            min: -10,
            max: 10,
            title: null
        },
        xAxis: {
            min: -10,
            max: 10,
            gridLineWidth: 1
        },
        zAxis: {
            min: -10,
            max: 10,
            showFirstLabel: false
        },
        legend: {
            enabled: false
        },
        series: [{
            name: 'Reading',
            data: dPoint
        }]
    });


    $(chart.container).bind('mousedown.hc touchstart.hc', function (eStart) {
        eStart = chart.pointer.normalize(eStart);

        var posX = eStart.pageX,
            posY = eStart.pageY,
            alpha = chart.options.chart.options3d.alpha,
            beta = chart.options.chart.options3d.beta,
            newAlpha,
            newBeta,
            sensitivity = 5; // lower is more sensitive

        $(document).bind({
            'mousemove.hc touchdrag.hc': function (e) {
                // Run beta
                newBeta = beta + (posX - e.pageX) / sensitivity;
                chart.options.chart.options3d.beta = newBeta;

                // Run alpha
                newAlpha = alpha + (e.pageY - posY) / sensitivity;
                chart.options.chart.options3d.alpha = newAlpha;

                chart.redraw(false);
            },
            'mouseup touchend': function () {
                $(document).unbind('.hc');
            }
        });
    });

}

$("#driver").click(function () {
    $.ajax({
        type: "GET",
        url: "/getcsv",
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
});
