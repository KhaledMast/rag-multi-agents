from fastapi import Depends, Request
from motor.motor_asyncio import AsyncIOMotorClient
from controllers import DataController, NLPController, ProcessController, ProjectController
from app_state import AppState
from helpers.config import Settings, get_settings
from repositories import AssetRepository, ChunkRepository, ProjectRepository
from services.file_storage_service import FileStorageService
from stores.llm.LLMInterface import LLMInterface
from stores.llm.templates.template_parser import TemplateParser
from stores.vectordb.VectorDBInterface import VectorDBInterface


def get_app_state(request: Request) -> AppState:
    """Point d'entrée unique vers l'état partagé. Tout le reste en découle."""
    return request.app.state.app_state


def get_db_client(state: AppState = Depends(get_app_state)) -> AsyncIOMotorClient:
    return state.mongodb_client


def get_generation_client(state: AppState = Depends(get_app_state)) -> LLMInterface:
    return state.generation_client


def get_embedding_client(state: AppState = Depends(get_app_state)) -> LLMInterface:
    return state.embedding_client


def get_vectordb_client(state: AppState = Depends(get_app_state)) -> VectorDBInterface:
    return state.vectordb_client


def get_template_parser(state: AppState = Depends(get_app_state)) -> TemplateParser:
    return state.template_parser


def get_storage_service(state: AppState = Depends(get_app_state)) -> FileStorageService:
    return state.storage_service


def get_project_model(
    db_client: AsyncIOMotorClient = Depends(get_db_client),
    settings: Settings = Depends(get_settings),
) -> ProjectRepository:
    return ProjectRepository(db_client=db_client, settings=settings)


def get_asset_model(
    db_client: AsyncIOMotorClient = Depends(get_db_client),
    settings: Settings = Depends(get_settings),
) -> AssetRepository:
    return AssetRepository(db_client=db_client, settings=settings)


def get_chunk_model(
    db_client: AsyncIOMotorClient = Depends(get_db_client),
    settings: Settings = Depends(get_settings),
) -> ChunkRepository:
    return ChunkRepository(db_client=db_client, settings=settings)


def get_project_controller(
    storage_service: FileStorageService = Depends(get_storage_service),
) -> ProjectController:
    return ProjectController(storage_service=storage_service)


def get_data_controller(
    storage_service: FileStorageService = Depends(get_storage_service),
    project_controller: ProjectController = Depends(get_project_controller),
    settings: Settings = Depends(get_settings),
) -> DataController:
    return DataController(
        storage_service=storage_service,
        project_controller=project_controller,
        settings=settings,
    )


def get_process_controller(
    project_id: str,
    project_controller: ProjectController = Depends(get_project_controller),
) -> ProcessController:
    return ProcessController(project_id=project_id, project_controller=project_controller)


def get_nlp_controller(
    vectordb_client: VectorDBInterface = Depends(get_vectordb_client),
    generation_client: LLMInterface = Depends(get_generation_client),
    embedding_client: LLMInterface = Depends(get_embedding_client),
    template_parser: TemplateParser = Depends(get_template_parser),
) -> NLPController:
    return NLPController(
        vectordb_client=vectordb_client,
        generation_client=generation_client,
        embedding_client=embedding_client,
        template_parser=template_parser,
    )