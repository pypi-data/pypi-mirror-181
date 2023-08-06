from wonda.tools.keyboard.abc import ABCButton, ABCKeyboard
from wonda.types.objects import KeyboardButton, ReplyKeyboardMarkup


class Button(ABCButton, KeyboardButton):
    """
    An inline button interface for inline keyboard markup.
    """

    pass


class Keyboard(ABCKeyboard, ReplyKeyboardMarkup):
    """
    A reply keyboard builder.
    """

    def add(self, button: Button) -> "Keyboard":
        if not len(self.keyboard):
            self.row()

        self.keyboard[-1].append(button)
        return self

    def row(self) -> "Keyboard":
        if len(self.keyboard) and not len(self.keyboard[-1]):
            raise ValueError("Last row is empty")

        self.keyboard.append([])
        return self
