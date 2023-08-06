from threading import Timer
from typing import Callable, Tuple

from PyQt6.QtCore import QObject, QEvent, Qt, QTimerEvent
from PyQt6.QtGui import QValidator
from PyQt6.QtWidgets import QComboBox

from damstrings import Strings

from ._common import _NotificationHolder
from ._qvalidators import QBaseValidator


class QBaseComboBox(QComboBox):
    _clear_focus_in_memo_delay = 0.1

    def __init__(self, *, itemsortkey=Strings.stripaccents_lower, stab_time=0, event_filter: QObject = None, **kwargs):
        super().__init__(**kwargs)
        self.setValidator(QBaseValidator())
        self._itemsortkey = itemsortkey
        self._stab_time = stab_time
        self._text_edited_timerid = 0
        self._text_changed_in_progress = False
        self._previndex = -1
        self.setEditable(True)
        self.lineEdit().textEdited.connect(self._text_edited)
        self._text_changed_holder = _NotificationHolder()
        self.currentTextChanged.connect(self._text_changed_holder.notify_if_not_held)
        self.add_text_changed_notify(self._text_changed)
        self._focus_in_memo = False
        self.installEventFilter(self)
        self.lineEdit().installEventFilter(self)
        if event_filter:
            self.installEventFilter(event_filter)
        self._clear_focus_in_memo_timer = Timer(self._clear_focus_in_memo_delay, self._clear_focus_in_memo)

    def add_text_changed_notify(self, fct: Callable[[], None]):
        self._text_changed_holder.add_function_to_notify(fct)

    def text_changed_holder(self):
        return self._text_changed_holder

    def setCurrentText(self, text: str, *, set_if_same=True) -> None:
        if set_if_same or not Strings.check_equal(self.currentText(), text, nocase=True):
            ix = self.findText(text)
            if ix >= 0:
                self.setCurrentIndex(ix)
            super().setCurrentText(text)

    def setItems(self, items):
        with self._text_changed_holder:
            if self._itemsortkey:
                items.sort(key=self._itemsortkey)
            self.clear()
            self.addItems(items)
            self.setCurrentText('')

    def eventFilter(self, o: 'QObject', e: 'QEvent') -> bool:
        if o is self:
            if e.type() == QEvent.Type.FocusIn:
                self._focus_in_memo = True
                self._clear_focus_in_memo_timer = Timer(self._clear_focus_in_memo_delay, self._clear_focus_in_memo)
                self._clear_focus_in_memo_timer.start()
            elif e.type() == QEvent.Type.FocusOut:
                if self._text_edited_timerid != 0:
                    self.killTimer(self._text_edited_timerid)
                    self._text_edited_timerid = 0
                    self._text_changed_holder.release_notifications()
        elif o is self.lineEdit():
            if e.type() == QEvent.Type.MouseButtonPress:
                self._clear_focus_in_memo_timer.cancel()
            elif e.type() == QEvent.Type.MouseButtonRelease:
                if self._focus_in_memo and not self.lineEdit().selectedText():
                    self.lineEdit().selectAll()
                self._focus_in_memo = False
            return o.eventFilter(o, e)
        return super().eventFilter(o, e)

    def _clear_focus_in_memo(self):
        self._focus_in_memo = False

    def _text_edited(self):
        if self._stab_time != 0:
            if self._text_edited_timerid == 0:
                self._text_changed_holder.hold_notifications()
            else:
                self.killTimer(self._text_edited_timerid)
            self._text_edited_timerid = self.startTimer(self._stab_time, Qt.TimerType.CoarseTimer)

    def timerEvent(self, e: QTimerEvent) -> None:
        if e.timerId() == self._text_edited_timerid:
            self.killTimer(self._text_edited_timerid)
            self._text_edited_timerid = 0
            self._text_changed_holder.release_notifications()

    def _text_changed(self):
        if self._text_changed_in_progress:
            return

        self._text_changed_in_progress = True

        if self.itemText(self.currentIndex()) != self.currentText():
            with self.text_changed_holder():
                new_text = self.currentText()
                item_ix = self._find_closest_item_ix(new_text)

                if item_ix:
                    selstart = self.lineEdit().cursorPosition()
                    sel_len = len(self.lineEdit().selectedText())
                    self.setCurrentIndex(item_ix)
                    self.setCurrentText(new_text, set_if_same=False)
                    self.lineEdit().setSelection(selstart, sel_len)

                elif self.currentText() == '':
                    self.setCurrentIndex(-1)

        elif self.hasFocus() and self.itemText(self.currentIndex()) == self.currentText()\
                and self.isEditable() and self.currentIndex() != self._previndex:
            self.lineEdit().selectAll()

        self._previndex = self.currentIndex()
        self._text_changed_in_progress = False

    def _find_closest_item_ix(self, text: str) -> int:
        lower_ix = None
        stripped_ix = None
        new_lower_text = text.lower()
        new_stripped_text = Strings.stripaccents(new_lower_text)

        for ix in range(self.count()):
            item_lower_text = self.itemText(ix).lower()
            item_stripped_text = Strings.stripaccents(item_lower_text)
            if lower_ix is None and item_lower_text.startswith(new_lower_text):
                lower_ix = ix
            elif stripped_ix is None and item_stripped_text.startswith(new_stripped_text):
                stripped_ix = ix
            elif item_stripped_text > new_stripped_text:
                break
            if lower_ix is not None and stripped_ix is not None:
                break

        stripped_ix = stripped_ix - 1 if stripped_ix is not None and stripped_ix > 0 else stripped_ix
        return lower_ix if lower_ix is not None else stripped_ix


class QExistingComboItemValidator(QBaseValidator):
    def __init__(self, *, parent: QBaseComboBox):
        super().__init__(parent=parent)
        self.__parent = parent

    def validate(self, text: str, pos: int) -> Tuple[QValidator.State, str, int]:
        state, text, pos = super().validate(text, pos)
        if state != QValidator.State.Invalid:
            if self.__parent.findText(text, Qt.MatchFlag.MatchExactly) != -1:
                state = QValidator.State.Acceptable
            elif self.__parent.findText(text, Qt.MatchFlag.MatchStartsWith) != -1:
                state = QValidator.State.Intermediate
            else:
                state = QValidator.State.Invalid
        return state, text, pos
