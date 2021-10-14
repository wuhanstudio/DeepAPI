from flask import Flask, request, jsonify, send_from_directory

import numpy as np
from PIL import Image

# Data IO and Encoding-Decoding
from io import BytesIO
import base64

# Import Keras models
from models.vgg16 import cifar10vgg, cifar10_labels

app = Flask(__name__)
model = cifar10vgg().model

# Serve the front-end
@app.route("/")
def index():
    return send_from_directory('static', "index.html")

@app.route('/<path:path>')
def send_website(path):
    print(path)
    return send_from_directory('static', path)

@app.route('/cifar10', methods=['GET', 'POST'])
def predict():
    global model
    response = {'success': False}
    if request.method == 'POST':
        if request.json.get('file'): # image is stored as name "file"
            img = Image.open(BytesIO(base64.b64decode(request.json.get('file'))))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Preprocessing
            img = img.resize((32, 32))
            img = np.array(img)
            img = np.expand_dims(img, axis=0)
            mean = 120.707
            std = 64.15

            results = model.predict((img-mean)/(std+1e-7))

            response['predictions'] = []
            for i in range(0, 10): # [0] as input is only one image
                row = {'label': cifar10_labels[i], 'probability': float(results[0][i])} # numpy float is not good for json
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
