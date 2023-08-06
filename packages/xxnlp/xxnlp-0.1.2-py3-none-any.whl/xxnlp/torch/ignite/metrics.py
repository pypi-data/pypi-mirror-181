from functools import partial
import warnings
import numpy as np

from ignite.metrics.metric import Metric, reinit__is_reduced
from ignite.metrics.loss import Loss
from sklearn.metrics import f1_score, recall_score, precision_score, roc_auc_score, accuracy_score
from typing import Callable, List, Tuple, Any
from xxnlp import Registry

__all__ = ['METRICS']

def default_preprocessing(output):
    "default: turn probability into class labels"
    y_pred, y  = output
    return np.round(y_pred) , y


class EpochMetric(Metric):

    def __init__(
        self, compute_fn: Callable, 
        output_transform: Callable = default_preprocessing,
        **kwargs
    ):
        super().__init__(output_transform)
        self.compute_fn = partial(compute_fn, **kwargs)
    
    @reinit__is_reduced
    def reset(self) -> None:
        self._predictions = []  # type: List[np.ndarray]
        self._targets = []      # type: List[np.ndarray]
    
    @reinit__is_reduced
    def update(self, output: Tuple[np.ndarray, np.ndarray]) -> None:
        y_pred, y = output
        if y_pred.ndim == 2 and y_pred.shape[1] == 1: 
            y_pred = y_pred.squeeze(axis=-1)
        if y.ndim == 2 and y.shape[1] == 1: 
            y = y.squeeze(axis=-1)
        self._predictions.append(y_pred.copy())
        self._targets.append(y.copy())
        # Check once the signature and execution of compute_fn
        if len(self._predictions) == 1:
            try:
                self.compute_fn(self._targets[0], self._predictions[0])
            except Exception as e:
                warnings.warn(f"Probably, there can be a problem with `compute_fn`:\n {e}.", UserWarning)
    
    def compute(self) -> Any:
        if len(self._predictions) < 1 or len(self._targets) < 1:
            raise RuntimeError("EpochMetric must have at least one example before it can be computed.")
        _prediction = np.concatenate(self._predictions)
        _target = np.concatenate(self._targets)
        result = self.compute_fn(_target, _prediction)
        return result


class AUC(EpochMetric):
    def __init__(self, **kwargs):
        super(AUC, self).__init__(
            compute_fn=roc_auc_score, output_transform=lambda x: x, **kwargs
        )

class F1(EpochMetric):
    def __init__(self, **kwargs):
        super(F1, self).__init__(compute_fn=f1_score, **kwargs)

class Recall(EpochMetric):
    def __init__(self, **kwargs):
        super(Recall, self).__init__(compute_fn=recall_score, **kwargs)

class Precision(EpochMetric):
    def __init__(self, **kwargs):
        super(Precision, self).__init__(compute_fn=precision_score, zero_division=0, **kwargs)

class Accuracy(EpochMetric):
    def __init__(self, **kwargs):
        super(Accuracy, self).__init__(compute_fn=accuracy_score, **kwargs)

METRICS = Registry('metric:torch')
for name, fn in {
    'f1': F1,
    'roc': AUC,
    'prec': Precision,
    'recall': Recall,
    'acc': Accuracy,
    'loss': Loss,
}.items():
    METRICS(fn=fn, name=name, engine='ignite')