import tkinter as tk
import customtkinter as ctk
from PIL import Image
from view.config import config
from view.inventaire_dash.produitmgmt import ProduitMgmt
from view.inventaire_dash.stockmgmt import StockMgmt

# Class pour géré l'affichage de menu inventaire
class Inventory(tk.Frame):
    def __init__(self, sub_frame_top, frame_bottom):
        tk.Frame.__init__(self)
        self.sub_frame_top = sub_frame_top
        self.frame_bottom = frame_bottom
        self.displayed = None

        self.frame = tk.Frame(self.sub_frame_top, bg=config.background)
        self.frame.grid(row=0, column=0)

        self.sub_frame_top.grid_rowconfigure(0, weight=1)
        self.sub_frame_top.grid_columnconfigure(0, weight=1)

        image_prdmgmt = ctk.CTkImage(Image.open("images/product-management.png"), size=(30, 30))           
        ctk.CTkButton(self.frame, text="Gestion Produit", image=image_prdmgmt, compound="left", 
                      font=("ARIAL", 14, "bold"), command=self.produitmgmt).grid(row=0, column=0, padx=20)
        
        image_stkmgmt = ctk.CTkImage(Image.open("images/inventory.png"), size=(30, 30))
        ctk.CTkButton(self.frame, text="Gestion Stock", image=image_stkmgmt, compound="left",
                      font=("ARIAL", 14, "bold"), command=self.stocktmgmt).grid(row=0, column=1, padx=20)

    # Fonction pour afficher et géré les produits
    def produitmgmt(self):
        if self.displayed == None:
            self.displayed = ProduitMgmt(self.frame_bottom)
        else:
            self.displayed.fermer()
            self.displayed = ProduitMgmt(self.frame_bottom)
    
    # Fonction pour afficher et géré le stock
    def stocktmgmt(self):
        if self.displayed == None:
            self.displayed = StockMgmt(self.frame_bottom)
        else:
            self.displayed.fermer()
            self.displayed = StockMgmt(self.frame_bottom)
        
    # Fonction pour géré la fermeture de menu inventaire   
    def fermer(self):
        self.frame.destroy()
        for widget in self.frame_bottom.winfo_children():   # Pour vider tous les widgets ouvrir dans le frame bottom
            widget.destroy()
        