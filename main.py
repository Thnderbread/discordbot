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


@bot.command()
async def spacify(ctx: commands.Context, *args: tuple[str]):
    if len(args) == 0:
        await ctx.send(f"## Usage:\n\n{spacify.help}")
        return
    elif len(args) > 100:
        await ctx.send("Whoa! Too much stuff! Try something shorter.")
        return

    bot_emotes = utils.get_bot_emotes(bot)

    ignoring = False

    spaced_message = ""
    for fragment in args:
        if len("".join(fragment)) > 50:
            await ctx.send("Whoa! Too much stuff! Try something shorter.")
            return

        if utils.is_emote(emote := "".join(fragment)):
            if utils.emote_is_available(emote, bot_emotes):
                spaced_message += emote
            else:
                spaced_message += emote + " "
            continue

        if fragment[0] == "{":
            word = "".join(fragment)
            if word.endswith("}"):
                spaced_message += word[1:-1] + " "
                continue
            else:
                ignoring = True
                spaced_message += word[1:] + " "
                continue

        if ignoring:
            word = "".join(fragment)
            if word.endswith("}"):
                ignoring = False
                word = word[:-1]
            spaced_message += word + " "
            continue

        for letter in fragment:
            if letter.isspace():
                spaced_message += " "
                continue

            elif emoji.is_emoji(letter):
                spaced_message += letter + " "
                continue

            spaced_message += letter + " "

    await ctx.send(spaced_message.strip())


spacify.usage = "- Type any message, {ignore words by using braces}"

if __name__ == "__main__":
    bot.run(TOKEN)
