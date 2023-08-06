# isegeval

This is a library to evaluate click-based interactive segmentation models. isegeval could evaluate
the number of click (NoC) performance of the given model on the given dataset.


## Usage

You could evaluate your model as follows. See [notebooks](./notebooks) for more detail.

```py
from isegeval import evaluate
from isegeval.core import ModelFactory


# Each item is the tuple of an image and its correspoinding ground truth mask.
dataset: Sequence[tuple[np.ndarray, np.ndarray]] = YourDataset()

# A factory of your model that you want to evaluate. The factory should implement get_model method.
model_factory: ModelFactory = YourModelFactory()

evaluate(dataset, model_factory)
```


## Installation

```bash
pip install isegeval
```
