import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QListWidget, QPushButton, QMessageBox
)

class DeleteAutomatonWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supprimer un automate")
        self.setGeometry(200, 200, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Sélectionnez un automate à supprimer:")
        self.layout.addWidget(self.label)

        self.list_widget = QListWidget()
        self.refresh_list()
        self.layout.addWidget(self.list_widget)

        self.delete_button = QPushButton("Supprimer l'automate sélectionné")
        self.delete_button.clicked.connect(self.delete_selected_automaton)
        self.layout.addWidget(self.delete_button)

    def refresh_list(self):
        self.list_widget.clear()
        self.json_files = [f for f in os.listdir(".") if f.endswith(".json")]
        if not self.json_files:
            self.list_widget.addItem("Aucun automate trouvé")
            self.list_widget.setEnabled(False)
        else:
            self.list_widget.setEnabled(True)
            self.list_widget.addItems(self.json_files)

    def delete_selected_automaton(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            file_name = selected_item.text()
            reply = QMessageBox.question(
                self,
                "Confirmer la suppression",
                f"Voulez-vous vraiment supprimer « {file_name} » ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    os.remove(file_name)
                    QMessageBox.information(self, "Succès", f"Fichier {file_name} supprimé.")
                    self.refresh_list()
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {e}")
        else:
            QMessageBox.warning(self, "Aucun fichier", "Veuillez sélectionner un fichier à supprimer.")

"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeleteAutomatonWindow()
    window.show()
    sys.exit(app.exec_())"""
