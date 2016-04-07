function craft_series_json(data_arr, view) {
    /*
     data_arr is a 2d array with the following format
     x-axis, y-axis, z-axis, doc_id
     */

    var config = [],        // Highchart series config
        doc_id = -1,        // Initialize doc_id
        dataPoints = [];

    for (var i = 0; i < data_arr.length; i++) {

        if (doc_id != data_arr[i][3] || i == (data_arr.length - 1)) { // craft object if doc_id != previous one or end of loop

            if (doc_id != -1) {
                config[config.length] = {
                    name: doc_id,
                    data: change_direction(dataPoints, view)
                }
            }

            doc_id = data_arr[i][3];
            dataPoints = [];
        }

        dataPoints.push(new Array(data_arr[i][0], data_arr[i][1], data_arr[i][2]));
    }

    return config;
}

function change_direction(dataPoints, view) {
    var dPoint = [];

    for (var i = 0; i < dataPoints.length; i++) {
        if (view == "s1")

            dPoint[dPoint.length] = {
                x: dataPoints[i][0],
                y: Number(dataPoints[i][1]),
                z: dataPoints[i][2],
            };

        else if (view == "s2")

            dPoint[dPoint.length] = {
                x: dataPoints[i][1],
                y: Number(dataPoints[i][2]),
                z: dataPoints[i][0],
            };

        else if (view == "s3")

            dPoint[dPoint.length] = {
                x: dataPoints[i][2],
                y: Number(dataPoints[i][0]),
                z: dataPoints[i][1],
            };

        else

            dPoint[dPoint.length] = {
                x: dataPoints[i][0],
                y: Number(dataPoints[i][1]),
                z: dataPoints[i][2],
            };

    }

    return dPoint;
}

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

function draw3dGraph(series_config, is3D) {

    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            margin: 100,
            type: 'scatter',
            options3d: {
                enabled: is3D,
                alpha: 10,
                beta: 30,
                depth: 500,
                viewDistance: 5,

                frame: {
                    bottom: {size: 1, color: 'rgba(0,0,0,0.02)'},
                    back: {size: 1, color: 'rgba(0,0,0,0.04)'},
                    side: {size: 1, color: 'rgba(0,0,0,0.06)'}
                }
            }
        },
        title: {
            text: 'Stylometric Value Visualization'
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
        series: series_config
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

