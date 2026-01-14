#!/usr/bin/env python3
"""
Cross-Service Integration Demo Script
서비스 의존성 매핑 시스템 데모
"""

from src.cross_service_integration import (
    get_service_dependency_mapper,
    generate_cross_day_integration_data,
    generate_all_integration_scenarios
)
from src.generators.cross_service_integration_generator import (
    CrossServiceIntegrationContentGenerator,
    generate_cross_service_integration_content,
    generate_all_integration_scenario_documents,
    generate_critical_services_report
)


def demo_service_dependencies():
    """서비스 의존성 데모"""
    print("=" * 80)
    print("서비스 의존성 매핑 데모")
    print("=" * 80)
    
    mapper = get_service_dependency_mapper()
    
    # Day 1의 의존성 조회
    print("\n[Day 1: AWS 개요 및 글로벌 인프라]")
    dependencies = mapper.get_service_dependencies(1)
    
    for dep in dependencies:
        print(f"\n서비스: {dep.service_name}")
        print(f"의존성 타입: {dep.dependency_type}")
        print(f"연계 서비스: {', '.join(dep.dependent_services[:3])}...")


def demo_cross_day_connections():
    """크로스 데이 연결 데모"""
    print("\n" + "=" * 80)
    print("크로스 데이 연결 정보 데모")
    print("=" * 80)
    
    mapper = get_service_dependency_mapper()
    
    # Day 3의 연결 조회
    print("\n[Day 3: EC2 기초]")
    connections = mapper.get_cross_day_connections(3)
    
    print(f"\n총 {len(connections)}개의 연결이 있습니다:")
    for conn in connections[:5]:  # 처음 5개만 표시
        print(f"\n- Day {conn.day_number}: {conn.service_name}")
        print(f"  타입: {conn.connection_type}")
        print(f"  설명: {conn.description}")


def demo_integration_scenarios():
    """통합 시나리오 데모"""
    print("\n" + "=" * 80)
    print("통합 시나리오 데모")
    print("=" * 80)
    
    scenarios = generate_all_integration_scenarios()
    
    print(f"\n총 {len(scenarios)}개의 통합 시나리오:")
    
    for scenario in scenarios:
        print(f"\n{scenario.name}")
        print(f"  ID: {scenario.scenario_id}")
        print(f"  주요 일차: Day {scenario.primary_day}")
        print(f"  관련 일차: {scenario.involved_days}")
        print(f"  서비스: {', '.join(scenario.services)}")
        print(f"  패턴: {scenario.integration_pattern}")


def demo_service_usage_frequency():
    """서비스 사용 빈도 데모"""
    print("\n" + "=" * 80)
    print("서비스 사용 빈도 분석")
    print("=" * 80)
    
    mapper = get_service_dependency_mapper()
    frequency = mapper.get_service_usage_frequency()
    
    print("\n상위 10개 서비스:")
    for i, (service, count) in enumerate(list(frequency.items())[:10], 1):
        print(f"{i}. {service}: {count}회")


def demo_critical_services():
    """핵심 서비스 데모"""
    print("\n" + "=" * 80)
    print("핵심 서비스 식별")
    print("=" * 80)
    
    mapper = get_service_dependency_mapper()
    critical = mapper.find_critical_services(threshold=2)
    
    print(f"\n{len(critical)}개의 핵심 서비스 (2회 이상 사용):")
    for service in critical[:10]:
        days = mapper.service_to_days[service]
        print(f"- {service}: Day {', '.join(map(str, days))}")


def demo_content_generation():
    """콘텐츠 생성 데모"""
    print("\n" + "=" * 80)
    print("콘텐츠 생성 데모")
    print("=" * 80)
    
    # Day 1의 통합 콘텐츠 생성
    print("\n[Day 1 크로스 서비스 통합 콘텐츠]")
    content = generate_cross_service_integration_content(1)
    
    print("\n--- 서비스 의존성 섹션 ---")
    print(content["dependencies"][:500] + "...")
    
    print("\n--- 크로스 데이 연결 섹션 ---")
    print(content["connections"][:500] + "...")


def demo_integration_scenario_document():
    """통합 시나리오 문서 생성 데모"""
    print("\n" + "=" * 80)
    print("통합 시나리오 문서 생성 데모")
    print("=" * 80)
    
    documents = generate_all_integration_scenario_documents()
    
    # Netflix 시나리오 문서 일부 표시
    netflix_doc = documents.get("netflix_streaming", "")
    print("\n[Netflix 글로벌 스트리밍 시나리오 문서 (일부)]")
    print(netflix_doc[:800] + "...")


def demo_week_integration_summary():
    """주차별 통합 요약 데모"""
    print("\n" + "=" * 80)
    print("주차별 통합 요약 데모")
    print("=" * 80)
    
    mapper = get_service_dependency_mapper()
    
    for week in range(1, 5):
        summary = mapper.get_week_integration_summary(week)
        print(f"\nWeek {week}:")
        print(f"  일차: {summary['days']}")
        print(f"  서비스 수: {len(summary['services'])}")
        print(f"  총 연결: {summary['total_connections']}")
        print(f"  고유 연결: {summary['unique_connections']}")


def demo_critical_services_report():
    """핵심 서비스 리포트 데모"""
    print("\n" + "=" * 80)
    print("핵심 서비스 리포트 생성 데모")
    print("=" * 80)
    
    report = generate_critical_services_report()
    print("\n[핵심 서비스 리포트 (일부)]")
    print(report[:1000] + "...")


def main():
    """메인 데모 실행"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "크로스 서비스 통합 시스템 데모" + " " * 27 + "║")
    print("║" + " " * 15 + "Service Dependency Mapping System Demo" + " " * 24 + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        demo_service_dependencies()
        demo_cross_day_connections()
        demo_integration_scenarios()
        demo_service_usage_frequency()
        demo_critical_services()
        demo_content_generation()
        demo_integration_scenario_document()
        demo_week_integration_summary()
        demo_critical_services_report()
        
        print("\n" + "=" * 80)
        print("데모 완료!")
        print("=" * 80)
        print("\n모든 기능이 정상적으로 작동합니다.")
        print("Task 8.1 (서비스 의존성 매핑 시스템) 구현 완료!\n")
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
