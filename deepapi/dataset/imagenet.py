from deepapi.dataset.imagenet_class_index import imagenet_json

# imagenet_json['134'] = ["n02012849", "crane"],
imagenet_json['517'] = ['n02012849', 'crane_bird']

# imagenet_json['638'] = ['n03710637', 'maillot']
imagenet_json['639'] = ['n03710721', 'maillot_tank_suit']

def decode_predictions(preds, top=5):
    """Decodes the prediction of an ImageNet model.

    Args:
    preds: Numpy array encoding a batch of predictions.
    top: Integer, how many top-guesses to return. Defaults to 5.

    Returns:
    A list of lists of top class prediction tuples
    `(class_name, class_description, score)`.
    One list of tuples per sample in batch input.

    Raises:
    ValueError: In case of invalid shape of the `pred` array
        (must be 2D).
    """

    if len(preds.shape) != 2 or preds.shape[1] != 1000:
        raise ValueError('`decode_predictions` expects '
                            'a batch of predictions '
                            '(i.e. a 2D array of shape (samples, 1000)). '
                            'Found array with shape: ' + str(preds.shape))
    results = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        result = [tuple(imagenet_json[str(i)]) + (pred[i],) for i in top_indices]
        result.sort(key=lambda x: x[2], reverse=True)
        results.append(result)

    return results
