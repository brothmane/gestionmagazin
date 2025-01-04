from database.connect import DB_Query
from view.config import config

# Class pour géré tous les opérations concernant l'utilisateur dans la base de données 
class UserModel:
    def __init__(self):
        self.id = None
        self.name = None
        self.password = None
    
    def set(self, name, password):
        self.name = str(name).lower()
        self.password = password
    
    # Fonction pour obtenir un utilisateurs à partir de la base de donnée
    def get(self, id=None, username=None):
        if id:          # Obtenir un utilisateur suivant leur id
            user = DB_Query(config.database, f"SELECT * FROM users WHERE ID = {id}").result
            if user:
                self.id = user[0][0]
                self.name = user[0][1]
                self.password = user[0][2]
                return 1
            else:
                return None
        elif username:          # Obtenir un utilisateur suivant leur username
            user = DB_Query(config.database, f"SELECT * FROM users WHERE username = '{str(username).lower()}'").result
            if user:
                self.id = user[0][0]
                self.name = user[0][1]
                self.password = user[0][2]
                return 1
            else:
                return None
        else:
            return None
    
    # Fonction pour sauvgarder l'utilisateur dans la base de donnée
    def save(self):
        try:
            if self.name and self.password:
                user = DB_Query(config.database, f"INSERT INTO users (username, password) VALUES ('{self.name}', '{self.password}');")
                self.id = user.lastrowid
                return self.id
            else:
                return "Le nom ou le mot de passe n'a pas été saisi"
        except:
            return "Erreur pendant le traitement"
    
    # Fonction pour editer les informations de l'utilisateur dans la base de donnée
    def edit(self, id):
        try:
            if self.name and self.password:
                DB_Query(config.database, f"UPDATE users SET username = '{self.name}', password = '{self.password}' WHERE id = {id};")
                self.id = id
                return 1
            else:
                return "Le nom ou le mot de passe n'a pas été saisi"
        except:
            return "Erreur pendant le traitement"

    # Fonction pour supprimer l'utilisateur 
    def delete(self, id):
        try:
            DB_Query(config.database, f"DELETE FROM users WHERE id = {id};")
            return "User supprimé"
        except:
            return "Erreur pendant le traitement"

    # Fonction pour obtenir tous les utilisateurs   
    def getall(self):
        users = DB_Query(config.database, f"SELECT * FROM users").result
        if users:
            return users
        else:
            return None