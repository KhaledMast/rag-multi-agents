from typing import List, Tuple
from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
import math

class ProjectModel(BaseDataModel):

    def __init__(self, db_client: AsyncIOMotorClient):
        super().__init__(db_client=db_client)
              
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECTS_NAME.value]
        

    async def create_project(self, project: Project) -> Project:
        """
        Create a new project in the database.

        Args:
            project (Project): The project data to be inserted.

        Returns:
            Project: The newly created project object.
        """
        try:
            project_data = project.model_dump(by_alias=True, exclude_none=True)

            result = await self.collection.insert_one(project_data)
            project.id = result.inserted_id  

            return project
        except DuplicateKeyError:
            raise ValueError(f"Project with id {project.project_id} already exists")

    async def get_project_or_create_one(self, project_id: str) -> Project:
        """
        Retrieve a project by ID or create a new one if it doesn't exist.

        Args:
            project_id (str): The ID of the project to retrieve or create.

        Returns:
            Project: The retrieved or newly created project object.
        """

        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record is None:
            project = Project(project_id=project_id)
            project = await self.create_project(project)

            return project

        return Project(**record)

    async def get_all_projects(self, page: int=1, page_size: int=10) -> Tuple[List[Project], int]:
        """
        Retrieve all projects from the database.

        Args:
            page (int): The page number for pagination.
            page_size (int): The maximum number of projects to retrieve per page.

        Returns:
            tuple[List[Project], int]: A tuple containing the list of retrieved project objects and the total number of pages.
        """
        total_documents = await self.collection.count_documents({})
        if total_documents == 0:
            return [], 0

        total_pages = math.ceil(total_documents / page_size)

        if total_documents % page_size > 0:
            total_pages += 1
    
        skip = (page - 1) * page_size
        cursor = self.collection.find().skip(skip).limit(page_size)
        records = await cursor.to_list(length=page_size)
        
        projects = [Project(**record) for record in records]
        return projects, total_pages

