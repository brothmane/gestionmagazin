import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter.font import nametofont
from tkcalendar import DateEntry
import datetime
from view.config import config
from control.report_control import ReportController

# Class pour géré l'afficher des rapport journalier et mensuel 
class SalesReport(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.master = master
        
        self.frame = tk.Frame(self.master, bg=config.background)
        self.frame.pack()

        self.radioVar = ctk.StringVar(value="journalier")
        radio_btn = ctk.CTkLabel(self.frame)
        radio_btn.grid(row=0, column=0, pady=10)
        ctk.CTkRadioButton(radio_btn, text="Mensuel", value="mensuel", variable=self.radioVar).grid(row=0, column=0, pady=5)
        ctk.CTkRadioButton(radio_btn, text="Journalier", value="journalier", variable=self.radioVar).grid(row=0, column=1, pady=5)

        label_btn = ctk.CTkLabel(self.frame)
        label_btn.grid(row=1, column=0, pady=10)
        ctk.CTkButton(label_btn, text="Général", font=("ARIAL", 20, "bold"), command=self.generaltable).grid(row=0, column=0, padx=5)
        
        self.date_entry = DateEntry(label_btn, state='readonly', font=("ARIAL", 15, "bold"))
        self.date_entry.grid(row=0, column=1)
        
        ctk.CTkButton(label_btn, text="Détaillé", font=("ARIAL", 20, "bold"), command=self.detailtable).grid(row=0, column=2, padx=5)

        self.label_table = tk.Label(self.frame, bg=config.background)
        self.label_table.grid(row=2, column=0, pady=10)

        self.report = ReportController()
        self.general_report = self.report.getreport(self.date_entry.get_date())
        self.detail_report = self.report.getdetailreport(self.date_entry.get_date())
        config.displayed = GeneralTable(self.label_table, self.general_report)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
    
    # Fonction pour afficher le rapport général
    def generaltable(self):
        if self.radioVar.get() == "journalier":         # Vérification de selection de rapport journalier ou mensuel
            self.general_report = self.report.getreport(str(self.date_entry.get_date()))
        else:
            self.general_report = self.report.getreport(str(datetime.datetime.strptime(str(self.date_entry.get_date()), 
                                                                                       "%Y-%m-%d").strftime("%Y-%m")))
        config.displayed.fermer()
        config.displayed = GeneralTable(self.label_table, self.general_report)
    
    # Fonction pour afficher le rapport détaillée
    def detailtable(self):
        if self.radioVar.get() == "journalier":         # Vérification de selection de rapport journalier ou mensuel
            self.detail_report = self.report.getdetailreport(str(self.date_entry.get_date()))
        else:
            self.detail_report = self.report.getdetailreport(str(datetime.datetime.strptime(str(self.date_entry.get_date()), 
                                                                                            "%Y-%m-%d").strftime("%Y-%m")))
        config.displayed.fermer()
        config.displayed = DetailTable(self.label_table, self.detail_report)

    # Fonction pour géré la fermeture
    def fermer(self):
        self.frame.destroy()

# Class pour afficher le tableau de rapport général
class GeneralTable(tk.Frame):
    def __init__(self, master, general_report):
        tk.Frame.__init__(self)
        self.frame = master
        self.master = tk.Frame(self.frame, bg=config.background)
        self.master.grid(row=0, column=0)
        self.general_report = general_report

        label_table = ctk.CTkLabel(self.master)
        label_table.grid(row=2, column=0, pady=10)

        self.table = ttk.Treeview(label_table, columns=("id", "username", "amount"), show="headings")
        self.table.heading("id", text="ID")
        self.table.heading("username", text="Vendeur")
        self.table.heading("amount", text="Montant")
        self.table.column("id", width=30)
        self.table.column("username", width=280)
        self.table.column("amount", width=300)

        self.table["displaycolumns"]=("username", "amount")  # pour cacher l'identification et affiche que le user et les montantes de ventes.
        
        for i, sale in enumerate(self.general_report["sales"]):
            self.table.insert("", index=tk.END, values=(sale["id"], sale["user"], sale["total_amount"]), tags=f"t{sale['id']}")
            if i % 2:
                self.table.tag_configure(f"t{sale['id']}", font=("ARIAL", 12), background="#b386fc")
            else:
                self.table.tag_configure(f"t{sale['id']}", font=("ARIAL", 12), background="#8d85f2")
            self.table.column("username", anchor="center")
            self.table.column("amount", anchor="center")

        style = ttk.Style(self.master)
        style.theme_use("clam")
        style.configure("Treeview", fieldbackground="#b386fc")
        style.configure("Treeview.heading", background="#8d85f2")
        nametofont("TkHeadingFont").configure(size=10, family="ARIAL", weight="bold")

        self.table.grid(row=0, column=0)

        label_total = tk.Label(self.master, bg=config.background)
        label_total.grid(row=3, column=0, pady=10, sticky="e")
        ctk.CTkLabel(label_total, text=f"Total : {self.general_report["total"]} DZD", text_color="white", font=("ARIAL", 15,"bold")).grid(row=0, column=1, padx=5)
        
    # Fonction pour géré la fermeture
    def fermer(self):
        self.master.destroy()

# Class pour afficher le tableau de rapport détaillé
class DetailTable(tk.Frame):
    def __init__(self, master, detail_report):
        tk.Frame.__init__(self)
        self.frame = master
        self.master = tk.Frame(self.frame, bg=config.background)
        self.master.grid(row=0, column=0)
        self.detail_report = detail_report

        label_table = ctk.CTkLabel(self.master)
        label_table.grid(row=2, column=0, pady=10)

        self.table = ttk.Treeview(label_table, columns=("user", "product_name", "quantity", "purshase_price", "sale_price", "total"), show="headings")
        self.table.heading("user", text="Vendeur")
        self.table.heading("product_name", text="Produit")
        self.table.heading("quantity", text="Quantité")
        self.table.heading("purshase_price", text="Prix Achat")
        self.table.heading("sale_price", text="Prix Vente")
        self.table.heading("total", text="Total")
        self.table.column("user", width=120)
        self.table.column("product_name", width=280)
        self.table.column("quantity", width=80)
        self.table.column("purshase_price", width=100)
        self.table.column("sale_price", width=100)
        self.table.column("total", width=100)

        check_sale_id = 0
        for i, detailsale in enumerate(self.detail_report["salesdetails"]):
            self.table.insert("", index=tk.END, values=(detailsale["user"], 
                                                        detailsale["product_name"], 
                                                        detailsale["quantity"], 
                                                        detailsale["purshase_price"],
                                                        detailsale["sale_price"], 
                                                        detailsale["quantity"] * detailsale["sale_price"]), 
                                                        tags=f"t{i}")
            
            if not check_sale_id:
                check_sale_id = detailsale["sale_id"]
                color = "#8d85f6"

            if check_sale_id == detailsale["sale_id"]:
                self.table.tag_configure(f"t{i}", font=("ARIAL", 12), background=color)
            else:
                check_sale_id = detailsale["sale_id"]

                if color == "#8d85f6":
                    color = "#b386fc"
                else:
                    color = "#8d85f6"

                self.table.tag_configure(f"t{i}", font=("ARIAL", 12), background=color)

            self.table.column("user", anchor="center")
            self.table.column("product_name", anchor="center")
            self.table.column("quantity", anchor="center")
            self.table.column("purshase_price", anchor="center")
            self.table.column("sale_price", anchor="center")
            self.table.column("total", anchor="center")

        style = ttk.Style(self.master)
        style.theme_use("clam")
        style.configure("Treeview", fieldbackground="#b386fc")
        style.configure("Treeview.heading", background="#8d85f2")
        nametofont("TkHeadingFont").configure(size=10, family="ARIAL", weight="bold")

        self.table.grid(row=0, column=0)

        label_total = tk.Label(self.master, bg=config.background)
        label_total.grid(row=3, column=0, pady=10, sticky="e")
        ctk.CTkLabel(label_total, text=f"Total Achat : {self.detail_report["total_purshase"]} DZD", text_color="white", 
                     font=("ARIAL", 15,"bold")).grid(row=0, column=1, padx=5, sticky="w")

        ctk.CTkLabel(label_total, text=f"Total Vente : {self.detail_report["total_sales"]} DZD", text_color="white", 
                     font=("ARIAL", 15,"bold")).grid(row=1, column=1, padx=5, sticky="w")

        ctk.CTkLabel(label_total, text=f"Revenu net : {self.detail_report["net_income"]} DZD", text_color="white", 
                     font=("ARIAL", 15,"bold")).grid(row=2, column=1, padx=5, sticky="w")
        
    # Fonction pour géré la fermeture
    def fermer(self):
        self.master.destroy()
        