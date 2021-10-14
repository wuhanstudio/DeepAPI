from flask import Flask, request, jsonify, send_from_directory

import numpy as np
from PIL import Image

# Data IO and Encoding-Decoding
from io import BytesIO
import base64

# Import Keras models
from models.vgg16 import VGG16Cifar10, VGG16ImageNet
from models.resnet50 import ResNet50ImageNet
from models.inceptionv3 import InceptionV3ImageNet

m_vgg16_cifar10     = VGG16Cifar10()
m_vgg16             = VGG16ImageNet()
m_resnet50          = ResNet50ImageNet()
m_inceptionv3       = InceptionV3ImageNet()

app = Flask(__name__)

# Serve the front-end
@app.route("/")
def index():
    return send_from_directory('static', "index.html")

@app.route('/<path:path>')
def send_website(path):
    print(path)
    return send_from_directory('static', path)

@app.route('/vgg16_cifar10', methods=['GET', 'POST'])
def vgg16cifar10():
    global m_vgg16_cifar10
    response = {'success': False}
    if request.method == 'POST':
        if request.json.get('file'): # image is stored as name "file"
            img = Image.open(BytesIO(base64.b64decode(request.json.get('file'))))
            if img.mode != 'RGB':
                img = img.convert('RGB')

            results = m_vgg16_cifar10.predict(img)

            response['predictions'] = []
            for i in range(0, len(results)):
                row = {'label': results[i][0], 'probability': float(results[i][1])} # numpy float is not good for json
                response['predictions'].append(row)
            response['success'] = True
            
            return jsonify(response)

    return '''
    <!doctype html>
    <title>Wrong Door</title>
    <h1>You knock the wrong door.</h1>
    '''

@app.route('/vgg16', methods=['GET', 'POST'])
def vgg16():
    global m_vgg16
    response = {'success': False}
    if request.method == 'POST':
        if request.json.get('file'): # image is stored as name "file"
            img = Image.open(BytesIO(base64.b64decode(request.json.get('file'))))
            if img.mode != 'RGB':
                img = img.convert('RGB')

            results = m_vgg16.predict(img)

            response['predictions'] = []
            for i in range(0, len(results)): # [0] as input is only one image
                row = {'label': results[i][1], 'probability': float(results[i][2])} # numpy float is not good for json
                response['predictions'].append(row)
            response['success'] = True
            
            return jsonify(response)

    return '''
    <!doctype html>
    <title>Wrong Door</title>
    <h1>You knock the wrong door.</h1>
    '''

@app.route('/resnet50', methods=['GET', 'POST'])
def resnet50():
    global m_resnet50
    response = {'success': False}
    if request.method == 'POST':
        if request.json.get('file'): # image is stored as name "file"
            img = Image.open(BytesIO(base64.b64decode(request.json.get('file'))))
            if img.mode != 'RGB':
                img = img.convert('RGB')

            results = m_resnet50.predict(img)

            response['predictions'] = []
            for i in range(0, len(results)): # [0] as input is only one image
                row = {'label': results[i][1], 'probability': float(results[i][2])} # numpy float is not good for json
                response['predictions'].append(row)
            response['success'] = True
            
            return jsonify(response)

    return '''
    <!doctype html>
    <title>Wrong Door</title>
    <h1>You knock the wrong door.</h1>
    '''

@app.route('/inceptionv3', methods=['GET', 'POST'])
def inceptionv3():
    global m_inceptionv3
    response = {'success': False}
    if request.method == 'POST':
        if request.json.get('file'): # image is stored as name "file"
            img = Image.open(BytesIO(base64.b64decode(request.json.get('file'))))
            if img.mode != 'RGB':
                img = img.convert('RGB')

            results = m_inceptionv3.predict(img)

            response['predictions'] = []
            for i in range(0, len(results)): # [0] as input is only one image
                row = {'label': results[i][1], 'probability': float(results[i][2])} # numpy float is not good for json
                response['predictions'].append(row)
            response['success'] = True
            
            return jsonify(response)

    return '''
    <!doctype html>
    <title>Wrong Door</title>
    <h1>You knock the wrong door.</h1>
    '''

if __name__ == '__main__':
    # no-thread: https://github.com/keras-team/keras/issues/2397#issuecomment-377914683
    # avoid model.predict runs before model initiated
    # To let this run on HEROKU, model.predict should run onece after initialized
    app.run(host="0.0.0.0", port=8080, threaded=False, debug=True)

    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080, threads=1)
