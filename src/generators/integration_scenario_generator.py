# Integration Scenario Generator
"""
통합 시나리오 생성기 (Task 8.2)
주요 통합 시나리오 (Netflix, Airbnb 등) 문서 생성
End-to-end 시나리오 및 서비스 플로우 생성
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from src.cross_service_integration import (
    CrossServiceIntegrationMapper,
    IntegrationScenario,
    get_service_dependency_mapper
)
from src.daily_topics import DAILY_TOPICS, get_topic_by_day
from src.config import STUDY_MATERIALS_ROOT


class IntegrationScenarioGenerator:
    """통합 시나리오 문서 생성기"""
    
    def __init__(self):
        self.mapper = get_service_dependency_mapper()
        self.output_base_path = STUDY_MATERIALS_ROOT
        self.scenarios = self.mapper.get_integration_scenarios()
    
    def generate_scenario_overview(self, scenario: IntegrationScenario) -> str:
        """시나리오 개요 섹션 생성"""
        involved_days_str = ", ".join([f"Day {d}" for d in scenario.involved_days])
        
        return f"""## 📋 시나리오 개요

- **시나리오 ID**: `{scenario.scenario_id}`
- **시나리오명**: {scenario.name}
- **설명**: {scenario.description}
- **관련 일차**: {involved_days_str}
- **주요 일차**: Day {scenario.primary_day}
- **핵심 서비스**: {", ".join(scenario.services)}
- **통합 패턴**: {scenario.integration_pattern}
- **사용 사례**: {scenario.use_case}
"""
    
    def generate_involved_days_section(self, scenario: IntegrationScenario) -> str:
        """관련 일차 섹션 생성"""
        section = "## 📅 관련 일차\n\n"
        
        for day in scenario.involved_days:
            try:
                topic = get_topic_by_day(day)
                is_primary = " **(주요)**" if day == scenario.primary_day else ""
                section += f"### Day {day}: {topic['title']}{is_primary}\n\n"
                section += f"**주요 서비스**: {', '.join(topic['primary_services'])}\n\n"
                section += f"**역할**: "
                
                if day == scenario.primary_day:
                    section += "이 시나리오의 핵심 서비스를 제공합니다.\n\n"
                else:
                    section += "통합 아키텍처의 지원 서비스를 제공합니다.\n\n"
                
                section += f"**학습 링크**: [Day {day} 학습 자료](../week{topic['week']}/day{day}/README.md)\n\n"
            except (ValueError, KeyError):
                continue
        
        return section
    
    def generate_architecture_diagram(self, scenario: IntegrationScenario) -> str:
        """아키텍처 다이어그램 생성"""
        diagram = "```mermaid\ngraph TB\n"
        diagram += '    subgraph "사용자 계층"\n'
        diagram += '        Users[전 세계 사용자]\n'
        diagram += '    end\n\n'
        
        # 서비스별 서브그래프 생성
        for i, day in enumerate(scenario.involved_days):
            try:
                topic = get_topic_by_day(day)
                diagram += f'    subgraph "Day {day}: {topic["title"]}"\n'
                
                for j, service in enumerate(topic['primary_services'][:2]):
                    node_id = f"D{day}S{j}"
                    diagram += f'        {node_id}[{service}]\n'
                
                diagram += '    end\n\n'
            except (ValueError, KeyError):
                continue
        
        # 연결 생성
        diagram += '    Users --> D' + str(scenario.involved_days[0]) + 'S0\n'
        
        for i in range(len(scenario.involved_days) - 1):
            current_day = scenario.involved_days[i]
            next_day = scenario.involved_days[i + 1]
            diagram += f'    D{current_day}S0 --> D{next_day}S0\n'
        
        diagram += "```\n"
        return diagram
    
    def generate_service_flow(self, scenario: IntegrationScenario) -> str:
        """서비스 플로우 섹션 생성"""
        section = "## 🔄 서비스 플로우\n\n"
        section += "### End-to-End 요청 처리 흐름\n\n"
        
        flow_steps = self._generate_flow_steps(scenario)
        
        for i, step in enumerate(flow_steps, 1):
            section += f"{i}. **{step['title']}**\n"
            section += f"   - 서비스: {step['service']}\n"
            section += f"   - 처리: {step['description']}\n"
            section += f"   - 다음 단계: {step['next']}\n\n"
        
        # 시퀀스 다이어그램 추가
        section += "### 시퀀스 다이어그램\n\n"
        section += self._generate_sequence_diagram(scenario)
        
        return section
    
    def _generate_flow_steps(self, scenario: IntegrationScenario) -> List[Dict]:
        """플로우 단계 생성"""
        steps = []
        
        # 시나리오별 맞춤 플로우
        if scenario.scenario_id == "netflix_streaming":
            steps = [
                {
                    "title": "사용자 요청 수신",
                    "service": "CloudFront (Day 1, 16)",
                    "description": "가장 가까운 엣지 로케이션에서 요청 수신",
                    "next": "캐시 확인"
                },
                {
                    "title": "콘텐츠 캐시 확인",
                    "service": "CloudFront",
                    "description": "엣지 캐시에 콘텐츠 존재 여부 확인",
                    "next": "캐시 히트 시 즉시 반환, 미스 시 오리진 요청"
                },
                {
                    "title": "오리진 콘텐츠 조회",
                    "service": "S3 (Day 8)",
                    "description": "원본 비디오 파일을 S3에서 조회",
                    "next": "콘텐츠 스트리밍"
                },
                {
                    "title": "콘텐츠 전송",
                    "service": "CloudFront → 사용자",
                    "description": "최적화된 경로로 콘텐츠 스트리밍",
                    "next": "완료"
                }
            ]
        elif scenario.scenario_id == "airbnb_security":
            steps = [
                {
                    "title": "사용자 인증",
                    "service": "IAM (Day 2)",
                    "description": "사용자 자격 증명 및 권한 확인",
                    "next": "네트워크 접근 제어"
                },
                {
                    "title": "네트워크 격리",
                    "service": "VPC (Day 5)",
                    "description": "프라이빗 서브넷에서 안전한 통신",
                    "next": "감사 로깅"
                },
                {
                    "title": "활동 감사",
                    "service": "CloudTrail (Day 23)",
                    "description": "모든 API 호출 및 활동 기록",
                    "next": "완료"
                }
            ]
        elif scenario.scenario_id == "spotify_scalability":
            steps = [
                {
                    "title": "로드 밸런싱",
                    "service": "ELB (Day 13)",
                    "description": "트래픽을 여러 인스턴스에 분산",
                    "next": "인스턴스 처리"
                },
                {
                    "title": "요청 처리",
                    "service": "EC2 (Day 3, 4)",
                    "description": "애플리케이션 로직 실행",
                    "next": "Auto Scaling 평가"
                },
                {
                    "title": "자동 확장",
                    "service": "Auto Scaling (Day 4)",
                    "description": "부하에 따라 인스턴스 자동 조정",
                    "next": "완료"
                }
            ]
        elif scenario.scenario_id == "dropbox_storage":
            steps = [
                {
                    "title": "파일 업로드",
                    "service": "S3 (Day 8)",
                    "description": "파일을 S3 버킷에 저장",
                    "next": "Lambda 트리거"
                },
                {
                    "title": "파일 처리",
                    "service": "Lambda (Day 18)",
                    "description": "썸네일 생성, 메타데이터 추출",
                    "next": "CDN 배포"
                },
                {
                    "title": "글로벌 배포",
                    "service": "CloudFront (Day 16)",
                    "description": "전 세계 엣지 로케이션에 캐싱",
                    "next": "완료"
                }
            ]
        else:  # serverless_app
            steps = [
                {
                    "title": "API 요청",
                    "service": "API Gateway (Day 19)",
                    "description": "RESTful API 엔드포인트 호출",
                    "next": "Lambda 실행"
                },
                {
                    "title": "비즈니스 로직",
                    "service": "Lambda (Day 18)",
                    "description": "서버리스 함수 실행",
                    "next": "데이터베이스 조회"
                },
                {
                    "title": "데이터 저장/조회",
                    "service": "DynamoDB (Day 11)",
                    "description": "NoSQL 데이터베이스 작업",
                    "next": "응답 반환"
                }
            ]
        
        return steps
    
    def _generate_sequence_diagram(self, scenario: IntegrationScenario) -> str:
        """시퀀스 다이어그램 생성"""
        diagram = "```mermaid\nsequenceDiagram\n"
        diagram += "    participant User as 사용자\n"
        
        # 시나리오별 참여자 추가
        for day in scenario.involved_days:
            try:
                topic = get_topic_by_day(day)
                if topic['primary_services']:
                    service = topic['primary_services'][0]
                    diagram += f"    participant S{day} as {service}\n"
            except (ValueError, KeyError):
                continue
        
        # 상호작용 추가
        diagram += "\n    User->>S" + str(scenario.involved_days[0]) + ": 요청 전송\n"
        
        for i in range(len(scenario.involved_days) - 1):
            current = scenario.involved_days[i]
            next_day = scenario.involved_days[i + 1]
            diagram += f"    S{current}->>S{next_day}: 데이터 전달\n"
        
        last_day = scenario.involved_days[-1]
        diagram += f"    S{last_day}-->>User: 응답 반환\n"
        diagram += "```\n"
        
        return diagram

    
    def generate_implementation_guide(self, scenario: IntegrationScenario) -> str:
        """구현 가이드 섹션 생성"""
        section = "## 💻 구현 가이드\n\n"
        section += "### 단계별 구현 방법\n\n"
        
        for i, day in enumerate(scenario.involved_days, 1):
            try:
                topic = get_topic_by_day(day)
                section += f"#### 단계 {i}: Day {day} - {topic['title']} 구성\n\n"
                section += f"**주요 서비스**: {', '.join(topic['primary_services'])}\n\n"
                section += f"**구현 방법**:\n"
                section += f"1. AWS Console에서 {topic['primary_services'][0] if topic['primary_services'] else 'AWS Service'} 생성\n"
                section += f"2. 기본 설정 구성 (Region: ap-northeast-2)\n"
                section += f"3. 보안 및 접근 제어 설정\n"
                section += f"4. 모니터링 및 알람 구성\n\n"
                section += f"**검증**:\n"
                section += f"- 리소스 상태 확인\n"
                section += f"- 연결 테스트 수행\n\n"
                section += f"**상세 가이드**: [Day {day} 실습 자료](../week{topic['week']}/day{day}/hands-on-console/README.md)\n\n"
            except (ValueError, KeyError):
                continue
        
        section += "### 통합 검증\n\n"
        section += "**End-to-End 테스트**:\n"
        section += "1. 사용자 시나리오 기반 테스트 수행\n"
        section += "2. 각 서비스 간 연결 확인\n"
        section += "3. 성능 및 응답 시간 측정\n"
        section += "4. 에러 처리 및 장애 조치 테스트\n\n"
        
        return section
    
    def generate_learning_path(self, scenario: IntegrationScenario) -> str:
        """학습 경로 섹션 생성"""
        section = "## 🎓 학습 경로\n\n"
        section += "### 권장 학습 순서\n\n"
        
        # 일차 순서대로 정렬
        sorted_days = sorted(scenario.involved_days)
        
        for i, day in enumerate(sorted_days, 1):
            try:
                topic = get_topic_by_day(day)
                is_primary = " **(핵심)**" if day == scenario.primary_day else ""
                section += f"{i}. **Day {day}: {topic['title']}{is_primary}**\n"
                section += f"   - 학습 내용: {', '.join(topic['primary_services'])}\n"
                section += f"   - 예상 시간: 2-3시간\n"
                section += f"   - 학습 자료: [Day {day} README](../week{topic['week']}/day{day}/README.md)\n\n"
            except (ValueError, KeyError):
                continue
        
        section += "### 실습 순서\n\n"
        section += "1. **개별 서비스 실습**: 각 일차의 hands-on-console 실습 완료\n"
        section += "2. **서비스 통합 실습**: 서비스 간 연결 및 통합 구성\n"
        section += "3. **End-to-End 테스트**: 전체 시나리오 검증\n"
        section += "4. **최적화 및 튜닝**: 성능 및 비용 최적화\n\n"
        
        section += "### 학습 목표\n\n"
        section += f"이 통합 시나리오를 완료하면 다음을 이해하게 됩니다:\n\n"
        section += f"- {scenario.use_case}를 위한 AWS 아키텍처 설계\n"
        section += f"- {scenario.integration_pattern} 통합 패턴 구현\n"
        section += f"- 여러 AWS 서비스를 조합한 실제 솔루션 구축\n"
        section += f"- 프로덕션 환경 운영 및 모니터링\n\n"
        
        return section
    
    def generate_best_practices(self, scenario: IntegrationScenario) -> str:
        """베스트 프랙티스 섹션 생성"""
        section = "## ✅ 베스트 프랙티스\n\n"
        
        section += "### 아키텍처 설계\n\n"
        section += "- **고가용성**: 멀티 AZ 배포로 장애 대응\n"
        section += "- **확장성**: Auto Scaling 및 로드 밸런싱 활용\n"
        section += "- **보안**: 최소 권한 원칙 및 네트워크 격리\n"
        section += "- **모니터링**: CloudWatch를 통한 포괄적 모니터링\n\n"
        
        section += "### 비용 최적화\n\n"
        section += "- 예약 인스턴스 및 Savings Plans 활용\n"
        section += "- 자동 스케일링으로 리소스 최적화\n"
        section += "- S3 Lifecycle 정책으로 스토리지 비용 절감\n"
        section += "- CloudWatch 알람으로 비정상 비용 감지\n\n"
        
        section += "### 운영 효율성\n\n"
        section += "- Infrastructure as Code (CloudFormation/Terraform) 사용\n"
        section += "- CI/CD 파이프라인 구축\n"
        section += "- 자동화된 백업 및 복구 절차\n"
        section += "- 정기적인 보안 감사 및 패치\n\n"
        
        return section
    
    def generate_troubleshooting(self, scenario: IntegrationScenario) -> str:
        """트러블슈팅 섹션 생성"""
        section = "## 🔧 트러블슈팅\n\n"
        
        section += "### 일반적인 문제\n\n"
        section += "#### 문제 1: 서비스 간 연결 실패\n\n"
        section += "**증상**: 한 서비스에서 다른 서비스로 요청이 전달되지 않음\n\n"
        section += "**진단**:\n"
        section += "1. Security Group 규칙 확인\n"
        section += "2. IAM 권한 검증\n"
        section += "3. 네트워크 ACL 설정 확인\n\n"
        section += "**해결**:\n"
        section += "- 필요한 포트 및 프로토콜 허용\n"
        section += "- 적절한 IAM 역할 및 정책 부여\n"
        section += "- VPC 피어링 또는 엔드포인트 구성\n\n"
        
        section += "#### 문제 2: 성능 저하\n\n"
        section += "**증상**: 응답 시간 증가, 처리량 감소\n\n"
        section += "**진단**:\n"
        section += "1. CloudWatch 메트릭 확인 (CPU, 메모리, 네트워크)\n"
        section += "2. 병목 지점 식별\n"
        section += "3. 로그 분석\n\n"
        section += "**해결**:\n"
        section += "- 리소스 스케일 업/아웃\n"
        section += "- 캐싱 전략 적용\n"
        section += "- 데이터베이스 쿼리 최적화\n\n"
        
        section += "#### 문제 3: 비용 급증\n\n"
        section += "**증상**: 예상보다 높은 AWS 비용\n\n"
        section += "**진단**:\n"
        section += "1. Cost Explorer에서 비용 분석\n"
        section += "2. 리소스 사용률 확인\n"
        section += "3. 불필요한 리소스 식별\n\n"
        section += "**해결**:\n"
        section += "- 미사용 리소스 삭제\n"
        section += "- 예약 인스턴스 구매\n"
        section += "- Auto Scaling 정책 최적화\n\n"
        
        return section
    
    def generate_references(self, scenario: IntegrationScenario) -> str:
        """참고 자료 섹션 생성"""
        section = "## 📚 참고 자료\n\n"
        
        section += "### AWS 공식 문서\n\n"
        for day in scenario.involved_days:
            try:
                topic = get_topic_by_day(day)
                if topic['primary_services']:
                    service = topic['primary_services'][0]
                    section += f"- [{service} 사용 설명서](https://docs.aws.amazon.com/)\n"
            except (ValueError, KeyError):
                continue
        
        section += "\n### 아키텍처 패턴\n\n"
        section += f"- [AWS 아키텍처 센터 - {scenario.integration_pattern}](https://aws.amazon.com/architecture/)\n"
        section += "- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)\n"
        section += "- [AWS 솔루션 라이브러리](https://aws.amazon.com/solutions/)\n\n"
        
        section += "### 관련 학습 자료\n\n"
        for day in scenario.involved_days:
            try:
                topic = get_topic_by_day(day)
                section += f"- [Day {day}: {topic['title']}](../week{topic['week']}/day{day}/README.md)\n"
            except (ValueError, KeyError):
                continue
        
        section += "\n"
        return section
    
    def generate_scenario_document(self, scenario: IntegrationScenario) -> str:
        """완전한 시나리오 문서 생성"""
        doc = f"# {scenario.name}\n\n"
        doc += f"> **통합 시나리오**: {scenario.scenario_id}\n"
        doc += f"> **사용 사례**: {scenario.use_case}\n\n"
        doc += "---\n\n"
        
        # 각 섹션 추가
        doc += self.generate_scenario_overview(scenario)
        doc += "\n---\n\n"
        
        doc += self.generate_involved_days_section(scenario)
        doc += "\n---\n\n"
        
        doc += "## 🏗️ 서비스 아키텍처\n\n"
        doc += self.generate_architecture_diagram(scenario)
        doc += "\n---\n\n"
        
        doc += self.generate_service_flow(scenario)
        doc += "\n---\n\n"
        
        doc += self.generate_implementation_guide(scenario)
        doc += "\n---\n\n"
        
        doc += self.generate_learning_path(scenario)
        doc += "\n---\n\n"
        
        doc += self.generate_best_practices(scenario)
        doc += "\n---\n\n"
        
        doc += self.generate_troubleshooting(scenario)
        doc += "\n---\n\n"
        
        doc += self.generate_references(scenario)
        
        # 메타데이터
        doc += f"\n---\n\n"
        doc += f"**생성일**: {datetime.now().strftime('%Y-%m-%d')}\n"
        doc += f"**버전**: 1.0\n"
        
        return doc
    
    def save_scenario_document(
        self, 
        scenario: IntegrationScenario, 
        output_path: Optional[Path] = None
    ) -> Path:
        """시나리오 문서를 파일로 저장"""
        if output_path is None:
            # 기본 출력 경로: aws-saa-study-materials/integration-scenarios/
            output_dir = self.output_base_path / "integration-scenarios"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{scenario.scenario_id}.md"
        
        # 문서 생성
        content = self.generate_scenario_document(scenario)
        
        # 파일 저장
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
    
    def generate_all_scenarios(self, output_dir: Optional[Path] = None) -> List[Path]:
        """모든 통합 시나리오 문서 생성"""
        if output_dir is None:
            output_dir = self.output_base_path / "integration-scenarios"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        generated_files = []
        
        for scenario in self.scenarios:
            output_path = output_dir / f"{scenario.scenario_id}.md"
            saved_path = self.save_scenario_document(scenario, output_path)
            generated_files.append(saved_path)
        
        # README 생성
        readme_path = self._generate_scenarios_readme(output_dir)
        generated_files.append(readme_path)
        
        return generated_files
    
    def _generate_scenarios_readme(self, output_dir: Path) -> Path:
        """통합 시나리오 디렉토리의 README 생성"""
        readme_content = "# AWS 통합 시나리오\n\n"
        readme_content += "이 디렉토리는 여러 AWS 서비스를 통합한 실제 사용 사례 기반 시나리오를 포함합니다.\n\n"
        readme_content += "## 📋 시나리오 목록\n\n"
        
        for scenario in self.scenarios:
            readme_content += f"### [{scenario.name}](./{scenario.scenario_id}.md)\n\n"
            readme_content += f"- **설명**: {scenario.description}\n"
            readme_content += f"- **관련 일차**: {', '.join([f'Day {d}' for d in scenario.involved_days])}\n"
            readme_content += f"- **사용 사례**: {scenario.use_case}\n\n"
        
        readme_content += "## 🎯 학습 목표\n\n"
        readme_content += "이 통합 시나리오들을 통해 다음을 학습할 수 있습니다:\n\n"
        readme_content += "- 여러 AWS 서비스를 조합한 실제 솔루션 설계\n"
        readme_content += "- 서비스 간 통합 패턴 및 베스트 프랙티스\n"
        readme_content += "- End-to-end 아키텍처 구현 및 운영\n"
        readme_content += "- 프로덕션 환경의 고가용성 및 확장성 확보\n\n"
        
        readme_content += "## 📚 학습 순서\n\n"
        readme_content += "1. 각 일차(Day 1-28)의 기본 학습 완료\n"
        readme_content += "2. 관심 있는 통합 시나리오 선택\n"
        readme_content += "3. 시나리오의 관련 일차 복습\n"
        readme_content += "4. 통합 시나리오 문서 학습\n"
        readme_content += "5. 실습 환경에서 직접 구현\n\n"
        
        readme_content += f"**생성일**: {datetime.now().strftime('%Y-%m-%d')}\n"
        
        readme_path = output_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return readme_path


def generate_integration_scenario(scenario_id: str, output_path: Optional[Path] = None) -> Path:
    """특정 통합 시나리오 문서 생성
    
    Args:
        scenario_id: 시나리오 ID (예: 'netflix_streaming')
        output_path: 출력 파일 경로 (None이면 자동 생성)
    
    Returns:
        생성된 파일 경로
    """
    generator = IntegrationScenarioGenerator()
    
    # 시나리오 찾기
    scenario = None
    for s in generator.scenarios:
        if s.scenario_id == scenario_id:
            scenario = s
            break
    
    if scenario is None:
        raise ValueError(f"Scenario not found: {scenario_id}")
    
    return generator.save_scenario_document(scenario, output_path)


def generate_all_integration_scenarios(output_dir: Optional[Path] = None) -> List[Path]:
    """모든 통합 시나리오 문서 생성
    
    Args:
        output_dir: 출력 디렉토리 (None이면 기본 경로 사용)
    
    Returns:
        생성된 파일 경로 리스트
    """
    generator = IntegrationScenarioGenerator()
    return generator.generate_all_scenarios(output_dir)
