import os

class FileStorageService:

    def __init__(self):
        
        self.base_path = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(
            self.base_path, 
            "assets/files"
        )

        self.database_dir = os.path.join(
            self.base_path,
            "assets/database"
        )
 

    def get_database_path(self, db_name: str):

        database_path = os.path.join(
            self.database_dir,
            db_name
        )

        if not os.path.exists(database_path):
            os.makedirs(database_path)

        return database_path
    