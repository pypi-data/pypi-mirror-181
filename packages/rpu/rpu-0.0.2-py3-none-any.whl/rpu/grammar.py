from typing import Union

__all__ = ["Plural", "possessive", "ordinal"]


class Plural:
    def __init__(self, num: Union[int, float]):
        """Returns the plural version of the given text

        Parameters
        ----------
        num: Union[`int`, `float`]
            the number you want to use for getting the plural of text

        Useage
        ----------
        Example: `Plural(5):the_text` -> `5 the_texts`
        """

        self.num = num

    def __format__(self, text: str) -> str:
        if abs(self.num) != 1:
            text += "s"

        return f"{self.num} {text}"


def possessive(text: str) -> str:
    """Returns the possessive version of the given text

    Parameters
    ----------
    text: `str`
        The text you want the possessive version of

    Returns
    ----------
    str
        The possessive version of the text
    """

    if text.endswith("s"):
        text += "'"
    else:
        text += "'s"

    return text


def ordinal(number: int) -> str:
    """Returns the ordinal version of a number

    Parameters
    ----------
    number: `int`
        the number to be turned ordinal

    Returns
    ----------
    str
        the ordinal version

    Examples
    ----------
    >>> ordinal(5)
    ... 5th

    >>> ordinal(2)
    ... 2nd
    """

    return f"{number}{'tsnrhtdd'[(number//10%10!=1)*(number%10<4)*number%10::4]}"
