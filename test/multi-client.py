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
        if(r['success']):
            r = sorted(r['predictions'], key=itemgetter('probability'), reverse=True)
            # for i in r:
                # print ('{:<15s}{:.5f}'.format(i['label'], i['probability']))
        else:
            print(r['error'])

    except Exception as e:
        print(e)

    return (time.time() - start_time)

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
        default=4
    )
    parser.add_argument(
        '--model',
        type=str,
        help='model name', 
        choices=['vgg16_cifar10', 'vgg16', 'resnet50', 'inceptionv3'], 
        required=False, 
        default="vgg16"
    )

    args = parser.parse_args()

    num_workers = args.num_workers

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(task, args.url + "/" + args.model, args.image) for i in range(num_workers)}

        print('----- start -----')
        start_time = time.time()
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
        print('------ end ------')

        print('Concurrent Requests: ' + str(num_workers))
        print('Total Runtime: ' + str(time.time() - start_time))
