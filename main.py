from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
import sys
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set global app icon
    icon_path = os.path.join(os.path.dirname(__file__), "assets/icon.png")
    app.setWindowIcon(QIcon(icon_path))

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
