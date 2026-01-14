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
            "{service_category}": "Compute" if "EC2" in str(config["primary_services"]) else "Storage",
            "{service_name}": config["primary_services"][0] if config["primary_services"] else "AWS Service",
            "{config_item_1}": "Region",
            "{config_value_1}": "ap-northeast-2 (서울)",
            "{config_item_2}": "Instance Type / Configuration",
            "{config_value_2}": "프로덕션 환경에 적합한 설정",
            "{config_item_3}": "Auto Scaling",
            "{config_value_3}": "활성화",
            
            # 관련 서비스
            "{related_service_1}": connections[0].service_name if connections else "CloudWatch",
            "{related_day_1}": str(connections[0].day_number) if connections else "22",
            "{integration_description_1}": connections[0].description if connections else "모니터링 및 알람 통합",
            "{related_service_2}": connections[1].service_name if len(connections) > 1 else "IAM",
            "{related_day_2}": str(connections[1].day_number) if len(connections) > 1 else "2",
            "{integration_description_2}": connections[1].description if len(connections) > 1 else "보안 및 접근 제어",
            
            # 구현 세부사항
            "{primary_service}": config["primary_services"][0] if config["primary_services"] else "AWS Service",
            "{category}": "Compute",
            "{service}": config["primary_services"][0] if config["primary_services"] else "AWS Service",
            "{resource}": "Resource",
            "{resource_name_example}": f"day{day_number}-resource",
            "{region}": "ap-northeast-2",
            "{config_field_1}": "Name",
            "{config_value_1}": f"day{day_number}-resource",
            "{config_field_2}": "Type",
            "{config_value_2}": "Standard",
            "{advanced_config_1}": "High Availability",
            "{advanced_value_1}": "Multi-AZ 배포",
            "{config_explanation_1}": "여러 가용 영역에 걸쳐 리소스 배포",
            "{advanced_config_2}": "Backup",
            "{advanced_value_2}": "자동 백업 활성화",
            "{config_explanation_2}": "일일 자동 백업 및 7일 보관",
            "{wait_time}": "5-10",
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
