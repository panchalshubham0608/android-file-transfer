from PyQt6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton,
    QWidget, QLabel, QHBoxLayout, QHeaderView
)
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import os

from adb_utils import list_files, push_file


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Android File Browser")
        self.resize(800, 600)

        # Set base and current path
        self.base_path = "/storage/emulated/0"
        self.current_path = self.base_path
        self.show_hidden = False
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

        # Toggle button
        self.toggle_hidden_button = QPushButton("Show Hidden")
        self.toggle_hidden_button.setCheckable(True)
        self.toggle_hidden_button.toggled.connect(self.toggle_hidden_files)

        # Navigation UI
        self.back_button = QPushButton("◀")
        self.back_button.clicked.connect(self.go_back)

        label_text = self.current_path if self.current_path == self.base_path else os.path.basename(self.current_path)
        self.path_label = QLabel(label_text)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.path_label)
        nav_layout.addWidget(self.toggle_hidden_button)
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
        visible_files = [f for f in files if self.show_hidden or not f.name.startswith(".")]
        self.table.setRowCount(len(visible_files))

        for row, entry in enumerate(visible_files):
            self.table.setItem(row, 0, QTableWidgetItem(("📁 " if entry.is_dir else "📄 ") + entry.name))
            try:
                size_bytes = int(entry.size)
                size_str = human_readable_size(size_bytes)
            except ValueError:
                size_str = entry.size  # fallback if parsing fails
            self.table.setItem(row, 1, QTableWidgetItem(size_str))
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
    
    def toggle_hidden_files(self, checked: bool):
        self.show_hidden = checked
        self.toggle_hidden_button.setText("Hide Hidden" if checked else "Show Hidden")
        self.load_files()

def human_readable_size(size_bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"
