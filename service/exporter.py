"""Export des fichiers reconstitues : dossier ou archive ZIP."""
import os
import re
import zipfile


def _safe_relpath(file_path):
    """Transforme un chemin absolu en chemin relatif portable."""
    p = file_path.replace("\\", "/")
    # retire la lettre de lecteur Windows
    p = re.sub(r"^[A-Za-z]:/", "", p)
    p = p.lstrip("/")
    return p or "fichier_sans_nom"


def export_to_folder(state, dest_folder):
    """state : dict {abs_path: content|None}. Ecrit chaque fichier sous dest_folder."""
    written, skipped = [], []
    os.makedirs(dest_folder, exist_ok=True)
    for fp, content in state.items():
        rel = _safe_relpath(fp)
        out = os.path.join(dest_folder, rel)
        if content is None:
            skipped.append(fp)
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        try:
            with open(out, "w", encoding="utf-8", newline="") as f:
                f.write(content)
            written.append(out)
        except Exception as e:
            skipped.append(f"{fp} ({e})")
    return written, skipped


def export_to_zip(state, dest_zip):
    written, skipped = [], []
    os.makedirs(os.path.dirname(dest_zip) or ".", exist_ok=True)
    with zipfile.ZipFile(dest_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp, content in state.items():
            if content is None:
                skipped.append(fp)
                continue
            rel = _safe_relpath(fp)
            try:
                zf.writestr(rel, content)
                written.append(rel)
            except Exception as e:
                skipped.append(f"{fp} ({e})")
    return written, skipped
