import pytest
import discord
import pytest_asyncio
from emoji import emojize
from discord.ext import commands
import discord.ext.test as dpytest
from discord.ext.commands.errors import UnexpectedQuoteError
from main import spacify as original_spacify

# test setup according to https://dpytest.readthedocs.io/en/latest/tutorials/using_pytest.html


class Misc(commands.Cog):
    """Test Cog for the discord bot."""

    @commands.command()
    async def test_original_spacify(self, ctx: commands.Context, *message: str):
        print(f"Message: {message}")
        message
        pass
        await original_spacify(ctx, *message)


@pytest_asyncio.fixture
async def setup_bot():
    # Setup
    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True
    intents.message_content = True

    b = commands.Bot(command_prefix="$", intents=intents)

    await b._async_setup_hook()
    await b.add_cog(Misc())

    dpytest.configure(b)

    yield b

    await dpytest.empty_queue()


@pytest.mark.asyncio
async def test_spacify(setup_bot):
    """Properly spaces letters in a regular string"""
    message = "Hello there!"  # noqa: F401
    expected = "H e l l o t h e r e !"

    await dpytest.message(f"$test_original_spacify {message}")
    assert dpytest.verify().message().content(expected)


@pytest.mark.asyncio
async def test_spacify_with_emoji(setup_bot):
    """Properly spaces letters in a string with an emoji"""
    message = emojize("This message has an emoji: :thumbs_up:")
    expected = emojize("T h i s m e s s a g e h a s a n e m o j i : :thumbs_up:")

    await dpytest.message(f"$test_original_spacify {message}")
    print(f"Expected: {expected}")
    assert dpytest.verify().message().content(expected)


@pytest.mark.asyncio
async def test_spacify_with_emote(setup_bot):
    """Properly spaces letters in a string with a discord emote"""
    message = "This message has an emote: <:monkaS:916034138673385492>"
    expected = (
        "T h i s m e s s a g e h a s a n e m o t e : <:monkaS:916034138673385492>"
    )

    await dpytest.message(f"$test_original_spacify {message}")
    assert dpytest.verify().message().content(expected)


@pytest.mark.asyncio
async def test_spacify_with_ignore(setup_bot):
    """Properly spaces letters in a string and ignores substrings in curly braces"""
    message = "Spaced {not spaced}"
    expected = "S p a c e d not spaced"

    await dpytest.message(f"$test_original_spacify {message}")
    assert dpytest.verify().message().content(expected)


@pytest.mark.asyncio
async def test_spacify_with_emotes_and_ignore(setup_bot):
    """
    Properly spaces letters in a string that has
    a discord emote and emoji, and ignores substrings in curly braces
    """
    message = emojize(
        "Spaced with emoji: :thumbs_up: and emote: <:monkaS:916034138673385492> and ignore: {ignored!}"
    )
    expected = emojize(
        "S p a c e d w i t h e m o j i : :thumbs_up: a n d e m o t e : <:monkaS:916034138673385492> a n d i g n o r e : ignored!"
    )

    await dpytest.message(f"$test_original_spacify {message}")
    assert dpytest.verify().message().content(expected)


@pytest.mark.asyncio
async def test_spacify_with_no_message(setup_bot):
    """Sends the usage message when no message is given"""
    message = ""
    expected = f"## Usage:\n\n{original_spacify.help}"

    await dpytest.message(f"$test_original_spacify {message}")
    assert dpytest.verify().message().content(expected)


# Enabled when the length check is implemented.
@pytest.mark.asyncio
async def test_spacify_with_long_message(setup_bot):
    """Sends the message "That shit too long man!"" When too long of a string is given"""
    message = "hi!" * 101
    expected = "That shit too long man!"

    await dpytest.message(f"$test_original_spacify {message}")
    assert dpytest.verify().message().content(expected)


@pytest.mark.asyncio
async def test_spacify_with_double_quote_in_parens(setup_bot):
    """
    Sends the message '"Sorry, I don't like double quotes!
    Please use singles (' ') instead!"' When a string like ("") is given
    """

    message = '("Hello!")'
    expected = "Sorry, I don't like double quotes! Please use singles (' ') instead!"

    try:
        await dpytest.message(f"$test_original_spacify {message}")
        print(f"Expected: {expected}")
    except Exception as e:
        assert isinstance(e, UnexpectedQuoteError)
