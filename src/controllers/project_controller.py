import os
from services.file_storage_service import FileStorageService

class ProjectController:

    def __init__(self, storage_service: FileStorageService):
        self.storage = storage_service


    def get_project_path(self, project_id: str):
        project_dir = os.path.join(
            self.storage.files_dir, 
            project_id
        )

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir