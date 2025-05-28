import sys
import os
import uuid
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTextEdit, QScrollArea, QFileDialog, QInputDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from graphviz import Digraph
from AAutomate import Automate
from Etat import Etat
from Alphabet import Alphabet
from Transition import Transition
from isComplet import isComplet
from completeAutomate import completeAutomate

class CompleteCheckGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automaton Completeness Checker")
        self.setGeometry(100, 100, 1200, 600)
        self.automate = None
        self.original_automate = None
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
        self.load_button = QPushButton("Load JSON Automate")
        self.load_button.clicked.connect(self.load_json)
        left_layout.addWidget(self.load_button)

        # Check and complete button
        self.check_complete_button = QPushButton("Check & Complete Automate")
        self.check_complete_button.clicked.connect(self.check_and_complete)
        self.check_complete_button.setEnabled(False)
        left_layout.addWidget(self.check_complete_button)

        #save_automate

        self.save_button = QPushButton("save automate")
        self.save_button.clicked.connect(self.save_automate)
        self.save_button.setEnabled(False)
        left_layout.addWidget(self.save_button)


        # Result display
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        left_layout.addWidget(QLabel("Automaton Details & Results:"))
        left_layout.addWidget(self.result_text)

        # Right panel: Visualization
        right_panel = QWidget()
        right_layout = QHBoxLayout(right_panel)

        # First visualization (Original)
        self.scroll_area1 = QScrollArea()
        self.graph_label1 = QLabel()
        self.graph_label1.setAlignment(Qt.AlignCenter)
        self.scroll_area1.setWidget(self.graph_label1)
        self.scroll_area1.setWidgetResizable(True)
        right_layout.addWidget(QLabel("Original Automaton:"))
        right_layout.addWidget(self.scroll_area1)

        # Second visualization (Completed)
        self.scroll_area2 = QScrollArea()
        self.graph_label2 = QLabel()
        self.graph_label2.setAlignment(Qt.AlignCenter)
        self.scroll_area2.setWidget(self.graph_label2)
        self.scroll_area2.setWidgetResizable(True)
        right_layout.addWidget(QLabel("Completed Automaton:"))
        right_layout.addWidget(self.scroll_area2)

        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

    def load_json(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("*.aut")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                self.automate = Automate.charger(file_path)
                self.original_automate = self.automate
                self.result_text.clear()
                self.result_text.append(f"Loaded automaton from {file_path}")
                self.display_automaton_details()
                self.visualize_automaton(self.automate, self.graph_label1, "Original automaton visualized")
                self.check_complete_button.setEnabled(True)
                self.save_button.setEnabled(True)
                self.graph_label2.clear()
            except Exception as e:
                self.result_text.append(f"Error loading JSON: {str(e)}")
                self.automate = None
                self.original_automate = None
                self.check_complete_button.setEnabled(False)
                self.graph_label1.clear()
                self.graph_label2.clear()

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

    def check_and_complete(self):
        if not self.automate:
            self.result_text.append("Error: No automaton loaded")
            return
        try:
            is_complete = isComplet(self.automate)
            self.result_text.append(f"\nCompleteness Check: The automaton is {'complete' if is_complete else 'not complete'}")
            self.original_automate = self.automate
            self.automate = completeAutomate(self.automate)
            if not is_complete:
                self.result_text.append("Automaton completed")
                self.display_automaton_details()
                self.visualize_automaton(self.original_automate, self.graph_label1, "Original automaton visualized")
                self.visualize_automaton(self.automate, self.graph_label2, "Completed automaton visualized")
            else:
                self.result_text.append("No changes needed")
                self.visualize_automaton(self.automate, self.graph_label2, "Completed automaton visualized (no changes)")
        except Exception as e:
            self.result_text.append(f"Error checking or completing automaton: {str(e)}")
            self.graph_label2.clear()

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

    def save_automate(self):
        if not self.automate:
            self.result_text.append("Error: No automaton defined")
            return
        try:
            filename, ok = QInputDialog.getText(self, "Save Automaton", "Enter filename:")
            if ok and filename.strip():
                self.automate.sauvegarder(filename.strip())
                self.result_text.append(f"Automaton saved to {filename}.json")
            elif not ok:
                self.result_text.append("Save canceled")
            else:
                self.result_text.append("Error: Invalid filename")
        except Exception as e:
            self.result_text.append(f"Error saving automaton: {str(e)}")

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
    window = CompleteCheckGUI()
    window.show()
    sys.exit(app.exec_())"""