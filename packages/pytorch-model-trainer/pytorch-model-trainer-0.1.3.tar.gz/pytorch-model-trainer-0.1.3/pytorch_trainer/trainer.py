"""Module containing the Trainer class"""

from collections import defaultdict

import torch
from torch import nn

from pytorch_trainer.metrics.metric_dispatcher import MetricDispatcher
from pytorch_trainer.metrics.base_metric import Metric
from pytorch_trainer.callbacks.callback_dispatcher import CallbackDispatcher
from pytorch_trainer.callbacks.base_callback import Callback


class Trainer:  # pylint: disable=R0902
    """Class implementing the train and test loop of the trainer"""

    # pylint: disable-next=R0913
    def __init__(self, model: nn.Module, loss_fn, optimizer, train_dataloader, test_dataloader,
                 device: str = "cuda" if torch.cuda.is_available() else "cpu",
                 metrics: list[Metric] = (), callbacks: list[Callback] = ()):
        """
        :param model: nn.Module to be trained
        :param loss_fn: Loss function used with the model
        :param optimizer: Optimizer used with the model
        :param train_dataloader: Dataloader used during the train loop
        :param test_dataloader: Dataloader used during the test loop
        :param device: Device to be used for model and data
        :param metrics: List of metric objects used to monitor model performance
        :param callbacks: List of callback objects used to implement additional functionality
        """
        self.model = model
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.train_dataloader = train_dataloader
        self.test_dataloader = test_dataloader
        self.device = device

        self.history = defaultdict(lambda: defaultdict(list))

        self.metrics_dispatcher = MetricDispatcher(metrics, self.history)
        self.callback_dispatcher = CallbackDispatcher(callbacks, self)

        self.stop_training = False

    def train(self, epochs) -> None:
        """
        Start training the model.
        Calls the on_train_begin and on_train_end method of the callbacks.
        :param epochs: Number of times the train and test loop will be called
        :return:
        """

        self.callback_dispatcher.dispatch_on_train_begin()
        for i in range(epochs):
            print(f"Training Epoch {i}")
            self.callback_dispatcher.dispatch_on_epoch_begin(i)

            self.train_loop()
            self.metrics_dispatcher.dispatch_reset_state()

            self.test_loop()
            self.metrics_dispatcher.dispatch_reset_state()

            self.callback_dispatcher.dispatch_on_epoch_end(i)

            if self.stop_training:
                break
        self.callback_dispatcher.dispatch_on_train_end()

    def train_loop(self) -> None:
        """
        Sets model to train modus and trains for 1 epoch. Calculates the train metrics.
        Calls the on_train_loop_begin and on_train_loop_end method of the callbacks.
        :return:
        """
        self.callback_dispatcher.dispatch_on_train_loop_begin()
        self.model.train()
        accumulated_loss = 0
        for X, y in self.train_dataloader:
            X, y = X.to(self.device), y.to(self.device)
            pred = self.model(X)
            loss = self.loss_fn(pred, y)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            self.metrics_dispatcher.dispatch_update_state(y, pred)
            accumulated_loss += loss.item()
        self.metrics_dispatcher.dispatch_update_history("train")
        self.history["loss"]["train"].append(accumulated_loss / len(self.train_dataloader))
        self.callback_dispatcher.dispatch_on_train_loop_end()

    def test_loop(self) -> None:
        """
        Sets model to eval modus and tests for 1 epoch. Calculates the test metrics.
        Calls the on_test_loop_begin and on_test_loop_end method of the callbacks.
        :return:
        """
        self.callback_dispatcher.dispatch_on_test_loop_begin()
        self.model.eval()
        accumulated_loss = 0
        with torch.no_grad():
            for X, y in self.test_dataloader:
                X, y = X.to(self.device), y.to(self.device)
                pred = self.model(X)
                loss = self.loss_fn(pred, y)

                self.metrics_dispatcher.dispatch_update_state(y, pred)
                accumulated_loss += loss.item()
        self.metrics_dispatcher.dispatch_update_history("test")
        self.history["loss"]["test"].append(accumulated_loss / len(self.test_dataloader))
        self.callback_dispatcher.dispatch_on_test_loop_end()
