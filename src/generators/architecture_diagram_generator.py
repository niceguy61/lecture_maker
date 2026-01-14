# Architecture Diagram Generator
"""
아키텍처 다이어그램 생성기
각 일별(Day 1-28) 주요 서비스 중심 아키텍처 다이어그램 생성
서비스 간 연결 및 데이터 플로우 시각화
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from src.daily_topics import DAILY_TOPICS, get_topic_by_day, get_related_topics
from src.models import MermaidDiagram
from src.config import STUDY_MATERIALS_ROOT, MERMAID_DIAGRAM_TYPES


class ArchitectureDiagramGenerator:
    """아키텍처 다이어그램 생성기"""
    
    def __init__(self):
        self.output_base_path = STUDY_MATERIALS_ROOT
        
    def get_daily_config(self, day_number: int) -> Dict:
        """일별 주제 설정 가져오기"""
        return get_topic_by_day(day_number)
    
    def generate_main_architecture_diagram(self, day_number: int) -> str:
        """메인 아키텍처 다이어그램 생성
        
        주요 서비스 중심의 전체 아키텍처를 시각화
        """
        config = self.get_daily_config(day_number)
        services = config["primary_services"]
        company = config["case_study_company"]
        
        diagram = f"""```mermaid
graph TB
    subgraph "사용자 계층"
        Users[👥 사용자/클라이언트]
    end
    
    subgraph "AWS 클라우드 - {company}"
        subgraph "리전: ap-northeast-2 (서울)"
"""
        
        # 주요 서비스 노드 생성
        if services:
            primary_service = services[0]
            diagram += f"            Primary[🎯 {primary_service}]\n"
            
            # 추가 서비스들
            for i, service in enumerate(services[1:4], start=1):
                diagram += f"            Service{i}[⚙️ {service}]\n"
        
        diagram += "        end\n"
        
        # 모니터링 및 보안 계층
        diagram += """        
        subgraph "관리 및 보안"
            Monitor[📊 CloudWatch]
            Security[🔒 IAM]
        end
    end
    
"""
        
        # 연결 관계 정의
        diagram += "    Users -->|요청| Primary\n"
        
        for i in range(1, min(4, len(services))):
            diagram += f"    Primary -->|데이터 처리| Service{i}\n"
        
        diagram += """    Primary -.->|모니터링| Monitor
    Primary -.->|인증/권한| Security
```
"""
        
        return diagram
    
    def generate_data_flow_diagram(self, day_number: int) -> str:
        """데이터 플로우 다이어그램 생성
        
        서비스 간 데이터 흐름을 시퀀스 다이어그램으로 시각화
        """
        config = self.get_daily_config(day_number)
        services = config["primary_services"]
        
        if not services:
            return ""
        
        primary_service = services[0]
        storage_service = next((s for s in services if any(x in s for x in ["S3", "RDS", "DynamoDB", "EBS"])), "데이터 저장소")
        
        diagram = f"""```mermaid
sequenceDiagram
    participant User as 👤 사용자
    participant Primary as {primary_service}
    participant Storage as {storage_service}
    participant Monitor as CloudWatch
    
    User->>Primary: 1. 요청 전송
    activate Primary
    
    Primary->>Storage: 2. 데이터 조회/저장
    activate Storage
    Storage-->>Primary: 3. 데이터 응답
    deactivate Storage
    
    Primary->>Monitor: 4. 메트릭 전송
    
    Primary-->>User: 5. 처리 결과 반환
    deactivate Primary
    
    Note over User,Monitor: 전체 처리 시간: < 100ms
```
"""
        
        return diagram

    
    def generate_cross_day_integration_diagram(self, day_number: int) -> str:
        """크로스 데이 통합 다이어그램 생성 (기본)
        
        현재 일차와 관련된 다른 일차들의 서비스 연계를 시각화
        """
        config = self.get_daily_config(day_number)
        related_days = config.get("related_days", [])[:4]  # 최대 4개
        
        diagram = f"""```mermaid
graph LR
    Current[Day {day_number}<br/>{config['title']}]
    
"""
        
        # 관련 일차 노드 생성
        for related_day in related_days:
            try:
                related_config = get_topic_by_day(related_day)
                diagram += f"    Day{related_day}[Day {related_day}<br/>{related_config['title']}]\n"
            except ValueError:
                continue
        
        diagram += "\n"
        
        # 연결 관계 정의
        for related_day in related_days:
            if related_day < day_number:
                # 이전 일차는 선행 학습
                diagram += f"    Day{related_day} -->|선행 학습| Current\n"
            else:
                # 이후 일차는 확장 학습
                diagram += f"    Current -.->|확장 학습| Day{related_day}\n"
        
        diagram += "```\n"
        
        return diagram
    
    def generate_multi_day_integration_scenario(self, day_number: int) -> str:
        """멀티 데이 통합 시나리오 다이어그램 생성
        
        여러 일차의 서비스들이 실제로 어떻게 통합되어 작동하는지 시각화
        예: Netflix 글로벌 스트리밍 (Day 1 + Day 8 + Day 16)
        """
        config = self.get_daily_config(day_number)
        company = config["case_study_company"]
        related_days = config.get("related_days", [])
        
        if not related_days:
            return ""
        
        # 주요 통합 시나리오 정의
        diagram = f"""```mermaid
graph TB
    subgraph "사용자 요청 플로우"
        User[👤 사용자]
    end
    
    subgraph "Day {day_number}: {config['title']}"
"""
        
        # 현재 일차의 주요 서비스
        for i, service in enumerate(config["primary_services"][:2]):
            diagram += f"        D{day_number}_S{i+1}[{service}]\n"
        
        diagram += "    end\n\n"
        
        # 관련 일차들의 서비스 통합
        for idx, related_day in enumerate(related_days[:3]):
            try:
                related_config = get_topic_by_day(related_day)
                diagram += f"""    subgraph "Day {related_day}: {related_config['title']}"
"""
                for i, service in enumerate(related_config["primary_services"][:2]):
                    diagram += f"        D{related_day}_S{i+1}[{service}]\n"
                diagram += "    end\n\n"
            except ValueError:
                continue
        
        # 통합 사례 설명
        diagram += f"""    subgraph "통합 사례: {company}"
        Integration[🎯 End-to-End<br/>통합 아키텍처]
    end
    
"""
        
        # 데이터 플로우 연결
        diagram += f"    User -->|1. 요청| D{day_number}_S1\n"
        
        if related_days:
            first_related = related_days[0]
            diagram += f"    D{day_number}_S1 -->|2. 데이터 처리| D{first_related}_S1\n"
            
            if len(related_days) > 1:
                second_related = related_days[1]
                diagram += f"    D{first_related}_S1 -->|3. 저장/전송| D{second_related}_S1\n"
                diagram += f"    D{second_related}_S1 -->|4. 응답| D{day_number}_S1\n"
            else:
                diagram += f"    D{first_related}_S1 -->|3. 응답| D{day_number}_S1\n"
        
        diagram += f"    D{day_number}_S1 -->|5. 결과 반환| User\n"
        diagram += f"    D{day_number}_S1 -.->|모니터링| Integration\n"
        
        diagram += "```\n"
        
        return diagram
    
    def generate_architecture_evolution_diagram(self, day_number: int) -> str:
        """아키텍처 진화 경로 다이어그램 생성
        
        기본 구성 → 중급 구성 → 고급 구성으로의 진화 과정 시각화
        """
        config = self.get_daily_config(day_number)
        related_days = config.get("related_days", [])
        
        if not related_days:
            return ""
        
        diagram = f"""```mermaid
graph LR
    subgraph "Stage 1: 기본 구성"
        S1_Title[Day {day_number}<br/>{config['title']}]
        S1_Services["{', '.join(config['primary_services'][:2])}"]
        S1_Title --> S1_Services
    end
    
"""
        
        # Stage 2: 중급 구성 (첫 번째 관련 일차 추가)
        if len(related_days) >= 1:
            first_related = related_days[0]
            try:
                first_config = get_topic_by_day(first_related)
                diagram += f"""    subgraph "Stage 2: 서비스 확장"
        S2_Base[Day {day_number} +<br/>Day {first_related}]
        S2_Services["{', '.join(config['primary_services'][:1] + first_config['primary_services'][:1])}"]
        S2_Base --> S2_Services
    end
    
"""
            except ValueError:
                pass
        
        # Stage 3: 고급 구성 (두 번째 관련 일차 추가)
        if len(related_days) >= 2:
            second_related = related_days[1]
            try:
                second_config = get_topic_by_day(second_related)
                all_services = (
                    config['primary_services'][:1] + 
                    [get_topic_by_day(related_days[0])['primary_services'][0]] +
                    second_config['primary_services'][:1]
                )
                diagram += f"""    subgraph "Stage 3: 완전한 통합"
        S3_Base[Day {day_number} +<br/>Day {related_days[0]} +<br/>Day {second_related}]
        S3_Services["{', '.join(all_services)}"]
        S3_Base --> S3_Services
    end
    
"""
            except ValueError:
                pass
        
        # 진화 경로 연결
        diagram += "    S1_Services ==>|확장| S2_Services\n"
        if len(related_days) >= 2:
            diagram += "    S2_Services ==>|최적화| S3_Services\n"
        
        # 스타일 적용
        diagram += """
    style S1_Services fill:#E8F5E9
    style S2_Services fill:#FFF9C4
    style S3_Services fill:#E1F5FE
```
"""
        
        return diagram
    
    def generate_end_to_end_flow_diagram(self, day_number: int) -> str:
        """End-to-End 플로우 다이어그램 생성
        
        사용자 요청이 여러 일차의 서비스를 거쳐 처리되는 전체 흐름 시각화
        """
        config = self.get_daily_config(day_number)
        related_days = config.get("related_days", [])
        
        if not related_days:
            return ""
        
        diagram = f"""```mermaid
sequenceDiagram
    participant User as 👤 사용자
    participant D{day_number} as Day {day_number}<br/>{config['primary_services'][0] if config['primary_services'] else 'Service'}
"""
        
        # 관련 일차 참여자 추가
        for related_day in related_days[:3]:
            try:
                related_config = get_topic_by_day(related_day)
                service_name = related_config['primary_services'][0] if related_config['primary_services'] else 'Service'
                diagram += f"    participant D{related_day} as Day {related_day}<br/>{service_name}\n"
            except ValueError:
                continue
        
        diagram += "    participant Monitor as 📊 모니터링\n\n"
        
        # 요청 플로우
        diagram += f"    User->>D{day_number}: 1. 초기 요청\n"
        diagram += f"    activate D{day_number}\n\n"
        
        # 관련 서비스 호출 체인
        for idx, related_day in enumerate(related_days[:3], start=2):
            diagram += f"    D{day_number}->>D{related_day}: {idx}. 데이터 처리 요청\n"
            diagram += f"    activate D{related_day}\n"
            diagram += f"    D{related_day}-->>D{day_number}: {idx+1}. 처리 결과\n"
            diagram += f"    deactivate D{related_day}\n\n"
        
        # 모니터링 및 응답
        diagram += f"    D{day_number}->>Monitor: 메트릭 전송\n"
        diagram += f"    D{day_number}-->>User: 최종 응답\n"
        diagram += f"    deactivate D{day_number}\n\n"
        
        # 노트 추가
        total_steps = 2 + len(related_days[:3]) * 2
        diagram += f"    Note over User,Monitor: 총 {total_steps}단계 처리<br/>여러 일차 서비스 통합\n"
        
        diagram += "```\n"
        
        return diagram
    
    def generate_multi_region_architecture(self, day_number: int) -> str:
        """멀티 리전 아키텍처 다이어그램 생성
        
        글로벌 서비스를 위한 멀티 리전 구성 시각화
        """
        config = self.get_daily_config(day_number)
        services = config["primary_services"]
        
        # 글로벌 서비스가 포함된 경우에만 생성
        global_services = ["CloudFront", "Route53", "Global Accelerator"]
        has_global = any(gs in str(services) for gs in global_services)
        
        if not has_global:
            return ""
        
        diagram = f"""```mermaid
graph TB
    subgraph "글로벌 계층"
        Users[🌍 글로벌 사용자]
        CDN[CloudFront CDN]
        DNS[Route53 DNS]
    end
    
    subgraph "리전: us-east-1 (버지니아)"
        US_Primary[{services[0] if services else 'Primary Service'}]
        US_DB[(데이터베이스)]
    end
    
    subgraph "리전: ap-northeast-2 (서울)"
        AP_Primary[{services[0] if services else 'Primary Service'}]
        AP_DB[(데이터베이스)]
    end
    
    subgraph "리전: eu-west-1 (아일랜드)"
        EU_Primary[{services[0] if services else 'Primary Service'}]
        EU_DB[(데이터베이스)]
    end
    
    Users --> DNS
    DNS --> CDN
    CDN --> US_Primary
    CDN --> AP_Primary
    CDN --> EU_Primary
    
    US_Primary --> US_DB
    AP_Primary --> AP_DB
    EU_Primary --> EU_DB
    
    US_DB -.->|복제| AP_DB
    AP_DB -.->|복제| EU_DB
```
"""
        
        return diagram
    
    def generate_high_availability_architecture(self, day_number: int) -> str:
        """고가용성 아키텍처 다이어그램 생성
        
        Multi-AZ 구성 및 장애 조치 메커니즘 시각화
        """
        config = self.get_daily_config(day_number)
        services = config["primary_services"]
        
        if not services:
            return ""
        
        primary_service = services[0]
        
        diagram = f"""```mermaid
graph TB
    subgraph "사용자"
        Users[👥 사용자]
    end
    
    subgraph "로드 밸런싱"
        ELB[Elastic Load Balancer]
    end
    
    subgraph "가용 영역 A"
        AZ_A_App[{primary_service}]
        AZ_A_DB[(Primary DB)]
    end
    
    subgraph "가용 영역 B"
        AZ_B_App[{primary_service}]
        AZ_B_DB[(Standby DB)]
    end
    
    subgraph "가용 영역 C"
        AZ_C_App[{primary_service}]
    end
    
    Users --> ELB
    ELB --> AZ_A_App
    ELB --> AZ_B_App
    ELB --> AZ_C_App
    
    AZ_A_App --> AZ_A_DB
    AZ_B_App --> AZ_A_DB
    AZ_C_App --> AZ_A_DB
    
    AZ_A_DB -.->|동기 복제| AZ_B_DB
    
    style AZ_A_DB fill:#90EE90
    style AZ_B_DB fill:#FFB6C1
```
"""
        
        return diagram
    
    def save_diagram(self, day_number: int, diagram_type: str, content: str) -> Path:
        """다이어그램 파일 저장
        
        Args:
            day_number: 일차 번호
            diagram_type: 다이어그램 유형 (main-architecture, data-flow, etc.)
            content: 다이어그램 콘텐츠
            
        Returns:
            저장된 파일 경로
        """
        config = self.get_daily_config(day_number)
        week_number = config["week"]
        
        output_dir = (
            self.output_base_path / 
            f"week{week_number}" / 
            f"day{day_number}" / 
            "advanced" / 
            "architecture-diagrams"
        )
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"day{day_number}-{diagram_type}.mmd"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
    
    def generate_diagrams_for_day(self, day_number: int) -> Dict[str, Path]:
        """특정 일차의 모든 다이어그램 생성
        
        Args:
            day_number: 일차 번호 (1-28)
            
        Returns:
            다이어그램 유형별 파일 경로 딕셔너리
        """
        results = {}
        
        # 1. 메인 아키텍처 다이어그램 (필수)
        main_diagram = self.generate_main_architecture_diagram(day_number)
        results["main-architecture"] = self.save_diagram(day_number, "main-architecture", main_diagram)
        
        # 2. 데이터 플로우 다이어그램 (필수)
        data_flow = self.generate_data_flow_diagram(day_number)
        if data_flow:
            results["data-flow"] = self.save_diagram(day_number, "data-flow", data_flow)
        
        # 3. 크로스 데이 통합 다이어그램 - 기본 (필수)
        cross_day = self.generate_cross_day_integration_diagram(day_number)
        if cross_day:
            results["cross-day-integration"] = self.save_diagram(day_number, "cross-day-integration", cross_day)
        
        # 4. 멀티 데이 통합 시나리오 (Task 6.3 - 새로 추가)
        multi_day_scenario = self.generate_multi_day_integration_scenario(day_number)
        if multi_day_scenario:
            results["multi-day-integration-scenario"] = self.save_diagram(day_number, "multi-day-integration-scenario", multi_day_scenario)
        
        # 5. 아키텍처 진화 경로 (Task 6.3 - 새로 추가)
        evolution_path = self.generate_architecture_evolution_diagram(day_number)
        if evolution_path:
            results["architecture-evolution"] = self.save_diagram(day_number, "architecture-evolution", evolution_path)
        
        # 6. End-to-End 플로우 (Task 6.3 - 새로 추가)
        e2e_flow = self.generate_end_to_end_flow_diagram(day_number)
        if e2e_flow:
            results["end-to-end-flow"] = self.save_diagram(day_number, "end-to-end-flow", e2e_flow)
        
        # 7. 멀티 리전 아키텍처 (선택적)
        multi_region = self.generate_multi_region_architecture(day_number)
        if multi_region:
            results["multi-region"] = self.save_diagram(day_number, "multi-region", multi_region)
        
        # 8. 고가용성 아키텍처 (선택적)
        ha_architecture = self.generate_high_availability_architecture(day_number)
        if ha_architecture:
            results["high-availability"] = self.save_diagram(day_number, "high-availability", ha_architecture)
        
        print(f"✓ Generated {len(results)} diagrams for Day {day_number}")
        
        return results
    
    def generate_all_diagrams(self, start_day: int = 1, end_day: int = 28) -> Dict[int, Dict[str, Path]]:
        """모든 일차의 아키텍처 다이어그램 생성
        
        Args:
            start_day: 시작 일차 (기본값: 1)
            end_day: 종료 일차 (기본값: 28)
            
        Returns:
            일차별 다이어그램 파일 경로 딕셔너리
        """
        results = {}
        
        print(f"\n{'='*60}")
        print(f"Architecture Diagram Generator - Days {start_day} to {end_day}")
        print(f"{'='*60}\n")
        
        for day in range(start_day, end_day + 1):
            try:
                results[day] = self.generate_diagrams_for_day(day)
            except Exception as e:
                print(f"✗ Error generating diagrams for Day {day}: {e}")
                results[day] = {"error": str(e)}
        
        total_diagrams = sum(len(v) for v in results.values() if isinstance(v, dict) and "error" not in v)
        print(f"\n{'='*60}")
        print(f"Generation Complete!")
        print(f"Total diagrams generated: {total_diagrams}")
        print(f"{'='*60}\n")
        
        return results


# CLI 실행을 위한 메인 함수
def main():
    """CLI 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS SAA Architecture Diagram Generator")
    parser.add_argument(
        "--day",
        type=int,
        help="Generate diagrams for specific day (1-28)"
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
    
    args = parser.parse_args()
    
    generator = ArchitectureDiagramGenerator()
    
    if args.day:
        # 단일 일차 생성
        results = generator.generate_diagrams_for_day(args.day)
        print(f"\nGenerated diagrams:")
        for diagram_type, path in results.items():
            print(f"  - {diagram_type}: {path}")
    else:
        # 배치 생성
        generator.generate_all_diagrams(args.start, args.end)


if __name__ == "__main__":
    main()
