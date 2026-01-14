# Generators Package
"""
콘텐츠 생성기 모듈
"""

# Lazy imports to avoid circular dependencies
def __getattr__(name):
    if name == 'CaseStudyGenerator':
        from .case_study_generator import CaseStudyGenerator
        return CaseStudyGenerator
    elif name == 'HandsOnConsoleGenerator':
        from .hands_on_console_generator import HandsOnConsoleGenerator
        return HandsOnConsoleGenerator
    elif name == 'BestPracticesGenerator':
        from .best_practices_generator import BestPracticesGenerator
        return BestPracticesGenerator
    elif name == 'TroubleshootingGenerator':
        from .troubleshooting_generator import TroubleshootingGenerator
        return TroubleshootingGenerator
    elif name == 'get_korean_term_dictionary':
        from .korean_term_dictionary import get_korean_term_dictionary
        return get_korean_term_dictionary
    elif name == 'get_korean_localization_processor':
        from .korean_localization_processor import get_korean_localization_processor
        return get_korean_localization_processor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    'CaseStudyGenerator',
    'HandsOnConsoleGenerator',
    'BestPracticesGenerator',
    'TroubleshootingGenerator',
    'get_korean_term_dictionary',
    'get_korean_localization_processor'
]
