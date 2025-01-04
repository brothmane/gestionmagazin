import tkinter as tk
from tkinter import StringVar, ttk
from tkinter.font import nametofont
from view.config import config
from control.product_control import ProductController

# Class pour afficher les produits et son état dans le stock
class ProductReport(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master
        self.username = StringVar()

        self.frame = tk.Frame(self.master, bg=config.background)
        self.frame.pack(fill=tk.BOTH, expand=False)

        self.table = ttk.Treeview(self.frame, columns=("name", "price", "qty"), show="headings")
        self.table.heading("name", text="Nom")
        self.table.heading("price", text="Prix")
        self.table.heading("qty", text="Quantité")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('ARIAL', 16))

        self.table.column("name", width=350)
        self.table.column("price", width=150)
        self.table.column("qty", width=100)
              
        productcontrol = ProductController()
        for i, product in enumerate(productcontrol.getall()):
            self.table.insert("", index=tk.END, values=(product["name"], product["price"], product["qty"]), tags=f"t{product['id']}")
            if i % 2:
                if int(product["minqty"]) != 0 and int(product["normalqty"]) != 0:
                    if int(product["qty"]) < int(product["minqty"]):
                        self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="red")
                    elif int(product["qty"]) < int(product["normalqty"]):
                        self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="orange")
                    else: 
                        self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="green")
                else:
                    self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="#b386fc")
            else:
                if int(product["minqty"]) != 0 and int(product["normalqty"]) != 0:
                    if int(product["qty"]) < int(product["minqty"]):
                        self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="red")
                    elif int(product["qty"]) < int(product["normalqty"]):
                        self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="orange")
                    else: 
                        self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="green")
                else:
                    self.table.tag_configure(f"t{product['id']}", font=("ARIAL", 12), background="#8d85f2")

            self.table.column("name", anchor="center")
            self.table.column("price", anchor="center")
            self.table.column("qty", anchor="center")
    

        style = ttk.Style(self.frame)
        style.theme_use("clam")
        style.configure("Treeview", fieldbackground="#b386fc")
        style.configure("Treeview.heading", background="#8d85f2")
        nametofont("TkHeadingFont").configure(size=10, family="ARIAL", weight="bold")

        self.table.grid(row=0, column=0, pady=20)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def fermer(self):
        self.frame.destroy()