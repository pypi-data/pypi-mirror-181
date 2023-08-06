from typing import Callable, Union

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDialog, QLayout, QWidget

from ._settings import Settings, SettingInfo


def clear_layout(layout: QLayout):
    if layout:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() if hasattr(item, 'widget') else None
            sublay = item.layout() if hasattr(item, 'layout') else None
            if isinstance(widget, QWidget):
                clear_layout(widget.layout())
                layout.removeWidget(widget)
                widget.setParent(None)
                widget.deleteLater()
            if isinstance(sublay, QLayout):
                clear_layout(sublay)
                layout.removeItem(sublay)
                sublay.deleteLater()


class _NotificationHolder:
    def __init__(self):
        self._hold_count = 0
        self._functions_to_notify = []
        self._notifications_held = False

    def add_function_to_notify(self, fct: Callable[[], None]):
        self._functions_to_notify.append(fct)

    def __enter__(self):
        self.hold_notifications()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release_notifications()

    def hold_notifications(self):
        self._hold_count += 1

    def release_notifications(self):
        assert self._hold_count > 0
        self._hold_count -= 1
        if self._notifications_held:
            self._notifications_held = False
            self.notify_if_not_held()

    def holding_notifications(self):
        return self._hold_count > 0

    def cancel_held_notifications(self):
        self._notifications_held = False

    def notify_if_not_held(self):
        if not self.holding_notifications():
            for fct in self._functions_to_notify:
                fct()
        else:
            self._notifications_held = True


class _DialogId:
    def __init__(self, *, dialogid: str, **kwargs):
        assert dialogid != '', f"{self.__class__}: missing 'dialogid'"
        super().__init__(**kwargs)
        self.dialogid = '/'.join(['dialog', dialogid])


class _QBaseMainWindow(QMainWindow, _DialogId):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _read_window_pos(self)

    def showEvent(self, e: QtGui.QShowEvent) -> None:
        _read_window_pos(self)
        super().showEvent(e)

    def hideEvent(self, e: QtGui.QHideEvent) -> None:
        _write_window_pos(self)
        super().hideEvent(e)


class _QBaseDialog(QDialog, _DialogId):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.CustomizeWindowHint |
                            Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)
        _read_window_pos(self)

    def show(self) -> None:
        if self.isVisible():
            self.activateWindow()
        else:
            super().show()

    def showNormal(self) -> None:
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized & ~Qt.WindowState.WindowMaximized)

    def showMinimized(self) -> None:
        self.show()
        self.setWindowState(self.windowState() | Qt.WindowState.WindowMinimized)

    def showMaximized(self) -> None:
        self.show()
        self.setWindowState(self.windowState() | Qt.WindowState.WindowMaximized)

    def showEvent(self, e: QtGui.QShowEvent) -> None:
        _read_window_pos(self)
        super().showEvent(e)

    def hideEvent(self, e: QtGui.QHideEvent) -> None:
        _write_window_pos(self)
        super().hideEvent(e)


_setting_window_left = SettingInfo(key='left', default=0)
_setting_window_top = SettingInfo(key='top', default=0)
_setting_window_width = SettingInfo(key='width', default=640)
_setting_window_height = SettingInfo(key='height', default=480)


def _read_window_pos(window: Union[_QBaseMainWindow, _QBaseDialog]):
    left = int(Settings.read(setting_info=_setting_window_left, source=window.dialogid))
    top = int(Settings.read(setting_info=_setting_window_top, source=window.dialogid))
    width = int(Settings.read(setting_info=_setting_window_width, source=window.dialogid))
    height = int(Settings.read(setting_info=_setting_window_height, source=window.dialogid))
    window.setGeometry(left, top, width, height)  # TODO ensure window/dialog is within screen boundaries


def _write_window_pos(window: Union[_QBaseMainWindow, _QBaseDialog]):
    Settings.write(setting_info=_setting_window_left, value=window.geometry().left(),
                   source=window.dialogid)
    Settings.write(setting_info=_setting_window_top, value=window.geometry().top(),
                   source=window.dialogid)
    Settings.write(setting_info=_setting_window_width, value=window.geometry().width(),
                   source=window.dialogid)
    Settings.write(setting_info=_setting_window_height, value=window.geometry().height(),
                   source=window.dialogid)
