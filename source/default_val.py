INDENT = 4
TMP_PATH = "tmp/"
DB_PATH = "data/main.db"

# DB Schema
DB_SCHEMA_MESSAGES = '''CREATE TABLE IF NOT EXISTS messages
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_id INTEGER,
                    to_id INTEGER,
                    text TEXT)'''