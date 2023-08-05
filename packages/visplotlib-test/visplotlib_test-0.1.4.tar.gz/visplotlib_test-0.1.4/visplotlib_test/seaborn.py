import seaborn as sns
import matplotlib

from typing import Callable
from functools import wraps


def _instantiate(
    f: Callable[..., matplotlib.axes.Axes]
) -> matplotlib.axes.Axes:
    """
    Instantiate function redefinition by wrapper.
    
    Args:
        f (Callable[..., matplotlib.axes.Axes]): Axes object to instantiate
    Returns:
        matplotlib.axes.Axes: instantiated Axes object
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        
        return f()(*args, **kwargs)
    
    return wrapper


def _confusion_matrix(
    f: Callable[..., matplotlib.axes.Axes]
) -> matplotlib.axes.Axes:
    """
    Instantiate Axes with defaults attributed to Confusion Matrix.
    
    Args:
        f (Callable[..., matplotlib.axes.Axes]): Axes object to instantiate
    Returns:
        matplotlib.axes.Axes: instantiated Axes object
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        
        ax = f()(*args, **kwargs)
        ax.set_xlabel('Prediction')
        ax.set_ylabel('Ground truth')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=45)
        
        return ax
    
    return wrapper


def _color_map(
    f: Callable
) -> Callable:
    """
    Wrapper that modifies default parameters `annot`, `cbar`, and `cmap`
    of Callable, if and only if they are not yet set.

    Args:
        f (Callable): Function with parameters `annot`, `cbar`, and `cmap`.

    Returns:
        Callable: Function with modified default parameters.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        
        overridden_args = dict(annot=True, cbar=False, cmap='Blues')
        overridden_args.update(kwargs)
        
        kwargs = overridden_args
        
        return f(*args, **kwargs)
    
    return wrapper


# Store seaborn function in temp
_temp_heatmap = sns.heatmap


# Redefine `seaborn.heatmap`
@_color_map
@_instantiate
def _visium_heatmap(*args, **kwargs):
    return _temp_heatmap


# Define `seaborn.confusion`
@_color_map
@_confusion_matrix
def _visium_confusion(*args, **kwargs):
    return _temp_heatmap


# Allocate functions to `seaborn` module
sns.heatmap = _visium_heatmap
sns.confusion = _visium_confusion
