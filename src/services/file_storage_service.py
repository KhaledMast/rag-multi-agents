from pathlib import Path

class FileStorageService:

    def __init__(self):
        
        self.base_path: Path = Path(__file__).resolve().parent.parent.parent   
        self.files_dir: Path = self.base_path / "storage" / "assets" / "files"        
        self.database_dir: Path = self.base_path / "storage" / "assets" / "database"
 
        self.files_dir.mkdir(parents=True, exist_ok=True)
        self.database_dir.mkdir(parents=True, exist_ok=True)
        
    def get_database_path(self, db_name: str):

        safe_db_name = Path(db_name).name        
        database_path = self.database_dir / safe_db_name
        database_path.mkdir(parents=True, exist_ok=True)

        return str(database_path)
    