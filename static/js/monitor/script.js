let isNavBarOpen = false;
let mainChartSelector = document.querySelector("#mainchart_1");
let homechartSelector = document.querySelector("#homechart_1");
let workchartSelector = document.querySelector("#workchart_1");
let dropdownMenuLinkSelector = document.querySelector("#dropdownMenuLink");
let countyDropDownMain = document.querySelector("#countyDropDownMain");
let datepickerSelector = document.querySelector("#datePicker");
let searchButtonSelector = document.querySelector("#searchButton");
let chart, homechart, workchart;
const months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
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
    $('#mainchart').css("width","940px");
    $('#homechart').css("width","940px");
    $('#workchart').css("width","940px");
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    $('#mainchart').css("width","1210px");
    $('#homechart').css("width","1210px");
    $('#workchart').css("width","1210px");
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
    if (datepickerSelector.classList && datepickerSelector.classList.contains('hideChart')) {
        datepickerSelector.classList.remove('hideChart');
    }
    if (searchButtonSelector.classList && searchButtonSelector.classList.contains('hideChart')) {
        searchButtonSelector.classList.remove('hideChart');
    }
    chart.reflow();
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
    if (datepickerSelector.classList && !datepickerSelector.classList.contains('hideChart')) {
        datepickerSelector.classList.add('hideChart');
    }
    if (searchButtonSelector.classList && !searchButtonSelector.classList.contains('hideChart')) {
        searchButtonSelector.classList.add('hideChart');
    }
    homechart.reflow();
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
    if (datepickerSelector.classList && !datepickerSelector.classList.contains('hideChart')) {
        datepickerSelector.classList.add('hideChart');
    }
    if (searchButtonSelector.classList && !searchButtonSelector.classList.contains('hideChart')) {
        searchButtonSelector.classList.add('hideChart');
    }
    searchButtonSelector
    workchart.reflow();
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
    //monthToCasesMap = {
    //    "December": 0, "January": 0, "February": 0, "March": 0, "April": 0, "May": 0, "June": 0, "July": 0, "August": 0, "September": 0,
    //    "October": 0, "November": 0
    //};
    monthToCasesMap = {};
    currentMonthName = new Date().getMonth();
    if ($('#dateFrom').val() != "" && $('#dateTo').val() != "") {
        currentMonthName = (new Date($('#dateFrom').val())).getMonth() - 1;
    }
    let i = 0;
    for (i=currentMonthName+1;i<=11;i++) {
        monthToCasesMap[months[i]] = 0;
    }
    for (i=0;i<=currentMonthName;i++) {
        monthToCasesMap[months[i]] = 0;
    }
    monthNumberToNameMap = {
        "01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June",
        "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"
    };
    seriesDataMap = [];
    let finalSeriesDataMap = [];
    for (temp in data) {
        monthToCasesMap[monthNumberToNameMap[data[temp][0].split("-")[1]]] += data[temp][1];
    }
    for (temp in monthToCasesMap) {
        let temp1 = { "name": temp, "y": monthToCasesMap[temp], "drilldown": temp };
        seriesDataMap.push(temp1);
    }
    for (temp in seriesDataMap) {
        if (seriesDataMap[temp].y != 0) {
            finalSeriesDataMap.push(seriesDataMap[temp]);
        }
    }
    return finalSeriesDataMap;
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
    let finalDrillDownData = [];
    for (temp in drilldownData) {
        if (drilldownData[temp].data.length != 0) {
            finalDrillDownData.push(drilldownData[temp])
        }
    }
    finalData = { "series": finalDrillDownData };
    return finalData;
}

function generateCountySpecificGraph(value) {
    document.querySelector('#dropdownCountyLink').innerText = value;
    if ($('#dateFrom').val() != "" && $('#dateTo').val() != "") {
        showDatewiseChart();
    }
    else {
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
}

function showDatewiseChart() {
    let fromDateValueStr = $('#dateFrom');
    let toDateValueStr = $('#dateTo');
    let fromDateValue = new Date(fromDateValueStr.val());
    let toDateValue = new Date(toDateValueStr.val());
    let currentDate = new Date();
    let countyName = document.querySelector('#dropdownCountyLink').innerText.trim();
    if (fromDateValue > toDateValue) {
        alert("From date should not be greater than To date");
    }
    if (fromDateValue > currentDate || toDateValue > currentDate) {
        alert("From Date or To Date cannot be greater than current date");
    }
    let res = [];
    for (index in historical) {
        let tempDate = new Date(historical[index][0]);
        if (tempDate >= fromDateValue && tempDate <= toDateValue && countyName == historical[index][2]) {
            let tempArr = [];
            tempArr.push(historical[index][0]);
            tempArr.push(historical[index][1]);
            res.push(tempArr);
        }
    }
    mainChartConfig.series[0].data = generateseriesData(res);
    mainChartConfig.drilldown = generateDrillDownData(res);
    chart = Highcharts.chart('mainchart', mainChartConfig);
}

document.addEventListener('DOMContentLoaded', function () {
    chart = Highcharts.chart('mainchart', mainChartConfig);
    $( "#dateFrom" ).datepicker();
    $( "#dateTo" ).datepicker({maxDate: new Date()});
});

$("#dateFrom").on("change",function(){
    let datetemp = new Date();
    let fromDate = new Date($(this).val());
    let year = fromDate.getFullYear();
    let month = fromDate.getMonth();
    let day = fromDate.getDate();
    let dateToBeSet = new Date(year + 1, month - 1, day);
    if (dateToBeSet > datetemp) {
        dateToBeSet = datetemp;
    }
    $('#dateTo').datepicker('destroy');
    $("#dateTo").datepicker({maxDate: dateToBeSet});
});

homechart = Highcharts.chart('homechart', homeChartConfig);

workchart = Highcharts.chart('workchart', workChartConfig);