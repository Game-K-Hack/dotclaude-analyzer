import os
from datetime import datetime
from PyQt5.QtWidgets import (QWizardPage, QHBoxLayout, QVBoxLayout, QListWidget,
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
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Colonne gauche : projets
        left = QWidget(); ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.addWidget(QLabel("Projets"))
        self.proj_list = QListWidget()
        self.proj_list.itemSelectionChanged.connect(self._on_project_selected)
        ll.addWidget(self.proj_list)

        # Colonne milieu : sessions
        mid = QWidget(); ml = QVBoxLayout(mid); ml.setContentsMargins(0, 0, 0, 0)
        ml.addWidget(QLabel("Sessions"))
        self.sess_list = QListWidget()
        self.sess_list.itemSelectionChanged.connect(self._on_session_selected)
        ml.addWidget(self.sess_list)

        # Colonne droite : conversation
        right = QWidget(); rl = QVBoxLayout(right); rl.setContentsMargins(0, 0, 0, 0)
        rl.addWidget(QLabel("Conversation"))
        self.conv = QTextEdit(); self.conv.setReadOnly(True)
        self.conv.setStyleSheet("QTextEdit { background:white; font-size:11px; }")
        rl.addWidget(self.conv)

        splitter.addWidget(left); splitter.addWidget(mid); splitter.addWidget(right)
        splitter.setSizes([140, 180, 380])
        root.addWidget(splitter)
        self.setLayout(root)

    def initializePage(self):
        self.proj_list.clear()
        for p in config.projects:
            it = QListWidgetItem(f"{p['name']}  ({len(p['sessions'])})")
            it.setData(Qt.ItemDataRole.UserRole, p)
            self.proj_list.addItem(it)

    def _on_project_selected(self):
        items = self.proj_list.selectedItems()
        self.sess_list.clear()
        self.conv.clear()
        if not items:
            return
        proj = items[0].data(Qt.ItemDataRole.UserRole)
        config.selected_project = proj
        for s in sorted(proj["sessions"], key=lambda x: x["modified"], reverse=True):
            label = f"{datetime.fromtimestamp(s['modified']).strftime('%Y-%m-%d %H:%M')}  -  {s['id'][:8]}"
            it = QListWidgetItem(label)
            it.setData(Qt.ItemDataRole.UserRole, s)
            self.sess_list.addItem(it)
        self.completeChanged.emit()

    def _on_session_selected(self):
        items = self.sess_list.selectedItems()
        if not items:
            return
        sess = items[0].data(Qt.ItemDataRole.UserRole)
        config.selected_session = sess
        msgs, files = scanner.parse_session(sess["jsonl"])
        sess["messages"] = msgs
        sess["file_events"] = files
        self._render_conversation(msgs)
        self.completeChanged.emit()

    def _render_conversation(self, msgs):
        html = ["<style>"
                ".u{background:#eef5ff;border-left:3px solid #0078d4;padding:6px;margin:4px 0;}"
                ".a{background:#f6f6f6;border-left:3px solid #888;padding:6px;margin:4px 0;}"
                ".t{color:#888;font-size:9px;}"
                "</style>"]
        for m in msgs[:300]:
            cls = "u" if m["role"] == "user" else "a"
            txt = (m["text"] or "").replace("&", "&amp;").replace("<", "&lt;").replace("\n", "<br>")
            html.append(f"<div class='{cls}'><span class='t'>{m['timestamp'] or ''} &middot; {m['role']}</span><br>{txt}</div>")
        if len(msgs) > 300:
            html.append(f"<p><i>... {len(msgs)-300} messages supplementaires</i></p>")
        self.conv.setHtml("".join(html))

    def isComplete(self):
        return config.selected_session is not None
