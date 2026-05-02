from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWizardPage, QVBoxLayout, QLabel, QWizard
from PyQt5.QtGui import QFont
from pages.welcome_page import _make_watermark


class FinishPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setPixmap(QWizard.WizardPixmap.WatermarkPixmap, _make_watermark())

        layout = QVBoxLayout()
        title_font = QFont(); title_font.setBold(True); title_font.setPixelSize(17)
        title = QLabel("Inspection terminee")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        body = QLabel(
            "Merci d'avoir utilise Inspecteur Claude.\n\n"
            "Vous pouvez relancer l'assistant a tout moment pour explorer\n"
            "d'autres projets ou exporter d'autres versions.\n\n"
            "Cliquez sur 'Terminer' pour quitter."
        )
        body.setWordWrap(True)
        body.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.setStyleSheet("padding: 10px;")
        layout.addWidget(body)
        layout.addStretch()
        self.setLayout(layout)

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
