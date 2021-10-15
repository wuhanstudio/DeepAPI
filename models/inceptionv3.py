from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
import numpy as np

class InceptionV3ImageNet:
    def __init__(self):
        self.model = InceptionV3(weights='imagenet')

    def predict(self, image, top=10):
        img = image.resize((299, 299))
        img = np.array(img)
        img = np.expand_dims(img, axis=0)
        x = preprocess_input(img)
        preds = self.model.predict(x)
        # decode the results into a list of tuples (class, description, probability)
        # (one such list for each sample in the batch)
        return decode_predictions(preds, top=top)[0]
