import json
import os
from Etat import Etat
from Alphabet import Alphabet
from Transition import Transition
from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet
with open("data/key.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)
class Automate:
    saveExt = '.aut'
    saveDir = './Saved_Automaton/'
    def __init__(self, alphabets=None, etats=None, initiaux=None, finaux=None, transitions=None):
        self.alphabet = set()  # Set of symbols
        self.etats = []  # List of Etat objects
        self.initiaux = set()  # Set of initial Etat objects
        self.finaux = set()  # Set of final Etat objects
        self.transitions = []  # List of Transition objects
        if alphabets is not None:
            for a in alphabets:
                self.ajouter_alphabet(a)
        if etats is not None:
            for e in etats:
                self.ajouter_etat(e)
        if initiaux is not None:
            for i in initiaux:
                if i in self.etats:
                    self.initiaux.add(i)
        if finaux is not None:
            for f in finaux:
                if f in self.etats:
                    self.finaux.add(f)
        if transitions is not None:
            for t in transitions:
                self.ajouter_transition(t)

    def ajouter_etat(self, etat):
        if etat not in self.etats:
            self.etats.append(etat)
        if "initial" in etat.typeEtat:
            self.initiaux.add(etat)
        if "final" in etat.typeEtat:
            self.finaux.add(etat)

    def ajouter_alphabet(self, alphabet):
        self.alphabet.update(alphabet.valAlphabet)

    def ajouter_transition(self, transition):
        if not isinstance(transition.alphabet.valAlphabet, set):
            transition.alphabet.valAlphabet = {transition.alphabet.valAlphabet}
        if transition.alphabet.valAlphabet.issubset(self.alphabet):
            if transition not in self.transitions:
                self.transitions.append(transition)
        else:
            raise ValueError(f"Symbol {transition.alphabet.valAlphabet} not in alphabet {self.alphabet}")

    def __repr__(self):
        return (
            f"--- AUTOMATE ---\n"
            f"États: {self.etats}\n"
            f"Initiaux: {self.initiaux}\n"
            f"Finaux: {self.finaux}\n"
            f"Alphabet: {self.alphabet}\n"
            f"Transitions:\n" + "\n".join(str(t) for t in self.transitions)
        )

    def get_etat_initial(self):
        for etat in self.etats:
            if 'initial' in etat.typeEtat:
                return etat.idEtat
        return None

    def est_etat_final(self, etat_id):
        for etat in self.etats:
            if etat.idEtat == etat_id and 'final' in etat.typeEtat:
                return True
        return False

    def transition_suivante(self, etat_id, symbole):
        for t in self.transitions:
            if t.etatSource.idEtat == etat_id and symbole in t.alphabet.valAlphabet:
                return t.etatDestination.idEtat
        return None
    def sauvegarder(self, nom_fichier):
        data = {
            'etats': [e.to_dict() for e in self.etats],
            'alphabet': list(self.alphabet),
            'transitions': [t.to_dict() for t in self.transitions]
        }
        # Sérialiser en JSON puis encoder
        json_data = json.dumps(data).encode('utf-8')

        # Chiffrer
        encrypted_data = cipher_suite.encrypt(json_data)

        nom_fichier = os.path.splitext(os.path.basename(nom_fichier))[0]
        if os.path.exists(Automate.saveDir+nom_fichier+Automate.saveExt):
            raise Exception("nom déjà existant !!")
        
        with open(Automate.saveDir+nom_fichier+Automate.saveExt, 'wb') as f:
            f.write(encrypted_data)
        print(f"Automate sauvegardé de manière sécurisée dans {nom_fichier}.aut")

        #################################

    """def sauvegarder(self, nom_fichier):
        data = {
            'etats': [e.to_dict() for e in self.etats],
            'alphabet': list(self.alphabet),
            'transitions': [t.to_dict() for t in self.transitions]
        }
        nom_fichier = os.path.splitext(os.path.basename(nom_fichier))[0]
        if not os.path.exists(Automate.saveDir):
            try:
                os.mkdir(Automate.saveDir)
            except IOError as e:
                raise
        if os.path.exists(Automate.saveDir+nom_fichier+Automate.saveExt):
            raise Exception("nom déjà existant !!")
        with open(Automate.saveDir+nom_fichier + Automate.saveExt, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return"""
        

    @staticmethod
    def charger(nom_fichier):
        ext = os.path.splitext(os.path.basename(nom_fichier))[1]
        """if  ext != Automate.saveExt:
            confirm = QMessageBox.warning(None,"fichier douteux",
                                         f"l'extention '{ext}' non reconnu, Voulez vous continuer ?",
                                         QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.No:
                raise Exception("Chargement Annulé par l'utilisateur")"""
        try:
            with open(nom_fichier , 'rb') as f:
                encrypted_data = f.read()

            # Déchiffrer
            decrypted_data = cipher_suite.decrypt(encrypted_data)

            # Charger le JSON
            data = json.loads(decrypted_data.decode('utf-8'))

            # Reconstruire l’automate
            auto = Automate()
            etat_map = {}
            for e_data in data['etats']:
                e = Etat.from_dict(e_data)
                auto.ajouter_etat(e)
                etat_map[e.idEtat] = e
            alphabet_map = {}
            for i, symb in enumerate(data['alphabet']):
                a = Alphabet(f"A{i}", symb)
                auto.ajouter_alphabet(a)
                alphabet_map[symb] = a
            for t_data in data['transitions']:
                src = etat_map[t_data['src']]
                dst = etat_map[t_data['dst']]
                t = Transition(t_data['id'], src, dst, alphabet_map[t_data['symb']])
                auto.transitions.append(t)

            print(f"Automate chargé de manière sécurisée depuis {nom_fichier}.aut")
            return auto

        except FileNotFoundError:
            print(f"Erreur: Fichier {nom_fichier}.aut introuvable")
            raise
        except Exception as e:
            print(f"Erreur lors du chargement: {str(e)}")
            raise

    """def charger(nom_fichier):
        ext = os.path.splitext(os.path.basename(nom_fichier))[1]
        if  ext != Automate.saveExt:
            confirm = QMessageBox.warning(None,"fichier douteux",
                                         f"l'extention '{ext}' non reconnu, Voulez vous continuer ?",
                                         QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.No:
                raise Exception("Chargement Annulé par l'utilisateur")
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as f:
                data = json.load(f)
            auto = Automate()
            etat_map = {}
            for e_data in data['etats']:
                e = Etat.from_dict(e_data)
                auto.ajouter_etat(e)
                etat_map[e.idEtat] = e
            alphabet_map = {}
            for i, symb in enumerate(data['alphabet']):
                a = Alphabet(f"A{i}", symb)
                auto.ajouter_alphabet(a)
                alphabet_map[symb] = a
            for t_data in data['transitions']:
                src = etat_map[t_data['src']]
                dst = etat_map[t_data['dst']]
                t = Transition(t_data['id'], src, dst, alphabet_map[t_data['symb']])
                auto.transitions.append(t)
            return auto
        except Exception:
            raise"""

    def supprimer_fichier_json(self, nom_fichier):
        nom_fichier = os.path.splitext(os.path.basename(nom_fichier))[0]
        nom_fichier = Automate.saveDir+nom_fichier+Automate.saveExt
        print("ok")
        if os.path.exists(nom_fichier):
            os.remove(nom_fichier)


    def supprimer_automate(self):
        self.alphabet.clear()
        self.etats.clear()
        self.initiaux.clear()
        self.finaux.clear()
        self.transitions.clear()

    @property
    def listEtat(self):
        return self.etats

    @property
    def listInitiaux(self):
        return list(self.initiaux)

    @property
    def listFinaux(self):
        return list(self.finaux)

    @property
    def listTransition(self):
        return self.transitions