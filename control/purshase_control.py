from model.purshases_model import PurshaseModel 
from model.product_model import ProductModel
from datetime import datetime

# Class pour adapter les informations des achat ou des nouveau récéption au calss view
class PurshaseController:
    def __init__(self, purshasemodel=PurshaseModel(), purshase={"user_id":int, "product_id":int, "date": datetime, "qty": int}):
        self.purshasemodel = purshasemodel
        self.purshase = purshase  
        self.productmodel = ProductModel()     
    
    # Fonction pour géré l'addition des nouveaux récéptions ou des nouveau achat
    def add(self):
        try:
            self.purshase["date"] = datetime.now()
            int(self.purshase["user_id"])
            int(self.purshase["product_id"])
            int(self.purshase["qty"])
            
            self.purshasemodel.set(self.purshase["user_id"], self.purshase["product_id"], self.purshase["date"],self.purshase["qty"])
            purshasesave = self.purshasemodel.save()
            checkproduct = self.productmodel.editqty(self.purshase["product_id"], self.purshase["qty"])
            if checkproduct:
                if type(purshasesave) == int:
                    return "Récéption enregistrer."
                else:
                    return purshasesave
            else:
                return "Problème de mise jour de produit."
        except:
            return "Vérifier le format des valeurs saisi."
    
    