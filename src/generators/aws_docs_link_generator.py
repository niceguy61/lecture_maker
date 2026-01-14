# AWS Documentation Link Generator
"""
AWS 문서 링크 생성기
AWS 공식 문서, API 레퍼런스, Well-Architected Framework, 가격 계산기, 화이트페이퍼 링크 자동 생성
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from src.config import (
    AWS_DOCS_BASE_URL,
    AWS_PRICING_BASE_URL,
    AWS_ARCHITECTURE_CENTER_URL
)


@dataclass
class AWSDocumentationLinks:
    """AWS 문서 링크 모음"""
    service_docs: List[str]
    api_references: List[str]
    well_architected: List[str]
    pricing_links: List[str]
    whitepapers: List[str]
    case_studies: List[str]


class AWSDocsLinkGenerator:
    """AWS 문서 링크 생성기"""
    
    # AWS 서비스명과 문서 경로 매핑
    SERVICE_DOC_PATHS = {
        # Compute
        "EC2": "ec2",
        "EC2 Instances": "ec2",
        "Lambda": "lambda",
        "Auto Scaling": "autoscaling",
        "Elastic Beanstalk": "elasticbeanstalk",
        
        # Storage
        "S3": "s3",
        "S3 Buckets": "s3",
        "EBS": "ebs",
        "EBS Volumes": "ebs",
        "EFS": "efs",
        "FSx": "fsx",
        "Storage Gateway": "storagegateway",
        
        # Database
        "RDS": "rds",
        "DynamoDB": "dynamodb",
        "Aurora": "rds/aurora",
        "ElastiCache": "elasticache",
        "Redis": "elasticache/redis",
        "Memcached": "elasticache/memcached",
        "Neptune": "neptune",
        "DocumentDB": "documentdb",
        
        # Networking
        "VPC": "vpc",
        "CloudFront": "cloudfront",
        "Route 53": "route53",
        "ELB": "elasticloadbalancing",
        "ALB": "elasticloadbalancing",
        "NLB": "elasticloadbalancing",
        "Direct Connect": "directconnect",
        "VPN": "vpn",
        
        # Security & Identity
        "IAM": "iam",
        "IAM Users": "iam",
        "IAM Roles": "iam",
        "IAM Policies": "iam",
        "Cognito": "cognito",
        "KMS": "kms",
        "CloudHSM": "cloudhsm",
        "Secrets Manager": "secretsmanager",
        "Certificate Manager": "acm",
        "GuardDuty": "guardduty",
        "Inspector": "inspector",
        "Macie": "macie",
        
        # Monitoring & Management
        "CloudWatch": "cloudwatch",
        "CloudTrail": "cloudtrail",
        "Config": "config",
        "Systems Manager": "systems-manager",
        "Parameter Store": "systems-manager/parameter-store",
        "Patch Manager": "systems-manager/patch-manager",
        "X-Ray": "xray",
        
        # Application Integration
        "SQS": "sqs",
        "SNS": "sns",
        "EventBridge": "eventbridge",
        "Step Functions": "step-functions",
        "API Gateway": "apigateway",
        
        # Developer Tools
        "CodeCommit": "codecommit",
        "CodeBuild": "codebuild",
        "CodeDeploy": "codedeploy",
        "CodePipeline": "codepipeline",
        
        # Analytics
        "Kinesis": "kinesis",
        "EMR": "emr",
        "Athena": "athena",
        "Glue": "glue",
        
        # Machine Learning
        "SageMaker": "sagemaker",
        "Rekognition": "rekognition",
        "Comprehend": "comprehend",
        
        # Management & Governance
        "Organizations": "organizations",
        "Control Tower": "controltower",
        "Service Catalog": "servicecatalog",
        
        # Global Infrastructure
        "Regions": "general/regions",
        "Availability Zones": "general/regions",
        "Edge Locations": "cloudfront/edge-locations",
    }
    
    # Well-Architected Framework 기둥별 링크
    WELL_ARCHITECTED_PILLARS = {
        "operational_excellence": "operational-excellence",
        "security": "security",
        "reliability": "reliability",
        "performance_efficiency": "performance-efficiency",
        "cost_optimization": "cost-optimization",
        "sustainability": "sustainability"
    }
    
    def __init__(self):
        self.base_docs_url = AWS_DOCS_BASE_URL
        self.pricing_url = AWS_PRICING_BASE_URL
        self.architecture_url = AWS_ARCHITECTURE_CENTER_URL
    
    def generate_service_doc_link(self, service_name: str) -> str:
        """서비스 문서 링크 생성
        
        Args:
            service_name: AWS 서비스명
            
        Returns:
            서비스 문서 URL
        """
        doc_path = self.SERVICE_DOC_PATHS.get(service_name)
        if not doc_path:
            # 기본 경로 생성 (서비스명을 소문자로 변환하고 공백을 하이픈으로 치환)
            doc_path = service_name.lower().replace(' ', '-')
        
        return f"{self.base_docs_url}/{doc_path}/latest/userguide/"
    
    def generate_api_reference_link(self, service_name: str) -> str:
        """API 레퍼런스 링크 생성
        
        Args:
            service_name: AWS 서비스명
            
        Returns:
            API 레퍼런스 URL
        """
        doc_path = self.SERVICE_DOC_PATHS.get(service_name)
        if not doc_path:
            doc_path = service_name.lower().replace(' ', '-')
        
        return f"{self.base_docs_url}/{doc_path}/latest/APIReference/"
    
    def generate_well_architected_link(self, pillar: Optional[str] = None) -> str:
        """Well-Architected Framework 링크 생성
        
        Args:
            pillar: 특정 기둥 (operational_excellence, security, reliability, 
                   performance_efficiency, cost_optimization, sustainability)
                   None이면 프레임워크 메인 페이지
            
        Returns:
            Well-Architected Framework URL
        """
        base_url = f"{self.base_docs_url}/wellarchitected/latest/framework"
        
        if pillar and pillar in self.WELL_ARCHITECTED_PILLARS:
            pillar_path = self.WELL_ARCHITECTED_PILLARS[pillar]
            return f"{base_url}/{pillar_path}.html"
        
        return f"{base_url}/welcome.html"
    
    def generate_pricing_link(self, service_name: Optional[str] = None) -> str:
        """가격 정보 링크 생성
        
        Args:
            service_name: AWS 서비스명 (None이면 가격 계산기)
            
        Returns:
            가격 정보 URL
        """
        if service_name:
            # 서비스별 가격 페이지
            service_slug = service_name.lower().replace(' ', '-')
            return f"{self.pricing_url}/{service_slug}/"
        else:
            # AWS 가격 계산기
            return "https://calculator.aws/"
    
    def generate_whitepaper_link(self, topic: Optional[str] = None) -> str:
        """화이트페이퍼 링크 생성
        
        Args:
            topic: 주제 (예: 'security', 'cost-optimization', 'migration')
                  None이면 화이트페이퍼 메인 페이지
            
        Returns:
            화이트페이퍼 URL
        """
        base_url = f"{self.base_docs_url}/whitepapers/latest"
        
        if topic:
            return f"{base_url}/{topic}/"
        
        return f"{base_url}/aws-overview/"
    
    def generate_case_study_link(self, company: Optional[str] = None, industry: Optional[str] = None) -> str:
        """사례 연구 링크 생성
        
        Args:
            company: 기업명
            industry: 산업 분야
            
        Returns:
            사례 연구 URL
        """
        if company:
            company_slug = company.lower().replace(' ', '-')
            return f"{self.architecture_url}/customers/{company_slug}"
        elif industry:
            industry_slug = industry.lower().replace(' ', '-')
            return f"{self.architecture_url}/industries/{industry_slug}"
        else:
            return f"{self.architecture_url}/customers/"
    
    def generate_architecture_pattern_link(self, pattern: Optional[str] = None) -> str:
        """아키텍처 패턴 링크 생성
        
        Args:
            pattern: 패턴명 (예: 'microservices', 'serverless', 'data-lakes')
            
        Returns:
            아키텍처 패턴 URL
        """
        if pattern:
            pattern_slug = pattern.lower().replace(' ', '-')
            return f"{self.architecture_url}/patterns/{pattern_slug}"
        
        return f"{self.architecture_url}/patterns/"
    
    def generate_best_practices_link(self, service_name: str) -> str:
        """베스트 프랙티스 링크 생성
        
        Args:
            service_name: AWS 서비스명
            
        Returns:
            베스트 프랙티스 URL
        """
        doc_path = self.SERVICE_DOC_PATHS.get(service_name)
        if not doc_path:
            doc_path = service_name.lower().replace(' ', '-')
        
        return f"{self.base_docs_url}/{doc_path}/latest/userguide/best-practices.html"
    
    def generate_security_docs_link(self, service_name: Optional[str] = None) -> str:
        """보안 문서 링크 생성
        
        Args:
            service_name: AWS 서비스명 (None이면 일반 보안 문서)
            
        Returns:
            보안 문서 URL
        """
        if service_name:
            doc_path = self.SERVICE_DOC_PATHS.get(service_name)
            if not doc_path:
                doc_path = service_name.lower().replace(' ', '-')
            return f"{self.base_docs_url}/{doc_path}/latest/userguide/security.html"
        
        return f"{self.base_docs_url}/security/"
    
    def generate_faq_link(self, service_name: str) -> str:
        """FAQ 링크 생성
        
        Args:
            service_name: AWS 서비스명
            
        Returns:
            FAQ URL
        """
        service_slug = service_name.lower().replace(' ', '-')
        return f"https://aws.amazon.com/{service_slug}/faqs/"
    
    def generate_comprehensive_links(
        self,
        service_names: List[str],
        include_well_architected: bool = True,
        include_pricing: bool = True,
        include_whitepapers: bool = True,
        company_name: Optional[str] = None
    ) -> AWSDocumentationLinks:
        """포괄적인 AWS 문서 링크 생성
        
        Args:
            service_names: AWS 서비스명 리스트
            include_well_architected: Well-Architected Framework 포함 여부
            include_pricing: 가격 정보 포함 여부
            include_whitepapers: 화이트페이퍼 포함 여부
            company_name: 사례 연구 기업명
            
        Returns:
            AWSDocumentationLinks 객체
        """
        # 서비스 문서 링크
        service_docs = [self.generate_service_doc_link(service) for service in service_names]
        
        # API 레퍼런스 링크
        api_references = [self.generate_api_reference_link(service) for service in service_names]
        
        # Well-Architected Framework 링크
        well_architected = []
        if include_well_architected:
            well_architected = [
                self.generate_well_architected_link(),  # 메인 페이지
                self.generate_well_architected_link("operational_excellence"),
                self.generate_well_architected_link("security"),
                self.generate_well_architected_link("reliability"),
                self.generate_well_architected_link("performance_efficiency"),
                self.generate_well_architected_link("cost_optimization"),
            ]
        
        # 가격 링크
        pricing_links = []
        if include_pricing:
            pricing_links = [
                self.generate_pricing_link(),  # 가격 계산기
            ]
            pricing_links.extend([self.generate_pricing_link(service) for service in service_names[:2]])
        
        # 화이트페이퍼 링크
        whitepapers = []
        if include_whitepapers:
            whitepapers = [
                self.generate_whitepaper_link(),  # AWS 개요
                self.generate_whitepaper_link("security"),
                self.generate_whitepaper_link("cost-optimization"),
                self.generate_whitepaper_link("migration"),
            ]
        
        # 사례 연구 링크
        case_studies = []
        if company_name:
            case_studies.append(self.generate_case_study_link(company=company_name))
        case_studies.append(self.generate_case_study_link())  # 메인 페이지
        
        return AWSDocumentationLinks(
            service_docs=service_docs,
            api_references=api_references,
            well_architected=well_architected,
            pricing_links=pricing_links,
            whitepapers=whitepapers,
            case_studies=case_studies
        )
    
    def format_links_as_markdown(self, links: AWSDocumentationLinks) -> str:
        """링크를 마크다운 형식으로 포맷팅
        
        Args:
            links: AWSDocumentationLinks 객체
            
        Returns:
            마크다운 형식의 링크 문자열
        """
        markdown = "## 📚 참고 자료\n\n"
        
        # 서비스 문서
        if links.service_docs:
            markdown += "### AWS 공식 문서\n"
            for i, link in enumerate(links.service_docs, 1):
                markdown += f"{i}. [서비스 사용자 가이드]({link})\n"
            markdown += "\n"
        
        # API 레퍼런스
        if links.api_references:
            markdown += "### API 레퍼런스\n"
            for i, link in enumerate(links.api_references, 1):
                markdown += f"{i}. [API Reference]({link})\n"
            markdown += "\n"
        
        # Well-Architected Framework
        if links.well_architected:
            markdown += "### AWS Well-Architected Framework\n"
            pillar_names = [
                "Framework 개요",
                "운영 우수성",
                "보안",
                "안정성",
                "성능 효율성",
                "비용 최적화"
            ]
            for i, (name, link) in enumerate(zip(pillar_names, links.well_architected), 1):
                markdown += f"{i}. [{name}]({link})\n"
            markdown += "\n"
        
        # 가격 정보
        if links.pricing_links:
            markdown += "### 가격 정보\n"
            markdown += f"1. [AWS 가격 계산기]({links.pricing_links[0]})\n"
            for i, link in enumerate(links.pricing_links[1:], 2):
                markdown += f"{i}. [서비스 가격 정보]({link})\n"
            markdown += "\n"
        
        # 화이트페이퍼
        if links.whitepapers:
            markdown += "### AWS 화이트페이퍼\n"
            for i, link in enumerate(links.whitepapers, 1):
                markdown += f"{i}. [화이트페이퍼]({link})\n"
            markdown += "\n"
        
        # 사례 연구
        if links.case_studies:
            markdown += "### 고객 사례 연구\n"
            for i, link in enumerate(links.case_studies, 1):
                markdown += f"{i}. [AWS 고객 사례]({link})\n"
            markdown += "\n"
        
        return markdown


def main():
    """CLI 실행 예시"""
    generator = AWSDocsLinkGenerator()
    
    # 예시: EC2 관련 링크 생성
    services = ["EC2", "VPC", "ELB"]
    links = generator.generate_comprehensive_links(
        service_names=services,
        company_name="Netflix"
    )
    
    # 마크다운 형식으로 출력
    markdown = generator.format_links_as_markdown(links)
    print(markdown)


if __name__ == "__main__":
    main()
