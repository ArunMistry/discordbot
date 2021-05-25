import discord
import os
from dotenv import load_dotenv
import importlib

load_dotenv()
msgparse = importlib.import_module("msgparse")

class myClient(discord.Client):
    async def on_connect(self):
        print("Connected")
    async def on_disconnect(self):
        print("Disconnected")
    async def on_ready(self):
        print(f"Logged in as {client.user}".format(client))

    async def on_message(self, ctx):
        print(f"Message from {ctx.author}: {ctx.content}")
        if ctx.author == client.user:
            return
        elif ctx.content.startswith("die"): # remove once done, only for prototyping
            await client.close()
        else:
            importlib.reload(msgparse) # remove once done, only for prototyping
            await msgparse.parser(client, ctx)



client = myClient()
client.run(os.getenv("DISCORD_TOKEN"), reconnect=True, bot=True)
