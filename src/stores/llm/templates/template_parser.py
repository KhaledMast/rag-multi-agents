import os
import logging

logger = logging.getLogger(__name__)


class TemplateParser:

    def __init__(self, default_language: str = "en"):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language

        if not self._language_exists(default_language):
            raise ValueError(
                f"default_language='{default_language}' not found in "
                f"{os.path.join(self.current_path, 'locales')}"
            )

    def _language_exists(self, language: str) -> bool:
        if not language:
            return False
        language_path = os.path.join(self.current_path, "locales", language)
        return os.path.exists(language_path)

    def get(self, group: str, key: str, language: str = None, vars: dict = None) -> str | None:

        if not group or not key:
            return None

        vars = vars or {}

        if language and not self._language_exists(language):
            logger.warning(
                "Language '%s' not found (group=%s, key=%s) — fallback to default_language='%s'",
                language, group, key, self.default_language,
            )

        target_language = language if self._language_exists(language) else self.default_language

        group_path = os.path.join(self.current_path, "locales", target_language, f"{group}.py")
        if not os.path.exists(group_path):
            logger.warning(
                "File '%s.py' not found for lang='%s' — fallback to default_language='%s'",
                group, target_language, self.default_language,
            )
            target_language = self.default_language
            group_path = os.path.join(self.current_path, "locales", target_language, f"{group}.py")

        if not os.path.exists(group_path):
            logger.warning(
                "File '%s.py' not found even for default_language='%s' — get() retourne None",
                group, target_language,
            )
            return None

        module = __import__(
            f"stores.llm.templates.locales.{target_language}.{group}",
            fromlist=[group],
        )

        if not module:
            return None

        key_attribute = getattr(module, key, None)
        if key_attribute is None:
            logger.warning(
                "Clé '%s' introuvable dans le module '%s' (lang='%s') — get() retourne None",
                key, group, target_language,
            )
            return None

        return key_attribute.render(**vars)