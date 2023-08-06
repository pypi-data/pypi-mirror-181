class Callback:
    def __init__(self):
        self.trainer = None

    def set_trainer(self, trainer):
        self.trainer = trainer

    def on_train_begin(self):
        pass

    def on_train_end(self):
        pass

    def on_epoch_begin(self, current_epoch):
        pass

    def on_epoch_end(self, current_epoch):
        pass

    def on_train_loop_begin(self):
        pass

    def on_train_loop_end(self):
        pass

    def on_test_loop_begin(self):
        pass

    def on_test_loop_end(self):
        pass
