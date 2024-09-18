from functools import lru_cache

from lingua import LanguageDetector, LanguageDetectorBuilder

from jg.coop.lib.async_utils import call_async


def parse_language(text: str) -> str:
    language = _get_language_detector().detect_language_of(text)
    return language.iso_code_639_1.name.lower()


async def async_parse_language(text: str) -> str:
    return await call_async(parse_language, text)


@lru_cache
def _get_language_detector() -> LanguageDetector:
    return LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().build()
