from model.product_model import ProductModel 
import string
from view.config import config

ALPHA = string.ascii_letters        # Variable utiliser pour matching que les lettres alphabétiques

# Class pour adapter les informations de produit au calss view
class ProductController:
    def __init__(self, product={"name":str, "unit":str, "prix": float, "qty": int, "minqty": int, "normalqty": int}):
        self.productmodel = ProductModel()
        self.product = product       
    
    # Fonction pour géré et controller l'addition des produits
    def add(self):
        try:
            float(self.product["prix"])
            str(self.product["unit"])

            if self.product["minqty"]:
                int(self.product["minqty"])
            else: 
                self.product["minqty"] = 0

            if self.product["normalqty"]:
                int(self.product["normalqty"])
            else:
                self.product["normalqty"] = 0

            if self.product["name"].startswith(tuple(ALPHA)):
                self.productmodel.set(self.product["name"], self.product["unit"], self.product["prix"], 
                                      self.product["minqty"], self.product["normalqty"])
                productsave = self.productmodel.save()
                if type(productsave) == int:
                    return "Produit enregistrer."
                else:
                    return productsave
            else:
                return "Vérifier les valeurs saisi."
        except:
            return "Vérifier le format des valeurs saisi."
    
    # Fonction pour géré et controller la recherche des produits
    def recherche(self, name=None):
        if name:
            pre_products = self.productmodel.getbyname(name)
            products = []
            if pre_products:
                for product in pre_products:
                    products.append({"id": product[0],
                                    "name": product[1],
                                    "unit": product[2],
                                    "price": product[3],
                                    "qty": product[4],
                                    "minqty": product[5],
                                    "normalqty": product[6]})
                return products
            else:
                return None
        else:
            return None

    # Fonction pour géré et controller la modification des produits
    def edit(self, id):
        try:
            float(self.product["prix"])
            str(self.product["unit"])
            if self.product["minqty"]:
                int(self.product["minqty"])
            else: 
                self.product["minqty"] = 0
            if self.product["normalqty"]:
                int(self.product["normalqty"])
            else:
                self.product["normalqty"] = 0
            if self.product["name"].startswith(tuple(ALPHA)):
                self.productmodel.set(self.product["name"], self.product["unit"],
                                      self.product["prix"], self.product["minqty"],
                                      self.product["normalqty"])
                productedit = self.productmodel.edit(id)
                if type(productedit) == int:
                    return "Produit modifier."
                else:
                    return productedit
            else:
                return "Vérifier les valeurs saisi."
                
        except:
            return "Vérifier le format des valeurs saisi."
        
    # Fonction pour géré et controller la suppression des produits
    def delete(self, id):
        try:
            productdelete = self.productmodel.delete(id)
            return productdelete
        except:
            return "Erreur durent le traitement des roles."
    
    # Fonction pour géré et controller l'obtention des produits par leur id
    def getproductbyid(self, id):
        if self.productmodel.get(id):
            product = {"id": self.productmodel.id,
                        "name": self.productmodel.name,
                        "unit": self.productmodel.unit,
                        "price": self.productmodel.price,
                        "qty": self.productmodel.qty,
                        "minqty": self.productmodel.minqty,
                        "normalqty": self.productmodel.normalqty}
            return product
        else:
            return None
    
    # Fonction pour géré et controller l'obtention des produits par leur name
    # L'argument for_sale est ajouter pour controller le prix returner
    def getproductbyname(self, name, for_sale=False):
        pre_products = self.productmodel.getbyname(name)
        products = []
        if pre_products:
            for product in pre_products:
                
                if for_sale:            # Si for_sale est True ça vue dire returner le prix de vente sinon il returne le prix d'achat
                    price = float(product[3]) + (float(product[3])*config.prixpercentage)
                else:
                    price = float(product[3])

                products.append({"id": product[0],
                                "name": product[1],
                                "unit": product[2],
                                "price": price,
                                "qty": product[4],
                                "minqty": product[5],
                                "normalqty": product[6]})
        return products
    
    # Fonction pour géré et controller l'obtention de tous les produits
    def getall(self):
        pre_products = self.productmodel.getall()
        products = []
        for product in pre_products:
            products.append({"id": product[0],
                        "name": product[1],
                        "unit": product[2],
                        "price": product[3],
                        "qty": product[4],
                        "minqty": product[5],
                        "normalqty": product[6]})
        return products