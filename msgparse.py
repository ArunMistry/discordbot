import discord
from discord.ext import commands
import os
from discord.ext.commands import Bot, cog
from dotenv import load_dotenv
import requests
import json
import importlib


finance = importlib.import_module("finance")

async def parser(client, ctx):
    importlib.reload(finance)
    msg = ctx.content.lower()
    if msg[0] in "!$%^&*?" or "pybot" in msg:
        if "help" in msg:
            await help(ctx)
        elif "currency" in msg or "rate" in msg:
            await finance.currency(ctx, msg)
        elif "stock" in msg or "price" in msg or "share" in msg:
            await finance.stock(ctx, msg)
        else:
            await ctx.channel.send(
                "Hi, I'm Pybot! Check out what I can do by typing `!help` or `Pybot help`"
            )
    else:
        return


async def help(ctx):
    embed = discord.Embed(
        title="Pybot Help",
        description="Pybot can be summoned by including `Pybot` in your message, or starting it with: `!`/`$`/`%`/`^`/`&`/`^`/`*`/`?`.\n"
        + "\nPybot ignores capitalization, and searches for keywords in your message, which are given below.",
        color=0x0044FF,
    )
    embed.add_field(
        name="Currency",
        value="*Keywords:* `rate` / `currency`\n\nPybot will return the exchange rates of 1 - 2 provided currencies."
        + "Provide their 3 letter code(s). Pybot defaults to `USD`, then`CAD`.",
        inline=False,
    )
    embed.add_field(
        name="Stock",
        value="*Keywords:* `stock` / `price` / `share`\n\nPybot will return a few details on the stock asked for."
        + "Provide the stock's ticker or its name within double apostrophes `\"`.",
        inline=False,
    )

    await ctx.channel.send(embed=embed)