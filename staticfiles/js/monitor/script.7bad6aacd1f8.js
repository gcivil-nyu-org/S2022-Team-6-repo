let isNavBarOpen = false;
let mainChartSelector = document.querySelector("#mainchart_1");
let homechartSelector = document.querySelector("#homechart_1");
let workchartSelector = document.querySelector("#workchart_1");
let dropdownMenuLinkSelector = document.querySelector("#dropdownMenuLink");
let chart,homechart,workchart;
let mainChartConfig = {
    chart: {
        type: 'spline',
        options3d: {
            enabled: true,
            alpha: 15,
            beta: 15,
            depth: 50,
            viewDistance: 25
        }
    },
    title: {
        text: 'NYC Covid Cases'
    },
    xAxis: [
        {
            'type': "category",
        title: {
            text: 'Month'
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
    tooltip: {
        pointFormat: '{point.x}: {point.y}'
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
        name: "",
        data: generateseriesData(_df_2021)
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
    },
    drilldown: generateDrillDownData(_df_2021)
}

let homeChartConfig = {
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Home Covid Cases'
    },
    xAxis: [
        {
            'categories': ["January", "February", "March", "April", "May", "June", "July", "August", "September", 
            "October", "November", "December"],
        title: {
            text: 'Month'
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
        data: generateseriesData(_df_2021_home)
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
    },
    drilldown: generateDrillDownData(_df_2021_home)
}


let workChartConfig = {
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Work Covid Cases'
    },
    xAxis: [
        {
            'categories': ["January", "February", "March", "April", "May", "June", "July", "August", "September", 
            "October", "November", "December"],
        title: {
            text: 'Month'
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
        data: generateseriesData(_df_2021_work)
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
    },
    drilldown: generateDrillDownData(_df_2021_work)
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

function generateLineGraph() {
    dropdownMenuLinkSelector.innerText = 'Line Graph';
    mainChartConfig.chart.type = 'spline';
    chart = Highcharts.chart('mainchart', mainChartConfig);
    homeChartConfig.chart.type = 'spline';
    chart = Highcharts.chart('homechart', homeChartConfig);
    workChartConfig.chart.type = 'spline';
    chart = Highcharts.chart('workchart', workChartConfig);
}
function generateBarGraph() {
    dropdownMenuLinkSelector.innerText = 'Bar Graph';
    mainChartConfig.chart.type = 'bar';
    chart = Highcharts.chart('mainchart', mainChartConfig);
    homeChartConfig.chart.type = 'bar';
    chart = Highcharts.chart('homechart', homeChartConfig);
    workChartConfig.chart.type = 'bar';
    chart = Highcharts.chart('workchart', workChartConfig);
}

function generateScatter() {
    dropdownMenuLinkSelector.innerText = 'Scatter Plot';
    mainChartConfig.chart.type = 'scatter';
    chart = Highcharts.chart('mainchart', mainChartConfig);
    homeChartConfig.chart.type = 'scatter';
    chart = Highcharts.chart('homechart', homeChartConfig);
    workChartConfig.chart.type = 'scatter';
    chart = Highcharts.chart('workchart', workChartConfig);
}

function generateColumn() {
    dropdownMenuLinkSelector.innerText = 'Column Graph';
    mainChartConfig.chart.type = 'column';
    chart = Highcharts.chart('mainchart', mainChartConfig);
    homeChartConfig.chart.type = 'column';
    chart = Highcharts.chart('homechart', homeChartConfig);
    workChartConfig.chart.type = 'column';
    chart = Highcharts.chart('workchart', workChartConfig);
}

function generatePie() {
    dropdownMenuLinkSelector.innerText = 'Pie Chart';
    mainChartConfig.chart.type = 'pie';
    chart = Highcharts.chart('mainchart', mainChartConfig);
    homeChartConfig.chart.type = 'pie';
    chart = Highcharts.chart('homechart', homeChartConfig);
    workChartConfig.chart.type = 'pie';
    chart = Highcharts.chart('workchart', workChartConfig);
}

function generateseriesData(data) {
    monthToCasesMap = {"January": 0, "February": 0, "March": 0, "April": 0, "May": 0, "June": 0, "July": 0, "August": 0, "September": 0, 
    "October": 0, "November": 0, "December": 0};
    monthNumberToNameMap = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", 
    "07": "July","08": "August", "09": "September", "10": "October", "11": "November", "12": "December"};
    seriesDataMap = [];
    for (temp in data) {
        monthToCasesMap[monthNumberToNameMap[data[temp][0].split("-")[1]]] += data[temp][1];
    }
    for (temp in monthToCasesMap) {
        let temp1 = {"name": temp, "y": monthToCasesMap[temp], "drilldown": temp};
        seriesDataMap.push(temp1);
    }
    return seriesDataMap;
}

function generateDrillDownData(data) {
    drilldownData = [{"id": "January", "data": []}, {"id": "February", "data": []}, {"id": "March", "data": []}, {"id": "April", "data": []},
    {"id": "May", "data": []}, {"id": "June", "data": []}, {"id": "July", "data": []}, {"id": "August", "data": []}, {"id": "September", "data": []},
    {"id": "October", "data": []}, {"id": "November", "data": []}, {"id": "December", "data": []}];
    monthNumberToNameMap = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", 
    "07": "July","08": "August", "09": "September", "10": "October", "11": "November", "12": "December"};
    for (temp in data) {
        for (temp2 in drilldownData) {
            if (drilldownData[temp2]["id"] == monthNumberToNameMap[data[temp][0].split("-")[1]]) {
                drilldownData[temp2]["data"].push([data[temp][0], data[temp][1]]);
            }
        }
    }
    finalData = {"series": drilldownData};
    return finalData;
}

window.addEventListener("scroll", changeCss , false);

document.addEventListener('DOMContentLoaded', function () {
    chart = Highcharts.chart('mainchart', mainChartConfig);
});
    
    homechart = Highcharts.chart('homechart', homeChartConfig);
    
    workchart = Highcharts.chart('workchart', workChartConfig);