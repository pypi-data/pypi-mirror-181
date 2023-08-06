from abc import ABC


class Metric(ABC):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def update_state(self, y_true, y_predict):
        raise NotImplementedError

    def result(self):
        raise NotImplementedError

    def reset_state(self):
        raise NotImplementedError
