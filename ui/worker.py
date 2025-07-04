from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
from typing import Callable


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)


class BackgroundTask(QRunnable):
    def __init__(self, task: Callable[[], None]):
        super().__init__()
        self.signals = WorkerSignals()
        self.task = task

    def run(self) -> None:
        try:
            self.task()
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()
