import sqlite3

# Nom du fichier de base de données
DB_NAME = "gestion_magasin.db"

def init_database():
    # Connexion à la base de données (le fichier sera créé s'il n'existe pas)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Commandes pour créer les tables
    queries = [
        """
        CREATE TABLE IF NOT EXISTS role (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS user_role (
            user_id INTEGER,
            role_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
            FOREIGN KEY (role_id) REFERENCES role(id) ON DELETE RESTRICT,
            UNIQUE (user_id, role_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            unit TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER DEFAULT 0,
            minqty INTEGER DEFAULT 0,
            normalqty INTEGER DEFAULT 0
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS sales_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE RESTRICT,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
        );
        """,
        "INSERT INTO role (name) VALUES ('admin');",
        "INSERT INTO role (name) VALUES ('inventory');",
        "INSERT INTO role (name) VALUES ('seller');",
        "INSERT INTO users (username, password) VALUES ('admin', 'admin');",
        "INSERT INTO user_role (user_id, role_id) VALUES (1, 1);"
    ]

    # Exécution des commandes
    for query in queries:
        cursor.execute(query)

    # Sauvegarde des changements et fermeture de la connexion
    conn.commit()
    conn.close()

    print("Base de données initialisée avec succès.")

# Appel de la fonction d'initialisation
if __name__ == "__main__":
    init_database()
