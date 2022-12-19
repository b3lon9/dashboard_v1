function changeClassName(s_num) {
    s_num = String(s_num)
    var cl1 = document.getElementById(s_num+'_pos').className;
    var cl2 = document.getElementById(s_num+'_neg').className;

    if (cl1.length > 0){
        document.getElementById(s_num+'_pos').className = '';
        document.getElementById(s_num+'_neg').className = 'on';

        document.getElementById(s_num+'_pos_post').style.display = 'none';
        document.getElementById(s_num+'_neg_post').style.display = 'block';

    }
    else{
        
        document.getElementById(s_num+'_neg').className = '';
        document.getElementById(s_num+'_pos').className = 'on';

        document.getElementById(s_num+'_neg_post').style.display = 'none';
        document.getElementById(s_num+'_pos_post').style.display = 'block';

    }

    return;
}

function category(cat) {

    var li = document.getElementsByClassName("original-data-item");
    const checkbox = document.getElementById('btn-check-' + cat);
    console.log(cat)

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
document.addEventListener('DOMContentLoaded', () => {

    const ctx = document.getElementById('myChart').getContext('2d');

    const DATA_COUNT = 7;
    const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

    const labels = ['갤럭시','아이폰'];
    const data = {
    labels: labels,
    datasets: [
        {
        label: '긍정',
        data: [8,2],
        borderColor: '#4dc9f6',            
        backgroundColor: '#4dc9f6',//Utils.transparentize('#4dc9f6', 0.5),
        pointStyle: 'circle',
        borderRadius: 10,
        
        },
        {
        label: '부정',
        data: [-3,-7],
        borderColor: '#f67019',
        backgroundColor: '#f67019',//Utils.transparentize('#f67019',, 0.5),
        pointStyle: 'circle',
        borderRadius: 10,
        
        
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
                    
                    },
                position: 'top',
                pointRadius: 5,
            },
            title: {
              display: false,
              //text: 'Chart.js Horizontal Bar Chart'
            }
          },
          scales: {
            x: {
                display:true,
                min:-10,
                max:10,
                grid: {
                    color: function(context) {
                        if (context.tick.value == 0) {
                          return '#000000';
                        } else {
                          return '#ffffff';
                        }
            
                        return '#000000';
                      },
                    },

              

            },
            y:{
                display:true,
                grid: {
                    color: '#ffffff',
                    },
                
            }
          }
        },
    };

    var chart = new Chart(ctx, config);
})();