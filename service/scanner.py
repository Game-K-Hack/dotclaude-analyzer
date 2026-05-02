"""Scan d'un dossier .claude : projets, sessions, conversations, fichiers touches."""
import os
import json
from datetime import datetime


def default_claude_dir():
    """Retourne l'emplacement par defaut du dossier .claude (auto-detection)."""
    candidates = []
    home = os.path.expanduser("~")
    candidates.append(os.path.join(home, ".claude"))
    userprofile = os.environ.get("USERPROFILE")
    if userprofile:
        candidates.append(os.path.join(userprofile, ".claude"))
    # variante du repertoire courant
    candidates.append(os.path.join(os.getcwd(), ".claude"))
    for c in candidates:
        if os.path.isdir(c) and os.path.isdir(os.path.join(c, "projects")):
            return c
    return candidates[0]


def is_valid_claude_dir(path):
    return bool(path) and os.path.isdir(path) and os.path.isdir(os.path.join(path, "projects"))


def load_settings(claude_dir):
    """Charge settings.json + petit resume des autres fichiers config."""
    out = {"settings": {}, "settings_local": {}, "files": []}
    for name in ("settings.json", "settings.local.json"):
        p = os.path.join(claude_dir, name)
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    out["settings" if name == "settings.json" else "settings_local"] = json.load(f)
            except Exception as e:
                out["files"].append(f"{name}: erreur ({e})")
        else:
            out["files"].append(f"{name}: absent")
    return out


def credentials_summary(claude_dir):
    """Resume non-sensible du fichier .credentials.json."""
    p = os.path.join(claude_dir, ".credentials.json")
    info = {"present": False}
    if not os.path.isfile(p):
        return info
    info["present"] = True
    info["size"] = os.path.getsize(p)
    info["modified"] = datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        # On extrait uniquement les meta-donnees connues, pas les tokens.
        keys = []
        def walk(o, prefix=""):
            if isinstance(o, dict):
                for k, v in o.items():
                    if isinstance(v, (dict, list)):
                        walk(v, prefix + k + ".")
                    else:
                        keys.append({prefix + k: v})
        walk(data)
        info["fields"] = keys
        # Tente d'extraire une expiration si presente
        def find_expiry(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if "expir" in k.lower() and isinstance(v, (int, float, str)):
                        return (k, v)
                    r = find_expiry(v)
                    if r: return r
            elif isinstance(o, list):
                for v in o:
                    r = find_expiry(v)
                    if r: return r
            return None
        exp = find_expiry(data)
        if exp:
            info["expiry"] = f"{exp[0]} = {exp[1]}"
    except Exception as e:
        info["error"] = str(e)
    return info


def list_projects(claude_dir):
    """Liste les projets et leurs sessions."""
    projects_dir = os.path.join(claude_dir, "projects")
    out = []
    if not os.path.isdir(projects_dir):
        return out
    for name in sorted(os.listdir(projects_dir)):
        p = os.path.join(projects_dir, name)
        if not os.path.isdir(p):
            continue
        sessions = []
        for entry in sorted(os.listdir(p)):
            full = os.path.join(p, entry)
            if entry.endswith(".jsonl") and os.path.isfile(full):
                sessions.append({
                    "id": entry[:-6],
                    "jsonl": full,
                    "size": os.path.getsize(full),
                    "modified": os.path.getmtime(full),
                })
        out.append({"name": name, "path": p, "sessions": sessions})
    return out


def parse_session(jsonl_path, max_events=None):
    """Parcourt un fichier .jsonl et retourne (messages, file_events).

    messages = liste de dicts {role, text, timestamp}
    file_events = liste de dicts {timestamp, tool, file_path, payload}
       payload depend de l'outil :
       - Write    : {"content": str}
       - Edit     : {"old_string": str, "new_string": str, "replace_all": bool}
       - MultiEdit: {"edits": [ {old_string, new_string, replace_all}, ... ]}
       - NotebookEdit / autre : payload brut
    """
    messages = []
    file_events = []
    if not os.path.isfile(jsonl_path):
        return messages, file_events
    with open(jsonl_path, "r", encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f):
            if max_events and i > max_events:
                break
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
            except Exception:
                continue
            etype = evt.get("type")
            ts = evt.get("timestamp")
            if etype == "user":
                msg = evt.get("message", {})
                content = msg.get("content")
                text = _extract_text(content)
                if text:
                    messages.append({"role": "user", "text": text, "timestamp": ts})
                # tool_results sont dans le contenu user mais on les ignore pour l'affichage
            elif etype == "assistant":
                msg = evt.get("message", {})
                content = msg.get("content", [])
                text = _extract_text(content)
                if text:
                    messages.append({"role": "assistant", "text": text, "timestamp": ts})
                if isinstance(content, list):
                    for blk in content:
                        if isinstance(blk, dict) and blk.get("type") == "tool_use":
                            ev = _file_event_from_tool(blk, ts)
                            if ev:
                                file_events.append(ev)
    return messages, file_events


def _extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for blk in content:
            if isinstance(blk, dict) and blk.get("type") == "text":
                t = blk.get("text", "")
                if t:
                    parts.append(t)
        return "\n".join(parts)
    return ""


def _file_event_from_tool(blk, ts):
    name = blk.get("name", "")
    inp = blk.get("input", {}) or {}
    fp = inp.get("file_path") or inp.get("notebook_path")
    if not fp:
        return None
    if name == "Write":
        return {"timestamp": ts, "tool": "Write", "file_path": fp, "payload": {"content": inp.get("content", "")}}
    if name == "Edit":
        return {"timestamp": ts, "tool": "Edit", "file_path": fp, "payload": {
            "old_string": inp.get("old_string", ""),
            "new_string": inp.get("new_string", ""),
            "replace_all": bool(inp.get("replace_all", False)),
        }}
    if name == "MultiEdit":
        return {"timestamp": ts, "tool": "MultiEdit", "file_path": fp, "payload": {"edits": inp.get("edits", [])}}
    if name == "NotebookEdit":
        return {"timestamp": ts, "tool": "NotebookEdit", "file_path": fp, "payload": dict(inp)}
    return None
