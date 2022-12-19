$(function() 
    {   //create color
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
        var chart_bar = new ApexCharts(document.querySelector("#line-chart-1"), options_bar);
        chart_bar.render();
        //bar chart end

        //pie chart start
        var options_pie = {
            series: dataPop,
            chart: {
            width: 380,
            type: 'donut',
          },
          labels: dataCate,
          colors:color,
          responsive: [{
            breakpoint: 480,
            options: {
                plotOptions: {
                    pie: {
                        expandOnClick: false,
                        donut: {
                            size: 200
                      }
                    }
                  },
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              }
            }
          }]
          };
          var chart_pie = new ApexCharts(document.querySelector("#pie-chart-1"), options_pie);
          chart_pie.render();
          //pie chart end

          // d3 word cloud start
          // 데이터 형식 text:~~~~,value:~~~~~

          //
          var data = [
            {text: "Hello", value:6260},
            {text: "happy", value:5370},
            {text: "beautiful", value:2480},
            {text: "rainbow", value:4350},
            {text: "unicorn", value:1250},
            {text: "glitter", value:3140},
            {text: "happy", value:990},
            {text: "pie", value:4230}];
          //

          var fill = d3.scaleOrdinal(d3.schemeCategory20);
          var layout = d3.layout.cloud()
                      .size([320, 320])
                      .words(wordcloud)
                      .padding(10) //space between words
                      .font('Helvetica')
                      .fontWeight("bold")
                      .on("end", draw);
                      
          layout.start();
          function draw(words) {
            d3.select("#my_dataviz")
            .append("g")
            .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter()
            .append("text")
            .text((d) => d.text)
            .style("font-size", (d) => Math.sqrt(d.value))
            .style("fill", (d, i) => fill(i))
            .style("font-family", (d) => d.font)
            .attr("text-anchor", "middle")
            .attr("transform", (d) => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")");
    }    
      //wordcloud end
})