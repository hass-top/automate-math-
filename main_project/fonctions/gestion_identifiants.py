import os
from cryptography.fernet import Fernet

# ✅ Clé Fernet valide (44 caractères encodés en base64)
FERNET_KEY = b'MUAKNH8rL8XsUwRpqbtS_25rsLVDJ_bASaKZ4K-XMFE='
CLE_CRYPTEE = Fernet(FERNET_KEY)

CHEMIN_FICHIER = "data/identifiants.txt"

# Identifiants par défaut
CLES = {
    "root": "root"
}

def crypter(texte):
    """Crypte une chaîne de texte avec Fernet."""
    return CLE_CRYPTEE.encrypt(texte.encode()).decode()

def decrypter(texte):
    """Décrypte une chaîne de texte avec Fernet."""
    return CLE_CRYPTEE.decrypt(texte.encode()).decode()

def initialiser_fichier():
    """Crée le fichier des identifiants avec cryptage si inexistant."""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(CHEMIN_FICHIER):
        with open(CHEMIN_FICHIER, "w") as f:
            for nom, mdp in CLES.items():
                ligne = crypter(f"{nom}:{mdp}")
                f.write(ligne + "\n")

def verifier_identifiants(nom, mdp):
    if nom == "root" and mdp == "root":
        return True
    
"""def verifier_identifiants(nom, mdp):
    Vérifie si les identifiants saisis sont corrects.
    if not os.path.exists(CHEMIN_FICHIER):
        return False

    with open(CHEMIN_FICHIER, "r") as f:
        lignes = f.readlines()
        for ligne in lignes:
            try:
                texte = decrypter(ligne.strip())
                nom_f, mdp_f = texte.split(":")
                if nom == nom_f and mdp == mdp_f:
                    return True
            except:
                continue
    return False"""
