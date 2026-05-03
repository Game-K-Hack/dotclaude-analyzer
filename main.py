import sys
import webbrowser
from PyQt5.QtWidgets import QApplication, QWizard, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from service.resources import resource_path
from service.updater import UpdateChecker, RELEASES_PAGE_URL
from pages.welcome_page import WelcomePage
from pages.source_page import SourcePage
from pages.settings_page import SettingsPage
from pages.project_page import ProjectPage
from pages.files_page import FilesPage
from pages.finish_page import FinishPage


class MainWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path('assets/logo.ico')))
        self.setWindowTitle("DotClaude Analyzer")
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setFixedSize(600, 450)

        self._update_checker = UpdateChecker(self)
        self._update_checker.update_available.connect(self._on_update_available)
        self._update_checker.start()

        self.addPage(WelcomePage())
        self.addPage(SourcePage())
        self.addPage(SettingsPage())
        self.addPage(ProjectPage())
        self.addPage(FilesPage())
        self.addPage(FinishPage())

        self.setButtonText(QWizard.WizardButton.BackButton, "< Precedent")
        self.setButtonText(QWizard.WizardButton.NextButton, "Suivant >")
        self.setButtonText(QWizard.WizardButton.FinishButton, "Terminer")
        self.setButtonText(QWizard.WizardButton.CancelButton, "Annuler")

        self.setStyleSheet("""
            QWizard { background-color: #f5f5f5; }
            QWizardPage { background-color: white; }
            QPushButton {
                padding: 5px 10px;
                background-color: #ffffff;
                color: black;
                border: 1px solid #cccccc;
                border-radius: 3px;
                min-width: 90px;
            }
            QPushButton:hover { background-color: #f0f0f0; }
            QPushButton:disabled { background-color: #e0e0e0; color: #555; }
            QLineEdit, QComboBox {
                padding: 5px; border: 1px solid #cccccc; border-radius: 3px;
            }
            QListWidget, QTextEdit, QTabWidget::pane {
                border: 1px solid #cccccc; border-radius: 3px;
            }
            QSlider::groove:horizontal {
                height: 6px; background: #ddd; border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #0078d4; width: 14px; margin: -5px 0; border-radius: 7px;
            }
        """)


    def _on_update_available(self, current: str, latest: str):
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Information)
        box.setWindowTitle("Mise a jour disponible")
        box.setText(
            f"Une nouvelle version est disponible.\n\n"
            f"Version actuelle : {current}\n"
            f"Derniere version : {latest}"
        )
        open_btn = box.addButton("Telecharger", QMessageBox.ButtonRole.AcceptRole)
        box.addButton("Plus tard", QMessageBox.ButtonRole.RejectRole)
        box.exec_()
        if box.clickedButton() is open_btn:
            webbrowser.open(RELEASES_PAGE_URL)


def main():
    app = QApplication(sys.argv)
    try:
        app.setStyle("WindowsVista")
    except Exception:
        pass
    w = MainWizard()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
