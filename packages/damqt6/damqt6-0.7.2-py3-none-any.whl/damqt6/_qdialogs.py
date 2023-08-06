from threading import Timer

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout

from ._common import _QBaseDialog
from ._qlineedits import QBaseLineEdit


QBaseDialog = _QBaseDialog


class QTopDialog(QBaseDialog):
    def __init__(self, **kwargs):
        super().__init__(parent=None, **kwargs)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)


class QModalDialog(QBaseDialog):
    def __init__(self, parent: QWidget, dialogid: str, **kwargs):
        super().__init__(parent=parent, dialogid=dialogid, **kwargs)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def show(self) -> None:
        assert False, f"Call to modal dialog '{self.dialogid}.show()'"


class QIsbnInputDialog(QModalDialog):
    def __init__(self, parent: QWidget, **kwargs):
        super().__init__(parent=parent, dialogid='isbn_input', **kwargs)
        self._notify_fct = None
        self.setWindowTitle(_('Enter ISBN'))
        self.setStyleSheet('background-color: orange;')
        self.setFixedWidth(200)
        self.setFixedHeight(60)
        self._edit_isbn = QBaseLineEdit()
        self._button_close = QPushButton(_('Close'))
        layout = QGridLayout()
        layout.addWidget(self._edit_isbn, 0, 0)
        layout.addWidget(self._button_close, 1, 0)
        self.setLayout(layout)
        self._button_close.clicked.connect(self.reject)
        self._cleartimer = Timer(2.0, self._clear_text)

    def getIsbns(self, notify_fct):
        assert self._notify_fct is None, f"Double call to '{self.dialogid}.getIsbns()'"
        self._notify_fct = notify_fct
        self.open()

    def reject(self) -> None:
        if self._edit_isbn.text():
            self._clear_text()
            self._edit_isbn.setFocus()
        else:
            self._notify_fct = None
            super().reject()

    def event(self, e: QtCore.QEvent) -> bool:
        if e.type() == QtCore.QEvent.Type.WindowActivate:
            self._button_close.setDefault(False)
            self._edit_isbn.setFocus()
        elif isinstance(e, QtGui.QKeyEvent) and e.type() == QtCore.QEvent.Type.KeyRelease:
            text = self._edit_isbn.text()
            if e.key() == Qt.Key.Key_Return:
                if not self._cleartimer.is_alive():
                    self._notify_fct(text)
                    self._cleartimer = Timer(2.0, self._clear_text)
                    self._cleartimer.start()
            elif self._cleartimer.is_alive():
                self._cleartimer.cancel()
                self._edit_isbn.setText(text[-1:])

        return super().event(e)

    def _clear_text(self):
        self._cleartimer.cancel()
        self._edit_isbn.setText('')
