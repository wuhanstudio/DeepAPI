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
var noProb = 0;
var filename = '';
var url = ''

// Codegen tamplate
var python_template = '';
var curl_template = '';

function check() {
    if(model !== '' && dataset !== '' && $('.drag-area img').attr('src')) {
        $('#recognize').prop('disabled', false);
    }
    else {
        $('#recognize').prop('disabled', true);
    }

    var query = ''
    if(dataset === 'cifar10') {
        query = 'vgg16_cifar10';
    }
    else if (dataset === 'imagenet') {
        // vgg16, resnet50, inceptionv3
        query = model
    }

    url =  window.location.protocol + '//' + window.location.host + '/' + query + '?top=' + topk.toString() + '&no-prob=' + noProb

    // Generate code
    $('#python-code').html(python_template.replace('T_URL', url).replace('T_FILE', filename));
    $('#curl-code').html(curl_template.replace('T_URL', url).replace('T_FILE', filename));
}

function setFile(name) {
    filename = name;
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
    topk = t;
    check();
}

function refresh() {
    location.reload();
};

function recognize() {
    var base64str = $('.drag-area img').attr('src');
    var base64str = base64str.replace('data:image/jpeg;base64,', '');

    $.ajax
    ({
        type: "POST",
        url: url,
        contentType : 'application/json',
        async: true,
        data: JSON.stringify({ "file": base64str}),
        success: function (res) {

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

            if (noProb == 0) {

                $("#with-prob").show();
                $("#no-prob").hide();


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
            }
            else {

                $("#with-prob").hide();
                $("#no-prob").show();

                res_table = '<ul class="list-group text-center mt-3">'
                for (var i = 0; i < labels.length; i++) {
                    res_table = res_table + '<li class="list-group-item">' + labels[i] + '</li>'
                }
                res_table = res_table + '</ul>';
                $("#no-prob").html(res_table);
            }

            $('#prediction').show();

            $([document.documentElement, document.body]).animate({
                scrollTop: $("#prediction").offset().top - 30
            }, 2000);

            $('#codegen').show();
        }
    })
}

function addCopyButtons(clipboard) {
    document.querySelectorAll('pre > code').forEach(function (codeBlock) {
        var button = document.createElement('button');
        button.className = 'btn btn-primary copy-code-button';
        button.type = 'button';
        button.innerText = 'Copy';

        button.addEventListener('click', function () {
            clipboard.writeText(codeBlock.innerText).then(function () {
                /* Chrome doesn't seem to blur automatically,
                   leaving the button in a focused state. */
                button.blur();

                button.innerText = 'Copied!';

                setTimeout(function () {
                    button.innerText = 'Copy';
                }, 2000);
            }, function (error) {
                button.innerText = 'Error';
            });
        });

        var pre = codeBlock.parentNode;
        if (pre.parentNode.classList.contains('highlight')) {
            var highlight = pre.parentNode;
            highlight.parentNode.insertBefore(button, highlight);
        } else {
            pre.parentNode.insertBefore(button, pre);
        }
    });
}

$(document).ready(function() {
    // Show probabilities by default
    $("#flexSwitchCheckShowProb").prop("checked", true);
    
    // Diable the button if no file is selected
    $('#recognize').prop('disabled', true);

    // Hide prediction and codegen
    $('#prediction').hide();
    $('#codegen').hide();

    // Show selected dataset and model
    $(".dropdown-menu li a").click(function(){
        $(this).parents(".dropdown").find('.btn').html($(this).text());
        $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
    });

    $("#flexSwitchCheckShowProb").on('change', function() {
        if ($(this).is(':checked')) {
            noProb = 0;
        }
        else {
            noProb = 1;
        }
    });

    // Copy to clipboard
    if (navigator && navigator.clipboard) {
        addCopyButtons(navigator.clipboard);
    } else {
        var script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/clipboard-polyfill/2.7.0/clipboard-polyfill.promise.js';
        script.integrity = 'sha256-waClS2re9NUbXRsryKoof+F9qc1gjjIhc2eT7ZbIv94=';
        script.crossOrigin = 'anonymous';
        script.onload = function() {
            addCopyButtons(clipboard);
        };
    
        document.body.appendChild(script);
    }

    python_template = $('#python-code').html();
    curl_template = $('#curl-code').html();
});
