from database.connect import DB_Query
from view.config import config
from tkinter import messagebox

# Class pour géré tous les opérations concernant le produit dans la base de données 
class ProductModel:
    def __init__(self):
        self.id = None
        self.name = None
        self.unit = None
        self.price = None
        self.qty = None
        self.minqty = None
        self.normalqty = None
    
    def set(self, name, unit, price, minqty, normalqty):
        self.name = name.lower()
        self.unit = unit
        self.price = price
        self.minqty = minqty
        self.normalqty = normalqty
    
    # Fonction pour obtenir un produit par id à partir de la base de donnée
    def get(self, id=None):
        if id:
            product = DB_Query(config.database, f"SELECT * FROM products WHERE ID = {id}").result
            if product:
                self.id = product[0][0]
                self.name = product[0][1]
                self.unit = product[0][2]
                self.price = product[0][3]
                self.qty = product[0][4]
                self.minqty = product[0][5]
                self.normalqty = product[0][6]
                return 1
            else:
                return None
        else:
            return None
    
    # Fonction pour obtenir un ou plusieurs produit par name à partir de la base de donnée
    def getbyname(self, name=None):
        if name:
            products = DB_Query(config.database, f"SELECT * FROM products WHERE name LIKE '%{str(name).lower()}%'").result
            if products:
                return products
            else:
                return None
        else:
            return None
        
    # Fonction pour sauvgarder un produit dans la base de donnée
    def save(self):
        try:
            if self.name and self.unit and self.price:
                user = DB_Query(config.database, f"INSERT INTO products (name, unit, price, minqty, normalqty) VALUES ('{self.name}', '{self.unit}', {self.price}, {self.minqty}, {self.normalqty});")
                self.id = user.lastrowid
                return self.id
            else:
                return "nom ou prix ou unit n'a pas été saisi."
        except:
            return "Erreur pendant le traitement"
    
    # Fonction pour editer les informations de produit dans la base de donnée
    def edit(self, id):
        try:
            if self.name and self.unit and self.price:
                DB_Query(config.database, 
                         f"UPDATE products SET name='{self.name}', unit='{self.unit}', price='{self.price}', minqty={self.minqty}, normalqty={self.normalqty} WHERE id = {id};")
                return 1
            else:
                return "Le nom ou l'unité ou le prix n'a pas été saisi"
        except:
            return "Erreur pendant le traitement"
    
    # Fonction pour editer les informations de quantité de produit dans la base de donnée
    def editqty(self, id, qty):
        try:
            self.get(id)
            self.qty = self.qty + qty
            DB_Query(config.database,
                    f"UPDATE products SET quantity={self.qty} WHERE id = {id};")
            return True
        except:
            return False

    # Fonction pour supprimer un produit
    def delete(self, id):
        try:
            DB_Query(config.database, f"DELETE FROM products WHERE id = {id};")
            return "Product supprimé"
        except:
            return "Erreur pendant le traitement"

    # Fonction pour obtenir tous les produits     
    def getall(self):
        products = DB_Query(config.database, f"SELECT * FROM products").result
        if products:
            return products
        else:
            return None