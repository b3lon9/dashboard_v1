$(function() {
    //create color
    const color =[];
    while (color.length < 20) {
        do {
            var arrs = Math.floor((Math.random()*1000000)+1);
        } while (color.indexOf(arrs) >= 0);
        color.push("#" + ("000000" + arrs.toString(16)).slice(-6));
    }
    //end create color
    //call database data
    const city_json = dict
    const wc_json = wordcloud
    var wc= []
    var dataYear = []
    var dataPop=[]
    var dataCate=[]
    //create input data
    for(var i = 0; i< wc_json.length;i++){
      wc.push({
          text:String(wc_json[i].text),
          value:wc_json[i].value,
    });
    }
    for(var i = 0; i< city_json.length;i++){
        dataCate.push(
            String(city_json[i].name),
        );
    }
    for(var i = 0; i< city_json.length;i++){
        dataYear.push(
            String(city_json[i].year)
        );
    }
    for(var i = 0; i< city_json.length;i++){
        dataPop.push(
            city_json[i].population);
    }
    console.log(dataPop)
    //end create data
    //bar chart start
    var options_bar = {
        series: [{
          name: "Desktops",
          data: dataPop
      }],
        chart: {
        height: 350,
        type: 'line',
        zoom: {
          enabled: false
        }
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'straight'
      },
      title: {
        text: 'Product Trends by Month',
        align: 'left'
      },
      grid: {
        row: {
          colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
          opacity: 0.5
        },
      },
      xaxis: {
        categories: dataYear,
      }
      };
    var chart_bar = new ApexCharts(document.querySelector("#unique-visitor-chart"), options_bar);
    chart_bar.render();

})
