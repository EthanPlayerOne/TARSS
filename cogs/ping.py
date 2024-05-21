import disnake
from disnake.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Пинг бота в мс.")
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(f"Понг! {round(self.bot.latency * 1000)} мс")

def setup(bot: commands.Bot):  # чтобы disnake мог загружать ког, когда он будет добавлен в main.py.
    bot.add_cog(PingCommand(bot))
    