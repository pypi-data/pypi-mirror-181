"""Module containing a basic interface the user can implement for additional metrics"""

from abc import ABC

import torch


class Metric(ABC):
    """Interface for metrics"""
    def __init__(self, name: str):
        """
        :param name: Name used in the history dict of the trainer
        """
        self.name = name

    def __str__(self):
        return self.name

    def update_state(self, y_true: torch.Tensor, y_predict: torch.Tensor) -> None:
        """
        Called when the model finishes processing a batch. Should then calculate some metric based on the output of
        this batch.
        :param y_true: Ground truth as given in the dataset
        :param y_predict: Output of the model in training
        :return:
        """
        raise NotImplementedError

    def result(self) -> float:
        """
        Calculate the metric which is stored in the history.
        :return: The calculated metric for the epoch
        """
        raise NotImplementedError

    def reset_state(self) -> None:
        """
        Reset the state to default if necessary, so it can be used in the next epoch.
        :return:
        """
        raise NotImplementedError
