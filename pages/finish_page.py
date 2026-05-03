from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWizardPage, QVBoxLayout, QLabel, QWizard
from PyQt5.QtGui import QFont, QPixmap

from service.resources import resource_path
from service import i18n
from service.i18n import tr


class FinishPage(QWizardPage):
    def __init__(self):
        super().__init__()

        watermark = QPixmap(resource_path("assets/banner.png"))
        watermark = watermark.scaledToHeight(402)
        self.setPixmap(QWizard.WizardPixmap.WatermarkPixmap, watermark)

        layout = QVBoxLayout()
        title_font = QFont(); title_font.setBold(True); title_font.setPixelSize(17)
        self.title_label = QLabel()
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        self.body_label = QLabel()
        self.body_label.setWordWrap(True)
        self.body_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_label.setStyleSheet("padding: 10px;")
        layout.addWidget(self.body_label)
        layout.addStretch()
        self.setLayout(layout)

        self._retranslate()
        i18n.signaler.language_changed.connect(self._retranslate)

    def _retranslate(self, *_):
        self.title_label.setText(tr("finish.title"))
        self.body_label.setText(tr("finish.body"))

    def initializePage(self):
        QTimer.singleShot(0, self._tweak_buttons)

    def _tweak_buttons(self):
        w = self.wizard()
        if not w:
            return
        w.button(QWizard.WizardButton.BackButton).setDisabled(False)
        w.button(QWizard.WizardButton.NextButton).hide()
        w.button(QWizard.WizardButton.CancelButton).setDisabled(True)
        w.button(QWizard.WizardButton.FinishButton).show()
