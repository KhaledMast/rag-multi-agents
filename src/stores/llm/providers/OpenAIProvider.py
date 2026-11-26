from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging

class OpenAIProvider(LLMInterface):

    def __init__(self, api_key: str, 
                        api_url: str=None,
                        default_input_max_characters: int=1000,
                        default_generation_max_output_tokens: int=1000,
                        default_generation_temperature: float=0.1):
        
        self.api_key = api_key
        self.api_url = api_url
        
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None


        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_url if self.api_url else None
        )

        self.enums = OpenAIEnums
        self.logger = logging.getLogger(__name__)


    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id


    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id  
        self.embedding_size = embedding_size  


    def process_text(self, text: str, max_characters: int = None):
        max_characters = max_characters if max_characters is not None else self.default_input_max_characters
        if max_characters <= 0:  # 0 ou None désactive la troncature
            return text.strip()
        return text[:max_characters].strip()


    def generate_text(self, prompt: str, chat_history: list=None, max_output_tokens: int=None,
                            temperature: float = None):
        

        if not self.client:
            self.logger.error("OpenAI Client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature


        messages = list(chat_history) if chat_history else []

        messages.append(
            self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value, truncate=False)
        )

        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=messages,
            max_tokens=max_output_tokens,
            temperature=temperature
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None

        return response.choices[0].message.content
    
        
    def embed_text(self, text: str, document_type: str=None):

        if not self.client:
            self.logger.error("OpenAI Client was not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None

        response = self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text,
        )

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with OpenAI")
            return None

        return response.data[0].embedding

    
    def construct_prompt(self, prompt: str, role: str, truncate: bool = True):
        return {
            "role": role,
            "content": self.process_text(prompt) if truncate else prompt.strip()
        }

    def rerank_documents(self, query: str, documents: list, top_n: int = None):
        return documents[:top_n] if top_n else documents

    def set_rerank_model(self, model_id: str):
        pass