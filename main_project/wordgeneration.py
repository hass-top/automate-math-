import sys
import os
import uuid
from collections import deque
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTextEdit, QScrollArea, QFileDialog, QLineEdit, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from graphviz import Digraph
from AAutomate import Automate
from Etat import Etat
from Alphabet import Alphabet
from Transition import Transition
from testMot import testMot_automate

class WordGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accepted and Rejected Words Generator")
        self.setGeometry(100, 100, 1200, 600)
        self.automate = None
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

        # Load JSON button
        self.load_button = QPushButton("Load Automaton")
        self.load_button.clicked.connect(self.load_json)
        left_layout.addWidget(self.load_button)

        # Test Mot field
        left_layout.addWidget(QLabel("Tester un mot: "))
        self.input_mot = QLineEdit()
        self.input_mot.setPlaceholderText("entre un mot contient uniquement les lettre dans l'alpabet")
        left_layout.addWidget(self.input_mot)
        self.test_mot_button = QPushButton("Tester")
        self.test_mot_button.clicked.connect(self.testMot)
        self.test_mot_button.setEnabled(False)
        left_layout.addWidget(self.test_mot_button)
        
        # Max length input
        left_layout.addWidget(QLabel("Maximum Word Length:"))
        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Enter max word length (e.g., 5)")
        left_layout.addWidget(self.length_input)

        # Generate accepted words button
        self.generate_accepted_button = QPushButton("Generate Accepted Words")
        self.generate_accepted_button.clicked.connect(self.generate_accepted_words)
        self.generate_accepted_button.setEnabled(False)
        left_layout.addWidget(self.generate_accepted_button)

        # Generate rejected words button
        self.generate_rejected_button = QPushButton("Generate Rejected Words")
        self.generate_rejected_button.clicked.connect(self.generate_rejected_words)
        self.generate_rejected_button.setEnabled(False)
        left_layout.addWidget(self.generate_rejected_button)

        # Result display
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        left_layout.addWidget(QLabel("Automaton Details & Results:"))
        left_layout.addWidget(self.result_text)

        # Right panel: Visualization
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Automaton visualization
        self.scroll_area = QScrollArea()
        self.graph_label = QLabel()
        self.graph_label.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.graph_label)
        self.scroll_area.setWidgetResizable(True)
        right_layout.addWidget(QLabel("Automaton Visualization:"))
        right_layout.addWidget(self.scroll_area)

        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)

    def load_json(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Automate files (*"+Automate.saveExt+")")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                self.automate = Automate.charger(file_path)
                self.result_text.clear()
                self.result_text.append(f"Loaded automaton from {file_path}")
                self.display_automaton_details()
                self.visualize_automaton(self.automate, self.graph_label, "Automaton visualized")
                self.generate_accepted_button.setEnabled(True)
                self.generate_rejected_button.setEnabled(True)
                self.test_mot_button.setEnabled(True)
            except Exception as e:
                self.result_text.append(f"Error loading JSON: {str(e)}")
                self.automate = None
                self.generate_accepted_button.setEnabled(False)
                self.generate_rejected_button.setEnabled(False)
                self.graph_label.clear()

    def display_automaton_details(self):
        if not self.automate:
            return
        self.result_text.append("\nAutomaton Details:")
        self.result_text.append(f"States: {', '.join(e.idEtat for e in self.automate.listEtat)}")
        self.result_text.append(f"Alphabet: {', '.join(self.automate.alphabet)}")
        self.result_text.append(f"Initial States: {', '.join(e.idEtat for e in self.automate.listInitiaux)}")
        self.result_text.append(f"Final States: {', '.join(e.idEtat for e in self.automate.listFinaux)}")
        self.result_text.append("Transitions:")
        for t in self.automate.listTransition:
            symbol = next(iter(t.alphabet.valAlphabet))
            self.result_text.append(f"  {t.etatSource.idEtat} --{symbol}--> {t.etatDestination.idEtat}")

    def generate_accepted_words(self):
        if not self.automate:
            self.result_text.append("Error: No automaton loaded")
            return
        try:
            max_length = self.length_input.text().strip()
            if not max_length.isdigit() or int(max_length) < 0:
                QMessageBox.warning(self, "Invalid Input", "Please enter a non-negative integer for max length.")
                return
            max_length = int(max_length)
            accepted_words, _ = self.generate_words(self.automate, max_length)
            self.result_text.append(f"\nAccepted Words (up to length {max_length}):")
            if accepted_words:
                self.result_text.append(", ".join(accepted_words))
            else:
                self.result_text.append("No words accepted.")
        except Exception as e:
            self.result_text.append(f"Error generating accepted words: {str(e)}")

    def generate_rejected_words(self):
        if not self.automate:
            self.result_text.append("Error: No automaton loaded")
            return
        try:
            max_length = self.length_input.text().strip()
            if not max_length.isdigit() or int(max_length) < 0:
                QMessageBox.warning(self, "Invalid Input", "Please enter a non-negative integer for max length.")
                return
            max_length = int(max_length)
            _, rejected_words = self.generate_words(self.automate, max_length)
            self.result_text.append(f"\nRejected Words (up to length {max_length}):")
            if rejected_words:
                self.result_text.append(", ".join(rejected_words))
            else:
                self.result_text.append("No words rejected.")
        except Exception as e:
            self.result_text.append(f"Error generating rejected words: {str(e)}")

    def generate_words(self, automate, max_length):
        accepted_words = set()
        rejected_words = set()
        # BFS queue: (current_state, current_word)
        queue = deque([(init, "") for init in automate.listInitiaux])
        visited = set()  # Track (state.idEtat, word) to avoid cycles
        while queue:
            state, word = queue.popleft()
            # Check if word length is within limit
            if len(word) > max_length:
                continue
            state_word = (state.idEtat, word)
            if state_word in visited:
                continue
            visited.add(state_word)
            # Check if current state is final
            if state in automate.listFinaux and len(word) <= max_length:
                accepted_words.add(word if word else "ε")
            elif len(word) <= max_length:
                # If not final and within length, word is rejected
                if word:  # Exclude empty word unless it's accepted
                    rejected_words.add(word)
            # Explore transitions
            for symbol in automate.alphabet:
                next_state_id = automate.transition_suivante(state.idEtat, symbol)
                if next_state_id:
                    next_state = next((s for s in automate.listEtat if s.idEtat == next_state_id), None)
                    if next_state:
                        queue.append((next_state, word + symbol))
                elif len(word) < max_length:
                    # Dead-end: word + symbol is rejected
                    rejected_word = word + symbol
                    if len(rejected_word) <= max_length:
                        rejected_words.add(rejected_word)
        # Convert ε to empty string for consistency, sort for readability
        accepted_words = sorted([w if w != "ε" else "" for w in accepted_words])
        rejected_words = sorted([w for w in rejected_words])
        return accepted_words, rejected_words

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
    def testMot(self):
        testMot_automate(self.automate,self.input_mot.text(),self.result_text,self.automate.alphabet)


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
    window = WordGeneratorGUI()
    window.show()
    sys.exit(app.exec_())