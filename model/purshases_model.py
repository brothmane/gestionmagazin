from database.connect import DB_Query
from view.config import config

# Class pour géré tous les opérations concernant l'utilisateur dans la base de données
class PurshaseModel:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.product_id = None
        self.date = None
        self.qty = None
    
    def set(self, user_id, product_id, date, qty):
        self.user_id = user_id
        self.product_id = product_id
        self.date = date
        self.qty = qty
    
    # Fonction pour obtenir un achat ou récéption suivant l'id de utilisateur
    def getbyuserid(self, user_id):
        if user_id:
            purshases = DB_Query(config.database, f"SELECT * FROM purchases WHERE user_id = {user_id}").result
            if purshases:
                self.id = purshases[0][0]
                self.user_id = purshases[0][1]
                self.product_id = purshases[0][2]
                self.date = purshases[0][3] 
                self.qty = purshases[0][4]               
                return purshases
            else:
                return None
            
    # Fonction pour sauvgarder les achats 
    def save(self):
        try:
            if self.user_id and self.product_id and self.date and self.qty:
                user = DB_Query(config.database, f"INSERT INTO purchases (user_id, product_id, date, quantity) \
                                                    VALUES ('{self.user_id}', '{self.product_id}', '{self.date}', {self.qty});")
                self.id = user.lastrowid
                return self.id
            else:
                return "Manque de données"
        except:
            return f"Erreur pendant le traitement"
    
   