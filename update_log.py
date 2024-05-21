from config import get_config  
import time
config = get_config()

def update_log(log_text): 
    seconds = time.time() 
    currentTime11 = time.localtime(seconds)

    latest = open(f'{config["settings"]["pass"]}/latest.log', 'a')  
    try:
        latest.write(f"[{time.asctime(currentTime11)}]     " + log_text + f"\n")  # ага
    finally:
        latest.close()

    main = open(f'{config["settings"]["pass"]}/main.log', 'a')
    try: 
        main.write(f"[{time.asctime(currentTime11)}]     " + log_text + f"\n")
    finally:
        main.close()