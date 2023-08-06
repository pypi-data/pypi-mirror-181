from typing import Union

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton as PyQt6_PushButton, QWidget


class QPushButton(PyQt6_PushButton):
    def __init__(self, *, text: str = '', parent: QWidget = None, event_filter: QObject = None, tag=None, **kwargs):
        super().__init__(text=text, parent=parent, **kwargs)
        if event_filter:
            self.installEventFilter(event_filter)
        self.tag = tag


class QLabelButton(QPushButton):
    def __init__(self, *, text: str = '', parent: QWidget = None, event_filter: QObject = None, tag=None, **kwargs):
        super().__init__(text=text, parent=parent, event_filter=event_filter, tag=tag, **kwargs)
        self.setStyleSheet('text-align: left; padding-left: 5px; padding-right: 5px')


class QIconButton(QPushButton):
    def __init__(self, *, icon: Union[QIcon, str], parent: QWidget = None, event_filter: QObject = None, tag=None,
                 **kwargs):
        super().__init__(parent=parent, event_filter=event_filter, tag=tag, **kwargs)
        if isinstance(icon, str):
            icon = QIcon(icon)
        self.setIcon(icon)
