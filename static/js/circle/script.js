heatmapFunction = (async () => {

    const topology = await fetch(
        'https://code.highcharts.com/mapdata/countries/us/us-ny-all.topo.json'
    ).then(response => response.json());

    const data = Highcharts.geojson(topology);

    const mapView = topology.objects.default['hc-recommended-mapview'];

    let newyorkCases = 0;
    liveData.forEach((a) => {
        if (a[0] == 'New York City') {
            newyorkCases = a[1];
        }
    }); 
    data.forEach((d) => {
        for (i in liveData) {
            if (liveData[i][0] == d.name) {
                d.value = liveData[i][1];
            }
            else if (d.name == 'Queens' || d.name == 'Kings' || d.name == 'Bronx' || d.name == 'New York' || d.name == 'Richmond') {
                d.value = newyorkCases;
            }
        }
    });

    Highcharts.mapChart('heatMap', {
        chart: {
        },

        title: {
            text: 'New York State HeatMap for Today'
        },

        exporting: { enabled: false },

        credits: {
            enabled: false
        },

        colorAxis: {
            min: 0,
            minColor: '#FFCCCB',
            maxColor: '#FF0000'
        },

        mapView,

       

        plotOptions: {
            map: {
                states: {
                    hover: {
                        color: '#EEDD66'
                    }
                }
            }
        },

        series: [{
            data,
            name: 'USA',
            dataLabels: {
                enabled: true,
                format: '{point.properties.postal-code}'
            },
            custom: {
                mapView
            }
        }]
    });

});

document.addEventListener('DOMContentLoaded', function () {
    heatmapFunction();
});