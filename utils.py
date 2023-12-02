import re


def isEmote(message: str) -> bool:
    """Checks if the given message is an emote via regex based on the
    following format: <a:emote_name:1234567890123456789>.

    ## Args:
        ~ message (str): The message to check.

    ## Returns:
        ~ bool: False if the emote format is not found in the string. True if it is.
    ## Raises:
        ~ TypeError: If ``message`` is not a string.
    """
    if not isinstance(message, str):
        raise TypeError(f"Expected {type(str).__name__}, not {type(message).__name__}")
    emote_regex = r"<a:[a-zA-Z0-9_]+:\d+>"
    if not isinstance(message, str):
        return False
    if message.startswith("<") and re.search(emote_regex, message) is not None:
        return True
