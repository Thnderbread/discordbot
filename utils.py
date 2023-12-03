import re
from discord.ext.commands import Bot


def is_emote(message: str) -> bool:
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
        raise TypeError(f"Expected {type(str).__name__}, not {type(message).__name__}.")
    emote_regex = r"<a?:[a-zA-Z0-9_]+:\d{17,}>"
    if not isinstance(message, str):
        return False
    if message.startswith("<") and re.search(emote_regex, message) is not None:
        return True


def emote_is_available(emote: str, emote_library: dict[int, str]) -> bool:
    """Tests if the bot has access to ``emote``.

    Args:
        emote (str): The emote to be tested
        emote_library (dict[int, str]): A dictionary containing the bot's
        available emotes.

    Raises:
        TypeError: If the given emote is not of type str.

    Returns:
        bool: True if the emote is found in the library. False otherwise.
    """
    if not isinstance(emote, str):
        raise TypeError(f"Expected {type(str).__name__} not {type(emote).__name__}.")

    emote_id_regex = r"\d{17,}>"
    emote_id = re.search(emote_id_regex, emote)

    if emote_id:
        # make sure to omit the ">"
        return int(emote_id.group()[:-1]) in emote_library
    return False


def get_bot_emotes(bot: Bot) -> dict[int, str]:
    """Return a dictionary containing all the emotes
    the bot has access to.

    Args:
        bot (Bot): The discord bot.

    Returns:
        dict[int, str]: The key is the emote's id. The value
        is the emote's name.
    """
    return {k: v for k, v in list(map(lambda e: {e.id, e.name}, bot.emojis))}
