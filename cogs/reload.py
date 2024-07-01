import disnake
from disnake.ext import commands
from update_log import update_log

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="reload_cog", description="Reloads a specified cog")
    async def reload(self, inter: disnake.AppCmdInter, cog_name: str):
        if cog_name=='all':
            for c in self.bot.cogs:
                self.bot.unload_extension(c)
                self.bot.load_extension(c)
            await inter.response.send_message(f'Все коги были успешно перезагружены.')
            log_text=f'[INFO]  RELOAD: all cogs were reloaded by {inter.author}'

        else:    
            self.bot.unload_extension(f"cogs.{cog_name}")
            self.bot.load_extension(f"cogs.{cog_name}")
            await inter.response.send_message(f"Ког `{cog_name}` был успешно перезапущен.")
            log_text = f"[INFO]  RELOAD: cog {cog_name} were reloaded by {inter.author}"
        
        update_log(log_text)

    @reload.error
    async def reload_error(self, inter:disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await inter.response.send_message(f"**ОШИБКА:** указанный ког не найден.")
            log_text=f"[ERROR]  RELOAD: Cog not found. User: {inter.author}"
            
        if isinstance(error, commands.MissingPermissions):
            await inter.response.send_message(f"**ОШИБКА:** недостаточно прав для выполнения операции перезагрузки.")
            log_text=f"[ERROR]  RELOAD: MissingPermissions Error. User: {inter.author}"

        else:
            await inter.response.send_message(f'**ОШИБКА**: неизвестная ошибка. Обратитесь к разработчику.')
            log_text = f'[ERROR]  RELOAD: Unknown error. User: {inter.author}'
        update_log(log_text=log_text)

'''
!!! ВАЖНО !!!
В случае любой ошибки которую берет этот обработчик, в терминал будет выпрыгивать ошибка:
disnake.ext.commands.errors.CommandInvokeError: Command raised an exception: InteractionResponded: This interaction has already been responded to before
Это нормально и ни на что не влияет так что ее можно спокойно игнорировать. Это будет исправлено в будущих версиях.

Кто скажет, каким образом "/reload cog_name:reload" работает, дам печеньку.
'''

def setup(bot):
    bot.add_cog(Reload(bot))
