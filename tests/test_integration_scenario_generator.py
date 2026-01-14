# Tests for Integration Scenario Generator
"""
통합 시나리오 생성기 테스트
Task 8.2: 통합 시나리오 생성기 검증
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from src.generators.integration_scenario_generator import (
    IntegrationScenarioGenerator,
    generate_integration_scenario,
    generate_all_integration_scenarios
)
from src.cross_service_integration import IntegrationScenario


class TestIntegrationScenarioGenerator:
    """통합 시나리오 생성기 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 픽스처"""
        return IntegrationScenarioGenerator()
    
    @pytest.fixture
    def temp_output_dir(self):
        """임시 출력 디렉토리"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        # 정리
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
    
    def test_generator_initialization(self, generator):
        """생성기 초기화 테스트"""
        assert generator is not None
        assert generator.mapper is not None
        assert len(generator.scenarios) > 0
        assert generator.output_base_path is not None
    
    def test_scenarios_loaded(self, generator):
        """시나리오 로드 테스트"""
        scenarios = generator.scenarios
        
        # 최소 5개 시나리오 존재
        assert len(scenarios) >= 5
        
        # 각 시나리오 검증
        for scenario in scenarios:
            assert isinstance(scenario, IntegrationScenario)
            assert scenario.scenario_id
            assert scenario.name
            assert scenario.description
            assert len(scenario.involved_days) > 0
            assert scenario.primary_day in scenario.involved_days
            assert len(scenario.services) > 0
    
    def test_expected_scenarios_exist(self, generator):
        """예상 시나리오 존재 확인"""
        scenario_ids = [s.scenario_id for s in generator.scenarios]
        
        expected_ids = [
            "netflix_streaming",
            "airbnb_security",
            "spotify_scalability",
            "dropbox_storage",
            "serverless_app"
        ]
        
        for expected_id in expected_ids:
            assert expected_id in scenario_ids, f"Expected scenario {expected_id} not found"
    
    def test_generate_scenario_overview(self, generator):
        """시나리오 개요 생성 테스트"""
        scenario = generator.scenarios[0]
        overview = generator.generate_scenario_overview(scenario)
        
        assert "## 📋 시나리오 개요" in overview
        assert scenario.scenario_id in overview
        assert scenario.name in overview
        assert scenario.description in overview
        assert f"Day {scenario.primary_day}" in overview
    
    def test_generate_involved_days_section(self, generator):
        """관련 일차 섹션 생성 테스트"""
        scenario = generator.scenarios[0]
        section = generator.generate_involved_days_section(scenario)
        
        assert "## 📅 관련 일차" in section
        
        for day in scenario.involved_days:
            assert f"Day {day}" in section
    
    def test_generate_architecture_diagram(self, generator):
        """아키텍처 다이어그램 생성 테스트"""
        scenario = generator.scenarios[0]
        diagram = generator.generate_architecture_diagram(scenario)
        
        assert "```mermaid" in diagram
        assert "graph TB" in diagram
        assert "사용자 계층" in diagram
        assert "```" in diagram
    
    def test_generate_service_flow(self, generator):
        """서비스 플로우 생성 테스트"""
        scenario = generator.scenarios[0]
        flow = generator.generate_service_flow(scenario)
        
        assert "## 🔄 서비스 플로우" in flow
        assert "End-to-End 요청 처리 흐름" in flow
        assert "시퀀스 다이어그램" in flow
        assert "```mermaid" in flow
        assert "sequenceDiagram" in flow
    
    def test_generate_implementation_guide(self, generator):
        """구현 가이드 생성 테스트"""
        scenario = generator.scenarios[0]
        guide = generator.generate_implementation_guide(scenario)
        
        assert "## 💻 구현 가이드" in guide
        assert "단계별 구현 방법" in guide
        assert "통합 검증" in guide
        
        for day in scenario.involved_days:
            assert f"Day {day}" in guide
    
    def test_generate_learning_path(self, generator):
        """학습 경로 생성 테스트"""
        scenario = generator.scenarios[0]
        path = generator.generate_learning_path(scenario)
        
        assert "## 🎓 학습 경로" in path
        assert "권장 학습 순서" in path
        assert "실습 순서" in path
        assert "학습 목표" in path
    
    def test_generate_best_practices(self, generator):
        """베스트 프랙티스 생성 테스트"""
        scenario = generator.scenarios[0]
        practices = generator.generate_best_practices(scenario)
        
        assert "## ✅ 베스트 프랙티스" in practices
        assert "아키텍처 설계" in practices
        assert "비용 최적화" in practices
        assert "운영 효율성" in practices
    
    def test_generate_troubleshooting(self, generator):
        """트러블슈팅 생성 테스트"""
        scenario = generator.scenarios[0]
        troubleshooting = generator.generate_troubleshooting(scenario)
        
        assert "## 🔧 트러블슈팅" in troubleshooting
        assert "일반적인 문제" in troubleshooting
        assert "문제 1" in troubleshooting
        assert "증상" in troubleshooting
        assert "진단" in troubleshooting
        assert "해결" in troubleshooting
    
    def test_generate_references(self, generator):
        """참고 자료 생성 테스트"""
        scenario = generator.scenarios[0]
        references = generator.generate_references(scenario)
        
        assert "## 📚 참고 자료" in references
        assert "AWS 공식 문서" in references
        assert "아키텍처 패턴" in references
        assert "관련 학습 자료" in references
    
    def test_generate_scenario_document(self, generator):
        """완전한 시나리오 문서 생성 테스트"""
        scenario = generator.scenarios[0]
        document = generator.generate_scenario_document(scenario)
        
        # 제목 확인
        assert scenario.name in document
        
        # 주요 섹션 확인
        required_sections = [
            "## 📋 시나리오 개요",
            "## 📅 관련 일차",
            "## 🏗️ 서비스 아키텍처",
            "## 🔄 서비스 플로우",
            "## 💻 구현 가이드",
            "## 🎓 학습 경로",
            "## ✅ 베스트 프랙티스",
            "## 🔧 트러블슈팅",
            "## 📚 참고 자료"
        ]
        
        for section in required_sections:
            assert section in document, f"Required section missing: {section}"
        
        # 메타데이터 확인
        assert "생성일" in document
        assert "버전" in document
    
    def test_save_scenario_document(self, generator, temp_output_dir):
        """시나리오 문서 저장 테스트"""
        scenario = generator.scenarios[0]
        output_path = temp_output_dir / f"{scenario.scenario_id}.md"
        
        saved_path = generator.save_scenario_document(scenario, output_path)
        
        assert saved_path.exists()
        assert saved_path == output_path
        
        # 파일 내용 확인
        with open(saved_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert scenario.name in content
            assert len(content) > 1000  # 최소 길이 확인
    
    def test_generate_all_scenarios(self, generator, temp_output_dir):
        """모든 시나리오 생성 테스트"""
        generated_files = generator.generate_all_scenarios(temp_output_dir)
        
        # 파일 수 확인 (시나리오 + README)
        assert len(generated_files) == len(generator.scenarios) + 1
        
        # 모든 파일 존재 확인
        for file_path in generated_files:
            assert file_path.exists()
            assert file_path.stat().st_size > 0
        
        # README 확인
        readme_path = temp_output_dir / "README.md"
        assert readme_path in generated_files
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
            assert "AWS 통합 시나리오" in readme_content
            assert "시나리오 목록" in readme_content
    
    def test_generate_integration_scenario_function(self, temp_output_dir):
        """개별 시나리오 생성 함수 테스트"""
        output_path = temp_output_dir / "netflix_streaming.md"
        
        saved_path = generate_integration_scenario("netflix_streaming", output_path)
        
        assert saved_path.exists()
        assert saved_path == output_path
        
        with open(saved_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Netflix" in content
            assert "글로벌 스트리밍" in content
    
    def test_generate_integration_scenario_invalid_id(self):
        """잘못된 시나리오 ID 테스트"""
        with pytest.raises(ValueError, match="Scenario not found"):
            generate_integration_scenario("invalid_scenario_id")
    
    def test_generate_all_integration_scenarios_function(self, temp_output_dir):
        """모든 시나리오 생성 함수 테스트"""
        generated_files = generate_all_integration_scenarios(temp_output_dir)
        
        assert len(generated_files) > 0
        
        for file_path in generated_files:
            assert file_path.exists()
    
    def test_netflix_scenario_specific_content(self, generator):
        """Netflix 시나리오 특정 내용 테스트"""
        netflix_scenario = None
        for s in generator.scenarios:
            if s.scenario_id == "netflix_streaming":
                netflix_scenario = s
                break
        
        assert netflix_scenario is not None
        
        document = generator.generate_scenario_document(netflix_scenario)
        
        # Netflix 특정 내용 확인
        assert "CloudFront" in document
        assert "S3" in document
        assert "스트리밍" in document
    
    def test_airbnb_scenario_specific_content(self, generator):
        """Airbnb 시나리오 특정 내용 테스트"""
        airbnb_scenario = None
        for s in generator.scenarios:
            if s.scenario_id == "airbnb_security":
                airbnb_scenario = s
                break
        
        assert airbnb_scenario is not None
        
        document = generator.generate_scenario_document(airbnb_scenario)
        
        # Airbnb 특정 내용 확인
        assert "IAM" in document
        assert "VPC" in document
        assert "보안" in document
    
    def test_document_structure_consistency(self, generator):
        """문서 구조 일관성 테스트"""
        for scenario in generator.scenarios:
            document = generator.generate_scenario_document(scenario)
            
            # 모든 시나리오가 동일한 구조를 가져야 함
            assert document.startswith(f"# {scenario.name}")
            assert "---" in document  # 구분선 존재
            assert "```mermaid" in document  # 다이어그램 존재
            assert "생성일" in document  # 메타데이터 존재
    
    def test_mermaid_diagram_validity(self, generator):
        """Mermaid 다이어그램 유효성 테스트"""
        for scenario in generator.scenarios:
            # 아키텍처 다이어그램
            arch_diagram = generator.generate_architecture_diagram(scenario)
            assert arch_diagram.count("```mermaid") == 1
            assert arch_diagram.count("```") == 2
            assert "graph TB" in arch_diagram
            
            # 시퀀스 다이어그램
            flow = generator.generate_service_flow(scenario)
            assert "sequenceDiagram" in flow
    
    def test_cross_references_validity(self, generator):
        """크로스 레퍼런스 유효성 테스트"""
        for scenario in generator.scenarios:
            document = generator.generate_scenario_document(scenario)
            
            # 모든 관련 일차가 문서에 언급되어야 함
            for day in scenario.involved_days:
                assert f"Day {day}" in document
    
    def test_korean_language_quality(self, generator):
        """한국어 품질 테스트"""
        for scenario in generator.scenarios:
            document = generator.generate_scenario_document(scenario)
            
            # 한국어 섹션 제목 확인
            korean_sections = [
                "시나리오 개요",
                "관련 일차",
                "서비스 아키텍처",
                "서비스 플로우",
                "구현 가이드",
                "학습 경로",
                "베스트 프랙티스",
                "트러블슈팅",
                "참고 자료"
            ]
            
            for section in korean_sections:
                assert section in document
    
    def test_file_size_reasonable(self, generator, temp_output_dir):
        """파일 크기 적정성 테스트"""
        generated_files = generator.generate_all_scenarios(temp_output_dir)
        
        for file_path in generated_files:
            file_size = file_path.stat().st_size
            
            # 최소 크기 (1KB)
            assert file_size > 1024, f"File too small: {file_path}"
            
            # 최대 크기 (500KB) - 너무 크면 문제
            assert file_size < 500 * 1024, f"File too large: {file_path}"


class TestIntegrationScenarioContent:
    """통합 시나리오 콘텐츠 품질 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 픽스처"""
        return IntegrationScenarioGenerator()
    
    @pytest.fixture
    def temp_output_dir(self):
        """임시 출력 디렉토리"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        # 정리
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
    
    def test_all_scenarios_have_flow_steps(self, generator):
        """모든 시나리오가 플로우 단계를 가지는지 테스트"""
        for scenario in generator.scenarios:
            flow_steps = generator._generate_flow_steps(scenario)
            assert len(flow_steps) > 0
            
            for step in flow_steps:
                assert "title" in step
                assert "service" in step
                assert "description" in step
                assert "next" in step
    
    def test_all_scenarios_have_sequence_diagrams(self, generator):
        """모든 시나리오가 시퀀스 다이어그램을 가지는지 테스트"""
        for scenario in generator.scenarios:
            seq_diagram = generator._generate_sequence_diagram(scenario)
            assert "```mermaid" in seq_diagram
            assert "sequenceDiagram" in seq_diagram
            assert "participant" in seq_diagram
    
    def test_scenarios_readme_completeness(self, generator, temp_output_dir):
        """시나리오 README 완전성 테스트"""
        generator.generate_all_scenarios(temp_output_dir)
        
        readme_path = temp_output_dir / "README.md"
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        # 모든 시나리오가 README에 언급되어야 함
        for scenario in generator.scenarios:
            assert scenario.name in readme_content
            assert scenario.scenario_id in readme_content
