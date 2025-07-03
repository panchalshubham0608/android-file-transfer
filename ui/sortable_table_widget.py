from PyQt6.QtWidgets import QTableWidgetItem
from typing import Any

class SortableTableWidgetItem(QTableWidgetItem):
    def __init__(self, text: str, sort_value: Any):
        super().__init__(text)
        self.sort_value: Any = sort_value

    def __lt__(self, other: QTableWidgetItem) -> bool:
        if isinstance(other, SortableTableWidgetItem):
            return self.sort_value < other.sort_value
        return super().__lt__(other)
