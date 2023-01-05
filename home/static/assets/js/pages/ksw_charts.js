const bar_pos = "--barchart-positive-color";
const bar_neg = "--barchart-negative-color";

const root = document.documentElement;
const rootStyle = getComputedStyle(root);
const color_pos = rootStyle.getPropertyValue(bar_pos);
const color_neg = rootStyle.getPropertyValue(bar_neg);



function changeClassName(s_num) {
    s_num = String(s_num)
    var cl1 = document.getElementById(s_num+'_pos').className;
    var cl2 = document.getElementById(s_num+'_neg').className;

    if (cl1.length > 0){
        document.getElementById(s_num+'_pos').className = '';
        document.getElementById(s_num+'_neg').className = 'on';

        document.getElementById('theme-' + s_num + '-pos-btn').className = '';
        document.getElementById('theme-' + s_num + '-neg-btn').className = 'theme-negative-btn';

        document.getElementById(s_num+'_pos_post').style.display = 'none';
        document.getElementById(s_num+'_neg_post').style.display = 'block';

    }
    else{
        
        document.getElementById(s_num+'_neg').className = '';
        document.getElementById(s_num+'_pos').className = 'on';

        document.getElementById('theme-' + s_num + '-pos-btn').className = 'theme-positive-btn';
        document.getElementById('theme-' + s_num + '-neg-btn').className = '';

        document.getElementById(s_num+'_neg_post').style.display = 'none';
        document.getElementById(s_num+'_pos_post').style.display = 'block';

    }

    return;
}

function category(cat) {

    var li = document.getElementsByClassName("original-data-item");
    const checkbox = document.getElementById('btn-check-' + cat);

    if (!checkbox.checked){
        for (var i = 0; i < li.length; i++){
            var element = li.item(i)
            if (element.id == cat){
                element.style.display = 'none';
            }
            

        }
    }
    else{
        for (var i = 0; i < li.length; i++){
            var element = li.item(i)
            if (element.id == cat){
                element.style.display = 'flex';
            }
            
        }
    }



    return;
}

(function() {

  //am4core.useTheme(am4themes_animated);

  // Create chart
  var chart = am4core.create("chartdiv", am4plugins_forceDirected.ForceDirectedTree);

  // Create series
  var series = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())
  chart.legend = new am4charts.Legend();
  let markerTemplate = chart.legend.markers.template;

  chart.fontSize = '12';
  chart.fontFamily = 'GyeonggiTitleM';
  chart.fontWeight = '0';

  markerTemplate.width = 18;
  markerTemplate.height = 18;
  // Set data
  // let title = chart.titles.create();
  // title.text = '커뮤니티 투표수';
  // title.fontSize=22;
  // title.fontWeight='blod';

  series.data = [{
      "name": keyword1,
      "value": keyword1_vote,
      "link": [keyword2],
      "fixed": true,
      "x": am4core.percent(35),
      "y": am4core.percent(50), 
    }, {
      "name": keyword2,
      "value": keyword2_vote
      ,"link": [keyword1],
      "fixed": true,
      "x": am4core.percent(65),
      "y": am4core.percent(50), 
    }, ];

    series.colors.list = [
      am4core.color("#009EFF"),
      am4core.color("#3EE8C6"),

      ];
    


  series.links.template.strokeOpacity = 0;
  series.dataFields.fixed = "fixed";
  series.nodes.template.propertyFields.x = "x";
  series.nodes.template.propertyFields.y = "y";
  
  
  // Set up data fields
  series.dataFields.value = "value";
  series.dataFields.name = "name";

  series.dataFields.id = "name";
  series.dataFields.linkWith = "link";
  
  series.nodes.template.label.text = "{value}";
  series.fontSize = 20;
  series.minRadius = 15;
  series.maxRadius = 60;
  series.centerStrength = 0.5;
  

})();


document.addEventListener('DOMContentLoaded', () => {

    const ctx = document.getElementById('myChart').getContext('2d');

    const DATA_COUNT = 7;
    const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

    var min_neg = Math.min(...negative_bar)
    var max_pos = Math.max(...positve_bar)

    max_pos = parseInt(max_pos / 0.8)
    min_neg = parseInt(min_neg / 0.8)

    var box_width = $('.card.p-4.right-box .card-body').width();
    var box_height = $('.card.p-4.right-box .card-body').height();
    
    console.log("right box2 width:", box_width);
    console.log("right box2 height:", box_height);
    // if (box_width > 388) box_width = 388;
    // if (box_height > 214) box_height = 214;

    // console.log("right box2 width:", box_width);
    // console.log("right box2 height:", box_height);
    
    var val = Math.max(max_pos,Math.abs(min_neg))

    const labels = [keyword1,keyword2];
    const data = {
    labels: labels,
    datasets: [
        {
        label: '긍정',
        data: positve_bar,
        borderColor: color_pos,            
        backgroundColor: color_pos,//Utils.transparentize('#4dc9f6', 0.5),
        pointStyle: 'circle',
        borderRadius: 5,
        },
        {
        label: '부정',
        data: negative_bar,
        borderColor: color_neg,
        backgroundColor: color_neg,//Utils.transparentize('#f67019',, 0.5),
        pointStyle: 'circle',
        borderRadius: 5,
        }
    ]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
          indexAxis: 'y',
          maintainAspectRatio :false,
          // Elements options apply to all of the options unless overridden in a dataset
          // In this case, we are setting the border of each horizontal bar to be 2px wide
          elements: {
            bar: {
              borderWidth: 2,
            }
          },
          responsive: true,
          plugins: {
            legend: {
                labels: {
                    usePointStyle: true,
                    
                    font : {
                      size:12,
                      family:'GyeonggiTitleM',
                      weight:'1',
                    }
                    },
                position: 'top',
                pointRadius: 5,
            },
            title: {
              display: false,
              // text: '긍부정 리뷰수',
              align:'center',
              font:{
                size:22
              }
            }
          },
          scales: {
            x: {
                display:true,
                min:-val,
                max:val,
                grid: {
                    color: function(context) {
                        if (context.tick.value == 0) {
                          return '#939598';
                        } else {
                          return '#ffffff';
                        }
            
                        return '#000000';
                      },
                    },

              

            },
            y:{
                display:true,
                height:box_height,
                grid: {
                    color: '#ffffff',
                    },
                
            }
          }
        },
    };

    var chart = new Chart(ctx, config);
})();

