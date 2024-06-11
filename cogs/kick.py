import disnake 
from disnake.ext import commands
from update_log import update_log

class KickCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reason: str
        self.member: disnake.Member

    @commands.slash_command(name="kickuser", description="Выгнать участника.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = "unspecified"):
        if member.id==1091070338126852166:
            await inter.response.send_message(f'Меня нельзя выгнать.')  # :^) 
            log_text=f'[INFO]  KICK: {inter.author} tried to kick TARSS.'
        else:
            await member.kick(reason=reason)
            await inter.response.send_message(f'{member.mention} был изгнан.')
            log_text = f"[INFO]  KICK used successfully. {member} was kicked by {inter.author}"

        update_log(log_text)

    @kick.error
    async def kick_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.response.send_message("**ОШИБКА:** недостаточно прав.", ephemeral=True)
            log_text = f"[ERROR]  KICK: MissingPermissions Error. User: {inter.author}"
            update_log(log_text)

        elif isinstance(error, commands.MissingRequiredArgument):
            await inter.response.send_message("**ОШИБКА**: укажите все необходимые аргументы.", ephemeral=True)
            log_text = f"[ERROR]  KICK: MissingRequiredArgument Error. User: {inter.author}"

        else:
            await inter.response.send_message("**ОШИБКА**: нет информации.", ephemeral=True)
            log_text = f"[ERROR]  KICK: unexpected Error. User: {inter.author}"
            print(error)


def setup(bot: commands.Bot):  
    bot.add_cog(KickCommand(bot))