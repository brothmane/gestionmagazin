import tkinter as tk
import customtkinter as ctk
from PIL import Image
from view.config import config
from view.vente_dash.ventemgmt import SalesMgmt

# Class pour géré l'affichage de menu de vente
class Sales(tk.Frame):
    def __init__(self, sub_frame_top, frame_bottom):
        tk.Frame.__init__(self)
        self.sub_frame_top = sub_frame_top
        self.frame_bottom = frame_bottom
        self.displayed = None

        self.frame = tk.Frame(self.sub_frame_top, bg=config.background)
        self.frame.grid(row=0, column=0)

        self.sub_frame_top.grid_rowconfigure(0, weight=1)
        self.sub_frame_top.grid_columnconfigure(0, weight=1)

        image_sell = ctk.CTkImage(Image.open("images/sell.png"), size=(30, 30))         
        ctk.CTkButton(self.frame, text="Vente", image=image_sell, compound="left", 
                      font=("ARIAL", 20, "bold"), command=self.salesmgmt).grid(row=0, column=0, padx=20)
        
        image_retour = ctk.CTkImage(Image.open("images/retour.png"), size=(30, 30))         
        ctk.CTkButton(self.frame, text="Retour", image=image_retour, compound="left",
                      font=("ARIAL", 20, "bold"), state="disabled", command=self.retourmgmt).grid(row=0, column=1, padx=20)

        self.displayed = SalesMgmt(self.frame_bottom)

    # Fonction pour géré l'affichage gestion des ventes des produits
    def salesmgmt(self):
        if self.displayed == None:
            self.displayed = SalesMgmt(self.frame_bottom)
        else:
            self.displayed.fermer()
            self.displayed = SalesMgmt(self.frame_bottom)
    
    # Fonction pour géré l'affichage et gestion des produits retourner
    def retourmgmt(self):
        if self.displayed == None:
            pass
        else:
            self.displayed.fermer()
           
    def fermer(self):
        self.frame.destroy()
        for widget in self.frame_bottom.winfo_children():   # Pour vider tous les widgets ouvrir dans le frame bottom
            widget.destroy()
        