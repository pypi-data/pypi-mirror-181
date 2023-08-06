from pytorch_trainer.callbacks.base_callback import Callback


class CallbackDispatcher:
    def __init__(self, callbacks: list[Callback], trainer):
        self.callbacks = callbacks
        for callback in self.callbacks:
            callback.set_trainer(trainer)

    def on_train_begin(self):
        for callback in self.callbacks:
            callback.on_train_begin()

    def on_train_end(self):
        for callback in self.callbacks:
            callback.on_train_end()

    def on_epoch_begin(self, current_epoch):
        for callback in self.callbacks:
            callback.on_epoch_begin(current_epoch)

    def on_epoch_end(self, current_epoch):
        for callback in self.callbacks:
            callback.on_epoch_end(current_epoch)

    def on_train_loop_begin(self):
        for callback in self.callbacks:
            callback.on_train_loop_begin()

    def on_train_loop_end(self):
        for callback in self.callbacks:
            callback.on_train_loop_end()

    def on_test_loop_begin(self):
        for callback in self.callbacks:
            callback.on_test_loop_begin()

    def on_test_loop_end(self):
        for callback in self.callbacks:
            callback.on_test_loop_end()
