import disnake
from disnake.ext import commands
from update_log import update_log

class BanCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reason: str
        self.member: disnake.Member

    @commands.slash_command(name="banuser", description="Забанить участника.")
    @commands.has_permissions(ban_members=True)
    async def banuser(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = "unspecified"):
        if member.id==1091070338126852166:
            await inter.response.send_message(f'Меня нельзя забанить.')  # :^)
            log_text=f'[INFO]  BAN: {inter.author} tried to ban TARSS.'
        else:
            await member.ban(reason=reason)
            await inter.response.send_message(f'{member.mention} был забанен.')
            log_text = f"[INFO]  BAN used successfully. {member} was banned by {inter.author}."

        update_log(log_text)
        print(log_text)

    @banuser.error
    async def ban_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.response.send_message("**ОШИБКА:** недостаточно прав.", ephemeral=True)
            log_text = f"[ERROR]  BAN: MissingPermissions Error. User: {inter.author}"
            update_log(log_text)

        elif isinstance(error, commands.MissingRequiredArgument):
            await inter.response.send_message("**ОШИБКА**: укажите все необходимые аргументы.", ephemeral=True)
            log_text = f"[ERROR]  BAN: MissingRequiredArgument Error. User: {inter.author}"

        else:
            await inter.response.send_message("**ОШИБКА**: нет информации.", ephemeral=True)
            log_text = f"[ERROR]  BAN: unexpected Error. User: {inter.author}"
            print(error)


def setup(bot: commands.Bot):  
    bot.add_cog(BanCommand(bot))