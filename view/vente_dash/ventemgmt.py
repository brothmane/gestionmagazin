import tkinter as tk
import customtkinter as ctk
from tkinter.font import nametofont
from PIL import Image
from tkinter import StringVar, ttk, messagebox, BooleanVar
from view.config import config
from control.product_control import ProductController
from control.sales_control import SalesController

# Class pour géré l'affichage et la gestion des différent opérations de ventes
class SalesMgmt(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master
        self.id = 0
        self.name = StringVar()
        self.prix = StringVar()
        self.prix.set(0.0)
        self.prix_org = StringVar()
        self.prix_org.set(0.0)
        self.qty = StringVar()
        self.qty.set(0)
        self.prix_total = StringVar()
        self.prix_total.set(0.0)
        self.lbl_prixtotal = StringVar()
        self.lbl_prixtotal.set(0.0)
        self.check_remise = BooleanVar()

        self.frame = tk.Frame(self.master, bg=config.background)
        self.frame.pack()
        
        self.firstcolumn = tk.Frame(self.frame, bg=config.background)
        self.firstcolumn.grid(row=0, column=0, padx=20)

        self.recherche_entry = ctk.CTkEntry(self.firstcolumn, width=250, placeholder_text="Rechercher")
        self.recherche_entry.grid(row=0, column=0, pady=10)

        self.recherche_entry.bind('<KeyRelease>', self.recherche)

        self.liste_produit = tk.Listbox(self.firstcolumn, width=22, font="ARIAL 15")
        self.liste_produit.grid(row=1, column=0, pady=10)

        self.liste_produit.bind("<<ListboxSelect>>", self.select_item)

        self.secondcolumn = tk.Frame(self.frame, bg=config.background)
        self.secondcolumn.grid(row=0, column=1, padx=20)

        ctk.CTkEntry(self.secondcolumn, width=250, state="disabled", textvariable=self.name).grid(row=0, column=0, columnspan=3,pady=10)
        ctk.CTkEntry(self.secondcolumn, width=110, state="disabled", textvariable=self.prix).grid(row=1, column=0, pady=10)
        ctk.CTkLabel(self.secondcolumn, text="DZD").grid(row=1, column=1, padx=4)
        check_remise = ctk.CTkCheckBox(self.secondcolumn, text="Remise", text_color="white", variable=self.check_remise)
        check_remise.grid(row=1, column=2, padx=4, sticky="e")
        check_remise.bind("<Button-1>", self.remise)
        
        self.qty_entry = ctk.CTkEntry(self.secondcolumn, width=250, placeholder_text="Qauntité", textvariable=self.qty)
        self.qty_entry.grid(row=2, column=0, columnspan=3, pady=10)
        self.qty_entry.bind('<KeyRelease>', self.calcul_total_byEvent)

        prix_total_entry = ctk.CTkLabel(self.secondcolumn)
        prix_total_entry.grid(row=3, column=0, columnspan=3, pady=10)
        ctk.CTkEntry(prix_total_entry, width=215, state="disabled", textvariable=self.prix_total).grid(row=0, column=0)
        ctk.CTkLabel(prix_total_entry, text="DZD").grid(row=0, column=1, padx=4)

        image_retour = ctk.CTkImage(Image.open("images/ajtpanier.png"), size=(30, 30))       
        ctk.CTkButton(self.secondcolumn, text="Ajouter au panier", image=image_retour, compound="left",
                      font=("ARIAL", 15, "bold"), command=self.ajt_panier).grid(row=4, column=0, columnspan=3, padx=20)

        self.theardcolumn = tk.Frame(self.frame, bg=config.background)
        self.theardcolumn.grid(row=0, column=2, padx=20)

        image_panier = ctk.CTkImage(Image.open("images/panier.png"), size=(30, 30))            
        ctk.CTkLabel(self.theardcolumn, text="Panier", image=image_panier, compound="left", text_color="white", 
                     font=("ARIAL", 20,"bold")).grid(row=0, column=0, pady=5, sticky="w")
        
        self.table = ttk.Treeview(self.theardcolumn, columns=("id", "name", "u_price", "qty", "t_price"), show="headings")
        self.table.heading("id", text="ID")
        self.table.heading("name", text="Nom Produit")
        self.table.heading("u_price", text="Prix Unité")
        self.table.heading("qty", text="Quantité")
        self.table.heading("t_price", text="Prix Total")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('ARIAL', 10))

        self.table.column("id", width=30)
        self.table.column("name", width=200)
        self.table.column("u_price", width=80)
        self.table.column("qty", width=100)
        self.table.column("t_price", width=100)

        self.table["displaycolumns"]=("name", "u_price", "qty", "t_price")  # pour cacher l'identification et affiche que les autres informations de produit.

        style = ttk.Style(self.theardcolumn)
        style.theme_use("clam")
        style.configure("Treeview", fieldbackground="#b386fc")
        style.configure("Treeview.heading", background="#8d85f2")
        nametofont("TkHeadingFont").configure(size=10, family="ARIAL", weight="bold")

        self.table.grid(row=1, column=0, columnspan=2)

        self.table.bind("<Delete>", self.remove_item)
      
        ctk.CTkButton(self.theardcolumn, text="Valider le panier", compound="left",
                      font=("ARIAL", 15, "bold"), command=self.valid_panier).grid(row=2, column=0, padx=20, sticky="w")

        totaldisplay = tk.Frame(self.theardcolumn, bg=config.background)
        totaldisplay.grid(row=2, column=1, pady=5, sticky="e")
        ctk.CTkLabel(totaldisplay, text="Total :", text_color="white", font=("ARIAL", 15,"bold")).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(totaldisplay, textvariable=self.lbl_prixtotal, text_color="white", font=("ARIAL", 15,"bold")).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(totaldisplay, text="DZD", text_color="white", font=("ARIAL", 15,"bold")).grid(row=0, column=2, padx=5)
        

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    # Fonction pour chercher les éléments où son caractères match dans la base de donnèes.
    def recherche(self, event):        
        produitcontrol = ProductController()
        list_produit = produitcontrol.getproductbyname(self.recherche_entry.get())

        self.liste_produit.delete(0, "end") 
        for produit in list_produit:
            self.liste_produit.insert("end", produit["name"])

    # Fonction pour prend l'élément selectionner dans la listebox et obtenir ces information à partir la base de données
    def select_item(self, event):
        produitcontrol = ProductController()
        for i in self.liste_produit.curselection():
            produits = produitcontrol.getproductbyname(self.liste_produit.get(i), for_sale=True)
            produit = produits[0]
            self.id = produit["id"]
            self.name.set(produit["name"])
            self.prix.set(produit["price"])
            self.prix_org.set(produit["price"])
            self.qty.set(0)
            self.prix_total.set(0.0)
            self.check_remise.set(False)
        
    # Fonction pour calculer le total de quantité demander
    def calcul_total(self):
        self.prix_total.set(0.0)
        if self.qty_entry.get():
            self.prix_total.set(int(self.qty_entry.get()) * float(self.prix.get()))
    
    # Fonction pour utiliser la fonction précédent de calcule en cas d'une suivi d'une événement spécifique.
    def calcul_total_byEvent(self, event):
        self.calcul_total()
    
    # Fonction pour ajouter les produits demander au panier.
    def ajt_panier(self):
        if float(self.prix_total.get()) != 0.0:
            index = self.table.index(self.table.insert("", index=tk.END, 
                                                values=(self.id, self.name.get(), self.prix.get(), self.qty.get(), self.prix_total.get()),
                                                tags=f"t{self.id}"))
            if index % 2:
                self.table.tag_configure(f"t{self.id}", font=("ARIAL", 12), background="#b386fc")
            else:
                self.table.tag_configure(f"t{self.id}", font=("ARIAL", 12), background="#8d85f2")

            self.table.column("name", anchor="center")
            self.table.column("u_price", anchor="center")
            self.table.column("qty", anchor="center")
            self.table.column("t_price", anchor="center")

            self.lbl_prixtotal.set(float(self.lbl_prixtotal.get()) + float(self.prix_total.get()))
     
        else:
            messagebox.showwarning("Attention", "Vérifier les valeurs entrer.")
    
    # Fonction pour supprimer les éléments ajouter par érreur au tableau
    def remove_item(self, event):
        selected_items = self.table.selection()
        if selected_items:
            if messagebox.askquestion("", "Etes-vous sûr de vouloir supprimer l'article du panier ?") == "yes":        
                for selected_item in selected_items: 
                    item = self.table.item(selected_item)
                    self.lbl_prixtotal.set(float(self.lbl_prixtotal.get()) - float(item["values"][4]))     
                    self.table.delete(selected_item)

    # Fonction pour valider le panier après l'accomplissement de la vente
    def valid_panier(self):
        salescontrol = SalesController()
        salescontrol.set_sale(sale={"user_id":config.session_user.id, "total_amount":float(self.lbl_prixtotal.get())})
        for value in self.table.get_children():
            salescontrol.set_saledetails({"product_id": self.table.item(value)["values"][0],
                                          "qty":self.table.item(value)["values"][3],
                                          "price":self.table.item(value)["values"][2]
                                          })
        check = salescontrol.validpanier()
        if check == "Vente enregistrer.":
            for row in self.table.get_children():
                self.table.delete(row)
            self.lbl_prixtotal.set(0.0)

        messagebox.showinfo("", check)
    
    # Fonction pour faire la remise de prix de 5% 
    def remise(self, event):
        if self.check_remise.get():
            price = float(self.prix_org.get())
            self.prix.set(price - (price * 0.05))
            self.calcul_total()
        else:
            self.prix.set(self.prix_org.get())
            self.calcul_total()

    # Function pour fermer l'interface généré par cette class.
    def fermer(self):
        self.frame.destroy()