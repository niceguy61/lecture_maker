# AWS Technical Terminology Dictionary (Korean-English Mappings)
"""
AWS 서비스 및 기술 용어 한영 매핑 데이터베이스
Requirements: 10.3 (표준화된 기술 용어 사전), 10.4 (일관된 한국어 번역)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class TermCategory(Enum):
    """용어 카테고리"""
    SERVICE = "service"
    TECHNICAL = "technical"
    ARCHITECTURAL = "architectural"
    OPERATIONAL = "operational"


@dataclass
class TerminologyEntry:
    """용어 사전 항목"""
    korean: str
    english: str
    category: TermCategory
    abbreviation: Optional[str] = None
    description_ko: Optional[str] = None
    description_en: Optional[str] = None
    related_terms: List[str] = None
    
    def __post_init__(self):
        if self.related_terms is None:
            self.related_terms = []


# AWS 서비스 한영 매핑 (알파벳 순서)
AWS_SERVICES: Dict[str, TerminologyEntry] = {}

# Core Compute Services
AWS_SERVICES["EC2"] = TerminologyEntry(
    korean="일래스틱 컴퓨트 클라우드",
    english="Elastic Compute Cloud",
    category=TermCategory.SERVICE,
    abbreviation="EC2",
    description_ko="가상 서버 인스턴스 제공 서비스",
    description_en="Virtual server instances in the cloud"
)

AWS_SERVICES["Lambda"] = TerminologyEntry(
    korean="람다",
    english="Lambda",
    category=TermCategory.SERVICE,
    description_ko="서버리스 컴퓨팅 서비스",
    description_en="Serverless compute service"
)

AWS_SERVICES["Auto Scaling"] = TerminologyEntry(
    korean="오토 스케일링",
    english="Auto Scaling",
    category=TermCategory.SERVICE,
    description_ko="자동 확장 서비스",
    description_en="Automatic scaling service"
)

AWS_SERVICES["Elastic Beanstalk"] = TerminologyEntry(
    korean="일래스틱 빈스토크",
    english="Elastic Beanstalk",
    category=TermCategory.SERVICE,
    description_ko="애플리케이션 배포 및 관리 서비스",
    description_en="Application deployment and management service"
)

# Storage Services
AWS_SERVICES["S3"] = TerminologyEntry(
    korean="심플 스토리지 서비스",
    english="Simple Storage Service",
    category=TermCategory.SERVICE,
    abbreviation="S3",
    description_ko="객체 스토리지 서비스",
    description_en="Object storage service"
)

AWS_SERVICES["EBS"] = TerminologyEntry(
    korean="일래스틱 블록 스토어",
    english="Elastic Block Store",
    category=TermCategory.SERVICE,
    abbreviation="EBS",
    description_ko="블록 스토리지 서비스",
    description_en="Block storage service"
)

AWS_SERVICES["EFS"] = TerminologyEntry(
    korean="일래스틱 파일 시스템",
    english="Elastic File System",
    category=TermCategory.SERVICE,
    abbreviation="EFS",
    description_ko="관리형 파일 스토리지 서비스",
    description_en="Managed file storage service"
)

AWS_SERVICES["FSx"] = TerminologyEntry(
    korean="FSx 파일 시스템",
    english="FSx",
    category=TermCategory.SERVICE,
    description_ko="완전 관리형 파일 시스템",
    description_en="Fully managed file systems"
)

AWS_SERVICES["Glacier"] = TerminologyEntry(
    korean="글래시어",
    english="Glacier",
    category=TermCategory.SERVICE,
    description_ko="장기 아카이브 스토리지",
    description_en="Long-term archive storage"
)

# Database Services
AWS_SERVICES["RDS"] = TerminologyEntry(
    korean="관계형 데이터베이스 서비스",
    english="Relational Database Service",
    category=TermCategory.SERVICE,
    abbreviation="RDS",
    description_ko="관리형 관계형 데이터베이스",
    description_en="Managed relational database"
)

AWS_SERVICES["DynamoDB"] = TerminologyEntry(
    korean="다이나모DB",
    english="DynamoDB",
    category=TermCategory.SERVICE,
    description_ko="NoSQL 데이터베이스 서비스",
    description_en="NoSQL database service"
)

AWS_SERVICES["Aurora"] = TerminologyEntry(
    korean="오로라",
    english="Aurora",
    category=TermCategory.SERVICE,
    description_ko="고성능 관계형 데이터베이스",
    description_en="High-performance relational database"
)

AWS_SERVICES["ElastiCache"] = TerminologyEntry(
    korean="일래스티캐시",
    english="ElastiCache",
    category=TermCategory.SERVICE,
    description_ko="인메모리 캐싱 서비스",
    description_en="In-memory caching service"
)

AWS_SERVICES["DAX"] = TerminologyEntry(
    korean="다이나모DB 액셀러레이터",
    english="DynamoDB Accelerator",
    category=TermCategory.SERVICE,
    abbreviation="DAX",
    description_ko="DynamoDB용 인메모리 캐시",
    description_en="In-memory cache for DynamoDB"
)

AWS_SERVICES["Redshift"] = TerminologyEntry(
    korean="레드시프트",
    english="Redshift",
    category=TermCategory.SERVICE,
    description_ko="데이터 웨어하우스 서비스",
    description_en="Data warehouse service"
)

# Networking & Content Delivery
AWS_SERVICES["VPC"] = TerminologyEntry(
    korean="가상 프라이빗 클라우드",
    english="Virtual Private Cloud",
    category=TermCategory.SERVICE,
    abbreviation="VPC",
    description_ko="격리된 가상 네트워크",
    description_en="Isolated virtual network"
)

AWS_SERVICES["CloudFront"] = TerminologyEntry(
    korean="클라우드프론트",
    english="CloudFront",
    category=TermCategory.SERVICE,
    description_ko="콘텐츠 전송 네트워크",
    description_en="Content Delivery Network"
)

AWS_SERVICES["Route 53"] = TerminologyEntry(
    korean="라우트 53",
    english="Route 53",
    category=TermCategory.SERVICE,
    description_ko="DNS 웹 서비스",
    description_en="DNS web service"
)

AWS_SERVICES["ELB"] = TerminologyEntry(
    korean="일래스틱 로드 밸런싱",
    english="Elastic Load Balancing",
    category=TermCategory.SERVICE,
    abbreviation="ELB",
    description_ko="부하 분산 서비스",
    description_en="Load balancing service"
)

AWS_SERVICES["ALB"] = TerminologyEntry(
    korean="애플리케이션 로드 밸런서",
    english="Application Load Balancer",
    category=TermCategory.SERVICE,
    abbreviation="ALB",
    description_ko="7계층 로드 밸런서",
    description_en="Layer 7 load balancer"
)

AWS_SERVICES["NLB"] = TerminologyEntry(
    korean="네트워크 로드 밸런서",
    english="Network Load Balancer",
    category=TermCategory.SERVICE,
    abbreviation="NLB",
    description_ko="4계층 로드 밸런서",
    description_en="Layer 4 load balancer"
)

AWS_SERVICES["Direct Connect"] = TerminologyEntry(
    korean="다이렉트 커넥트",
    english="Direct Connect",
    category=TermCategory.SERVICE,
    description_ko="전용 네트워크 연결",
    description_en="Dedicated network connection"
)

AWS_SERVICES["API Gateway"] = TerminologyEntry(
    korean="API 게이트웨이",
    english="API Gateway",
    category=TermCategory.SERVICE,
    description_ko="API 생성 및 관리 서비스",
    description_en="API creation and management service"
)

# Security, Identity & Compliance
AWS_SERVICES["IAM"] = TerminologyEntry(
    korean="아이덴티티 및 액세스 관리",
    english="Identity and Access Management",
    category=TermCategory.SERVICE,
    abbreviation="IAM",
    description_ko="사용자 및 권한 관리 서비스",
    description_en="User and permission management service"
)

AWS_SERVICES["KMS"] = TerminologyEntry(
    korean="키 관리 서비스",
    english="Key Management Service",
    category=TermCategory.SERVICE,
    abbreviation="KMS",
    description_ko="암호화 키 관리 서비스",
    description_en="Encryption key management service"
)

AWS_SERVICES["CloudHSM"] = TerminologyEntry(
    korean="클라우드 HSM",
    english="CloudHSM",
    category=TermCategory.SERVICE,
    description_ko="하드웨어 보안 모듈",
    description_en="Hardware Security Module"
)

AWS_SERVICES["Secrets Manager"] = TerminologyEntry(
    korean="시크릿 매니저",
    english="Secrets Manager",
    category=TermCategory.SERVICE,
    description_ko="비밀 정보 관리 서비스",
    description_en="Secrets management service"
)

AWS_SERVICES["Certificate Manager"] = TerminologyEntry(
    korean="인증서 관리자",
    english="Certificate Manager",
    category=TermCategory.SERVICE,
    abbreviation="ACM",
    description_ko="SSL/TLS 인증서 관리",
    description_en="SSL/TLS certificate management"
)

AWS_SERVICES["GuardDuty"] = TerminologyEntry(
    korean="가드듀티",
    english="GuardDuty",
    category=TermCategory.SERVICE,
    description_ko="위협 탐지 서비스",
    description_en="Threat detection service"
)

AWS_SERVICES["Inspector"] = TerminologyEntry(
    korean="인스펙터",
    english="Inspector",
    category=TermCategory.SERVICE,
    description_ko="보안 취약점 평가 서비스",
    description_en="Security vulnerability assessment service"
)

AWS_SERVICES["Macie"] = TerminologyEntry(
    korean="메이시",
    english="Macie",
    category=TermCategory.SERVICE,
    description_ko="데이터 보안 및 프라이버시 서비스",
    description_en="Data security and privacy service"
)

AWS_SERVICES["WAF"] = TerminologyEntry(
    korean="웹 애플리케이션 방화벽",
    english="Web Application Firewall",
    category=TermCategory.SERVICE,
    abbreviation="WAF",
    description_ko="웹 애플리케이션 보호 서비스",
    description_en="Web application protection service"
)

AWS_SERVICES["Shield"] = TerminologyEntry(
    korean="쉴드",
    english="Shield",
    category=TermCategory.SERVICE,
    description_ko="DDoS 방어 서비스",
    description_en="DDoS protection service"
)

# Management & Governance
AWS_SERVICES["CloudWatch"] = TerminologyEntry(
    korean="클라우드워치",
    english="CloudWatch",
    category=TermCategory.SERVICE,
    description_ko="모니터링 및 관찰 서비스",
    description_en="Monitoring and observability service"
)

AWS_SERVICES["CloudTrail"] = TerminologyEntry(
    korean="클라우드트레일",
    english="CloudTrail",
    category=TermCategory.SERVICE,
    description_ko="API 활동 추적 서비스",
    description_en="API activity tracking service"
)

AWS_SERVICES["Config"] = TerminologyEntry(
    korean="컨피그",
    english="Config",
    category=TermCategory.SERVICE,
    description_ko="리소스 구성 관리 서비스",
    description_en="Resource configuration management service"
)

AWS_SERVICES["Systems Manager"] = TerminologyEntry(
    korean="시스템즈 매니저",
    english="Systems Manager",
    category=TermCategory.SERVICE,
    description_ko="운영 관리 서비스",
    description_en="Operations management service"
)

AWS_SERVICES["CloudFormation"] = TerminologyEntry(
    korean="클라우드포메이션",
    english="CloudFormation",
    category=TermCategory.SERVICE,
    description_ko="인프라 코드화 서비스",
    description_en="Infrastructure as Code service"
)

AWS_SERVICES["Organizations"] = TerminologyEntry(
    korean="오거니제이션즈",
    english="Organizations",
    category=TermCategory.SERVICE,
    description_ko="계정 관리 서비스",
    description_en="Account management service"
)

AWS_SERVICES["Control Tower"] = TerminologyEntry(
    korean="컨트롤 타워",
    english="Control Tower",
    category=TermCategory.SERVICE,
    description_ko="멀티 계정 거버넌스 서비스",
    description_en="Multi-account governance service"
)

AWS_SERVICES["Service Catalog"] = TerminologyEntry(
    korean="서비스 카탈로그",
    english="Service Catalog",
    category=TermCategory.SERVICE,
    description_ko="IT 서비스 관리",
    description_en="IT service management"
)

AWS_SERVICES["Trusted Advisor"] = TerminologyEntry(
    korean="트러스티드 어드바이저",
    english="Trusted Advisor",
    category=TermCategory.SERVICE,
    description_ko="모범 사례 권장 서비스",
    description_en="Best practice recommendation service"
)

# Application Integration
AWS_SERVICES["SQS"] = TerminologyEntry(
    korean="심플 큐 서비스",
    english="Simple Queue Service",
    category=TermCategory.SERVICE,
    abbreviation="SQS",
    description_ko="메시지 큐 서비스",
    description_en="Message queue service"
)

AWS_SERVICES["SNS"] = TerminologyEntry(
    korean="심플 노티피케이션 서비스",
    english="Simple Notification Service",
    category=TermCategory.SERVICE,
    abbreviation="SNS",
    description_ko="알림 서비스",
    description_en="Notification service"
)

AWS_SERVICES["Step Functions"] = TerminologyEntry(
    korean="스텝 펑션즈",
    english="Step Functions",
    category=TermCategory.SERVICE,
    description_ko="워크플로우 오케스트레이션 서비스",
    description_en="Workflow orchestration service"
)

AWS_SERVICES["EventBridge"] = TerminologyEntry(
    korean="이벤트브릿지",
    english="EventBridge",
    category=TermCategory.SERVICE,
    description_ko="이벤트 버스 서비스",
    description_en="Event bus service"
)

AWS_SERVICES["AppSync"] = TerminologyEntry(
    korean="앱싱크",
    english="AppSync",
    category=TermCategory.SERVICE,
    description_ko="GraphQL API 서비스",
    description_en="GraphQL API service"
)

# Analytics
AWS_SERVICES["Athena"] = TerminologyEntry(
    korean="아테나",
    english="Athena",
    category=TermCategory.SERVICE,
    description_ko="서버리스 쿼리 서비스",
    description_en="Serverless query service"
)

AWS_SERVICES["EMR"] = TerminologyEntry(
    korean="일래스틱 맵리듀스",
    english="Elastic MapReduce",
    category=TermCategory.SERVICE,
    abbreviation="EMR",
    description_ko="빅데이터 처리 플랫폼",
    description_en="Big data processing platform"
)

AWS_SERVICES["Kinesis"] = TerminologyEntry(
    korean="키네시스",
    english="Kinesis",
    category=TermCategory.SERVICE,
    description_ko="실시간 데이터 스트리밍",
    description_en="Real-time data streaming"
)

AWS_SERVICES["Glue"] = TerminologyEntry(
    korean="글루",
    english="Glue",
    category=TermCategory.SERVICE,
    description_ko="ETL 서비스",
    description_en="ETL service"
)

AWS_SERVICES["QuickSight"] = TerminologyEntry(
    korean="퀵사이트",
    english="QuickSight",
    category=TermCategory.SERVICE,
    description_ko="비즈니스 인텔리전스 서비스",
    description_en="Business intelligence service"
)

# Developer Tools
AWS_SERVICES["CodeCommit"] = TerminologyEntry(
    korean="코드커밋",
    english="CodeCommit",
    category=TermCategory.SERVICE,
    description_ko="소스 제어 서비스",
    description_en="Source control service"
)

AWS_SERVICES["CodeBuild"] = TerminologyEntry(
    korean="코드빌드",
    english="CodeBuild",
    category=TermCategory.SERVICE,
    description_ko="빌드 서비스",
    description_en="Build service"
)

AWS_SERVICES["CodeDeploy"] = TerminologyEntry(
    korean="코드디플로이",
    english="CodeDeploy",
    category=TermCategory.SERVICE,
    description_ko="배포 자동화 서비스",
    description_en="Deployment automation service"
)

AWS_SERVICES["CodePipeline"] = TerminologyEntry(
    korean="코드파이프라인",
    english="CodePipeline",
    category=TermCategory.SERVICE,
    description_ko="CI/CD 파이프라인 서비스",
    description_en="CI/CD pipeline service"
)

# Container Services
AWS_SERVICES["ECS"] = TerminologyEntry(
    korean="일래스틱 컨테이너 서비스",
    english="Elastic Container Service",
    category=TermCategory.SERVICE,
    abbreviation="ECS",
    description_ko="컨테이너 오케스트레이션 서비스",
    description_en="Container orchestration service"
)

AWS_SERVICES["EKS"] = TerminologyEntry(
    korean="일래스틱 쿠버네티스 서비스",
    english="Elastic Kubernetes Service",
    category=TermCategory.SERVICE,
    abbreviation="EKS",
    description_ko="관리형 쿠버네티스 서비스",
    description_en="Managed Kubernetes service"
)

AWS_SERVICES["ECR"] = TerminologyEntry(
    korean="일래스틱 컨테이너 레지스트리",
    english="Elastic Container Registry",
    category=TermCategory.SERVICE,
    abbreviation="ECR",
    description_ko="컨테이너 이미지 레지스트리",
    description_en="Container image registry"
)

AWS_SERVICES["Fargate"] = TerminologyEntry(
    korean="파게이트",
    english="Fargate",
    category=TermCategory.SERVICE,
    description_ko="서버리스 컨테이너 실행",
    description_en="Serverless container execution"
)

# Technical Terms Dictionary
TECHNICAL_TERMS: Dict[str, TerminologyEntry] = {
    # Infrastructure & Architecture
    "Region": TerminologyEntry(
        korean="리전",
        english="Region",
        category=TermCategory.ARCHITECTURAL,
        description_ko="지리적으로 분리된 AWS 데이터센터 그룹",
        description_en="Geographically separated AWS data center groups"
    ),
    "Availability Zone": TerminologyEntry(
        korean="가용 영역",
        english="Availability Zone",
        category=TermCategory.ARCHITECTURAL,
        abbreviation="AZ",
        description_ko="리전 내 격리된 데이터센터",
        description_en="Isolated data centers within a region"
    ),
    "Edge Location": TerminologyEntry(
        korean="엣지 로케이션",
        english="Edge Location",
        category=TermCategory.ARCHITECTURAL,
        description_ko="콘텐츠 캐싱을 위한 글로벌 거점",
        description_en="Global points of presence for content caching"
    ),
    "VPC": TerminologyEntry(
        korean="가상 프라이빗 클라우드",
        english="Virtual Private Cloud",
        category=TermCategory.ARCHITECTURAL,
        description_ko="격리된 가상 네트워크 환경",
        description_en="Isolated virtual network environment"
    ),
    "Subnet": TerminologyEntry(
        korean="서브넷",
        english="Subnet",
        category=TermCategory.ARCHITECTURAL,
        description_ko="VPC 내 IP 주소 범위",
        description_en="IP address range within VPC"
    ),
    "Internet Gateway": TerminologyEntry(
        korean="인터넷 게이트웨이",
        english="Internet Gateway",
        category=TermCategory.ARCHITECTURAL,
        abbreviation="IGW",
        description_ko="VPC와 인터넷 간 연결",
        description_en="Connection between VPC and internet"
    ),
    "NAT Gateway": TerminologyEntry(
        korean="NAT 게이트웨이",
        english="NAT Gateway",
        category=TermCategory.ARCHITECTURAL,
        description_ko="프라이빗 서브넷의 아웃바운드 인터넷 연결",
        description_en="Outbound internet connection for private subnets"
    ),
    "Route Table": TerminologyEntry(
        korean="라우팅 테이블",
        english="Route Table",
        category=TermCategory.ARCHITECTURAL,
        description_ko="네트워크 트래픽 경로 규칙",
        description_en="Network traffic routing rules"
    ),
    "Security Group": TerminologyEntry(
        korean="보안 그룹",
        english="Security Group",
        category=TermCategory.ARCHITECTURAL,
        description_ko="인스턴스 수준 방화벽",
        description_en="Instance-level firewall"
    ),
    "Network ACL": TerminologyEntry(
        korean="네트워크 ACL",
        english="Network Access Control List",
        category=TermCategory.ARCHITECTURAL,
        abbreviation="NACL",
        description_ko="서브넷 수준 방화벽",
        description_en="Subnet-level firewall"
    ),
    
    # Compute Terms
    "Instance": TerminologyEntry(
        korean="인스턴스",
        english="Instance",
        category=TermCategory.TECHNICAL,
        description_ko="가상 서버",
        description_en="Virtual server"
    ),
    "AMI": TerminologyEntry(
        korean="아마존 머신 이미지",
        english="Amazon Machine Image",
        category=TermCategory.TECHNICAL,
        abbreviation="AMI",
        description_ko="인스턴스 템플릿",
        description_en="Instance template"
    ),
    "Instance Type": TerminologyEntry(
        korean="인스턴스 유형",
        english="Instance Type",
        category=TermCategory.TECHNICAL,
        description_ko="컴퓨팅 리소스 사양",
        description_en="Computing resource specifications"
    ),
    "Elastic IP": TerminologyEntry(
        korean="탄력적 IP",
        english="Elastic IP",
        category=TermCategory.TECHNICAL,
        abbreviation="EIP",
        description_ko="고정 공인 IP 주소",
        description_en="Static public IP address"
    ),
    "Placement Group": TerminologyEntry(
        korean="배치 그룹",
        english="Placement Group",
        category=TermCategory.TECHNICAL,
        description_ko="인스턴스 물리적 배치 전략",
        description_en="Instance physical placement strategy"
    ),
    
    # Storage Terms
    "Bucket": TerminologyEntry(
        korean="버킷",
        english="Bucket",
        category=TermCategory.TECHNICAL,
        description_ko="S3 객체 저장 컨테이너",
        description_en="S3 object storage container"
    ),
    "Object": TerminologyEntry(
        korean="객체",
        english="Object",
        category=TermCategory.TECHNICAL,
        description_ko="S3에 저장된 파일",
        description_en="File stored in S3"
    ),
    "Storage Class": TerminologyEntry(
        korean="스토리지 클래스",
        english="Storage Class",
        category=TermCategory.TECHNICAL,
        description_ko="데이터 저장 계층",
        description_en="Data storage tier"
    ),
    "Lifecycle Policy": TerminologyEntry(
        korean="수명 주기 정책",
        english="Lifecycle Policy",
        category=TermCategory.TECHNICAL,
        description_ko="자동 데이터 관리 규칙",
        description_en="Automatic data management rules"
    ),
    "Versioning": TerminologyEntry(
        korean="버저닝",
        english="Versioning",
        category=TermCategory.TECHNICAL,
        description_ko="객체 버전 관리",
        description_en="Object version management"
    ),
    "Volume": TerminologyEntry(
        korean="볼륨",
        english="Volume",
        category=TermCategory.TECHNICAL,
        description_ko="블록 스토리지 단위",
        description_en="Block storage unit"
    ),
    "Snapshot": TerminologyEntry(
        korean="스냅샷",
        english="Snapshot",
        category=TermCategory.TECHNICAL,
        description_ko="볼륨 백업 이미지",
        description_en="Volume backup image"
    ),
    
    # Database Terms
    "Multi-AZ": TerminologyEntry(
        korean="다중 AZ",
        english="Multi-AZ",
        category=TermCategory.ARCHITECTURAL,
        description_ko="다중 가용 영역 배포",
        description_en="Multi-Availability Zone deployment"
    ),
    "Read Replica": TerminologyEntry(
        korean="읽기 전용 복제본",
        english="Read Replica",
        category=TermCategory.TECHNICAL,
        description_ko="읽기 성능 향상을 위한 복제본",
        description_en="Replica for read performance"
    ),
    "Global Tables": TerminologyEntry(
        korean="글로벌 테이블",
        english="Global Tables",
        category=TermCategory.TECHNICAL,
        description_ko="다중 리전 복제 테이블",
        description_en="Multi-region replicated tables"
    ),
    "Streams": TerminologyEntry(
        korean="스트림",
        english="Streams",
        category=TermCategory.TECHNICAL,
        description_ko="데이터 변경 이벤트 스트림",
        description_en="Data change event stream"
    ),
    
    # Load Balancing Terms
    "Target Group": TerminologyEntry(
        korean="대상 그룹",
        english="Target Group",
        category=TermCategory.TECHNICAL,
        description_ko="로드 밸런서 라우팅 대상",
        description_en="Load balancer routing targets"
    ),
    "Health Check": TerminologyEntry(
        korean="상태 확인",
        english="Health Check",
        category=TermCategory.TECHNICAL,
        description_ko="리소스 상태 모니터링",
        description_en="Resource health monitoring"
    ),
    "Listener": TerminologyEntry(
        korean="리스너",
        english="Listener",
        category=TermCategory.TECHNICAL,
        description_ko="로드 밸런서 연결 수신기",
        description_en="Load balancer connection receiver"
    ),
    
    # Security & Identity Terms
    "User": TerminologyEntry(
        korean="사용자",
        english="User",
        category=TermCategory.TECHNICAL,
        description_ko="IAM 사용자 계정",
        description_en="IAM user account"
    ),
    "Group": TerminologyEntry(
        korean="그룹",
        english="Group",
        category=TermCategory.TECHNICAL,
        description_ko="사용자 모음",
        description_en="Collection of users"
    ),
    "Role": TerminologyEntry(
        korean="역할",
        english="Role",
        category=TermCategory.TECHNICAL,
        description_ko="임시 권한 부여",
        description_en="Temporary permission grant"
    ),
    "Policy": TerminologyEntry(
        korean="정책",
        english="Policy",
        category=TermCategory.TECHNICAL,
        description_ko="권한 정의 문서",
        description_en="Permission definition document"
    ),
    "MFA": TerminologyEntry(
        korean="다중 인증",
        english="Multi-Factor Authentication",
        category=TermCategory.TECHNICAL,
        abbreviation="MFA",
        description_ko="다단계 인증",
        description_en="Multi-step authentication"
    ),
    "Encryption": TerminologyEntry(
        korean="암호화",
        english="Encryption",
        category=TermCategory.TECHNICAL,
        description_ko="데이터 보안 변환",
        description_en="Data security transformation"
    ),
    "Key": TerminologyEntry(
        korean="키",
        english="Key",
        category=TermCategory.TECHNICAL,
        description_ko="암호화 키",
        description_en="Encryption key"
    ),
    
    # Serverless Terms
    "Function": TerminologyEntry(
        korean="함수",
        english="Function",
        category=TermCategory.TECHNICAL,
        description_ko="Lambda 실행 단위",
        description_en="Lambda execution unit"
    ),
    "Layer": TerminologyEntry(
        korean="레이어",
        english="Layer",
        category=TermCategory.TECHNICAL,
        description_ko="공유 코드 패키지",
        description_en="Shared code package"
    ),
    "Event Source": TerminologyEntry(
        korean="이벤트 소스",
        english="Event Source",
        category=TermCategory.TECHNICAL,
        description_ko="Lambda 트리거",
        description_en="Lambda trigger"
    ),
    "Cold Start": TerminologyEntry(
        korean="콜드 스타트",
        english="Cold Start",
        category=TermCategory.TECHNICAL,
        description_ko="초기 실행 지연",
        description_en="Initial execution delay"
    ),
    
    # Messaging Terms
    "Queue": TerminologyEntry(
        korean="큐",
        english="Queue",
        category=TermCategory.TECHNICAL,
        description_ko="메시지 대기열",
        description_en="Message queue"
    ),
    "FIFO Queue": TerminologyEntry(
        korean="FIFO 큐",
        english="FIFO Queue",
        category=TermCategory.TECHNICAL,
        description_ko="순서 보장 큐",
        description_en="Order-guaranteed queue"
    ),
    "Dead Letter Queue": TerminologyEntry(
        korean="배달 못한 편지 큐",
        english="Dead Letter Queue",
        category=TermCategory.TECHNICAL,
        abbreviation="DLQ",
        description_ko="실패 메시지 저장소",
        description_en="Failed message storage"
    ),
    "Topic": TerminologyEntry(
        korean="토픽",
        english="Topic",
        category=TermCategory.TECHNICAL,
        description_ko="SNS 메시지 채널",
        description_en="SNS message channel"
    ),
    "Subscription": TerminologyEntry(
        korean="구독",
        english="Subscription",
        category=TermCategory.TECHNICAL,
        description_ko="알림 수신 등록",
        description_en="Notification receiver registration"
    ),
    
    # Monitoring Terms
    "Metric": TerminologyEntry(
        korean="지표",
        english="Metric",
        category=TermCategory.TECHNICAL,
        description_ko="성능 측정값",
        description_en="Performance measurement"
    ),
    "Alarm": TerminologyEntry(
        korean="경보",
        english="Alarm",
        category=TermCategory.TECHNICAL,
        description_ko="임계값 알림",
        description_en="Threshold notification"
    ),
    "Dashboard": TerminologyEntry(
        korean="대시보드",
        english="Dashboard",
        category=TermCategory.TECHNICAL,
        description_ko="시각화 패널",
        description_en="Visualization panel"
    ),
    "Log Group": TerminologyEntry(
        korean="로그 그룹",
        english="Log Group",
        category=TermCategory.TECHNICAL,
        description_ko="로그 스트림 컨테이너",
        description_en="Log stream container"
    ),
    "Log Stream": TerminologyEntry(
        korean="로그 스트림",
        english="Log Stream",
        category=TermCategory.TECHNICAL,
        description_ko="로그 이벤트 시퀀스",
        description_en="Log event sequence"
    ),
}


# Architectural Concepts
ARCHITECTURAL_CONCEPTS: Dict[str, TerminologyEntry] = {
    "High Availability": TerminologyEntry(
        korean="고가용성",
        english="High Availability",
        category=TermCategory.ARCHITECTURAL,
        abbreviation="HA",
        description_ko="시스템 지속적 운영 능력",
        description_en="System continuous operation capability"
    ),
    "Fault Tolerance": TerminologyEntry(
        korean="장애 허용",
        english="Fault Tolerance",
        category=TermCategory.ARCHITECTURAL,
        description_ko="장애 발생 시 지속 운영",
        description_en="Continuous operation during failures"
    ),
    "Disaster Recovery": TerminologyEntry(
        korean="재해 복구",
        english="Disaster Recovery",
        category=TermCategory.ARCHITECTURAL,
        abbreviation="DR",
        description_ko="재해 시 복구 전략",
        description_en="Recovery strategy for disasters"
    ),
    "Scalability": TerminologyEntry(
        korean="확장성",
        english="Scalability",
        category=TermCategory.ARCHITECTURAL,
        description_ko="부하 증가 대응 능력",
        description_en="Ability to handle increased load"
    ),
    "Elasticity": TerminologyEntry(
        korean="탄력성",
        english="Elasticity",
        category=TermCategory.ARCHITECTURAL,
        description_ko="자동 리소스 조정",
        description_en="Automatic resource adjustment"
    ),
    "Horizontal Scaling": TerminologyEntry(
        korean="수평 확장",
        english="Horizontal Scaling",
        category=TermCategory.ARCHITECTURAL,
        description_ko="인스턴스 수 증가",
        description_en="Increase number of instances"
    ),
    "Vertical Scaling": TerminologyEntry(
        korean="수직 확장",
        english="Vertical Scaling",
        category=TermCategory.ARCHITECTURAL,
        description_ko="인스턴스 크기 증가",
        description_en="Increase instance size"
    ),
    "Loose Coupling": TerminologyEntry(
        korean="느슨한 결합",
        english="Loose Coupling",
        category=TermCategory.ARCHITECTURAL,
        description_ko="독립적 컴포넌트 설계",
        description_en="Independent component design"
    ),
    "Microservices": TerminologyEntry(
        korean="마이크로서비스",
        english="Microservices",
        category=TermCategory.ARCHITECTURAL,
        description_ko="작은 독립 서비스 아키텍처",
        description_en="Small independent service architecture"
    ),
    "Serverless": TerminologyEntry(
        korean="서버리스",
        english="Serverless",
        category=TermCategory.ARCHITECTURAL,
        description_ko="서버 관리 불필요 아키텍처",
        description_en="No server management architecture"
    ),
    "Event-Driven": TerminologyEntry(
        korean="이벤트 기반",
        english="Event-Driven",
        category=TermCategory.ARCHITECTURAL,
        description_ko="이벤트 중심 아키텍처",
        description_en="Event-centric architecture"
    ),
    "Well-Architected Framework": TerminologyEntry(
        korean="Well-Architected 프레임워크",
        english="Well-Architected Framework",
        category=TermCategory.ARCHITECTURAL,
        description_ko="AWS 아키텍처 모범 사례",
        description_en="AWS architecture best practices"
    ),
}


# Operational Terms
OPERATIONAL_TERMS: Dict[str, TerminologyEntry] = {
    "Deployment": TerminologyEntry(
        korean="배포",
        english="Deployment",
        category=TermCategory.OPERATIONAL,
        description_ko="애플리케이션 릴리스",
        description_en="Application release"
    ),
    "Blue-Green Deployment": TerminologyEntry(
        korean="블루-그린 배포",
        english="Blue-Green Deployment",
        category=TermCategory.OPERATIONAL,
        description_ko="무중단 배포 전략",
        description_en="Zero-downtime deployment strategy"
    ),
    "Canary Deployment": TerminologyEntry(
        korean="카나리 배포",
        english="Canary Deployment",
        category=TermCategory.OPERATIONAL,
        description_ko="점진적 배포 전략",
        description_en="Gradual deployment strategy"
    ),
    "Rolling Update": TerminologyEntry(
        korean="롤링 업데이트",
        english="Rolling Update",
        category=TermCategory.OPERATIONAL,
        description_ko="순차적 업데이트",
        description_en="Sequential update"
    ),
    "Rollback": TerminologyEntry(
        korean="롤백",
        english="Rollback",
        category=TermCategory.OPERATIONAL,
        description_ko="이전 버전 복구",
        description_en="Revert to previous version"
    ),
    "Backup": TerminologyEntry(
        korean="백업",
        english="Backup",
        category=TermCategory.OPERATIONAL,
        description_ko="데이터 복사본 생성",
        description_en="Create data copy"
    ),
    "Restore": TerminologyEntry(
        korean="복원",
        english="Restore",
        category=TermCategory.OPERATIONAL,
        description_ko="백업에서 복구",
        description_en="Recover from backup"
    ),
    "Patch": TerminologyEntry(
        korean="패치",
        english="Patch",
        category=TermCategory.OPERATIONAL,
        description_ko="보안 업데이트",
        description_en="Security update"
    ),
    "Maintenance Window": TerminologyEntry(
        korean="유지보수 기간",
        english="Maintenance Window",
        category=TermCategory.OPERATIONAL,
        description_ko="정기 점검 시간",
        description_en="Scheduled maintenance time"
    ),
    "Throttling": TerminologyEntry(
        korean="스로틀링",
        english="Throttling",
        category=TermCategory.OPERATIONAL,
        description_ko="요청 제한",
        description_en="Request limiting"
    ),
    "Rate Limiting": TerminologyEntry(
        korean="속도 제한",
        english="Rate Limiting",
        category=TermCategory.OPERATIONAL,
        description_ko="요청 빈도 제한",
        description_en="Request frequency limiting"
    ),
    "Caching": TerminologyEntry(
        korean="캐싱",
        english="Caching",
        category=TermCategory.OPERATIONAL,
        description_ko="데이터 임시 저장",
        description_en="Temporary data storage"
    ),
    "TTL": TerminologyEntry(
        korean="생존 시간",
        english="Time To Live",
        category=TermCategory.OPERATIONAL,
        abbreviation="TTL",
        description_ko="데이터 유효 기간",
        description_en="Data validity period"
    ),
}


# Helper Functions
def get_korean_term(english_term: str) -> Optional[str]:
    """영어 용어의 한국어 번역 반환"""
    # AWS Services 검색
    if english_term in AWS_SERVICES:
        return AWS_SERVICES[english_term].korean
    
    # Technical Terms 검색
    if english_term in TECHNICAL_TERMS:
        return TECHNICAL_TERMS[english_term].korean
    
    # Architectural Concepts 검색
    if english_term in ARCHITECTURAL_CONCEPTS:
        return ARCHITECTURAL_CONCEPTS[english_term].korean
    
    # Operational Terms 검색
    if english_term in OPERATIONAL_TERMS:
        return OPERATIONAL_TERMS[english_term].korean
    
    return None


def get_english_term(korean_term: str) -> Optional[str]:
    """한국어 용어의 영어 번역 반환"""
    # 모든 딕셔너리 검색
    all_terms = {
        **AWS_SERVICES,
        **TECHNICAL_TERMS,
        **ARCHITECTURAL_CONCEPTS,
        **OPERATIONAL_TERMS
    }
    
    for key, entry in all_terms.items():
        if entry.korean == korean_term:
            return entry.english
    
    return None


def get_term_entry(term: str) -> Optional[TerminologyEntry]:
    """용어 항목 전체 정보 반환 (한글 또는 영어)"""
    # 영어로 검색
    all_terms = {
        **AWS_SERVICES,
        **TECHNICAL_TERMS,
        **ARCHITECTURAL_CONCEPTS,
        **OPERATIONAL_TERMS
    }
    
    if term in all_terms:
        return all_terms[term]
    
    # 한글로 검색
    for entry in all_terms.values():
        if entry.korean == term:
            return entry
    
    return None


def get_terms_by_category(category: TermCategory) -> Dict[str, TerminologyEntry]:
    """카테고리별 용어 필터링"""
    all_terms = {
        **AWS_SERVICES,
        **TECHNICAL_TERMS,
        **ARCHITECTURAL_CONCEPTS,
        **OPERATIONAL_TERMS
    }
    
    return {
        key: entry for key, entry in all_terms.items()
        if entry.category == category
    }


def search_terms(keyword: str) -> List[TerminologyEntry]:
    """키워드로 용어 검색 (한글/영어 모두)"""
    all_terms = {
        **AWS_SERVICES,
        **TECHNICAL_TERMS,
        **ARCHITECTURAL_CONCEPTS,
        **OPERATIONAL_TERMS
    }
    
    keyword_lower = keyword.lower()
    results = []
    
    for entry in all_terms.values():
        if (keyword_lower in entry.korean.lower() or
            keyword_lower in entry.english.lower() or
            (entry.abbreviation and keyword_lower in entry.abbreviation.lower())):
            results.append(entry)
    
    return results


def get_all_aws_services() -> Dict[str, TerminologyEntry]:
    """모든 AWS 서비스 용어 반환"""
    return AWS_SERVICES.copy()


def get_service_count() -> int:
    """등록된 AWS 서비스 수 반환"""
    return len(AWS_SERVICES)


def get_total_term_count() -> int:
    """전체 용어 수 반환"""
    return (len(AWS_SERVICES) + 
            len(TECHNICAL_TERMS) + 
            len(ARCHITECTURAL_CONCEPTS) + 
            len(OPERATIONAL_TERMS))


def validate_terminology_consistency() -> Dict[str, List[str]]:
    """용어 일관성 검증"""
    issues = {
        "duplicates": [],
        "missing_descriptions": [],
        "missing_categories": []
    }
    
    all_terms = {
        **AWS_SERVICES,
        **TECHNICAL_TERMS,
        **ARCHITECTURAL_CONCEPTS,
        **OPERATIONAL_TERMS
    }
    
    korean_terms = {}
    for key, entry in all_terms.items():
        # 중복 한글 용어 체크
        if entry.korean in korean_terms:
            issues["duplicates"].append(
                f"Duplicate Korean term: {entry.korean} ({key} and {korean_terms[entry.korean]})"
            )
        else:
            korean_terms[entry.korean] = key
        
        # 설명 누락 체크
        if not entry.description_ko or not entry.description_en:
            issues["missing_descriptions"].append(key)
        
        # 카테고리 누락 체크
        if not entry.category:
            issues["missing_categories"].append(key)
    
    return issues
