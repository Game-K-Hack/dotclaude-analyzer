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


def _read_disk(fp):
    """Lit le fichier sur disque ; retourne (content, None) ou (None, raison)."""
    if not os.path.isfile(fp):
        return None, "absent du disque"
    try:
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            return f.read(), None
    except Exception as e:
        return None, str(e)


def _placeholder(fp, reason):
    return (
        f"# Fichier seulement modifie - contenu non reconstituable.\n"
        f"# Chemin original : {fp}\n"
        f"# Raison : {reason}\n"
    )


def export_to_folder(state, dest_folder, include_modified_only=False):
    """state : dict {abs_path: content|None}. Ecrit chaque fichier sous dest_folder.

    Si include_modified_only est vrai, les fichiers dont le contenu n'a pas pu
    etre reconstitue sont copies depuis le disque (version actuelle).
    """
    written, skipped = [], []
    os.makedirs(dest_folder, exist_ok=True)
    for fp, content in state.items():
        if content is None:
            if not include_modified_only:
                skipped.append(fp)
                continue
            content, err = _read_disk(fp)
            if content is None:
                content = _placeholder(fp, err)
        rel = _safe_relpath(fp)
        out = os.path.join(dest_folder, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        try:
            with open(out, "w", encoding="utf-8", newline="") as f:
                f.write(content)
            written.append(out)
        except Exception as e:
            skipped.append(f"{fp} ({e})")
    return written, skipped


def export_to_zip(state, dest_zip, include_modified_only=False):
    written, skipped = [], []
    os.makedirs(os.path.dirname(dest_zip) or ".", exist_ok=True)
    with zipfile.ZipFile(dest_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp, content in state.items():
            if content is None:
                if not include_modified_only:
                    skipped.append(fp)
                    continue
                content, err = _read_disk(fp)
                if content is None:
                    content = _placeholder(fp, err)
            rel = _safe_relpath(fp)
            try:
                zf.writestr(rel, content)
                written.append(rel)
            except Exception as e:
                skipped.append(f"{fp} ({e})")
    return written, skipped
