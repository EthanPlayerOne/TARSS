import disnake
from disnake.ext import commands
import time
from update_log import update_log

from config import get_config  

seconds = time.time() 
currentTime11 = time.localtime(seconds)
print(f'[{time.asctime(currentTime11)}]   STARTING...\n')

intents = disnake.Intents.all()  # берем интенты
intents.message_content = True  # и чтоб реагировал на сообщения ставим это 
bot = commands.Bot(command_prefix="_", intents=intents)  
config = get_config()  # получаем переменную с конфигом
idle = disnake.Status.idle
activity = disnake.Activity(type=disnake.ActivityType.watching, name="за порядком")
dnd = disnake.Status.dnd


"""COGS"""
bot.load_extension("cogs.ban")
bot.load_extension("cogs.ping")
bot.load_extension("cogs.clear")
bot.load_extension("cogs.kick")
bot.load_extension("cogs.reload")
bot.load_extension("cogs.antiraid")

@bot.event
async def on_ready():
    seconds = time.time() 
    currentTime = time.localtime(seconds)
    
    await bot.change_presence(status=dnd, activity=activity)  
    log_text = f'[{time.asctime(currentTime)}] \nLogged in as {bot.user.name} sucsessfuly! \nID: {config["settings"]["id"]}. \nCurrent status: {config["settings"]["status"]}. \n\n'
    print(log_text) 

    log = open(f'{config["settings"]["path"]}/latest.log', 'w')  # тут мы переоткрываем latest лог, чтобы он был реально latest. в основном логфайле все как надо
    try:
        log.write(log_text)
    finally:
        log.close()


@bot.event
async def on_member_join(member):
    if member.bot:
        update_log(f"[WARNING]  Detected attempt to join bot to server: {member}") 
        print("Попытка добавить бота на сервер!")
        await member.kick(reason="Подозрение на бота. Если возникла ошибка, обратитесь к администрации.") 
    else:
        welcome = disnake.utils.get(member.guild.channels, id=config["settings"]["welcome_channel_id"])
        embed=disnake.Embed(title=f'{member.name}, добро пожаловать на сервер!', description='Рады тебя видеть!', color=0x1a5fb4)
        embed.set_author(name='Название сервера', icon_url='иконка сервера')
        embed.set_thumbnail(url='еще иконка какая нибудь')
        embed.add_field(name='что нибудь', value='Это наше "что-нибудь"!', inline=True)
        embed.add_field(name='текст', value='а это очень крутой текст!', inline=True)
        embed.set_footer(text='Made by @zephyr30 with love')  # эту строчку не менять! (см. условия использования в README)
        await welcome.send(embed=embed)

        update_log(f"[INFO]  {member} joined.")
        pass  # работает - не трогай. (С)           если есть идеи получше - делайте как считаете нужным

"""
Настоятельно рекомендуется сделать свой ембед, чтобы да.
Чтобы не запариваться с эмбедом, рекомендую использовать этот классный генератор:
https://cog-creators.github.io/discord-embed-sandbox/
"""

if __name__ == "__main__":
    bot.run(config["settings"]["token"])  #      #якрутой - 1: юзаю входную точку
