from functools import lru_cache

from lingua import LanguageDetector, LanguageDetectorBuilder


def parse_language(text: str) -> str:
    language = _get_language_detector().detect_language_of(text)
    return language.iso_code_639_1.name.lower()


@lru_cache
def _get_language_detector() -> LanguageDetector:
    return LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().build()
