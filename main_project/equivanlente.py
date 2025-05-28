import sys
import os
import uuid
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTextEdit, QScrollArea, QFileDialog, QMessageBox)
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
from minimiseAutomate import minimiseAutomate

class EquivalenceCheckGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automata Equivalence Checker")
        self.setGeometry(100, 100, 1200, 600)
        self.automate1 = None
        self.automate2 = None
        self.temp_files = []
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        self.showMaximized()
        # Left panel: Controls and results
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Load buttons
        self.load_button1 = QPushButton("Load First Automaton")
        self.load_button1.clicked.connect(lambda: self.load_json(1))
        left_layout.addWidget(self.load_button1)

        self.load_button2 = QPushButton("Load Second Automaton")
        self.load_button2.clicked.connect(lambda: self.load_json(2))
        left_layout.addWidget(self.load_button2)

        # Check equivalence button
        self.check_button = QPushButton("Check Equivalence")
        self.check_button.clicked.connect(self.check_equivalence)
        self.check_button.setEnabled(False)
        left_layout.addWidget(self.check_button)

        # Result display
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        left_layout.addWidget(QLabel("Automata Details & Results:"))
        left_layout.addWidget(self.result_text)

        # Right panel: Visualizations
        right_panel = QWidget()
        right_layout = QHBoxLayout(right_panel)

        # First automaton visualization
        self.scroll_area1 = QScrollArea()
        self.graph_label1 = QLabel()
        self.graph_label1.setAlignment(Qt.AlignCenter)
        self.scroll_area1.setWidget(self.graph_label1)
        self.scroll_area1.setWidgetResizable(True)
        right_layout.addWidget(QLabel("First Automaton:"))
        right_layout.addWidget(self.scroll_area1)

        # Second automaton visualization
        self.scroll_area2 = QScrollArea()
        self.graph_label2 = QLabel()
        self.graph_label2.setAlignment(Qt.AlignCenter)
        self.scroll_area2.setWidget(self.graph_label2)
        self.scroll_area2.setWidgetResizable(True)
        right_layout.addWidget(QLabel("Second Automaton:"))
        right_layout.addWidget(self.scroll_area2)

        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

    def load_json(self, automaton_number):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("automate files (*"+Automate.saveExt+")")
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
                self.check_button.setEnabled(self.automate1 is not None and self.automate2 is not None)
            except Exception as e:
                self.result_text.append(f"Error loading JSON: {str(e)}")
                if automaton_number == 1:
                    self.automate1 = None
                    self.graph_label1.clear()
                else:
                    self.automate2 = None
                    self.graph_label2.clear()
                self.check_button.setEnabled(self.automate1 is not None and self.automate2 is not None)

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

    def check_equivalence(self):
        if not (self.automate1 and self.automate2):
            self.result_text.append("Error: Both automata must be loaded")
            return
        try:
            equivalent, message = self.are_equivalent(self.automate1, self.automate2)
            self.result_text.append(f"\nEquivalence Check: The automata are {'equivalent' if equivalent else 'not equivalent'}")
            self.result_text.append(message)
        except Exception as e:
            self.result_text.append(f"Error checking equivalence: {str(e)}")

    def are_equivalent(self, automate1, automate2):
        # Check determinism
        if not isDeterministe(automate1) or not isDeterministe(automate2):
            return False, "Both automata must be deterministic for equivalence checking."

        # Combine alphabets
        combined_alphabet = automate1.alphabet.union(automate2.alphabet)
        # Create copies to avoid modifying originals
        a1 = Automate(
            alphabets=[Alphabet(f"A_{s}", s) for s in combined_alphabet],
            etats=automate1.listEtat.copy(),
            initiaux=automate1.listInitiaux.copy(),
            finaux=automate1.listFinaux.copy(),
            transitions=automate1.listTransition.copy()
        )
        a2 = Automate(
            alphabets=[Alphabet(f"A_{s}", s) for s in combined_alphabet],
            etats=automate2.listEtat.copy(),
            initiaux=automate2.listInitiaux.copy(),
            finaux=automate2.listFinaux.copy(),
            transitions=automate2.listTransition.copy()
        )

        # Complete automata if needed
        if not isComplet(a1):
            a1 = completeAutomate(a1)
        if not isComplet(a2):
            a2 = completeAutomate(a2)

        # Minimize automata
        min_a1 = minimiseAutomate(a1)
        min_a2 = minimiseAutomate(a2)
        if min_a1 is None or min_a2 is None:
            return False, "Error minimizing automata."

        # Compare minimized automata
        if set(min_a1.alphabet) != set(min_a2.alphabet):
            return False, "Automata have different alphabets after minimization."

        # Map states to normalized IDs
        state_map1 = {s.idEtat: f"s{i}" for i, s in enumerate(min_a1.listEtat)}
        state_map2 = {s.idEtat: f"s{i}" for i, s in enumerate(min_a2.listEtat)}

        # Compare states
        if len(min_a1.listEtat) != len(min_a2.listEtat):
            return False, "Minimized automata have different numbers of states."

        # Compare initial states
        initial1 = set(state_map1[s.idEtat] for s in min_a1.listInitiaux)
        initial2 = set(state_map2[s.idEtat] for s in min_a2.listInitiaux)
        if initial1 != initial2:
            return False, "Minimized automata have different initial states."

        # Compare final states
        final1 = set(state_map1[s.idEtat] for s in min_a1.listFinaux)
        final2 = set(state_map2[s.idEtat] for s in min_a2.listFinaux)
        if final1 != final2:
            return False, "Minimized automata have different final states."

        # Compare transitions
        transitions1 = {}
        for t in min_a1.listTransition:
            src = state_map1[t.etatSource.idEtat]
            dst = state_map1[t.etatDestination.idEtat]
            symbol = next(iter(t.alphabet.valAlphabet))
            transitions1[(src, symbol)] = dst

        transitions2 = {}
        for t in min_a2.listTransition:
            src = state_map2[t.etatSource.idEtat]
            dst = state_map2[t.etatDestination.idEtat]
            symbol = next(iter(t.alphabet.valAlphabet))
            transitions2[(src, symbol)] = dst

        if transitions1 != transitions2:
            return False, "Minimized automata have different transitions."

        return True, "The minimized automata are identical."

    def visualize_automaton(self, automate, label, message):
        if not automate:
            self.result_text.append("Error: No automaton to visualize")
            return
        try:
            filename = f"automaton_{uuid.uuid4().hex}"
            dot = Digraph()
            dot.attr(size='8,8')
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
            if pixmap.width() > 600 or pixmap.height() > 600:
                pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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

"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquivalenceCheckGUI()
    window.show()
    sys.exit(app.exec_())"""