from model.user_model import UserModel
from model.role_model import RoleModel
from model.user_role_model import UserRoleModel
import string

ALPHA = string.ascii_letters        # Variable utiliser pour matching que les lettres alphabétiques

# Class pour adapter les informations de l'utilisateur au calss view
class UserController:
    def __init__(self, usermodel=UserModel(), user={"username":str, "password":str}, roles=[]):
        self.usermodel = usermodel
        self.user = user
        self.roles = roles        
    
    # Fonction pour géré et controller le login
    def login(self):   
        if self.user["username"].startswith(tuple(ALPHA)):
            if self.usermodel.get(username=self.user["username"]):
                login_arg = {"check": False, "roles": None}
                if self.user["username"].lower() == self.usermodel.name and self.user["password"] == self.usermodel.password :
                    roles = UserRoleModel(self.usermodel)
                    login_arg["check"] = True
                    login_arg["roles"] = roles.get()
                    return login_arg
                else:
                    return "User ou Mot de passe erroné."
            else:
                return f"Username {self.user["username"].lower()} non trouver."
        else:
            return "Vérifier les valeurs saisi."

    # Fonction pour géré l'addition des utilisateurs
    def add(self):
        if self.user["username"].startswith(tuple(ALPHA)):
            self.usermodel.set(self.user["username"], self.user["password"])
            usersave = self.usermodel.save()
            if type(usersave) == int:
                if self.roles:
                    for role in self.roles:
                        role_set = RoleModel()
                        role_set.get(role_name=role)
                        user_roles = UserRoleModel(self.usermodel, role_set)
                        user_roles.save()
                else:
                    return "Utilisateur enregistrer.\nLes roles non pas été implémenter."
                return "Utilisateur enregistrer."
            else:
                return usersave
        else:
            return "Vérifier les valeurs saisi."
    
    # Fonction pour controller la modification des informations des utilisateurs
    def edit(self, id):
        if self.user["username"].startswith(tuple(ALPHA)):
            self.usermodel.set(self.user["username"], self.user["password"])
            useredit = self.usermodel.edit(id)
            if type(useredit) == int:
                userroles = UserRoleModel()
                rolesdelete = userroles.delete(id)
                if rolesdelete:
                    if self.roles:
                        for role in self.roles:
                            role_set = RoleModel()
                            role_set.get(role_name=role)
                            user_roles = UserRoleModel(self.usermodel, role_set)
                            user_roles.save()
                        return "Utilisateur modifier."
                    else:
                       return "Utilisateur modifier.\nLes roles non pas été implémenter."
                else:
                    return "Utilisateur modifier.\nUne erreur pendant le traiatement des roles."
            else:
                return useredit
        else:
            return "Vérifier les valeurs saisi."
    
    # Fonction pour controler la supprission des utilisateurs 
    def delete(self, id):
        userroles = UserRoleModel()
        delete = userroles.delete(id)
        userdelete = self.usermodel.delete(id)
        
        if delete:
            return userdelete
        else:
            return "Erreur durent le traitement des roles."

    # Fonction pour controller l'obtention de tous les utilisateurs
    def getusers(self):
        users = self.usermodel.getall()
        user_list = []
        for user in users:
            userrolemodel = UserRoleModel()
            userrolemodel.set_userid(user[0])
            users_roles = userrolemodel.get()
            user_list.append({"id": user[0], "username": user[1], "roles": users_roles})
        return user_list
    
    # Fonction pour controller l'obtention d'un utilisateur suivant son id
    def getuser(self, id):
        self.usermodel.get(id)
        userrolemodel = UserRoleModel()
        userrolemodel.set_userid(self.usermodel.id)
        user_roles = userrolemodel.get()
        user = {"id": self.usermodel.id, "username": self.usermodel.name, "roles": user_roles}
        return user
       
