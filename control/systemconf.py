# Class pour géré les variables et les paramètres de session
class GlobalVar:
    def __init__(self, database=None, background=None, session_user=None, session_roles=[], displayed=None):
        self.background = background
        self.database = database
        self.session_user = session_user
        self.session_roles = session_roles
        self.displayed = displayed
        self.prixpercentage = 0.25          
