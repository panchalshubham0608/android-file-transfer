from PyQt6.QtWidgets import (
    QMenu,
    QFileDialog,
    QTableWidget,
    QWidget,
)
import os
from typing import Callable, List
from utils.adb_utils import pull_files, delete_files_on_device
from PyQt6.QtGui import QAction, QCursor
from ui.loading_dialog import LoadingDialog
from PyQt6.QtWidgets import QApplication
from ui.worker import BackgroundTask
from PyQt6.QtCore import QThreadPool
from ui.dialog_utils import show_delete_confirmation

thread_pool = QThreadPool.globalInstance()


def show_context_menu(
    parent: QWidget,
    table_widget: QTableWidget,
    current_path: str,
    reload_callback: Callable[[], None],
) -> None:
    selected_items = table_widget.selectedItems()
    if not selected_items:
        return

    selected_rows: set[int] = set(item.row() for item in selected_items)
    entries: List[str] = []

    for row in selected_rows:
        name_item = table_widget.item(row, 0)
        if not name_item:
            continue
        name: str = name_item.text()[2:].strip()  # Remove 📁 or 📄
        full_path: str = os.path.join(current_path, name)
        entries.append(full_path)

    menu: QMenu = QMenu(parent)
    menu.setStyleSheet(
        """
        QMenu {
            font-size: 14px;
        }
        QMenu::item {
            padding: 5px 20px;
            height: 25px;
        }
        QMenu::item:selected {
            background-color: #e0e0e0;
        }
    """
    )

    export_action: QAction = QAction("Export", parent)
    export_action.triggered.connect(  # type: ignore
        lambda: export_files(entries, parent, reload_callback)
    )
    menu.addAction(export_action)  # type: ignore

    delete_action: QAction = QAction("Delete", parent)
    delete_action.triggered.connect(  # type: ignore
        lambda: delete_files(entries, parent, reload_callback)
    )
    menu.addAction(delete_action)  # type: ignore

    menu.exec(QCursor.pos())  # type: ignore


def export_files(
    paths: List[str], parent: QWidget, reload_callback: Callable[[], None]
) -> None:
    target_dir: str = QFileDialog.getExistingDirectory(parent, "Export to...")
    if not target_dir:
        return

    loading = LoadingDialog("Exporting files...")
    loading.show()
    QApplication.processEvents()

    task = BackgroundTask(lambda: pull_files(paths, target_dir))
    task.signals.finished.connect(lambda: (loading.close(), reload_callback()))  # type: ignore
    task.signals.error.connect(lambda err: print(f"Export error: {err}"))  # type: ignore # Optional error logging
    thread_pool.start(task)  # type: ignore


def delete_files(
    paths: List[str], parent: QWidget, reload_callback: Callable[[], None]
) -> None:
    if not show_delete_confirmation(parent, len(paths)):
        return
    loading = LoadingDialog("Deleting files...")
    loading.show()
    QApplication.processEvents()  # Make sure dialog is shown before blocking task starts

    task = BackgroundTask(lambda: delete_files_on_device(paths))
    task.signals.finished.connect(lambda: (loading.close(), reload_callback()))  # type: ignore
    task.signals.error.connect(lambda err: print(f"Delete error: {err}"))  # type: ignore # Optional: error handling
    thread_pool.start(task)  # type: ignore
