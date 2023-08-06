from typing import Union, Callable

from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QListWidget

from damstrings import Strings


class QBaseListWidget(QListWidget):
    _SortFunction = Union[None, Callable[[str], str]]

    def __init__(self, *, itemsortkey: _SortFunction = Strings.stripaccents_lower, event_filter: QObject = None,
                 **kwargs):
        super().__init__(**kwargs)
        self._itemsortkey = itemsortkey
        self._selection_changed_notify_funtions = []
        if event_filter:
            self.installEventFilter(event_filter)

    def addSelectionChangedNotify(self, fct):
        self._selection_changed_notify_funtions.append(fct)

    def selectionChanged(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection) -> None:
        super().selectionChanged(selected, deselected)
        for fct in self._selection_changed_notify_funtions:
            fct()

    def setItems(self, items) -> None:
        if self._itemsortkey:
            items.sort(key=self._itemsortkey)
        self.clear()
        self.addItems(items)

    def addItem(self, new_item: str) -> None:
        self.__addItem(new_item)

    def insertItem(self, row: int, new_item: str) -> None:
        if row >= self.count() or self._itemsortkey is not None:
            self.__addItem(new_item)
        else:
            super().insertItem(row, new_item)

    def getItem(self, index: int):
        if 0 <= index < self.count():
            return self.item(index)
        else:
            return None

    def curItem(self):
        return self.getItem(self.currentRow())

    def __addItem(self, new_item: str):
        if self._itemsortkey and self.count() > 0:
            sort_item = self._itemsortkey(new_item)
            for ix in range(self.count()):
                list_item = self.item(ix).text()
                if sort_item < self._itemsortkey(list_item):
                    super().insertItem(ix, new_item)
                    break
                elif new_item.lower() == list_item.lower():
                    break
                elif ix == self.count() - 1:
                    super().addItem(new_item)
        else:
            super().addItem(new_item)
