"""Main module."""

import string
import random
import ipyleaflet

class Map(ipyleaflet.Map):

    def __init__(self,center, zoom, **kwargs) -> None:

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(center=center, zoom=zoom, **kwargs)

    def add_search_control(self, position="topleft", **kwargs):
        """Add a search control to the map.

        Args:
            **kwargs: Keyword arguments passed to the search control.
        """
        if "url" not in kwargs:
            kwargs["url"] = "https://nominatim.openstreetmap.org/search?format=json&q={s}"

        search_control = ipyleaflet.SearchControl(position=position, **kwargs)
        self.add_control(search_control)

    def add_draw_control(self, **kwargs):
        """Add a draw control to the map.
        
        Args:
            **kwargs: Keyword arguments passed to the draw control.
        """
        draw_control = ipyleaflet.DrawControl(**kwargs)
        self.add_control(draw_control)


def generate_random_string(length=10, upper=False, digits=False, punctuation=False):
    """Generate a random string of a given length.
        
    Args:
        length (int, optional): The length of the string. Defaults to 10.
        upper (bool, optional): Whether to include uppercase letters. Defaults to False.
        digits (bool, optional): Whether to include digits. Defaults to False.
        punctuation (bool, optional): Whether to include punctuation. Defaults to False.

    Returns:
        str: The generated string.
    """
        
    letters = string.ascii_lowercase
    if upper:
        letters += string.ascii_uppercase
    if digits:
        letters += string.digits
    if punctuation:
        letters += string.punctuation
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    

def generate_lucky_number(length=1):
    """Generate a random number of a given length.

    Args:
        length (int, optional): The length of the number. Defaults to 1.
        
    Returns:
        int: The generated number.
    """

    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return int(result_str)