"""Module containing the dispatcher for callbacks"""

from pytorch_trainer.callbacks.base_callback import Callback


class CallbackDispatcher:
    """Dispatcher class for propagating the call to all callbacks"""
    def __init__(self, callbacks: list[Callback], trainer):
        self.callbacks = callbacks
        for callback in self.callbacks:
            callback.set_trainer(trainer)

    def dispatch_on_train_begin(self) -> None:
        for callback in self.callbacks:
            callback.on_train_begin()

    def dispatch_on_train_end(self) -> None:
        for callback in self.callbacks:
            callback.on_train_end()

    def dispatch_on_epoch_begin(self, current_epoch) -> None:
        for callback in self.callbacks:
            callback.on_epoch_begin(current_epoch)

    def dispatch_on_epoch_end(self, current_epoch) -> None:
        for callback in self.callbacks:
            callback.on_epoch_end(current_epoch)

    def dispatch_on_train_loop_begin(self) -> None:
        for callback in self.callbacks:
            callback.on_train_loop_begin()

    def dispatch_on_train_loop_end(self) -> None:
        for callback in self.callbacks:
            callback.on_train_loop_end()

    def dispatch_on_test_loop_begin(self) -> None:
        for callback in self.callbacks:
            callback.on_test_loop_begin()

    def dispatch_on_test_loop_end(self) -> None:
        for callback in self.callbacks:
            callback.on_test_loop_end()
