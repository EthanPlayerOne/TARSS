#!/bin/bash

echo "________________  _________  _________ _________"
echo "\__    ___/  _  \\\______   \/   _____//   _____/"
echo "  |    | /  /_\  \|       _/\_____  \ \_____  \ "
echo "  |    |/    |    \    |   \/        \/        \ "
echo "  |____|\____|__  /____|_  /_______  /_______  / "
echo "                \/       \/        \/        \/ "
# не ржать, так надо из за символов \\\


echo Добро пожаловать! Приступим?
echo 

if [ "$UID" -eq 0 ]; then
    echo "Настоятельно не рекомендуется выполнять скрипт от имени суперпользователя."  # ну мало ли )
    exit 3
fi

currentpwd="$PWD"
echo "[INFO]  Текущая рабочая директория: $currentpwd "

echo "Что вы хотите сделать? 
1 - запустить полный сетап бота (первый запуск);
2 - поменять токен;
3 - поменять имя бота; 
4 - изменить ID бота; 
5 - изменить id мут-роли;
6 - изменить id приветственного канала;
7 - изменить путь к папке с логами."
read -p "Что вы хотите сделать? (1-7): " action


if [ "$action" -eq 1 ]; then
    echo ""  # да
    echo "Спасибо, что выбрали нас! Будем рады звездочке на гитхабе, если Вам понравится :)
Приступим. Для начала убедитесь, что Вы находитесь в рабочей директории бота. Это важно.
Далее скрипт создаст необходимые директории и файлы для работы.
Вам так же будет предложено ввести токен Вашего бота, его название и айди, путь к папке с логами бота, а так же айди мут-роли на вашем сервере.
Их можно будет поменять в будущем, снова запустив этот скрипт."
    
    read -p "Скопируйте токен бота (и убедитесь, что сзади никого нет ;) : " token
    read -p "Как назовем вашего бота: " bot
    read -p "Скопируйте user ID вашего бота: " id
    read -p "Скопируйте ПОЛНЫЙ путь к папке, куда будут литься логи (по умолчанию - текущая с подпапкой /logs): " path
    read -p "Введите id мут-роли: " muteid
    read -p "Введите id канала с сообщениями приветствия новых участников: " welcomeid
    echo "Приступаю к установке..."
    
    echo "Установка зависимостей..."
    pip install -r requirements.txt

    if [ ${#path} -eq 0 ]; then
        path="$(pwd)/logs"
        mkdir $(pwd)/logs
    fi

    echo "Создание config.yaml..."
    touch config.yaml 
    cat << EOF > config.yaml
settings:
    token: "$token" 
    bot: "$bot"
    id: $id
    prefix: ""  # не необходимо  
    status: online  # не необходимо
    path: $path
    muted_role_id: $muteid
    welcome_channel_id: $welcomeid
EOF
    mkdir $path

    echo "Создание config.py..."
    touch config.py
    cat << EOF > config.py

from yaml import load
from yaml.loader import SafeLoader

def get_config():
    with open('$currentpwd/config.yaml', 'r') as f:
        return load(f, Loader=SafeLoader)
EOF

    echo "Поздравляем, все прошло успешно!
Не забудте поставить роль бота выше всех остальных ролей. 
Надеемся, что Вам понравится! :^)"
    exit 0
fi


if [ "$action" -eq 2 ]; then
    read -p "Введите ПОЛНЫЙ путь к конфигурационному файлу (config.yaml): " path
    read -p "Введите новый токен бота: " token
    echo "..."

    if [ ! -f "$path" ]; then
        echo "Не удалось найти файл. ($path)"
        exit 4
    fi

    newtoken="    token: \"$token\""
    sed -i "2s/.*/$newtoken/" $path
    echo "Успешно!" 
fi

if [ "$action" -eq 3 ]; then
    echo "ВНИМАНИЕ: эта переменная находится в конфигурационном файле и существует лишь для того, чтобы избежать путанницы.
Если Вы хотите переименовать бота, это необходимо сделать на DDP: https://discord.com/developers/applications/ "
    read -p "Введите ПОЛНЫЙ путь к конфигурационному файлу (config.yaml): " path
    read -p "Введите новое имя бота: " bot
    echo "..."

    if [ ! -f "$path" ]; then
        echo "Не удалось найти файл. ($path)"
        exit 4
    fi

    newbotname="    bot: \"$bot\""
    sed -i "3s/.*/$newbotname/" $path
    echo "Успешно!" 
fi

if [ "$action" -eq 4 ]; then
    read -p "Введите ПОЛНЫЙ путь к конфигурационному файлу (config.yaml): " path
    read -p "Введите новый id бота: " id
    echo "..."

    if [ ! -f "$path" ]; then
        echo "Не удалось найти файл. ($path)"
        exit 4
    fi
    newid="    id: $id"
    sed -i "4s/.*/$newid/" $path
    echo "Успешно!"
fi

if [ "$action" -eq 5 ]; then
    read -p "Введите ПОЛНЫЙ путь к конфигурационному файлу (config.yaml): " path
    read -p "Введите новый id мут-роли: " muteid
    echo "..."

    if [ ! -f "$path" ]; then
        echo "Не удалось найти файл. ($path)"  # "я уже говорил тебе, что такое безумие?..." 
        exit 4                                 # да простят меня труъшные скриптоделы, но я не осилил.
    fi                                         # если могете и если желание будет можете оформить в функцию и открыть pull request. спасибо за понимание

    newmuteid="    muted_role_id: $muteid"    
    sed -i "8s/.*/$newmuteid/" $path
    echo "Успешно!"
fi


if [ "$action" -eq 6 ]; then
    read -p "Введите ПОЛНЫЙ путь к конфигурационному файлу (config.yaml): " path
    read -p "Введите новый id канала с приветствиями: " id
    echo "..."

    if [ ! -f "$path" ]; then
        echo "Не удалось найти файл. ($path)"
        exit 4
    fi

    newwelcomeid="    welcome_channel_id: $id"
    sed -i "9s/.*/$newwelcomeid/" $path
    echo "Успешно!"
fi

if [ "$action" -eq 7 ]; then
    read -p "Введите ПОЛНЫЙ путь к конфигурационному файлу (config.yaml): " path
    read -p "Введите новый путь к папке с логами: " path2
    echo "..."

    if [ ! -f "$path" ]; then
        echo "Не удалось найти файл. ($path)"
        exit 4   
    fi
    if [ ! -d "$path2" ]; then
        echo "Не удалось найти директорию. ($path2)"
        exit 4   
    fi

    newlogpath="    path: $path2"
    sed -i "7s#.*#$newlogpath#" "$path"  # не спрашивайте
    echo "Успешно!"
fi

