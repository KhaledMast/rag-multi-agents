import re, os
from .project_controller import ProjectController
from services.file_storage_service import FileStorageService
from helpers.config import Settings
from fastapi import UploadFile
from repositories import ResponseSignal
from helpers.utils import generate_random_string


class DataController:

    def __init__(self, storage_service: FileStorageService, project_controller: ProjectController, settings: Settings):
        self.app_settings = settings
        self.storage = storage_service 
        self.size_scale = 1024 * 1024  
        self.project = project_controller


    def check_upload(self, file: UploadFile):
        # Validate file type
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        # Validate file size
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:  
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value


        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    def generate_unique_file_path(self, original_file_name: str, project_id: str) -> str:

        random_key = generate_random_string()
        project_path = self.project.get_project_path(project_id=project_id)

        cleaned_file_name = self.get_cleaned_file_name(
            original_file_name = original_file_name
        )

        new_file_name = os.path.join(
            project_path,
            f"{random_key}_{cleaned_file_name}"
        )

        while os.path.exists(new_file_name):
            random_key = generate_random_string()
            new_file_name = os.path.join(
                project_path,
                f"{random_key}_{cleaned_file_name}"
            )

        return new_file_name, f"{random_key}_{cleaned_file_name}"

    def get_cleaned_file_name(self, original_file_name: str) -> str:
        cleaned_file_name = re.sub(r'[^\w.]', '', original_file_name.strip())
        cleaned_file_name = cleaned_file_name.replace(' ', '_')
        return cleaned_file_name