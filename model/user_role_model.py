from database.connect import DB_Query
from view.config import config
from model.role_model import RoleModel
from model.user_model import UserModel

# Class pour géré tous les opérations concernant les roles des utilisateurs dans la base de données 
class UserRoleModel:
    def __init__(self, user=UserModel(), role=RoleModel()):
        self.user = user
        self.role = role
    
    # Fonction pour sauvgarder et affecter un role à un utilisateur
    def save(self):
        try:
            if self.role and self.user.name:
                DB_Query(config.database, f"INSERT INTO user_role (user_id, role_id) VALUES ('{self.user.id}', '{self.role.id}');")
            else:
                return "username ou role n'a pas été saisi"
        except:
            return "Erreur pendant le traitement"
    
    # Fonction pour obtenir les roles d'un utilisateur
    def get(self):
        if self.user.name:
            query_result = DB_Query(config.database, f"SELECT * FROM user_role WHERE user_id = '{self.user.id}'")
            roles = []
            for user_role in query_result.result:
                role = RoleModel()
                role.get(id=user_role[1])
                roles.append(role.name)
            return roles
        else:
            return "Insérer le nom de l'utilisateur"
    
    # Fonction pour obtenir un utilisateur et le défini dans l'instance de l'objet
    def set_userid(self, user_id):
        self.user.get(id=user_id)
    
    # Fonction pour supprimer les roles d'un utilisateur 
    def delete(self, id):
        try:
            DB_Query(config.database, f"DELETE FROM user_role WHERE user_id = {id};")
            return True
        except:
            return False