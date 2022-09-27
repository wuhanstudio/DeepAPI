## Deep API

> Deep Learning as Cloud APIs.

This project provides pre-trained deep learning models as a cloud API service. A web interface is available as well.

![](demo.gif)


* [Quick Start](#quick-start)
* [API Client](#api-client)
  + [Using curl](#using-curl)
  + [Using Python](#using-python)
* [Concurrent clients](#concurrent-clients)
* [Full APIs](#full-apis)
  + [Post URLs](#post-urls)
  + [Post Data (JSON)](#post-data-json)
  + [Query Parameters](#query-parameters)
  + [Returns (JSON)](#returns-json)
  
  

### Quick Start

#### Using Docker:

CPU:

```
docker run -p 8080:8080 wuhanstudio/deepapi
```

GPU:

```
docker run -p 8080:8080 wuhanstudio/deepapi:gpu
```

#### Python 3:

```
$ pip instlal deepapi
# By default, we enable all models on the server.
$ deepapi
```

Navigate to https://localhost:8080



### API Client

It's possible to get predictions by sending a POST request to http://127.0.0.1:8080/vgg16_cifar10. 

#### Using curl:

```
export IMAGE_FILE=test/cat.jpg
(echo -n '{"file": "'; base64 $IMAGE_FILE; echo '"}') | \
curl -H "Content-Type: application/json" \
     -d @- http://127.0.0.1:8080/vgg16_cifar10
```

#### Using Python:

```
def classification(url, file):
    # Load the input image and construct the payload for the request
    image = Image.open(file)
    buff = BytesIO()
    image.save(buff, format="JPEG")

    data = {'file': base64.b64encode(buff.getvalue()).decode("utf-8")}
    return requests.post(url, json=data).json()

res = classification('http://127.0.0.1:8080/vgg', 'cat.jpg')
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



### Concurrent clients

Sending 5 concurrent requests to the api server:

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



### Full APIs

#### Post URLs:

| Model        | Dataset  | Post URL                            |
| ------------ | -------- | ----------------------------------- |
| VGG-16       | Cifar10  | http://127.0.0.1:8080/vgg16_cifar10 |
| VGG-16       | ImageNet | http://127.0.0.1:8080/vgg16         |
| Resnet-50    | ImageNet | http://127.0.0.1:8080/resnet50      |
| Inception v3 | ImageNet | http://127.0.0.1:8080/inceptionv3   |

#### Post Data (JSON):

```
{
  "file": ""
}
```

#### Query Parameters:

| Name    | Type    | Default | Value                                                        |
| ------- | ------- | ------- | ------------------------------------------------------------ |
| top     | integer | 10      | One of [1, 3, 5, 10], top=5 returns top 5 predictions.       |
| no-prob | integer | 0       | no-prob=1 returns labels without probabilities. no-prob=0 returns labels and probabilities. |

Example post urls (returns top 10 predictions with probabilities):

```
http://127.0.0.1:8080/vgg16?top=10&no-prob=0
```

#### Returns (JSON):

| Key         | Value                                                        |
| ----------- | ------------------------------------------------------------ |
| success     | True / False                                                 |
| Predictions | Array of prediction results, each element contains {"labels": "cat", "probability": 0.99} |
| error       | The error message if any                                     |

Example returned json:

```
{
  "success": true,
  "predictions": [
    {
      "label": "cat",
      "probability": 0.9996376037597656
    },
    {
      "label": "dog",
      "probability": 0.0002855948405340314
    },
    {
      "label": "deer",
      "probability": 0.000021985460989526473
    },
    {
      "label": "bird",
      "probability": 0.000021391952031990513
    },
    {
      "label": "horse",
      "probability": 0.000013297495570441242
    },
    {
      "label": "airplane",
      "probability": 0.000006046993803465739
    },
    {
      "label": "ship",
      "probability": 0.0000044226785576029215
    },
    {
      "label": "frog",
      "probability": 0.0000036349929359857924
    },
    {
      "label": "truck",
      "probability": 0.0000035354278224986047
    },
    {
      "label": "automobile",
      "probability": 0.000002384880417594104
    }
  ],
}
```



### References

- https://github.com/geifmany/cifar-vgg

- https://keras.io/api/applications/

