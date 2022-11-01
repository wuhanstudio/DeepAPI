import requests
from operator import itemgetter

import numpy as np
np.set_printoptions(suppress=True)
from PIL import Image

from io import BytesIO
import base64

import argparse

def classification(url, file):

    # Load the input image and construct the payload for the request
    image = Image.open(file)
    buff = BytesIO()
    image.save(buff, format="JPEG")

    print('Sending requests')
    data = {'file': base64.b64encode(buff.getvalue()).decode("utf-8")}

    return  requests.post(url, json=data).json()


parser = argparse.ArgumentParser(description='Distributed Image Classification Client')
parser.add_argument(
    '--url',
    type=str,
    help='API url',
    default='http://localhost:8080'
)
parser.add_argument(
    '--top',
    type=int,
    help='Top k classes',
    default='10'
)
parser.add_argument(
    '--model',
    type=str,
    help='model name', 
    choices=['vgg16_cifar10', 'vgg16', 'resnet50', 'inceptionv3'], 
    required=False, 
    default="vgg16_cifar10"
)
parser.add_argument('--no-prob', dest='no_prob', action='store_true')
parser.set_defaults(no_prob=False)

args = parser.parse_args()

no_prob = 1 if args.no_prob else 0;

res = classification(args.url + '/' + args.model + '?top=' + str(args.top) + '&no-prob=' + str(no_prob), 'cat.jpg')

# Print prediction results
if res['success']:
    if no_prob == 0:
        res = sorted(res['predictions'], key=itemgetter('probability'), reverse=True)
        for i in res:
            print('{:<15s}{:.5f}'.format(i['label'], i['probability']))
    else:
        for i in res['predictions']:
            print('{:<15s}'.format(i['label']))
else:
    print(res['error'])
