import os
import json
import logging
from datetime import datetime

class AutomataIndex:
    def __init__(self, index_file="automata_index.json"):
        self.index_file = index_file
        self.index = self.load_index()

    def load_index(self):
        try:
            if os.path.exists(self.index_file):
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logging.error(f"Erreur lors du chargement de l'index : {str(e)}")
            return []

    def save_index(self):
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=4)
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde de l'index : {str(e)}")

    def add_automaton(self, filename, name):
        entry = {
            "filename": filename,
            "name": name,
            "created_at": datetime.now().isoformat()
        }
        self.index = [e for e in self.index if e["filename"] != filename]
        self.index.append(entry)
        self.save_index()
        logging.info(f"Automate ajouté à l'index : {filename}")

    def delete_automaton(self, filename):
        self.index = [e for e in self.index if e["filename"] != filename]
        self.save_index()
        logging.info(f"Automate supprimé de l'index : {filename}")

    def list_automata(self):
        return self.index

    def safe_file_path(self, filename):
        base_path = os.path.abspath("automata")
        file_path = os.path.abspath(os.path.join("automata", filename))
        if not file_path.startswith(base_path):
            raise ValueError("Chemin de fichier non sécurisé")
        return file_path