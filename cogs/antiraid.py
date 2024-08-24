import asyncio
from collections import deque
import disnake
from disnake.ext import commands
from update_log import update_log
from config import get_config, get_ignore_antiraid_ids 

config = get_config()
ign_channels = get_ignore_antiraid_ids()


class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_cache = {}  # кэш сообщений, бот должен видеть все каналы

    @commands.Cog.listener()
    async def on_message(self, message):
        welcome = disnake.utils.get(message.guild.channels, id=config["settings"]["welcome_channel_id"])
        if message.author.bot:
            return

        guild_id = message.guild.id  # я тестил :^) вроде работает
        user_id = message.author.id


        if guild_id not in self.message_cache:
            self.message_cache[guild_id] = {}  # создаем пустой кэш для пользователя
        if user_id not in self.message_cache[guild_id]:
            self.message_cache[guild_id][user_id] = deque(maxlen=7)

        self.message_cache[guild_id][user_id].append(message)

        if len(self.message_cache[guild_id][user_id]) >= 7:
            messages = list(self.message_cache[guild_id][user_id])

            if all((message.created_at - messages[0].created_at).total_seconds() <= 7 for message in messages):
                muted_role = message.guild.get_role(config["settings"]["muted_role_id"])
                await message.author.add_roles(muted_role)
                try:
                    await asyncio.gather(*(message.delete() for message in messages))
                except disnake.errors.NotFound:
                    pass  # я не знаю как это исправить пока так просто глушить

                await message.author.send("**Вы были заблокированы за спам.** Это часто случается из-за того, что вы слишком быстро отправляете сообщения.\n Если вы считаете, что произошла ошибка, напишите `@ethanplayerone` за размутом.")
                log_text=f"[WARNING]    RAID DETECDED! Possible raiders: {message.author}"
                update_log(log_text)
    
        channel = message.channel
        if channel in ign_channels:
            return

        messages = await channel.history(limit=6).flatten()

        if len(messages) == 6 and all(m.content == messages[0].content for m in messages):
            role = disnake.utils.get(message.guild.roles, id=config["settings"]["muted_role_id"])
            try:
                await message.author.add_roles(role)
            except AttributeError:
                pass
                
            await channel.purge(limit=9)  # с рассчетом на задержку. оно того стоит, поверьте
            await channel.send(f"**Сработала анти-рейд защита.** В случае ошибки обратитесь к модераторам.")
            log_text = f"[WARNING]  RAID DETECTED! Possible raiders: {message.author}"
            update_log(log_text)
            print(log_text)
        await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(AntiRaid(bot))
