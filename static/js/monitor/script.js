let isNavBarOpen = false;
let mainChartSelector = document.querySelector("#mainchart_1");
let homechartSelector = document.querySelector("#homechart_1");
let workchartSelector = document.querySelector("#workchart_1");
let chart,homechart,workchart;
let mainChartConfig = {
    chart: {
        type: 'spline'
    },
    title: {
        text: 'NYC Covid Cases'
    },
    xAxis: [
        {
            'categories': _categories_2021,
        title: {
            text: 'Date'
        },
        }
    ],

    exporting: { enabled: false },

    credits: {
        enabled: false
      },

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
        showInLegend: false,
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
}

function toggleNav() {
    if (!isNavBarOpen) {
        openNav();
        isNavBarOpen = true;
    }
    else {
        closeNav();
        isNavBarOpen = false;
    }
    chart.reflow();
    homechart.reflow();
    workchart.reflow();
}


function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}
  
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
}

function changeCss () {
    //var side_bar = document.querySelector(".sidebar");
    let side_bar = document.querySelector("#mySidebar");
    let toggle_bar = document.querySelector("#toggleBtn")
    this.scrollY > 30 ? side_bar.style.top = "0px" : side_bar.style.top = "92px";
    this.scrollY > 30 ? toggle_bar.style.top = "0px" : toggle_bar.style.top = "132px";
}

function showMainChart() {
    //let mainChart = document.querySelector("#mainchart");
    //let homechart = document.querySelector("#homechart");
    //let workchart = document.querySelector("#workchart");
    if (mainChartSelector.classList && mainChartSelector.classList.contains('hideChart')) {
        mainChartSelector.classList.remove('hideChart');
    }
    if (homechartSelector.classList && !homechartSelector.classList.contains('hideChart')) {
        homechartSelector.classList.add('hideChart');
    }
    if (workchartSelector.classList && !workchartSelector.classList.contains('hideChart')) {
        workchartSelector.classList.add('hideChart');
    }
}

function showHomeChart() {
    //let mainChart = document.querySelector("#mainchart");
    //let homechart = document.querySelector("#homechart");
    //let workchart = document.querySelector("#workchart");
    if (mainChartSelector.classList && !mainChartSelector.classList.contains('hideChart')) {
        mainChartSelector.classList.add('hideChart');
    }
    if (homechartSelector.classList && homechartSelector.classList.contains('hideChart')) {
        homechartSelector.classList.remove('hideChart');
    }
    if (workchartSelector.classList && !workchartSelector.classList.contains('hideChart')) {
        workchartSelector.classList.add('hideChart');
    }
}

function showWorkChart() {
    //let mainChart = document.querySelector("#mainchart");
    //let homechart = document.querySelector("#homechart");
    //let workchart = document.querySelector("#workchart");
    if (mainChartSelector.classList && !mainChartSelector.classList.contains('hideChart')) {
        mainChartSelector.classList.add('hideChart');
    }
    if (homechartSelector.classList && !homechartSelector.classList.contains('hideChart')) {
        homechartSelector.classList.add('hideChart');
    }
    if (workchartSelector.classList && workchartSelector.classList.contains('hideChart')) {
        workchartSelector.classList.remove('hideChart');
    }
}

function generateBarGraph() {
    mainChartConfig.chart.type = 'bar';
    chart = Highcharts.chart('mainchart', mainChartConfig);
}

function generateScatter() {
    mainChartConfig.chart.type = 'scatter';
    chart = Highcharts.chart('mainchart', mainChartConfig);
}

function generateColumn() {
    mainChartConfig.chart.type = 'column';
    chart = Highcharts.chart('mainchart', mainChartConfig);
}

window.addEventListener("scroll", changeCss , false);

document.addEventListener('DOMContentLoaded', function () {
    chart = Highcharts.chart('mainchart', mainChartConfig);
});
    
    homechart = Highcharts.chart('homechart', {
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
    
    workchart = Highcharts.chart('workchart', {
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