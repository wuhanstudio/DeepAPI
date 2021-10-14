import requests
import argparse
import concurrent.futures

import time
import argparse
from operator import itemgetter

import numpy as np
np.set_printoptions(suppress=True)

from PIL import Image

from io import BytesIO
import base64

def classification(url, file):

    # Load the input image and construct the payload for the request
    image = Image.open(file)
    data = {'file': np.array(image).tolist()}

    print('Sending requests')
    return  requests.post(url, json=data).json()

def task(url, file):
    start_time = time.time()

    # submit the request
    try:
        r = classification(url, file)
        r = sorted(r['predictions'], key=itemgetter('probability'), reverse=True)
        # for i in r:
            # print ('{:<15s}{:.5f}'.format(i['label'], i['probability']))
    except Exception as e:
        print(e)

    return (time.time() - start_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Distributed Image Classification API')
    parser.add_argument(
        'num_workers',
        type=int,
        help='Number of workers.'
    )
    parser.add_argument(
        'image',
        type=str,
        help='image file'
    )
    args = parser.parse_args()

    num_workers = args.num_workers

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(task, "http://127.0.0.1:8080/predict_np", args.image) for i in range(num_workers)}

        print('----- start -----')
        start_time = time.time()
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            # print(data)
        print('------ end ------')

        print('Concurrent Requests: ' + str(num_workers))
        print('Total Runtime: ' + str(time.time() - start_time))
