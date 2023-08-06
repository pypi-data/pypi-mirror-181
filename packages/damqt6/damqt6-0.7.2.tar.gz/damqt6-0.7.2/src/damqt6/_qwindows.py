from PyQt6.QtCore import Qt

from ._common import _QBaseMainWindow


class QTopMainWindow(_QBaseMainWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
