import tkinter as tk
from tkinter import StringVar, messagebox
import customtkinter as ctk
from view.config import config
from model.user_model import UserModel
from control.user_control import UserController

# Class pour gestion de login
class Login(tk.Frame):
    def __init__(self, root, master, btn_function, btn_quit, user_session):
        tk.Frame.__init__(self)
        self.root = root
        self.master = master
        self.btn_function = btn_function
        self.btn_quit = btn_quit
        self.user_session = user_session

        self.frame = tk.Frame(self.master, bg=config.background)
        self.frame.grid(row=0, column=0)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.username_entry = StringVar()
        self.password_entry = StringVar()

        ctk.CTkLabel(self.frame, text="Utilisateur", font=("ARIAL", 20, "bold"), text_color="white").grid(row=0, column=0, sticky="w")
        user_entry = ctk.CTkEntry(self.frame, textvariable=self.username_entry, font=("ARIAL", 20, "bold"), 
                     width=200)
        user_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        user_entry.bind('<Return>', self.submit_enter)

        ctk.CTkLabel(self.frame, text="Mot de passe", font=("ARIAL", 20, "bold"), text_color="white").grid(row=1, column=0, sticky="w")
        pass_entry = ctk.CTkEntry(self.frame, show="*", textvariable=self.password_entry, font=("ARIAL", 20, "bold"),
                 width=200)
        pass_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        pass_entry.bind('<Return>', self.submit_enter)

        ctk.CTkButton(self.frame, text="Entrer", font=("ARIAL", 20, "bold"), command=self.submit).grid(row=3, column=1, pady=5)
        ctk.CTkButton(self.frame, text="Quiter", font=("ARIAL", 20, "bold"), command=self.root.destroy).grid(row=4, column=1, pady=5)

    def submit_enter(self, event):
        self.submit()

    # Fonction pour géré le login après la vérification username et mot de passe
    def submit(self):
        user = {"username": self.username_entry.get(), "password": self.password_entry.get()}
        userget = UserModel()
        logincheck =  UserController(userget, user)
        login = logincheck.login()

        if type(login) == str:
            messagebox.showwarning("Warning", logincheck.login())
        else:
            if login["check"] :
                self.btn_function.pack(side=tk.LEFT, ipady=20) 
                self.btn_quit.pack(side=tk.RIGHT, ipadx=20)
                config.session_user = userget
                self.user_session.configure(text=self.username_entry.get().capitalize())
                self.user_session.pack(side=tk.RIGHT, ipadx=20)  
                config.session_roles = login["roles"]
                self.frame.destroy()
            else:
                messagebox.showwarning("Warning", logincheck.login())
            
    def fermer(self):
        self.frame.destroy()