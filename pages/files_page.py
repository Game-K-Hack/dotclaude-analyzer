import os
from datetime import datetime
from PyQt5.QtWidgets import (QWizardPage, QVBoxLayout, QHBoxLayout, QLabel,
                             QSlider, QListWidget, QListWidgetItem, QPushButton,
                             QFileDialog, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from service import config
from service import reconstructor, exporter


class FilesPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Fichiers crees / modifies")
        self.setSubTitle("Selectionnez une date pour reconstruire l'etat du projet a ce moment")

        layout = QVBoxLayout()

        self.summary = QLabel("")
        layout.addWidget(self.summary)

        # Slider de date
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

        layout.addWidget(QLabel("Fichiers a cette date :"))
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        # Boutons d'export
        btns = QHBoxLayout()
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Dossier", "Archive ZIP"])
        btns.addWidget(QLabel("Format :"))
        btns.addWidget(self.format_combo)
        btns.addStretch()
        self.export_btn = QPushButton("Exporter le projet a cette date")
        self.export_btn.clicked.connect(self._export)
        btns.addWidget(self.export_btn)
        layout.addLayout(btns)

        self.setLayout(layout)

        self._timestamps = []   # liste des timestamps tries
        self._events = []       # file_events

    def initializePage(self):
        sess = config.selected_session or {}
        self._events = sess.get("file_events", []) or []
        ts = sorted({e["timestamp"] for e in self._events if e.get("timestamp")})
        self._timestamps = ts
        if not ts:
            self.summary.setText("<i>Aucun fichier touche dans cette session.</i>")
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
        self.summary.setText(f"<b>{len(files_uniq)}</b> fichier(s), <b>{len(self._events)}</b> operation(s) au total.")
        self._refresh()

    def _on_slider(self, _):
        self._refresh()

    def _refresh(self):
        if not self._timestamps:
            return
        idx = self.slider.value()
        cur_ts = self._timestamps[idx]
        self.date_cur.setText(f"Version au {_short(cur_ts)}  ({idx+1}/{len(self._timestamps)})")
        state = reconstructor.reconstruct(self._events, until_ts=cur_ts)
        self.file_list.clear()
        for fp in sorted(state.keys()):
            content = state[fp]
            if content is None:
                tag = "[Edits seulement]"
                size = "?"
            else:
                tag = "[OK]"
                size = f"{len(content)} car."
            it = QListWidgetItem(f"{tag}  {fp}    {size}")
            it.setData(Qt.ItemDataRole.UserRole, (fp, content))
            self.file_list.addItem(it)
        self._current_state = state

    def _export(self):
        if not getattr(self, "_current_state", None):
            QMessageBox.warning(self, "Export", "Aucun fichier a exporter.")
            return
        fmt = self.format_combo.currentText()
        if fmt == "Dossier":
            d = QFileDialog.getExistingDirectory(self, "Choisir le dossier de destination")
            if not d:
                return
            written, skipped = exporter.export_to_folder(self._current_state, d)
        else:
            f, _ = QFileDialog.getSaveFileName(self, "Enregistrer l'archive", "export-claude.zip", "Archive ZIP (*.zip)")
            if not f:
                return
            written, skipped = exporter.export_to_zip(self._current_state, f)
        msg = f"{len(written)} fichier(s) exporte(s)."
        if skipped:
            msg += f"\n{len(skipped)} fichier(s) ignore(s) (contenu non reconstituable)."
        QMessageBox.information(self, "Export termine", msg)


def _short(ts):
    if not ts:
        return "--"
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ts[:16]
