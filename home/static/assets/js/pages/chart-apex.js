$(function () {   //create color
  const root = document.documentElement;
  const rootStyle = getComputedStyle(root);
  const search1 = keyword1;
  const search2 = keyword2;
  const color_pos = rootStyle.getPropertyValue("--barchart-positive-color");
  const color_neg = rootStyle.getPropertyValue("--barchart-negative-color");
  const color_pie1 = rootStyle.getPropertyValue("--piechart-1-color");
  const color_pie2 = rootStyle.getPropertyValue("--piechart-2-color");
  const color_pie3 = rootStyle.getPropertyValue("--piechart-3-color");
  const color_pie4 = rootStyle.getPropertyValue("--piechart-4-color");
  const color_pie5 = rootStyle.getPropertyValue("--piechart-5-color");
  
  const color = [];
  var card_width = 285;
  var chart_width = $('.wordcloud-size').width();
  var chart_height = $('.wordcloud-size').height();
  console.log("chart_height : ", chart_height);
  // while (color.length < 20) {
  //   do {
  //     var arrs = Math.floor((Math.random() * 1000000) + 1);
  //   } while (color.indexOf(arrs) >= 0);
  //   color.push("#" + ("000000" + arrs.toString(16)).slice(-6));
  // }
  //end create color

  color.push('#59E0C5');
  color.push('#004295');
  color.push('#005FB7');
  color.push('#007EDB');
  color.push('#009EFF');
  var dataCate = ['1점','2점','3점','4점','5점'];

  //pie chart_1 start
  var options_donut_1 = {
    series: keyword1_pie,
    chart: {
      width: card_width,
      type: 'donut',
    },
    dataLabels: {
      enabled: false,
      style : {
        fontFamily: 'GyeonggiTitleM',
      }
    },
    labels: dataCate,
    colors: color,
    plotOptions: {
      pie: {
        expandOnClick: false,
        donut: {
          size: '50%'
        },
      }
    },
    // title:{
    //   text:search1 + ' 별점별 비율', 
    // },
    legend: {
      fontFamily: 'GyeonggiTitleM',
    },
    responsive: [{
      breakpoint: 480,
      options: {
        
        chart: {
          width: 200
        },
        legend: {
          position: 'bottom',
        }
      }
    }]
  };
  var chart_donut_1 = new ApexCharts(document.querySelector("#pie-chart-1"), options_donut_1);
  chart_donut_1.render();
  //pie chart_1 end

  //pie chart_2 start
  var options_donut_2 = {
    series: keyword1_pie,
    chart: {
      width: card_width,
      type: 'donut',
    },
    dataLabels: {
      enabled: false
    },
    labels: dataCate,
    colors: color,
    plotOptions: {
      pie: {
        expandOnClick: false,
        donut: {
          size: '50%'
        }
      }
    },
    legend: {
      fontFamily: 'GyeonggiTitleM',
    },
    // title:{
    //   text:search2 + ' 별점별 비율', 
    // },
    responsive: [{
      breakpoint: 480,
      options: {
        
        chart: {
          width: 200
        },
        legend: {
          position: 'bottom'
        }
      }
    }]
  };
  var chart_donut_2 = new ApexCharts(document.querySelector("#pie-chart-2"), options_donut_2);
  chart_donut_2.render();
  //pie chart_2 end

  // d3 word cloud 1번 4-5점
  var fill = d3.scaleOrdinal(d3.schemeCategory20);
  var layout = d3.layout.cloud()
    .size([chart_width, chart_height])
    .words(keyword1_wordcloud_45)
    .padding(2) //space between words
    .font('Helvetica')
    .fontWeight("bold")
    .rotate(0)//word cloud 형태
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
      // .style("fill", (d, i) => fill(i))
      .style("fill", "#009EFF")
      .style("font-family", (d) => d.font)
      .attr("text-anchor", "middle")
      .attr("transform", (d) => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")");
  }
  //wordcloud end

  // d3 word cloud 1번 1-3점
  var layout = d3.layout.cloud()
    .size([chart_width, chart_height])
    .words(keyword1_wordcloud_13)
    .padding(2) //space between words
    .font('Helvetica')
    .fontWeight("bold")
    .rotate(0)//word cloud 형태
    .on("end", draw_1);

  layout.start();
  function draw_1(words) {
    d3.select("#my_dataviz_2")
      .append("g")
      .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
      .selectAll("text")
      .data(words)
      .enter()
      .append("text")
      .text((d) => d.text)
      .style("font-size", (d) => Math.sqrt(d.value))
      // .style("fill", (d, i) => fill(i))
      .style("fill", "#FF5370")
      .style("font-family", (d) => d.font)
      .attr("text-anchor", "middle")
      .attr("transform", (d) => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")");
  }
  //wordcloud end

  // d3 word cloud 2번 4-5점
  var layout = d3.layout.cloud()
    .size([chart_width, chart_height])
    .words(keyword2_wordcloud_45)
    .padding(2) //space between words
    .font('Helvetica')
    .fontWeight("bold")
    .rotate(0)//word cloud 형태
    .on("end", draw_2);

  layout.start();
  function draw_2(words) {
    d3.select("#my_dataviz_3")
      .append("g")
      .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
      .selectAll("text")
      .data(words)
      .enter()
      .append("text")
      .text((d) => d.text)
      .style("font-size", (d) => Math.sqrt(d.value))
      // .style("fill", (d, i) => fill(i))
      .style("fill", "#009EFF")
      .style("font-family", (d) => d.font)
      .attr("text-anchor", "middle")
      .attr("transform", (d) => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")");
  }
  //wordcloud end

  // d3 word cloud 2번 1-3점
  var layout = d3.layout.cloud()
    .size([chart_width, chart_height])
    .words(keyword2_wordcloud_13)
    .padding(2) //space between words
    .font('Helvetica')
    .fontWeight("bold")
    .rotate(0)//word cloud 형태
    .on("end", draw_3);

  layout.start();
  function draw_3(words) {
    d3.select("#my_dataviz_4")
      .append("g")
      .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
      .selectAll("text")
      .data(words)
      .enter()
      .append("text")
      .text((d) => d.text)
      .style("font-size", (d) => Math.sqrt(d.value))
      // .style("fill", (d, i) => fill(i))
      .style("fill", "#FF5370")
      .style("font-family", (d) => d.font)
      .attr("text-anchor", "middle")
      .attr("transform", (d) => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")");
  }
  //wordcloud end
})