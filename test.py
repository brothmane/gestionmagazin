import tkinter as tk
from view.config import config
from database.connect import DB_Query
from model.user_model import UserModel
from model.role_model import RoleModel
from model.user_role_model import UserRoleModel
from model.product_model import ProductModel

from model.purshases_model import PurshaseModel
from control.product_control import ProductController
from control.purshase_control import PurshaseController
from control.report_control import ReportController
from model.sales_model import SalesModel, SalesDetailModel

# role = UserRoleModel()
# print(role.getall())
# role.get(role_name="admin")
# print(str(role.id)+"---"+role.name)
# user  = UserModel()
# print(user.getall())
# user.get(username="b")
# role = UserRoleModel(user)
# print(role.get())

# user.get(5)
# print(str(user.id)+"---"+user.name)
# user_roles = UserRoleModel(user, role)
# # userget.set("Nesrin", "test123")
#user_roles.save()

# print(user.name)
# print(user_roles.get())

# DB_Query(config.database, """
#         CREATE TABLE IF NOT EXISTS user_role (
#             user_id INTEGER,
#             role_id INTEGER,
#             FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
#             FOREIGN KEY (role_id) REFERENCES role(id) ON DELETE RESTRICT,
#             UNIQUE (user_id, role_id)
#         );
#         """)
# # 
# DB_Query(config.database, "ALTER TABLE products ADD minqty INTEGER DEFAULT 0;")
# DB_Query(config.database, "ALTER TABLE products ADD normalqty INTEGER DEFAULT 0;")
# print(DB_Query(config.database, f"SELECT * FROM products WHERE name LIKE '%h%'").result)
# print(DB_Query(config.database, "PRAGMA foreign_keys;").result)

# product = ProductController()
# # result = product.getbyname(name="g")
# print(product.getproduct(2))
# data = DB_Query(config.database, f"SELECT u.username, p.name, sales_details.quantity, p.price, sales_details.price FROM sales_details \
#                                                         INNER JOIN products as p on sales_details.product_id = p.id \
#                                                         INNER JOIN sales as s on sales_details.sale_id = s.id \
#                                                         INNER JOIN users as u on s.user_id = u.id \
#                                                         WHERE sale_id IN (SELECT id FROM sales WHERE date LIKE '%2025-01%')")
# print(data.result)

# products = ProductController()
# print(products.getproductbyname("diodorant 2"))

# purshase = PurshaseController()
# purshase.set(2, 3, '12/12/2024', 40)
# print(purshase.save())
# print(purshase.add())

# sales = SalesDetailModel()
# print(sales.getbydate("2025"))

report = ReportController()
print(report.getdetailreport("2025"))