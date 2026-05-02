"""Etat partage entre les pages du wizard."""

claude_dir = ""           # racine .claude selectionnee
claude_dir_valid = False
projects = []             # liste des dicts {name, path, sessions:[...]}
selected_project = None   # dict du projet selectionne
selected_session = None   # dict de la session
settings = {}             # contenu settings.json
credentials_info = {}     # infos non-sensibles sur .credentials.json
