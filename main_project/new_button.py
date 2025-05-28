import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QScrollArea, 
                             QInputDialog, QDialog, QListWidget, QDialogButtonBox, QFileDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

from graphviz import Digraph

from AAutomate import Automate
from Etat import Etat
from Alphabet import Alphabet
from Transition import Transition
from isComplet import isComplet

from testMot import testMot_automate
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
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        self.showMaximized()
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.states_input = QLineEdit()
        self.states_input.setPlaceholderText("Enter states (comma-separated, e.g., q0,q1,q2)")
        left_layout.addWidget(QLabel("States:"))
        left_layout.addWidget(self.states_input)
        left_layout.addWidget(QPushButton("Add States", clicked=self.add_states))

        # Bouton pour tester le mot



        self.alphabet_input = QLineEdit()
        self.alphabet_input.setPlaceholderText("Enter alphabet (comma-separated, e.g., a,b)")
        left_layout.addWidget(QLabel("Alphabet:"))
        left_layout.addWidget(self.alphabet_input)
        left_layout.addWidget(QPushButton("Add Alphabet", clicked=self.add_alphabet))

        self.transition_input = QLineEdit()
        self.transition_input.setPlaceholderText("Enter transition (source,symbol,destination, e.g., q0,a,q1)")
        left_layout.addWidget(QLabel("Transitions:"))
        left_layout.addWidget(self.transition_input)
        left_layout.addWidget(QPushButton("Add Transition", clicked=self.add_transition))

        self.initial_input = QLineEdit()
        self.initial_input.setPlaceholderText("Enter initial states (comma-separated, e.g., q0)")
        left_layout.addWidget(QLabel("Initial States:"))
        left_layout.addWidget(self.initial_input)
        left_layout.addWidget(QPushButton("Add Initial States", clicked=self.add_initial))

        self.final_input = QLineEdit()
        self.final_input.setPlaceholderText("Enter final states (comma-separated, e.g., q1)")
        left_layout.addWidget(QLabel("Final States:"))
        left_layout.addWidget(self.final_input)
        left_layout.addWidget(QPushButton("Add Final States", clicked=self.add_final))

        left_layout.addWidget(QPushButton("Create Automaton", clicked=self.create_automate))
        left_layout.addWidget(QPushButton("Visualize Automaton", clicked=self.visualize_automate))
        left_layout.addWidget(QPushButton("Save Automaton", clicked=self.save_automate)) 
        left_layout.addWidget(QPushButton("Check Complete", clicked=self.check_complete))
        left_layout.addWidget(QPushButton("List Saved Automata", clicked=self.show_saved_automata))
        left_layout.addWidget(QPushButton("Open Automaton", clicked=self.open_automaton))
        self.mot_input = QLineEdit()
        self.mot_input.setPlaceholderText("Entrer un mot (ex: aabb)")
        left_layout.addWidget(QLabel("Mot:"))
        left_layout.addWidget(self.mot_input)
        left_layout.addWidget(QPushButton("test mot ", clicked=self.testMot))
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        left_layout.addWidget(QLabel("Results:"))
        left_layout.addWidget(self.result_text)

        right_panel = QScrollArea()
        self.graph_label = QLabel()
        self.graph_label.setAlignment(Qt.AlignCenter)
        right_panel.setWidget(self.graph_label)
        right_panel.setWidgetResizable(True)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

    def add_states(self):
        states = self.states_input.text().strip().split(",")
        if not states or not all(s.strip() for s in states):
            self.result_text.append("Error: Invalid states input")
            return
        self.states = []
        self.state_map = {}
        for i, s in enumerate(states):
            s = s.strip()
            e = Etat(s, s, "normal")
            self.states.append(e)
            self.state_map[s] = e
        self.result_text.append(f"Added states: {', '.join(states)}")

    def add_alphabet(self):
        symbols = self.alphabet_input.text().strip().split(",")
        if not symbols or not all(s.strip() for s in symbols):
            self.result_text.append("Error: Invalid alphabet input")
            return
        self.alphabets = []
        self.alphabet_map = {}
        for i, s in enumerate(symbols):
            s = s.strip()
            a = Alphabet(f"a{i}", s)
            self.alphabets.append(a)
            self.alphabet_map[s] = a
        self.result_text.append(f"Added alphabet: {', '.join(symbols)}")


    def show_saved_automata(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Saved Automata")
        dialog.setGeometry(200, 200, 400, 300)
        layout = QVBoxLayout(dialog)

        label = QLabel("Select an automaton to load:")
        layout.addWidget(label)

        list_widget = QListWidget()
        if os.path.exists(Automate.saveDir):
            json_files = [f for f in os.listdir(Automate.saveDir) if f.endswith(Automate.saveExt)]
        else:
            json_files = []
        if not json_files:
            list_widget.addItem("No saved automata found")
            list_widget.setEnabled(False)
        else:
            list_widget.addItems(json_files)
        layout.addWidget(list_widget)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec_()
        if dialog.accepted:
            file = list_widget.currentItem()
            if file:

                self.load_automaton(Automate.saveDir+file.text())

        
        
        

    def add_transition(self):
        trans = self.transition_input.text().strip().split(",")
        if len(trans) != 3 or not all(t.strip() for t in trans):
            self.result_text.append("Error: Invalid transition format (source,symbol,destination)")
            return
        source, symbol, dest = [t.strip() for t in trans]
        if source not in self.state_map or dest not in self.state_map:
            self.result_text.append("Error: Source or destination state not found")
            return
        if symbol not in self.alphabet_map:
            self.result_text.append("Error: Symbol not in alphabet")
            return
        t = Transition(f"{source}_{symbol}_{dest}", self.state_map[source], 
                      self.state_map[dest], self.alphabet_map[symbol])
        self.transitions.append(t)
        self.result_text.append(f"Added transition: {source},{symbol},{dest}")

    def add_initial(self):
        initials = self.initial_input.text().strip().split(",")
        if not initials or not all(i.strip() for i in initials):
            self.result_text.append("Error: Invalid initial states input")
            return
        self.initial_states = []
        for i in initials:
            i = i.strip()
            if i not in self.state_map:
                self.result_text.append(f"Error: Initial state {i} not found")
                return
            self.state_map[i].typeEtat = "initial"
            self.initial_states.append(self.state_map[i])
        self.result_text.append(f"Added initial states: {', '.join(initials)}")

    def add_final(self):
        finals = self.final_input.text().strip().split(",")
        if not finals or not all(f.strip() for f in finals):
            self.result_text.append("Error: Invalid final states input")
            return
        self.final_states = []
        for f in finals:
            f = f.strip()
            if f not in self.state_map:
                self.result_text.append(f"Error: Final state {f} not found")
                return
            self.state_map[f].typeEtat = "final" if self.state_map[f].typeEtat != "initial" else "initial_final"
            self.final_states.append(self.state_map[f])
        self.result_text.append(f"Added final states: {', '.join(finals)}")

    def create_automate(self):
        if not (self.states and self.alphabets and self.transitions and self.initial_states):
            self.result_text.append("Error: Incomplete automaton definition")
            return
        try:
            self.automate = Automate(self.alphabets, self.states, self.initial_states, self.final_states, self.transitions)
            self.result_text.append("Automaton created successfully")
        except Exception as e:
            self.result_text.append(f"Error creating automaton: {str(e)}")

    def visualize_automate(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            dot = Digraph()
            dot.attr(size='8,8')
            
            for s in self.automate.listEtat:
                shape = "doublecircle" if s in self.automate.listFinaux else "circle"
                dot.node(s.idEtat, shape=shape)
            
            for t in self.automate.listTransition:
                label = list(t.alphabet.valAlphabet)[0]
                dot.edge(t.etatSource.idEtat, t.etatDestination.idEtat, label=label)
            
            for i in self.automate.listInitiaux:
                dot.node("start_" + i.idEtat, shape="point")
                dot.edge("start_" + i.idEtat, i.idEtat)
            dot.render("automaton", format="png", cleanup=True)
            
            pixmap = QPixmap("automaton.png")
            
            if pixmap.width() > 600 or pixmap.height() > 600:
                pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.graph_label.setPixmap(pixmap)
            self.result_text.append("Automaton visualized")
            
        except Exception as e:
            self.result_text.append(f"Error visualizing automaton: {str(e)}")
    def save_automate(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            filename, ok = QInputDialog.getText(self, "Save Automaton", "Enter filename: ")
            if ok and filename.strip():
                self.automate.sauvegarder(filename.strip())
                self.result_text.append(f"Automaton saved to {os.path.curdir +filename+Automate.saveExt}")
            elif not ok:
                self.result_text.append("Save canceled")
            else:
                self.result_text.append("Error: Invalid filename")
        except Exception as e:
            self.result_text.append(f"Error saving automaton: {str(e)}")
    def check_complete(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            result = isComplet(self.automate)
            self.result_text.append(f"Automaton is complete: {result}")
        except Exception as e:
            self.result_text.append(f"Error checking completeness: {str(e)}")
    def load_automaton(self, file_name):
        if file_name:
            try:
            
                self.automate = Automate.charger(file_name)
                self.states = self.automate.listEtat
                self.initial_states = self.automate.listInitiaux
                self.final_states = self.automate.listFinaux
                self.transitions = self.automate.listTransition
                self.alphabets = [Alphabet(f"a{i}", symb) for i, symb in enumerate(self.automate.alphabet)]
                self.state_map = {e.idEtat: e for e in self.states}
                self.alphabet_map = {list(a.valAlphabet)[0]: a for a in self.alphabets}
                self.result_text.append(f"Opened automaton from {file_name}")
                self.visualize_automate()
            except FileNotFoundError:
                self.result_text.append(f"Error: File {file_name} not found")
            except Exception as e:
                self.result_text.append(f"Error opening {file_name}: {str(e)}")
        else:
            self.result_text.append("Open canceled")
    def open_automaton(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Automaton File",
            "",
            "Automate Files (*"+Automate.saveExt+");;All Files ()"
        )
        if file_name:
            try:
                file_base = os.path.splitext(os.path.basename(file_name))[0]
                self.automate = Automate.charger(file_name)
                self.states = self.automate.listEtat
                self.initial_states = self.automate.listInitiaux
                self.final_states = self.automate.listFinaux
                self.transitions = self.automate.listTransition
                self.alphabets = [Alphabet(f"a{i}", symb) for i, symb in enumerate(self.automate.alphabet)]
                self.state_map = {e.idEtat: e for e in self.states}
                self.alphabet_map = {list(a.valAlphabet)[0]: a for a in self.alphabets}
                self.result_text.append(f"Opened automaton from {file_name}")
                self.visualize_automate()
            except FileNotFoundError:
                self.result_text.append(f"Error: File {file_name} not found")
            except Exception as e:
                self.result_text.append(f"Error opening {file_name}: {str(e)}")
        else:
            self.result_text.append("Open canceled")
    def testMot(self):
        testMot_automate(self.automate,self.mot_input.text(),self.result_text,self.alphabets)    
            
        
"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutomateGUI()
    window.show()
    sys.exit(app.exec_())"""