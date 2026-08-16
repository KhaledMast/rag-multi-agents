from fastapi import Request, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings, Settings
from helpers.database import get_db_client
from services.file_storage_service import FileStorageService
from stores.llm.templates.template_parser import TemplateParser
from stores.vectordb.providers import QdrantDBProvider
from stores.llm.LLMInterface import LLMInterface

from repositories import (
    ProjectRepository, 
    AssetRepository, 
    ChunkRepository)

from controllers import (
    ProjectController,
    ProcessController, 
    DataController, 
    NLPController)



def get_template_parser(request: Request) -> TemplateParser:
    return request.app.state.template_parser

def get_generation_client(request: Request) -> LLMInterface:
    return request.app.state.generation_client


def get_embedding_client(request: Request) -> LLMInterface:
    return request.app.state.embedding_client


def get_vectordb_client(request: Request) -> QdrantDBProvider:
    return request.app.state.vectordb_client


def get_storage_service() -> FileStorageService:
    return FileStorageService()


def get_project_model(
    db_client: AsyncIOMotorClient = Depends(get_db_client),
    settings: Settings = Depends(get_settings)) -> ProjectRepository:
    return ProjectRepository(db_client=db_client, settings=settings)


def get_asset_model(
    db_client: AsyncIOMotorClient = Depends(get_db_client),
    settings: Settings = Depends(get_settings)) -> AssetRepository:
    return AssetRepository(db_client=db_client, settings=settings)


def get_chunk_model(
    db_client: AsyncIOMotorClient = Depends(get_db_client),
    settings: Settings = Depends(get_settings)) -> ChunkRepository:
    return ChunkRepository(db_client=db_client, settings=settings)


def get_project_controller(
    storage_service: FileStorageService = Depends(get_storage_service)) -> ProjectController:
    return ProjectController(storage_service=storage_service)
    
def get_data_controller(
    storage_service: FileStorageService = Depends(get_storage_service),
    project_controller: ProjectController = Depends(get_project_controller),
    settings: Settings = Depends(get_settings)) -> DataController:
    return DataController(
        storage_service=storage_service, 
        project_controller=project_controller, 
        settings=settings
    )

def get_process_controller(
    project_id: str, 
    project_controller: ProjectController = Depends(get_project_controller)) -> ProcessController:
    return ProcessController(
        project_id=project_id, 
        project_controller=project_controller
    )


def get_process_controller(
    project_id: str, 
    project_controller: ProjectController = Depends(get_project_controller)) -> ProcessController:
    return ProcessController(
        project_id=project_id, 
        project_controller=project_controller
    )


def get_nlp_controller(
    vectordb_client: QdrantDBProvider = Depends(get_vectordb_client),
    generation_client: LLMInterface = Depends(get_generation_client),
    embedding_client: LLMInterface = Depends(get_embedding_client),
    template_parser: TemplateParser = Depends(get_template_parser)) -> NLPController:
    return NLPController(
        vectordb_client=vectordb_client,
        generation_client=generation_client,
        embedding_client=embedding_client,
        template_parser=template_parser
    )
