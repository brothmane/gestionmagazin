from database.connect import DB_Query
from view.config import config

# Class pour géré tous les opérations concernant les roles 
class RoleModel:
    def __init__(self):
        self.id = None
        self.name = None
    
    def set(self, role_name):
        self.name = str(role_name).lower()
    
    # Fonction pour obtenir un role à partir de la base de donnée
    def get(self, id=None, role_name=None):
        if id:                      # Obtenir un role suivant leur id
            role = DB_Query(config.database, f"SELECT * FROM role WHERE ID = {id}").result
            if role:
                self.id = role[0][0]
                self.name = role[0][1]
                return role
            else:
                return None
        elif role_name:                     # Obtenir un role suivant leur name
            role = DB_Query(config.database, f"SELECT * FROM role WHERE name = '{str(role_name).lower()}'").result
            if role:
                self.id = role[0][0]
                self.name = role[0][1]
                return role
            else:
                return None
        else:
            return None
    
    # Fonction pour sauvgarder le role dans la base de donnée
    def save(self):
        try:
            if self.name:
                role = DB_Query(config.database, f"INSERT INTO role (name) VALUES ('{self.name}');")
                return role.lastrowid
            else:
                return "Le nom de role n'a pas été saisi"
        except:
            return "Erreur pendant le traitement"

    # Fonction pour obtenir tous les roles      
    def getall(self):
        roles = DB_Query(config.database, f"SELECT * FROM role").result
        if roles:
            return roles
        else:
            return None