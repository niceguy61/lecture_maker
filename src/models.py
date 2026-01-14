# Core Data Models
"""
핵심 데이터 모델 정의
CaseStudyContent, TroubleshootingContent, BestPracticesContent 등
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class CompanySize(Enum):
    """기업 규모"""
    STARTUP = "startup"
    MEDIUM = "medium"
    ENTERPRISE = "enterprise"


class Severity(Enum):
    """문제 심각도"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SolutionType(Enum):
    """해결 방법 유형"""
    IMMEDIATE = "immediate"
    TEMPORARY = "temporary"
    PERMANENT = "permanent"


class Difficulty(Enum):
    """난이도"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class CompanyInfo:
    """기업 정보"""
    name: str
    industry: str
    size: CompanySize
    region: str
    is_real_company: bool
    public_references: List[str] = field(default_factory=list)


@dataclass
class BusinessRequirement:
    """비즈니스 요구사항"""
    category: str  # 'performance', 'scalability', 'security', 'cost'
    description: str
    metric: Optional[str] = None  # 예: "응답시간 < 100ms"
    priority: str = "medium"  # 'low', 'medium', 'high'


@dataclass
class BusinessContext:
    """비즈니스 컨텍스트"""
    challenge: str
    requirements: List[BusinessRequirement]
    constraints: List[str]
    success_criteria: List[str]
    timeline: str


@dataclass
class AWSServiceUsage:
    """AWS 서비스 사용 정보"""
    service_name: str
    purpose: str
    configuration: Dict[str, str]
    cost_estimate: Optional[str] = None
    related_days: List[int] = field(default_factory=list)


@dataclass
class DesignDecision:
    """설계 결정"""
    decision: str
    rationale: str
    alternatives: List[str]
    tradeoffs: Dict[str, str]  # {'pros': '...', 'cons': '...'}


@dataclass
class ArchitectureDetails:
    """아키텍처 세부사항"""
    diagram_path: str
    description: str
    components: List[str]
    data_flow: List[str]
    security_boundaries: List[str]


@dataclass
class ImplementationStep:
    """구현 단계"""
    step_number: int
    title: str
    description: str
    console_path: str
    configuration: Dict[str, str]
    verification: List[str]
    estimated_time: str


@dataclass
class ImplementationDetails:
    """구현 세부사항"""
    steps: List[ImplementationStep]
    configuration_files: List[str] = field(default_factory=list)
    code_snippets: List[str] = field(default_factory=list)
    monitoring_setup: Optional[str] = None


@dataclass
class BusinessImpactMetrics:
    """비즈니스 임팩트 메트릭"""
    performance_improvements: Dict[str, str]
    cost_savings: Dict[str, str]
    operational_efficiency: Dict[str, str]
    user_experience_improvements: List[str] = field(default_factory=list)


@dataclass
class ServiceIntegration:
    """서비스 통합 정보"""
    primary_service: str
    integrated_service: str
    integration_pattern: str
    data_flow: str
    benefits: List[str]


@dataclass
class CrossDayConnection:
    """크로스 데이 연결"""
    day_number: int
    service_name: str
    connection_type: str  # 'prerequisite', 'enhancement', 'alternative'
    description: str


@dataclass
class CaseStudyContent:
    """사례 연구 콘텐츠"""
    day_number: int
    week_number: int
    
    # 기업 정보
    company: CompanyInfo
    business_context: BusinessContext
    
    # 기술적 솔루션
    primary_services: List[AWSServiceUsage]
    supporting_services: List[AWSServiceUsage]
    architecture: ArchitectureDetails
    design_decisions: List[DesignDecision]
    implementation: ImplementationDetails
    
    # 결과 및 영향
    business_impact: BusinessImpactMetrics
    lessons_learned: List[str]
    
    # 서비스 연계
    service_integrations: List[ServiceIntegration]
    cross_day_connections: List[CrossDayConnection]
    
    # 참고 자료
    aws_documentation_links: List[str] = field(default_factory=list)
    external_references: List[str] = field(default_factory=list)
    
    # 학습 포인트
    key_takeaways: List[str] = field(default_factory=list)


@dataclass
class Symptom:
    """문제 증상"""
    description: str
    observable_metrics: List[str]
    user_impact: str


@dataclass
class DiagnosticStep:
    """진단 단계"""
    step_number: int
    description: str
    console_path: str
    tools_required: List[str]
    expected_results: List[str]
    next_steps: List[str]
    time_estimate: str


@dataclass
class Action:
    """조치 사항"""
    description: str
    console_path: str
    configuration_changes: Dict[str, str]
    expected_effect: str
    estimated_time: str


@dataclass
class Solution:
    """해결 방법"""
    solution_type: SolutionType
    description: str
    steps: List[Action]
    required_permissions: List[str]
    estimated_time: str
    risk_level: str  # 'low', 'medium', 'high'
    rollback_plan: List[str]


@dataclass
class PreventiveMeasure:
    """예방 조치"""
    measure_type: str  # 'monitoring', 'automation', 'configuration'
    description: str
    implementation_steps: List[str]
    console_path: str
    expected_benefit: str


@dataclass
class MonitoringConfiguration:
    """모니터링 설정"""
    service_name: str
    metrics: List[Dict[str, str]]  # [{'name': '...', 'threshold': '...', 'action': '...'}]
    alarms: List[Dict[str, str]]
    dashboard_config: Optional[str] = None


@dataclass
class TroubleshootingCase:
    """트러블슈팅 사례"""
    case_id: str
    title: str
    severity: Severity
    
    # 문제 상황
    symptoms: List[Symptom]
    affected_services: List[str]
    business_impact: str
    
    # 진단 과정
    diagnostic_steps: List[DiagnosticStep]
    tools_used: List[str]
    
    # 해결 방법
    immediate_actions: List[Action]
    root_cause_analysis: str
    permanent_solution: Solution
    
    # 예방 조치
    prevention_measures: List[PreventiveMeasure]
    monitoring_improvements: List[str]
    
    # 학습 포인트
    key_takeaways: List[str]
    related_cases: List[str] = field(default_factory=list)


@dataclass
class TroubleshootingContent:
    """트러블슈팅 콘텐츠"""
    day_number: int
    week_number: int
    service_name: str
    
    # 트러블슈팅 사례들
    common_issues: List[TroubleshootingCase]
    
    # 모니터링 설정
    monitoring_setup: MonitoringConfiguration
    
    # 실습 시나리오
    practice_scenarios: List[Dict[str, str]] = field(default_factory=list)
    
    # 참고 자료
    aws_troubleshooting_guides: List[str] = field(default_factory=list)


@dataclass
class UseCase:
    """사용 사례"""
    title: str
    description: str
    scenario: str
    benefits: List[str]


@dataclass
class ConfigurationExample:
    """설정 예시"""
    title: str
    description: str
    console_path: str
    configuration: Dict[str, str]
    notes: List[str] = field(default_factory=list)


@dataclass
class CodeSnippet:
    """코드 스니펫"""
    language: str
    title: str
    code: str
    description: str
    use_case: str


@dataclass
class IntegrationPattern:
    """통합 패턴"""
    name: str
    description: str
    
    # 서비스 조합
    primary_service: str
    integrated_services: List[str]
    
    # 사용 사례
    use_cases: List[UseCase]
    benefits: List[str]
    tradeoffs: Dict[str, List[str]]  # {'pros': [...], 'cons': [...]}
    
    # 구현 가이드
    implementation_steps: List[ImplementationStep]
    configuration_examples: List[ConfigurationExample]
    code_snippets: List[CodeSnippet]
    
    # 실제 사례
    real_world_examples: List[str]
    
    # 연관 일차
    related_days: List[int]
    prerequisites: List[str]


@dataclass
class EvolutionStage:
    """진화 단계"""
    stage: int
    name: str
    description: str
    services_involved: List[str]
    complexity: Difficulty
    estimated_effort: str
    business_value: str
    prerequisites: List[str]
    deliverables: List[str]


@dataclass
class EvolutionPath:
    """아키텍처 진화 경로"""
    name: str
    description: str
    stages: List[EvolutionStage]
    decision_points: List[str]
    migration_strategies: List[str]


@dataclass
class CostOptimizationStrategy:
    """비용 최적화 전략"""
    strategy_name: str
    description: str
    applicable_services: List[str]
    implementation_steps: List[str]
    expected_savings: str
    effort_level: Difficulty
    console_paths: List[str] = field(default_factory=list)


@dataclass
class SecurityBestPractice:
    """보안 베스트 프랙티스"""
    practice_name: str
    description: str
    applicable_services: List[str]
    implementation_steps: List[str]
    compliance_standards: List[str]
    console_paths: List[str] = field(default_factory=list)


@dataclass
class OperationalPractice:
    """운영 우수성 프랙티스"""
    practice_name: str
    description: str
    category: str  # 'automation', 'monitoring', 'documentation'
    implementation_steps: List[str]
    benefits: List[str]
    tools_used: List[str] = field(default_factory=list)


@dataclass
class BestPracticesContent:
    """베스트 프랙티스 콘텐츠"""
    day_number: int
    week_number: int
    service_name: str
    
    # 서비스 연계 패턴
    integration_patterns: List[IntegrationPattern]
    
    # 아키텍처 진화 경로
    evolution_paths: List[EvolutionPath]
    
    # 비용 최적화
    cost_optimization: List[CostOptimizationStrategy]
    
    # 보안 베스트 프랙티스
    security_best_practices: List[SecurityBestPractice]
    
    # 운영 우수성
    operational_excellence: List[OperationalPractice]
    
    # 참고 자료
    aws_well_architected_links: List[str] = field(default_factory=list)
    related_case_studies: List[str] = field(default_factory=list)


@dataclass
class MermaidDiagram:
    """Mermaid 다이어그램"""
    diagram_type: str  # 'architecture', 'sequence', 'flow', 'sankey'
    title: str
    description: str
    mermaid_code: str
    related_section: str  # 어느 섹션에서 사용되는지


@dataclass
class HandsOnExercise:
    """실습 연습"""
    exercise_number: int
    title: str
    objective: str
    estimated_time: str
    difficulty: Difficulty
    
    # 실습 단계
    steps: List[ImplementationStep]
    
    # 검증
    verification_checklist: List[str]
    expected_results: List[str]
    
    # 리소스 정리
    cleanup_steps: List[str]


@dataclass
class HandsOnContent:
    """실습 콘텐츠"""
    day_number: int
    week_number: int
    service_name: str
    
    # 사전 요구사항
    prerequisites: List[str]
    estimated_cost: str
    estimated_time: str
    
    # 실습 아키텍처
    architecture_diagram: Optional[MermaidDiagram] = None
    
    # 실습 목표
    objectives: List[str] = field(default_factory=list)
    
    # 실습 연습들
    exercises: List[HandsOnExercise] = field(default_factory=list)
    
    # 학습 포인트
    key_learnings: List[str] = field(default_factory=list)
    
    # 다음 단계
    next_steps: List[str] = field(default_factory=list)


@dataclass
class AdvancedContent:
    """통합 심화 콘텐츠"""
    day_number: int
    week_number: int
    
    case_study: CaseStudyContent
    best_practices: BestPracticesContent
    troubleshooting: TroubleshootingContent
    architecture_diagrams: List[MermaidDiagram]
    hands_on: HandsOnContent
