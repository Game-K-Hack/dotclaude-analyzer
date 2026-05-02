import json
from PyQt5.QtWidgets import QWizardPage, QVBoxLayout, QLabel, QTextEdit, QTabWidget, QWidget
from service import config
from service.log_format import format_log


class SettingsPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Parametres et connexion")
        self.setSubTitle("Apercu de la configuration et de l'etat d'authentification")

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.tab_settings = QTextEdit()
        self.tab_settings.setReadOnly(True)
        self.tab_settings.setStyleSheet(
            "QTextEdit { background:white; border:1px solid #999; "
            "font-family: Consolas, monospace; font-size: 11px; }")

        self.tab_local = QTextEdit()
        self.tab_local.setReadOnly(True)
        self.tab_settings.setStyleSheet(
            "QTextEdit { background:white; border:1px solid #999; "
            "font-family: Consolas, monospace; font-size: 11px; }")

        self.tab_creds = QTextEdit()
        self.tab_creds.setReadOnly(True)
        self.tab_creds.setStyleSheet(
            "QTextEdit { background:white; border:1px solid #999; "
            "font-family: Consolas, monospace; font-size: 11px; }")

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
        self.tab_settings.setText(self._dump(s.get("settings", {})))
        self.tab_local.setText(self._dump(s.get("settings_local", {})))
        info = config.credentials_info or {}
        if not info.get("present"):
            self.tab_creds.setText("Aucun fichier .credentials.json trouve.")
        else:
            self.tab_creds.setText(f"Fichier present : oui")
            self.tab_creds.append(f"Taille          : {info.get('size')} octets")
            self.tab_creds.append(f"Modifie le      : {info.get('modified')}")
            if "expiry" in info:
                self.tab_creds.append(f"Expiration      : {info['expiry']}")
            if info.get("fields"):
                self.tab_creds.append("")
                self.tab_creds.append("Champs detectes :")
                for elm in info["fields"]:
                    key = list(elm.keys())[0]
                    value = elm[key]
                    self.tab_creds.append(f"  - <b>{key}</b>: {value}")
            if info.get("error"):
                self.tab_creds.append(f"Erreur de lecture : {info['error']}")

    @staticmethod
    def _dump(o):
        try:
            return json.dumps(o, indent=2, ensure_ascii=False)
        except Exception:
            return str(o)
