from typing import Any, Callable, List, Mapping

import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command


class TextSpacerHelp(commands.HelpCommand):
    def get_command_signature(
        self, command: Command[Any, Callable[..., Any], Any]
    ) -> str:
        return (
            f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
        )

    async def send_bot_help(
        self, mapping: Mapping[Cog | None, List[Command[Any, Callable[..., Any], Any]]]
    ) -> None:
        # create the embed
        embed = discord.Embed(title="Help", color=discord.Color.blurple())

        # go through the list of tuples containing
        # cogs and the list of commands.
        # Add the Cog (category), its sub commands,
        # and their params for each item in mapping.items.
        for cog, cmds in mapping.items():
            # command_signatures are the params or args.
            filtered = await self.filter_commands(cmds, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]

            if command_signatures:
                # get the name of the cog. Default to No Category
                # then, add a field for the cog and its command.
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(
                    name=cog_name, value="\n".join(command_signatures), inline=False
                )

        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command: Command):
        embed = discord.Embed(
            title=self.get_command_signature(command), color=discord.Color.random()
        )

        embed.description = f"Custom text: {command.usage or 'No usage provided.'}"

        if command.help:
            embed.add_field(
                name="Command Description", value=command.help, inline=False
            )
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: Cog) -> None:
        embed = discord.Embed(
            title=cog.qualified_name or "No Category",
            color=discord.Color.blurple(),
        )

        if filtered_commands := await self.filter_commands(cog.get_commands()):
            for command in filtered_commands:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.help or "No Help Message For This One...",
                )

        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error: str) -> None:
        embed = discord.Embed(
            title="Error", description=error, color=discord.Color.red()
        )
        await self.get_destination().send(embed=embed)
