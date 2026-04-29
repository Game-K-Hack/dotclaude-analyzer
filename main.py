import os
import sys
import json
from utils import log, Style, check_and_open, set_log_level, get_info_from_project


if "-v" in sys.argv:
    set_log_level("debug")
elif sum([1 if ("-v" + ("v" * i) in sys.argv) else 0 for i in range(1, 51)]) > 0:
    set_log_level("trace")

input_path = input(log("input", f"Chemin vers le dossier \".claude\" {Style.DIM}(laisser vide pour prendre le chemin par défaut){Style.NORMAL}: ", only_get=True) + Style.BRIGHT)
print(Style.NORMAL, end="\r")

if len(input_path) == 0:
    current_claude_path = os.path.join(os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"))
    if ".claude" in os.listdir(current_claude_path):
        claude_path = os.path.join(current_claude_path, ".claude")
    else:
        log("error", "Dossier \".claude\" par défaut non trouvé.")

elif os.path.exists(input_path):
    if input_path.replace("/", "").replace("\\", "").endswith(".claude"):
        claude_path = input_path
    else:
        if ".claude" in os.listdir(input_path):
            claude_path = os.path.join(input_path, ".claude")
        else:
            log("error", "Dossier \".claude\" non trouvé.")
            quit()

else:
    log("error", "Le chemin n'existe pas.")
    quit()

log("info", f"Chemin correct: {Style.BRIGHT}{claude_path}{Style.NORMAL}")

sep = "/" if "/" in claude_path else "\\"
_claude_path = sep.join(claude_path.split(sep)[:-1])
claude = check_and_open(_claude_path, ".claude.json")

credentials = check_and_open(claude_path, ".credentials.json")
mcp_needs_auth_cache = check_and_open(claude_path, "mcp-needs-auth-cache.json")
settings = check_and_open(claude_path, "settings.json")

backups: list[dict] = []
for filename in os.listdir(os.path.join(claude_path, "backups")):
    with open(os.path.join(claude_path, "backups", filename)) as file:
        content = json.load(file)
    comp = filename.split(".")
    backups.append({ "timestamp": comp[4], "content": content })
    log("trace", f"Le fichier backups \"{filename}\" a été chargé")
log("debug", "Tous les fichiers du dossier backups ont été chargé")

file_history: list[dict] = []
for dirname in os.listdir(os.path.join(claude_path, "file-history")):
    for filename in os.listdir(os.path.join(claude_path, "file-history", dirname)):
        with open(os.path.join(claude_path, "file-history", dirname, filename), "r", encoding="utf8") as file:
            content = file.read()
        idfile, version = filename.split("@v")
        file_history.append({ "id": idfile, "version": version, "content": content })
        log("trace", f"Le fichier file-history \"{filename}\" a été chargé")
    log("trace", f"Dossier file-history \"{dirname}\" a été chargé")
log("debug", "Tous les dossiers et fichiers du dossier file-history ont été chargé")

shell_snapshots: list[dict] = []
for filename in os.listdir(os.path.join(claude_path, "shell-snapshots")):
    with open(os.path.join(claude_path, "shell-snapshots", filename), "r", encoding="utf8") as file:
        content = file.read()
    comp = filename.split(".")[0].split("-")
    shell_snapshots.append({ "id": comp[3], "timestamp": comp[2], "content": content })
    log("trace", f"Le fichier shell-snapshots \"{filename}\" a été chargé (id:{comp[3]})")
log("debug", "Tous les fichiers du dossier shell-snapshots ont été chargé")

projects: list[dict] = {}
for projectname in os.listdir(os.path.join(claude_path, "projects")):
    projects[projectname] = get_info_from_project(os.path.join(claude_path, "projects", projectname), None)
    log("trace", f"Projet \"{projectname}\" a été chargé")
log("debug", "Tous les dossiers et fichiers du dossier projects ont été chargé")

log("ok", "Tous les fichiers ont été chargé")

def json_serial(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='ignore') # Convert bytes to string
    raise TypeError(f"Type {type(obj)} not serializable")

with open("data.json", "w", encoding="utf8") as file:
    # Use the 'default' parameter to call our helper
    file.write(json.dumps(projects, indent=4, default=json_serial))
