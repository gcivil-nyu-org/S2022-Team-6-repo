(async () => {

    const topology = await fetch(
        'https://code.highcharts.com/mapdata/countries/us/us-ny-all.topo.json'
    ).then(response => response.json());

    const data = Highcharts.geojson(topology);

    const mapView = topology.objects.default['hc-recommended-mapview'];

    data.forEach((d, i) => {
        d.drilldown = d.properties['hc-key'];
        d.value = i; 
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

})();