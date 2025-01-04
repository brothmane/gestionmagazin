import sqlite3

# Class pour facilite et sécurise la connexion au base de donnée
class DB_Query:
    def __init__(self, db_name, query):
        connction = sqlite3.connect(db_name)
        cursur = connction.cursor()
        cursur.execute("PRAGMA foreign_keys = ON;")  # Empêcher la suppression indésirable d'objets ayant une relation dans les déffirent tables 
        cursur.execute(query)
        connction.commit()
        self.result = cursur.fetchall()
        self.lastrowid = cursur.lastrowid
        connction.close()