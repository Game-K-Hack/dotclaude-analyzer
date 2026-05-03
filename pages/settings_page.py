import json
from PyQt5.QtWidgets import QWizardPage, QVBoxLayout, QLabel, QTextEdit, QTabWidget
from service import config
from service import i18n
from service.i18n import tr


class SettingsPage(QWizardPage):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.tab_settings = QTextEdit()
        self.tab_settings.setReadOnly(True)
        self.tab_local = QTextEdit()
        self.tab_local.setReadOnly(True)
        self.tab_creds = QTextEdit()
        self.tab_creds.setReadOnly(True)

        for w in (self.tab_settings, self.tab_local, self.tab_creds):
            w.setStyleSheet("QTextEdit { background:white; font-family: Consolas, monospace; font-size:11px; }")

        self.tabs.addTab(self.tab_settings, "settings.json")
        self.tabs.addTab(self.tab_local, "settings.local.json")
        self.tabs.addTab(self.tab_creds, "")

        self.data_label = QLabel()
        layout.addWidget(self.data_label)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self._retranslate()
        i18n.signaler.language_changed.connect(self._retranslate)

    def _retranslate(self, *_):
        self.setTitle(tr("settings.title"))
        self.setSubTitle(tr("settings.subtitle"))
        self.data_label.setText(tr("settings.data_label"))
        self.tabs.setTabText(0, tr("settings.tab_settings"))
        self.tabs.setTabText(1, tr("settings.tab_local"))
        self.tabs.setTabText(2, tr("settings.tab_creds"))
        # Réaffiche le contenu si déjà chargé.
        if config.settings or config.credentials_info:
            self.initializePage()

    def initializePage(self):
        s = config.settings or {}
        self.tab_settings.setText(self._dump(s.get("settings", {})))
        self.tab_local.setText(self._dump(s.get("settings_local", {})))
        info = config.credentials_info or {}
        if not info.get("present"):
            self.tab_creds.setText(tr("settings.no_credentials"))
        else:
            self.tab_creds.setText(tr("settings.cred_present"))
            self.tab_creds.append(tr("settings.cred_size", size=info.get("size")))
            self.tab_creds.append(tr("settings.cred_modified", date=info.get("modified")))
            if "expiry" in info:
                self.tab_creds.append(tr("settings.cred_expiry", expiry=info["expiry"]))
            if info.get("fields"):
                self.tab_creds.append("")
                self.tab_creds.append(tr("settings.cred_fields"))
                for elm in info["fields"]:
                    key = list(elm.keys())[0]
                    value = elm[key]
                    self.tab_creds.append(f"  - <b>{key}</b>: {value}")
            if info.get("error"):
                self.tab_creds.append(tr("settings.cred_error", error=info["error"]))

    @staticmethod
    def _dump(o):
        try:
            return json.dumps(o, indent=2, ensure_ascii=False)
        except Exception:
            return str(o)
