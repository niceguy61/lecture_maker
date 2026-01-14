# Cross-Service Integration and Dependency Mapping
"""
서비스 의존성 매핑 시스템 (Task 8.1)
Day 1-28 간 서비스 의존성 및 통합 패턴 매핑
크로스 데이 서비스 연결 정보 생성
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from src.daily_topics import DAILY_TOPICS, DailyTopicConfig
from src.models import ServiceIntegration, CrossDayConnection


@dataclass
class ServiceDependency:
    """서비스 의존성 정보"""
    service_name: str
    dependent_services: List[str] = field(default_factory=list)
    dependency_type: str = "integration"  # 'prerequisite', 'integration', 'enhancement'
    description: str = ""


@dataclass
class IntegrationScenario:
    """통합 시나리오"""
    scenario_id: str
    name: str
    description: str
    involved_days: List[int]
    primary_day: int
    services: List[str]
    integration_pattern: str
    use_case: str


@dataclass
class ServiceConnectionMap:
    """서비스 연결 맵"""
    day_number: int
    service_name: str
    connections: List[CrossDayConnection] = field(default_factory=list)
    integration_patterns: List[str] = field(default_factory=list)


class CrossServiceIntegrationMapper:
    """크로스 서비스 통합 매퍼"""
    
    def __init__(self):
        self.daily_topics = DAILY_TOPICS
        self.service_to_days: Dict[str, List[int]] = {}
        self.day_to_services: Dict[int, List[str]] = {}
        self._build_service_mappings()
    
    def _build_service_mappings(self):
        """서비스와 일차 간 매핑 구축"""
        for day, topic in self.daily_topics.items():
            services = topic["primary_services"]
            self.day_to_services[day] = services
            
            for service in services:
                if service not in self.service_to_days:
                    self.service_to_days[service] = []
                self.service_to_days[service].append(day)
    
    def get_service_dependencies(self, day: int) -> List[ServiceDependency]:
        """특정 일차의 서비스 의존성 반환"""
        topic = self.daily_topics[day]
        services = topic["primary_services"]
        related_days = topic["related_days"]
        
        dependencies = []
        for service in services:
            dependent_services = []
            
            # 연관된 일차의 서비스들을 의존성으로 추가
            for related_day in related_days:
                if related_day in self.daily_topics:
                    related_services = self.daily_topics[related_day]["primary_services"]
                    dependent_services.extend(related_services)
            
            # 의존성 타입 결정
            dependency_type = self._determine_dependency_type(day, related_days)
            
            dependencies.append(ServiceDependency(
                service_name=service,
                dependent_services=list(set(dependent_services)),
                dependency_type=dependency_type,
                description=f"{service}와 연계되는 서비스들"
            ))
        
        return dependencies
    
    def _determine_dependency_type(self, day: int, related_days: List[int]) -> str:
        """의존성 타입 결정"""
        # 이전 일차는 prerequisite, 이후 일차는 enhancement
        if any(d < day for d in related_days):
            return "prerequisite"
        elif any(d > day for d in related_days):
            return "enhancement"
        return "integration"
    
    def get_cross_day_connections(self, day: int) -> List[CrossDayConnection]:
        """특정 일차의 크로스 데이 연결 정보 생성"""
        topic = self.daily_topics[day]
        related_days = topic["related_days"]
        connections = []
        
        for related_day in related_days:
            if related_day not in self.daily_topics:
                continue
            
            related_topic = self.daily_topics[related_day]
            connection_type = self._get_connection_type(day, related_day)
            
            for service in related_topic["primary_services"]:
                connections.append(CrossDayConnection(
                    day_number=related_day,
                    service_name=service,
                    connection_type=connection_type,
                    description=self._generate_connection_description(
                        day, related_day, service, connection_type
                    )
                ))
        
        return connections
    
    def _get_connection_type(self, current_day: int, related_day: int) -> str:
        """연결 타입 결정"""
        if related_day < current_day:
            return "prerequisite"
        elif related_day > current_day:
            return "enhancement"
        return "alternative"
    
    def _generate_connection_description(
        self, 
        current_day: int, 
        related_day: int, 
        service: str,
        connection_type: str
    ) -> str:
        """연결 설명 생성"""
        current_topic = self.daily_topics[current_day]
        related_topic = self.daily_topics[related_day]
        
        if connection_type == "prerequisite":
            return f"Day {related_day}의 {service}는 {current_topic['title']}의 기반이 됩니다"
        elif connection_type == "enhancement":
            return f"Day {related_day}의 {service}로 {current_topic['title']}을 확장할 수 있습니다"
        else:
            return f"Day {related_day}의 {service}는 대안적인 접근 방법을 제공합니다"
    
    def get_service_integration_patterns(self, day: int) -> List[ServiceIntegration]:
        """서비스 통합 패턴 생성"""
        topic = self.daily_topics[day]
        primary_services = topic["primary_services"]
        related_days = topic["related_days"]
        
        integrations = []
        
        for primary_service in primary_services:
            for related_day in related_days:
                if related_day not in self.daily_topics:
                    continue
                
                related_services = self.daily_topics[related_day]["primary_services"]
                
                for related_service in related_services:
                    integration = self._create_service_integration(
                        primary_service,
                        related_service,
                        day,
                        related_day
                    )
                    integrations.append(integration)
        
        return integrations
    
    def _create_service_integration(
        self,
        primary_service: str,
        integrated_service: str,
        primary_day: int,
        integrated_day: int
    ) -> ServiceIntegration:
        """서비스 통합 정보 생성"""
        pattern = self._identify_integration_pattern(primary_service, integrated_service)
        data_flow = self._describe_data_flow(primary_service, integrated_service)
        benefits = self._list_integration_benefits(primary_service, integrated_service)
        
        return ServiceIntegration(
            primary_service=primary_service,
            integrated_service=integrated_service,
            integration_pattern=pattern,
            data_flow=data_flow,
            benefits=benefits
        )
    
    def _identify_integration_pattern(self, service1: str, service2: str) -> str:
        """통합 패턴 식별"""
        # 일반적인 AWS 서비스 통합 패턴
        patterns = {
            ("CloudFront", "S3"): "CDN + Storage",
            ("EC2", "ELB"): "Compute + Load Balancing",
            ("Lambda", "DynamoDB"): "Serverless + NoSQL",
            ("API Gateway", "Lambda"): "API + Serverless",
            ("RDS", "VPC"): "Database + Network Isolation",
            ("IAM", "S3"): "Access Control + Storage",
        }
        
        # 양방향 검색
        key1 = (service1, service2)
        key2 = (service2, service1)
        
        if key1 in patterns:
            return patterns[key1]
        elif key2 in patterns:
            return patterns[key2]
        
        return f"{service1} + {service2} Integration"
    
    def _describe_data_flow(self, service1: str, service2: str) -> str:
        """데이터 플로우 설명"""
        return f"{service1} → {service2}: 데이터 전송 및 처리"
    
    def _list_integration_benefits(self, service1: str, service2: str) -> List[str]:
        """통합 이점 나열"""
        return [
            f"{service1}과 {service2}의 시너지 효과",
            "확장성 및 성능 향상",
            "운영 효율성 개선"
        ]
    
    def get_all_service_connections(self) -> Dict[int, ServiceConnectionMap]:
        """모든 일차의 서비스 연결 맵 생성"""
        connection_maps = {}
        
        for day in range(1, 29):
            topic = self.daily_topics[day]
            
            for service in topic["primary_services"]:
                connections = self.get_cross_day_connections(day)
                integrations = self.get_service_integration_patterns(day)
                
                connection_map = ServiceConnectionMap(
                    day_number=day,
                    service_name=service,
                    connections=connections,
                    integration_patterns=[i.integration_pattern for i in integrations]
                )
                
                if day not in connection_maps:
                    connection_maps[day] = []
                connection_maps[day].append(connection_map)
        
        return connection_maps
    
    def find_service_dependency_chain(self, start_day: int, end_day: int) -> List[int]:
        """서비스 의존성 체인 찾기"""
        if start_day == end_day:
            return [start_day]
        
        visited = set()
        path = []
        
        def dfs(current_day: int, target_day: int) -> bool:
            if current_day == target_day:
                path.append(current_day)
                return True
            
            if current_day in visited:
                return False
            
            visited.add(current_day)
            path.append(current_day)
            
            topic = self.daily_topics.get(current_day)
            if not topic:
                path.pop()
                return False
            
            for related_day in topic["related_days"]:
                if dfs(related_day, target_day):
                    return True
            
            path.pop()
            return False
        
        if dfs(start_day, end_day):
            return path
        return []
    
    def get_integration_scenarios(self) -> List[IntegrationScenario]:
        """주요 통합 시나리오 생성"""
        scenarios = []
        
        # Netflix 글로벌 스트리밍 시나리오
        scenarios.append(IntegrationScenario(
            scenario_id="netflix_streaming",
            name="Netflix 글로벌 스트리밍 아키텍처",
            description="멀티 리전 콘텐츠 배포 및 스트리밍",
            involved_days=[1, 8, 16],
            primary_day=1,
            services=["CloudFront", "S3", "Regions"],
            integration_pattern="CDN + Storage + Global Infrastructure",
            use_case="대규모 비디오 스트리밍 서비스"
        ))
        
        # Airbnb 보안 아키텍처 시나리오
        scenarios.append(IntegrationScenario(
            scenario_id="airbnb_security",
            name="Airbnb IAM 보안 아키텍처",
            description="대규모 조직의 보안 및 규정 준수",
            involved_days=[2, 5, 23],
            primary_day=2,
            services=["IAM", "VPC", "CloudTrail"],
            integration_pattern="Identity + Network + Audit",
            use_case="엔터프라이즈 보안 관리"
        ))
        
        # Spotify 확장성 시나리오
        scenarios.append(IntegrationScenario(
            scenario_id="spotify_scalability",
            name="Spotify 확장 가능한 컴퓨팅",
            description="음악 스트리밍을 위한 Auto Scaling 아키텍처",
            involved_days=[3, 4, 13],
            primary_day=3,
            services=["EC2", "Auto Scaling", "ELB"],
            integration_pattern="Compute + Scaling + Load Balancing",
            use_case="고가용성 웹 애플리케이션"
        ))
        
        # Dropbox 스토리지 시나리오
        scenarios.append(IntegrationScenario(
            scenario_id="dropbox_storage",
            name="Dropbox 페타바이트급 스토리지",
            description="대규모 파일 스토리지 및 CDN 통합",
            involved_days=[8, 16, 18],
            primary_day=8,
            services=["S3", "CloudFront", "Lambda"],
            integration_pattern="Storage + CDN + Serverless",
            use_case="파일 공유 및 동기화 서비스"
        ))
        
        # Serverless 애플리케이션 시나리오
        scenarios.append(IntegrationScenario(
            scenario_id="serverless_app",
            name="서버리스 애플리케이션 아키텍처",
            description="Lambda, API Gateway, DynamoDB 통합",
            involved_days=[18, 19, 11],
            primary_day=18,
            services=["Lambda", "API Gateway", "DynamoDB"],
            integration_pattern="Serverless + API + NoSQL",
            use_case="이벤트 기반 마이크로서비스"
        ))
        
        return scenarios
    
    def generate_service_dependency_graph(self) -> Dict[str, List[str]]:
        """서비스 의존성 그래프 생성 (Mermaid 다이어그램용)"""
        graph = defaultdict(list)
        
        for day in range(1, 29):
            topic = self.daily_topics[day]
            primary_services = topic["primary_services"]
            related_days = topic["related_days"]
            
            for service in primary_services:
                for related_day in related_days:
                    if related_day in self.daily_topics:
                        related_services = self.daily_topics[related_day]["primary_services"]
                        for related_service in related_services:
                            if related_service not in graph[service]:
                                graph[service].append(related_service)
        
        return dict(graph)
    
    def get_service_usage_frequency(self) -> Dict[str, int]:
        """서비스 사용 빈도 계산"""
        frequency = defaultdict(int)
        
        for topic in self.daily_topics.values():
            for service in topic["primary_services"]:
                frequency[service] += 1
        
        return dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))
    
    def find_critical_services(self, threshold: int = 3) -> List[str]:
        """핵심 서비스 식별 (여러 일차에서 사용되는 서비스)"""
        frequency = self.get_service_usage_frequency()
        return [service for service, count in frequency.items() if count >= threshold]
    
    def get_week_integration_summary(self, week: int) -> Dict[str, any]:
        """주차별 통합 요약"""
        week_days = [day for day, topic in self.daily_topics.items() if topic["week"] == week]
        
        all_services = set()
        all_connections = []
        
        for day in week_days:
            topic = self.daily_topics[day]
            all_services.update(topic["primary_services"])
            all_connections.extend(self.get_cross_day_connections(day))
        
        return {
            "week": week,
            "days": week_days,
            "services": list(all_services),
            "total_connections": len(all_connections),
            "unique_connections": len(set((c.day_number, c.service_name) for c in all_connections))
        }


def get_service_dependency_mapper() -> CrossServiceIntegrationMapper:
    """서비스 의존성 매퍼 인스턴스 반환"""
    return CrossServiceIntegrationMapper()


def generate_cross_day_integration_data(day: int) -> Dict[str, any]:
    """특정 일차의 크로스 데이 통합 데이터 생성"""
    mapper = get_service_dependency_mapper()
    
    return {
        "day": day,
        "dependencies": mapper.get_service_dependencies(day),
        "connections": mapper.get_cross_day_connections(day),
        "integrations": mapper.get_service_integration_patterns(day)
    }


def generate_all_integration_scenarios() -> List[IntegrationScenario]:
    """모든 통합 시나리오 생성"""
    mapper = get_service_dependency_mapper()
    return mapper.get_integration_scenarios()


def get_service_dependency_graph() -> Dict[str, List[str]]:
    """서비스 의존성 그래프 반환"""
    mapper = get_service_dependency_mapper()
    return mapper.generate_service_dependency_graph()
