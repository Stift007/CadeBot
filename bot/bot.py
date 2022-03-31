from pathlib import Path

import PyXML
from discord.ext import commands


class Format:
    xml = "xml"
    json = "json"

class MusicBot(commands.Bot):
    def __init__(self,*,load_dotenv:bool=False,format:str=Format.xml):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        self.load_dotenv = load_dotenv
        super().__init__(command_prefix=self.prefix, case_insensitive=True)

    def setup(self):
        print("Starting Setup...")
        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` Cog.")

        print("Setup complete!")

    def run(self):
        self.setup()

        with open("data/secrets.xml") as f:
            TOKEN = PyXML.ParseXMLElement(f.read(),"bottoken")

        print("Running Bot...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print(" Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing (on Keyboard interrupt)")
        await self.shutdown()

    async def on_connect(self):
        print(f"Bot connected to Discord! (Latency: {self.latency*1000} ms)")

    async def on_resumed(self):
        print(f"Bot resumed (Latency: {self.latency*1000} ms)")

    async def on_disconnect(self):
        print(f"Bot disconnected")

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print(f"Bot ready (Latency: {self.latency*1000} ms)")

    async def prefix(self,bot,msg):
        return commands.when_mentioned_or("?c ")(bot,msg)

    async def process_commands(self, message):
        ctx = await self.get_context(message,cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)
