import os
from datetime import datetime
from PyQt5.QtWidgets import (QComboBox, QWizardPage, QHBoxLayout, QVBoxLayout, QListWidget,
                             QListWidgetItem, QTextEdit, QLabel, QSplitter, QWidget)
from PyQt5.QtCore import Qt
from service import config
from service import scanner


class ProjectPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Projets et conversation")
        self.setSubTitle("Selectionnez un projet puis une session pour visualiser la conversation")

        root = QVBoxLayout()
        splitter = QSplitter(Qt.Orientation.Vertical)

        top = QWidget()
        tl = QVBoxLayout(top)
        tl.setContentsMargins(0, 0, 0, 0)
        tl.addWidget(QLabel("Projets"))
        self.proj_list = QComboBox()
        self.proj_list.currentTextChanged.connect(self._on_project_selected)
        tl.addWidget(self.proj_list)

        mid = QWidget()
        ml = QVBoxLayout(mid)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.addWidget(QLabel("Sessions"))
        self.sess_list = QComboBox()
        self.sess_list.currentTextChanged.connect(self._on_session_selected)
        ml.addWidget(self.sess_list)

        btm = QWidget()
        bl = QVBoxLayout(btm)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.addWidget(QLabel("Conversation"))
        self.conv = QTextEdit()
        self.conv.setReadOnly(True)
        self.conv.setStyleSheet("QTextEdit { background:white; font-size:11px; }")
        bl.addWidget(self.conv)

        splitter.addWidget(top)
        splitter.addWidget(mid)
        splitter.addWidget(btm)
        splitter.setSizes([10, 10, 300])
        root.addWidget(splitter)
        self.setLayout(root)

    def initializePage(self):
        self.proj_list.clear()
        for p in config.projects:
            label = f"{p['name']} ({len(p['sessions'])})"
            self.proj_list.addItem(label, p)

    def _on_project_selected(self):
        self.sess_list.clear()
        self.conv.clear()
        if self.proj_list.currentIndex() < 0:
            return
        proj = self.proj_list.currentData(Qt.ItemDataRole.UserRole)
        if proj is None:
            return
        config.selected_project = proj
        for s in sorted(proj["sessions"], key=lambda x: x["modified"], reverse=True):
            label = f"{datetime.fromtimestamp(s['modified']).strftime('%Y-%m-%d %H:%M')}  -  {s['id'][:8]}"
            self.sess_list.addItem(label, s)
        self.completeChanged.emit()

    def _on_session_selected(self):
        if self.sess_list.currentIndex() < 0:
            return
        sess = self.sess_list.currentData(Qt.ItemDataRole.UserRole)
        if sess is None or not sess.get("jsonl"):
            return
        config.selected_session = sess
        msgs, files = scanner.parse_session(sess["jsonl"])
        sess["messages"] = msgs
        sess["file_events"] = files
        self._render_conversation(msgs)
        self.completeChanged.emit()

    def _render_conversation(self, msgs):
        parts = []
        for m in msgs[:300]:
            role = m["role"]
            icon = "🧑" if role == "user" else "🤖"
            ts = m["timestamp"] or ""
            parts.append(f"### {icon} {role} — `{ts}`\n\n{m['text'] or ''}\n\n---\n")
        if len(msgs) > 300:
            parts.append(f"\n*... {len(msgs)-300} messages supplementaires*\n")
        self.conv.setMarkdown("\n".join(parts))

    def isComplete(self):
        return config.selected_session is not None
