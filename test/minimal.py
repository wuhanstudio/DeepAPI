import requests
from operator import itemgetter

import numpy as np
np.set_printoptions(suppress=True)
from PIL import Image

from io import BytesIO
import base64

def classification(url, file):

    # Load the input image and construct the payload for the request
    image = Image.open(file)
    buff = BytesIO()
    image.save(buff, format="JPEG")

    print('Sending requests')
    data = {'file': base64.b64encode(buff.getvalue()).decode("utf-8")}
    return  requests.post(url, json=data).json()

res = classification('http://127.0.0.1:8080/predict', 'cat.jpg')

# Print prediction results
res = sorted(res['predictions'], key=itemgetter('probability'), reverse=True)
for i in res:
    print('{:<15s}{:.5f}'.format(i['label'], i['probability']))
