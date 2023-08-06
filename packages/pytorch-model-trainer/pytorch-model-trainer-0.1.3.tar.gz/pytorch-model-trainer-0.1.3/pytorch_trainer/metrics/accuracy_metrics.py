"""Module containing implementation for some common metrics"""

from abc import ABC

import torch

from pytorch_trainer.metrics.base_metric import Metric


class _AccuracyMetric(Metric, ABC):
    """Class implementing common functionality for accuracy metrics"""
    def __init__(self, name):
        super().__init__(name)
        self.positives = 0
        self.total = 0

    def result(self):
        return self.positives / self.total

    def reset_state(self):
        self.positives = 0
        self.total = 0


class Accuracy(_AccuracyMetric):
    """Class implementing the accuracy metric for multi class classification tasks"""
    def __init__(self, name="accuracy"):
        super().__init__(name)

    def update_state(self, y_true: torch.Tensor, y_predict: torch.Tensor):
        self.positives += (y_true == y_predict.argmax(1)).type(torch.int).sum().item()
        self.total += len(y_true)


class BinaryAccuracy(_AccuracyMetric):
    """Class implementing the accuracy metric for binary classification tasks"""
    def __init__(self, name="binary_accuracy", threshold: float = 0.5):
        """
        :param threshold: Threshold for considering a prediction to be of class 1
        """
        super().__init__(name)
        self.threshold = threshold

    def update_state(self, y_true, y_predict):
        y_predict = y_predict.reshape(1, -1)
        self.positives += (torch.where(y_predict >= self.threshold, 1, 0) == y_true).type(torch.int).sum().item()
        self.total += len(y_true)
