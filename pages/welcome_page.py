from PyQt5.QtWidgets import QWizard, QWizardPage, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

from service.resources import resource_path


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
        title = QLabel("Bienvenue dans DotClaude Analyzer")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        body = QLabel(
            "Cet assistant explore votre dossier .claude pour vous aider a :\n\n"
            "  - inspecter vos parametres et votre connexion ;\n"
            "  - parcourir vos projets et leurs conversations ;\n"
            "  - lister tous les fichiers crees ou modifies par Claude ;\n"
            "  - exporter une version d'un projet a une date donnee.\n\n"
            "Cliquez sur 'Suivant' pour continuer."
        )
        body.setWordWrap(True)
        body.setAlignment(Qt.AlignmentFlag.AlignJustify)
        body.setStyleSheet("padding: 10px;")
        layout.addWidget(body)
        layout.addStretch()
        self.setLayout(layout)
