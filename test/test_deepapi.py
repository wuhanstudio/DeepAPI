import numpy as np
from PIL import Image

from deepapi.api import DeepAPI_VGG16_Cifar10

if __name__ == '__main__':

    # Load the image
    x = Image.open("dog.jpg")
    x = np.array(x)

    # Initialize the model
    model  = DeepAPI_VGG16_Cifar10('http://localhost:8080', concurrency=8)

    # Predict
    y = model.predict(np.array([x]))[0]

    # Print the result
    model.print(y)
