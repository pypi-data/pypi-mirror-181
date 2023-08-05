# visplotlib

[![flake8 Actions Status](https://github.com/VisiumCH/visplotlib/actions/workflows/lint.yml/badge.svg)](https://github.com/VisiumCH/visplotlib/actions) [![PyPI version](https://badge.fury.io/py/visplotlib.svg)](https://badge.fury.io/py/visplotlib)

Standardized plot styling for Visium SA

## Installation

To plot with **visplotlib**, you need to install the library into your environment:

```bash
pip install visplotlib
```

You can then use the following import statements:

```python
import visplotlib as vpl
from visplotlib.pyplot import mpl, plt  # <-- Wrapped Matplotlib and Pyplot
from visplotlib.seaborn import sns  # <-- Wrapped Seaborn
```

## Example

We want to make your plots beautiful. We don't want to change your coding practices with long and annoying procedures.

All you need to do is call `plt.format()` when making a plot. That's it.

```python
fig, ax = plt.subplots()

iris = sns.load_dataset('iris')

sns.scatterplot(data=iris, x='sepal_length', y='petal_length', ax=ax)
ax.set_title('Sepal vs. Petal length')

plt.format()  # All we need to do is call plt.format()!
plt.show()
```

## Loom demonstration



https://user-images.githubusercontent.com/32436482/124758979-6c65cd00-df2f-11eb-8b3e-fc156d441913.mp4

