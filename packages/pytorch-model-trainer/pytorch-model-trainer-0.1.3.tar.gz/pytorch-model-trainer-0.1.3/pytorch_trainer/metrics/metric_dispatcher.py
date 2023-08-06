"""Module containing the dispatcher for metrics"""

from pytorch_trainer.metrics.base_metric import Metric


class MetricDispatcher:
    """Dispatcher class for propagating the call to all metrics"""
    def __init__(self, metrics: list[Metric], history_dict):
        self.metrics = metrics
        self.history_dict = history_dict

    def dispatch_update_state(self, y_true, y_predict) -> None:
        for metric in self.metrics:
            metric.update_state(y_true, y_predict)

    def dispatch_update_history(self, origin_loop) -> None:
        for metric in self.metrics:
            self.history_dict[f"{metric}"][f"{origin_loop}"].append(metric.result())

    def dispatch_reset_state(self) -> None:
        for metric in self.metrics:
            metric.reset_state()
