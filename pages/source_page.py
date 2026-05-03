import os
from PyQt5.QtWidgets import (QWizardPage, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QFileDialog, QTextEdit, QCheckBox, QLabel)
from service import config
from service import scanner
from service import i18n
from service.i18n import tr
from service.log_format import format_log, should_log


class SourcePage(QWizardPage):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.auto_chk = QCheckBox()
        self.auto_chk.setChecked(True)
        self.auto_chk.stateChanged.connect(self._toggle_auto)
        layout.addWidget(self.auto_chk)

        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.textChanged.connect(self._update_source)
        path_layout.addWidget(self.path_edit)
        self.browse_btn = QPushButton()
        self.browse_btn.clicked.connect(self._browse)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)

        self.diag_label = QLabel()
        layout.addWidget(self.diag_label)
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

        self._retranslate()
        i18n.signaler.language_changed.connect(self._retranslate)

    def _retranslate(self, *_):
        self.setTitle(tr("source.title"))
        self.setSubTitle(tr("source.subtitle"))
        self.auto_chk.setText(tr("source.auto_detect"))
        self.browse_btn.setText(tr("source.browse"))
        self.diag_label.setText(tr("source.diagnostic"))
        # Re-affiche le diagnostic dans la nouvelle langue.
        self._update_source(self.path_edit.text())

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
        d = QFileDialog.getExistingDirectory(self, tr("source.dialog_choose"), start)
        if d:
            self.path_edit.setText(d)

    def _update_source(self, text):
        config.claude_dir = text
        config.claude_dir_valid = scanner.is_valid_claude_dir(text)
        self.log.clear()
        self._log(tr("source.log_path_chosen", path=text or tr("source.path_empty")), "debug")
        if not text:
            self.completeChanged.emit(); return
        if not os.path.isdir(text):
            self._log(tr("source.log_not_found"), "error")
        elif not config.claude_dir_valid:
            self._log(tr("source.log_invalid"), "error")
        else:
            self._log(tr("source.log_valid"), "ok")
            projects = scanner.list_projects(text)
            self._log(tr("source.log_projects_detected", count=len(projects)))
            sessions = sum(len(p['sessions']) for p in projects)
            self._log(tr("source.log_sessions_total", count=sessions))
            config.projects = projects
            config.settings = scanner.load_settings(text)
            config.credentials_info = scanner.credentials_summary(text)
        self.completeChanged.emit()

    def _log(self, msg: str, level: str = "info"):
        if not should_log(level):
            return
        self.log.append(format_log(level, msg, only_text=False))

    def isComplete(self):
        return bool(config.claude_dir_valid)
