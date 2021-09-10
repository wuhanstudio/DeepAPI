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
