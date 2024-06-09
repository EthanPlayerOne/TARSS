import disnake
from disnake.ext import commands
import time
from update_log import update_log

from config import get_config  
"""
config нет в репозитории. сорян.
В общем случае, суть в том, чтобы открыть .yaml файл с токеном, префиксом, 
айди, и прочими конфигурационными параметрами. 
Если вы, так же как и я, используете yaml для хранения этих данных,
то сначала надо его импортировать:

from yaml import load
from yaml.loader import SafeLoader

И как обычно открыть файл:

def get_config():
    with open('ПОЛНЫЙ/путь/к/вашему/файлу/config.yaml', 'r') as f:
        return load(f, Loader=SafeLoader)

Самого yaml файла тоже нет, его структуру рекомендую погуглить. Там все
очень просто и очень прикольно.

Пример использования ямла можете найти в update_log.py. 
"""

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
"""
Две переменных ниже обязательно поменять на свои перед запуском! (см. условия использования в README)
"""
welcome_channel_id = 1168249842863194272  # этот канал будет игнорироваться в антирейде, и в него будут поступать сообщения о новых участниках
muted_role_id = 1205580212977279067


"""COGS"""
bot.load_extension("cogs.banuser")
bot.load_extension("cogs.ping")
bot.load_extension("cogs.clear")
bot.load_extension("cogs.kickuser")


@bot.slash_command(name="reload", description="Перезагрузить ког.")
@commands.has_guild_permissions(administrator=True)
async def reload(inter: disnake.ApplicationCommandInteraction, rcog:str):
    if rcog == 'all':
        for c in bot.cogs:
            bot.unload_extension(c)
            bot.load_extension(c)
        log_text=f"[INFO]  RELOAD: All cogs was reloaded by {inter.author}"
    
    else:
        cog=f"cogs.{cog}"
        bot.get_cog(cog)
        bot.unload_extension(cog)
        bot.load_extension(cog)
        await inter.response.send_message(f"Ког {cog} был успешно перезапущен.")
        log_text=f"[INFO]  RELOAD: Cog {cog} was reloaded by {inter.author}."

    update_log(log_text)

@reload.error
async def reload_error(inter:disnake.ApplicationCommandInteraction, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await inter.response.send_message(f"**ОШИБКА:** указанный ког не найден.")
        log_text=f"[ERROR]  RELOAD: Cog not found."
        
    if isinstance(error, commands.MissingPermissions):
        await inter.response.send_message(f"**ОШИБКА:** недостаточно прав для выполнения операции перезагрузки.")
        log_text=f"[ERROR]  RELOAD: MissingPermissions Error. User: {inter.author}"
    update_log(log_text=log_text)


@bot.event
async def on_ready():
    seconds = time.time() 
    currentTime = time.localtime(seconds)
    
    await bot.change_presence(status=dnd, activity=activity)  
    log_text = f'[{time.asctime(currentTime)}] \nLogged in as {bot.user.name} sucsessfuly! \nID: {config["settings"]["id"]}. \nCurrent status: {config["settings"]["status"]}. \n\n'
    print(log_text) 

    log = open(f'{config["settings"]["pass"]}/latest.log', 'w')  # тут мы переоткрываем latest лог, чтобы он был реально latest. в основном логфайле все как надо
    try:
        log.write(log_text)
    finally:
        log.close()


@bot.event
async def on_member_join(member):
    if member.bot:
        update_log(f"[WARNING]  Detected attempt to join bot to server: {member}") 
        print("Попытка добавить бота на сервер!")
        await member.kick(reason="Подозрение на бота. Если возникла ошибка, обратитесь к `@ethanplayerone`.")
    else:
        welcome = disnake.utils.get(member.guild.channels, id=welcome_channel_id)
        embed=disnake.Embed(title=f'{member.name}, добро пожаловать на сервер!', description='МП - уникальный проект, где ты обязательно найдешь себе место.', color=0x1a5fb4)
        embed.set_author(name='МыжПрограммисты |МП | Open Beta', icon_url='https://cdn.discordapp.com/icons/1143119676726059089/63c4bda8ff64c01fcbddec1ce1c05b43.webp?size=100')
        embed.set_thumbnail(url='https://cdn.discordapp.com/icons/1143119676726059089/63c4bda8ff64c01fcbddec1ce1c05b43.webp?size=100')
        embed.add_field(name='<#1143121715665313902>', value='Рекомендуем прочитать правила.', inline=True)
        embed.add_field(name='<#1143119677229383692>', value='Енто наша главная чатилка!', inline=True)
        embed.set_footer(text='Made by @ethanplayerone with love')  # эту строчку не менять! (см. условия использования в README)
        await welcome.send(embed=embed)

        update_log(f"[INFO]  {member} joined.")
        pass  # работает - не трогай. (С)           если есть идеи получше - делайте как считаете нужным

"""
Настоятельно рекомендуется сделать свой ембед, чтобы не было как штампом отмечено с Тарсса.
Чтобы не запариваться с эмбедом, рекомендую использовать этот классный генератор:
https://cog-creators.github.io/discord-embed-sandbox/
"""

@bot.event
async def on_message(message):
    welcome = disnake.utils.get(message.guild.channels, id=welcome_channel_id)
    if message.author.bot:  
        return
    channel = message.channel  # позуй)
    if channel == welcome:
        return

    messages = await channel.history(limit=6).flatten()

    if len(messages) == 6 and all(m.content == messages[0].content for m in messages):
        role = disnake.utils.get(message.guild.roles, id=muted_role_id)
        try:
            await message.author.add_roles(role)
        except AttributeError:
            pass
            
        await channel.purge(limit=6)
        await channel.send(f"**Сработала анти-рейд защита.** В случае ошибки обратитесь к модераторам.")
        log_text = f"[WARNING]  RAID DETECTED! Possible raiders: {message.author}."
        update_log(log_text)
        print(log_text)
    await bot.process_commands(message)

"""
Я ЗНАЮ НАСКОЛЬКО ЭТО НЕКРУТО,
но если я пытаюсь придумать и реализовать что-то понадежнее и эффективнее
ничего хорошего не получается, хотя я понимаю, что анти-рейд это должна быть
одна из самых основных функций бота, нормальный рабочий метод был безвозвратно 
утерян, и в связи с отсутствием времени на разработку нового я прошу вас
меня простить, и, если у вас есть идеи по улучшению защиты от рейдов
я буду очень рад если вы предложите мне в дискорд в лс (@ethanplayerone) или 
откроете pull request которому я тоже буду безмерно рад и благодарен. 

Такие дела. 
Обнял, приподнял,
Ита
"""

bot.run(config["settings"]["token"])
