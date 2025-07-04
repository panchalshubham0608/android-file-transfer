from PyQt6.QtWidgets import QMessageBox, QWidget, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer


def show_no_device_dialog(parent: QWidget) -> bool:
    box = QMessageBox(parent)
    box.setWindowTitle("No Device Found")
    box.setText("No Android device is connected.\nPlease connect a device and try again.")

    pixmap = QPixmap("assets/device-error.png")
    if not pixmap.isNull():
        box.setIconPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
    else:
        box.setIcon(QMessageBox.Icon.Critical)

    box.setStandardButtons(QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel)
    result = box.exec()
    if result == QMessageBox.StandardButton.Cancel:
        QTimer.singleShot(  # type: ignore
            0, QApplication.quit
        )  # Ensure event loop starts, then quit
        return False

    return True
