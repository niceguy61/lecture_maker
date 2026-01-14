# Tests for AWS Documentation Link Generator
"""
AWS 문서 링크 생성기 테스트
"""

import pytest
from src.generators.aws_docs_link_generator import (
    AWSDocsLinkGenerator,
    AWSDocumentationLinks
)
from src.config import (
    AWS_DOCS_BASE_URL,
    AWS_PRICING_BASE_URL,
    AWS_ARCHITECTURE_CENTER_URL
)


class TestAWSDocsLinkGenerator:
    """AWS 문서 링크 생성기 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 인스턴스"""
        return AWSDocsLinkGenerator()
    
    def test_generator_initialization(self, generator):
        """생성기 초기화 테스트"""
        assert generator.base_docs_url == AWS_DOCS_BASE_URL
        assert generator.pricing_url == AWS_PRICING_BASE_URL
        assert generator.architecture_url == AWS_ARCHITECTURE_CENTER_URL
    
    def test_generate_service_doc_link_known_service(self, generator):
        """알려진 서비스의 문서 링크 생성"""
        link = generator.generate_service_doc_link("EC2")
        assert AWS_DOCS_BASE_URL in link
        assert "ec2" in link.lower()
        assert "/latest/userguide/" in link
    
    def test_generate_service_doc_link_unknown_service(self, generator):
        """알려지지 않은 서비스의 문서 링크 생성"""
        link = generator.generate_service_doc_link("Unknown Service")
        assert AWS_DOCS_BASE_URL in link
        assert "unknown-service" in link.lower()
    
    def test_generate_api_reference_link(self, generator):
        """API 레퍼런스 링크 생성"""
        link = generator.generate_api_reference_link("S3")
        assert AWS_DOCS_BASE_URL in link
        assert "s3" in link.lower()
        assert "/latest/APIReference/" in link
    
    def test_generate_well_architected_link_main(self, generator):
        """Well-Architected Framework 메인 링크 생성"""
        link = generator.generate_well_architected_link()
        assert AWS_DOCS_BASE_URL in link
        assert "wellarchitected" in link
        assert "framework" in link
    
    def test_generate_well_architected_link_pillar(self, generator):
        """Well-Architected Framework 기둥별 링크 생성"""
        pillars = [
            "operational_excellence",
            "security",
            "reliability",
            "performance_efficiency",
            "cost_optimization",
            "sustainability"
        ]
        
        for pillar in pillars:
            link = generator.generate_well_architected_link(pillar)
            assert AWS_DOCS_BASE_URL in link
            assert "wellarchitected" in link
            assert pillar.replace('_', '-') in link
    
    def test_generate_pricing_link_calculator(self, generator):
        """가격 계산기 링크 생성"""
        link = generator.generate_pricing_link()
        assert "calculator.aws" in link
    
    def test_generate_pricing_link_service(self, generator):
        """서비스별 가격 링크 생성"""
        link = generator.generate_pricing_link("EC2")
        assert AWS_PRICING_BASE_URL in link
        assert "ec2" in link.lower()
    
    def test_generate_whitepaper_link_main(self, generator):
        """화이트페이퍼 메인 링크 생성"""
        link = generator.generate_whitepaper_link()
        assert AWS_DOCS_BASE_URL in link
        assert "whitepapers" in link
    
    def test_generate_whitepaper_link_topic(self, generator):
        """주제별 화이트페이퍼 링크 생성"""
        topics = ["security", "cost-optimization", "migration"]
        
        for topic in topics:
            link = generator.generate_whitepaper_link(topic)
            assert AWS_DOCS_BASE_URL in link
            assert "whitepapers" in link
            assert topic in link
    
    def test_generate_case_study_link_company(self, generator):
        """기업별 사례 연구 링크 생성"""
        link = generator.generate_case_study_link(company="Netflix")
        assert AWS_ARCHITECTURE_CENTER_URL in link
        assert "customers" in link
        assert "netflix" in link.lower()
    
    def test_generate_case_study_link_industry(self, generator):
        """산업별 사례 연구 링크 생성"""
        link = generator.generate_case_study_link(industry="Financial Services")
        assert AWS_ARCHITECTURE_CENTER_URL in link
        assert "industries" in link
        assert "financial-services" in link.lower()
    
    def test_generate_case_study_link_main(self, generator):
        """사례 연구 메인 링크 생성"""
        link = generator.generate_case_study_link()
        assert AWS_ARCHITECTURE_CENTER_URL in link
        assert "customers" in link
    
    def test_generate_architecture_pattern_link(self, generator):
        """아키텍처 패턴 링크 생성"""
        link = generator.generate_architecture_pattern_link("microservices")
        assert AWS_ARCHITECTURE_CENTER_URL in link
        assert "patterns" in link
        assert "microservices" in link
    
    def test_generate_best_practices_link(self, generator):
        """베스트 프랙티스 링크 생성"""
        link = generator.generate_best_practices_link("EC2")
        assert AWS_DOCS_BASE_URL in link
        assert "ec2" in link.lower()
        assert "best-practices" in link
    
    def test_generate_security_docs_link_service(self, generator):
        """서비스별 보안 문서 링크 생성"""
        link = generator.generate_security_docs_link("S3")
        assert AWS_DOCS_BASE_URL in link
        assert "s3" in link.lower()
        assert "security" in link
    
    def test_generate_security_docs_link_general(self, generator):
        """일반 보안 문서 링크 생성"""
        link = generator.generate_security_docs_link()
        assert AWS_DOCS_BASE_URL in link
        assert "security" in link
    
    def test_generate_faq_link(self, generator):
        """FAQ 링크 생성"""
        link = generator.generate_faq_link("EC2")
        assert "aws.amazon.com" in link
        assert "ec2" in link.lower()
        assert "faqs" in link
    
    def test_generate_comprehensive_links(self, generator):
        """포괄적인 링크 생성"""
        services = ["EC2", "S3", "RDS"]
        links = generator.generate_comprehensive_links(
            service_names=services,
            include_well_architected=True,
            include_pricing=True,
            include_whitepapers=True,
            company_name="Netflix"
        )
        
        assert isinstance(links, AWSDocumentationLinks)
        assert len(links.service_docs) == 3
        assert len(links.api_references) == 3
        assert len(links.well_architected) > 0
        assert len(links.pricing_links) > 0
        assert len(links.whitepapers) > 0
        assert len(links.case_studies) > 0
    
    def test_generate_comprehensive_links_minimal(self, generator):
        """최소 옵션으로 포괄적인 링크 생성"""
        services = ["Lambda"]
        links = generator.generate_comprehensive_links(
            service_names=services,
            include_well_architected=False,
            include_pricing=False,
            include_whitepapers=False
        )
        
        assert len(links.service_docs) == 1
        assert len(links.api_references) == 1
        assert len(links.well_architected) == 0
        assert len(links.pricing_links) == 0
        assert len(links.whitepapers) == 0
    
    def test_format_links_as_markdown(self, generator):
        """마크다운 형식으로 링크 포맷팅"""
        services = ["EC2", "S3"]
        links = generator.generate_comprehensive_links(
            service_names=services,
            company_name="Netflix"
        )
        
        markdown = generator.format_links_as_markdown(links)
        
        assert "## 📚 참고 자료" in markdown
        assert "### AWS 공식 문서" in markdown
        assert "### API 레퍼런스" in markdown
        assert "### AWS Well-Architected Framework" in markdown
        assert "### 가격 정보" in markdown
        assert "### AWS 화이트페이퍼" in markdown
        assert "### 고객 사례 연구" in markdown
        
        # 링크 형식 확인
        assert "[" in markdown and "](" in markdown


class TestServiceDocPaths:
    """서비스 문서 경로 매핑 테스트"""
    
    @pytest.fixture
    def generator(self):
        return AWSDocsLinkGenerator()
    
    def test_compute_services(self, generator):
        """컴퓨팅 서비스 경로"""
        services = ["EC2", "Lambda", "Auto Scaling"]
        for service in services:
            link = generator.generate_service_doc_link(service)
            assert AWS_DOCS_BASE_URL in link
    
    def test_storage_services(self, generator):
        """스토리지 서비스 경로"""
        services = ["S3", "EBS", "EFS"]
        for service in services:
            link = generator.generate_service_doc_link(service)
            assert AWS_DOCS_BASE_URL in link
    
    def test_database_services(self, generator):
        """데이터베이스 서비스 경로"""
        services = ["RDS", "DynamoDB", "ElastiCache"]
        for service in services:
            link = generator.generate_service_doc_link(service)
            assert AWS_DOCS_BASE_URL in link
    
    def test_networking_services(self, generator):
        """네트워킹 서비스 경로"""
        services = ["VPC", "CloudFront", "Route 53"]
        for service in services:
            link = generator.generate_service_doc_link(service)
            assert AWS_DOCS_BASE_URL in link
    
    def test_security_services(self, generator):
        """보안 서비스 경로"""
        services = ["IAM", "KMS", "GuardDuty"]
        for service in services:
            link = generator.generate_service_doc_link(service)
            assert AWS_DOCS_BASE_URL in link


class TestWellArchitectedPillars:
    """Well-Architected Framework 기둥 테스트"""
    
    @pytest.fixture
    def generator(self):
        return AWSDocsLinkGenerator()
    
    def test_all_pillars_have_links(self, generator):
        """모든 기둥이 링크를 가지는지 확인"""
        pillars = list(generator.WELL_ARCHITECTED_PILLARS.keys())
        
        for pillar in pillars:
            link = generator.generate_well_architected_link(pillar)
            assert AWS_DOCS_BASE_URL in link
            assert "wellarchitected" in link
    
    def test_invalid_pillar_returns_main_page(self, generator):
        """유효하지 않은 기둥은 메인 페이지 반환"""
        link = generator.generate_well_architected_link("invalid_pillar")
        assert AWS_DOCS_BASE_URL in link
        assert "wellarchitected" in link
        assert "welcome" in link


class TestLinkFormatting:
    """링크 포맷팅 테스트"""
    
    @pytest.fixture
    def generator(self):
        return AWSDocsLinkGenerator()
    
    def test_service_name_with_spaces(self, generator):
        """공백이 있는 서비스명 처리"""
        link = generator.generate_service_doc_link("EC2 Instances")
        assert "ec2" in link.lower()
        assert " " not in link.split("/")[-2]  # 경로에 공백 없음
    
    def test_company_name_with_spaces(self, generator):
        """공백이 있는 기업명 처리"""
        link = generator.generate_case_study_link(company="Capital One")
        assert "capital-one" in link.lower()
        assert " " not in link.split("/")[-1]  # 경로에 공백 없음
    
    def test_all_links_are_https(self, generator):
        """모든 링크가 HTTPS인지 확인"""
        services = ["EC2", "S3"]
        links = generator.generate_comprehensive_links(service_names=services)
        
        all_links = (
            links.service_docs +
            links.api_references +
            links.well_architected +
            links.pricing_links +
            links.whitepapers +
            links.case_studies
        )
        
        for link in all_links:
            assert link.startswith("https://"), f"Link is not HTTPS: {link}"
