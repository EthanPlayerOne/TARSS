import disnake
from disnake.ext import commands
from update_log import update_log

class ClearCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.limit: int

    @commands.slash_command(name="clear", description="Удалить limit сообщений в текущем канале.")
    @commands.has_guild_permissions(manage_messages=True) 
    async def clear(self, inter: disnake.ApplicationCommandInteraction, limit: int): # задаем параметр команды limit который является целым числом 
        if limit>0:  # и положительным
            channel = inter.channel
            await channel.purge(limit=limit) 

            await inter.response.send_message(f"**Успешно удалено {limit} сообщений в канале {channel.mention}.**")
            log_text = f"[INFO]  CLEAR used successfully by {inter.author} with {limit} limit."

        else:
            await inter.response.send_message(f"**ОШИБКА:** аргумент *limit* должен быть больше нуля.")
            log_text=f'[ERROR]  CLEAR: InvalidArgument Error. User: {inter.author}'

        update_log(log_text)

    @clear.error
    async def clear_error(self, inter: disnake.ApplicationCommandInteraction, error): 
        if isinstance(error, commands.MissingPermissions): # если недостаточно прав (нет админки):
            await inter.response.send_message("**Ошибка.** Недостаточно прав для выполнения операции очистки.")
            log_text = f"[ERROR]  CLEAR: MissingPermissions Error. User: {inter.author}"
            update_log(log_text)
    

def setup(bot: commands.Bot):  
    bot.add_cog(ClearCommand(bot))