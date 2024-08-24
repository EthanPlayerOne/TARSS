import os
import subprocess
import yaml

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(text, color):
    print(f"{color}{text}{Colors.ENDC}")

def print_success(text):
    print_colored(text, Colors.OKGREEN)

def print_error(text):
    print_colored(text, Colors.FAIL)

def print_warning(text):
    print_colored(text, Colors.WARNING)


def print_banner():
    banner_color = Colors.FAIL
    print(f"{banner_color}________________  _________  _________ _________")
    print(f"{banner_color}\\__    ___/  _  \\\\______   \\/   _____//   _____/")
    print(f"{banner_color}  |    | /  /_\\  \\|       _/\\_____  \\ \\_____  \\ ")
    print(f"{banner_color}  |    |/    |    \\    |   \\/        \\/        \\ ")
    print(f"{banner_color}  |____|\\____|__  /____|_  /_______  /_______  / ")
    print(f"{banner_color}                \\/       \\/        \\/        \\/ {Colors.ENDC}")

def check_root():
    if os.geteuid() == 0:
        print("Настоятельно не рекомендуется выполнять скрипт от имени суперпользователя.")
        exit(3)

def get_current_pwd():
    return os.getcwd()

def print_menu():
    print(f"\nЧто вы хотите сделать?")
    print("1 - запустить полный сетап бота (первый запуск);")
    print("2 - поменять токен;")
    print("3 - поменять имя бота;")
    print("4 - изменить ID бота;")
    print("5 - изменить id мут-роли;")
    print("6 - изменить id приветственного канала;")
    print("7 - изменить путь к папке с логами.")

def get_action():
    return int(input("Что вы хотите сделать? (1-7): "))

def setup_bot():
    print("Спасибо, что выбрали нас! Будем рады звездочке на гитхабе, если Вам понравится :)")
    print("Приступим. Для начала убедитесь, что Вы находитесь в рабочей директории бота. Это важно.")
    print("Далее скрипт создаст необходимые директории и файлы для работы.")
    print("Вам так же будет предложено ввести токен Вашего бота, его название и айди, путь к папке с логами бота, а так же айди мут-роли на вашем сервере.")
    print("Их можно будет поменять в будущем, снова запустив этот скрипт.")

    token = input("Скопируйте токен бота (и убедитесь, что сзади никого нет ;) : ")
    bot = input("Как назовем вашего бота: ")
    id = input("Скопируйте user ID вашего бота: ")
    path = input("Скопируйте ПОЛНЫЙ путь к папке, куда будут литься логи (по умолчанию - текущая с подпапкой /logs): ")
    muteid = input("Введите id мут-роли: ")
    welcomeid = input("Введите id канала с сообщениями приветствия новых участников: ")

    print("Приступаю к установке...")

    print("Установка зависимостей...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"])

    if not path:
        path = os.path.join(os.getcwd(), "logs")
        os.makedirs(path, exist_ok=True)

    print("Создание config.yaml...")
    config_data = {
        "settings": {
            "token": token,
            "bot": bot,
            "id": id,
            "prefix": "",
            "status": "online",
            "path": path,
            "muted_role_id": muteid,
            "welcome_channel_id": welcomeid
        }
    }
    with open("config.yaml", "w") as config_file:
        yaml.dump(config_data, config_file)

    print("Создание config.py...")
    config_py_content = f"""
from yaml import load
from yaml.loader import SafeLoader

def get_config():
    with open('{os.getcwd()}/config.yaml', 'r') as f:
        return load(f, Loader=SafeLoader)
"""
    with open("config.py", "w") as config_py_file:
        config_py_file.write(config_py_content)

    print_success("Поздравляем, все прошло успешно!")
    print("Не забудте поставить роль бота выше всех остальных ролей.")
    print("Надеемся, что Вам понравится! :^)")
    exit(0)

def update_config(action):
    path = input("Введите ПОЛНЫЙ путь к конфигурационному файлу (config.yaml): ")
    if not os.path.isfile(path):
        print_error(f"Не удалось найти файл. ({path})")
        exit(4)

    with open(path, "r") as config_file:
        config_data = yaml.load(config_file, Loader=yaml.SafeLoader)

    if action == 2:
        token = input("Введите новый токен бота: ")
        config_data["settings"]["token"] = token
    elif action == 3:
        print_warning("ВНИМАНИЕ: эта переменная находится в конфигурационном файле и существует лишь для того, чтобы избежать путанницы.")
        print("Если Вы хотите переименовать бота, это необходимо сделать на DDP: https://discord.com/developers/applications/")
        bot = input("Введите новое имя бота: ")
        config_data["settings"]["bot"] = bot
    elif action == 4:
        id = input("Введите новый id бота: ")
        config_data["settings"]["id"] = id
    elif action == 5:
        muteid = input("Введите новый id мут-роли: ")
        config_data["settings"]["muted_role_id"] = muteid
    elif action == 6:
        welcomeid = input("Введите новый id канала с приветствиями: ")
        config_data["settings"]["welcome_channel_id"] = welcomeid
    elif action == 7:
        path2 = input("Введите новый путь к папке с логами: ")
        if not os.path.isdir(path2):
            print_error(f"Не удалось найти директорию. ({path2})")
            exit(4)
        config_data["settings"]["path"] = path2

    with open(path, "w") as config_file:
        yaml.dump(config_data, config_file)

    print_success("Успешно!")

def main():
    print_banner()
    print(f"\nДобро пожаловать! Приступим?")
    print()

    check_root()
    current_pwd = get_current_pwd()
    print(f"[INFO]  Текущая рабочая директория: {current_pwd}")

    print_menu()
    action = get_action()

    if action == 1:
        setup_bot()
    elif 2 <= action <= 7:
        update_config(action)
    else:
        print_error("Неверный выбор.")

if __name__ == "__main__":
    main()