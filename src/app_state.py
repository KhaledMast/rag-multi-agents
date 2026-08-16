from dataclasses import dataclass
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from services.file_storage_service import FileStorageService
from stores.llm.LLMInterface import LLMInterface
from stores.llm.templates.template_parser import TemplateParser
from stores.vectordb.VectorDBInterface import VectorDBInterface  # cf. note en bas


@dataclass
class AppState:
    """Regroupe toutes les ressources partagées de l'app RAG."""
    storage_service: FileStorageService
    mongodb_client: AsyncIOMotorClient
    mongodb_database: AsyncIOMotorDatabase
    generation_client: LLMInterface
    embedding_client: LLMInterface
    vectordb_client: VectorDBInterface
    template_parser: TemplateParser

    async def shutdown(self) -> None:
        self.mongodb_client.close()
        if self.vectordb_client is not None:
            self.vectordb_client.disconnect()
            