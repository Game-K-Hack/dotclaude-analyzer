from PyQt5.QtWidgets import QWizard, QWizardPage, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

from service.resources import resource_path
from service import i18n
from service.i18n import tr, LANGUAGES


class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()

        watermark = QPixmap(resource_path("assets/banner.png"))
        watermark = watermark.scaledToHeight(402)
        self.setPixmap(QWizard.WizardPixmap.WatermarkPixmap, watermark)

        layout = QVBoxLayout()

        title_font = QFont()
        title_font.setBold(True)
        title_font.setPixelSize(17)
        self.title_label = QLabel()
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        self.body_label = QLabel()
        self.body_label.setWordWrap(True)
        self.body_label.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.body_label.setStyleSheet("padding: 10px;")
        layout.addWidget(self.body_label)
        layout.addStretch()

        lang_row = QHBoxLayout()
        self.lang_label = QLabel()
        self.lang_combo = QComboBox()
        for code, name in LANGUAGES.items():
            self.lang_combo.addItem(name, code)
        cur_idx = self.lang_combo.findData(i18n.current_lang)
        if cur_idx >= 0:
            self.lang_combo.setCurrentIndex(cur_idx)
        self.lang_combo.currentIndexChanged.connect(self._on_lang_changed)
        lang_row.addStretch()
        lang_row.addWidget(self.lang_label)
        lang_row.addWidget(self.lang_combo)
        layout.addLayout(lang_row)

        self.setLayout(layout)

        self._retranslate()
        i18n.signaler.language_changed.connect(self._retranslate)

    def _on_lang_changed(self, idx: int):
        code = self.lang_combo.itemData(idx)
        if code:
            i18n.set_language(code)

    def _retranslate(self, *_):
        self.title_label.setText(tr("welcome.title"))
        self.body_label.setText(tr("welcome.body"))
        self.lang_label.setText(tr("welcome.language"))
        cur_idx = self.lang_combo.findData(i18n.current_lang)
        if cur_idx >= 0 and self.lang_combo.currentIndex() != cur_idx:
            self.lang_combo.blockSignals(True)
            self.lang_combo.setCurrentIndex(cur_idx)
            self.lang_combo.blockSignals(False)
