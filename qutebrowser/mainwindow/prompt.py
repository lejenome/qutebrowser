# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2016 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Showing prompts above the statusbar."""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLineEdit, QLabel, QSpacerItem

from qutebrowser.config import style, config
from qutebrowser.utils import usertypes


class PromptContainer(QWidget):

    update_geometry = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Prompt')
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(10, 10, 10, 10)
        style.set_register_stylesheet(self,
                                      generator=self._generate_stylesheet)

    def _generate_stylesheet(self):
        """Generate a stylesheet with the right edge rounded."""
        stylesheet = """
            QWidget#Prompt {
                border-POSITION-left-radius: 10px;
                border-POSITION-right-radius: 10px;
            }

            QWidget {
                /* FIXME
                font: {{ font['keyhint'] }};
                FIXME
                */
                color: {{ color['statusbar.fg.prompt'] }};
                background-color: {{ color['statusbar.bg.prompt'] }};
            }

            QLineEdit {
                border: 1px solid grey;
            }
        """
        position = config.get('ui', 'status-position')
        if position == 'top':
            return stylesheet.replace('POSITION', 'bottom')
        elif position == 'bottom':
            return stylesheet.replace('POSITION', 'top')
        else:
            raise ValueError("Invalid position {}!".format(position))


    def _show_prompt(self, prompt):
        while True:
            # FIXME do we really want to delete children?
            child = self._layout.takeAt(0)
            if child is None:
                break
            child.deleteLater()

        self._layout.addWidget(prompt)
        self.update_geometry.emit()


class _BasePrompt(QWidget):

    """Base class for all prompts."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QGridLayout(self)
        self._layout.setVerticalSpacing(15)

    def _init_title(self, title, *, span=1):
        label = QLabel('<b>{}</b>'.format(title), self)
        self._layout.addWidget(label, 0, 0, 1, span)

    def accept(self, value=None):
        pass


class LineEditPrompt(_BasePrompt):

    def __init__(self, question, parent=None):
        super().__init__(parent)
        qle = QLineEdit(self)
        self._layout.addWidget(qle, 1, 0)
        self._init_title(question.text)
        if question.default:
            qle.setText(question.default)


class AuthenticationPrompt(_BasePrompt):

    def __init__(self, question, parent=None):
        super().__init__(parent)
        self._init_title(question.text, span=2)
        user_label = QLabel("Username:", self)
        user_qle = QLineEdit(self)
        password_label = QLabel("Password:", self)
        password_qle = QLineEdit(self)
        password_qle.setEchoMode(QLineEdit.Password)
        self._layout.addWidget(user_label, 1, 0)
        self._layout.addWidget(user_qle, 1, 1)
        self._layout.addWidget(password_label, 2, 0)
        self._layout.addWidget(password_qle, 2, 1)
        if question.default:
            qle.setText(question.default)

        spacer = QSpacerItem(0, 10)
        self._layout.addItem(spacer, 3, 0)

        help_1 = QLabel("<b>Accept:</b> Enter")
        help_2 = QLabel("<b>Abort:</b> Escape")
        self._layout.addWidget(help_1, 4, 0)
        self._layout.addWidget(help_2, 5, 0)


# def _display_question_yesno(self, prompt):
#     """Display a yes/no question."""
#     if self._question.default is None:
#         suffix = ""
#     elif self._question.default:
#         suffix = " (yes)"
#     else:
#         suffix = " (no)"
#     prompt.txt.setText(self._question.text + suffix)
#     prompt.lineedit.hide()

# def _display_question_input(self, prompt):
#     """Display a question with an input."""
#     text = self._question.text
#     if self._question.mode == usertypes.PromptMode.download:
#         key_mode = self.KEY_MODES[self._question.mode]
#         key_config = objreg.get('key-config')
#         all_bindings = key_config.get_reverse_bindings_for(key_mode.name)
#         bindings = all_bindings.get('prompt-open-download', [])
#         if bindings:
#             text += ' ({} to open)'.format(bindings[0])
#     prompt.txt.setText(text)
#     if self._question.default:
#         prompt.lineedit.setText(self._question.default)
#     prompt.lineedit.show()

# def _display_question_alert(self, prompt):
#     """Display a JS alert 'question'."""
#     prompt.txt.setText(self._question.text + ' (ok)')
#     prompt.lineedit.hide()

