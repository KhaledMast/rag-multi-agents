from repositories.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from helpers.config import Settings
from typing import List
from langdetect import detect, LangDetectException
import json, logging

logger = logging.getLogger(__name__)


class NLPController:

    def __init__(self, vectordb_client, generation_client, embedding_client, 
                        template_parser=None, reranking_client=None,
                        rerank_top: int = 5, settings: Settings = None):

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.reranking_client = reranking_client
        self.template_parser = template_parser
        self.rerank_top = rerank_top
        self.settings = settings

        self.default_language = settings.DEFAULT_LANG
        self.supported_languages = {
            lang for lang in (settings.DEFAULT_LANG, settings.PRIMARY_LANG, settings.SECONDARY_LANG)
            if lang
        }


    def _detect_supported_language(self, query: str) -> str:
        try:
            detected = detect(query)
        except LangDetectException:
            logger.warning("langdetect failed — fallback to '%s'", self.default_language)
            return self.default_language

        if detected not in self.supported_languages:
            logger.info("Language detected '%s' unsupported — fallback to '%s'", detected, self.default_language)
            return self.default_language

        return detected


    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()

    def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )

    def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                                    chunks_ids: List[int], 
                                    do_reset: bool = False):
        
        collection_name = self.create_collection_name(project_id=project.project_id)

        texts = [c.chunk_text for c in chunks ]
        metadata = [c.chunk_metadata for c in  chunks]
        vectors = [
            self.embedding_client.embed_text(text=text, 
                                            document_type=DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]

        # Create collection if not exists
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )

        # Insert into vector db
        _ = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )

        return True

    def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):

        collection_name = self.create_collection_name(project_id=project.project_id)

        vector = self.embedding_client.embed_text(text=text, 
                                                 document_type=DocumentTypeEnum.QUERY.value)

        if not vector or len(vector) == 0:
            return False

        # Semantic search
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )

        if not results:
            return False

        return results

    def rerank_retrieved_documents(self, query: str, documents: list, top_n: int = None):

        if not self.reranking_client or not documents:
            return documents

        top_n = top_n if top_n is not None else self.rerank_top

        return self.reranking_client.rerank_documents(
            query=query,
            documents=documents,
            top_n=top_n,
        )

    def answer_rag_question(self, project: Project, query: str, limit: int = 10):
        
        answer, full_prompt, chat_history = None, None, None

        # result = detect(query)
        # detected_lang = result if result is not None else "en"

        detected_lang = self._detect_supported_language(query)

        retrieved_documents = self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit,
        )

        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history

        
        retrieved_documents = self.rerank_retrieved_documents(
            query=query,
            documents=retrieved_documents,
        )

        system_prompt = self.template_parser.get("rag", "system_prompt", detected_lang)


        documents_prompts = self.template_parser.get("rag", "document_prompt", detected_lang, {
            "documents": [
                {"num": idx + 1, "chunk_text": doc.text}
                for idx, doc in enumerate(retrieved_documents)
            ]
        })

        footer_prompt = self.template_parser.get("rag", "footer_prompt", detected_lang,{
            "query": query
        })

        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

        full_prompt = "\n\n".join([ documents_prompts,  footer_prompt])

     
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history
        )

        return answer, full_prompt, chat_history
    