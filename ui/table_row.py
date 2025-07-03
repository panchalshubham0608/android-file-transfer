from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt
from utils.adb_utils import AdbFileEntry
from utils.size_utils import human_readable_size
from typing import List
from ui.sortable_table_widget import SortableTableWidgetItem

def build_file_table_row(entry: AdbFileEntry) -> List[QTableWidgetItem]:
    name = QTableWidgetItem(("📁 " if entry.is_dir else "📄 ") + entry.name)
    modified = QTableWidgetItem(entry.modified)
    try:
        size_bytes = int(entry.size)
        size_str = human_readable_size(size_bytes)
        size_item = SortableTableWidgetItem(size_str, size_bytes)
    except ValueError:
        size_str = entry.size  # fallback if parsing fails
        size_item = QTableWidgetItem(entry.size)


    name.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    size_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    modified.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

    return [name, size_item, modified]
