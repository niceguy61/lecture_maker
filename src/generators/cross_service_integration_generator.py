# Cross-Service Integration Content Generator
"""
크로스 서비스 통합 콘텐츠 생성기
서비스 의존성 매핑 데이터를 기반으로 문서 생성
"""

from typing import Dict, List
from src.cross_service_integration import (
    CrossServiceIntegrationMapper,
    IntegrationScenario,
    get_service_dependency_mapper,
    generate_cross_day_integration_data
)
from src.daily_topics import DAILY_TOPICS


class CrossServiceIntegrationContentGenerator:
    """크로스 서비스 통합 콘텐츠 생성기"""
    
    def __init__(self):
        self.mapper = get_service_dependency_mapper()
    
    def generate_service_dependency_section(self, day: int) -> str:
        """서비스 의존성 섹션 생성"""
        dependencies = self.mapper.get_service_dependencies(day)
        
        if not dependencies:
            return "## 서비스 의존성\n\n이 일차는 독립적인 서비스를 다룹니다.\n"
        
        content = "## 서비스 의존성\n\n"
        
        for dep in dependencies:
            content += f"### {dep.service_name}\n\n"
            content += f"**의존성 타입**: {dep.dependency_type}\n\n"
            
            if dep.dependent_services:
                content += "**연계 서비스**:\n"
                for service in dep.dependent_services:
                    content += f"- {service}\n"
                content += "\n"
            
            content += f"{dep.description}\n\n"
        
        return content
    
    def generate_cross_day_connections_section(self, day: int) -> str:
        """크로스 데이 연결 섹션 생성"""
        connections = self.mapper.get_cross_day_connections(day)
        
        if not connections:
            return "## 다른 일차와의 연계\n\n이 일차는 다른 일차와 직접적인 연계가 없습니다.\n"
        
        content = "## 다른 일차와의 연계\n\n"
        
        # 연결 타입별로 그룹화
        prerequisites = [c for c in connections if c.connection_type == "prerequisite"]
        enhancements = [c for c in connections if c.connection_type == "enhancement"]
        alternatives = [c for c in connections if c.connection_type == "alternative"]
        
        if prerequisites:
            content += "### 사전 학습 내용\n\n"
            for conn in prerequisites:
                topic = DAILY_TOPICS[conn.day_number]
                content += f"- **Day {conn.day_number}: {topic['title']}** - {conn.service_name}\n"
                content += f"  - {conn.description}\n"
            content += "\n"
        
        if enhancements:
            content += "### 향후 학습 내용\n\n"
            for conn in enhancements:
                topic = DAILY_TOPICS[conn.day_number]
                content += f"- **Day {conn.day_number}: {topic['title']}** - {conn.service_name}\n"
                content += f"  - {conn.description}\n"
            content += "\n"
        
        if alternatives:
            content += "### 대안적 접근\n\n"
            for conn in alternatives:
                topic = DAILY_TOPICS[conn.day_number]
                content += f"- **Day {conn.day_number}: {topic['title']}** - {conn.service_name}\n"
                content += f"  - {conn.description}\n"
            content += "\n"
        
        return content
    
    def generate_integration_patterns_section(self, day: int) -> str:
        """통합 패턴 섹션 생성"""
        integrations = self.mapper.get_service_integration_patterns(day)
        
        if not integrations:
            return "## 서비스 통합 패턴\n\n통합 패턴 정보가 없습니다.\n"
        
        content = "## 서비스 통합 패턴\n\n"
        
        # 중복 제거를 위해 패턴별로 그룹화
        patterns = {}
        for integ in integrations:
            pattern = integ.integration_pattern
            if pattern not in patterns:
                patterns[pattern] = []
            patterns[pattern].append(integ)
        
        for pattern, integ_list in patterns.items():
            content += f"### {pattern}\n\n"
            
            # 첫 번째 통합 정보 사용
            integ = integ_list[0]
            content += f"**주요 서비스**: {integ.primary_service}\n"
            content += f"**통합 서비스**: {integ.integrated_service}\n\n"
            content += f"**데이터 플로우**: {integ.data_flow}\n\n"
            
            content += "**이점**:\n"
            for benefit in integ.benefits:
                content += f"- {benefit}\n"
            content += "\n"
        
        return content
    
    def generate_integration_scenario_document(self, scenario: IntegrationScenario) -> str:
        """통합 시나리오 문서 생성"""
        content = f"# {scenario.name}\n\n"
        content += f"**시나리오 ID**: {scenario.scenario_id}\n\n"
        content += f"## 개요\n\n{scenario.description}\n\n"
        
        content += f"## 관련 일차\n\n"
        content += f"**주요 일차**: Day {scenario.primary_day}\n\n"
        content += "**연관 일차**:\n"
        for day in scenario.involved_days:
            topic = DAILY_TOPICS[day]
            content += f"- Day {day}: {topic['title']}\n"
        content += "\n"
        
        content += "## 사용 서비스\n\n"
        for service in scenario.services:
            content += f"- {service}\n"
        content += "\n"
        
        content += f"## 통합 패턴\n\n{scenario.integration_pattern}\n\n"
        content += f"## 사용 사례\n\n{scenario.use_case}\n\n"
        
        content += "## 아키텍처 다이어그램\n\n"
        content += "```mermaid\n"
        content += self._generate_scenario_diagram(scenario)
        content += "```\n\n"
        
        content += "## 구현 가이드\n\n"
        for i, day in enumerate(scenario.involved_days, 1):
            topic = DAILY_TOPICS[day]
            content += f"### 단계 {i}: Day {day} - {topic['title']}\n\n"
            content += f"이 단계에서는 {', '.join(topic['primary_services'])}를 설정합니다.\n\n"
        
        content += "## 학습 경로\n\n"
        for day in scenario.involved_days:
            topic = DAILY_TOPICS[day]
            content += f"1. Day {day}: {topic['title']} 학습 완료\n"
        content += f"{len(scenario.involved_days) + 1}. 통합 시나리오 실습\n\n"
        
        return content
    
    def _generate_scenario_diagram(self, scenario: IntegrationScenario) -> str:
        """시나리오 다이어그램 생성"""
        diagram = "graph TB\n"
        
        # 서비스 노드 생성
        for i, service in enumerate(scenario.services):
            node_id = f"S{i+1}"
            diagram += f"    {node_id}[{service}]\n"
        
        # 간단한 연결 (순차적)
        for i in range(len(scenario.services) - 1):
            diagram += f"    S{i+1} --> S{i+2}\n"
        
        return diagram
    
    def generate_service_dependency_graph_mermaid(self) -> str:
        """서비스 의존성 그래프 Mermaid 다이어그램 생성"""
        graph = self.mapper.generate_service_dependency_graph()
        
        diagram = "```mermaid\ngraph LR\n"
        
        # 주요 서비스만 포함 (너무 복잡하지 않도록)
        critical_services = self.mapper.find_critical_services(threshold=2)
        
        for service in critical_services:
            if service in graph:
                dependencies = graph[service]
                for dep in dependencies:
                    if dep in critical_services:
                        # 서비스명을 노드 ID로 변환 (공백 제거)
                        service_id = service.replace(" ", "_")
                        dep_id = dep.replace(" ", "_")
                        diagram += f"    {service_id}[{service}] --> {dep_id}[{dep}]\n"
        
        diagram += "```\n"
        return diagram
    
    def generate_week_integration_summary_document(self, week: int) -> str:
        """주차별 통합 요약 문서 생성"""
        summary = self.mapper.get_week_integration_summary(week)
        
        content = f"# Week {week} 서비스 통합 요약\n\n"
        content += f"## 개요\n\n"
        content += f"Week {week}에서는 총 {len(summary['services'])}개의 주요 서비스를 학습합니다.\n\n"
        
        content += "## 학습 일차\n\n"
        for day in summary['days']:
            topic = DAILY_TOPICS[day]
            content += f"- Day {day}: {topic['title']}\n"
        content += "\n"
        
        content += "## 주요 서비스\n\n"
        for service in summary['services']:
            content += f"- {service}\n"
        content += "\n"
        
        content += f"## 통합 정보\n\n"
        content += f"- 총 연결 수: {summary['total_connections']}\n"
        content += f"- 고유 연결 수: {summary['unique_connections']}\n\n"
        
        content += "## 서비스 연계 다이어그램\n\n"
        content += "```mermaid\n"
        content += self._generate_week_diagram(week, summary)
        content += "```\n\n"
        
        return content
    
    def _generate_week_diagram(self, week: int, summary: Dict) -> str:
        """주차별 다이어그램 생성"""
        diagram = "graph TB\n"
        
        # 일차별 서브그래프
        for day in summary['days']:
            topic = DAILY_TOPICS[day]
            diagram += f"    subgraph Day{day}[Day {day}: {topic['title']}]\n"
            for service in topic['primary_services']:
                service_id = f"D{day}_{service.replace(' ', '_')}"
                diagram += f"        {service_id}[{service}]\n"
            diagram += "    end\n"
        
        return diagram
    
    def generate_critical_services_report(self) -> str:
        """핵심 서비스 리포트 생성"""
        critical_services = self.mapper.find_critical_services(threshold=2)
        frequency = self.mapper.get_service_usage_frequency()
        
        content = "# 핵심 AWS 서비스 분석\n\n"
        content += "## 개요\n\n"
        content += f"28일 학습 과정에서 {len(critical_services)}개의 핵심 서비스가 식별되었습니다.\n\n"
        
        content += "## 핵심 서비스 목록\n\n"
        content += "| 서비스 | 사용 빈도 | 중요도 |\n"
        content += "|--------|----------|--------|\n"
        
        for service in critical_services:
            freq = frequency[service]
            importance = "높음" if freq >= 3 else "중간"
            content += f"| {service} | {freq}회 | {importance} |\n"
        
        content += "\n## 서비스별 상세 정보\n\n"
        
        for service in critical_services[:5]:  # 상위 5개만
            content += f"### {service}\n\n"
            content += f"**사용 빈도**: {frequency[service]}회\n\n"
            
            # 해당 서비스가 사용되는 일차 찾기
            days = self.mapper.service_to_days.get(service, [])
            content += "**사용 일차**:\n"
            for day in days:
                topic = DAILY_TOPICS[day]
                content += f"- Day {day}: {topic['title']}\n"
            content += "\n"
        
        return content


def generate_cross_service_integration_content(day: int) -> Dict[str, str]:
    """특정 일차의 크로스 서비스 통합 콘텐츠 생성"""
    generator = CrossServiceIntegrationContentGenerator()
    
    return {
        "dependencies": generator.generate_service_dependency_section(day),
        "connections": generator.generate_cross_day_connections_section(day),
        "patterns": generator.generate_integration_patterns_section(day)
    }


def generate_all_integration_scenario_documents() -> Dict[str, str]:
    """모든 통합 시나리오 문서 생성"""
    generator = CrossServiceIntegrationContentGenerator()
    mapper = get_service_dependency_mapper()
    scenarios = mapper.get_integration_scenarios()
    
    documents = {}
    for scenario in scenarios:
        doc = generator.generate_integration_scenario_document(scenario)
        documents[scenario.scenario_id] = doc
    
    return documents


def generate_service_dependency_graph() -> str:
    """서비스 의존성 그래프 생성"""
    generator = CrossServiceIntegrationContentGenerator()
    return generator.generate_service_dependency_graph_mermaid()


def generate_week_summaries() -> Dict[int, str]:
    """모든 주차의 통합 요약 생성"""
    generator = CrossServiceIntegrationContentGenerator()
    
    summaries = {}
    for week in range(1, 5):
        summaries[week] = generator.generate_week_integration_summary_document(week)
    
    return summaries


def generate_critical_services_report() -> str:
    """핵심 서비스 리포트 생성"""
    generator = CrossServiceIntegrationContentGenerator()
    return generator.generate_critical_services_report()
