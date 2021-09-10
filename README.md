## Cifar10-VGG Image Classification API Server

Distributed

### Quick Start

docker run

python minimal.py

### Minimal Client

```
def classification(url, file):

    # Load the input image and construct the payload for the request
    image = Image.open(file)
    buff = BytesIO()
    image.save(buff, format="JPEG")

    print('Sending requests')
    data = {'file': base64.b64encode(buff.getvalue()).decode("utf-8")}
    return  requests.post(url, json=data).json()

res = classification('http://127.0.0.1/predict', 'cat.jpg')

# Print prediction results
res = sorted(res['predictions'], key=itemgetter('probability'), reverse=True)
for i in res:
    print('{:<15s}{:.5f}'.format(i['label'], i['probability']))

```

You should see prediction results:

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

```
$ python .\client.py 10 .\cat.jpg
```

The result:

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
