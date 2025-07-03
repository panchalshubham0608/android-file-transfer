from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class LoadingDialog(QDialog):
    def __init__(self, message: str = "Processing..."):
        super().__init__()
        self.setWindowTitle("")
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()
        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #333;
                padding: 10px;
            }
        """)        
        layout.addWidget(label)
        self.setLayout(layout)
        self.setFixedSize(300, 150)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
        """)

