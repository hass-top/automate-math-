import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QScrollArea, QFrame,
                             QDialog, QListWidget, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from graphviz import Digraph
from AAutomate import Automate
from Etat import Etat
from Alphabet import Alphabet
from Transition import Transition
from isComplet import isComplet
from completeAutomate import completeAutomate

class FileListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Liste des fichiers JSON")
        self.setGeometry(200, 200, 400, 300)
        self.parent = parent
        layout = QVBoxLayout()

        # Liste des fichiers
        self.file_list = QListWidget()
        self.load_files()
        self.file_list.itemDoubleClicked.connect(self.load_selected_file)
        layout.addWidget(QLabel("Fichiers JSON disponibles (double-cliquez pour charger) :"))
        layout.addWidget(self.file_list)

        # Bouton Fermer
        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def load_files(self):
        self.file_list.clear()
        try:
            for file in os.listdir("."):
                if file.endswith(".json"):
                    self.file_list.addItem(file)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la lecture des fichiers: {str(e)}")

    def load_selected_file(self, item):
        file_name = item.text()
        base_name = os.path.splitext(file_name)[0]
        try:
            self.parent.load_automate_from_file(base_name)
            self.close()
        except FileNotFoundError:
            QMessageBox.critical(self, "Erreur", f"Fichier {file_name} introuvable")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Erreur", "Format JSON invalide")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {str(e)}")

class AutomateGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finite Automaton GUI")
        self.setGeometry(100, 100, 1200, 800)
        self.automate = None
        self.states = []
        self.alphabets = []
        self.transitions = []
        self.initial_states = []
        self.final_states = []
        self.state_map = {}
        self.alphabet_map = {}
        self.init_ui()

    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left panel: Input and controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Frame for input controls
        control_frame = QFrame()
        control_frame.setFrameShape(QFrame.StyledPanel)
        control_frame.setFrameShadow(QFrame.Raised)
        control_frame.setStyleSheet("QFrame { border: 1px solid #cccccc; padding: 10px; }")
        control_layout = QVBoxLayout(control_frame)

        # States input
        self.states_input = QLineEdit()
        self.states_input.setPlaceholderText("Entrez les états (séparés par des virgules, ex. q0,q1,q2)")
        control_layout.addWidget(QLabel("États :"))
        control_layout.addWidget(self.states_input)
        control_layout.addWidget(QPushButton("Ajouter États", clicked=self.add_states))

        # Alphabet input
        self.alphabet_input = QLineEdit()
        self.alphabet_input.setPlaceholderText("Entrez l'alphabet (séparés par des virgules, ex. a,b)")
        control_layout.addWidget(QLabel("Alphabet :"))
        control_layout.addWidget(self.alphabet_input)
        control_layout.addWidget(QPushButton("Ajouter Alphabet", clicked=self.add_alphabet))

        # Transitions input
        self.transition_input = QLineEdit()
        self.transition_input.setPlaceholderText("Entrez la transition (source,symbole,destination, ex. q0,a,q1)")
        control_layout.addWidget(QLabel("Transitions :"))
        control_layout.addWidget(self.transition_input)
        control_layout.addWidget(QPushButton("Ajouter Transition", clicked=self.add_transition))

        # Initial states input
        self.initial_input = QLineEdit()
        self.initial_input.setPlaceholderText("Entrez les états initiaux (séparés par des virgules, ex. q0)")
        control_layout.addWidget(QLabel("États Initiaux :"))
        control_layout.addWidget(self.initial_input)
        control_layout.addWidget(QPushButton("Ajouter États Initiaux", clicked=self.add_initial))

        # Final states input
        self.final_input = QLineEdit()
        self.final_input.setPlaceholderText("Entrez les états finaux (séparés par des virgules, ex. q1)")
        control_layout.addWidget(QLabel("États Finaux :"))
        control_layout.addWidget(self.final_input)
        control_layout.addWidget(QPushButton("Ajouter États Finaux", clicked=self.add_final))

        # Operation buttons
        control_layout.addWidget(QPushButton("Créer Automate", clicked=self.create_automate))
        control_layout.addWidget(QPushButton("Visualiser Automate", clicked=self.visualize_automate))
        control_layout.addWidget(QPushButton("Vérifier Complétude", clicked=self.check_complete))
        control_layout.addWidget(QPushButton("Compléter Automate", clicked=self.complete_automate))
        control_layout.addWidget(QPushButton("Sauvegarder Automate", clicked=self.save_automate))
        control_layout.addWidget(QPushButton("Voir tous les fichiers", clicked=self.show_file_list))

        # Add frame to left layout
        left_layout.addWidget(control_frame)

        # Results display
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        left_layout.addWidget(QLabel("Résultats :"))
        left_layout.addWidget(self.result_text)

        # Right panel: Graph visualization
        self.right_panel = QWidget()
        layout = QHBoxLayout()

        # First section
        self.scroll_area1 = QScrollArea()
        self.graph_label1 = QLabel()
        self.graph_label1.setAlignment(Qt.AlignCenter)
        self.scroll_area1.setWidget(self.graph_label1)
        self.scroll_area1.setWidgetResizable(True)
        layout.addWidget(self.scroll_area1)

        # Second section
        self.scroll_area2 = QScrollArea()
        self.graph_label2 = QLabel()
        self.graph_label2.setAlignment(Qt.AlignCenter)
        self.scroll_area2.setWidget(self.graph_label2)
        self.scroll_area2.setWidgetResizable(True)
        layout.addWidget(self.scroll_area2)

        # Set the layout for the right panel
        self.right_panel.setLayout(layout)

        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.right_panel, 2)

    def add_states(self):
        states = self.states_input.text().strip().split(",")
        if not states or not all(s.strip() for s in states):
            self.result_text.append("Erreur: Entrée des états invalide")
            return
        self.states = []
        self.state_map = {}
        for i, s in enumerate(states):
            s = s.strip()
            e = Etat(s, s, "normal")
            self.states.append(e)
            self.state_map[s] = e
        self.result_text.append(f"États ajoutés: {', '.join(states)}")

    def add_alphabet(self):
        symbols = self.alphabet_input.text().strip().split(",")
        if not symbols or not all(s.strip() for s in symbols):
            self.result_text.append("Erreur: Entrée de l'alphabet invalide")
            return
        self.alphabets = []
        self.alphabet_map = {}
        for i, s in enumerate(symbols):
            s = s.strip()
            a = Alphabet(f"a{i}", s)
            self.alphabets.append(a)
            self.alphabet_map[s] = a
        self.result_text.append(f"Alphabet ajouté: {', '.join(symbols)}")

    def add_transition(self):
        trans = self.transition_input.text().strip().split(",")
        if len(trans) != 3 or not all(t.strip() for t in trans):
            self.result_text.append("Erreur: Format de transition invalide (source,symbole,destination)")
            return
        source, symbol, dest = [t.strip() for t in trans]
        if source not in self.state_map or dest not in self.state_map:
            self.result_text.append("Erreur: État source ou destination non trouvé")
            return
        if symbol not in self.alphabet_map:
            self.result_text.append("Erreur: Symbole non présent dans l'alphabet")
            return
        t = Transition(f"{source}_{symbol}_{dest}", self.state_map[source], 
                       self.state_map[dest], self.alphabet_map[symbol])
        self.transitions.append(t)
        self.result_text.append(f"Transition ajoutée: {source},{symbol},{dest}")

    def add_initial(self):
        initials = self.initial_input.text().strip().split(",")
        if not initials or not all(i.strip() for i in initials):
            self.result_text.append("Erreur: Entrée des états initiaux invalide")
            return
        self.initial_states = []
        for i in initials:
            i = i.strip()
            if i not in self.state_map:
                self.result_text.append(f"Erreur: État initial {i} non trouvé")
                return
            self.state_map[i].typeEtat = "initial"
            self.initial_states.append(self.state_map[i])
        self.result_text.append(f"États initiaux ajoutés: {', '.join(initials)}")

    def add_final(self):
        finals = self.final_input.text().strip().split(",")
        if not finals or not all(f.strip() for f in finals):
            self.result_text.append("Erreur: Entrée des états finaux invalide")
            return
        self.final_states = []
        for f in finals:
            f = f.strip()
            if f not in self.state_map:
                self.result_text.append(f"Erreur: État final {f} non trouvé")
                return
            self.state_map[f].typeEtat = "final" if self.state_map[f].typeEtat != "initial" else "initial_final"
            self.final_states.append(self.state_map[f])
        self.result_text.append(f"États finaux ajoutés: {', '.join(finals)}")

    def create_automate(self):
        if not (self.states and self.alphabets and self.transitions and self.initial_states):
            self.result_text.append("Erreur: Définition de l'automate incomplète")
            return
        try:
            self.automate = Automate(self.alphabets, self.states, self.initial_states, 
                                    self.final_states, self.transitions)
            self.result_text.append("Automate créé avec succès")
        except Exception as e:
            self.result_text.append(f"Erreur lors de la création de l'automate: {str(e)}")

    def visualize_automate(self):
        if not self.automate:
            self.result_text.append("Erreur: Aucun automate défini")
            return
        try:
            dot = Digraph()
            dot.attr(size='8,8')
            for s in self.automate.listEtat:
                shape = "doublecircle" if s in self.automate.listFinaux else "circle"
                dot.node(s.idEtat, shape=shape)
            for t in self.automate.listTransition:
                dot.edge(t.etatSource.idEtat, t.etatDestination.idEtat, label=t.alphabet.valAlphabet)
            for i in self.automate.listInitiaux:
                dot.node("start_" + i.idEtat, shape="point")
                dot.edge("start_" + i.idEtat, i.idEtat)
            dot.render("automaton", format="png", cleanup=True)
            pixmap = QPixmap("automaton.png")
            if pixmap.width() > 600 or pixmap.height() > 600:
                pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.graph_label1.setPixmap(pixmap)
            self.result_text.append("Automate visualisé dans la première section")
            self.graph_label2.clear()
        except Exception as e:
            self.result_text.append(f"Erreur lors de la visualisation: {str(e)}")

    def check_complete(self):
        if not self.automate:
            self.result_text.append("Erreur: Aucun automate défini")
            return
        try:
            result = isComplet(self.automate)
            self.result_text.append(f"L'automate est complet: {result}")
        except AttributeError as e:
            self.result_text.append(f"Erreur lors de la vérification de complétude: Attribut invalide - {str(e)}")
        except Exception as e:
            self.result_text.append(f"Erreur lors de la vérification de complétude: {str(e)}")

    def complete_automate(self):
        if not self.automate:
            self.result_text.append("Erreur: Aucun automate défini")
            return
        try:
            original_automate = Automate(
                self.automate.listAlphabets[:],
                self.automate.listEtat[:],
                self.automate.listInitiaux[:],
                self.automate.listFinaux[:],
                self.automate.listTransition[:]
            )
            self.automate = completeAutomate(self.automate)
            self.states = self.automate.listEtat
            self.transitions = self.automate.listTransition
            self.initial_states = self.automate.listInitiaux
            self.final_states = self.automate.listFinaux
            self.state_map = {e.idEtat: e for e in self.states}
            self.alphabet_map = {a.valAlphabet: a for a in self.alphabets}
            self.result_text.append("Automate complété")
            self.visualize_two_automata(original_automate, self.automate, "Original", "Complété")
        except NameError as e:
            self.result_text.append(f"Erreur lors de la complétion: Fonction ou module manquant - {str(e)}")
        except AttributeError as e:
            self.result_text.append(f"Erreur lors de la complétion: Attribut invalide - {str(e)}")
        except Exception as e:
            self.result_text.append(f"Erreur lors de la complétion: {str(e)}")

    def save_automate(self):
        if not self.automate:
            self.result_text.append("Erreur: Aucun automate défini")
            return
        try:
            file_name = f"automate_{len([f for f in os.listdir('.') if f.startswith('automate_') and f.endswith('.json')])}"
            self.automate.sauvegarder(file_name)
            self.result_text.append(f"Automate sauvegardé dans {file_name}.json")
        except Exception as e:
            self.result_text.append(f"Erreur lors de la sauvegarde: {str(e)}")

    def show_file_list(self):
        dialog = FileListDialog(self)
        dialog.exec_()

    def load_automate_from_file(self, base_name):
        try:
            self.automate = Automate.charger(base_name)
            self.states = self.automate.listEtat
            self.alphabets = self.automate.listAlphabets
            self.initial_states = self.automate.listInitiaux
            self.final_states = self.automate.listFinaux
            self.transitions = self.automate.listTransition
            self.state_map = {e.idEtat: e for e in self.states}
            self.alphabet_map = {a.valAlphabet: a for a in self.alphabets}
            self.result_text.append(f"Automate chargé depuis {base_name}.json")
            self.visualize_automate()
        except FileNotFoundError:
            self.result_text.append(f"Erreur: Fichier {base_name}.json introuvable")
        except json.JSONDecodeError:
            self.result_text.append("Erreur: Format JSON invalide")
        except Exception as e:
            self.result_text.append(f"Erreur lors du chargement de l'automate: {str(e)}")

    def visualize_two_automata(self, automate1, automate2, label1, label2):
        try:
            # Visualize first automaton
            dot1 = Digraph()
            dot1.attr(size='8,8')
            for s in automate1.listEtat:
                shape = "doublecircle" if s in automate1.listFinaux else "circle"
                dot1.node(s.idEtat, shape=shape)
            for t in automate1.listTransition:
                dot1.edge(t.etatSource.idEtat, t.etatDestination.idEtat, label=t.alphabet.valAlphabet)
            for i in automate1.listInitiaux:
                dot1.node("start_" + i.idEtat, shape="point")
                dot1.edge("start_" + i.idEtat, i.idEtat)
            dot1.render("automaton1", format="png", cleanup=True)
            pixmap1 = QPixmap("automaton1.png")
            if pixmap1.width() > 600 or pixmap1.height() > 600:
                pixmap1 = pixmap1.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.graph_label1.setPixmap(pixmap1)

            # Visualize second automaton
            dot2 = Digraph()
            dot2.attr(size='8,8')
            for s in automate2.listEtat:
                shape = "doublecircle" if s in automate2.listFinaux else "circle"
                dot2.node(s.idEtat, shape=shape)
            for t in automate2.listTransition:
                dot2.edge(t.etatSource.idEtat, t.etatDestination.idEtat, label=t.alphabet.valAlphabet)
            for i in automate2.listInitiaux:
                dot2.node("start_" + i.idEtat, shape="point")
                dot2.edge("start_" + i.idEtat, i.idEtat)
            dot2.render("automaton2", format="png", cleanup=True)
            pixmap2 = QPixmap("automaton2.png")
            if pixmap2.width() > 600 or pixmap2.height() > 600:
                pixmap2 = pixmap2.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.graph_label2.setPixmap(pixmap2)

            self.result_text.append(f"Visualisé {label1} dans la première section et {label2} dans la deuxième section")
        except Exception as e:
            self.result_text.append(f"Erreur lors de la visualisation des automates: {str(e)}")

"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutomateGUI()
    window.show()
    sys.exit(app.exec_())"""