## Image Classification Online (Cifar10-VGG16)

![](demo.gif)

### Quick Start

```
$ conda env create -f environment.yml
$ conda activate cloudapi
$ python main.py
```

Navigate to https://localhost



### Using Docker

```
docker run -p 80:80 wuhanstudio/adversarial-classification
```

### Deploy to Google Cloud App Engine

```
# GCP App Engined does not allow access to models on local disk
# Thus, you need to upload cifar10vgg.h5 to a public avaiable file server
# Then change MODEL_URL in app.yml to be the download address of your model 
gcloud app deploy .\app.yml
```


### API Client

It's possible to get prediction results by sending a POST request to http://127.0.0.1/predict. 

```
def classification(url, file):
    # Load the input image and construct the payload for the request
    image = Image.open(file)
    buff = BytesIO()
    image.save(buff, format="JPEG")

    data = {'file': base64.b64encode(buff.getvalue()).decode("utf-8")}
    return requests.post(url, json=data).json()

res = classification('http://127.0.0.1/predict', 'cat.jpg')
```

This python script is available as `test/minimal.py`. You should see prediction results by running `python minimal.py`:

```
cat            0.99804
deer           0.00156
truck          0.00012
airplane       0.00010
dog            0.00009
bird           0.00005
ship           0.00003
frog           0.00001
horse          0.00001
automobile     0.00001
```

### Concurrent client test

Sending 10 concurrent requests to the api server:

```
$ python client.py 5 cat.jpg
```

You should see the result:

```
----- start -----
Sending requests
Sending requests
Sending requests
Sending requests
Sending requests
------ end ------
Concurrent Requests: 5
Total Runtime: 2.441638708114624
```
