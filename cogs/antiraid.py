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
        if message.author.bot:
            return

        guild_id = message.guild.id  # я тестил :^) вроде работает
        user_id = message.author.id


        if guild_id not in self.message_cache:
            self.message_cache[guild_id] = {}  # создаем пустой кэш для пользователя
        if user_id not in self.message_cache[guild_id]:
            self.message_cache[guild_id][user_id] = deque(maxlen=8)  # на всякий

        self.message_cache[guild_id][user_id].append(message)

        if len(self.message_cache[guild_id][user_id]) >= 6:
            messages = list(self.message_cache[guild_id][user_id])

            if all((message.created_at - messages[0].created_at).total_seconds() <= 12 for message in messages):
                role = disnake.utils.get(message.guild.roles, id=int(config["settings"]["muted_role_id"]))
                await message.author.add_roles(role)
                try:
                    await asyncio.gather(*(message.delete() for message in messages))
                except disnake.errors.NotFound:
                    pass  # я не знаю как это исправить пока так просто глушить. я хз что это, все работает как надо

                await message.author.send("**Вас замутили.** Это часто случается из-за того, что вы слишком быстро отправляете сообщения.\n Если вы считаете, что произошла ошибка, напишите администраторам/модераторам сервера за размутом.")
                log_text=f"[WARNING]    RAID DETECDED! Possible raiders: {message.author}"
                update_log(log_text)
    
        channel = message.channel
        if channel in ign_channels:
            return

        messages = await channel.history(limit=7).flatten()

        if len(messages) == 7 and all(m.content == messages[0].content for m in messages):
            role = disnake.utils.get(message.guild.roles, id=int(config["settings"]["muted_role_id"]))
            await message.author.add_roles(role)
            await channel.purge(limit=9)  # с рассчетом на задержку. оно того стоит, поверьте
            await channel.send(f"**Сработала анти-рейд защита.** В случае ошибки обратитесь к модераторам.")
            log_text = f"[WARNING]  RAID DETECTED! Possible raiders: {message.author}"
            update_log(log_text)
            print(log_text)
        await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(AntiRaid(bot))

'''
Я знаю, что можно лучше, и на этом я останавливаться не собираюсь. Уверен, что одаренные челы найдут лазейки, 
поэтому я щас таких ищу по всему дискорду. А если вы сами найдете лазейку, напишите об этом мне (@zephyr.30 в дисике), я закрою
любую дыру в ближайшее время. 
Ну, а если вы герой, котроый знает как испрвить такую дыру или дажу уже сделал это, я буду раз увидеть ваш Pull Request,
и если все будет ок, то ваше имя обязательно засветится в списке контрибьюторов. Спасибо всем заранее <3

ЧТО Я ТЕСТИЛ:
- спам в один канал очень быстро рандомными/одинаковыми сообщениями 
- спам в один канал одинаковыми сообщениями с периодичностью в минуту между сообщениями
- спам одинаковыми сообщениями в разных каналах (наверное самый распространенный вид спама в дисике)

ЧТО Я НЕ ТЕСТИЛ:
- много одинаковых сообов от разных челов в одном канале
- много одинаковых сообов от вебхуков/ботов
- много разных сообщений от разных челов где угодно

Короче говоря, в боевых условиях крупного сервера он себя еще показать не успел, ибо крупных серверов у меня нет...
Буду рад вашему фидбеку если вы его протестите, у меня лапки :))
'''
