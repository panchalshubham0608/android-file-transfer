from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent


class LoadingDialog(QDialog):
    def __init__(self, message: str = "Processing...", parent: QWidget = None) -> None:  # type: ignore
        super().__init__()
        self.setWindowTitle("")
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        if parent:
            parent.setEnabled(False)  # Disable the main window

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                color: #333;
                padding: 10px;
            }
        """
        )
        layout.addWidget(label)
        self.setLayout(layout)
        self.setFixedSize(300, 150)
        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
        """
        )

    def closeEvent(self, event: QCloseEvent) -> None:  # type: ignore
        # Re-enable parent when dialog closes
        if self.parent():
            self.parent().setEnabled(True)  # type: ignore
        super().closeEvent(event)
