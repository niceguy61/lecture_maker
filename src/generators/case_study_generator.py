# Case Study Generator
"""
사례 연구 콘텐츠 생성기
각 일별(Day 1-28) case-study.md 파일을 템플릿 기반으로 생성
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from src.daily_topics import DAILY_TOPICS, get_topic_by_day, get_related_topics
from src.models import (
    CaseStudyContent, CompanyInfo, BusinessContext, BusinessRequirement,
    AWSServiceUsage, ArchitectureDetails, ImplementationStep, ImplementationDetails,
    BusinessImpactMetrics, ServiceIntegration, CrossDayConnection, CompanySize
)
from src.config import (
    TEMPLATES_ROOT, STUDY_MATERIALS_ROOT, AWS_DOCS_BASE_URL,
    AWS_PRICING_BASE_URL, AWS_ARCHITECTURE_CENTER_URL
)
class CaseStudyGenerator:
    """사례 연구 생성기"""
    
    def __init__(self):
        self.template_path = TEMPLATES_ROOT / "case-study-template.md"
        self.output_base_path = STUDY_MATERIALS_ROOT
        
    def load_template(self) -> str:
        """템플릿 파일 로드"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_daily_config(self, day_number: int) -> Dict:
        """일별 주제 설정 가져오기"""
        return get_topic_by_day(day_number)
    
    def generate_company_info(self, day_number: int) -> CompanyInfo:
        """기업 정보 생성"""
        config = self.get_daily_config(day_number)
        company_name = config["case_study_company"]
        
        # 실제 기업 여부 판단 (간단한 휴리스틱)
        is_real = company_name not in ["AWS Certified Solutions Architect", "Startup Best Practices"]
        
        # 업종 매핑
        industry_map = {
            "Netflix": "미디어 & 엔터테인먼트",
            "Airbnb": "여행 & 숙박",
            "Spotify": "음악 스트리밍",
            "Uber": "모빌리티",
            "Slack": "엔터프라이즈 소프트웨어",
            "Capital One": "금융 서비스",
            "Lyft": "모빌리티",
            "Dropbox": "클라우드 스토리지",
            "Adobe": "소프트웨어 & 크리에이티브",
            "Expedia": "여행 & 예약",
            "Duolingo": "교육 기술",
            "Tinder": "소셜 네트워킹",
            "Pinterest": "소셜 미디어",
            "Zillow": "부동산 기술",
            "Robinhood": "핀테크",
            "Twitch": "라이브 스트리밍",
            "Coursera": "온라인 교육",
            "Coca-Cola": "제조 & 유통",
            "Stripe": "결제 플랫폼",
            "Instacart": "식료품 배달",
            "DoorDash": "음식 배달",
            "Datadog": "모니터링 & 관측성",
            "Goldman Sachs": "금융 서비스",
            "GE Healthcare": "의료 기기",
            "Coinbase": "암호화폐 거래소",
            "Samsung Electronics": "전자 제조",
        }
        
        # 기업 규모 매핑
        size_map = {
            "Netflix": CompanySize.ENTERPRISE,
            "Airbnb": CompanySize.ENTERPRISE,
            "Spotify": CompanySize.ENTERPRISE,
            "Uber": CompanySize.ENTERPRISE,
            "Slack": CompanySize.MEDIUM,
            "Capital One": CompanySize.ENTERPRISE,
            "Lyft": CompanySize.ENTERPRISE,
            "Dropbox": CompanySize.ENTERPRISE,
            "Adobe": CompanySize.ENTERPRISE,
            "Expedia": CompanySize.ENTERPRISE,
            "Duolingo": CompanySize.MEDIUM,
            "Tinder": CompanySize.MEDIUM,
            "Pinterest": CompanySize.ENTERPRISE,
            "Zillow": CompanySize.ENTERPRISE,
            "Robinhood": CompanySize.MEDIUM,
            "Twitch": CompanySize.ENTERPRISE,
            "Coursera": CompanySize.MEDIUM,
            "Coca-Cola": CompanySize.ENTERPRISE,
            "Stripe": CompanySize.ENTERPRISE,
            "Instacart": CompanySize.ENTERPRISE,
            "DoorDash": CompanySize.ENTERPRISE,
            "Datadog": CompanySize.ENTERPRISE,
            "Goldman Sachs": CompanySize.ENTERPRISE,
            "GE Healthcare": CompanySize.ENTERPRISE,
            "Coinbase": CompanySize.ENTERPRISE,
            "Samsung Electronics": CompanySize.ENTERPRISE,
        }
        
        return CompanyInfo(
            name=company_name,
            industry=industry_map.get(company_name, "기술"),
            size=size_map.get(company_name, CompanySize.MEDIUM),
            region="글로벌" if is_real else "가상",
            is_real_company=is_real,
            public_references=[] if not is_real else [
                f"{AWS_ARCHITECTURE_CENTER_URL}/customers/{company_name.lower().replace(' ', '-')}"
            ]
        )
    
    def generate_business_context(self, day_number: int) -> BusinessContext:
        """비즈니스 컨텍스트 생성"""
        config = self.get_daily_config(day_number)
        focus = config["case_study_focus"]
        
        # 기본 비즈니스 요구사항 생성
        requirements = [
            BusinessRequirement(
                category="performance",
                description="높은 처리량과 낮은 지연시간 요구",
                metric="응답시간 < 100ms",
                priority="high"
            ),
            BusinessRequirement(
                category="scalability",
                description="트래픽 급증에 대한 자동 확장",
                metric="동시 사용자 100만명 지원",
                priority="high"
            ),
            BusinessRequirement(
                category="security",
                description="데이터 보안 및 규정 준수",
                priority="high"
            ),
            BusinessRequirement(
                category="cost",
                description="비용 효율적인 인프라 운영",
                priority="medium"
            )
        ]
        
        return BusinessContext(
            challenge=f"{focus}를 위한 확장 가능하고 안정적인 인프라 구축",
            requirements=requirements,
            constraints=[
                "제한된 예산 내에서 최대 성능 달성",
                "기존 시스템과의 호환성 유지",
                "빠른 시장 출시 요구"
            ],
            success_criteria=[
                "99.99% 가용성 달성",
                "응답 시간 100ms 이하 유지",
                "월간 인프라 비용 30% 절감"
            ],
            timeline="3-6개월"
        )

    
    def generate_architecture_section(self, day_number: int) -> ArchitectureDetails:
        """아키텍처 섹션 생성"""
        config = self.get_daily_config(day_number)
        services = config["primary_services"]
        
        # 아키텍처 다이어그램 경로
        diagram_path = f"./architecture-diagrams/day{day_number}-main-architecture.mmd"
        
        return ArchitectureDetails(
            diagram_path=diagram_path,
            description=f"{', '.join(services[:2])} 등을 활용한 {config['case_study_focus']}",
            components=services,
            data_flow=[
                "사용자 요청 수신",
                f"{services[0]} 처리",
                "데이터 저장 및 응답 반환"
            ],
            security_boundaries=[
                "VPC 네트워크 격리",
                "IAM 역할 기반 접근 제어",
                "데이터 암호화 (전송 중/저장 시)"
            ]
        )
    
    def generate_implementation_details(self, day_number: int) -> ImplementationDetails:
        """구현 세부사항 생성"""
        config = self.get_daily_config(day_number)
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # Day 1 (CloudFront) 특별 처리
        if day_number == 1 and primary_service == "CloudFront":
            steps = [
                ImplementationStep(
                    step_number=1,
                    title="CloudFront Distribution 생성",
                    description="AWS Console을 통해 CloudFront Distribution을 생성하고 Origin을 설정합니다.",
                    console_path="Services > Networking & Content Delivery > CloudFront > Create Distribution",
                    configuration={
                        "Origin Domain": "example-bucket.s3.amazonaws.com 또는 ALB DNS",
                        "Origin Protocol Policy": "HTTPS Only",
                        "Viewer Protocol Policy": "Redirect HTTP to HTTPS",
                        "Cache Policy": "CachingOptimized",
                        "Price Class": "Use All Edge Locations (Best Performance)",
                    },
                    verification=[
                        "Distribution 상태가 'Deployed'로 표시되는지 확인 (약 15-20분 소요)",
                        "Distribution Domain Name (예: d111111abcdef8.cloudfront.net) 확인",
                        "테스트 요청으로 콘텐츠가 정상적으로 제공되는지 검증"
                    ],
                    estimated_time="20-30분"
                ),
                ImplementationStep(
                    step_number=2,
                    title="Cache Behavior 및 최적화 설정",
                    description="캐싱 동작을 구성하고 성능을 최적화합니다.",
                    console_path="CloudFront > Distributions > [Distribution ID] > Behaviors",
                    configuration={
                        "Path Pattern": "기본값 (*) 또는 특정 경로 (예: /images/*)",
                        "Compress Objects Automatically": "Yes (Gzip 압축 활성화)",
                        "TTL Settings": "Min: 0, Max: 31536000, Default: 86400",
                        "Query String Forwarding": "필요에 따라 설정",
                    },
                    verification=[
                        "Cache Hit Ratio가 정상적으로 증가하는지 CloudWatch에서 확인",
                        "압축이 적용되는지 응답 헤더 확인 (Content-Encoding: gzip)"
                    ],
                    estimated_time="10-15분"
                ),
                ImplementationStep(
                    step_number=3,
                    title="모니터링 및 알람 설정",
                    description="CloudWatch를 통해 CloudFront 메트릭을 모니터링하고 알람을 설정합니다.",
                    console_path="CloudWatch > Alarms > Create alarm",
                    configuration={
                        "Metric": "CloudFront > Per-Distribution Metrics > 4xxErrorRate",
                        "Threshold": "> 5% for 2 consecutive periods",
                        "Action": "SNS 토픽으로 알림 전송",
                        "Additional Metrics": "Requests, BytesDownloaded, BytesUploaded",
                    },
                    verification=[
                        "CloudWatch 대시보드에서 메트릭이 정상적으로 수집되는지 확인",
                        "테스트 알람이 올바르게 트리거되는지 검증"
                    ],
                    estimated_time="10-15분"
                )
            ]
        else:
            # 기존 일반 서비스 구현 단계
            steps = [
                ImplementationStep(
                    step_number=1,
                    title=f"{primary_service} 생성 및 구성",
                    description=f"AWS Console을 통해 {primary_service} 리소스를 생성하고 기본 설정을 구성합니다.",
                    console_path=f"Services > [Category] > {primary_service}",
                    configuration={
                        "Region": "ap-northeast-2 (서울)",
                        "Name": f"day{day_number}-{primary_service.lower().replace(' ', '-')}",
                    },
                    verification=[
                        "리소스 상태가 'Available' 또는 'Active'로 표시되는지 확인",
                        "기본 설정이 올바르게 적용되었는지 검증"
                    ],
                    estimated_time="10-15분"
                ),
                ImplementationStep(
                    step_number=2,
                    title="보안 및 접근 제어 설정",
                    description="IAM 역할 및 보안 그룹을 구성하여 안전한 접근을 보장합니다.",
                    console_path="IAM > Roles > Create role",
                    configuration={
                        "Trust Policy": "서비스 신뢰 관계 설정",
                        "Permissions": "최소 권한 원칙 적용",
                    },
                    verification=[
                        "IAM 역할이 올바르게 생성되었는지 확인",
                        "보안 그룹 규칙이 적절히 설정되었는지 검증"
                    ],
                    estimated_time="5-10분"
                ),
                ImplementationStep(
                    step_number=3,
                    title="모니터링 및 알람 설정",
                    description="CloudWatch를 통해 핵심 메트릭을 모니터링하고 알람을 설정합니다.",
                    console_path="CloudWatch > Alarms > Create alarm",
                    configuration={
                        "Metric": "주요 성능 지표",
                        "Threshold": "임계값 설정",
                        "Action": "SNS 알림 구성",
                    },
                    verification=[
                        "알람이 정상적으로 생성되었는지 확인",
                        "테스트 알림이 올바르게 전송되는지 검증"
                    ],
                    estimated_time="5-10분"
                )
            ]
        
        return ImplementationDetails(
            steps=steps,
            configuration_files=[
                "cloudformation-template.yaml (선택사항)",
                "terraform-main.tf (선택사항)"
            ],
            code_snippets=[
                "AWS CLI 명령어 예시",
                "SDK 코드 예시 (Python/Node.js)"
            ],
            monitoring_setup="CloudWatch 대시보드 및 알람 구성"
        )
    
    def generate_business_impact(self, day_number: int) -> BusinessImpactMetrics:
        """비즈니스 임팩트 생성"""
        return BusinessImpactMetrics(
            performance_improvements={
                "응답 시간": "200ms → 50ms (75% 개선)",
                "처리량": "1,000 TPS → 10,000 TPS (10배 증가)",
                "가용성": "99.9% → 99.99% (0.09% 향상)"
            },
            cost_savings={
                "월간 인프라 비용": "$10,000 → $7,000 (30% 절감)",
                "운영 인력 비용": "5명 → 3명 (40% 절감)",
                "총 소유 비용": "연간 $50,000 절감"
            },
            operational_efficiency={
                "배포 시간": "2시간 → 15분 (87.5% 단축)",
                "장애 복구 시간": "30분 → 5분 (83% 개선)",
                "자동화율": "30% → 90% (3배 증가)"
            },
            user_experience_improvements=[
                "페이지 로딩 속도 2배 향상",
                "서비스 중단 시간 90% 감소",
                "사용자 만족도 25% 증가"
            ]
        )
    
    def generate_service_integrations(self, day_number: int) -> List[ServiceIntegration]:
        """서비스 통합 정보 생성"""
        config = self.get_daily_config(day_number)
        related_topics = get_related_topics(day_number)
        integrations = []
        
        if config["primary_services"]:
            primary = config["primary_services"][0]
            
            # 관련 일차의 서비스와 통합
            for related_day, related_config in list(related_topics.items())[:2]:
                if related_config["primary_services"]:
                    related_service = related_config["primary_services"][0]
                    integrations.append(
                        ServiceIntegration(
                            primary_service=primary,
                            integrated_service=related_service,
                            integration_pattern="Direct Integration",
                            data_flow=f"{primary} → {related_service}",
                            benefits=[
                                "향상된 성능 및 확장성",
                                "통합된 모니터링 및 관리",
                                "비용 최적화"
                            ]
                        )
                    )
        
        return integrations
    
    def generate_cross_day_connections(self, day_number: int) -> List[CrossDayConnection]:
        """크로스 데이 연결 생성"""
        config = self.get_daily_config(day_number)
        related_days = config.get("related_days", [])
        connections = []
        
        for related_day in related_days[:3]:  # 최대 3개
            try:
                related_config = get_topic_by_day(related_day)
                connection_type = "prerequisite" if related_day < day_number else "enhancement"
                
                connections.append(
                    CrossDayConnection(
                        day_number=related_day,
                        service_name=related_config["primary_services"][0] if related_config["primary_services"] else "AWS Service",
                        connection_type=connection_type,
                        description=f"Day {related_day}의 {related_config['title']}와 연계"
                    )
                )
            except (ValueError, KeyError):
                continue
        
        return connections
    
    def generate_mermaid_diagrams(self, day_number: int) -> Dict[str, str]:
        """Mermaid 다이어그램 생성"""
        config = self.get_daily_config(day_number)
        services = config["primary_services"]
        
        # 기본 아키텍처 다이어그램
        architecture_diagram = f"""graph TB
    subgraph "사용자 계층"
        Users[사용자/애플리케이션]
    end
    
    subgraph "AWS 인프라 - Day {day_number}"
        A[{services[0] if services else 'AWS Service'}]
"""
        
        if len(services) > 1:
            for i, service in enumerate(services[1:3], start=1):
                architecture_diagram += f"        B{i}[{service}]\n"
        
        architecture_diagram += "    end\n\n"
        architecture_diagram += "    Users --> A\n"
        
        if len(services) > 1:
            for i in range(1, min(3, len(services))):
                architecture_diagram += f"    A --> B{i}\n"
        
        # 데이터 플로우 다이어그램
        data_flow_diagram = f"""sequenceDiagram
    participant User as 사용자
    participant Service as {services[0] if services else 'AWS Service'}
    participant Storage as 데이터 저장소
    
    User->>Service: 요청 전송
    Service->>Storage: 데이터 조회/저장
    Storage-->>Service: 응답
    Service-->>User: 결과 반환
"""
        
        # 크로스 데이 통합 다이어그램
        related_days = config.get("related_days", [])[:3]
        cross_day_diagram = f"""graph LR
    D{day_number}[Day {day_number}:<br/>{config['title']}]
"""
        
        for i, related_day in enumerate(related_days):
            try:
                related_config = get_topic_by_day(related_day)
                cross_day_diagram += f"    D{related_day}[Day {related_day}:<br/>{related_config['title']}]\n"
            except ValueError:
                continue
        
        cross_day_diagram += "\n"
        for related_day in related_days:
            if related_day < day_number:
                cross_day_diagram += f"    D{related_day} --> D{day_number}\n"
            else:
                cross_day_diagram += f"    D{day_number} -.확장.-> D{related_day}\n"
        
        return {
            "architecture": architecture_diagram,
            "data_flow": data_flow_diagram,
            "cross_day_integration": cross_day_diagram
        }
    
    def _get_service_role_description(self, service_name: str) -> str:
        """서비스별 역할 설명 생성"""
        role_map = {
            # 글로벌 인프라 (Day 1 - 개념 및 설계)
            "Regions": "지리적으로 분리된 AWS 데이터센터 위치 - 지연시간 최소화, 규정 준수, 재해 복구를 위한 리전 선택",
            "Availability Zones": "리전 내 물리적으로 분리된 데이터센터 - 단일 장애점 제거 및 고가용성 보장",
            "Edge Locations": "CloudFront CDN의 전 세계 캐시 서버 - 사용자와 가까운 위치에서 콘텐츠 제공",
            "CloudFront": "글로벌 콘텐츠 전송 네트워크(CDN) - 정적/동적 콘텐츠를 엣지 로케이션에서 캐싱 및 배포",
            
            # IAM
            "IAM Users": "사용자 계정 및 인증 관리",
            "Groups": "사용자 그룹 기반 권한 관리",
            "Roles": "서비스 간 권한 위임 및 임시 자격 증명",
            "Policies": "세밀한 권한 정책 정의",
            "MFA": "다중 인증을 통한 보안 강화",
            
            # EC2 기초
            "EC2 Instances": "가상 서버 인스턴스 제공",
            "Instance Types": "워크로드에 최적화된 인스턴스 타입 선택",
            "AMI": "사전 구성된 이미지를 통한 빠른 배포",
            "Security Groups": "인스턴스 수준 방화벽 및 네트워크 보안",
            
            # EC2 고급
            "Auto Scaling": "트래픽에 따른 자동 확장 및 축소",
            "Load Balancing": "트래픽 분산 및 고가용성 보장",
            "Placement Groups": "인스턴스 배치 최적화",
            "Elastic IP": "고정 공인 IP 주소 할당",
            
            # VPC 기초
            "VPC": "격리된 가상 네트워크 환경 제공",
            "Subnets": "네트워크 세그먼테이션 및 리소스 격리",
            "Route Tables": "네트워크 트래픽 라우팅 제어",
            "Internet Gateway": "VPC와 인터넷 간 연결",
            
            # VPC 고급
            "NAT Gateway": "프라이빗 서브넷의 아웃바운드 인터넷 액세스",
            "VPC Peering": "VPC 간 프라이빗 네트워크 연결",
            "VPN": "온프레미스와 AWS 간 암호화된 연결",
            "Direct Connect": "전용 네트워크 연결을 통한 안정적인 통신",
            
            # 스토리지
            "S3": "객체 스토리지 및 정적 콘텐츠 호스팅",
            "S3 Buckets": "데이터 저장을 위한 버킷 생성 및 관리",
            "Storage Classes": "비용 최적화를 위한 스토리지 클래스 선택",
            "Lifecycle Policies": "자동 데이터 수명 주기 관리",
            "Versioning": "객체 버전 관리 및 데이터 보호",
            "EBS": "블록 스토리지 제공 및 데이터 영속성 보장",
            "EBS Volumes": "EC2 인스턴스용 블록 스토리지 볼륨",
            "EBS Snapshots": "볼륨 백업 및 복구",
            "EFS": "공유 파일 시스템 제공",
            "FSx": "완전 관리형 파일 시스템",
            "Glacier": "장기 아카이브 스토리지",
            
            # 데이터베이스
            "RDS": "관계형 데이터베이스 관리",
            "Multi-AZ": "고가용성을 위한 다중 AZ 배포",
            "Read Replicas": "읽기 성능 향상을 위한 복제본",
            "Aurora": "고성능 관계형 데이터베이스",
            "DynamoDB": "NoSQL 데이터베이스 및 고성능 키-값 저장소",
            "DAX": "DynamoDB 가속기를 통한 마이크로초 지연 시간",
            "Global Tables": "글로벌 다중 리전 복제",
            "Streams": "실시간 데이터 스트림 처리",
            "ElastiCache": "인메모리 캐싱 및 성능 최적화",
            "Redis": "인메모리 데이터 구조 저장소",
            "Memcached": "분산 메모리 캐싱 시스템",
            
            # 컴퓨팅
            "Lambda": "서버리스 함수 실행",
            "Lambda Layers": "공통 코드 및 라이브러리 공유",
            "Lambda@Edge": "엣지 로케이션에서 함수 실행",
            "Event Sources": "다양한 이벤트 소스와의 통합",
            
            # 로드 밸런싱
            "ELB": "로드 밸런싱 및 트래픽 분산",
            "ALB": "애플리케이션 계층 로드 밸런싱 (HTTP/HTTPS)",
            "NLB": "네트워크 계층 로드 밸런싱 (TCP/UDP)",
            "CLB": "클래식 로드 밸런서",
            "Target Groups": "로드 밸런서 대상 그룹 관리",
            
            # 메시징 및 통합
            "SQS": "메시지 큐잉 및 비동기 처리",
            "Standard Queue": "표준 메시지 큐",
            "FIFO Queue": "순서 보장 메시지 큐",
            "Dead Letter Queue": "실패한 메시지 처리",
            "SNS": "푸시 알림 및 메시지 발행",
            "EventBridge": "이벤트 기반 통합 및 라우팅",
            "Event Bus": "이벤트 버스를 통한 이벤트 전달",
            "Step Functions": "워크플로우 오케스트레이션",
            "State Machines": "상태 머신 기반 워크플로우 정의",
            
            # DNS 및 CDN
            "Route 53": "DNS 라우팅 및 도메인 관리",
            "DNS": "도메인 네임 시스템 관리",
            "Health Checks": "엔드포인트 상태 모니터링",
            "Routing Policies": "트래픽 라우팅 정책 설정",
            
            # API
            "API Gateway": "API 관리 및 엔드포인트 제공",
            "REST API": "RESTful API 생성 및 관리",
            "WebSocket API": "실시간 양방향 통신 API",
            "API Keys": "API 액세스 키 관리",
            "AppSync": "GraphQL API 제공",
            
            # 모니터링 및 보안
            "CloudWatch": "모니터링 및 알람 기능 제공",
            "Metrics": "시스템 메트릭 수집 및 분석",
            "Logs": "로그 수집 및 분석",
            "Alarms": "임계값 기반 알람 설정",
            "Dashboards": "시각화 대시보드 생성",
            "CloudTrail": "API 호출 감사 및 로깅",
            "GuardDuty": "위협 탐지 및 보안 모니터링",
            "Inspector": "보안 취약점 평가",
            "Macie": "민감한 데이터 검색 및 보호",
            "IAM": "인증 및 권한 관리",
            "KMS": "암호화 키 관리",
            "CloudHSM": "하드웨어 보안 모듈",
            "Secrets Manager": "비밀 정보 안전 저장 및 자동 교체",
            "Certificate Manager": "SSL/TLS 인증서 관리",
            
            # 관리 및 거버넌스
            "Config": "리소스 구성 추적 및 규정 준수",
            "Systems Manager": "운영 작업 자동화",
            "Parameter Store": "구성 데이터 및 비밀 정보 저장",
            "Patch Manager": "패치 관리 자동화",
            "Organizations": "다중 계정 중앙 관리",
            "Control Tower": "멀티 계정 거버넌스 자동화",
            "Service Catalog": "승인된 IT 서비스 카탈로그",
            "Well-Architected": "아키텍처 모범 사례 검토",
        }
        
        return role_map.get(service_name, f"{service_name} 서비스 통합 및 기능 제공")
    
    def _get_config_summary(self, service_name: str) -> str:
        """서비스별 구성 요약 생성"""
        config_map = {
            # 글로벌 인프라 (Day 1 - 선택/설계 관점)
            "Regions": "비즈니스 요구사항(지연시간, 규정 준수, 비용)에 따라 최적의 리전 선택",
            "Availability Zones": "고가용성 확보를 위해 최소 2개 이상의 AZ에 리소스 분산 배치",
            "Edge Locations": "CloudFront 배포 시 자동으로 전 세계 엣지 로케이션 활용",
            "CloudFront": "배포 생성, 오리진 설정, 캐싱 동작 구성",
            
            # IAM
            "IAM Users": "사용자 생성 및 액세스 키 발급",
            "Groups": "그룹 생성 및 사용자 할당",
            "Roles": "역할 생성 및 신뢰 정책 설정",
            "Policies": "정책 문서 작성 및 권한 부여",
            "MFA": "MFA 디바이스 등록 및 활성화",
            
            # EC2
            "EC2 Instances": "인스턴스 타입 선택 및 시작",
            "Instance Types": "워크로드에 맞는 인스턴스 타입 선택",
            "AMI": "AMI 선택 또는 커스텀 AMI 생성",
            "Security Groups": "인바운드/아웃바운드 규칙 설정",
            "Auto Scaling": "Auto Scaling 그룹 및 정책 구성",
            "Load Balancing": "로드 밸런서 생성 및 대상 그룹 구성",
            "Placement Groups": "배치 그룹 전략 선택 (Cluster/Spread/Partition)",
            "Elastic IP": "탄력적 IP 할당 및 인스턴스 연결",
            
            # VPC
            "VPC": "CIDR 블록 설정 및 VPC 생성",
            "Subnets": "퍼블릭/프라이빗 서브넷 생성 및 CIDR 할당",
            "Route Tables": "라우팅 테이블 생성 및 라우트 규칙 설정",
            "Internet Gateway": "IGW 생성 및 VPC 연결",
            "NAT Gateway": "NAT Gateway 생성 및 프라이빗 서브넷 라우팅",
            "VPC Peering": "피어링 연결 생성 및 라우팅 설정",
            "VPN": "VPN 게이트웨이 및 고객 게이트웨이 구성",
            "Direct Connect": "전용 연결 설정 및 가상 인터페이스 구성",
            
            # 스토리지
            "S3": "버킷 생성 및 스토리지 클래스 설정",
            "S3 Buckets": "버킷 생성, 버전 관리 및 암호화 설정",
            "Storage Classes": "Standard, IA, Glacier 등 스토리지 클래스 선택",
            "Lifecycle Policies": "수명 주기 규칙 생성 및 전환 정책 설정",
            "Versioning": "버전 관리 활성화 및 MFA Delete 설정",
            "EBS": "볼륨 타입 및 크기 설정",
            "EBS Volumes": "볼륨 생성 및 인스턴스 연결",
            "EBS Snapshots": "스냅샷 생성 및 백업 스케줄 설정",
            "EFS": "파일 시스템 생성 및 마운트 타겟 구성",
            "FSx": "파일 시스템 타입 선택 및 구성",
            
            # 데이터베이스
            "RDS": "데이터베이스 엔진 및 인스턴스 타입 선택",
            "Multi-AZ": "다중 AZ 배포 활성화",
            "Read Replicas": "읽기 전용 복제본 생성 및 구성",
            "Aurora": "Aurora 클러스터 생성 및 엔드포인트 구성",
            "DynamoDB": "테이블 생성 및 읽기/쓰기 용량 설정",
            "DAX": "DAX 클러스터 생성 및 DynamoDB 연결",
            "Global Tables": "글로벌 테이블 생성 및 리전 추가",
            "Streams": "DynamoDB Streams 활성화 및 Lambda 트리거 설정",
            "ElastiCache": "클러스터 생성 및 노드 타입 선택",
            "Redis": "Redis 클러스터 모드 및 복제 구성",
            "Memcached": "Memcached 노드 구성 및 Auto Discovery 설정",
            
            # 컴퓨팅
            "Lambda": "함수 코드 업로드 및 트리거 구성",
            "Lambda Layers": "레이어 생성 및 함수에 연결",
            "Lambda@Edge": "CloudFront 트리거 설정",
            "Event Sources": "이벤트 소스 매핑 구성",
            
            # 로드 밸런싱
            "ELB": "로드 밸런서 생성 및 대상 그룹 구성",
            "ALB": "리스너 규칙 및 대상 그룹 설정",
            "NLB": "TCP/UDP 리스너 및 대상 그룹 구성",
            "CLB": "클래식 로드 밸런서 설정",
            "Target Groups": "대상 그룹 생성 및 헬스 체크 설정",
            
            # 메시징
            "SQS": "큐 생성 및 메시지 보존 기간 설정",
            "Standard Queue": "표준 큐 생성 및 속성 설정",
            "FIFO Queue": "FIFO 큐 생성 및 중복 제거 설정",
            "Dead Letter Queue": "DLQ 설정 및 재시도 정책 구성",
            "SNS": "토픽 생성 및 구독자 설정",
            "EventBridge": "이벤트 버스 및 규칙 생성",
            "Event Bus": "커스텀 이벤트 버스 생성",
            "Step Functions": "상태 머신 정의 및 워크플로우 구성",
            "State Machines": "JSON 기반 상태 머신 정의",
            
            # DNS 및 CDN
            "Route 53": "호스팅 영역 생성 및 레코드 설정",
            "DNS": "DNS 레코드 타입 선택 및 값 설정",
            "Health Checks": "헬스 체크 생성 및 알람 설정",
            "Routing Policies": "라우팅 정책 선택 (Simple/Weighted/Latency/Failover)",
            
            # API
            "API Gateway": "REST API 엔드포인트 생성",
            "REST API": "리소스 및 메서드 정의",
            "WebSocket API": "WebSocket 라우트 및 통합 설정",
            "API Keys": "API 키 생성 및 사용량 계획 설정",
            
            # 모니터링 및 보안
            "CloudWatch": "메트릭 수집 및 알람 설정",
            "Metrics": "커스텀 메트릭 생성 및 네임스페이스 설정",
            "Logs": "로그 그룹 생성 및 보존 기간 설정",
            "Alarms": "알람 임계값 및 알림 대상 설정",
            "Dashboards": "대시보드 생성 및 위젯 구성",
            "CloudTrail": "트레일 생성 및 S3 버킷 설정",
            "GuardDuty": "GuardDuty 활성화 및 탐지 설정",
            "Inspector": "평가 대상 및 규칙 패키지 선택",
            "Macie": "데이터 검색 작업 생성",
            "IAM": "역할 및 정책 생성",
            "KMS": "암호화 키 생성 및 권한 설정",
            "CloudHSM": "HSM 클러스터 생성 및 초기화",
            "Secrets Manager": "시크릿 생성 및 자동 교체 설정",
            "Certificate Manager": "인증서 요청 및 검증",
            
            # 관리 및 거버넌스
            "Config": "구성 레코더 및 규칙 설정",
            "Systems Manager": "관리 인스턴스 등록 및 문서 실행",
            "Parameter Store": "파라미터 생성 및 계층 구조 설정",
            "Patch Manager": "패치 베이스라인 및 유지 관리 기간 설정",
            "Organizations": "조직 생성 및 계정 초대",
            "Control Tower": "랜딩 존 설정 및 가드레일 구성",
            "Service Catalog": "포트폴리오 및 제품 생성",
            "Well-Architected": "워크로드 정의 및 검토 수행",
        }
        
        return config_map.get(service_name, f"{service_name} 기본 설정 및 구성")
    
    def _get_integration_method(self, primary_service: str, supporting_service: str) -> str:
        """서비스 간 통합 방식 생성"""
        # 특정 서비스 조합에 대한 통합 패턴
        integration_patterns = {
            # Lambda 통합
            ("Lambda", "DynamoDB"): "Event-Driven Integration",
            ("Lambda", "SQS"): "Event Source Mapping",
            ("Lambda", "SNS"): "Event Subscription",
            ("Lambda", "S3"): "Event Notification",
            ("Lambda", "EventBridge"): "Event-Driven Integration",
            ("Lambda", "Step Functions"): "Workflow Integration",
            
            # API Gateway 통합
            ("API Gateway", "Lambda"): "Proxy Integration",
            ("API Gateway", "DynamoDB"): "Direct Integration",
            ("API Gateway", "SQS"): "Service Integration",
            
            # CloudFront 통합
            ("CloudFront", "S3"): "Origin Configuration",
            ("CloudFront", "ALB"): "Custom Origin",
            ("CloudFront", "Lambda@Edge"): "Edge Function Integration",
            
            # ELB 통합
            ("ELB", "EC2"): "Target Group Registration",
            ("ALB", "EC2 Instances"): "Target Group Registration",
            ("ALB", "Lambda"): "Lambda Target Integration",
            ("NLB", "EC2"): "Target Group Registration",
            
            # Route 53 통합
            ("Route 53", "CloudFront"): "Alias Record",
            ("Route 53", "ALB"): "Alias Record",
            ("Route 53", "ELB"): "Alias Record",
            ("Route 53", "S3"): "Static Website Hosting",
            
            # VPC 통합
            ("VPC", "RDS"): "Security Group Configuration",
            ("VPC", "EC2"): "Network Configuration",
            ("VPC", "Lambda"): "VPC Configuration",
            ("VPC", "ElastiCache"): "Subnet Group Configuration",
            
            # EC2 통합
            ("EC2 Instances", "Auto Scaling"): "Auto Scaling Group Integration",
            ("EC2 Instances", "EBS"): "Volume Attachment",
            ("EC2 Instances", "Security Groups"): "Network Security Configuration",
            ("Auto Scaling", "Load Balancing"): "Target Group Integration",
            ("Auto Scaling", "ALB"): "Target Group Integration",
            
            # IAM 통합
            ("IAM", "S3"): "Bucket Policy",
            ("IAM Users", "Groups"): "Group Membership",
            ("IAM Users", "Roles"): "Role Assumption",
            ("Roles", "EC2"): "Instance Profile",
            ("Roles", "Lambda"): "Execution Role",
            
            # 암호화 통합
            ("KMS", "S3"): "Server-Side Encryption",
            ("KMS", "RDS"): "Encryption at Rest",
            ("KMS", "EBS"): "Volume Encryption",
            ("KMS", "Lambda"): "Environment Variable Encryption",
            
            # 모니터링 통합
            ("CloudWatch", "Lambda"): "Automatic Logging",
            ("CloudWatch", "EC2"): "CloudWatch Agent",
            ("CloudWatch", "RDS"): "Enhanced Monitoring",
            ("CloudWatch", "ALB"): "Access Logs",
            ("CloudTrail", "S3"): "Log Delivery",
            ("CloudTrail", "CloudWatch"): "Log Stream Integration",
            
            # 메시징 통합
            ("SQS", "Lambda"): "Event Source Mapping",
            ("SNS", "SQS"): "Fan-out Pattern",
            ("SNS", "Lambda"): "Event Subscription",
            ("EventBridge", "Lambda"): "Event Target",
            ("EventBridge", "Step Functions"): "Workflow Trigger",
            ("Step Functions", "Lambda"): "Task Integration",
            
            # 스토리지 통합
            ("S3", "CloudFront"): "Origin Configuration",
            ("S3", "Lambda"): "Event Notification",
            ("EBS", "EC2 Instances"): "Volume Attachment",
            ("EFS", "EC2"): "Mount Target",
            
            # 데이터베이스 통합
            ("RDS", "Lambda"): "VPC Configuration",
            ("DynamoDB", "Lambda"): "Event-Driven Integration",
            ("DynamoDB", "DAX"): "Caching Layer",
            ("ElastiCache", "EC2"): "In-Memory Caching",
            
            # 리전 및 AZ 통합
            ("Regions", "Availability Zones"): "Multi-AZ Deployment",
            ("Regions", "Edge Locations"): "Global Distribution",
            ("Availability Zones", "Subnets"): "Network Segmentation",
            
            # VPC 네트워킹
            ("Subnets", "Route Tables"): "Routing Configuration",
            ("Route Tables", "Internet Gateway"): "Internet Access",
            ("NAT Gateway", "Route Tables"): "Outbound Routing",
            ("VPC Peering", "Route Tables"): "Cross-VPC Routing",
        }
        
        # 조합 확인
        key = (primary_service, supporting_service)
        if key in integration_patterns:
            return integration_patterns[key]
        
        # 역방향 조합 확인
        reverse_key = (supporting_service, primary_service)
        if reverse_key in integration_patterns:
            return integration_patterns[reverse_key]
        
        # 일반적인 패턴
        if "CloudWatch" in supporting_service or "CloudWatch" in primary_service:
            return "Monitoring Integration"
        elif "IAM" in supporting_service or "IAM" in primary_service:
            return "Permission-Based Integration"
        elif supporting_service in ["SQS", "SNS", "EventBridge"] or primary_service in ["SQS", "SNS", "EventBridge"]:
            return "Event-Driven Integration"
        elif supporting_service in ["Lambda", "API Gateway"] or primary_service in ["Lambda", "API Gateway"]:
            return "API Integration"
        elif "KMS" in supporting_service or "KMS" in primary_service:
            return "Encryption Integration"
        else:
            return "Direct Integration"

    
    def generate_aws_links(self, day_number: int) -> List[str]:
        """AWS 문서 링크 생성"""
        config = self.get_daily_config(day_number)
        services = config["primary_services"]
        links = []
        
        # 주요 서비스 문서 링크
        for service in services[:2]:
            service_slug = service.lower().replace(' ', '-')
            links.append(f"{AWS_DOCS_BASE_URL}/{service_slug}/latest/userguide/")
        
        # Well-Architected Framework
        links.append(f"{AWS_DOCS_BASE_URL}/wellarchitected/latest/framework/")
        
        # 가격 정보
        links.append(f"{AWS_PRICING_BASE_URL}/")
        
        # 아키텍처 센터
        links.append(f"{AWS_ARCHITECTURE_CENTER_URL}/")
        
        return links
    
    def populate_template(self, day_number: int, template: str) -> str:
        """템플릿 플레이스홀더 치환"""
        config = self.get_daily_config(day_number)
        company = self.generate_company_info(day_number)
        business_context = self.generate_business_context(day_number)
        architecture = self.generate_architecture_section(day_number)
        implementation = self.generate_implementation_details(day_number)
        impact = self.generate_business_impact(day_number)
        integrations = self.generate_service_integrations(day_number)
        connections = self.generate_cross_day_connections(day_number)
        diagrams = self.generate_mermaid_diagrams(day_number)
        aws_links = self.generate_aws_links(day_number)
        
        # Day 1 (CloudFront) 특별 처리
        is_cloudfront_day = day_number == 1 and config['primary_services'][0] == "CloudFront"
        
        # Day 1 CloudFront용 특별 설정
        if is_cloudfront_day:
            primary_service_action = "생성"
            primary_service_description = "CloudFront Distribution 생성 및 글로벌 콘텐츠 전송 네트워크 구성"
            console_path_prefix = "Services > Networking & Content Delivery"
            step1_title = "CloudFront Distribution 생성"
            step1_description = "AWS Console을 통해 CloudFront Distribution을 생성하고 Origin을 설정합니다."
            step1_console_path = "Services > Networking & Content Delivery > CloudFront > Create Distribution"
            config_field_1_label = "Origin Domain"
            config_field_2_label = "Viewer Protocol Policy"
            config_field_3_label = "Price Class"
        else:
            primary_service_action = "생성"
            primary_service_description = f"{config['primary_services'][0] if config['primary_services'] else 'AWS Service'} 리소스 생성 및 구성"
            console_path_prefix = "Services > Compute"
            step1_title = f"{config['primary_services'][0] if config['primary_services'] else 'AWS Service'} 생성"
            step1_description = f"AWS Console을 통해 {config['primary_services'][0] if config['primary_services'] else 'AWS Service'} 리소스를 생성하고 기본 설정을 구성합니다."
            step1_console_path = f"Services > Compute > {config['primary_services'][0] if config['primary_services'] else 'AWS Service'} > Create Resource"
            config_field_1_label = "Name/ID"
            config_field_2_label = "Region"
            config_field_3_label = "Type"
        
        # 기본 정보 치환
        replacements = {
            "{day_number}": str(day_number),
            "{day_title}": config["title"],
            "{company_name}": company.name,
            "{case_study_focus}": config["case_study_focus"],
            "{primary_services}": ", ".join(config["primary_services"]),
            "{industry}": company.industry,
            "{company_size}": company.size.value.capitalize(),
            "{case_source}": company.public_references[0] if company.public_references else "AWS Well-Architected Framework 기반",
            "{case_type}": "실제 기업 사례" if company.is_real_company else "Best Practice 기반 가상 사례",
            
            # 비즈니스 도전과제
            "{business_challenge_description}": business_context.challenge,
            "{problem_point_1}": "높은 트래픽 처리 요구",
            "{problem_point_2}": "글로벌 사용자 대응 필요",
            "{problem_point_3}": "비용 효율적인 확장성 확보",
            "{technical_constraint_1}": business_context.constraints[0] if business_context.constraints else "제한된 예산",
            "{technical_constraint_2}": business_context.constraints[1] if len(business_context.constraints) > 1 else "기존 시스템 호환성",
            "{infrastructure_limitation_1}": "온프레미스 인프라의 확장성 한계",
            "{infrastructure_limitation_2}": "수동 운영으로 인한 느린 대응 속도",
            
            # 요구사항
            "{performance_requirement_1}": business_context.requirements[0].description if business_context.requirements else "응답시간 < 100ms",
            "{performance_requirement_2}": business_context.requirements[1].description if len(business_context.requirements) > 1 else "처리량 > 10,000 TPS",
            "{scalability_requirement_1}": "동시 사용자 100만명 지원",
            "{scalability_requirement_2}": "트래픽 10배 증가 대응",
            "{security_requirement_1}": "데이터 암호화 및 접근 제어",
            "{compliance_requirement_1}": "산업 표준 규정 준수",
            "{cost_constraint_1}": "월간 인프라 비용 $10,000 이하",
            "{cost_constraint_2}": "ROI 6개월 이내 달성",
            
            # 아키텍처
            "{architecture_diagram}": diagrams["architecture"],
            "{data_flow_diagram}": diagrams["data_flow"],
            "{cross_day_integration_diagram}": diagrams["cross_day_integration"],
            
            # 서비스 구성
            "{primary_service_1}": config["primary_services"][0] if config["primary_services"] else "AWS Service",
            "{selection_reason_1}": "높은 가용성 및 확장성 제공",
            "{selection_reason_2}": "관리형 서비스로 운영 부담 감소",
            "{service_category}": "Networking & Content Delivery" if is_cloudfront_day else ("Compute" if "EC2" in str(config["primary_services"]) else "Storage"),
            "{service_name}": config["primary_services"][0] if config["primary_services"] else "AWS Service",
            "{config_item_1}": "Origin Domain" if is_cloudfront_day else "Region",
            "{config_value_1}": "example-bucket.s3.amazonaws.com" if is_cloudfront_day else f"day{day_number}-resource",
            "{config_item_2}": "Viewer Protocol Policy" if is_cloudfront_day else "Instance Type / Configuration",
            "{config_value_2}": "Redirect HTTP to HTTPS" if is_cloudfront_day else "Standard",
            "{config_item_3}": "Price Class" if is_cloudfront_day else "Auto Scaling",
            "{config_value_3}": "Use All Edge Locations" if is_cloudfront_day else "활성화",
            
            # 지원 서비스 (템플릿에서 사용되지만 누락된 변수들)
            "{supporting_service_1}": config["primary_services"][1] if len(config["primary_services"]) > 1 else "CloudWatch",
            "{supporting_service_2}": config["primary_services"][2] if len(config["primary_services"]) > 2 else "IAM",
            "{service_role_description}": self._get_service_role_description(config["primary_services"][1] if len(config["primary_services"]) > 1 else "CloudWatch"),
            "{service_role_description_2}": self._get_service_role_description(config["primary_services"][2] if len(config["primary_services"]) > 2 else "IAM"),
            "{config_summary}": self._get_config_summary(config["primary_services"][1] if len(config["primary_services"]) > 1 else "CloudWatch"),
            "{config_summary_2}": self._get_config_summary(config["primary_services"][2] if len(config["primary_services"]) > 2 else "IAM"),
            "{integration_method}": self._get_integration_method(config["primary_services"][0] if config["primary_services"] else "AWS Service", config["primary_services"][1] if len(config["primary_services"]) > 1 else "CloudWatch"),
            "{integration_method_2}": self._get_integration_method(config["primary_services"][0] if config["primary_services"] else "AWS Service", config["primary_services"][2] if len(config["primary_services"]) > 2 else "IAM"),
            
            # 데이터 플로우 (템플릿에서 사용되지만 누락된 변수들)
            "{service_a}": config["primary_services"][0] if config["primary_services"] else "Primary Service",
            "{service_b}": config["primary_services"][1] if len(config["primary_services"]) > 1 else "Supporting Service",
            "{service_c}": "Data Storage",
            "{flow_step_1_description}": "사용자 요청을 받아 처리 시작",
            "{flow_step_2_description}": "비즈니스 로직 처리 및 데이터 변환",
            "{flow_step_3_description}": "데이터 저장 및 영속화",
            "{flow_step_4_description}": "처리 결과를 사용자에게 반환",
            
            # CloudFormation/Terraform 템플릿 변수
            "{case_study_name}": f"{company.name} - {config['case_study_focus']}",
            "{resource_name}": f"netflix-cdn-distribution" if is_cloudfront_day else f"day{day_number}-resource",
            "{ResourceLogicalId}": f"NetflixCDNDistribution" if is_cloudfront_day else f"Day{day_number}Resource",
            "{ServiceNamespace}": "CloudFront" if is_cloudfront_day else (config["primary_services"][0].replace(" ", "") if config["primary_services"] else "Service"),
            "{ResourceType}": "Distribution" if is_cloudfront_day else "Resource",
            "{Property1}": "Origins" if is_cloudfront_day else "Name",
            "{Value1}": "[{DomainName: netflix-content.s3.amazonaws.com}]" if is_cloudfront_day else f"day{day_number}-resource",
            "{Property2}": "Enabled" if is_cloudfront_day else "Type",
            "{Value2}": "true" if is_cloudfront_day else "Standard",
            "{project_name}": f"day{day_number}-project",
            "{environment}": "production",
            "{resource_type}": config["primary_services"][0].lower().replace(" ", "_") if config["primary_services"] else "resource",
            "{property_1}": "name",
            "{value_1}": f"day{day_number}-resource",
            "{property_2}": "type",
            "{value_2}": "standard",
            
            # 모니터링 관련 (템플릿에서 사용되지만 누락된 변수들)
            "{service_namespace}": "AWS/CloudFront" if is_cloudfront_day else (config["primary_services"][0].replace(" ", "") if config["primary_services"] else "AWS/Service"),
            "{metric_description_1}": "CloudFront 요청 수 측정" if is_cloudfront_day else "평균 응답 시간 측정",
            "{normal_range_1}": "> 1000 requests/min" if is_cloudfront_day else "< 100ms",
            "{warning_threshold_1}": "< 100 requests/min" if is_cloudfront_day else "> 200ms",
            "{metric_description_2}": "4xx 에러율 모니터링" if is_cloudfront_day else "초당 처리 요청 수",
            "{normal_range_2}": "< 5%" if is_cloudfront_day else "> 1000 TPS",
            "{warning_threshold_2}": "> 10%" if is_cloudfront_day else "< 500 TPS",
            "{alarm_name}": f"day{day_number}-cloudfront-error-alarm" if is_cloudfront_day else f"day{day_number}-high-latency-alarm",
            "{metric_name}": "4xxErrorRate" if is_cloudfront_day else "ResponseTime",
            "{condition}": ">=",
            "{period}": "5분",
            "{evaluation_periods}": "2회 연속",
            "{sns_topic_arn}": "arn:aws:sns:ap-northeast-2:123456789012:alerts",
            "{widget_1}": "요청 수 그래프" if is_cloudfront_day else "응답 시간 그래프",
            "{metric_visualization_1}": "시계열 라인 차트",
            "{widget_2}": "에러율 그래프" if is_cloudfront_day else "처리량 그래프",
            "{metric_visualization_2}": "시계열 라인 차트",
            "{widget_3}": "데이터 전송량 그래프" if is_cloudfront_day else "에러율 그래프",
            "{metric_visualization_3}": "시계열 라인 차트",
            
            # 관련 서비스
            "{related_service_1}": connections[0].service_name if connections else "CloudWatch",
            "{related_day_1}": str(connections[0].day_number) if connections else "22",
            "{integration_description_1}": connections[0].description if connections else "모니터링 및 알람 통합",
            "{related_service_2}": connections[1].service_name if len(connections) > 1 else "IAM",
            "{related_day_2}": str(connections[1].day_number) if len(connections) > 1 else "2",
            "{integration_description_2}": connections[1].description if len(connections) > 1 else "보안 및 접근 제어",
            
            # 구현 세부사항
            "{primary_service}": config["primary_services"][0] if config["primary_services"] else "AWS Service",
            "{category}": "Networking & Content Delivery" if is_cloudfront_day else "Compute",
            "{service}": config["primary_services"][0] if config["primary_services"] else "AWS Service",
            "{resource}": "Distribution" if is_cloudfront_day else "Resource",
            "{resource_name_example}": f"netflix-cdn-distribution" if is_cloudfront_day else f"day{day_number}-resource",
            "{region}": "Global (CloudFront는 글로벌 서비스)" if is_cloudfront_day else "ap-northeast-2",
            "{config_field_1}": "Origin Domain" if is_cloudfront_day else "Name",
            "{config_value_1}": "netflix-content.s3.amazonaws.com" if is_cloudfront_day else f"day{day_number}-resource",
            "{config_field_2}": "Viewer Protocol Policy" if is_cloudfront_day else "Type",
            "{config_value_2}": "Redirect HTTP to HTTPS" if is_cloudfront_day else "Standard",
            "{advanced_config_1}": "Cache Behavior" if is_cloudfront_day else "High Availability",
            "{advanced_value_1}": "CachingOptimized" if is_cloudfront_day else "Multi-AZ 배포",
            "{config_explanation_1}": "최적화된 캐싱 정책 적용" if is_cloudfront_day else "여러 가용 영역에 걸쳐 리소스 배포",
            "{advanced_config_2}": "Compress Objects" if is_cloudfront_day else "Backup",
            "{advanced_value_2}": "Yes (Gzip 압축)" if is_cloudfront_day else "자동 백업 활성화",
            "{config_explanation_2}": "자동 압축으로 전송 속도 향상" if is_cloudfront_day else "일일 자동 백업 및 7일 보관",
            "{wait_time}": "15-20" if is_cloudfront_day else "5-10",
            "{related_service}": "CloudWatch",
            "{integration_feature}": "Monitoring",
            "{verification_step_1}": "메트릭이 정상적으로 수집되는지 확인",
            "{verification_step_2}": "알람이 올바르게 설정되었는지 검증",
            "{trust_policy}": "서비스 신뢰 관계",
            "{permission_policy}": "최소 권한 정책",
            
            # 비즈니스 임팩트
            "{metric_1}": "응답 시간",
            "{before_value_1}": "200ms",
            "{after_value_1}": "50ms",
            "{improvement_1}": "75",
            "{metric_2}": "처리량",
            "{before_value_2}": "1,000 TPS",
            "{after_value_2}": "10,000 TPS",
            "{improvement_2}": "900",
            "{metric_3}": "가용성",
            "{before_value_3}": "99.9%",
            "{after_value_3}": "99.99%",
            "{improvement_3}": "0.09",
            "{achievement_1}": "응답 시간 75% 개선",
            "{achievement_2}": "처리량 10배 증가",
            "{achievement_3}": "가용성 99.99% 달성",
            "{cost_before}": "10,000",
            "{cost_after}": "7,000",
            "{cost_savings}": "3,000",
            "{cost_reduction_percentage}": "30",
            "{cost_factor_1}": "자동 스케일링 최적화",
            "{savings_1}": "1,500",
            "{cost_factor_2}": "예약 인스턴스 활용",
            "{savings_2}": "1,000",
            "{cost_factor_3}": "스토리지 계층화",
            "{savings_3}": "500",
            "{initial_investment}": "20,000",
            "{monthly_savings}": "3,000",
            "{payback_period}": "7",
            "{deploy_time_before}": "2시간",
            "{deploy_time_after}": "15분",
            "{deploy_improvement}": "87.5",
            "{mttr_before}": "30분",
            "{mttr_after}": "5분",
            "{mttr_improvement}": "83",
            "{ops_team_before}": "5",
            "{ops_team_after}": "3",
            "{uptime_before}": "99.9",
            "{uptime_after}": "99.99",
            "{downtime_before}": "8.76",
            "{downtime_after}": "0.88",
            
            # 서비스 연계
            "{previous_day_1}": str(connections[0].day_number) if connections else "1",
            "{previous_service_1}": connections[0].service_name if connections else "글로벌 인프라",
            "{integration_description_1}": connections[0].description if connections else "기본 인프라 구성",
            "{usage_in_case_1}": "멀티 리전 배포 기반",
            "{usage_in_case_2}": "글로벌 사용자 대응",
            "{learning_point_1}": "리전 선택의 중요성",
            "{previous_day_2}": str(connections[1].day_number) if len(connections) > 1 else "2",
            "{previous_service_2}": connections[1].service_name if len(connections) > 1 else "IAM",
            "{integration_description_2}": connections[1].description if len(connections) > 1 else "보안 설정",
            "{usage_in_case_3}": "역할 기반 접근 제어",
            "{future_day_1}": str(connections[2].day_number) if len(connections) > 2 else str(day_number + 5),
            "{future_service_1}": connections[2].service_name if len(connections) > 2 else "고급 서비스",
            "{expansion_description_1}": "추가 기능 통합",
            "{evolution_point_1}": "성능 최적화",
            "{evolution_point_2}": "비용 효율성 향상",
            "{expected_benefit_1}": "운영 효율성 증대",
            "{future_day_2}": str(day_number + 7),
            "{future_service_2}": "모니터링 서비스",
            "{expansion_description_2}": "고급 모니터링 통합",
            "{integration_scenario_1}": "실시간 알람 및 대시보드",
            "{integration_scenario_description}": f"Day {day_number}의 서비스들이 전체 아키텍처에서 핵심 역할 수행",
            "{day_1}": str(day_number),
            "{service_1}": config["primary_services"][0] if config["primary_services"] else "Primary Service",
            "{day_2}": str(connections[0].day_number) if connections else str(day_number + 1),
            "{service_2}": connections[0].service_name if connections else "Related Service",
            "{day_3}": str(connections[1].day_number) if len(connections) > 1 else str(day_number + 2),
            "{service_3}": connections[1].service_name if len(connections) > 1 else "Supporting Service",
            
            # 참고 자료
            "{aws_docs_url}": aws_links[0] if aws_links else f"{AWS_DOCS_BASE_URL}/",
            "{api_reference_url}": aws_links[0] if aws_links else f"{AWS_DOCS_BASE_URL}/",
            "{well_architected_url}": aws_links[2] if len(aws_links) > 2 else f"{AWS_DOCS_BASE_URL}/wellarchitected/",
            "{architecture_center_url}": aws_links[4] if len(aws_links) > 4 else AWS_ARCHITECTURE_CENTER_URL,
            "{best_practices_url}": aws_links[0] if aws_links else f"{AWS_DOCS_BASE_URL}/",
            "{security_docs_url}": f"{AWS_DOCS_BASE_URL}/security/",
            "{pricing_calculator_url}": "https://calculator.aws/",
            "{pricing_url}": AWS_PRICING_BASE_URL,
            "{cost_optimization_url}": f"{AWS_DOCS_BASE_URL}/cost-management/",
            "{company_blog_url}": company.public_references[0] if company.public_references else "#",
            "{reinvent_url}": "https://reinvent.awsevents.com/",
            "{case_study_url}": f"{AWS_ARCHITECTURE_CENTER_URL}/customers/",
            "{whitepaper_url}": f"{AWS_DOCS_BASE_URL}/whitepapers/",
            "{pillar}": "Operational Excellence",
            "{architecture_pattern}": config["case_study_focus"],
            "{security_topic}": "IAM Best Practices",
            "{presentation_title}": f"{company.name} - {config['case_study_focus']}",
            "{whitepaper_title}": "AWS Well-Architected Framework",
            
            # 학습 포인트
            "{learning_point_1_1}": f"{config['primary_services'][0] if config['primary_services'] else 'AWS 서비스'}의 핵심 기능 이해",
            "{learning_point_1_2}": "실제 프로덕션 환경 구성 방법",
            "{learning_point_1_3}": "모범 사례 및 안티 패턴",
            "{scalability_consideration}": "자동 스케일링 및 로드 밸런싱",
            "{availability_consideration}": "멀티 AZ 배포 및 장애 조치",
            "{performance_consideration}": "캐싱 및 최적화 전략",
            "{security_consideration}": "최소 권한 원칙 및 암호화",
            "{integration_pattern_1}": integrations[0].integration_pattern if integrations else "Direct Integration",
            "{integration_pattern_2}": integrations[1].integration_pattern if len(integrations) > 1 else "Event-Driven Integration",
            "{integration_pattern_3}": "API Gateway Pattern",
            "{cost_strategy_1}": "예약 인스턴스 활용",
            "{cost_strategy_2}": "자동 스케일링 최적화",
            "{cost_strategy_3}": "스토리지 계층화",
            "{ops_best_practice_1}": "Infrastructure as Code 사용",
            "{ops_best_practice_2}": "자동화된 배포 파이프라인",
            "{ops_best_practice_3}": "포괄적인 모니터링 및 알람",
            
            # 다음 단계
            "{related_day_1}": str(connections[0].day_number) if connections else str(day_number + 1),
            "{related_topic_1}": connections[0].service_name if connections else "다음 주제",
            "{related_day_2}": str(connections[1].day_number) if len(connections) > 1 else str(day_number + 2),
            "{related_topic_2}": connections[1].service_name if len(connections) > 1 else "관련 주제",
            "{related_day_3}": str(connections[2].day_number) if len(connections) > 2 else str(day_number + 3),
            "{related_topic_3}": connections[2].service_name if len(connections) > 2 else "심화 주제",
            
            # 메타데이터
            "{current_date}": datetime.now().strftime("%Y-%m-%d"),
            "{author_name}": "AWS SAA Study Materials Generator",
        }
        
        # 템플릿 치환
        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, str(value))
        
        return result

    
    def generate_case_study(self, day_number: int, output_path: Optional[Path] = None) -> str:
        """특정 일차의 사례 연구 생성
        
        Args:
            day_number: 일차 번호 (1-28)
            output_path: 출력 파일 경로 (None이면 자동 생성)
            
        Returns:
            생성된 콘텐츠 문자열
        """
        # 템플릿 로드
        template = self.load_template()
        
        # 템플릿 치환
        content = self.populate_template(day_number, template)
        
        # 출력 경로 결정
        if output_path is None:
            config = self.get_daily_config(day_number)
            week_number = config["week"]
            output_path = (
                self.output_base_path / 
                f"week{week_number}" / 
                f"day{day_number}" / 
                "advanced" / 
                "case-study.md"
            )
        
        # 디렉토리 생성
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 파일 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Generated case study for Day {day_number}: {output_path}")
        
        return content
    
    def generate_all_case_studies(self, start_day: int = 1, end_day: int = 28) -> Dict[int, str]:
        """모든 일차의 사례 연구 생성
        
        Args:
            start_day: 시작 일차 (기본값: 1)
            end_day: 종료 일차 (기본값: 28)
            
        Returns:
            일차별 생성된 파일 경로 딕셔너리
        """
        results = {}
        
        print(f"\n{'='*60}")
        print(f"Case Study Generator - Generating Days {start_day} to {end_day}")
        print(f"{'='*60}\n")
        
        for day in range(start_day, end_day + 1):
            try:
                config = self.get_daily_config(day)
                week_number = config["week"]
                output_path = (
                    self.output_base_path / 
                    f"week{week_number}" / 
                    f"day{day}" / 
                    "advanced" / 
                    "case-study.md"
                )
                
                self.generate_case_study(day, output_path)
                results[day] = str(output_path)
                
            except Exception as e:
                print(f"✗ Error generating case study for Day {day}: {e}")
                results[day] = f"Error: {e}"
        
        print(f"\n{'='*60}")
        print(f"Generation Complete!")
        print(f"Successfully generated: {sum(1 for v in results.values() if not v.startswith('Error'))} / {end_day - start_day + 1}")
        print(f"{'='*60}\n")
        
        return results


# CLI 실행을 위한 메인 함수
def main():
    """CLI 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS SAA Case Study Generator")
    parser.add_argument(
        "--day",
        type=int,
        help="Generate case study for specific day (1-28)"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start day for batch generation (default: 1)"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=28,
        help="End day for batch generation (default: 28)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Custom output path (optional)"
    )
    
    args = parser.parse_args()
    
    generator = CaseStudyGenerator()
    
    if args.day:
        # 단일 일차 생성
        output_path = Path(args.output) if args.output else None
        generator.generate_case_study(args.day, output_path)
    else:
        # 배치 생성
        generator.generate_all_case_studies(args.start, args.end)


if __name__ == "__main__":
    main()
