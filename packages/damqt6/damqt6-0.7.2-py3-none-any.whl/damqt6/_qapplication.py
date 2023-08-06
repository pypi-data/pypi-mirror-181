from typing import List

from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QApplication as PyQt6_QApplication, QLineEdit, QComboBox


class QApplication(PyQt6_QApplication):
    _prev_focus = QObject()
    _prev_selection = QObject()

    def __init__(self, argv: List):
        super().__init__(argv)
        self.installEventFilter(self)

    def eventFilter(self, o: QObject, e: QEvent) -> bool:
        if e.type() == QEvent.Type.FocusOut:
            if isinstance(o, QLineEdit):
                self._prev_focus = o
                self._prev_selection = o.selectedText()
            elif isinstance(o, QComboBox):
                self._prev_focus = o
                self._prev_selection = o.lineEdit().selectedText()

        return super().eventFilter(o, e)

    @classmethod
    def prev_focus(cls) -> QObject:
        return cls._prev_focus

    @classmethod
    def prev_selection(cls) -> QObject:
        return cls._prev_selection
