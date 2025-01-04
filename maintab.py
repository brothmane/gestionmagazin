import tkinter as tk
import customtkinter as ctk
from PIL import Image
from tkinter import PhotoImage, messagebox
from view.login import Login
from view.config import config

from view.admindash.admin_main import Administrator
from view.inventaire_dash.inventaire_main import Inventory
from view.vente_dash.vente_main import Sales

# Fonction pour gérer le passage entre les défférent menu
def pass_menu(menu):
    global displayed_menu
    displayed_menu.fermer()
    displayed_menu = menu
    
# Fonction pour vérifier et autorise accès au diffirents menu
def check_role(role):
    if role in config.session_roles: 
        if role == "admin":        
            pass_menu(Administrator(sub_frame_top, frame_bottom))
        elif role == "inventory": 
            pass_menu(Inventory(sub_frame_top, frame_bottom)) 
        elif role == "seller": 
            pass_menu(Sales(sub_frame_top, frame_bottom))
        else:
            messagebox.showinfo("info", "Vous n'étes pas autorisé")
    else:
        messagebox.showinfo("info", "Vous n'étes pas autorisé")

root = tk.Tk()
root.title("Magazin Management")
root.attributes('-fullscreen', True)  # Pour utiliser l'affichage au plein écran

# Déviser l'écran au trois frame

frame_top = tk.Frame(root, bg=config.background)            # Top frame
frame_top.pack(fill=tk.BOTH, expand=False, side=tk.TOP, ipady=10)

sub_frame_top = tk.Frame(root, bg=config.background)        # Sub top frame
sub_frame_top.pack(fill=tk.BOTH, expand=False, ipady=10)

frame_bottom = tk.Frame(root, bg=config.background)         # Bottom frame
frame_bottom.pack(side="bottom", fill=tk.BOTH, expand=True, ipady=150)


btn_function = tk.Frame(frame_top, bg=config.background, padx=20, pady=25)       # Pour rassembler tous les button

photo_admin = PhotoImage(file="images/administrator.png")
image_admin = photo_admin.subsample(8, 8)
tk.Button(btn_function, image=image_admin, bd=0, activebackground=config.background,
                    bg=config.background, command=lambda : check_role("admin")).grid(row=0, column=0)
tk.Label(btn_function, text="ADMINISTRATOR", bg=config.background, fg="white", font="ARIAL 10 bold", padx=20).grid(row=1, column=0)

photo_inventory = PhotoImage(file="images/inventory.png")
image_inventory = photo_inventory.subsample(8, 8)
tk.Button(btn_function, image=image_inventory, bd=0, activebackground=config.background,
                    bg=config.background, command=lambda : check_role("inventory")).grid(row=0, column=1)
tk.Label(btn_function, text="INVENTAIRE", bg=config.background, fg="white", font="ARIAL 10 bold", padx=20).grid(row=1, column=1)

photo_selling = PhotoImage(file="images/selling.png")
image_selling = photo_selling.subsample(8, 8)
tk.Button(btn_function, image=image_selling, bd=0, activebackground=config.background,
                    bg=config.background, command=lambda : check_role("seller")).grid(row=0, column=2)
tk.Label(btn_function, text="VENTES", bg=config.background, fg="white", font="ARIAL 10 bold", padx=20).grid(row=1, column=2)


photo_exit = PhotoImage(file="images/quit.png")
image_exit = photo_exit.subsample(8, 8)
btn_quit = tk.Button(frame_top, image=image_exit, bd=0, activebackground=config.background,
          bg=config.background, height=80, width=80, command=root.destroy)

image_user_session = ctk.CTkImage(Image.open("images/utilisateur.png"), size=(30, 30))  
user_session = ctk.CTkLabel(frame_top, image=image_user_session, text_color="white",
                            font=("ARIAL", 16, "bold"), compound="top")

displayed_menu = Login(root, frame_bottom, btn_function, btn_quit, user_session)

# Exécuter l'application
root.mainloop()