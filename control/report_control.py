from model.sales_model import SalesModel, SalesDetailModel
from view.config import config

# Class pour adapter les informations de rapport au calss view
class ReportController:
    def __init__(self):
        self.salesmodel = SalesModel()
        self.salesdetailmodel = SalesDetailModel()

    # Fonction pour obtenir un rapport général des ventes
    def getreport(self, date):
        pre_sales = self.salesmodel.getbydate(date)
        sales = []
        total = 0.0
        if pre_sales:
            for sale in pre_sales:
                sales.append({"id": sale[0],
                            "user": sale[1],
                            "total_amount": sale[3]
                            })
                total += sale[3]
                
        return {"sales": sales, "total": total}

    # Fonction pour obtenir un rapport détaillé des ventes
    def getdetailreport(self, date):
        pre_salesdetails = self.salesdetailmodel.getbydate(date)
        salesdetails = []
        total_purshase = 0.0
        total_sales = 0.0

        if pre_salesdetails:
            for saledetail in pre_salesdetails:
                salesdetails.append({"sale_id": saledetail[0],
                                    "user": saledetail[1],
                                    "product_name": saledetail[2],
                                    "quantity": saledetail[3],
                                    "purshase_price": saledetail[4],
                                    "sale_price": saledetail[5]
                                    })
                total_purshase += saledetail[3] * saledetail[4]
                total_sales += saledetail[3] * saledetail[5]

        return {"salesdetails": salesdetails, 
                "total_purshase": total_purshase, 
                "total_sales": total_sales, 
                "net_income": total_sales-total_purshase}