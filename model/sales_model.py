from database.connect import DB_Query
from view.config import config

# Class pour géré tous les opérations concernant les ventes dans la base de données 
class SalesModel:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.date = None
        self.total_amount = None
    
    def set(self, user_id, date, total_amount):
        self.user_id = user_id
        self.date = date
        self.total_amount = total_amount
    
    # Fonction pour obtenir tous les ventes faire l'utilisateur ayant l'id user_id
    def getbyuserid(self, user_id=None):
        if user_id:
            sales = DB_Query(config.database, f"SELECT * FROM sales WHERE user_id = {user_id}").result
            if sales:
                return sales
            else:
                return None
        else:
            return None
    
    # Fonction pour sauvgarder un vente
    def save(self):
        try:
            user = DB_Query(config.database, f"INSERT INTO sales (user_id, date, total_amount) \
                            VALUES ('{self.user_id}', '{self.date}', '{self.total_amount}');")
            self.id = user.lastrowid
            return self.id
        except:
            return "Erreur pendant le traitement"
    
    # Fonction pour obtenir les ventes à la base de son date    
    def getbydate(self, date=None):
        if date:
            sales = DB_Query(config.database, f"SELECT sales.id, u.username, sales.date, sales.total_amount FROM sales \
                                                INNER JOIN users as u on sales.user_id = u.id \
                                                WHERE date LIKE '%{date}%'").result
            if sales:
                return sales
            else:
                return None
        else:
            return None
    
    def delete(self, id):
        try:
            DB_Query(config.database, f"DELETE FROM sales WHERE id = {id};")
            return "Vente supprimé"
        except:
            return "Erreur pendant le traitement"

# Class pour géré tous les opérations concernant les détailles de chaque vente dans la base de données
class SalesDetailModel:
    def __init__(self):
        self.id = None
        self.sale_id = None
        self.product_id = None
        self.qty = None
        self.price = None
    
    def set(self, sale_id, product_id, qty, price):
        self.sale_id = sale_id
        self.product_id = product_id
        self.qty = qty
        self.price = price
    
    # Fonction pour sauvgarder les détailles de vente
    def save(self):
        try:
            sale_detail = DB_Query(config.database, f"INSERT INTO sales_details (sale_id, product_id, quantity, price) \
                            VALUES ('{self.sale_id}', '{self.product_id}', '{self.qty}', '{self.price}');")
            self.id = sale_detail.lastrowid
            return self.id
        except:
            return "Erreur pendant le traitement"
    
    # Fonction pour obtenir le vente qui matche l'id déclarer
    def getbysaleid(self, sale_id):
        if sale_id:
            salesdetail = DB_Query(config.database, f"SELECT * FROM sales_details WHERE sale_id = {sale_id}").result
            if salesdetail:
                return salesdetail
            else:
                return None
        else:
            return None
    
    # Fonction pour obtenir les detailles de chaque vente à base de date de vente
    def getbydate(self, date=None):
        if date:
            sales_detail = DB_Query(config.database, f"SELECT sale_id, users.username, products.name, sales_details.quantity, products.price, sales_details.price FROM sales_details \
                                                        INNER JOIN products on sales_details.product_id = products.id \
                                                        INNER JOIN sales on sales_details.sale_id = sales.id \
                                                        INNER JOIN users on sales.user_id = users.id \
                                                        WHERE sale_id IN (SELECT id FROM sales WHERE date LIKE '%{date}%')").result
            if sales_detail:
                return sales_detail
            else:
                return None
        else:
            return None