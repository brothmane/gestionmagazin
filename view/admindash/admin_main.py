import tkinter as tk
import customtkinter as ctk
from PIL import Image
from view.config import config
from view.admindash.usermgmt import UserMgmt
from view.admindash.produit_rapport import ProductReport
from view.admindash.sale_rapport import SalesReport

# Class pour géré l'affichage de menu administrateur
class Administrator(tk.Frame):
    def __init__(self, sub_frame_top, frame_bottom):
        tk.Frame.__init__(self)
        self.sub_frame_top = sub_frame_top
        self.frame_bottom = frame_bottom
        self.displayed = None

        self.frame = tk.Frame(self.sub_frame_top, bg=config.background)
        self.frame.grid(row=0, column=0)

        self.sub_frame_top.grid_rowconfigure(0, weight=1)
        self.sub_frame_top.grid_columnconfigure(0, weight=1)

        image_user = ctk.CTkImage(Image.open("images/utilisateur.png"), size=(30, 30))        
        ctk.CTkButton(self.frame, text="Utilisateur", image=image_user, compound="left",
                      font=("ARIAL", 14, "bold"), command=self.utilisateur).grid(row=0, column=0, padx=20)
      
        image_produit =  ctk.CTkImage(Image.open("images/produit.png"), size=(30, 30))           
        ctk.CTkButton(self.frame, text="Produits", image=image_produit, compound="left",
                      font=("ARIAL", 14, "bold"), command=self.produit).grid(row=0, column=1, padx=20)
        
        image_rapport = ctk.CTkImage(Image.open("images/rapport.png"), size=(30, 30))           
        ctk.CTkButton(self.frame, text="Rapport", image=image_rapport, compound="left",
                      font=("ARIAL", 14, "bold"), command=self.rapport).grid(row=0, column=2, padx=20)
    
    # Fonction pour afficher et géré les utilisateurs
    def utilisateur(self):
        if self.displayed == None:
            self.displayed = UserMgmt(self.frame_bottom)
        else:
            self.displayed.fermer()
            self.displayed = UserMgmt(self.frame_bottom)
    
    # Fonction pour afficher les produits et son état dans le stock
    def produit(self):
        if self.displayed == None:
            self.displayed = ProductReport(self.frame_bottom)
        else:
            self.displayed.fermer()
            self.displayed = ProductReport(self.frame_bottom)
    
    # Fonction pour afficher les rapports journalier et mensuel
    def rapport(self):
        if self.displayed == None:
            self.displayed = SalesReport(self.frame_bottom)
        else:
            self.displayed.fermer()
            self.displayed = SalesReport(self.frame_bottom)

    # Fonction pour géré la fermeture de menu administrateur
    def fermer(self):
        self.frame.destroy()
        for widget in self.frame_bottom.winfo_children():   # Pour vider tous les widgets ouvrir dans le frame bottom
            widget.destroy()
        