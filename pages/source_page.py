import os
from PyQt5.QtWidgets import (QWizardPage, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QFileDialog, QTextEdit, QCheckBox, QLabel)
from service import config
from service import scanner
from service.log_format import format_log, should_log


class SourcePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Dossier .claude")
        self.setSubTitle("Detection automatique ou choix manuel du dossier source")

        layout = QVBoxLayout()

        self.auto_chk = QCheckBox("Detection automatique")
        self.auto_chk.setChecked(True)
        self.auto_chk.stateChanged.connect(self._toggle_auto)
        layout.addWidget(self.auto_chk)

        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.textChanged.connect(self._update_source)
        path_layout.addWidget(self.path_edit)
        self.browse_btn = QPushButton("Parcourir...")
        self.browse_btn.clicked.connect(self._browse)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)

        layout.addWidget(QLabel("Diagnostic :"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet(
            "QTextEdit { background:white; border:1px solid #999; "
            "font-family: Consolas, monospace; font-size: 11px; }"
        )
        self.log.setFixedHeight(220)
        layout.addWidget(self.log)
        layout.addStretch()

        self.setLayout(layout)

    def initializePage(self):
        if self.auto_chk.isChecked():
            self.path_edit.setText(scanner.default_claude_dir())

    def _toggle_auto(self, state):
        auto = self.auto_chk.isChecked()
        self.path_edit.setReadOnly(auto)
        self.browse_btn.setEnabled(not auto)
        if auto:
            self.path_edit.setText(scanner.default_claude_dir())

    def _browse(self):
        start = self.path_edit.text() or os.path.expanduser("~")
        d = QFileDialog.getExistingDirectory(self, "Choisir un dossier .claude", start)
        if d:
            self.path_edit.setText(d)

    def _update_source(self, text):
        config.claude_dir = text
        config.claude_dir_valid = scanner.is_valid_claude_dir(text)
        self.log.clear()
        self._log(f"Chemin choisi : <b>{text or '(vide)'}</b>", "debug")
        if not text:
            self.completeChanged.emit(); return
        if not os.path.isdir(text):
            self._log("Dossier introuvable.", "error")
        elif not config.claude_dir_valid:
            self._log("Sous-dossier 'projects/' absent : ce n'est pas un .claude valide.", "error")
        else:
            self._log("Dossier .claude valide.", "ok")
            projects = scanner.list_projects(text)
            self._log(f"Projets detectes : <b>{len(projects)}</b>")
            sessions = sum(len(p['sessions']) for p in projects)
            self._log(f"Sessions cumulees : <b>{sessions}</b>")
            config.projects = projects
            config.settings = scanner.load_settings(text)
            config.credentials_info = scanner.credentials_summary(text)
        self.completeChanged.emit()

    def _log(self, msg: str, level: str = "info"):
        # Filtrage par niveau (configurable via service.log_format.log_level).
        if not should_log(level):
            return
        self.log.append(format_log(level, msg, only_text=False))

    def isComplete(self):
        return bool(config.claude_dir_valid)
