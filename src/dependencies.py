from fastapi import Request, Depends
from stores.llm.templates.template_parser import TemplateParser
from stores.vectordb.providers import QdrantDBProvider
from stores.llm.LLMInterface import LLMInterface
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings, Settings
from helpers.database import get_db_client
from controllers import ProcessController, DataController, NLPController
from models.ProjectModel import ProjectModel
from models.AssetModel import AssetModel
from models.ChunkModel import ChunkModel



def get_template_parser(request: Request) -> TemplateParser:
    return request.app.state.template_parser


def get_project_model(
    db_client: AsyncIOMotorClient = Depends(get_db_client),
    settings: Settings = Depends(get_settings)) -> ProjectModel:
    return ProjectModel(db_client=db_client, settings=settings)


def get_asset_model(
    db_client: AsyncIOMotorClient = Depends(get_db_client),
    settings: Settings = Depends(get_settings)) -> AssetModel:
    return AssetModel(db_client=db_client, settings=settings)


def get_chunk_model(
    db_client: AsyncIOMotorClient = Depends(get_db_client),
    settings: Settings = Depends(get_settings)) -> ChunkModel:
    return ChunkModel(db_client=db_client, settings=settings)

def get_generation_client(request: Request) -> LLMInterface:
    return request.app.state.generation_client


def get_embedding_client(request: Request) -> LLMInterface:
    return request.app.state.embedding_client


def get_vectordb_client(request: Request) -> QdrantDBProvider:
    return request.app.state.vectordb_client

def get_process_controller(
    project_id: str, 
    settings: Settings = Depends(get_settings)
) -> ProcessController:
    return ProcessController(project_id=project_id, settings=settings)

def get_data_controller(
    settings: Settings = Depends(get_settings)
) -> DataController:
    return DataController(settings=settings)

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



