from PyQt6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton,
    QWidget, QLabel, QHBoxLayout, QHeaderView
)
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import os

from adb_utils import list_files, pull_file, push_file, AdbFileEntry


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Android File Browser")
        self.resize(800, 600)

        # Set base and current path
        self.base_path = "/storage/emulated/0"
        self.current_path = self.base_path
        self.history = []

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Size", "Modified"])
        self.table.cellDoubleClicked.connect(self.navigate)
        self.table.setAcceptDrops(True)
        self.table.viewport().setAcceptDrops(True)
        self.setAcceptDrops(True)

        # Resize columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        # Navigation UI
        self.back_button = QPushButton("◀")
        self.back_button.clicked.connect(self.go_back)

        label_text = self.current_path if self.current_path == self.base_path else os.path.basename(self.current_path)
        self.path_label = QLabel(label_text)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.path_label)
        nav_layout.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(nav_layout)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_files()

    def load_files(self):
        label_text = self.current_path if self.current_path == self.base_path else os.path.basename(self.current_path)
        self.path_label.setText(label_text)

        files = list_files(self.current_path)
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
