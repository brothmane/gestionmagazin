from model.sales_model import SalesDetailModel, SalesModel 
from model.product_model import ProductModel
from datetime import datetime

# Class pour adapter les informations de ventes au calss view
class SalesController:
    def __init__(self):
        self.salesmodel = SalesModel()
        self.salesdetailmodel = SalesDetailModel()
        self.productmodel = ProductModel()
        self.sale = None
        self.salesdetails = []

    # Fonction pour fixé les informations de l'id utilisateur et le prix total de vente
    def set_sale(self, sale={"user_id":int, "total_amount": float} ):
        self.sale = sale

    # Fonction pour fixé les informations détaillé de vente
    def set_saledetails(self, salesdetails={"product_id":int, "qty":int, "price":float}):
        self.salesdetails.append(salesdetails)
    
    # Fonction pour valider le panier 
    def validpanier(self):
        if self.sale:
            self.salesmodel.set(self.sale["user_id"], datetime.now(), self.sale["total_amount"])
            self.sale_id = self.salesmodel.save()
            if self.salesdetails:
                for saledetail in self.salesdetails:
                    self.salesdetailmodel.set(self.sale_id, saledetail["product_id"], saledetail["qty"], saledetail["price"])
                    self.productmodel.get(saledetail["product_id"])
                    if int(saledetail["qty"]) <= int(self.productmodel.qty):
                        self.productmodel.editqty(saledetail["product_id"], -int(saledetail["qty"]))
                        self.salesdetailmodel.save()
                    else:
                        self.salesmodel.delete(self.sale_id)
                        return f"Quntité de {self.productmodel.name} est insufisante pour términe le vente."
                return "Vente enregistrer."
            else:
                self.salesmodel.delete(self.sale_id)
                return "C'est une vente sans produits."
        else:
            return "Il n'y a pas de vente appliqué."