# Configuration and Constants
"""
시스템 전역 설정 및 상수 정의
"""

import os
from pathlib import Path

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent
STUDY_MATERIALS_ROOT = PROJECT_ROOT / "aws-saa-study-materials"
RESOURCES_ROOT = STUDY_MATERIALS_ROOT / "resources"
PREREQUISITES_ROOT = RESOURCES_ROOT / "prerequisites"

# 템플릿 경로
TEMPLATES_ROOT = PROJECT_ROOT / "templates"

# 콘텐츠 생성 설정
DEFAULT_LANGUAGE = "ko"
ENABLE_MERMAID_DIAGRAMS = True
ENABLE_CONSOLE_GUIDES = True

# AWS 문서 링크 베이스 URL
AWS_DOCS_BASE_URL = "https://docs.aws.amazon.com"
AWS_PRICING_BASE_URL = "https://aws.amazon.com/pricing"
AWS_ARCHITECTURE_CENTER_URL = "https://aws.amazon.com/architecture"

# 콘텐츠 섹션 필수 항목
REQUIRED_CASE_STUDY_SECTIONS = [
    "사례 개요",
    "비즈니스 도전과제",
    "AWS 솔루션 아키텍처",
    "구현 세부사항",
    "비즈니스 임팩트",
    "다른 서비스와의 연계",
    "참고 자료",
    "학습 포인트"
]

REQUIRED_BEST_PRACTICES_SECTIONS = [
    "서비스 연계 패턴",
    "아키텍처 진화 경로",
    "비용 최적화 전략",
    "보안 베스트 프랙티스"
]

REQUIRED_TROUBLESHOOTING_SECTIONS = [
    "일반적인 문제 상황들",
    "실습 시나리오",
    "모니터링 및 알람 설정"
]

# Mermaid 다이어그램 유형
MERMAID_DIAGRAM_TYPES = [
    "main-architecture",
    "data-flow",
    "troubleshooting-flow",
    "cost-optimization",
    "cross-day-integration",
    "evolution-path"
]

# 실습 환경 설정
DEFAULT_AWS_REGION = "ap-northeast-2"  # 서울 리전
FREE_TIER_PRIORITY = True
INCLUDE_CLEANUP_SCRIPTS = True

# 로깅 설정
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
