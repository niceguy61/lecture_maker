# Tests for Cross-Service Integration Mapper
"""
서비스 의존성 매핑 시스템 테스트
"""

import pytest
from src.cross_service_integration import (
    CrossServiceIntegrationMapper,
    ServiceDependency,
    IntegrationScenario,
    ServiceConnectionMap,
    get_service_dependency_mapper,
    generate_cross_day_integration_data,
    generate_all_integration_scenarios,
    get_service_dependency_graph
)
from src.models import CrossDayConnection, ServiceIntegration


class TestCrossServiceIntegrationMapper:
    """CrossServiceIntegrationMapper 테스트"""
    
    def test_mapper_initialization(self):
        """매퍼 초기화 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        assert mapper.daily_topics is not None
        assert len(mapper.daily_topics) == 28
        assert len(mapper.service_to_days) > 0
        assert len(mapper.day_to_services) == 28
    
    def test_service_to_days_mapping(self):
        """서비스-일차 매핑 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # CloudFront는 Day 1과 Day 16에서 사용됨
        assert "CloudFront" in mapper.service_to_days
        cloudfront_days = mapper.service_to_days["CloudFront"]
        assert 1 in cloudfront_days
        assert 16 in cloudfront_days
    
    def test_day_to_services_mapping(self):
        """일차-서비스 매핑 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # Day 1의 서비스 확인
        day1_services = mapper.day_to_services[1]
        assert "Regions" in day1_services
        assert "CloudFront" in day1_services
    
    def test_get_service_dependencies(self):
        """서비스 의존성 조회 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # Day 1의 의존성 조회
        dependencies = mapper.get_service_dependencies(1)
        
        assert len(dependencies) > 0
        assert all(isinstance(dep, ServiceDependency) for dep in dependencies)
        
        # 첫 번째 의존성 검증
        first_dep = dependencies[0]
        assert first_dep.service_name in mapper.day_to_services[1]
        assert isinstance(first_dep.dependent_services, list)
        assert first_dep.dependency_type in ["prerequisite", "integration", "enhancement"]
    
    def test_get_cross_day_connections(self):
        """크로스 데이 연결 조회 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # Day 1의 크로스 데이 연결 조회
        connections = mapper.get_cross_day_connections(1)
        
        assert len(connections) > 0
        assert all(isinstance(conn, CrossDayConnection) for conn in connections)
        
        # 연결 정보 검증
        for conn in connections:
            assert conn.day_number in range(1, 29)
            assert conn.service_name != ""
            assert conn.connection_type in ["prerequisite", "enhancement", "alternative"]
            assert conn.description != ""
    
    def test_connection_type_determination(self):
        """연결 타입 결정 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # Day 3의 연결 (Day 4는 enhancement, Day 5는 integration)
        connections = mapper.get_cross_day_connections(3)
        
        # 이후 일차는 enhancement
        enhancement_conns = [c for c in connections if c.connection_type == "enhancement"]
        assert len(enhancement_conns) > 0
    
    def test_get_service_integration_patterns(self):
        """서비스 통합 패턴 조회 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # Day 1의 통합 패턴 조회
        integrations = mapper.get_service_integration_patterns(1)
        
        assert len(integrations) > 0
        assert all(isinstance(integ, ServiceIntegration) for integ in integrations)
        
        # 통합 정보 검증
        for integ in integrations:
            assert integ.primary_service != ""
            assert integ.integrated_service != ""
            assert integ.integration_pattern != ""
            assert integ.data_flow != ""
            assert len(integ.benefits) > 0
    
    def test_integration_pattern_identification(self):
        """통합 패턴 식별 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # 알려진 패턴 테스트
        pattern1 = mapper._identify_integration_pattern("CloudFront", "S3")
        assert pattern1 == "CDN + Storage"
        
        pattern2 = mapper._identify_integration_pattern("EC2", "ELB")
        assert pattern2 == "Compute + Load Balancing"
        
        # 양방향 테스트
        pattern3 = mapper._identify_integration_pattern("S3", "CloudFront")
        assert pattern3 == "CDN + Storage"
    
    def test_get_all_service_connections(self):
        """모든 서비스 연결 맵 조회 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        connection_maps = mapper.get_all_service_connections()
        
        assert len(connection_maps) == 28
        
        # 각 일차의 연결 맵 검증
        for day, maps in connection_maps.items():
            assert day in range(1, 29)
            assert len(maps) > 0
            assert all(isinstance(m, ServiceConnectionMap) for m in maps)
    
    def test_find_service_dependency_chain(self):
        """서비스 의존성 체인 찾기 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # Day 1에서 Day 16으로의 체인 (CloudFront 연결)
        chain = mapper.find_service_dependency_chain(1, 16)
        
        assert len(chain) > 0
        assert chain[0] == 1
        assert chain[-1] == 16
    
    def test_get_integration_scenarios(self):
        """통합 시나리오 조회 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        scenarios = mapper.get_integration_scenarios()
        
        assert len(scenarios) >= 5
        assert all(isinstance(s, IntegrationScenario) for s in scenarios)
        
        # Netflix 시나리오 검증
        netflix_scenario = next((s for s in scenarios if s.scenario_id == "netflix_streaming"), None)
        assert netflix_scenario is not None
        assert netflix_scenario.name == "Netflix 글로벌 스트리밍 아키텍처"
        assert 1 in netflix_scenario.involved_days
        assert 8 in netflix_scenario.involved_days
        assert 16 in netflix_scenario.involved_days
    
    def test_generate_service_dependency_graph(self):
        """서비스 의존성 그래프 생성 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        graph = mapper.generate_service_dependency_graph()
        
        assert isinstance(graph, dict)
        assert len(graph) > 0
        
        # 각 서비스의 의존성 확인
        for service, dependencies in graph.items():
            assert isinstance(service, str)
            assert isinstance(dependencies, list)
    
    def test_get_service_usage_frequency(self):
        """서비스 사용 빈도 계산 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        frequency = mapper.get_service_usage_frequency()
        
        assert isinstance(frequency, dict)
        assert len(frequency) > 0
        
        # 빈도가 내림차순으로 정렬되어 있는지 확인
        frequencies = list(frequency.values())
        assert frequencies == sorted(frequencies, reverse=True)
    
    def test_find_critical_services(self):
        """핵심 서비스 식별 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        critical_services = mapper.find_critical_services(threshold=2)
        
        assert isinstance(critical_services, list)
        assert len(critical_services) > 0
        
        # 각 핵심 서비스가 최소 2번 이상 사용되는지 확인
        frequency = mapper.get_service_usage_frequency()
        for service in critical_services:
            assert frequency[service] >= 2
    
    def test_get_week_integration_summary(self):
        """주차별 통합 요약 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # Week 1 요약
        week1_summary = mapper.get_week_integration_summary(1)
        
        assert week1_summary["week"] == 1
        assert len(week1_summary["days"]) == 7
        assert len(week1_summary["services"]) > 0
        assert week1_summary["total_connections"] >= 0
        assert week1_summary["unique_connections"] >= 0


class TestHelperFunctions:
    """헬퍼 함수 테스트"""
    
    def test_get_service_dependency_mapper(self):
        """매퍼 인스턴스 반환 테스트"""
        mapper = get_service_dependency_mapper()
        
        assert isinstance(mapper, CrossServiceIntegrationMapper)
        assert mapper.daily_topics is not None
    
    def test_generate_cross_day_integration_data(self):
        """크로스 데이 통합 데이터 생성 테스트"""
        data = generate_cross_day_integration_data(1)
        
        assert data["day"] == 1
        assert "dependencies" in data
        assert "connections" in data
        assert "integrations" in data
        
        assert len(data["dependencies"]) > 0
        assert len(data["connections"]) > 0
        assert len(data["integrations"]) > 0
    
    def test_generate_all_integration_scenarios(self):
        """모든 통합 시나리오 생성 테스트"""
        scenarios = generate_all_integration_scenarios()
        
        assert len(scenarios) >= 5
        assert all(isinstance(s, IntegrationScenario) for s in scenarios)
        
        # 주요 시나리오 ID 확인
        scenario_ids = [s.scenario_id for s in scenarios]
        assert "netflix_streaming" in scenario_ids
        assert "airbnb_security" in scenario_ids
        assert "spotify_scalability" in scenario_ids
    
    def test_get_service_dependency_graph(self):
        """서비스 의존성 그래프 반환 테스트"""
        graph = get_service_dependency_graph()
        
        assert isinstance(graph, dict)
        assert len(graph) > 0


class TestEdgeCases:
    """엣지 케이스 테스트"""
    
    def test_day_without_related_days(self):
        """연관 일차가 없는 경우 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # Day 27과 28은 모든 이전 일차를 참조
        connections = mapper.get_cross_day_connections(27)
        assert len(connections) > 0
    
    def test_service_dependency_chain_same_day(self):
        """같은 일차의 의존성 체인 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        chain = mapper.find_service_dependency_chain(1, 1)
        assert chain == [1]
    
    def test_service_dependency_chain_no_path(self):
        """경로가 없는 의존성 체인 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        # 연결되지 않은 일차 간 체인 (존재하지 않을 수 있음)
        chain = mapper.find_service_dependency_chain(1, 28)
        # 체인이 있거나 없을 수 있음 (빈 리스트 또는 경로)
        assert isinstance(chain, list)
    
    def test_week_integration_summary_all_weeks(self):
        """모든 주차의 통합 요약 테스트"""
        mapper = CrossServiceIntegrationMapper()
        
        for week in range(1, 5):
            summary = mapper.get_week_integration_summary(week)
            assert summary["week"] == week
            assert len(summary["days"]) > 0
            assert len(summary["services"]) > 0


class TestIntegrationScenarios:
    """통합 시나리오 상세 테스트"""
    
    def test_netflix_scenario_details(self):
        """Netflix 시나리오 상세 테스트"""
        scenarios = generate_all_integration_scenarios()
        netflix = next((s for s in scenarios if s.scenario_id == "netflix_streaming"), None)
        
        assert netflix is not None
        assert netflix.primary_day == 1
        assert "CloudFront" in netflix.services
        assert "S3" in netflix.services
        assert netflix.integration_pattern == "CDN + Storage + Global Infrastructure"
    
    def test_airbnb_scenario_details(self):
        """Airbnb 시나리오 상세 테스트"""
        scenarios = generate_all_integration_scenarios()
        airbnb = next((s for s in scenarios if s.scenario_id == "airbnb_security"), None)
        
        assert airbnb is not None
        assert airbnb.primary_day == 2
        assert "IAM" in airbnb.services
        assert "VPC" in airbnb.services
        assert "CloudTrail" in airbnb.services
    
    def test_serverless_scenario_details(self):
        """서버리스 시나리오 상세 테스트"""
        scenarios = generate_all_integration_scenarios()
        serverless = next((s for s in scenarios if s.scenario_id == "serverless_app"), None)
        
        assert serverless is not None
        assert serverless.primary_day == 18
        assert "Lambda" in serverless.services
        assert "API Gateway" in serverless.services
        assert "DynamoDB" in serverless.services


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
