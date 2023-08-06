"""
Source: https://github.com/tartley/colorama/blob/master/colorama/ansi.py
Copyright: Jonathan Hartley 2013. BSD 3-Clause license.
"""

CSI = "\033["
OSC = "\033]"
BEL = "\007"


def code_to_chars(code):
    """
    Convert a color code to the corresponding ANSI escape sequence.
    :param code:
    :return:
    """
    return CSI + str(code) + "m"


def set_title(title):
    """
    Set the terminal title.
    :param title:
    :return:
    """
    return OSC + "2;" + title + BEL


def clear_screen(mode=2):
    """
    Clear the screen.
    :param mode:
    :return:
    """
    return CSI + str(mode) + "J"


def clear_line(mode=2):
    """
    Clear the current line.
    :param mode:
    :return:
    """
    return CSI + str(mode) + "K"


class AnsiCodes(object):
    """
    ANSI Codes for terminal control.
    """

    def __init__(self):
        """
        Initialize the ANSI codes.
        """
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation, we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith("_"):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class AnsiCursor(object):
    """
    ANSI Cursor Control
    """

    def UP(self, n=1):
        """
        Move the cursor up by `n` rows.
        :param n:
        :return:
        """
        return CSI + str(n) + "A"

    def DOWN(self, n=1):
        """
        Move the cursor down by `n` rows.
        :param n:
        :return:
        """
        return CSI + str(n) + "B"

    def FORWARD(self, n=1):
        """
        Move the cursor forward by `n` columns.
        :param n:
        :return:
        """
        return CSI + str(n) + "C"

    def BACK(self, n=1):
        """
        Move the cursor back by `n` columns.
        :param n:
        :return:
        """
        return CSI + str(n) + "D"

    def POS(self, x=1, y=1):
        """
        Move the cursor to row `x`, column `y`.
        :param x:
        :param y:
        :return:
        """
        return CSI + str(y) + ";" + str(x) + "H"


class AnsiFore(AnsiCodes):
    """
    ANSI Foreground Colours
    """

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 90
    LIGHTRED_EX = 91
    LIGHTGREEN_EX = 92
    LIGHTYELLOW_EX = 93
    LIGHTBLUE_EX = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX = 96
    LIGHTWHITE_EX = 97


class AnsiBack(AnsiCodes):
    """
    ANSI Background Colours
    """

    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 100
    LIGHTRED_EX = 101
    LIGHTGREEN_EX = 102
    LIGHTYELLOW_EX = 103
    LIGHTBLUE_EX = 104
    LIGHTMAGENTA_EX = 105
    LIGHTCYAN_EX = 106
    LIGHTWHITE_EX = 107


class AnsiStyle(AnsiCodes):
    """
    ANSI Text Styles
    """

    BRIGHT = 1
    DIM = 2
    NORMAL = 22
    RESET_ALL = 0


Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()
