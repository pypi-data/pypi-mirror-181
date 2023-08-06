from typing import overload

from PyQt6 import QtGui
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


class QBaseTable(QTableWidget):
    def __init__(self, event_filter: QObject = None, **kwargs):
        super().__init__(**kwargs)
        self.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        if event_filter:
            self.installEventFilter(event_filter)

    def clear(self):
        super().clear()

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() - e.angleDelta().y())


class QBaseTableItem(QTableWidgetItem):
    @overload
    def __init__(self, type_: int = QTableWidgetItem.ItemType): ...
    @overload
    def __init__(self, text: str, type_: int = QTableWidgetItem.ItemType): ...
    @overload
    def __init__(self, icon: QIcon, text: str, type_: int = QTableWidgetItem.ItemType): ...
    @overload
    def __init__(self, other: 'QBaseTableItem'): ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
