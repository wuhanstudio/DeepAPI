### Full APIs

#### Post URLs:

| Model        | Dataset  | Post URL                            |
| ------------ | -------- | ----------------------------------- |
| VGG-16       | Cifar10  | http://127.0.0.1:8080/vgg16_cifar10 |
| VGG-16       | ImageNet | http://127.0.0.1:8080/vgg16         |
| Resnet-50    | ImageNet | http://127.0.0.1:8080/resnet50      |
| Inception v3 | ImageNet | http://127.0.0.1:8080/inceptionv3   |

#### Post Data (JSON):

```
{
  "file": ""
}
```

#### Query Parameters:

| Name    | Type    | Default | Value                                                        |
| ------- | ------- | ------- | ------------------------------------------------------------ |
| top     | integer | 10      | One of [1, 3, 5, 10], top=5 returns top 5 predictions.       |
| no-prob | integer | 0       | no-prob=1 returns labels without probabilities. no-prob=0 returns labels and probabilities. |

Example post urls (returns top 10 predictions with probabilities):

```
http://127.0.0.1:8080/vgg16?top=10&no-prob=0
```

#### Returns (JSON):

| Key         | Value                                                        |
| ----------- | ------------------------------------------------------------ |
| success     | True / False                                                 |
| Predictions | Array of prediction results, each element contains {"labels": "cat", "probability": 0.99} |
| error       | The error message if any                                     |

Example returned json:

```
{
  "success": true,
  "predictions": [
    {
      "label": "cat",
      "probability": 0.9996376037597656
    },
    {
      "label": "dog",
      "probability": 0.0002855948405340314
    },
    {
      "label": "deer",
      "probability": 0.000021985460989526473
    },
    {
      "label": "bird",
      "probability": 0.000021391952031990513
    },
    {
      "label": "horse",
      "probability": 0.000013297495570441242
    },
    {
      "label": "airplane",
      "probability": 0.000006046993803465739
    },
    {
      "label": "ship",
      "probability": 0.0000044226785576029215
    },
    {
      "label": "frog",
      "probability": 0.0000036349929359857924
    },
    {
      "label": "truck",
      "probability": 0.0000035354278224986047
    },
    {
      "label": "automobile",
      "probability": 0.000002384880417594104
    }
  ],
}
```
