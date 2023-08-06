from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QObject
from PyQt6.QtWidgets import QLabel


class QBaseLabel(QLabel):
    def __init__(self, *, text: str = '', bold=False, italic=False,
                 alignment: Qt.AlignmentFlag = None,
                 event_filter: QObject = None, **kwargs):
        super().__init__(text=text, **kwargs)
        if bold or italic:
            font = self.font()
            font.setBold(bold)
            font.setItalic(italic)
            self.setFont(font)
        if alignment is not None:
            self.setAlignment(alignment)
        if event_filter:
            self.installEventFilter(event_filter)


class QFieldNameLabel(QBaseLabel):
    def __init__(self, *, text: str = '', **kwargs):
        super().__init__(text=text, bold=True, **kwargs)


class QLinkLabel(QBaseLabel):
    def enterEvent(self, e: QtCore.QEvent) -> None:
        font = self.font()
        font.setUnderline(True)
        self.setFont(font)

    def leaveEvent(self, e: QtCore.QEvent) -> None:
        font = self.font()
        font.setUnderline(False)
        self.setFont(font)
