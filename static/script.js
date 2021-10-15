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

var model = '';
var dataset = '';
var topk = 10;

function check() {
    if(model !== '' && dataset !== '' && $('.drag-area img').attr('src')) {
        $('#recognize').prop('disabled', false);
    }
    else {
        $('#recognize').prop('disabled', true);
    }
}

function setDataset(name) {
    dataset = name;
    if(name === 'cifar10') {
        $('#dropdownMenuButtonModel').html('VGG16');
        model = 'vgg16';
        $("#model-resnet50").hide();
        $("#model-inceptionv3").hide();
    }
    else
    {
        $("#model-resnet50").show();
        $("#model-inceptionv3").show();
    }
    check();
}

function setModel(name) {
    model = name;
    check();
}

function setTop(t) {
    topk = t
}

function refresh() {
    location.reload();
};

function recognize() {
    var base64str = $('.drag-area img').attr('src');
    var base64str = base64str.replace('data:image/jpeg;base64,', '');

    var query = ''
    if(dataset === 'cifar10') {
        query = 'vgg16_cifar10';
    }
    else if (dataset === 'imagenet') {
        // vgg16, resnet50, inceptionv3
        query = model
    }

    // console.log(window.location.protocol + '//' + window.location.host + '/' + query + '?top=' + topk.toString())

    $.ajax
    ({
        type: "POST",
        url: window.location.protocol + '//' + window.location.host + '/' + query + '?top=' + topk.toString(),
        contentType : 'application/json',
        async: true,
        data: JSON.stringify({ "file": base64str}),
        success: function (res) {
            $('#prediction').show();

            console.log(res)

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
                  label: model + '_' + dataset + ' Predictions',
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

    $(".dropdown-menu li a").click(function(){
        $(this).parents(".dropdown").find('.btn').html($(this).text());
        $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
    });
});
