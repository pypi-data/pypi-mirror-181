import re
from typing import Tuple

from PyQt6.QtGui import QValidator


class QBaseValidator(QValidator):
    _re_dup_spaces = re.compile(' +')

    def validate(self, text: str, pos: int) -> Tuple['QValidator.State', str, int]:
        while text and text[0] == ' ':
            text = text[1:]
            pos = max(0, pos - 1)

        valtext = ''
        for ix, char in enumerate(text):
            if char == ' ' and ix + 1 < len(text) and text[ix + 1] == ' ':
                if pos > len(valtext):
                    pos -= 1
            else:
                valtext += char

        state = QValidator.State.Intermediate if valtext.endswith(' ') else QValidator.State.Acceptable
        return state, valtext, pos
