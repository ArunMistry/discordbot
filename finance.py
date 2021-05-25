import discord
import os
from dotenv import load_dotenv
import requests
import importlib

curlist = importlib.import_module("list").curlist
load_dotenv()
key1 = os.getenv("ALPHA1")
key2 = os.getenv("ALPHA2")
key3 = os.getenv("ALPHA3")


async def currency(ctx, msg):
    import string

    msg = msg.translate(str.maketrans("", "", string.punctuation))
    cur1 = "USD"
    cur2 = "CAD"

    check = 0
    for word in msg.upper().split():
        if word in curlist:
            if word == cur1:
                check = 1
                continue
            if check == 0:
                cur2 = word
                check = 1
            else:
                cur1 = word
                break

    async def get_info(cur1, cur2, key):
        response = requests.get(
            f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={cur1}&to_currency={cur2}&apikey={key}"
        )
        return response.json()["Realtime Currency Exchange Rate"]

    info = await get_info(cur1, cur2, key1)
    rate = float(info["5. Exchange Rate"])

    embed = discord.Embed(
        title=f"Currency: {cur1} / {cur2}",
        description=f"1 {cur1} = {rate} {cur2}\n1 {cur2} = {(1/rate):.3f} {cur1}",
        color=0xFF4400,
    )
    await ctx.channel.send(embed=embed)


async def stock(ctx, msg):
    index1 = msg.find('"')
    index2 = 0
    if index1 == -1:
        print("Could not find any double apostrophes")
        return
    else:
        index2 = msg.find('"', index1 + 1)
        if index2 == -1:
            print("Please use double apostrophes around the stock name or ticker")
            return
    stock = msg[index1 + 1 : index2].replace(" ", '%20')

    async def get_ticker(stock, key):
        r1 = requests.get(
            f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={stock}&apikey={key}"
        ).json()
        if r1["bestMatches"]:
            return r1["bestMatches"][0]["1. symbol"]
        else:
            return

    async def get_stock_info(ticker, key):
        r1 = requests.get(
            f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={key}"
        ).json()["Global Quote"]
        r2 = requests.get(
            f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={key}"
        ).json()

        import regex as re
        desc = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", r2['Description'])

        return {
            "name": f"{r2['Symbol']} - {r2['Name']}",
            "price": f"{r1['05. price']} {r2['Currency']}",
            "volume": f"{r1['06. volume']}",
            "change": f"{r1['09. change']} {r2['Currency']} ({r1['10. change percent']}) from previous day",
            "52week": f"{r2['52WeekLow']} {r2['Currency']} to {r2['52WeekHigh']} {r2['Currency']}",
            "exchange": f"{r2['Exchange']} - {r2['Country']}",
            "industry": f"{r2['Sector']} - {r2['Industry']}",
            "desc": f"{desc[0] + desc[1]}",
        }

    ticker = await get_ticker(stock, key3)
    if ticker:
        info = await get_stock_info(ticker, key2)
        embed = discord.Embed(
            title=f"{info['name']}",
            description=f"**Price:** {info['price']}\n**Volume Traded Today:** {info['volume']}\n**Price Change:** {info['change']}\n**52 Week Range:** {info['52week']}",
            color=0xF066AA,
        )
        embed.add_field(
        name="Description",
        value=f"**Exchange:** {info['exchange']}\n**Industry:** {info['industry']}\n**Description:** {info['desc']}",
        inline=False,
        )
        await ctx.channel.send(embed=embed)
    else:
        print("Could not find any ticker for the given stock")
        return
