## Cifar10-VGG Image Classification API Server

Distributed

### Quick Start

docker run

python minimal.py

### Minimal Client

```
import requests
from operator import itemgetter

import numpy as np
np.set_printoptions(suppress=True)
from PIL import Image

def classification(url, file):
    # load the input image and construct the payload for the request
    image = Image.open(file)
    data = {'file': np.asarray(image).tolist()}
    res = requests.post(url, json=data).json()

    res = sorted(res['predictions'], key=itemgetter('probability'), reverse=True)
    for i in res:
        print('{:<15s}{:.5f}'.format(i['label'], i['probability']))


classification('http://127.0.0.1:5000/predict', 'cat.jpg')
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
