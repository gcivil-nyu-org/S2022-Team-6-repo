


document.addEventListener('DOMContentLoaded', function () {
    
    const chart = Highcharts.chart('mainchart', {
        chart: {
            type: 'spline'
        },
        title: {
            text: 'NYC Covid Cases'
        },
        subtitle: {
            text: 'Winter of 2021'
        },
        xAxis: [
            {
                'categories': _categories_2021,
            title: {
                text: 'Date'
            },
            }
        ],

        yAxis: {
            title: {
                text: 'Covid Cases'
            }
        },

        plotOptions: {
            series: {
                marker: {
                    enabled: true
                }
            }
        },

        colors: ['#6CF'],

        series: [
        {
            name: "Winter 2021",
            data: _df_2021
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 100
                },
                chartOptions: {
                    plotOptions: {
                        series: {
                            marker: {
                                radius: 2.5
                            }
                        }
                    }
                }
            }]
        }
    });
});
    
    const homechart = Highcharts.chart('homechart', {
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Home Location Covid Cases'
        },
        subtitle: {
            text: 'Winter 2021'
        },
        xAxis: [
            {
                'categories': _categories_2021,
            title: {
                text: 'Date'
            },
            }
        ],
        yAxis: {
            title: {
                text: 'Covid Cases'
            }
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
        },

        plotOptions: {
            series: {
                marker: {
                    enabled: true
                },
                turboThreshold: 50000
            }
        },

        colors: ['#39F'],

        series: [{
            name: "Winter 2021",
            data: _df_2021_home
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 100
                },
                chartOptions: {
                    plotOptions: {
                        series: {
                            marker: {
                                radius: 2.5
                            }
                        }
                    }
                }
            }]
        }
    });
    
    const workchart = Highcharts.chart('workchart', {
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Workspace Covid Cases'
        },
        subtitle: {
            text: 'Winter 2021'
        },
        xAxis: [
            {
                'categories': _categories_2021,
            title: {
                text: 'Date'
            },
            }
        ],
        yAxis: {
            title: {
                text: 'Covid Cases'
            }
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
        },

        plotOptions: {
            series: {
                marker: {
                    enabled: true
                },
                turboThreshold: 50000
            }
        },

        colors: ['#036'],

        series: [{
            name: "Winter 2021",
            data: _df_2021_work
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 100
                },
                chartOptions: {
                    plotOptions: {
                        series: {
                            marker: {
                                radius: 2.5
                            }
                        }
                    }
                }
            }]
        }
    });