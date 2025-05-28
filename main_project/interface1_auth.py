import tkinter as tk
from fonctions.gestion_identifiants import verifier_identifiants, initialiser_fichier
#from interfaces.interface2_menu import InterfaceMenu
from reel import Ui_MainWindow
from PIL import Image, ImageTk
import os

class LancementApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Application Automate")
        # Dimensions de la fenêtre
        largeur = 1000
        hauteur = 600

# Dimensions de l'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

# Coordonnées pour centrer
        x = (screen_width // 2) - (largeur // 2)
        y = (screen_height // 2) - (hauteur // 2)

# Appliquer la géométrie centrée
        self.geometry(f"{largeur}x{hauteur}+{x}+{y}")

        self.fullscreen = False
        self.attributes("-fullscreen", False)

        initialiser_fichier()
        self.config(bg="white")

        # Barre personnalisée
        self.barre = tk.Frame(self, bg="#e0f0ff", height=30)
        self.barre.pack(fill="x", side="top")
        self._ajouter_boutons_fenetre()

        # Zone centrale
        self.frame = tk.Frame(self, bg="white")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.frame, text="Nom d'utilisateur :", font=("Arial", 16), bg="white").pack(pady=10)
        self.nom_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.nom_entry.pack()

        tk.Label(self.frame, text="Mot de passe :", font=("Arial", 16), bg="white").pack(pady=10)
        self.mdp_entry = tk.Entry(self.frame, show="*", font=("Arial", 14))
        self.mdp_entry.pack()

        self.message = tk.Label(self.frame, text="", fg="red", bg="white")
        self.message.pack(pady=5)

        tk.Button(self.frame, text="Valider", font=("Arial", 14), command=self.verifier).pack(pady=20)

        self.barre.bind("<B1-Motion>", self._move_window)
        self.barre.bind("<Button-1>", self._click_position)

    def _ajouter_boutons_fenetre(self):
        try:
            icon_path = os.path.join("assets", "iconr.png")
            icon_img = Image.open(icon_path).resize((24, 24))
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            tk.Label(self.barre, image=self.icon_photo, bg="#e0f0ff").pack(side="left", padx=8)
        except:
            tk.Label(self.barre, text="Au", font=("Arial", 12, "bold"), bg="#e0f0ff", fg="skyblue").pack(side="left", padx=10)

        tk.Label(self.barre, text="  Application Automate", bg="#e0f0ff", font=("Arial", 10)).pack(side="left")

        tk.Button(self.barre, text="–", bg="#e0f0ff", bd=0, command=self.iconify).pack(side="right", padx=5)
        tk.Button(self.barre, text="🗖", bg="#e0f0ff", bd=0, command=self.toggle_fullscreen).pack(side="right", padx=5)
        tk.Button(self.barre, text="✕", bg="#e0f0ff", bd=0, fg="red", command=self.destroy).pack(side="right", padx=5)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def _click_position(self, event):
        self._x_offset = event.x
        self._y_offset = event.y

    def _move_window(self, event):
        x = event.x_root - self._x_offset
        y = event.y_root - self._y_offset
        self.geometry(f'+{x}+{y}')

    def verifier(self):
        nom = self.nom_entry.get()
        mdp = self.mdp_entry.get()
        if verifier_identifiants(nom, mdp):
            #self.frame.destroy()
            #self.barre.destroy()
            self.destroy()
            #InterfaceMenu(self)
            ui=Ui_MainWindow()
            ui.lancer_reel_ui()
        else:
            self.message.config(text="Nom ou mot de passe incorrect")
