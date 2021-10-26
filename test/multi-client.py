import time
import argparse

import requests
import argparse
import concurrent.futures
from operator import itemgetter

import numpy as np
np.set_printoptions(suppress=True)

from PIL import Image
from io import BytesIO
import base64

def classification(url, file):

    # load the input image and construct the payload for the request
    image = Image.open(file)
    buff = BytesIO()
    image.save(buff, format="JPEG")

    print('Sending requests')
    data = {'file': base64.b64encode(buff.getvalue()).decode("utf-8")}

    return requests.post(url, json=data).json()

def task(url, file):
    start_time = time.time()

    # submit the request
    try:
        r = classification(url, file)

    except Exception as e:
        print(e)

    return r, (time.time() - start_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Distributed Image Classification API')
    parser.add_argument(
        'image',
        type=str,
        help='image file'
    )
    parser.add_argument(
        '--url',
        type=str,
        help='API url',
        default='http://localhost:8080'
    )
    parser.add_argument(
        '--num_workers',
        type=int,
        help='number of workers.',
        default=5
    )
    parser.add_argument(
        '--model',
        type=str,
        help='model name', 
        choices=['vgg16_cifar10', 'vgg16', 'resnet50', 'inceptionv3'], 
        required=False, 
        default="vgg16_cifar10"
    )
    parser.add_argument(
        '--top',
        type=int,
        help='Top k classes',
        default='10'
    )
    parser.add_argument('--no-prob', dest='no_prob', action='store_true')
    parser.set_defaults(no_prob=False)

    args = parser.parse_args()

    num_workers = args.num_workers

    no_prob = 1 if args.no_prob else 0;

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(task, args.url + '/' + args.model + '?top=' + str(args.top) + '&no-prob=' + str(no_prob), args.image) for i in range(num_workers)}

        print('----- start -----')
        start_time = time.time()
        for future in concurrent.futures.as_completed(futures):
            r, data = future.result()
            if(r['success']):
                if no_prob:
                    print ('{:<15s}'.format(r['predictions'][0]['label']))
                else:
                    r = sorted(r['predictions'], key=itemgetter('probability'), reverse=True)
                    print ('{:<15s}{:.5f}'.format(r[0]['label'], r[0]['probability']))
            else:
                print(r['error'])
        print('------ end ------')

        print('Concurrent Requests: ' + str(num_workers))
        print('Total Runtime: ' + str(time.time() - start_time))
