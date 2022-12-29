'use strict';
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function() {
        floatchart()
    }, 100);
    // [ campaign-scroll ] start
    var px = new PerfectScrollbar('.customer-scroll', {
        wheelSpeed: .5,
        swipeEasing: 0,
        wheelPropagation: 1,
        minScrollbarLength: 40,
    });
    var px = new PerfectScrollbar('.customer-scroll1', {
        wheelSpeed: .5,
        swipeEasing: 0,
        wheelPropagation: 1,
        minScrollbarLength: 40,
    });
    var px = new PerfectScrollbar('.customer-scroll2', {
        wheelSpeed: .5,
        swipeEasing: 0,
        wheelPropagation: 1,
        minScrollbarLength: 40,
    });
    var px = new PerfectScrollbar('.customer-scroll3', {
        wheelSpeed: .5,
        swipeEasing: 0,
        wheelPropagation: 1,
        minScrollbarLength: 40,
    });
    // [ campaign-scroll ] end
});

function floatchart() {
    (function () {
        var options = {
            chart: {
                height: 220,
                width: 460,
                type: 'line',
                zoom: {
                    enabled: false
                },
                toolbar: {
                    show: false,
                },
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                width: 2,
                curve: 'smooth'
            },
            series:[keyword1_serise,keyword2_serise],
            // series: [{
            //     name: 'Arts',
            //     data: [20, 50, 30, 60, 30, 50]
            // }, {
            //     name: 'Commerce',
            //     data: [60, 30, 65, 45, 67, 35]
            // }],
            legend: {
                position: 'top',
            },
            xaxis: {
                categories: serise_xaxis,//['1/11/2000', '2/11/2000', '3/11/2000', '4/11/2000', '5/11/2000', '6/11/2000'],
                axisBorder: {
                    show: false,
                },
                label: {
                    style: {
                        color: '#ccc'
                    }
                },
            },
            yaxis: {
                show: true,
                min: data_min,
                max: data_max,
                tickAmount: 3,
                labels: {
                    style: {
                        color: '#ccc'
                    },
                    formatter: function(val, index) {
                        const cn1 = parseInt(val).toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
                        return cn1;
                    }
                }
            },
            colors: ['#73b4ff', '#59e0c5'],
            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'light',
                    gradientToColors: ['#4099ff', '#2ed8b6'],
                    shadeIntensity: 0.5,
                    type: 'horizontal',
                    opacityFrom: 1,
                    opacityTo: 1,
                    stops: [0, 100]
                },
            },
            markers: {
                size: 5,
                colors: ['#4099ff', '#2ed8b6'],
                opacity: 0.9,
                strokeWidth: 2,
                hover: {
                    size: 7,
                }
            },
            grid: {
                borderColor: '#cccccc3b',
            }
        }
        var chart = new ApexCharts(document.querySelector("#unique-visitor-chart"), options);
        chart.render();
    })();
    // [ unique-visitor-chart ] end
}
