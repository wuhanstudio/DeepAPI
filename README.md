## Deep API

> Deep Learning as Cloud APIs.

This project provides an image classification cloud service for research on **Black-box Adversarial Attacks**.

![](demo.gif)


### Quick Start

#### Using Docker:

```
docker run -p 8080:8080 wuhanstudio/deepapi
```

#### Python 3:

```
$ pip instlal deepapi

# By default, we enable all models on the server.
# Use deepapi -h to see more options.

$ deepapi
```

The website and API service are available at https://localhost:8080.



### API Client

To initiate **black-box adversarial attacks**, we can get predictions by sending a POST request to http://127.0.0.1:8080/vgg16_cifar10 without knowing details about deep learning models behind the cloud service.

#### Using Python:

```
def classification(url, file):
    # Load the input image and construct the payload for the request
    image = Image.open(file)
    buff = BytesIO()
    image.save(buff, format="JPEG")

    data = {'file': base64.b64encode(buff.getvalue()).decode("utf-8")}
    return requests.post(url, json=data).json()

res = classification('http://127.0.0.1:8080/vgg16_cifar10', 'cat.jpg')
```

This python script is available in the `test` folder. You should see prediction results by running `python3 minimal.py`:

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

#### Concurrent requests

Sending 5 concurrent requests to the API server:

```
$ python3 multi-client.py --num_workers 5 cat.jpg
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

#### Using curl:

```
export IMAGE_FILE=test/cat.jpg
(echo -n '{"file": "'; base64 $IMAGE_FILE; echo '"}') | \
curl -H "Content-Type: application/json" \
     -d @- http://127.0.0.1:8080/vgg16_cifar10
```