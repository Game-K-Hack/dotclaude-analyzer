"""Formatage de log HTML pour QTextEdit, calqué sur le format console
colorama de l'utilisateur :

    | LEVEL    | YYYY-MM-DD HH:MM:SS | <texte coloré>

Les blocs colorés sont rendus avec des <span> à background-color, le
timestamp dans un bloc gris, et le texte dans la couleur du niveau.
"""

from __future__ import annotations

import datetime


# Niveaux dans l'ordre de verbosité croissante (du plus important au plus bavard).
LEVELS = ["input", "error", "warning", "info", "ok", "debug", "trace"]

# Couleurs par niveau : (background du bloc, couleur du texte du message).
# Le background est saturé (équivalent Back.X), le texte légèrement plus
# foncé pour rester lisible sur fond blanc.
COLORS = {
    "input":   {"bg": "#00ACC1", "fg": "#00838F"},  # cyan
    "error":   {"bg": "#C93030", "fg": "#B71C1C"},  # red
    "warning": {"bg": "#F9A825", "fg": "#E65100"},  # yellow/orange
    "info":    {"bg": "#1976D2", "fg": "#0D47A1"},  # blue
    "ok":      {"bg": "#50B450", "fg": "#2E7D32"},  # green
    "debug":   {"bg": "#9C27B0", "fg": "#6A1B9A"},  # magenta
    "trace":   {"bg": "#424242", "fg": "#212121"},  # black/gray
}

TIMESTAMP_BG = "#5a5a5a"
TIMESTAMP_FG = "#ffffff"

# Largeur de la colonne du nom de niveau (pour l'alignement vertical).
COLUMN_WIDTH = max(len(k) for k in LEVELS)  # = 7 ("warning")

# Niveau au-delà duquel on filtre les messages (voir should_log()).
log_level: str = "debug"


def _esc(s: str) -> str:
    """Échappe le HTML basique pour ne pas casser le rendu."""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


def should_log(level: str) -> bool:
    """Reproduit le filtre `level not in colors_keys[:idx(log_level)+1]`."""
    if level not in LEVELS or log_level not in LEVELS:
        return True
    return LEVELS.index(level) <= LEVELS.index(log_level)


def format_log(level: str, text: str, ts: datetime.datetime | None = None, only_text: bool = True) -> str:
    """Renvoie une ligne HTML prête à être passée à QTextEdit.append()."""
    level = (level or "info").lower().strip()
    c = COLORS.get(level, COLORS["info"])
    if ts is None:
        ts = datetime.datetime.now()

    # Padding du nom de niveau pour aligner les colonnes.
    label = level.upper().ljust(COLUMN_WIDTH)
    # &nbsp; pour préserver les espaces de padding dans le HTML rendu.
    label_html = label.replace(" ", "&nbsp;")

    # Style commun aux blocs : padding compact, gras pour le label.
    block_style = (
        "padding: 1px 6px; font-family: Consolas, monospace; "
        "font-size: 10px;"
    )

    level_block = (
        f'<span style="{block_style} background-color: {c["bg"]}; '
        f'color: white; font-weight: bold;">&nbsp;{label_html}&nbsp;</span>'
    )

    ts_block = (
        f'<span style="{block_style} background-color: {TIMESTAMP_BG}; '
        f'color: {TIMESTAMP_FG};">&nbsp;{ts.strftime("%Y-%m-%d %H:%M:%S")}&nbsp;</span>'
    )

    # Petit séparateur coloré (équivalent du `c['b']` après le timestamp).
    sep_block = (
        f'<span style="{block_style} background-color: {c["bg"]}; '
        f'color: white;">&nbsp;</span>'
    )

    msg = (
        f'<span style="font-family: Consolas, monospace; font-size: 10px; '
        f'color: {c["fg"]};">&nbsp;{_esc(text) if only_text else text}</span>'
    )

    return level_block + ts_block + sep_block + msg
