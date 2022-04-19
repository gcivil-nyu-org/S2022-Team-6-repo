let isNavBarOpen = false;
let mainChartSelector = document.querySelector("#mainchart_1");
let homechartSelector = document.querySelector("#homechart_1");
let workchartSelector = document.querySelector("#workchart_1");
let dropdownMenuLinkSelector = document.querySelector("#dropdownMenuLink");
let countyDropDownMain = document.querySelector("#countyDropDownMain");
let chart, homechart, workchart;
let mainChartConfig = {
    chart: {
        type: 'spline'
    },
    title: {
        text: 'New York City Covid Cases'
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
        text: _locations[0] + ' Covid Cases'
    },
    exporting: { enabled: false },

    credits: {
        enabled: false
    },
    xAxis: [
        {
            'type': "category",
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
        pointFormat: '{point.x}: {point.y}'
    },

    plotOptions: {
        series: {
            marker: {
                enabled: true
            },
            turboThreshold: 50000
        }
    },

    series: [{
        showInLegend: false,
        name: "",
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
        text: _locations[1] + ' Covid Cases'
    },
    exporting: { enabled: false },

    credits: {
        enabled: false
    },
    xAxis: [
        {
            'type': "category",
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
        pointFormat: '{point.x}: {point.y}'
    },

    plotOptions: {
        series: {
            marker: {
                enabled: true
            },
            turboThreshold: 50000
        }
    },

    series: [{
        showInLegend: false,
        name: "",
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
    document.getElementById("main").style.marginLeft = "0";
}

function showMainChart() {
    if (mainChartSelector.classList && mainChartSelector.classList.contains('hideChart')) {
        mainChartSelector.classList.remove('hideChart');
    }
    if (homechartSelector.classList && !homechartSelector.classList.contains('hideChart')) {
        homechartSelector.classList.add('hideChart');
    }
    if (workchartSelector.classList && !workchartSelector.classList.contains('hideChart')) {
        workchartSelector.classList.add('hideChart');
    }
    if (countyDropDownMain.classList && countyDropDownMain.classList.contains('hideChart')) {
        countyDropDownMain.classList.remove('hideChart');
    }
}

function showHomeChart() {
    if (mainChartSelector.classList && !mainChartSelector.classList.contains('hideChart')) {
        mainChartSelector.classList.add('hideChart');
    }
    if (homechartSelector.classList && homechartSelector.classList.contains('hideChart')) {
        homechartSelector.classList.remove('hideChart');
    }
    if (workchartSelector.classList && !workchartSelector.classList.contains('hideChart')) {
        workchartSelector.classList.add('hideChart');
    }
    if (countyDropDownMain.classList && !countyDropDownMain.classList.contains('hideChart')) {
        countyDropDownMain.classList.add('hideChart');
    }
}

function showWorkChart() {
    if (mainChartSelector.classList && !mainChartSelector.classList.contains('hideChart')) {
        mainChartSelector.classList.add('hideChart');
    }
    if (homechartSelector.classList && !homechartSelector.classList.contains('hideChart')) {
        homechartSelector.classList.add('hideChart');
    }
    if (workchartSelector.classList && workchartSelector.classList.contains('hideChart')) {
        workchartSelector.classList.remove('hideChart');
    }
    if (countyDropDownMain.classList && !countyDropDownMain.classList.contains('hideChart')) {
        countyDropDownMain.classList.add('hideChart');
    }
}

function generateLineGraph() {
    dropdownMenuLinkSelector.innerText = 'Line Graph';
    mainChartConfig.chart.type = 'spline';
    if (mainChartConfig.chart.options3d)
        delete mainChartConfig.chart.options3d;
    if (homeChartConfig.chart.options3d)
        delete homeChartConfig.chart.options3d;
    if (workChartConfig.chart.options3d)
        delete workChartConfig.chart.options3d;
    chart = Highcharts.chart('mainchart', mainChartConfig);
    homeChartConfig.chart.type = 'spline';
    homechart = Highcharts.chart('homechart', homeChartConfig);
    workChartConfig.chart.type = 'spline';
    workchart = Highcharts.chart('workchart', workChartConfig);
}
function generateBarGraph() {
    dropdownMenuLinkSelector.innerText = 'Bar Graph';
    mainChartConfig.chart.type = 'bar';
    if (mainChartConfig.chart.options3d)
        delete mainChartConfig.chart.options3d;
    if (homeChartConfig.chart.options3d)
        delete homeChartConfig.chart.options3d;
    if (workChartConfig.chart.options3d)
        delete workChartConfig.chart.options3d;
    chart = Highcharts.chart('mainchart', mainChartConfig);
    homeChartConfig.chart.type = 'bar';
    homechart = Highcharts.chart('homechart', homeChartConfig);
    workChartConfig.chart.type = 'bar';
    workchart = Highcharts.chart('workchart', workChartConfig);
}

function generateScatter() {
    dropdownMenuLinkSelector.innerText = 'Scatter Plot';
    mainChartConfig.chart.type = 'scatter';
    if (mainChartConfig.chart.options3d)
        delete mainChartConfig.chart.options3d;
    if (homeChartConfig.chart.options3d)
        delete homeChartConfig.chart.options3d;
    if (workChartConfig.chart.options3d)
        delete workChartConfig.chart.options3d;
    chart = Highcharts.chart('mainchart', mainChartConfig);
    homeChartConfig.chart.type = 'scatter';
    homechart = Highcharts.chart('homechart', homeChartConfig);
    workChartConfig.chart.type = 'scatter';
    workchart = Highcharts.chart('workchart', workChartConfig);
}

function generateColumn() {

    dropdownMenuLinkSelector.innerText = 'Column Graph';
    mainChartConfig.chart.type = 'column';
    if (mainChartConfig.chart.options3d)
        delete mainChartConfig.chart.options3d;
    if (homeChartConfig.chart.options3d)
        delete homeChartConfig.chart.options3d;
    if (workChartConfig.chart.options3d)
        delete workChartConfig.chart.options3d;

    chart = Highcharts.chart('mainchart', mainChartConfig);
    homeChartConfig.chart.type = 'column';
    homechart = Highcharts.chart('homechart', homeChartConfig);
    workChartConfig.chart.type = 'column';
    workchart = Highcharts.chart('workchart', workChartConfig);
}

function generatePie() {
    let pieGraph3d = {
        enabled: true,
        alpha: 45,
        beta: 0,
        depth: 50,
    };
    dropdownMenuLinkSelector.innerText = 'Pie Chart';
    mainChartConfig.chart.type = 'pie';
    if (mainChartConfig.plotOptions.pie)
        delete mainChartConfig.plotOptions.pie;
    if (homeChartConfig.plotOptions.pie)
        delete homeChartConfig.plotOptions.pie;
    if (workChartConfig.plotOptions.pie)
        delete workChartConfig.plotOptions.pie;
    mainChartConfig.plotOptions.pie = { allowPointSelect: true };
    mainChartConfig.plotOptions.pie.depth = 35;
    homeChartConfig.plotOptions.pie = { allowPointSelect: true };
    homeChartConfig.plotOptions.pie.depth = 35;
    workChartConfig.plotOptions.pie = { allowPointSelect: true };
    workChartConfig.plotOptions.pie.depth = 35;
    if (mainChartConfig.chart.options3d)
        delete mainChartConfig.chart.options3d;
    if (homeChartConfig.chart.options3d)
        delete homeChartConfig.chart.options3d;
    if (workChartConfig.chart.options3d)
        delete workChartConfig.chart.options3d;
    if (!mainChartConfig.chart.options3d)
        mainChartConfig.chart.options3d = pieGraph3d;
    if (!homeChartConfig.chart.options3d)
        homeChartConfig.chart.options3d = pieGraph3d;
    if (!workChartConfig.chart.options3d)
        workChartConfig.chart.options3d = pieGraph3d;
    chart = Highcharts.chart('mainchart', mainChartConfig);
    homeChartConfig.chart.type = 'pie';
    homechart = Highcharts.chart('homechart', homeChartConfig);
    workChartConfig.chart.type = 'pie';
    workchart = Highcharts.chart('workchart', workChartConfig);
}

function generateseriesData(data) {
    monthToCasesMap = {
        "January": 0, "February": 0, "March": 0, "April": 0, "May": 0, "June": 0, "July": 0, "August": 0, "September": 0,
        "October": 0, "November": 0, "December": 0
    };
    monthNumberToNameMap = {
        "01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June",
        "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"
    };
    seriesDataMap = [];
    for (temp in data) {
        monthToCasesMap[monthNumberToNameMap[data[temp][0].split("-")[1]]] += data[temp][1];
    }
    for (temp in monthToCasesMap) {
        let temp1 = { "name": temp, "y": monthToCasesMap[temp], "drilldown": temp };
        seriesDataMap.push(temp1);
    }
    return seriesDataMap;
}

function generateDrillDownData(data) {
    drilldownData = [{ "id": "January", "data": [] }, { "id": "February", "data": [] }, { "id": "March", "data": [] }, { "id": "April", "data": [] },
    { "id": "May", "data": [] }, { "id": "June", "data": [] }, { "id": "July", "data": [] }, { "id": "August", "data": [] }, { "id": "September", "data": [] },
    { "id": "October", "data": [] }, { "id": "November", "data": [] }, { "id": "December", "data": [] }];
    monthNumberToNameMap = {
        "01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June",
        "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"
    };
    for (temp in data) {
        for (temp2 in drilldownData) {
            if (drilldownData[temp2]["id"] == monthNumberToNameMap[data[temp][0].split("-")[1]]) {
                drilldownData[temp2]["data"].push([data[temp][0], data[temp][1]]);
            }
        }
    }
    finalData = { "series": drilldownData };
    return finalData;
}

function generateCountySpecificGraph(value) {
    document.querySelector('#dropdownCountyLink').innerText = value;
    let countyData = [];
    for (i in _df_2021_all) {
        if (_df_2021_all[i][2] == value) {
            dateToCasesArray = [];
            dateToCasesArray.push(_df_2021_all[i][0]);
            dateToCasesArray.push(_df_2021_all[i][1]);
            countyData.push(dateToCasesArray);
        }
    }
    mainChartConfig.series[0]['data'] = generateseriesData(countyData);
    mainChartConfig.drilldown = generateDrillDownData(countyData);
    mainChartConfig.title.text = value + ' Covid Cases';
    chart = Highcharts.chart('mainchart', mainChartConfig);
}

document.addEventListener('DOMContentLoaded', function () {
    chart = Highcharts.chart('mainchart', mainChartConfig);
});

homechart = Highcharts.chart('homechart', homeChartConfig);

workchart = Highcharts.chart('workchart', workChartConfig);