from flask import Flask, request, redirect, url_for, jsonify, Response
from flask import Flask, send_from_directory
from flask import render_template

from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
import numpy as np
from PIL import Image

# Data IO and Encoding-Decoding
from io import BytesIO
import base64

app = Flask(__name__)
model = None

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras import regularizers

class cifar10vgg:
    def __init__(self,train=False):
        self.num_classes = 10
        self.weight_decay = 0.0005
        self.x_shape = [32,32,3]

        self.model = self.build_model()
        self.model.load_weights('cifar10vgg.h5')
        self.model.summary()

    def build_model(self):
        # Build the network of vgg for 10 classes with massive dropout and weight decay as described in the paper.

        model = Sequential()
        weight_decay = self.weight_decay

        model.add(Conv2D(64, (3, 3), padding='same',
                         input_shape=self.x_shape,kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.3))

        model.add(Conv2D(64, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())

        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(128, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))

        model.add(Conv2D(128, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())

        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(256, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))

        model.add(Conv2D(256, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))

        model.add(Conv2D(256, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())

        model.add(MaxPooling2D(pool_size=(2, 2)))


        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))

        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))

        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())

        model.add(MaxPooling2D(pool_size=(2, 2)))


        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))

        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))

        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())

        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.5))

        model.add(Flatten())
        model.add(Dense(512,kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())

        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes))
        model.add(Activation('softmax'))
        return model

def load_model():
    global model
    model = cifar10vgg().model
    # model = VGG16(weights='imagenet', include_top=True)

# Serve the front end
@app.route("/")
def index():
    return send_from_directory('static', "index.html")

@app.route('/<path:path>')
def send_website(path):
    print(path)
    return send_from_directory('static', path)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    global model
    labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    response = {'success': False}
    if request.method == 'POST':
        if request.json.get('file'): # image is stored as name "file"
            img = Image.open(BytesIO(base64.b64decode(request.json.get('file'))))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.resize((32, 32))
            img = np.array(img)
            img = np.expand_dims(img, axis=0)
            # inputs = preprocess_input(img)
            mean = 120.707
            std = 64.15
            results = model.predict((img-mean)/(std+1e-7))
            # results = decode_predictions(results, top=10)

            response['predictions'] = []
            for i in range(0, 10): # [0] as input is only one image
                row = {'label': labels[i], 'probability': float(results[0][i])} # numpy float is not good for json
                response['predictions'].append(row)
            response['success'] = True
            return jsonify(response)

    return '''
    <!doctype html>
    <title>Wrong Door</title>
    <h1>You knock the wrong door.</h1>
    '''

@app.route('/predict_np', methods=['GET', 'POST'])
def predict_np():
    labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    response = {'success': False}
    if request.method == 'POST':
        if request.json.get('file'): # image is stored as name "file"
            img = Image.fromarray( (np.array(request.json['file']) * 255).astype(np.uint8) )
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.resize((32, 32))
            img = np.array(img)
            img = np.expand_dims(img, axis=0)
            # inputs = preprocess_input(img)
            mean = 120.707
            std = 64.15
            results = model.predict((img-mean)/(std+1e-7))
            # results = decode_predictions(results, top=10)

            response['predictions'] = []
            for i in range(0, 10): # [0] as input is only one image
                row = {'label': labels[i], 'probability': float(results[0][i])} # numpy float is not good for json
                response['predictions'].append(row)
            response['success'] = True
            return jsonify(response)

    return '''
    <!doctype html>
    <title>Wrong Door</title>
    <h1>You knock the wrong door.</h1>
    '''

if __name__ == '__main__':
    load_model()
    # no-thread: https://github.com/keras-team/keras/issues/2397#issuecomment-377914683
    # avoid model.predict runs before model initiated
    # To let this run on HEROKU, model.predict should run onece after initialized
    # app.run(host="0.0.0.0", port=80, threaded=False)

    from waitress import serve
    serve(app, host="0.0.0.0", port=80, threads=1)
