import os
import emoji
from dotenv import load_dotenv

import discord
from discord.ext import commands

from utils import isEmote
from help import TextSpacerHelp

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    print("Could not find BOT_TOKEN environment variable.")
    exit(1)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

help_command = commands.DefaultHelpCommand(no_category="Commands")

description = "My sole job is to spacify your words! Type $help for a demonstration."

bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    description=description,
    help_command=TextSpacerHelp(),
)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected to Discord!")


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

    # For when the user wants to ignore a substring.
    # Toggled via {}.
    ignoring = False

    spaced_message = ""
    for fragment in args:
        # ignore discord emote fragments
        if isEmote(emote := "".join(fragment)):
            spaced_message += emote
            continue

        # spacing the letters in the fragment
        for idx, letter in enumerate(fragment):
            if letter.isspace():
                spaced_message += " "
                continue

            # add a space behind emojis
            elif emoji.is_emoji(letter):
                spaced_message += letter + " "
                continue

            if letter == "{":
                ignoring = True
                continue
            elif letter == "}" and ignoring:
                spaced_message += " "
                ignoring = False
                continue

            # add a space if this is the last
            # word in the ignored substring
            if ignoring:
                if idx == len(fragment) - 1:
                    spaced_message += letter + " "
                    continue
                spaced_message += letter
                continue

            # Just a regular letter to space
            spaced_message += letter + " "

    await ctx.send(spaced_message)


spacify.usage = "- Type any message, {ignore words by using braces}"

if __name__ == "__main__":
    bot.run(TOKEN)
