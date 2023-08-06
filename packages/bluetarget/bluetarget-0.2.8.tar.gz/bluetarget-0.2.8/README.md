# BlueTarget

**Deploy, monitor and explain machine learning models.**

![Logo](https://deploy.bluetarget.ai/statics/bt.jpg)

BlueTarget is a MLops platform which allows ML engineer and Data Science deploy, monitor and explain their machine learning models. We're able to deploy your model using different kind of strategies like A/B testing, Canary or Rolling update.

Get started with the [BlueTarget](https://docs.deploy.bluetarget.ai).

## What can I do with BlueTarget?

If you've ever tried to get a model out of a Jupyter notebook, BlueTargert is for you.

BlueTarget allow your to deploy your ML model taking away the whole complexity of the cloud. However If you prefer to have the control of the infrastructure, BlueTarget can work with your preferred cloud:

Here are some of the things BlueTarget does:

- Turns your Python model into a microservice with a production-ready API endpoint, no need for Flask or Django.
- Track your model's version and metadata
- Understad the drift of your model
- Track your inference
- Deployment strategies like A/B testing, canary and rolling update

## Installation

BlueTarget requires Python >=3.7

To install from [PyPi](https://pypi.org/project/bluetarget/), run:

```
pip install bluetarget
```

BlueTarget is actively developed, and we recommend using the latest version. To update your BlueTarget installation, run:

```
pip install --upgrade bluetarget
```

## How to use BlueTarget

### Quickstart: making a BlueTarget

#### train.py

```python
!pip install --upgrade scikit-learn bluetarget pickle-mixin

from sklearn import svm
from sklearn import datasets

import pickle

# Load training data set
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Train the model
clf = svm.SVC(gamma='scale')
clf.fit(X, y)

pickle.dump(clf, open('model.pkl', 'wb'))

```

#### service.py

```python
import os
from typing import Dict, List

class Model:
    def __init__(self) -> None:
        self._model = None

    def load(self):
        import pickle

        with open(f"{os.path.dirname(__file__)}/model.pkl", 'rb') as pickle_file:
            self._model = pickle.load(pickle_file)

    def predict(self, request: Dict) -> Dict[str, List]:
        response = {}
        inputs = request["inputs"]
        result = self._model.predict(inputs).tolist()
        response["predictions"] = result

        return response
```

#### requirements.txt

```
scikit-learn==1.0.2
pickle-mixin==1.0.2
```

#### deploy.py

```python
from bluetarget import BlueTarget

bt = BlueTarget(api_key="YOUR_API_KEY")

bt.deploy(
    model_name="YourFirstModel",
    model_class="Model",
    model_files=["model.py", "model.pkl"],
    requirements_file="requirements.txt"
)

inputs = [
    [6.9, 3.1, 5.1, 2.3],
    [5.8, 2.7, 5.1, 1.9],
    [6.8, 3.2, 5.9, 2.3],
    [6.7, 3.3, 5.7, 2.5],
    [6.7, 3.,  5.2, 2.3],
    [6.3, 2.5, 5.,  1.9],
    [6.5, 3.,  5.2, 2.],
    [6.2, 3.4, 5.4, 2.3],
    [5.9, 3.,  5.1, 1.8]
]

bt.predict(inputs)

# {
#     "predictions": [
#         2,
#         1,
#         2,
#         3,
#         0,
#         2,
#         3,
#         2,
#         1
#     ]
# }

```
