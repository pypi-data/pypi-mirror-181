"""Module containing implementation for some common callbacks"""

import datetime
import io
from pathlib import Path

import torch
from torch.utils.tensorboard import SummaryWriter

from pytorch_trainer.callbacks.base_callback import Callback


class ModelCheckpointer(Callback):
    """
    Class implementing a checkpointer, which will save the:
    - current epoch
    - current model state dict
    - current optimizer state dict
    every x epochs
    """
    def __init__(self, checkpoint_frequency: int = 1, checkpoint_dir: str = "./checkpoints"):
        """
        :param checkpoint_frequency: Save model every checkpoint_frequency epochs
        :param checkpoint_dir: Directory to save the model to. Will be created if not already there
        """
        super().__init__()
        self.checkpoint_frequency = checkpoint_frequency
        self.checkpoint_dir = Path(checkpoint_dir).absolute() / str(datetime.datetime.now())
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def on_epoch_end(self, current_epoch):
        if current_epoch % self.checkpoint_frequency == 0:
            torch.save({
                "epoch": current_epoch,
                "model_state_dict": self.trainer.model.state_dict(),
                "optimizer_state_dict": self.trainer.optimizer.state_dict(),
            }, self.checkpoint_dir / f"post_epoch_{current_epoch}.pth")


class EarlyStopping(Callback):  # pylint: disable=R0902
    """Class implementing early stopping, a common method to prevent overfitting"""
    MIN_METRICS = ["loss"]
    MAX_METRICS = ["accuracy", "binary_accuracy"]

    # pylint: disable-next=R0913
    def __init__(self, monitor: str = "test_loss", min_delta: float = 0, patience: int = 0, mode: str = "auto",
                 restore_weights: bool = False, verbose: int = 0):
        """
        :param monitor: The metric which is monitored. This is given through the loop: {train, test}
        and the name of the metric
        :param min_delta: Minimum difference needed to be considered an improvement
        :param patience: If the patience reaches 0 the trainer will stop training
        :param mode: {auto, min, max}. Determines if a smaller metric is better or a higher one {loss vs acc}
        :param restore_weights: Restores the weights of the model to the best epoch if True
        :param verbose: Print statements to stdout
        """
        super().__init__()
        self.prefix, self.metric = monitor.split("_", 1)
        self.min_delta = min_delta
        self.patience = patience
        self.mode = mode
        self.restore_weights = restore_weights
        self.verbose = verbose

        self.current_patience = patience
        self.comparison_method = None
        self.current_best_metric = None

        self.buffer = None

        if self.mode == "auto":
            self._infer_mode()
        self._init_mode()

    def _infer_mode(self):
        if self.metric in EarlyStopping.MIN_METRICS:
            self.mode = "min"
        elif self.metric in EarlyStopping.MAX_METRICS:
            self.mode = "max"
        else:
            raise RuntimeError(f"Mode could not be inferred for {self.metric}")

    def _init_mode(self):
        if self.mode == "min":
            self.current_best_metric = float("inf")
            self.comparison_method = self._min_comparison
        elif self.mode == "max":
            self.current_best_metric = float("-inf")
            self.comparison_method = self._max_comparison
        else:
            raise RuntimeError(f"Mode: {self.mode} not valid")

    def _min_comparison(self, current):
        return (current - self.current_best_metric) <= -self.min_delta

    def _max_comparison(self, current):
        return (current - self.current_best_metric) >= self.min_delta

    def on_epoch_end(self, current_epoch):
        current_metric = self.trainer.history.get(self.metric).get(self.prefix)[-1]
        if self.comparison_method(current_metric):
            self._model_improvement(current_metric)
        else:
            self._model_stagnation()

    def _model_improvement(self, current_metric):
        self.current_best_metric = current_metric
        self.current_patience = self.patience
        if self.restore_weights:
            self._save_model_state()

    def _model_stagnation(self):
        self.current_patience -= 1
        self._check_patience_reached()

    def _check_patience_reached(self):
        if self.current_patience <= 0:
            self.trainer.stop_training = True
            if self.verbose:
                print("Stopping training because patience reached 0")
            if self.restore_weights:
                self._restore_model_state()

    def _restore_model_state(self):
        self.buffer.seek(0)
        self.trainer.model.load_state_dict(torch.load(self.buffer))

    def _save_model_state(self):
        self.buffer = io.BytesIO()
        torch.save(self.trainer.model.state_dict(), self.buffer)


class TensorBoard(Callback):
    """Class to create a tensorboard logfile for the current run"""
    def __init__(self, logdir: str = "./runs"):
        """
        :param logdir: Directory to save the log to
        """
        super().__init__()
        self.logdir = logdir

        self.writer = SummaryWriter()

    def on_epoch_end(self, current_epoch):
        for metric, train_test_dict in self.trainer.history.items():
            self.writer.add_scalar(f"{metric}/train", train_test_dict.get("train")[-1], current_epoch)
            self.writer.add_scalar(f"{metric}/test", train_test_dict.get("test")[-1], current_epoch)

    def on_train_begin(self):
        X, _ = next(iter(self.trainer.train_dataloader))  # Get sample input so graph of model can be calculated
        self.writer.add_graph(self.trainer.model, X.to(self.trainer.device))
