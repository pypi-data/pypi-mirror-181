[![docs](https://img.shields.io/badge/-docs-success)](https://neuro-ml.github.io/amid/)
[![pypi](https://img.shields.io/pypi/v/amid?logo=pypi&label=PyPi)](https://pypi.org/project/amid/)
![License](https://img.shields.io/github/license/neuro-ml/amid)

Awesome Medical Imaging Datasets (AMID) - a curated list of medical imaging datasets with unified interfaces

# Getting started

Just import a dataset and start using it!

Note that for some datasets you must manually download the raw files first.

```python
from amid.verse import VerSe

ds = VerSe()
# get the available ids
print(len(ds.ids))
i = ds.ids[0]

# use the available methods:
#   load the image and vertebrae masks
x, y = ds.image(i), ds.masks(i)
print(ds.split(i), ds.patient(i))

# or get a namedTuple-like object:
entry = ds(i)
x, y = entry.image, entry.masks
print(entry.split, entry.patient)
```

Check out [our docs](https://neuro-ml.github.io/amid/) for a list of available datasets and their fields.

# Install

Just get it from PyPi:

```shell
pip install amid
```

Or if you want to use version control features:

```shell
git clone https://github.com/neuro-ml/amid.git
cd amid && pip install -e .
```
