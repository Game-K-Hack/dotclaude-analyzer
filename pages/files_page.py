import os
from datetime import datetime
from PyQt5.QtWidgets import (QWizardPage, QVBoxLayout, QHBoxLayout, QLabel,
                             QSlider, QListWidget, QListWidgetItem, QPushButton,
                             QFileDialog, QMessageBox, QComboBox, QCheckBox)
from PyQt5.QtCore import Qt
from service import config
from service import reconstructor, exporter
from service import i18n
from service.i18n import tr


class FilesPage(QWizardPage):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.summary = QLabel("")
        layout.addWidget(self.summary)

        slider_box = QHBoxLayout()
        self.date_min = QLabel("--"); self.date_max = QLabel("--")
        self.date_cur = QLabel("--")
        self.date_cur.setStyleSheet("font-weight:bold;color:#0078d4;")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0); self.slider.setMaximum(0)
        self.slider.valueChanged.connect(self._on_slider)
        slider_box.addWidget(self.date_min)
        slider_box.addWidget(self.slider, 1)
        slider_box.addWidget(self.date_max)
        layout.addLayout(slider_box)
        layout.addWidget(self.date_cur, alignment=Qt.AlignmentFlag.AlignCenter)

        self.lbl_files_at_date = QLabel()
        layout.addWidget(self.lbl_files_at_date)
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        btns = QHBoxLayout()
        self.format_combo = QComboBox()
        self.format_combo.addItem("", "folder")
        self.format_combo.addItem("", "zip")
        self.lbl_format = QLabel()
        btns.addWidget(self.lbl_format)
        btns.addWidget(self.format_combo)
        btns.addStretch()
        self.export_btn = QPushButton()
        self.export_btn.clicked.connect(self._export)
        btns.addWidget(self.export_btn)
        layout.addLayout(btns)

        self.include_modified_cb = QCheckBox()
        layout.addWidget(self.include_modified_cb, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

        self._timestamps = []
        self._events = []
        self._current_state = None

        self._retranslate()
        i18n.signaler.language_changed.connect(self._retranslate)

    def _retranslate(self, *_):
        self.setTitle(tr("files.title"))
        self.setSubTitle(tr("files.subtitle"))
        self.lbl_files_at_date.setText(tr("files.files_at_date"))
        self.lbl_format.setText(tr("files.format"))
        self.format_combo.setItemText(0, tr("files.format_folder"))
        self.format_combo.setItemText(1, tr("files.format_zip"))
        self.export_btn.setText(tr("files.export_btn"))
        self.include_modified_cb.setText(tr("files.include_modified"))
        self.include_modified_cb.setToolTip(tr("files.include_modified_tooltip"))
        # Re-render du contenu dynamique si la page a deja ete initialisee.
        if self._timestamps:
            files_uniq = {e["file_path"] for e in self._events}
            self.summary.setText(tr("files.summary", files=len(files_uniq), ops=len(self._events)))
            self._refresh()
        elif self._events is not None and self.summary.text():
            self.summary.setText(tr("files.no_touched"))

    def initializePage(self):
        sess = config.selected_session or {}
        self._events = sess.get("file_events", []) or []
        ts = sorted({e["timestamp"] for e in self._events if e.get("timestamp")})
        self._timestamps = ts
        if not ts:
            self.summary.setText(tr("files.no_touched"))
            self.slider.setMaximum(0); self.slider.setEnabled(False)
            self.date_min.setText("--"); self.date_max.setText("--"); self.date_cur.setText("--")
            self.file_list.clear()
            return
        self.slider.setEnabled(True)
        self.slider.setMinimum(0); self.slider.setMaximum(len(ts) - 1)
        self.slider.setValue(len(ts) - 1)
        self.date_min.setText(_short(ts[0]))
        self.date_max.setText(_short(ts[-1]))
        files_uniq = {e["file_path"] for e in self._events}
        self.summary.setText(tr("files.summary", files=len(files_uniq), ops=len(self._events)))
        self._refresh()

    def _on_slider(self, _):
        self._refresh()

    def _refresh(self):
        if not self._timestamps:
            return
        idx = self.slider.value()
        cur_ts = self._timestamps[idx]
        self.date_cur.setText(tr("files.version_at", date=_short(cur_ts), idx=idx + 1, total=len(self._timestamps)))
        state = reconstructor.reconstruct(self._events, until_ts=cur_ts)
        self.file_list.clear()
        for fp in sorted(state.keys()):
            content = state[fp]
            if content is None:
                tag = tr("files.tag_edits")
                size = "?"
            else:
                tag = tr("files.tag_ok")
                size = tr("files.unit_chars", n=len(content))
            it = QListWidgetItem(f"{tag}  {fp}    {size}")
            it.setData(Qt.ItemDataRole.UserRole, (fp, content))
            self.file_list.addItem(it)
        self._current_state = state

    def _export(self):
        if not self._current_state:
            QMessageBox.warning(self, tr("files.export_title"), tr("files.export_none"))
            return
        fmt = self.format_combo.currentData()
        include_mod = self.include_modified_cb.isChecked()
        if fmt == "folder":
            d = QFileDialog.getExistingDirectory(self, tr("files.dialog_dest"))
            if not d:
                return
            written, skipped = exporter.export_to_folder(self._current_state, d, include_modified_only=include_mod)
        else:
            f, _ = QFileDialog.getSaveFileName(self, tr("files.dialog_save"), "export-claude.zip", tr("files.zip_filter"))
            if not f:
                return
            written, skipped = exporter.export_to_zip(self._current_state, f, include_modified_only=include_mod)
        msg = tr("files.export_count", n=len(written))
        if skipped:
            msg += tr("files.export_skipped", n=len(skipped))
        QMessageBox.information(self, tr("files.export_done_title"), msg)


def _short(ts):
    if not ts:
        return "--"
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ts[:16]
