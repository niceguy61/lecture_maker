# Tests for Terminology Dictionary
"""
Task 11.1: 기술 용어 사전 구축 테스트
Requirements: 10.3, 10.4
"""

import pytest
from src.terminology import (
    TerminologyEntry,
    TermCategory,
    AWS_SERVICES,
    TECHNICAL_TERMS,
    ARCHITECTURAL_CONCEPTS,
    OPERATIONAL_TERMS,
    get_korean_term,
    get_english_term,
    get_term_entry,
    get_terms_by_category,
    search_terms,
    get_all_aws_services,
    get_service_count,
    get_total_term_count,
    validate_terminology_consistency
)


class TestTerminologyEntry:
    """TerminologyEntry 데이터 클래스 테스트"""
    
    def test_terminology_entry_creation(self):
        """용어 항목 생성 테스트"""
        entry = TerminologyEntry(
            korean="테스트 서비스",
            english="Test Service",
            category=TermCategory.SERVICE,
            abbreviation="TS"
        )
        
        assert entry.korean == "테스트 서비스"
        assert entry.english == "Test Service"
        assert entry.category == TermCategory.SERVICE
        assert entry.abbreviation == "TS"
        assert entry.related_terms == []
    
    def test_terminology_entry_with_descriptions(self):
        """설명이 포함된 용어 항목 테스트"""
        entry = TerminologyEntry(
            korean="테스트",
            english="Test",
            category=TermCategory.TECHNICAL,
            description_ko="테스트 설명",
            description_en="Test description"
        )
        
        assert entry.description_ko == "테스트 설명"
        assert entry.description_en == "Test description"


class TestAWSServices:
    """AWS 서비스 용어 테스트"""
    
    def test_aws_services_not_empty(self):
        """AWS 서비스 딕셔너리가 비어있지 않은지 확인"""
        assert len(AWS_SERVICES) > 0
    
    def test_ec2_service_exists(self):
        """EC2 서비스 용어 존재 확인"""
        assert "EC2" in AWS_SERVICES
        ec2 = AWS_SERVICES["EC2"]
        assert ec2.korean == "일래스틱 컴퓨트 클라우드"
        assert ec2.english == "Elastic Compute Cloud"
        assert ec2.abbreviation == "EC2"
    
    def test_s3_service_exists(self):
        """S3 서비스 용어 존재 확인"""
        assert "S3" in AWS_SERVICES
        s3 = AWS_SERVICES["S3"]
        assert s3.korean == "심플 스토리지 서비스"
        assert s3.english == "Simple Storage Service"
    
    def test_lambda_service_exists(self):
        """Lambda 서비스 용어 존재 확인"""
        assert "Lambda" in AWS_SERVICES
        lambda_entry = AWS_SERVICES["Lambda"]
        assert lambda_entry.korean == "람다"
        assert lambda_entry.english == "Lambda"
    
    def test_all_services_have_category(self):
        """모든 서비스가 카테고리를 가지는지 확인"""
        for key, entry in AWS_SERVICES.items():
            assert entry.category is not None
            assert isinstance(entry.category, TermCategory)


class TestTechnicalTerms:
    """기술 용어 테스트"""
    
    def test_technical_terms_not_empty(self):
        """기술 용어 딕셔너리가 비어있지 않은지 확인"""
        assert len(TECHNICAL_TERMS) > 0
    
    def test_region_term_exists(self):
        """Region 용어 존재 확인"""
        assert "Region" in TECHNICAL_TERMS
        region = TECHNICAL_TERMS["Region"]
        assert region.korean == "리전"
        assert region.english == "Region"
    
    def test_availability_zone_term_exists(self):
        """Availability Zone 용어 존재 확인"""
        assert "Availability Zone" in TECHNICAL_TERMS
        az = TECHNICAL_TERMS["Availability Zone"]
        assert az.korean == "가용 영역"
        assert az.abbreviation == "AZ"


class TestArchitecturalConcepts:
    """아키텍처 개념 용어 테스트"""
    
    def test_architectural_concepts_not_empty(self):
        """아키텍처 개념 딕셔너리가 비어있지 않은지 확인"""
        assert len(ARCHITECTURAL_CONCEPTS) > 0
    
    def test_high_availability_exists(self):
        """High Availability 용어 존재 확인"""
        assert "High Availability" in ARCHITECTURAL_CONCEPTS
        ha = ARCHITECTURAL_CONCEPTS["High Availability"]
        assert ha.korean == "고가용성"
        assert ha.abbreviation == "HA"
    
    def test_serverless_exists(self):
        """Serverless 용어 존재 확인"""
        assert "Serverless" in ARCHITECTURAL_CONCEPTS
        serverless = ARCHITECTURAL_CONCEPTS["Serverless"]
        assert serverless.korean == "서버리스"


class TestOperationalTerms:
    """운영 용어 테스트"""
    
    def test_operational_terms_not_empty(self):
        """운영 용어 딕셔너리가 비어있지 않은지 확인"""
        assert len(OPERATIONAL_TERMS) > 0
    
    def test_deployment_term_exists(self):
        """Deployment 용어 존재 확인"""
        assert "Deployment" in OPERATIONAL_TERMS
        deployment = OPERATIONAL_TERMS["Deployment"]
        assert deployment.korean == "배포"
    
    def test_rollback_term_exists(self):
        """Rollback 용어 존재 확인"""
        assert "Rollback" in OPERATIONAL_TERMS
        rollback = OPERATIONAL_TERMS["Rollback"]
        assert rollback.korean == "롤백"


class TestHelperFunctions:
    """헬퍼 함수 테스트"""
    
    def test_get_korean_term_for_service(self):
        """영어 서비스명의 한글 번역 조회"""
        korean = get_korean_term("EC2")
        assert korean == "일래스틱 컴퓨트 클라우드"
    
    def test_get_korean_term_for_technical(self):
        """영어 기술 용어의 한글 번역 조회"""
        korean = get_korean_term("Region")
        assert korean == "리전"
    
    def test_get_korean_term_not_found(self):
        """존재하지 않는 용어 조회"""
        korean = get_korean_term("NonExistentService")
        assert korean is None
    
    def test_get_english_term_from_korean(self):
        """한글 용어의 영어 번역 조회"""
        english = get_english_term("람다")
        assert english == "Lambda"
    
    def test_get_english_term_not_found(self):
        """존재하지 않는 한글 용어 조회"""
        english = get_english_term("존재하지않는서비스")
        assert english is None
    
    def test_get_term_entry_by_english(self):
        """영어로 용어 항목 전체 조회"""
        entry = get_term_entry("S3")
        assert entry is not None
        assert entry.korean == "심플 스토리지 서비스"
        assert entry.english == "Simple Storage Service"
    
    def test_get_term_entry_by_korean(self):
        """한글로 용어 항목 전체 조회"""
        entry = get_term_entry("람다")
        assert entry is not None
        assert entry.english == "Lambda"
    
    def test_get_terms_by_category_service(self):
        """서비스 카테고리 용어 필터링"""
        services = get_terms_by_category(TermCategory.SERVICE)
        assert len(services) > 0
        # AWS_SERVICES의 모든 항목이 포함되어야 함
        assert "EC2" in services
        assert "S3" in services
    
    def test_get_terms_by_category_architectural(self):
        """아키텍처 카테고리 용어 필터링"""
        architectural = get_terms_by_category(TermCategory.ARCHITECTURAL)
        assert len(architectural) > 0
        assert any(entry.korean == "고가용성" for entry in architectural.values())
    
    def test_search_terms_by_korean(self):
        """한글 키워드로 용어 검색"""
        results = search_terms("스토리지")
        assert len(results) > 0
        # S3가 검색 결과에 포함되어야 함
        assert any(r.english == "Simple Storage Service" for r in results)
    
    def test_search_terms_by_english(self):
        """영어 키워드로 용어 검색"""
        results = search_terms("compute")
        assert len(results) > 0
        # EC2가 검색 결과에 포함되어야 함
        assert any(r.abbreviation == "EC2" for r in results)
    
    def test_search_terms_case_insensitive(self):
        """대소문자 구분 없이 검색"""
        results_lower = search_terms("lambda")
        results_upper = search_terms("LAMBDA")
        assert len(results_lower) == len(results_upper)
    
    def test_get_all_aws_services(self):
        """모든 AWS 서비스 조회"""
        services = get_all_aws_services()
        assert len(services) > 0
        assert "EC2" in services
        assert "S3" in services
        assert "Lambda" in services
    
    def test_get_service_count(self):
        """AWS 서비스 수 조회"""
        count = get_service_count()
        assert count > 0
        assert count == len(AWS_SERVICES)
    
    def test_get_total_term_count(self):
        """전체 용어 수 조회"""
        total = get_total_term_count()
        expected = (len(AWS_SERVICES) + 
                   len(TECHNICAL_TERMS) + 
                   len(ARCHITECTURAL_CONCEPTS) + 
                   len(OPERATIONAL_TERMS))
        assert total == expected
        assert total > 0


class TestTerminologyConsistency:
    """용어 일관성 테스트"""
    
    def test_validate_terminology_consistency(self):
        """용어 일관성 검증"""
        issues = validate_terminology_consistency()
        
        assert "duplicates" in issues
        assert "missing_descriptions" in issues
        assert "missing_categories" in issues
        
        # 중복 용어가 없어야 함
        assert len(issues["duplicates"]) == 0, f"Duplicate terms found: {issues['duplicates']}"
    
    def test_all_services_have_korean_translation(self):
        """모든 서비스가 한글 번역을 가지는지 확인"""
        for key, entry in AWS_SERVICES.items():
            assert entry.korean, f"Service {key} missing Korean translation"
            assert len(entry.korean) > 0
    
    def test_all_services_have_english_name(self):
        """모든 서비스가 영어 이름을 가지는지 확인"""
        for key, entry in AWS_SERVICES.items():
            assert entry.english, f"Service {key} missing English name"
            assert len(entry.english) > 0
    
    def test_no_duplicate_korean_terms(self):
        """중복된 한글 용어가 없는지 확인"""
        all_terms = {
            **AWS_SERVICES,
            **TECHNICAL_TERMS,
            **ARCHITECTURAL_CONCEPTS,
            **OPERATIONAL_TERMS
        }
        
        korean_terms = [entry.korean for entry in all_terms.values()]
        unique_korean = set(korean_terms)
        
        assert len(korean_terms) == len(unique_korean), "Duplicate Korean terms found"


class TestRequirementCompliance:
    """요구사항 준수 테스트 (Requirements 10.3, 10.4)"""
    
    def test_requirement_10_3_standardized_glossary(self):
        """Requirement 10.3: 표준화된 기술 용어 사전"""
        # 최소 50개 이상의 용어가 등록되어 있어야 함
        total_terms = get_total_term_count()
        assert total_terms >= 50, f"Expected at least 50 terms, got {total_terms}"
        
        # 주요 AWS 서비스들이 포함되어 있어야 함
        required_services = ["EC2", "S3", "Lambda", "RDS", "DynamoDB", "VPC"]
        for service in required_services:
            assert service in AWS_SERVICES, f"Required service {service} not found"
    
    def test_requirement_10_4_consistent_korean_translations(self):
        """Requirement 10.4: 일관된 한국어 번역"""
        # 모든 용어가 한글 번역을 가져야 함
        all_terms = {
            **AWS_SERVICES,
            **TECHNICAL_TERMS,
            **ARCHITECTURAL_CONCEPTS,
            **OPERATIONAL_TERMS
        }
        
        for key, entry in all_terms.items():
            assert entry.korean, f"Term {key} missing Korean translation"
            # 한글이 포함되어 있는지 확인
            assert any('\uac00' <= char <= '\ud7a3' for char in entry.korean), \
                f"Term {key} Korean translation does not contain Hangul characters"
    
    def test_daily_topics_services_covered(self):
        """일별 주제의 주요 서비스들이 용어 사전에 포함되어 있는지 확인"""
        # daily_topics.py에서 자주 언급되는 서비스들
        common_services = [
            "EC2", "S3", "Lambda", "RDS", "DynamoDB", "VPC",
            "CloudFront", "Route 53", "ELB", "IAM", "CloudWatch",
            "SQS", "SNS", "API Gateway", "ElastiCache"
        ]
        
        for service in common_services:
            assert service in AWS_SERVICES, \
                f"Common service {service} from daily topics not in terminology"
