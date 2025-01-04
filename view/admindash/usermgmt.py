import tkinter as tk
import customtkinter as ctk
from tkinter.font import nametofont
from PIL import Image
from tkinter import StringVar, ttk, messagebox
from view.config import config
from control.user_control import UserController


# Class pour géré les différents opérations de gestion des utilisateurs
class UserMgmt(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master

        self.frame = tk.Frame(self.master, bg=config.background)
        self.frame.pack()

        self.btn_collection = tk.Label(self.frame, bg=config.background)
        self.btn_collection.grid(row=0, column=0, pady=20)

        image_display =  ctk.CTkImage(Image.open("images/display.png"), size=(30, 30))      
        self.btn_aff = ctk.CTkButton(self.btn_collection, text="Afficher", image=image_display, compound="left",
                      font=("ARIAL", 20, "bold"), command=self.usertable)
        self.btn_aff.grid(row=0, column=0, padx=10, pady=5)

        image_add = ctk.CTkImage(Image.open("images/add.png"), size=(30, 30))                   
        self.btn_add = ctk.CTkButton(self.btn_collection, text="Ajouter", image=image_add, compound="left",
                      font=("ARIAL", 20, "bold"), command=self.useradd)
        self.btn_add.grid(row=1, column=0, padx=10, pady=5)
        
        image_edit = ctk.CTkImage(Image.open("images/edit.png"), size=(30, 30))           
        self.btn_mod = ctk.CTkButton(self.btn_collection, text="Modifier", image=image_edit, compound="left",
                      font=("ARIAL", 20, "bold"), command=self.usermod)
        self.btn_mod.grid(row=2, column=0, padx=10, pady=5)
        
        image_delete = ctk.CTkImage(Image.open("images/delete.png"), size=(30, 30))        
        self.btn_sup = ctk.CTkButton(self.btn_collection, text="Supprimer", image=image_delete, compound="left",
                      font=("ARIAL", 20, "bold"), command=self.usersup)
        self.btn_sup.grid(row=3, column=0, padx=10, pady=5)

        self.user_info = ctk.CTkLabel(self.frame, text="")
        self.user_info.grid(row=0, column=1, pady=20)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        config.displayed = UserDisplay(self.user_info)
    # Fonction pour géré l'ajout d'un utilisateur
    def useradd(self):
        user = {"username": config.displayed.userget["username"], "password": config.displayed.userget["password"]}
        usercontrol = UserController(user=user, roles=config.displayed.userget["roles"])
        messagebox.showinfo("", usercontrol.add())
        config.displayed.entry_init()
    # Fonction pour supprimer un utilisateur
    def usersup(self):
        if config.displayed.userget["id"]:
            if messagebox.askquestion("Attention", f"Tu es sur de supprimer l'utilisateur : {config.displayed.userget["username"]}") == "yes":
                usercontrol = UserController()
                messagebox.showinfo("", usercontrol.delete(config.displayed.userget["id"]))
                config.displayed.entry_init()
        else:
            messagebox.showinfo("", "Il n'y aucun utilisateur séléctionner.")

    # Fonction pour géré la modification d'un utilisateur
    def usermod(self):
        user = {"username": config.displayed.userget["username"], "password": config.displayed.userget["password"]}
        usercontrol = UserController(user=user, roles=config.displayed.userget["roles"])
        messagebox.showinfo("", usercontrol.edit(config.displayed.userget["id"]))
        config.displayed.entry_init()

    # Fonction pour afficher tous les utilisateurs et ces roles et en meme temps désactive la fonctionnalité des buttons d'opérations
    def usertable(self):
        config.displayed.fermer()
        self.btn_aff.configure(state="disabled")
        self.btn_add.configure(state="disabled")
        self.btn_mod.configure(state="disabled")
        self.btn_sup.configure(state="disabled")
        config.displayed = UsersTable(self.user_info)
        config.displayed.get_btn(self.btn_aff, self.btn_add, self.btn_mod, self.btn_sup)
    
    def fermer(self):
        self.frame.destroy()

# Class pour afficher les entrées de saisie des informations utilisateurs
class UserDisplay(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master
        self.frame = tk.Frame(self.master, bg=config.background)
        self.frame.grid(row=0, column=0)

        self.id = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.check_admin_role = tk.BooleanVar()
        self.check_vendeur_role = tk.BooleanVar()
        self.check_inventaire_role = tk.BooleanVar()

        
        ctk.CTkLabel(self.frame, text="Nom Utilisateur", font=("Helvetica", 20,"bold"), 
                     text_color="white").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        ctk.CTkEntry(self.frame, width=200, font=("Helvetica", 20,"bold"), textvariable=self.username).grid(row=0, column=1, padx=10, sticky="w")

        ctk.CTkLabel(self.frame, text="Mot de passe", font=("Helvetica", 20,"bold"), 
                     text_color="white").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        ctk.CTkEntry(self.frame, show="*", width=200, font=("Helvetica", 20,"bold"), textvariable=self.password).grid(row=1, column=1, padx=10, sticky="w")

        ctk.CTkLabel(self.frame, text="Role", font=("Helvetica", 20,"bold"), 
                     text_color="white").grid(row=2, column=0, pady=5, padx=10, sticky="w")
        ctk.CTkCheckBox(self.frame, text="Administrateur", text_color="white", font=("Helvetica", 15,"bold"), 
                        variable=self.check_admin_role).grid(row=2, column=1, pady=5, padx=10, sticky="w")
        ctk.CTkCheckBox(self.frame, text="Vendeur", text_color="white", font=("Helvetica", 15,"bold"),
                        variable=self.check_vendeur_role).grid(row=3, column=1, pady=5, padx=10, sticky="w")
        ctk.CTkCheckBox(self.frame, text="Inventaire", text_color="white", font=("Helvetica", 15,"bold"),
                        variable=self.check_inventaire_role).grid(row=4, column=1, pady=5, padx=10, sticky="w")
    
    # Fonction uriliser comme un propriété pour returner les informations saisie
    @property
    def userget(self):
        roles=[]

        if self.check_admin_role.get():
            roles.append("admin")
        if self.check_vendeur_role.get():
            roles.append("seller")
        if self.check_inventaire_role.get():
            roles.append("inventory")

        return {"id": self.id.get(),
                "username": self.username.get(), 
                "password": self.password.get(), 
                "roles": roles}
    
    # Fonction pour initialiser les entrées
    def entry_init(self):
        self.id.set("")
        self.username.set("")
        self.password.set("")
        self.check_admin_role.set(False)
        self.check_vendeur_role.set(False)
        self.check_inventaire_role.set(False)

    # Fonction pour géré la ferméture
    def fermer(self):
        self.frame.destroy()

# Class pour afficher les noms des utilisateurs et ces roles
class UsersTable(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master

        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)

        self.table = ttk.Treeview(self.frame, columns=("id", "username", "role"), show="headings")
        self.table.heading("id", text="ID")
        self.table.heading("username", text="Nom Utilisateur")
        self.table.heading("role", text="Roles")
        self.table.column("id", width=30)
        self.table.column("username", width=280)
        self.table.column("role", width=300)

        self.table["displaycolumns"]=("username", "role")  # pour cacher l'identification et affiche que le user et son role.
        
        usercontrol = UserController()
        for i, user in enumerate(usercontrol.getusers()):
            self.table.insert("", index=tk.END, values=(user["id"], user["username"], user["roles"]), tags=f"t{user['id']}")
            if i % 2:
                self.table.tag_configure(f"t{user['id']}", font=("ARIAL", 12), background="#b386fc")
            else:
                self.table.tag_configure(f"t{user['id']}", font=("ARIAL", 12), background="#8d85f2")
            self.table.column("username", anchor="center")
            self.table.column("role", anchor="center")

        style = ttk.Style(self.frame)
        style.theme_use("clam")
        style.configure("Treeview", fieldbackground="#b386fc")
        style.configure("Treeview.heading", background="#8d85f2")
        nametofont("TkHeadingFont").configure(size=10, family="ARIAL", weight="bold")

        self.table.grid(row=0, column=0)

        self.table.bind('<ButtonRelease-1>', self.selectItem)

    # Fonction pour prend l'utilisateur séléctionner dans le tableau et l'afficher par l'appel de class UserDisplay 
    def selectItem(self, event):
        selectedrow = self.table.focus()
        item = self.table.item(selectedrow)
        usercontrol = UserController()
        user = usercontrol.getuser(item["values"][0])
        self.btn_activate()
        config.displayed.fermer()
        config.displayed = UserDisplay(self.master)
        config.displayed.id.set(user["id"])
        config.displayed.username.set(user["username"])
        if "admin" in user["roles"]:
            config.displayed.check_admin_role.set(True)
        if "inventory" in user["roles"]:
            config.displayed.check_inventaire_role.set(True)
        if "seller" in user["roles"]:
            config.displayed.check_vendeur_role.set(True)
    
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

    # Fonction pour géré la ferméture
    def fermer(self):
        self.frame.destroy()
