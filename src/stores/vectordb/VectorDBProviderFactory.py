from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBEnums
from controllers.BaseController import BaseController

class VectorDBProviderFactory:

    def __init__(self, settings):
        self.config = settings
        self.base_controller = BaseController()
        self._providers = {
            VectorDBEnums.QDRANT.value: self._create_qdrant,
        }

    def create(self, provider: str):
        if provider not in self._providers:
            return None
        return self._providers[provider]()

    def _create_qdrant(self):
        db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
        return QdrantDBProvider(
            db_path=db_path,
            distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
        )