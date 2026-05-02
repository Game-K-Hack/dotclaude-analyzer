"""Reconstruit l'etat des fichiers a partir des evenements d'une session."""
import os


def parse_ts(ts):
    """Convertit le timestamp ISO en str triable, ou retourne tel quel."""
    return ts or ""


def reconstruct(file_events, until_ts=None):
    """Retourne dict {file_path: content_str_or_None}.

    None signifie que la session a touche au fichier mais qu'on ne peut pas
    reconstituer son contenu (premier evenement etait un Edit sans contenu de base).
    """
    state = {}            # path -> str | None
    base_loaded = {}      # path -> bool : a-t-on charge la base depuis le disque ?

    events = sorted([e for e in file_events if not until_ts or parse_ts(e["timestamp"]) <= until_ts],
                    key=lambda e: parse_ts(e["timestamp"]))

    for ev in events:
        fp = ev["file_path"]
        tool = ev["tool"]
        payload = ev["payload"]

        if tool == "Write":
            state[fp] = payload.get("content", "")
            base_loaded[fp] = True
            continue

        if tool in ("Edit", "MultiEdit"):
            # On a besoin d'un contenu de base
            if fp not in state or state[fp] is None:
                # Tente de lire la version actuelle sur disque (meilleur effort)
                if not base_loaded.get(fp) and os.path.isfile(fp):
                    try:
                        with open(fp, "r", encoding="utf-8", errors="replace") as f:
                            state[fp] = f.read()
                    except Exception:
                        state[fp] = None
                else:
                    state[fp] = None
                base_loaded[fp] = True

            if state.get(fp) is None:
                continue

            if tool == "Edit":
                _apply_edit(state, fp, payload)
            else:
                for sub in payload.get("edits", []):
                    _apply_edit(state, fp, sub)
            continue

        if tool == "NotebookEdit":
            # On garde une trace mais on ne reconstruit pas les notebooks ici.
            state.setdefault(fp, None)

    return state


def _apply_edit(state, fp, payload):
    content = state.get(fp)
    if content is None:
        return
    old = payload.get("old_string", "")
    new = payload.get("new_string", "")
    if not old:
        return
    if payload.get("replace_all"):
        state[fp] = content.replace(old, new)
    else:
        idx = content.find(old)
        if idx >= 0:
            state[fp] = content[:idx] + new + content[idx + len(old):]
