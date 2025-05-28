import sys
import os
import uuid
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton,QInputDialog, QTextEdit, QScrollArea, QFileDialog, QComboBox, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from graphviz import Digraph
from AAutomate import Automate
from Etat import Etat
from Alphabet import Alphabet
from Transition import Transition
from deterministe import isDeterministe
from isComplet import isComplet
from completeAutomate import completeAutomate

class AutomataOperationsGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automata Operations")
        self.setGeometry(100, 100, 1400, 600)
        self.automate1 = None
        self.automate2 = None
        self.result_automate = None
        self.temp_files = []
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        self.showMaximized()
        # Top panel: Controls
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        # Load buttons
        self.load_button1 = QPushButton("Load First Automaton")
        self.load_button1.clicked.connect(lambda: self.load_json(1))
        control_layout.addWidget(self.load_button1)

        self.load_button2 = QPushButton("Load Second Automaton")
        self.load_button2.clicked.connect(lambda: self.load_json(2))
        control_layout.addWidget(self.load_button2)

        # Operation selection
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Union", "Intersection", "Complement"])
        control_layout.addWidget(QLabel("Select Operation:"))
        control_layout.addWidget(self.operation_combo)

        # Perform operation button
        self.perform_button = QPushButton("Perform Operation")
        self.perform_button.clicked.connect(self.perform_operation)
        self.perform_button.setEnabled(False)
        control_layout.addWidget(self.perform_button)

        self.save_button = QPushButton("save result automation ")
        self.save_button.clicked.connect(self.save_automate)
        self.save_button.setEnabled(False)
        control_layout.addWidget(self.save_button)


        main_layout.addWidget(control_panel)

        # Middle panel: Results
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        main_layout.addWidget(QLabel("Automata Details & Results:"))
        main_layout.addWidget(self.result_text, 1)

        # Bottom panel: Visualizations
        vis_panel = QWidget()
        vis_layout = QHBoxLayout(vis_panel)

        # First automaton visualization
        self.scroll_area1 = QScrollArea()
        self.graph_label1 = QLabel()
        self.graph_label1.setAlignment(Qt.AlignCenter)
        self.scroll_area1.setWidget(self.graph_label1)
        self.scroll_area1.setWidgetResizable(True)
        vis_layout.addWidget(QLabel("First Automaton:"))
        vis_layout.addWidget(self.scroll_area1)

        # Second automaton visualization
        self.scroll_area2 = QScrollArea()
        self.graph_label2 = QLabel()
        self.graph_label2.setAlignment(Qt.AlignCenter)
        self.scroll_area2.setWidget(self.graph_label2)
        self.scroll_area2.setWidgetResizable(True)
        vis_layout.addWidget(QLabel("Second Automaton:"))
        vis_layout.addWidget(self.scroll_area2)

        # Result automaton visualization
        self.scroll_area3 = QScrollArea()
        self.graph_label3 = QLabel()
        self.graph_label3.setAlignment(Qt.AlignCenter)
        self.scroll_area3.setWidget(self.graph_label3)
        self.scroll_area3.setWidgetResizable(True)
        vis_layout.addWidget(QLabel("Result Automaton:"))
        vis_layout.addWidget(self.scroll_area3)

        main_layout.addWidget(vis_panel, 1)

    def load_json(self, automaton_number):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("JSON files (*"+Automate.saveExt+")")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                automate = Automate.charger(file_path)
                if automaton_number == 1:
                    self.automate1 = automate
                    self.result_text.append(f"Loaded first automaton from {file_path}")
                    self.display_automaton_details(automate, "First Automaton")
                    self.visualize_automaton(automate, self.graph_label1, "First automaton visualized")
                else:
                    self.automate2 = automate
                    self.result_text.append(f"Loaded second automaton from {file_path}")
                    self.display_automaton_details(automate, "Second Automaton")
                    self.visualize_automaton(automate, self.graph_label2, "Second automaton visualized")
                self.perform_button.setEnabled(self.automate1 is not None)
               
            except Exception as e:
                self.result_text.append(f"Error loading JSON: {str(e)}")
                if automaton_number == 1:
                    self.automate1 = None
                    self.graph_label1.clear()
                else:
                    self.automate2 = None
                    self.graph_label2.clear()
                self.perform_button.setEnabled(self.automate1 is not None)

    def display_automaton_details(self, automate, title):
        if not automate:
            return
        self.result_text.append(f"\n{title} Details:")
        self.result_text.append(f"States: {', '.join(e.idEtat for e in automate.listEtat)}")
        self.result_text.append(f"Alphabet: {', '.join(automate.alphabet)}")
        self.result_text.append(f"Initial States: {', '.join(e.idEtat for e in automate.listInitiaux)}")
        self.result_text.append(f"Final States: {', '.join(e.idEtat for e in automate.listFinaux)}")
        self.result_text.append("Transitions:")
        for t in automate.listTransition:
            symbol = next(iter(t.alphabet.valAlphabet))
            self.result_text.append(f"  {t.etatSource.idEtat} --{symbol}--> {t.etatDestination.idEtat}")

    def perform_operation(self):
        operation = self.operation_combo.currentText()
        self.result_automate = None
        self.graph_label3.clear()

        try:
            if operation == "Complement":
                if not self.automate1:
                    QMessageBox.warning(self, "Error", "First automaton is required for complement.")
                    return
                if not isDeterministe(self.automate1):
                    QMessageBox.warning(self, "Error", "Complement requires a deterministic automaton.")
                    return
                if not isComplet(self.automate1):
                    self.result_text.append("Automaton is not complete. Completing it for complement.")
                    self.automate1 = completeAutomate(self.automate1)
                self.result_automate = self.complement_automaton(self.automate1)
                self.result_text.append("\nComplement operation performed.")
            else:
                if not (self.automate1 and self.automate2):
                    QMessageBox.warning(self, "Error", "Both automata are required for union or intersection.")
                    return
                if operation == "Union":
                    self.result_automate = self.union_automata(self.automate1, self.automate2)
                    self.result_text.append("\nUnion operation performed.")
                else:  # Intersection
                    self.result_automate = self.intersection_automata(self.automate1, self.automate2)
                    self.result_text.append("\nIntersection operation performed.")

            if self.result_automate:
                self.display_automaton_details(self.result_automate, "Result Automaton")
                self.visualize_automaton(self.result_automate, self.graph_label3, "Result automaton visualized")
                self.save_button.setEnabled( self.result_automate is not None )
        except Exception as e:
            self.result_text.append(f"Error performing {operation.lower()}: {str(e)}")

    def union_automata(self, automate1, automate2):
        # Combine alphabets
        combined_alphabet = automate1.alphabet.union(automate2.alphabet)
        alphabets = [Alphabet(f"A_{s}", s) for s in combined_alphabet]

        # Create product states
        states = []
        initial_states = []
        final_states = []
        state_map = {}
        for s1 in automate1.listEtat:
            for s2 in automate2.listEtat:
                state_id = f"{s1.idEtat}_{s2.idEtat}"
                is_initial = s1 in automate1.listInitiaux and s2 in automate2.listInitiaux
                is_final = s1 in automate1.listFinaux or s2 in automate2.listFinaux
                state_type = "normal"
                if is_initial:
                    state_type = "initial"
                if is_final:
                    state_type = "final" if state_type == "normal" else "initial_final"
                state = Etat(state_id, state_id, state_type)
                states.append(state)
                state_map[(s1.idEtat, s2.idEtat)] = state
                if is_initial:
                    initial_states.append(state)
                if is_final:
                    final_states.append(state)

        # Create transitions
        transitions = []
        for (s1_id, s2_id), state in state_map.items():
            s1 = next(s for s in automate1.listEtat if s.idEtat == s1_id)
            s2 = next(s for s in automate2.listEtat if s.idEtat == s2_id)
            for symbol in combined_alphabet:
                next_s1_id = automate1.transition_suivante(s1_id, symbol) if symbol in automate1.alphabet else None
                next_s2_id = automate2.transition_suivante(s2_id, symbol) if symbol in automate2.alphabet else None
                if next_s1_id and next_s2_id:
                    next_state = state_map.get((next_s1_id, next_s2_id))
                    if next_state:
                        t_id = f"t_{s1_id}_{s2_id}_{symbol}_{next_s1_id}_{next_s2_id}"
                        transitions.append(Transition(t_id, state, next_state, Alphabet(f"A_{symbol}", symbol)))

        return Automate(
            alphabets=alphabets,
            etats=states,
            initiaux=initial_states,
            finaux=final_states,
            transitions=transitions
        )

    def intersection_automata(self, automate1, automate2):
        # Combine alphabets
        combined_alphabet = automate1.alphabet.union(automate2.alphabet)
        alphabets = [Alphabet(f"A_{s}", s) for s in combined_alphabet]

        # Create product states
        states = []
        initial_states = []
        final_states = []
        state_map = {}
        for s1 in automate1.listEtat:
            for s2 in automate2.listEtat:
                state_id = f"{s1.idEtat}_{s2.idEtat}"
                is_initial = s1 in automate1.listInitiaux and s2 in automate2.listInitiaux
                is_final = s1 in automate1.listFinaux and s2 in automate2.listFinaux
                state_type = "normal"
                if is_initial:
                    state_type = "initial"
                if is_final:
                    state_type = "final" if state_type == "normal" else "initial_final"
                state = Etat(state_id, state_id, state_type)
                states.append(state)
                state_map[(s1.idEtat, s2.idEtat)] = state
                if is_initial:
                    initial_states.append(state)
                if is_final:
                    final_states.append(state)

        # Create transitions
        transitions = []
        for (s1_id, s2_id), state in state_map.items():
            s1 = next(s for s in automate1.listEtat if s.idEtat == s1_id)
            s2 = next(s for s in automate2.listEtat if s.idEtat == s2_id)
            for symbol in combined_alphabet:
                next_s1_id = automate1.transition_suivante(s1_id, symbol) if symbol in automate1.alphabet else None
                next_s2_id = automate2.transition_suivante(s2_id, symbol) if symbol in automate2.alphabet else None
                if next_s1_id and next_s2_id:
                    next_state = state_map.get((next_s1_id, next_s2_id))
                    if next_state:
                        t_id = f"t_{s1_id}_{s2_id}_{symbol}_{next_s1_id}_{next_s2_id}"
                        transitions.append(Transition(t_id, state, next_state, Alphabet(f"A_{symbol}", symbol)))

        return Automate(
            alphabets=alphabets,
            etats=states,
            initiaux=initial_states,
            finaux=final_states,
            transitions=transitions
        )


#
    def save_automate(self):
        if not self.result_automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            filename, ok = QInputDialog.getText(self, "Save Automaton", "Enter filename (without .json):")
            if ok and filename.strip():
                self.result_automate.sauvegarder(filename.strip())
                self.result_text.append(f"Automaton saved to {filename}.json")
            elif not ok:
                self.result_text.append("Save canceled")
            else:
                self.result_text.append("Error: Invalid filename")
        except Exception as e:
            self.result_text.append(f"Error saving automaton: {str(e)}")
#


    def complement_automaton(self, automate):
        # Copy automaton
        new_automate = Automate(
            alphabets=[Alphabet(f"A_{s}", s) for s in automate.alphabet],
            etats=automate.listEtat.copy(),
            initiaux=automate.listInitiaux.copy(),
            finaux=automate.listFinaux.copy(),
            transitions=automate.listTransition.copy()
        )
        # Swap final and non-final states
        new_automate.finaux.clear()
        for state in new_automate.listEtat:
            is_final = state not in automate.listFinaux
            state.typeEtat = "final" if is_final else "normal"
            if state in new_automate.listInitiaux and is_final:
                state.typeEtat = "initial_final"
            elif state in new_automate.listInitiaux:
                state.typeEtat = "initial"
            if is_final:
                new_automate.finaux.add(state)
        return new_automate

    def visualize_automaton(self, automate, label, message):
        if not automate:
            self.result_text.append("Error: No automaton to visualize")
            return
        try:
            filename = f"automaton_{uuid.uuid4().hex}"
            dot = Digraph()
            dot.attr(size='6,6')
            for s in automate.listEtat:
                shape = "doublecircle" if s in automate.listFinaux else "circle"
                dot.node(s.idEtat, shape=shape)
            for t in automate.listTransition:
                symbol = next(iter(t.alphabet.valAlphabet))
                dot.edge(t.etatSource.idEtat, t.etatDestination.idEtat, label=symbol)
            for i in automate.listInitiaux:
                dot.node(f"start_{i.idEtat}", shape="point")
                dot.edge(f"start_{i.idEtat}", i.idEtat)
            dot.render(filename, format="png", cleanup=False)
            pixmap = QPixmap(f"{filename}.png")
            if pixmap.isNull():
                raise ValueError("Failed to load generated image")
            if pixmap.width() > 400 or pixmap.height() > 400:
                pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            self.temp_files.extend([f"{filename}.png", filename])
            self.result_text.append(message)
        except Exception as e:
            self.result_text.append(f"Error visualizing automaton: {str(e)}")
            label.clear()

    def closeEvent(self, event):
        for f in self.temp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
        self.temp_files.clear()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutomataOperationsGUI()
    window.show()
    sys.exit(app.exec_())