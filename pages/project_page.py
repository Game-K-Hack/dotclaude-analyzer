from datetime import datetime
from PyQt5.QtWidgets import QComboBox, QWizardPage, QVBoxLayout, QTextEdit, QLabel, QSplitter, QWidget, QCheckBox
from PyQt5.QtCore import Qt
from service import config
from service import scanner
from service import i18n
from service.i18n import tr


class ProjectPage(QWizardPage):
    def __init__(self):
        super().__init__()

        root = QVBoxLayout()
        splitter = QSplitter(Qt.Orientation.Vertical)

        top = QWidget()
        tl = QVBoxLayout(top)
        tl.setContentsMargins(0, 0, 0, 0)
        self.lbl_projects = QLabel()
        tl.addWidget(self.lbl_projects)
        self.proj_list = QComboBox()
        self.proj_list.currentTextChanged.connect(self._on_project_selected)
        tl.addWidget(self.proj_list)

        mid = QWidget()
        ml = QVBoxLayout(mid)
        ml.setContentsMargins(0, 0, 0, 0)
        self.lbl_sessions = QLabel()
        ml.addWidget(self.lbl_sessions)
        self.sess_list = QComboBox()
        self.sess_list.currentTextChanged.connect(self._on_session_selected)
        ml.addWidget(self.sess_list)
        self.all_sess = QCheckBox()
        self.all_sess.toggled.connect(self._on_all_toggled)
        ml.addWidget(self.all_sess)

        btm = QWidget()
        bl = QVBoxLayout(btm)
        bl.setContentsMargins(0, 0, 0, 0)
        self.lbl_conv = QLabel()
        bl.addWidget(self.lbl_conv)
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

        self._last_msgs = []
        self._retranslate()
        i18n.signaler.language_changed.connect(self._retranslate)

    def _retranslate(self, *_):
        self.setTitle(tr("project.title"))
        self.setSubTitle(tr("project.subtitle"))
        self.lbl_projects.setText(tr("project.label_projects"))
        self.lbl_sessions.setText(tr("project.label_sessions"))
        self.lbl_conv.setText(tr("project.label_conversation"))
        self.all_sess.setText(tr("project.all_sessions"))
        if self._last_msgs:
            self._render_conversation(self._last_msgs)

    def initializePage(self):
        self.proj_list.clear()
        for p in config.projects:
            label = f"{p['name']} ({len(p['sessions'])})"
            self.proj_list.addItem(label, p)

    def _on_project_selected(self):
        self.sess_list.clear()
        self.conv.clear()
        self.all_sess.setChecked(False)
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
        if self.all_sess.isChecked():
            return
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

    def _on_all_toggled(self, checked):
        self.sess_list.setEnabled(not checked)
        if not checked:
            self._on_session_selected()
            return
        proj = config.selected_project
        if not proj:
            return
        all_msgs, all_files = [], []
        sessions_sorted = sorted(proj["sessions"], key=lambda x: x["modified"])
        for s in sessions_sorted:
            if not s.get("jsonl"):
                continue
            msgs, files = scanner.parse_session(s["jsonl"])
            s["messages"] = msgs
            s["file_events"] = files
            header = {
                "role": "assistant",
                "text": tr(
                    "project.session_header",
                    id=s["id"][:8],
                    date=datetime.fromtimestamp(s["modified"]).strftime("%Y-%m-%d %H:%M"),
                ),
                "timestamp": "",
            }
            all_msgs.append(header)
            all_msgs.extend(msgs)
            all_files.extend(files)
        all_files.sort(key=lambda e: e.get("timestamp") or "")
        config.selected_session = {
            "id": f"ALL-{proj['name']}",
            "jsonl": None,
            "messages": all_msgs,
            "file_events": all_files,
            "modified": max((s["modified"] for s in proj["sessions"]), default=0),
            "all_sessions": True,
        }
        self._render_conversation(all_msgs)
        self.completeChanged.emit()

    def _render_conversation(self, msgs):
        self._last_msgs = msgs
        parts = []
        for m in msgs[:300]:
            role = m["role"]
            icon = "🧑" if role == "user" else "🤖"
            ts = m["timestamp"] or ""
            parts.append(f"### {icon} {role} — `{ts}`\n\n{m['text'] or ''}\n\n---\n")
        if len(msgs) > 300:
            parts.append(tr("project.more_messages", count=len(msgs) - 300))
        self.conv.setMarkdown("\n".join(parts))

    def isComplete(self):
        return config.selected_session is not None
