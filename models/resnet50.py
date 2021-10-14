from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

class ResNet50ImageNet:
    def __init__(self):
        self.model = ResNet50(weights='imagenet')

    def predict(self, image, top=5):
        img = image.resize((224, 224))
        img = np.array(img)
        img = np.expand_dims(img, axis=0)
        x = preprocess_input(img)
        preds = self.model.predict(x)
        # decode the results into a list of tuples (class, description, probability)
        # (one such list for each sample in the batch)
        return decode_predictions(preds, top=top)[0]
