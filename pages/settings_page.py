import json
from PyQt5.QtWidgets import QWizardPage, QVBoxLayout, QLabel, QTextEdit, QTabWidget, QWidget
from service import config


class SettingsPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Parametres et connexion")
        self.setSubTitle("Apercu de la configuration et de l'etat d'authentification")

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.tab_settings = QTextEdit(); self.tab_settings.setReadOnly(True)
        self.tab_local = QTextEdit(); self.tab_local.setReadOnly(True)
        self.tab_creds = QTextEdit(); self.tab_creds.setReadOnly(True)

        for w in (self.tab_settings, self.tab_local, self.tab_creds):
            w.setStyleSheet("QTextEdit { background:white; font-family: Consolas, monospace; font-size:11px; }")

        self.tabs.addTab(self.tab_settings, "settings.json")
        self.tabs.addTab(self.tab_local, "settings.local.json")
        self.tabs.addTab(self.tab_creds, "Connexion")

        layout.addWidget(QLabel("Donnees lues depuis le dossier .claude :"))
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def initializePage(self):
        s = config.settings or {}
        self.tab_settings.setPlainText(self._dump(s.get("settings", {})))
        self.tab_local.setPlainText(self._dump(s.get("settings_local", {})))
        info = config.credentials_info or {}
        if not info.get("present"):
            self.tab_creds.setPlainText("Aucun fichier .credentials.json trouve.")
        else:
            lines = [
                f"Fichier present : oui",
                f"Taille          : {info.get('size')} octets",
                f"Modifie le      : {info.get('modified')}",
            ]
            if "expiry" in info:
                lines.append(f"Expiration      : {info['expiry']}")
            if info.get("fields"):
                lines.append("")
                lines.append("Champs detectes (cles uniquement, valeurs masquees) :")
                for k in info["fields"]:
                    lines.append(f"  - {k}")
            if info.get("error"):
                lines.append(f"Erreur de lecture : {info['error']}")
            self.tab_creds.setPlainText("\n".join(lines))

    @staticmethod
    def _dump(o):
        try:
            return json.dumps(o, indent=2, ensure_ascii=False)
        except Exception:
            return str(o)
