from abc import ABC, abstractmethod


class ABCButton(ABC):
    """
    An abstract button interface.
    Currently does not hold anything.
    """

    pass


class ABCKeyboard(ABC):
    """
    An abstract keyboard builder interface.
    """

    @abstractmethod
    def add(self, button: ABCButton) -> "ABCKeyboard":
        """
        Adds a button to the keyboard.
        """
        pass

    @abstractmethod
    def row(self) -> "ABCKeyboard":
        """
        Adds a row to the keyboard.
        Panics if the last row was empty.
        """
        pass
