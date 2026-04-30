import os
import sys
import json
import datetime
from utils import log, Style, check_and_open, set_log_level, get_info_from_project, json_serial


if "-v" in sys.argv or "--v" in sys.argv:
    set_log_level("debug")
elif sum([1 if ("-v" + ("v" * i) in sys.argv) else 0 for i in range(1, 51)]) > 0 or sum([1 if ("--v" + ("v" * i) in sys.argv) else 0 for i in range(1, 51)]) > 0:
    set_log_level("trace")

# input_path = input(log("input", f"Chemin vers le dossier \".claude\" {Style.DIM}(laisser vide pour prendre le chemin par défaut){Style.NORMAL}: ", only_get=True) + Style.BRIGHT)
input_path = ""
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
        idfile, version = filename.split("@v")
        file_history.append({ "id": idfile, "version": version, "path": os.path.join(claude_path, "file-history", dirname, filename) })
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

projects: dict = {}
for projectname in os.listdir(os.path.join(claude_path, "projects")):
    projects[projectname] = get_info_from_project(os.path.join(claude_path, "projects", projectname), None)
    log("trace", f"Projet \"{projectname}\" a été chargé")
log("debug", "Tous les dossiers et fichiers du dossier projects ont été chargé")

log("ok", "Tous les fichiers ont été chargé")



# with open("data.json", "w", encoding="utf8") as file:
#     file.write(json.dumps(projects, indent=4, default=json_serial))

# log("info", "Liste des projets:")
# for index, project in enumerate(projects.keys()):
#     log("info", f"    {index+1}) {project}")
# index = input(log("input", "Choisisser un projet à exporter: ", only_get=True) + Style.BRIGHT)
# print(Style.NORMAL, end="\r")

# export = {}
# p = list(projects.keys())[int(index)-1]
# datas = projects[p]["data"]
# for data in datas:
#     # filtrer les fichiers
#     if "type" in data.keys() and data["type"] == "file-history-snapshot":
#         # récupérer les fichiers
#         files = data["snapshot"]["trackedFileBackups"]
#         # pour tous les fichiers trouvés
#         for path in files.keys():
#             # vérifier si le fichier est plus récent
#             file_ts = datetime.datetime.strptime(files["backupTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
#             if file_ts > export[path]:




#         paths = data["snapshot"]["trackedFileBackups"].keys()
#         for path in paths:
#             d = data["snapshot"]["trackedFileBackups"][path]
#             ts = datetime.datetime.strptime(d["backupTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
#             if (path not in files.keys() or files[path] < ts) and "backupFileName" in d.keys():
#                 print(d)
#                 file_path = os.path.realpath(os.path.join("export", path))
#                 os.makedirs(os.path.dirname(file_path), exist_ok=True)
#                 with open(file_path, "wb") as file:
#                     with open(d["path"], "rb") as original:
#                         file.write(original.read())
#                         files[path] = ts
#                         log("trace", f"Fichier \"{file_path}\" créé")
#             else:
#                 log("trace", f"Fichier \"{file_path}\" non enregistré, une version plus récente existe déjà.")
# log("debug", f"Tous les fichiers du projet \"{p}\" ont été exporté.")



# with open("data.json", "w", encoding="utf8") as file:
#     file.write(json.dumps(projects[list(projects.keys())[int(index)-1]], indent=4, default=json_serial))



claude = {}
cache = {}
for project in projects:
    claude[project] = {}

    for data in projects[project]["data"]:

        if data["type"] == "file-history-snapshot":
            uuid = data["snapshot"]["messageId"]
            if uuid not in cache.keys():
                cache[uuid] = {}

            for filepath in data["snapshot"]["trackedFileBackups"]:
                detail = data["snapshot"]["trackedFileBackups"][filepath]
                if filepath not in cache[uuid].keys():
                    cache[uuid][filepath] = []
                cache[uuid][filepath].append(detail)

        else:
            sid = data["sessionId"]
            if sid not in claude[project].keys():
                claude[project][sid] = {}

            match data["type"]:
                case "user":
                    pass
                case "ai-title":
                    claude[project][sid]["title"] = data["aiTitle"]
                case "assistant":
                    claude[project][sid][uuid] = data
                case "last-prompt":
                    pass

    for uuid in cache:
        for session_id in claude[project]:
            if uuid in claude[project][session_id].keys():
                # anti doublon
                t: dict[str, list] = {}
                for path in cache[uuid]:
                    t[path] = []
                    for detail in cache[uuid][path]:
                        if detail not in t[path]:
                            t[path].append(detail)

                claude[project][session_id][uuid]["files"] = t


def getpathbyinfo(idfile: str, version: str = None, session_id: str = None, uuid: str = None, only_lasted: bool = True) -> str | None:
    high, normal, low = [], [], []
    
    for path in file_history:
        if path["id"] == idfile and ((version is None and path["version"] == version) or version is not None):
            if session_id in path["path"] and uuid in path["path"]:
                high.append(path["path"])
            elif session_id in path["path"] or uuid in path["path"]:
                normal.append(path["path"])
            else:
                low.append(path["path"])
    
    res = high if len(high) > 0 else (normal if len(normal) > 0 else (low if len(low) > 0 else None))
    
    if only_lasted and res is not None:
        return res[0]

    return res


def file2export(project: str, path: str, filesversion: list[dict], session_id: str, uuid: str) -> None:
    realpath = os.path.realpath(os.path.join("export", project, path))
    dirpath = os.path.dirname(realpath)
    os.makedirs(dirpath, exist_ok=True)
    for file in filesversion:
        if file["backupFileName"] is not None:
            idf, v = file["backupFileName"].split("@v")
            filepath = getpathbyinfo(idfile=idf, version=v, session_id=session_id, uuid=uuid)
            if filepath is not None:
                with open(realpath, "wb") as new:
                    with open(filepath, "rb") as original:
                        new.write(original.read())
                        log("trace", "Fichier enregistré: " + realpath)
            else:
                log("warning", "Chemin local non trouvé pour le fichier: " + path)
        else:
            log("warning", "Pas de fichier trouvé pour le chemin: " + path)


def export(project: str) -> None:
    export_path = {}
    data = claude[project]
    for session in data:
        for uuid in data[session]:
            if uuid != "title":
                for filepath in data[session][uuid]["files"]:
                    file2export(project=project, 
                                 path=filepath, 
                                 filesversion=data[session][uuid]["files"][filepath], 
                                 session_id=session, 
                                 uuid=uuid)

    # os.makedirs(exist_ok=True)
    log("debug", f"Projet \"{project}\" exporté")


def exportJSON(projects: str = None) -> None:
    if projects is None:
        data = claude
        filepath = "dotclaude-recovery.json"
    else:
        data = claude[projects]
        filepath = "dotclaude-recovery-" + projects + ".json"

    with open(filepath, "w", encoding="utf8") as file:
        file.write(json.dumps(data, indent=4, default=json_serial))
        log("debug", "Fichier JSON exporté: " + filepath)



# print(claude.keys())
# export("d--Bureau-claria")
exportJSON()
