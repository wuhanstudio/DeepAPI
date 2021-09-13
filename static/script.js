
function refresh() {
    location.reload();
};

function recognize() {
    base64str = $('.drag-area img').attr('src');
    base64str = base64str.replace('data:image/jpeg;base64,', '');

    $.ajax
    ({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: window.location.protocol + '//' + window.location.hostname + '/predict',
        contentType : 'application/json',
        async: true,
        //json object to sent to the authentication url
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

$('#recognize').prop('disabled', true);
$('#prediction').hide();

//selecting all required elements
const dropArea = document.querySelector(".drag-area"),
dragText = dropArea.querySelector("header"),
button = dropArea.querySelector("button"),
input = dropArea.querySelector("input");
let file;                                       // this is a global variable and we'll use it inside multiple functions

button.onclick = ()=>{
input.click();                                  // if user click on the button then the input also clicked
}

input.addEventListener("change", function(){
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); 
});


//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault();                       // preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event)=>{
  event.preventDefault();                                           // preventing from default behaviour
  // getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0];
  showFile();
});

function showFile(){
  let fileType = file.type;                                         // getting selected file type
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"];   // adding some valid image extensions in array
  if(validExtensions.includes(fileType)){                           // if user selected file is an image file
    let fileReader = new FileReader();                              // creating new FileReader object
    fileReader.onload = ()=>{
      let fileURL = fileReader.result;                              // passing user file source in fileURL variable
      let imgTag = `<img src="${fileURL}" alt="">`;                 // creating an img tag and passing user selected file source inside src attribute
      dropArea.innerHTML = imgTag;                                  // adding that created img tag inside dropArea container
    $('#recognize').prop('disabled', false);
    }
    fileReader.readAsDataURL(file);
  }else{
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}
