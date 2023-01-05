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
    /* 차트 높이 수정 2023.01.02. */
    var fill_height = $('.row-direction .flex-box').height();
    // console.log('fill_height height:', fill_height);
    var box1_height = $('.right-column-rate.flex-box .text-center').height();
    // console.log('box1_height height:', box1_height);
    var box2_height = $('.right-column-rate.flex-box .p-4').height();
    // console.log('box2_height height:', box2_height);
    var chart_width = $('.card.right-box').width() * 0.9;
    var chart_height = fill_height - (box1_height + box2_height + 50 + 41.39);

    // console.log('right-box3 width:', chart_width);
    // console.log('right-box3 height:', chart_height);

    // chart_height = 200;
    // console.log('right-box3 height:', chart_height);
    (function () {
        var options = {
            chart: {
                height: chart_height,
                width: chart_width,
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
            // title:{
            //     text:"최저가 비교",
            //     align:'center',
            //     style:{
            //         fontSize:'22px',
            //         fontWeight:'bold',
            //     }
            // },
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
