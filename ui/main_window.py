from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from adb_utils import list_files, pull_file, push_file, AdbFileEntry
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Android File Browser")
        self.resize(800, 600)

        self.current_path = "/storage/self/primary/"
        self.history = []

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Size", "Modified"])
        self.table.cellDoubleClicked.connect(self.navigate)

        self.table.setAcceptDrops(True)
        self.table.viewport().setAcceptDrops(True)
        self.setAcceptDrops(True)

        back_button = QPushButton("⬅️ Back")
        back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(back_button)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_files()

    def load_files(self):
        self.setWindowTitle(f"Android File Browser - {self.current_path}")
        files = list_files(self.current_path)
        print(f"Loaded {len(files)} entries from: {self.current_path}")
        self.table.setRowCount(len(files))
        for row, entry in enumerate(files):
            self.table.setItem(row, 0, QTableWidgetItem(("📁 " if entry.is_dir else "📄 ") + entry.name))
            self.table.setItem(row, 1, QTableWidgetItem(entry.size))
            self.table.setItem(row, 2, QTableWidgetItem(entry.modified))

    def navigate(self, row, _):
        item = self.table.item(row, 0)
        if item and item.text().startswith("📁"):
            folder_name = item.text()[2:].strip()
            self.history.append(self.current_path)
            self.current_path = os.path.join(self.current_path, folder_name)
            self.load_files()

    def go_back(self):
        if self.history:
            self.current_path = self.history.pop()
            self.load_files()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            local_file = url.toLocalFile()
            if os.path.isfile(local_file):
                push_file(local_file, self.current_path)
        self.load_files()

    def start_drag(self, row):
        file_name = self.table.item(row, 0).text()[2:].strip()
        android_file_path = os.path.join(self.current_path, file_name)

        # Pull to temp
        temp_path = os.path.join("/tmp", file_name)
        pull_file(android_file_path, temp_path)

        mime = QMimeData()
        mime.setUrls([QtCore.QUrl.fromLocalFile(temp_path)])
        drag = QtGui.QDrag(self)
        drag.setMimeData(mime)
        drag.exec()
