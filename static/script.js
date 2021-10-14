var myChart = new Chart(
    document.getElementById('myChart'),
    {
        type: 'bar',
        data: [],
        options: {
            indexAxis: 'y',
        }
    }
);

function refresh() {
    location.reload();
};

function recognize() {
    base64str = $('.drag-area img').attr('src');
    base64str = base64str.replace('data:image/jpeg;base64,', '');

    $.ajax
    ({
        type: "POST",
        url: window.location.protocol + '//' + window.location.host + '/cifar10',
        contentType : 'application/json',
        async: true,
        data: JSON.stringify({ "file": base64str}),
        success: function (res) {
            $('#prediction').show();

            // Sort predictions
            res = res.predictions.sort(function(a,b) {
                return b.probability - a.probability
            });
    
            // Class names
            const labels = res.reduce(function(pV, cV, cI){
                pV.push(cV.label);
                return pV; 
            }, []);

            // Probabilities
            const probs = res.reduce(function(pV, cV, cI){
                pV.push(cV.probability);
                return pV; 
            }, []);

            const data = {
                labels: labels,
                datasets: [{
                  axis: 'y',
                  label: 'Cifar10 Predictions',
                  data: probs,
                  fill: true,
                  backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 205, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(201, 203, 207, 0.2)',
                    'rgba(201, 203, 207, 0.2)',
                    'rgba(201, 203, 207, 0.2)',
                    'rgba(201, 203, 207, 0.2)',
                  ],
                  borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(255, 159, 64)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(54, 162, 235)',
                    'rgb(153, 102, 255)',
                    'rgb(201, 203, 207)',
                    'rgb(201, 203, 207)',
                    'rgb(201, 203, 207)',
                    'rgb(201, 203, 207)',
                  ],
                  borderWidth: 1
                }]
            };
                
            myChart.data = data;
            myChart.update();

            $([document.documentElement, document.body]).animate({
                scrollTop: $("#myChart").offset().top - 150
            }, 2000);
        }
    })
}

$(document).ready(function() {
    $('#recognize').prop('disabled', true);
    $('#prediction').hide();
});
