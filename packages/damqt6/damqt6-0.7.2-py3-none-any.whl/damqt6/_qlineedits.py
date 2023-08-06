from threading import Timer
from typing import Callable

from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QLineEdit

from ._common import _NotificationHolder
from ._qvalidators import QBaseValidator


class QBaseLineEdit(QLineEdit):
    def __init__(self, *, event_filter: QObject = None, edited_delay=0.0, **kwargs):
        super().__init__(**kwargs)
        self.setValidator(QBaseValidator())
        self._focus_in_memo = False
        self.installEventFilter(self)
        if event_filter:
            self.installEventFilter(event_filter)
        self.setTextMargins(5, 0, 5, 0)
        self._clear_focus_in_memo_timer = Timer(0.1, self._clear_focus_in_memo)

        self._text_changed_holder = _NotificationHolder()
        self.textChanged.connect(self._textChanged)
        self._edited_delay = edited_delay
        self._edited_timer = Timer(0.0, ..., None)
        self.textEdited.connect(self._textEdited)

    def add_text_changed_notify(self, fct: Callable[[], None]):
        self._text_changed_holder.add_function_to_notify(fct)

    def text_changed_holder(self):
        return self._text_changed_holder

    def eventFilter(self, o: QObject, e: QEvent) -> bool:
        if o is self:
            if e.type() == QEvent.Type.FocusIn:
                self._focus_in_memo = True
                self._clear_focus_in_memo_timer = Timer(0.1, self._clear_focus_in_memo)
                self._clear_focus_in_memo_timer.start()
                self.selectAll()
            elif e.type() == QEvent.Type.FocusOut:
                if self._edited_timer.is_alive():
                    self._cancel_edited_timer()
                    self._text_changed_holder.notify_if_not_held()
            elif e.type() == QEvent.Type.MouseButtonPress:
                self._clear_focus_in_memo_timer.cancel()
            elif e.type() == QEvent.Type.MouseButtonRelease:
                if self._focus_in_memo and not self.selectedText():
                    self.selectAll()
                self._focus_in_memo = False
        return super().eventFilter(o, e)

    def _clear_focus_in_memo(self):
        self._focus_in_memo = False

    def clear(self) -> None:
        self._cancel_edited_timer()
        super().clear()

    def setText(self, text: str, keep_timer_running=False) -> None:
        if not keep_timer_running:
            self._cancel_edited_timer()
        super().setText(text)

    def selectAll(self) -> None:
        textlen = len(self.text())
        self.setSelection(textlen, - textlen)

    def _cancel_edited_timer(self):
        if self._edited_timer.is_alive():
            self._edited_timer.cancel()

    def _textChanged(self):
        if not self._edited_timer.is_alive():
            self._text_changed_holder.notify_if_not_held()

    def _textEdited(self, text: str):
        if self._edited_delay:
            self._cancel_edited_timer()
            self._edited_timer = Timer(self._edited_delay, self._delayed_edited)
            self._edited_timer.start()
        else:
            self._text_changed_holder.notify_if_not_held()

    def _delayed_edited(self):
        self._text_changed_holder.notify_if_not_held()
