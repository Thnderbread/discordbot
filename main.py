import os
import emoji
from dotenv import load_dotenv

import discord
from discord.ext import commands

import utils
from help import TextSpacerHelp

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    print("Could not find BOT_TOKEN environment variable.")
    exit(1)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

description = "My sole job is to spacify your words! Type $help for a demonstration."

bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    help_command=TextSpacerHelp(),
)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected to Discord!")


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    if (
        isinstance(error, commands.errors.UnexpectedQuoteError)
        and ctx.command == "spacify"
    ):
        await ctx.send(
            "Sorry, I don't like double quotes! Please use singles (' ') instead!"
        )
    else:
        print(error)
        await ctx.send("Sorry, I couldn't spacify that. Try it again.")


# Actually made a mistake. The function should have params
# of ctx, *, and message (args) - this brings in the entire message
# without splitting words into letters in a tuple per word.
# I was just blindly following tutorials and did it wrong.
# For now though, this provides an easier way to process
# Discord emotes via the is_emote's regex implementation,
# s+o I'll keep it like this until I feel like cleaning it up.
@bot.command()
async def spacify(ctx: commands.Context, *args: tuple[str]):
    """
    Spacify your text! Use {} to ignore words.
    For example, $spacify Hello {there!} yields:
    H e l l o there!
    (Note - I only have access to emotes in this server!)
    """
    if len(args) == 0:
        await ctx.send(f"## Usage:\n\n{spacify.help}")
        return
    elif len(args) > 100:
        await ctx.send("That shit too long man!")
        return

    # get the emotes at the start of processing
    # to know what the bot has access to when it
    # encounters an emote
    bot_emotes = utils.get_bot_emotes(bot)

    # For when the user wants to ignore a substring.
    # Toggled via {}.
    ignoring = False

    spaced_message = ""
    for fragment in args:
        if len("".join(fragment)) > 50:
            await ctx.send("That shit too long man!")
            return
        # ignore discord emote fragments
        if utils.is_emote(emote := "".join(fragment)):
            # add a space if the bot doesn't have access to the emote
            if utils.emote_is_available(emote, bot_emotes):
                spaced_message += emote
            else:
                spaced_message += emote + " "
            continue

        # check for ignore
        if fragment[0] == "{":
            word = "".join(fragment)
            # if the ignore starts and ends
            # on the same value, e.g. {ignored},
            # handle it here at once.
            if word.endswith("}"):
                spaced_message += word[1:-1] + " "
                continue
            else:
                ignoring = True
                spaced_message += word[1:] + " "
                continue

        # if ignoring, first see if the end flag is present.
        # if so, add the message, stop ignoring.
        # if not, add the message and continue.
        if ignoring:
            word = "".join(fragment)
            if word.endswith("}"):
                ignoring = False
                word = word[:-1]
            spaced_message += word + " "
            continue

        # spacing the letters in the fragment
        for letter in fragment:
            if letter.isspace():
                spaced_message += " "
                continue

            # add a space behind emojis
            elif emoji.is_emoji(letter):
                spaced_message += letter + " "
                continue

            # Just a regular letter to space
            spaced_message += letter + " "

    await ctx.send(spaced_message.strip())


spacify.usage = "- Type any message, {ignore words by using braces}"

if __name__ == "__main__":
    bot.run(TOKEN)
