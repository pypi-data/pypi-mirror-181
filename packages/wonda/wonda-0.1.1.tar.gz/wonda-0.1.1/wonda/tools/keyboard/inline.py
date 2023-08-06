from wonda.tools.keyboard.abc import ABCButton, ABCKeyboard
from wonda.types.objects import InlineKeyboardButton, InlineKeyboardMarkup


class InlineButton(ABCButton, InlineKeyboardButton):
    """
    An inline button interface for inline keyboard markup.
    """

    pass


class InlineKeyboard(ABCKeyboard, InlineKeyboardMarkup):
    """
    An inline keyboard builder.
    """

    def add(self, button: InlineButton) -> "InlineKeyboard":
        if not len(self.inline_keyboard):
            self.row()

        self.inline_keyboard[-1].append(button)
        return self

    def row(self) -> "InlineKeyboard":
        if len(self.inline_keyboard) and not len(self.inline_keyboard[-1]):
            raise ValueError("Last row is empty")

        self.inline_keyboard.append([])
        return self
