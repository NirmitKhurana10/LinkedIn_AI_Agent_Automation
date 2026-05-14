import sys, os
sys.path.insert(0, os.getcwd())

from src.database.db_manager import DatabaseManager

db = DatabaseManager()
db.init_database()

print(os.path.exists(db.db_path))