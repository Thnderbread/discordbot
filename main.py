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


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.content.startswith("$spacify"):
        await message.delete()

    bot.process_commands(message)


# TODO: the " " in fragment check doesn't work if the user wants to ignore only one word.
# TODO: figure out how to show more descriptive help messages.
@bot.command()
async def spacify(ctx: commands.Context, *args: tuple[str]):
    print(f"Look at the args!: {args}")
    if len(args) == 0:
        return

    spaced_message = ""
    for fragment in args:
        # The user wants to ignore this substring, join it and
        # add a space behind it.
        if " " in fragment:
            print(f"Space in {fragment}!")
            ignore = "".join(fragment)
            spaced_message += ignore + " "
            continue
        # if the current fragment is a discord emote, ignore it
        elif isEmote(emote := "".join(fragment)):
            f"{emote} is an emote!"
            spaced_message += emote
            continue
        # space out the letters in the word
        for letter in fragment:
            if letter.isspace():
                spaced_message += " "
                continue
            # if the letter is an emoji, add a space and keep going
            elif emoji.is_emoji(letter):
                spaced_message += letter + " "
                continue
            spaced_message += letter + " "

    await ctx.send(spaced_message)


if __name__ == "__main__":
    bot.run(TOKEN)
