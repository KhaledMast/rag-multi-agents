from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBEnums
from services.file_storage_service import FileStorageService

class VectorDBProviderFactory:

    def __init__(self, storage_service: FileStorageService, settings):
        self.config = settings
        self.storage = storage_service 
        self._providers = {
            VectorDBEnums.QDRANT.value: self._create_qdrant,
        }

    def create(self, provider: str):
        if provider not in self._providers:
            return None
        return self._providers[provider]()

    def _create_qdrant(self):
        db_path = self.storage.get_database_path(db_name=self.config.VECTOR_DB_PATH)
        return QdrantDBProvider(
            db_path=db_path,
            distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
        )