# Pytest Configuration
"""
pytest 설정 및 공통 픽스처
"""

import pytest
from pathlib import Path
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def project_root_path():
    """프로젝트 루트 경로 픽스처"""
    return Path(__file__).parent.parent


@pytest.fixture
def sample_day_number():
    """샘플 일차 번호"""
    return 1


@pytest.fixture
def sample_week_number():
    """샘플 주차 번호"""
    return 1


@pytest.fixture
def study_materials_path(project_root_path):
    """스터디 자료 경로 픽스처"""
    return project_root_path / "aws-saa-study-materials"


@pytest.fixture
def templates_path(project_root_path):
    """템플릿 경로 픽스처"""
    return project_root_path / "templates"
