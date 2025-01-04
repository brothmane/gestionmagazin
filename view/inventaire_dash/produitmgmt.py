import tkinter as tk
import customtkinter as ctk
from tkinter.font import nametofont
from PIL import Image
from tkinter import StringVar, ttk, messagebox
from view.config import config
from control.product_control import ProductController

# Class pour géré les différents opérations de gestion des produits
class ProduitMgmt(tk.Frame):
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
                      font=("ARIAL", 20, "bold"), command=self.produittable)
        self.btn_aff.grid(row=0, column=0, padx=10, pady=5)
     
        image_add = ctk.CTkImage(Image.open("images/add.png"), size=(30, 30))         
        self.btn_add = ctk.CTkButton(self.btn_collection, text="Ajouter", image=image_add, compound="left",
                      font=("ARIAL", 20, "bold"), command=self.produitadd)
        self.btn_add.grid(row=1, column=0, padx=10, pady=5)
       
        image_edit = ctk.CTkImage(Image.open("images/edit.png"), size=(30, 30))           
        self.btn_mod = ctk.CTkButton(self.btn_collection, text="Modifier", image=image_edit, compound="left",
                      font=("ARIAL", 20, "bold"), command=self.produitmod)
        self.btn_mod.grid(row=2, column=0, padx=10, pady=5)
       
        image_delete = ctk.CTkImage(Image.open("images/delete.png"), size=(30, 30))    
        self.btn_sup = ctk.CTkButton(self.btn_collection, text="Supprimer", image=image_delete, compound="left",
                      font=("ARIAL", 20, "bold"), command=self.produitsup)
        self.btn_sup.grid(row=3, column=0, padx=10, pady=5)

        self.user_info = ctk.CTkLabel(self.frame, text="")
        self.user_info.grid(row=0, column=1, pady=20)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        config.displayed = ProduitDisplay(self.user_info)
    # Fonction pour géré l'ajout d'un produit
    def produitadd(self):
        productcontrol = ProductController(product=config.displayed.getproduit)
        try:
            if int(config.displayed.getproduit["minqty"]) == int(config.displayed.getproduit["normalqty"]):            
                messagebox.showinfo("", productcontrol.add())
                config.displayed.entry_init()
            elif int(config.displayed.getproduit["minqty"]) < int(config.displayed.getproduit["normalqty"]):
                messagebox.showinfo("", productcontrol.add())
                config.displayed.entry_init()
            else:
                messagebox.showwarning("Attention", "Vérifier les valeur de minimum quantité et normal quantité.")
        except:
            messagebox.showwarning("Attention", "Vérifier les valeur de minimum quantité et normal quantité.")
    
    # Fonction pour géré la modification d'un produit
    def produitmod(self):
        productcontrol = ProductController(product=config.displayed.getproduit)
        
        try:
            if int(config.displayed.getproduit["minqty"]) == int(config.displayed.getproduit["normalqty"]):            
                messagebox.showinfo("", productcontrol.edit(config.displayed.getproduit["id"]))
                config.displayed.entry_init()
            elif int(config.displayed.getproduit["minqty"]) < int(config.displayed.getproduit["normalqty"]):
                messagebox.showinfo("", productcontrol.edit(config.displayed.getproduit["id"]))
                config.displayed.entry_init()
            else:
                messagebox.showwarning("Attention", "Vérifier les valeur de minimum quantité et normal quantité.")
        except:
            messagebox.showwarning("Attention", "Vérifier les valeur de minimum quantité et normal quantité.")
    
    # Fonction pour supprimer un produit
    def produitsup(self):
        if config.displayed.getproduit["id"]:
            if messagebox.askquestion("Attention", f"Tu es sur de supprimer l'utilisateur : {config.displayed.getproduit["name"]}") == "yes":
                produitcontrol = ProductController()
                messagebox.showinfo("", produitcontrol.delete(config.displayed.getproduit["id"]))
                config.displayed.entry_init()
        else:
            messagebox.showinfo("", "Il n'y pas de produit séléctionner.")
    
    # Fonction pour afficher les produits à rechercher et en meme temps désactive la fonctionnalité des buttons d'opérations
    def produittable(self):
        config.displayed.fermer()
        self.btn_aff.configure(state="disabled")
        self.btn_add.configure(state="disabled")
        self.btn_mod.configure(state="disabled")
        self.btn_sup.configure(state="disabled")
        config.displayed = ProduitTable(self.user_info)
        config.displayed.get_btn(self.btn_aff, self.btn_add, self.btn_mod, self.btn_sup)
    
    
    def fermer(self):
        self.frame.destroy()

# Class pour afficher les entrées de saisie des informations de produit
class ProduitDisplay(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master
        self.frame = tk.Frame(self.master, bg=config.background)
        self.frame.grid(row=0, column=0)

        self.id = StringVar()
        self.name = StringVar()
        self.unit = StringVar()
        self.prix = StringVar()
        self.minqty = StringVar()
        self.minqty.set(0)
        self.normalqty = StringVar()
        self.normalqty.set(0)

        ctk.CTkLabel(self.frame, text="Name", font=("Helvetica", 20,"bold"), 
                     text_color="white").grid(row=0, column=0, pady=5, padx=10, sticky="w")
        ctk.CTkEntry(self.frame, width=200, font=("Helvetica", 20,"bold"), textvariable=self.name).grid(row=0, column=1, padx=10, sticky="w")

        ctk.CTkLabel(self.frame, text="Unité", font=("Helvetica", 20,"bold"), 
                     text_color="white").grid(row=1, column=0, pady=5, padx=10, sticky="w")
        ctk.CTkComboBox(self.frame, width=200, font=("Helvetica", 20,"bold"), 
                        values=["cm", "piéce"], state="readonly", variable=self.unit).grid(row=1, column=1, padx=10, sticky="w")

        ctk.CTkLabel(self.frame, text="Prix", font=("Helvetica", 20,"bold"), 
                     text_color="white").grid(row=2, column=0, pady=5, padx=10, sticky="w")
        ctk.CTkEntry(self.frame, width=200, font=("Helvetica", 20,"bold"), textvariable=self.prix).grid(row=2, column=1, padx=10, sticky="w")

        ctk.CTkLabel(self.frame, text="Min Quantity", font=("Helvetica", 20,"bold"), 
                     text_color="white").grid(row=4, column=0, pady=5, padx=10, sticky="w")
        ctk.CTkEntry(self.frame, width=200, font=("Helvetica", 20,"bold"), textvariable=self.minqty).grid(row=4, column=1, padx=10, sticky="w")

        ctk.CTkLabel(self.frame, text="Normal Quantity", font=("Helvetica", 20,"bold"), 
                     text_color="white").grid(row=5, column=0, pady=5, padx=10, sticky="w")
        ctk.CTkEntry(self.frame, width=200, font=("Helvetica", 20,"bold"), textvariable=self.normalqty).grid(row=5, column=1, padx=10, sticky="w")
    
    # Fonction uriliser comme un propriété pour returner les informations saisie
    @property
    def getproduit(self):
        return {"id": self.id.get(),
                "name": self.name.get(),
                "unit": self.unit.get(),
                "prix": self.prix.get(),
                "minqty": self.minqty.get(),
                "normalqty": self.normalqty.get()}

    # Fonction pour initialiser les entrées
    def entry_init(self):
        self.id.set("")
        self.name.set("")
        self.prix.set("")
        self.minqty.set(0)
        self.normalqty.set(0)

       
    def fermer(self):
        self.frame.destroy()

# Class pour afficher les noms des produits rechercher et son prix d'achat
class ProduitTable(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master
        self.frame = tk.Frame(self.master, bg=config.background)
        self.frame.grid(row=0, column=0)

        self.recherche_entry = ctk.CTkEntry(self.frame, placeholder_text="Chercher produit",
                     font=("Helvetica", 15,"bold"))
        self.recherche_entry.grid(row=0, column=0, pady=10)

        self.recherche_entry.bind('<KeyRelease>', self.recherche)
        
        self.table = ttk.Treeview(self.frame, columns=("id", "name", "price"), show="headings")
        self.table.heading("id", text="ID")
        self.table.heading("name", text="Nom Produit")
        self.table.heading("price", text="Prix")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('ARIAL', 16))

        self.table.column("id", width=30)
        self.table.column("name", width=280)
        self.table.column("price", width=100)

        self.table["displaycolumns"]=("name", "price")  # pour cacher l'identification et affiche que les autres informations de produit.


        style = ttk.Style(self.frame)
        style.theme_use("clam")
        style.configure("Treeview", fieldbackground="#b386fc")
        style.configure("Treeview.heading", background="#8d85f2")
        nametofont("TkHeadingFont").configure(size=10, family="ARIAL", weight="bold")
        
        self.table.grid(row=1, column=0, pady=10)

        self.table.bind('<ButtonRelease-1>', self.selectItem)

    # Fonction pour prend le produit séléctionner dans le tableau et l'afficher par l'appel de class ProduitDisplay
    def selectItem(self, event):
        selectedrow = self.table.focus()
        item = self.table.item(selectedrow)
        productcontrol = ProductController()
        product = productcontrol.getproductbyid(item["values"][0])
        self.btn_activate()
        config.displayed.fermer()
        config.displayed = ProduitDisplay(self.master)
        config.displayed.id.set(product["id"])
        config.displayed.name.set(product["name"])
        config.displayed.unit.set(product["unit"])
        config.displayed.prix.set(product["price"])
        config.displayed.minqty.set(product["minqty"])
        config.displayed.normalqty.set(product["normalqty"])

    # Fonction pour prend les buttons d'opérations comme paramètres
    def get_btn(self, btn_aff, btn_add, btn_mod, btn_sup):
        self.btn_aff = btn_aff
        self.btn_add = btn_add
        self.btn_mod = btn_mod
        self.btn_sup = btn_sup

    # Fonction pour active le fonctionnement des buttons d'opérations
    def btn_activate(self):
        self.btn_aff.configure(state="normal")
        self.btn_add.configure(state="normal")
        self.btn_mod.configure(state="normal")
        self.btn_sup.configure(state="normal")

    # Fonction utiliser pour la recherche des produits
    def recherche(self, event):
        produitcontrol = ProductController()
        products = produitcontrol.recherche(self.recherche_entry.get())
        
        for item in self.table.get_children():
            self.table.delete(item)
        
        if products:
            for i, product in enumerate(products):
                self.table.insert("", index=tk.END, values=(product["id"], product["name"], product["price"]), tags=f"t{product['id']}")
                if i % 2:
                    self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="#b386fc")
                else:
                    self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="#8d85f2")
                self.table.column("name", anchor="center")
                self.table.column("price", anchor="center")

    def fermer(self):
        self.frame.destroy()