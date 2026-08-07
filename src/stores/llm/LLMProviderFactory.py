from .LLMEnums import LLMEnums
from .providers import OpenAIProvider, CoHereProvider

class LLMProviderFactory:

    def __init__(self, settings):

        self.app_settings = settings

        self._providers = {
            LLMEnums.OPENAI.value: self._create_openai,
            LLMEnums.COHERE.value: self._create_cohere,
        }

    def create(self, provider: str):
        if provider not in self._providers:
            return None
        return self._providers[provider]()

    def _create_openai(self):
        return OpenAIProvider(
            api_key=self.app_settings.OPENAI_API_KEY,
            api_url=self.app_settings.OPENAI_API_URL,
            default_input_max_characters=self.app_settings.INPUT_DAFAULT_MAX_CHARACTERS,
            default_generation_max_output_tokens=self.app_settings.GENERATION_DAFAULT_MAX_TOKENS,
            default_generation_temperature=self.app_settings.GENERATION_DAFAULT_TEMPERATURE,
        )

    def _create_cohere(self):
        return CoHereProvider(
            api_key=self.app_settings.COHERE_API_KEY,
            default_input_max_characters=self.app_settings.INPUT_DAFAULT_MAX_CHARACTERS,
            default_generation_max_output_tokens=self.app_settings.GENERATION_DAFAULT_MAX_TOKENS,
            default_generation_temperature=self.app_settings.GENERATION_DAFAULT_TEMPERATURE,
        )
    