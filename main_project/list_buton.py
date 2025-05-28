import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QScrollArea, 
                             QInputDialog, QDialog, QListWidget, QDialogButtonBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from graphviz import Digraph
from AAutomate import Automate
from Etat import Etat
from Alphabet import Alphabet
from Transition import Transition
from isComplet import isComplet
from completeAutomate import completeAutomate
from deterministe import isDeterministe
from AFN_AFD import afn_afd
from minimiseAutomate import minimiseAutomate
from isMinimal import isMinimal

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
        left_layout.addWidget(QPushButton("Save Automaton", clicked=self.save_automate))
        left_layout.addWidget(QPushButton("List Saved Automata", clicked=self.show_saved_automata))
        left_layout.addWidget(QPushButton("Visualize Automaton", clicked=self.visualize_automate))
        left_layout.addWidget(QPushButton("Check Complete", clicked=self.check_complete))
        left_layout.addWidget(QPushButton("Complete Automaton", clicked=self.complete_automate))
        left_layout.addWidget(QPushButton("Check Deterministic", clicked=self.check_deterministic))
        left_layout.addWidget(QPushButton("Convert to DFA", clicked=self.convert_to_dfa))
        left_layout.addWidget(QPushButton("Minimize Automaton", clicked=self.minimize_automate))
        left_layout.addWidget(QPushButton("Check Minimal", clicked=self.check_minimal))

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

    def save_automate(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            filename, ok = QInputDialog.getText(self, "Save Automaton", "Enter filename (without .json):")
            if ok and filename.strip():
                self.automate.sauvegarder(filename.strip())
                self.result_text.append(f"Automaton saved to {filename}.json")
            elif not ok:
                self.result_text.append("Save canceled")
            else:
                self.result_text.append("Error: Invalid filename")
        except Exception as e:
            self.result_text.append(f"Error saving automaton: {str(e)}")

    def show_saved_automata(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Saved Automata")
        dialog.setGeometry(200, 200, 400, 300)
        layout = QVBoxLayout(dialog)

        label = QLabel("Select an automaton to load:")
        layout.addWidget(label)

        list_widget = QListWidget()
        json_files = [f for f in os.listdir(".") if f.endswith(".json")]
        if not json_files:
            list_widget.addItem("No saved automata found")
            list_widget.setEnabled(False)
        else:
            list_widget.addItems(json_files)
        layout.addWidget(list_widget)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.load_selected_automaton(list_widget, dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec_()

    def load_selected_automaton(self, list_widget, dialog):
        selected = list_widget.currentItem()
        if not selected or selected.text() == "No saved automata found":
            self.result_text.append("Error: No automaton selected")
            dialog.accept()
            return
        filename = selected.text().replace(".json", "")
        try:
            self.automate = Automate.charger(filename)
            self.states = self.automate.listEtat
            self.initial_states = self.automate.listInitiaux
            self.final_states = self.automate.listFinaux
            self.transitions = self.automate.listTransition
            self.alphabets = [Alphabet(f"a{i}", symb) for i, symb in enumerate(self.automate.alphabet)]
            self.state_map = {e.idEtat: e for e in self.states}
            self.alphabet_map = {list(a.valAlphabet)[0]: a for a in self.alphabets}
            self.result_text.append(f"Loaded automaton from {filename}.json")
            self.visualize_automate()
            dialog.accept()
        except Exception as e:
            self.result_text.append(f"Error loading {filename}.json: {str(e)}")
            dialog.accept()

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

    def check_complete(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            result = isComplet(self.automate)
            self.result_text.append(f"Automaton is complete: {result}")
        except Exception as e:
            self.result_text.append(f"Error checking completeness: {str(e)}")

    def complete_automate(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            self.automate = completeAutomate(self.automate)
            self.states = self.automate.listEtat
            self.transitions = self.automate.listTransition
            self.result_text.append("Automaton completed")
            self.visualize_automate()
        except Exception as e:
            self.result_text.append(f"Error completing automaton: {str(e)}")

    def check_deterministic(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            result = isDeterministe(self.automate)
            self.result_text.append(f"Automaton is deterministic: {result}")
        except Exception as e:
            self.result_text.append(f"Error checking deterministic: {str(e)}")

    def convert_to_dfa(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            self.automate = afn_afd(self.automate)
            self.states = self.automate.listEtat
            self.initial_states = self.automate.listInitiaux
            self.final_states = self.automate.listFinaux
            self.transitions = self.automate.listTransition
            self.result_text.append("Converted to DFA")
            self.visualize_automate()
        except Exception as e:
            self.result_text.append(f"Error converting to DFA: {str(e)}")

    def minimize_automate(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            result = minimiseAutomate(self.automate)
            if result is None:
                self.result_text.append("Error: Automaton is not deterministic")
                return
            self.automate = result
            self.states = self.automate.listEtat
            self.initial_states = self.automate.listInitiaux
            self.final_states = self.automate.listFinaux
            self.transitions = self.automate.listTransition
            self.result_text.append("Automaton minimized")
            self.visualize_automate()
        except Exception as e:
            self.result_text.append(f"Error minimizing automaton: {str(e)}")

    def check_minimal(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            result = isMinimal(self.automate)
            self.result_text.append(f"Automaton is minimal: {result}")
        except Exception as e:
            self.result_text.append(f"Error checking minimal: {str(e)}")

"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutomateGUI()
    window.show()
    sys.exit(app.exec_())"""