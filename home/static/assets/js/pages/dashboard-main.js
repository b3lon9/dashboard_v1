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
//최저가 비교 chart start
function floatchart() {
    var fill_height = $('.row-direction .flex-box').height();
    var box1_height = $('.right-column-rate.flex-box .text-center').height();
    var box2_height = $('.right-column-rate.flex-box .p-4').height();
    var chart_width = $('.card.right-box').width() * 0.9;
    var chart_height = fill_height - (box1_height + box2_height + 50 + 41.39);
    (function () {
        var options = {
            chart: {
                height: chart_height,
                type: 'line',
                fontFamily: 'GyeonggiTitleM',
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
            legend: {
                position: 'top',
                markers: {
                    width: 18,
                    height: 18,
                }
            },
            xaxis: {
                categories: serise_xaxis,
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
    // 최저가 비교 chart end
}
