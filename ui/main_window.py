from PyQt6.QtWidgets import (
    QMainWindow,
    QTableWidget,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QHBoxLayout,
    QHeaderView
)
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon
from PyQt6.QtCore import QSize, QPoint, Qt
from utils.adb_utils import list_files, push_file, is_device_connected
import os
from typing import List
from ui.table_row import build_file_table_row
from ui.context_menu import show_context_menu
from ui.dialog_utils import show_no_device_dialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Android File Browser")
        self.resize(800, 600)
        self.headers: List[str] = ["Name", "Size", "Modified"]

        # Set base and current path
        self.base_path = "/storage/emulated/0"
        self.current_path: str = self.base_path
        self.show_hidden = False
        self.history: List[str] = []

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(self.headers)  # type: ignore
        self.table.cellDoubleClicked.connect(self.navigate)  # type: ignore
        self.table.setSortingEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.viewport().setAcceptDrops(True)  # type: ignore
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handle_context_menu) # type: ignore
        self.setAcceptDrops(True)

        # Resize columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # type: ignore
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # type: ignore
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # type: ignore

        # Toggle button
        self.toggle_hidden_button = QPushButton("Show Hidden")
        self.toggle_hidden_button.setCheckable(True)
        self.toggle_hidden_button.toggled.connect(self.toggle_hidden_files)  # type: ignore

        # Navigation UI
        self.back_button = QPushButton()
        back_button_icon_path = os.path.join(
            os.path.dirname(__file__), "../assets/chevron-left.png"
        )
        self.back_button.setIcon(QIcon(back_button_icon_path))
        self.back_button.setIconSize(QSize(16, 16))
        self.back_button.setFlat(True)
        self.back_button.setStyleSheet("background: transparent; border: none;")
        self.back_button.clicked.connect(self.go_back)  # type: ignore

        label_text: str = (
            self.current_path
            if self.current_path == self.base_path
            else os.path.basename(self.current_path)
        )
        self.path_label = QLabel(label_text)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.path_label)
        nav_layout.addStretch()
        nav_layout.addWidget(self.toggle_hidden_button)

        layout = QVBoxLayout()
        layout.addLayout(nav_layout)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_files()

    def ensure_device_connected(self) -> bool:
        while not is_device_connected():
            if not show_no_device_dialog(self):
                return False

        return True

    def load_files(self):
        if not self.ensure_device_connected():
            return  # Prevent loading files if no device is connected

        label_text = (
            self.current_path
            if self.current_path == self.base_path
            else os.path.basename(self.current_path)
        )
        self.path_label.setText(label_text)
        self.back_button.setEnabled(bool(self.history))

        files = list_files(self.current_path)
        visible_files = [
            f for f in files if self.show_hidden or not f.name.startswith(".")
        ]
        self.table.setRowCount(len(visible_files))

        for row, entry in enumerate(visible_files):
            items = build_file_table_row(entry)
            for col, item in enumerate(items):
                self.table.setItem(row, col, item)

    def navigate(self, row: int, _: int) -> None:
        item = self.table.item(row, 0)
        if item and item.text().startswith("📁"):
            folder_name = item.text()[2:].strip()
            self.history.append(self.current_path)
            self.current_path = os.path.join(self.current_path, folder_name)
            self.load_files()

    def go_back(self) -> None:
        if self.history:
            self.current_path = self.history.pop()
            self.load_files()

    def dragEnterEvent(self, event: QDragEnterEvent):  # type: ignore
        if event.mimeData().hasUrls():  # type: ignore
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):  # type: ignore
        for url in event.mimeData().urls():  # type: ignore
            local_file = url.toLocalFile()
            if os.path.isfile(local_file):
                push_file(local_file, self.current_path)
        self.load_files()

    def toggle_hidden_files(self, checked: bool) -> None:
        self.show_hidden = checked
        self.toggle_hidden_button.setText("Hide Hidden" if checked else "Show Hidden")
        self.load_files()

    def handle_context_menu(self, _: QPoint):
        show_context_menu(
            parent=self,
            table_widget=self.table,
            current_path=self.current_path,
            reload_callback=self.load_files,
        )
