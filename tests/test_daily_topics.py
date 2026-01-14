# Tests for Daily Topics Configuration
"""
일별 주제 매핑 설정 테스트
"""

import pytest
from src.daily_topics import (
    DAILY_TOPICS,
    get_topic_by_day,
    get_topics_by_week,
    get_related_topics,
    get_all_companies,
    get_topics_by_difficulty
)


class TestDailyTopicsStructure:
    """일별 주제 구조 테스트"""
    
    def test_all_28_days_exist(self):
        """28일 모두 정의되어 있는지 확인"""
        assert len(DAILY_TOPICS) == 28
        for day in range(1, 29):
            assert day in DAILY_TOPICS
    
    def test_topic_has_required_fields(self):
        """각 주제가 필수 필드를 포함하는지 확인"""
        required_fields = [
            "title",
            "primary_services",
            "case_study_company",
            "case_study_focus",
            "related_days",
            "week",
            "difficulty",
            "estimated_hours"
        ]
        
        for day, topic in DAILY_TOPICS.items():
            for field in required_fields:
                assert field in topic, f"Day {day} missing field: {field}"
    
    def test_week_numbers_valid(self):
        """주차 번호가 1-4 범위인지 확인"""
        for day, topic in DAILY_TOPICS.items():
            assert 1 <= topic["week"] <= 4, f"Day {day} has invalid week: {topic['week']}"
    
    def test_difficulty_levels_valid(self):
        """난이도가 유효한 값인지 확인"""
        valid_difficulties = ["basic", "intermediate", "advanced"]
        for day, topic in DAILY_TOPICS.items():
            assert topic["difficulty"] in valid_difficulties, \
                f"Day {day} has invalid difficulty: {topic['difficulty']}"
    
    def test_primary_services_not_empty(self):
        """주요 서비스 목록이 비어있지 않은지 확인"""
        for day, topic in DAILY_TOPICS.items():
            assert len(topic["primary_services"]) > 0, \
                f"Day {day} has no primary services"
    
    def test_case_study_company_exists(self):
        """사례 연구 기업이 지정되어 있는지 확인"""
        for day, topic in DAILY_TOPICS.items():
            assert topic["case_study_company"], \
                f"Day {day} has no case study company"
    
    def test_estimated_hours_positive(self):
        """예상 학습 시간이 양수인지 확인"""
        for day, topic in DAILY_TOPICS.items():
            assert topic["estimated_hours"] > 0, \
                f"Day {day} has invalid estimated hours: {topic['estimated_hours']}"


class TestDailyTopicsHelperFunctions:
    """헬퍼 함수 테스트"""
    
    def test_get_topic_by_day_valid(self):
        """유효한 일차로 주제 가져오기"""
        topic = get_topic_by_day(1)
        assert topic["title"] == "AWS 개요 및 글로벌 인프라"
        assert topic["case_study_company"] == "Netflix"
    
    def test_get_topic_by_day_invalid(self):
        """유효하지 않은 일차로 예외 발생 확인"""
        with pytest.raises(ValueError):
            get_topic_by_day(0)
        
        with pytest.raises(ValueError):
            get_topic_by_day(29)
    
    def test_get_topics_by_week(self):
        """주차별 주제 가져오기"""
        week1_topics = get_topics_by_week(1)
        assert len(week1_topics) == 7
        
        # Week 1은 Day 1-7
        for day in range(1, 8):
            assert day in week1_topics
    
    def test_get_topics_by_week_invalid(self):
        """유효하지 않은 주차로 예외 발생 확인"""
        with pytest.raises(ValueError):
            get_topics_by_week(0)
        
        with pytest.raises(ValueError):
            get_topics_by_week(5)
    
    def test_get_related_topics(self):
        """연관 주제 가져오기"""
        related = get_related_topics(1)
        
        # Day 1의 related_days는 [16, 17]
        assert 16 in related
        assert 17 in related
    
    def test_get_all_companies(self):
        """모든 기업 목록 가져오기"""
        companies = get_all_companies()
        
        assert "Netflix" in companies
        assert "Airbnb" in companies
        assert "Spotify" in companies
        assert len(companies) > 0
    
    def test_get_topics_by_difficulty(self):
        """난이도별 주제 필터링"""
        basic_topics = get_topics_by_difficulty("basic")
        assert len(basic_topics) > 0
        
        for day, topic in basic_topics.items():
            assert topic["difficulty"] == "basic"
    
    def test_get_topics_by_difficulty_invalid(self):
        """유효하지 않은 난이도로 예외 발생 확인"""
        with pytest.raises(ValueError):
            get_topics_by_difficulty("invalid")


class TestWeekDistribution:
    """주차별 분포 테스트"""
    
    def test_week1_has_7_days(self):
        """Week 1이 7일인지 확인"""
        week1 = get_topics_by_week(1)
        assert len(week1) == 7
    
    def test_week2_has_7_days(self):
        """Week 2가 7일인지 확인"""
        week2 = get_topics_by_week(2)
        assert len(week2) == 7
    
    def test_week3_has_7_days(self):
        """Week 3이 7일인지 확인"""
        week3 = get_topics_by_week(3)
        assert len(week3) == 7
    
    def test_week4_has_7_days(self):
        """Week 4가 7일인지 확인"""
        week4 = get_topics_by_week(4)
        assert len(week4) == 7


class TestServiceCoverage:
    """서비스 커버리지 테스트"""
    
    def test_all_topics_have_services(self):
        """모든 주제가 서비스를 포함하는지 확인"""
        for day in range(1, 29):
            topic = get_topic_by_day(day)
            assert len(topic["primary_services"]) > 0
    
    def test_review_days_reference_all_services(self):
        """복습 일차(7, 14, 21, 28)가 이전 일차들을 참조하는지 확인"""
        review_days = [7, 14, 21, 28]
        
        for review_day in review_days:
            topic = get_topic_by_day(review_day)
            related_days = topic["related_days"]
            
            # 복습 일차는 여러 이전 일차를 참조해야 함
            assert len(related_days) > 3, \
                f"Review day {review_day} should reference multiple previous days"


class TestCaseStudyCompanies:
    """사례 연구 기업 테스트"""
    
    def test_unique_companies_per_day(self):
        """각 일차가 고유한 기업을 가지는지 확인 (복습 일차 제외)"""
        companies = []
        review_days = [7, 14, 21, 28]
        
        for day in range(1, 29):
            if day not in review_days:
                topic = get_topic_by_day(day)
                company = topic["case_study_company"]
                companies.append(company)
        
        # 대부분의 기업이 고유해야 함 (일부 중복 허용)
        unique_companies = set(companies)
        assert len(unique_companies) >= 20, \
            "Most days should have unique case study companies"
    
    def test_case_study_focus_not_empty(self):
        """모든 사례 연구 포커스가 비어있지 않은지 확인"""
        for day in range(1, 29):
            topic = get_topic_by_day(day)
            assert topic["case_study_focus"], \
                f"Day {day} has empty case_study_focus"
