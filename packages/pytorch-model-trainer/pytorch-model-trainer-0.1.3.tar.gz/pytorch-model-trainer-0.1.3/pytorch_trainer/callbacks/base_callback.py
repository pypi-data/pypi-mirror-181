"""Module containing a basic interface the user can implement for additional functionality"""

from abc import ABC


class Callback(ABC):
    """Interface for callbacks"""
    def __init__(self):
        self.trainer = None

    def set_trainer(self, trainer):
        self.trainer = trainer

    def on_train_begin(self) -> None:
        """
        Called as first method after the train method of the trainer is called.
        :return:
        """

    def on_train_end(self) -> None:
        """
        Called as the last method before the train method of the trainer returns.
        :return:
        """

    def on_epoch_begin(self, current_epoch) -> None:
        """
        Called as first method in the current epoch.
        :param current_epoch:
        :return:
        """

    def on_epoch_end(self, current_epoch) -> None:
        """
        Called as last method in the current epoch.
        :param current_epoch:
        :return:
        """

    def on_train_loop_begin(self) -> None:
        """Called as first method when the train_loop method is called"""

    def on_train_loop_end(self) -> None:
        """Called as last method before the train_loop method returns"""

    def on_test_loop_begin(self) -> None:
        """Called as first method when the test_loop method is called"""

    def on_test_loop_end(self) -> None:
        """Called as last method before the test_loop method returns"""
