import tkinter as tk
import customtkinter as ctk
from tkinter.font import nametofont
from PIL import Image
from tkinter import StringVar, ttk, messagebox
from view.config import config
from control.product_control import ProductController
from control.purshase_control import PurshaseController

# Class pour géré l'affichage et la gestion de stock
class StockMgmt(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master
        self.username = StringVar()

        self.frame = tk.Frame(self.master, bg=config.background)
        self.frame.pack()
        
        self.btn_collection = tk.Label(self.frame, pady=20, bg=config.background)
        self.btn_collection.grid(row=0, column=0)

        image_display = ctk.CTkImage(Image.open("images/display.png"), size=(30, 30))        
        self.btn_aff = ctk.CTkButton(self.btn_collection, text="Afficher", image=image_display, compound="left",
                      font=("ARIAL", 20, "bold"), command=self.stocktable)
        self.btn_aff.grid(row=0, column=0, padx=10, pady=5)
        
        image_reception = ctk.CTkImage(Image.open("images/reception.png"), size=(30, 30))         
        self.btn_add = ctk.CTkButton(self.btn_collection, text="Nouveau\nRécéption", image=image_reception, compound="left",
                      font=("ARIAL", 20, "bold"), command=self.ajtqty)
        self.btn_add.grid(row=1, column=0, padx=10, pady=5)
        
        self.user_info = ctk.CTkLabel(self.frame, text="")
        self.user_info.grid(row=0, column=1, pady=20)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        config.displayed = StockReception(self.user_info)
    # Fonction pour crée un nouveau réception et ajouter les quantité des produits
    def ajtqty(self):
        try:
            int(config.displayed.qty.get())
            user_id = config.session_user.id
            if config.displayed.produit.get():
                produit = ProductController()
                product_id = produit.getproductbyname(config.displayed.produit.get())[0]["id"]
            else:
                product_id = None
            purshase = {"user_id": user_id, "product_id": product_id, "qty": int(config.displayed.qty.get())}
            purshasecontrol = PurshaseController(purshase=purshase)
            messagebox.showinfo("", purshasecontrol.add())
        except:
            messagebox.showinfo("", "Vérifier les valeurs entrer")
    
    # Fonction pour afficher tous les produits et son quantité au stock
    def stocktable(self):
        config.displayed.fermer()
        self.btn_aff.configure(state="disabled")
        self.btn_add.configure(state="disabled")
        config.displayed = StockTable(self.user_info)
    
    def fermer(self):
        self.frame.destroy()

# Fonction pour géré l'ajout de nouveau quantité
class StockReception(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master
        self.frame = tk.Frame(self.master, bg=config.background)
        self.frame.grid(row=0, column=0)
        self.qty = StringVar()
        
        ctk.CTkLabel(self.frame, text="Name", font=("Helvetica", 20,"bold"), 
                     text_color="white").grid(row=0, column=0, pady=5, padx=10, sticky="w")
        self.produit = ctk.CTkComboBox(self.frame, width=200, font=("Helvetica", 20,"bold"), values=[""])
        self.produit.grid(row=0, column=1, padx=10, sticky="w")

        self.produit.bind('<KeyRelease>', self.recherche)        

        ctk.CTkLabel(self.frame, text="Quantity", font=("Helvetica", 20,"bold"), 
                     text_color="white").grid(row=2, column=0, pady=5, padx=10, sticky="w")
        ctk.CTkEntry(self.frame, width=200, font=("Helvetica", 20,"bold"), textvariable=self.qty).grid(row=2, column=1, padx=10, sticky="w")
    
    # Fonction pour recherche un produit
    def recherche(self, event):
        pre_produits = ProductController()
        produits = []
        for produit in pre_produits.getproductbyname(self.produit.get()):
            produits.append(produit["name"])
        self.produit.configure(values=produits)


    def fermer(self):
        self.frame.destroy()

# Class pour géré l'affichage de tous les produits et son quantité
class StockTable(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)

        self.table = ttk.Treeview(self.frame, columns=("id", "name", "qty"), show="headings")
        self.table.heading("id", text="ID")
        self.table.heading("name", text="Nom Produit")
        self.table.heading("qty", text="Quantité")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('ARIAL', 16))

        self.table.column("id", width=30)
        self.table.column("name", width=280)
        self.table.column("qty", width=100)

        self.table["displaycolumns"]=("name", "qty")  # pour cacher l'identification et affiche que les autres informations de produit.

        productcontrol = ProductController()
        for i, product in enumerate(productcontrol.getall()):
            self.table.insert("", index=tk.END, values=(product["id"], product["name"], product["qty"]), tags=f"t{product['id']}")
            if i % 2:
                self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="#b386fc")
            else:
                self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="#8d85f2")
            self.table.column("name", anchor="center")
            self.table.column("qty", anchor="center")

        style = ttk.Style(self.frame)
        style.theme_use("clam")
        style.configure("Treeview", fieldbackground="#b386fc")
        style.configure("Treeview.heading", background="#8d85f2")
        nametofont("TkHeadingFont").configure(size=10, family="ARIAL", weight="bold")

        self.table.grid(row=0, column=0)

    def fermer(self):
        self.frame.destroy()