"""This module contains metrics based on true/false positives/negatives"""
from abc import ABC

import torch

from pytorch_trainer.metrics.base_metric import Metric


class _ClassificationMetric(Metric, ABC):
    """Helper which provides functions for calculating tp, fp, fn"""

    def __init__(self, name: str):
        super().__init__(name)
        self.tps = 0
        self.fps = 0
        self.fns = 0

    def _tps(self, y_true: torch.Tensor, y_predict: torch.Tensor):
        self.tps += torch.where((y_true == 1) & (y_predict == 1), 1, 0).sum().item()

    def _fps(self, y_true: torch.Tensor, y_predict: torch.Tensor):
        self.fps += torch.where((y_true == 0) & (y_predict == 1), 1, 0).sum().item()

    def _fns(self, y_true: torch.Tensor, y_predict: torch.Tensor):
        self.fns += torch.where((y_true == 1) & (y_predict == 0), 1, 0).sum().item()

    def result(self) -> float:
        try:
            return self._result()
        except ZeroDivisionError:
            return 0

    def _result(self) -> float:
        """Overwrite with actual calculation of the result"""
        raise NotImplementedError

    def reset_state(self) -> None:
        self.tps = 0
        self.fps = 0
        self.fns = 0


class Precision(_ClassificationMetric):
    """Implementation of the precision metric (positive predictive value)"""

    def __init__(self, name: str = "precision"):
        super().__init__(name)

    def update_state(self, y_true: torch.Tensor, y_predict: torch.Tensor) -> None:
        self._tps(y_true, y_predict)
        self._fps(y_true, y_predict)

    def _result(self) -> float:
        return self.tps / (self.tps + self.fps)


class Recall(_ClassificationMetric):
    """Implementation of the recall metric (sensitivity)"""

    def __init__(self, name: str = "recall"):
        super().__init__(name)

    def update_state(self, y_true: torch.Tensor, y_predict: torch.Tensor) -> None:
        self._tps(y_true, y_predict)
        self._fns(y_true, y_predict)

    def _result(self) -> float:
        return self.tps / (self.tps + self.fns)


class FBetaScore(_ClassificationMetric):
    """Implementation of the F-Beta-Score"""

    def __init__(self, name: str = "f{}score", beta: int = 1):
        """
        :param beta: The value for beta where recall will be considered beta times as important as precision
        When beta is 1 this is the F1-Score
        """
        super().__init__(name.format(beta))
        self.beta = beta ** 2
        self.tps = 0
        self.fps = 0
        self.fns = 0

    def update_state(self, y_true: torch.Tensor, y_predict: torch.Tensor) -> None:
        self._tps(y_true, y_predict)
        self._fps(y_true, y_predict)
        self._fns(y_true, y_predict)

    def _result(self) -> float:
        return ((1 + self.beta) * self.tps) / ((1 + self.beta) * self.tps + self.beta * self.fns + self.fps)
