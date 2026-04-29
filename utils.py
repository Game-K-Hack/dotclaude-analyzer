import os
import json
import datetime
from colorama import init, Fore, Back, Style

init()

log_level = "ok"
column_width = 10

def set_log_level(level: str) -> None:
    global log_level
    log_level = level

def log(level: str, text: str, only_get: bool = False) -> None | str:
    colors = {
        "input": { "b": Back.CYAN, "t": Fore.CYAN }, 
        "error": { "b": Back.RED, "t": Fore.RED }, 
        "warning": { "b": Back.YELLOW, "t": Fore.YELLOW }, 
        "info": { "b": Back.BLUE, "t": Fore.BLUE }, 
        "ok": { "b": Back.GREEN, "t": Fore.GREEN }, 
        "debug": { "b": Back.MAGENTA, "t": Fore.MAGENTA }, 
        "trace": { "b": Back.BLACK, "t": Fore.BLACK }, 
    }
    colors_keys = list(colors.keys())
    if not only_get and level not in colors_keys[:colors_keys.index(log_level)+1]:
        return None
    c = colors[level.lower().strip()]
    # Set color
    color = Style.DIM if c['b'] in [Back.GREEN, Back.CYAN] else Style.BRIGHT
    line = f"{color}{c['b']} | {level} "
    line += " " * (column_width - len(level))
    # Set date of log
    now = datetime.datetime.now()
    line += f"{Style.RESET_ALL}{Style.BRIGHT}{Back.LIGHTBLACK_EX} {now.strftime('%Y-%m-%d %H:%M:%S')} {Back.RESET}"
    # Message of log
    line += f"{c['b']} {Back.RESET}{Style.RESET_ALL} {c['t']}{text}"
    # Reset all format
    line += Fore.RESET + Back.RESET + Style.RESET_ALL
    if only_get: return line
    print(line)

def check_and_open(*args) -> str | dict | list | None:
    path = os.path.join(*args)
    if os.path.exists(path):
        with open(path, "r", encoding="utf8") as f:
            content = f.read()
            content =  json.loads(content) if "{" in content or "[" in content else content
            log("debug", f"Le fichier \"{os.path.basename(path)}\" a été chargé")
            return content
    else:
        log("warning", f"Le fichier \"{os.path.basename(path)}\" n'a pas été trouvé")
        return None
    
def get_info_from_project(path: str, data: dict[str, list|dict] | None = None) -> dict[str, list|dict]:
    if data is None:
        data = {"data": [], "tool-results": [], "memory": [], "meta": {}}
    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path, name)):
            data = get_info_from_project(os.path.join(path, name), data)
        else:
            if path.endswith("tool-results"):
                with open(os.path.join(path, name), "rb") as file:
                    data["tool-results"].append({ "name": name, "content": file.read() })
            else:
                with open(os.path.join(path, name), "r", encoding="utf8") as file:
                    content = file.read()
                    if path.endswith("memory"):
                        data["memory"].append({ "name": name, "content": content })
                    elif name.endswith(".meta.json"):
                        data["meta"][name.replace(".meta.json", "").replace("agent-", "")] = json.loads(content)
                    elif name.endswith(".jsonl"):
                        for i in content.split("\n"):
                            if len(i) > 0:
                                data["data"].append(json.loads(i))
    return data
