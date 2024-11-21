# TARSS
## Введение
Добро пожаловать! Ты читаешь документацию проекта TARSS - Tony's Anti-Raid Security System - самого надежного и безопасного бота в стиле "сделай-сам", который сделает ваш любимый сервер чуть-чуть безопаснее. Весь проект был написан с нуля энтузиастом `@zephyr30` (Discord). В отличии от других анти-рейд ботов Тарсс предоставляется "как есть", полностью с исходным кодом, для личного использования. Вы можете спокойно изменять код, дополнять его (см. усл. использования в конце) и делать его еще лучше :)

## Коротко о главном
### Структура бота
Структура бота представляет из себя:
- конфигурационный файл;
- скрипт для чтения конфигурационного файла;
- директория с логами;
- скрипт для записи логов в файлы;
- директория с когами*;
- основной файл main;
- установочный скрипт (setup).

Конфигурационный файл содержит в себе необходимые переменные для запуска бота (токен, айди некоторых каналов, мут-роли, и т.п.). Его заполнение осуществляется с помощью setup файла.

**! О мут-роли:** рекомендуется создать эту роль c правами по умолчанию, и добавить ее в права каждой категории сервера и запретить отправлять сообщения, ствить реакции, подключаться к войсам и т.д.. у меня работает :^)

**! О канале с приветствиями:** в этот канал будут поступать сообщения о прибывших на сервер участниках. В этот же канал должны поступать _системные_ сообщеиня о новых участниках. Это нужно, чтобы бот игнорировал этот канал и не считал, что 10 сообщений подряд в нем - это рейд.

**! Об Intents:** так как бот авторизируется на сервере как администратор, по мимо того, что его роль должна быть выше остальных, также необходимо включить поставить галки везде в пунктах _Privileged Gateway Intents_ во вкладке _Bot_ вашего бота.

! * [Про коги](https://docs.disnake.dev/en/stable/ext/commands/cogs.html#cogs)


### Про анти-рейд
Системка довольно простая, но эффективная.
При запуске бот создает кеш в виде словаря, в котором хранится информация о сообщениях каждого участника. Каждое новое сообещние, бот проверяет, не переполнен ли кеш (макс. 5 вхождений для 1 пользователя) и, если да, то проверяет дату создания сообщений. Если эти 5 сообщений были созданы менее чем с перерывом в 8 секунд, то он их удаляет и выдает участнику мут. С такой скоростью печатают только рейдеры.

Еще одна ступень защиты, простая, как столб, но не менее эффективная. 
Бот проверяет последние 5 сообщений в канале, и, если они одинаковые, то удаляет их. 
Звучит просто? Да. Правильно ли с точки зрения морали? не очень...))
Дело в том, что вторая ступень иногда работает не совсем так, как хотелось бы. На некоторых серверах присутствуют, например, каналы с мемами, и, если отправлять их без контекста, даже пачками с разным количеством мемов, когда их накопится 5 штук и никто ничего в канал не напишет, бот выдаст мемным поставщикам мут. 
Не знаю как, но это будет исправлено в грядущих версиях.

### Built-in команды
Тут все в общем просто:
- `/banuser` - забанить участника. Ког - `ban`
- `/kickuser` - выгнать участника. Ког - `kick`
- `/clear [amonut]` - очистить [amount] сообщений в текущем канале. Ког - `clear`
- `/reload_cog [cog]` - перезагрузить определенный ког. Ког - `reload`
- `/ping` - пинг бота в мс. Ког - `ping`

TODO - команда `/mute` чтобы вручную мутить пользователей.
## Установка

### Linux
Перейдите в рабочую директорию Вашего бота. 
```
git clone https://github.com/EthanPlayerOne/TARSS
cd TARSS/
python3 setup.py
```
Следуйте инструкциям в скрипте. 
Обратите внимание, что иногда для корректной установки всех зависимостей pip требует наличие среды в текущей папке, если pip не установил зависимости, попробуйте создать env и попробовать еще раз. Так же можно установить зависимости вручную:
```
pip install disnake pyyaml --break-system-packages
```

__Рекомендуется [создать свой embed](https://cog-creators.github.io/discord-embed-sandbox) для приветствия новых участников (см. `main.py`)__
После успешной установки, запустите файл где-нибудь в терминале: `python3 main.py`

### Windows
Установочный скрипт еще не тестировался на Windows, но в теории он должен работать на Windows 10 и выше. Если вы используете винду, пожалуйста, оставьте фидбек мне в лс в дискорд: `@zephyr30`. Буду очень вам признателен!

## Я нашел ошибку! / У меня что-то не работает!
Если у вас есть предложения по улучшению или вы нашли какой-то баг, вы можете открыть [issue](https://github.com/EthanPlayerOne/TARSS/issues/new/choose) (если что-то сломалось и вы не знаете как это чинить) или [pull request](https://github.com/EthanPlayerOne/TARSS/compare) (если вы уже знаете как починить или починили), и я обязательно рассмотрю эту проблему в течении нескольких дней.
# УСЛОВИЯ ИСПОЛЬЗОВАНИЯ
TARSS - бот для Discord, разработанный @zephyr30 (Discord) распространяется как открытый исходный код. Бот предназначен для использования на ОДНОМ сервере; это значит, что бот "запилен" под каждый отдельный сервер и привязан к айди некоторых каналов/ролей. 
Исходным (коренным) репозиторием является TARSS (https://github.com/EthanPlayerOne/TARSS).
Копиируя и используя этот код в своих проектах (ботах) публикуя их исходный код, Вы обязуетесь:
- распространять Ваш проект так же с открытым исходным кодом;
- придерживаться комментариев в коде, ссылающихся на данный документ;
- использовать Вашего бота только на ОДНОМ сервере (запретить добавлять его на другие всяким способом через Discord Developer Portal);
- для пункта выше: допускается использования приватных тестовых серверов.
- применять все те же условия использования к своему проекту; допускается дополнение условий новыми пунктами, не пересекающими условия использования исходного (коренного) репозитория;

Разработчик и владелец коренного (исходного) репозитория снимает с себя ответственность за любой ущерб, вызванный некорректным, необдуманным, неграмотным, или не соответствующим условиям использования кодом.
Допускается обновление условий использования в исходном (коренном) репозитории (https://github.com/EthanPlayerOne/TARSS), в этом случае условия использования, распространяющиеся на Ваш проект тоже должны быть обновлены в соответствии с обновленной версией условий настоящего репозитория.  
Допускается дополнение условий использование в Вашем проекте в соответствии с Вашими нуждами. 
