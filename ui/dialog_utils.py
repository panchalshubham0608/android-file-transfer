from PyQt6.QtWidgets import QMessageBox, QWidget, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer


def show_no_device_dialog(parent: QWidget) -> bool:
    box = QMessageBox(parent)
    box.setWindowTitle("No Device Found")
    box.setText(
        "No Android device is connected.\nPlease connect a device and try again."
    )

    pixmap = QPixmap("assets/device-error.png")
    if not pixmap.isNull():
        box.setIconPixmap(
            pixmap.scaled(
                64,
                64,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
    else:
        box.setIcon(QMessageBox.Icon.Critical)

    box.setStandardButtons(
        QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel
    )
    result = box.exec()
    if result == QMessageBox.StandardButton.Cancel:
        QTimer.singleShot(  # type: ignore
            0, QApplication.quit
        )  # Ensure event loop starts, then quit
        return False

    return True


def show_delete_confirmation(parent: QWidget, file_count: int) -> bool:
    box = QMessageBox(parent)
    box.setWindowTitle("Delete Confirmation")
    box.setText(f"Are you sure you want to delete {file_count} file(s)?")
    box.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    box.setDefaultButton(QMessageBox.StandardButton.No)

    pixmap = QPixmap("assets/delete_warning.png")
    if not pixmap.isNull():
        box.setIconPixmap(
            pixmap.scaled(
                48,
                48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
    else:
        box.setIcon(QMessageBox.Icon.Warning)

    reply = box.exec()
    return reply == QMessageBox.StandardButton.Yes


def show_usb_debugging_reminder(parent: QWidget) -> None:
    box = QMessageBox(parent)
    box.setWindowTitle("Security Tip")
    box.setText(
        "USB debugging is still enabled.\n\n"
        "If you're done using the app, consider turning off USB debugging "
        "from Developer Options to prevent unauthorized access."
    )

    pixmap = QPixmap("assets/usb_debug_warning.png")
    if not pixmap.isNull():
        box.setIconPixmap(
            pixmap.scaled(
                64,
                64,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
    else:
        box.setIcon(QMessageBox.Icon.Warning)

    box.setStandardButtons(QMessageBox.StandardButton.Ok)
    box.exec()
