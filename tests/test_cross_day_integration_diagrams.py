"""
Tests for Cross-Day Integration Diagram Generator (Task 6.3)
여러 일차에 걸친 서비스 통합 시각화 및 아키텍처 진화 경로 다이어그램 테스트
"""

import pytest
from pathlib import Path
from src.generators.architecture_diagram_generator import ArchitectureDiagramGenerator
from src.daily_topics import DAILY_TOPICS


class TestCrossDayIntegrationDiagrams:
    """크로스 데이 통합 다이어그램 생성 테스트"""
    
    @pytest.fixture
    def generator(self):
        """다이어그램 생성기 인스턴스"""
        return ArchitectureDiagramGenerator()
    
    def test_multi_day_integration_scenario_generation(self, generator):
        """멀티 데이 통합 시나리오 다이어그램 생성 테스트"""
        # Day 1 (글로벌 인프라) - Netflix 사례
        diagram = generator.generate_multi_day_integration_scenario(1)
        
        assert diagram, "Multi-day integration scenario should be generated"
        assert "```mermaid" in diagram
        assert "graph TB" in diagram
        assert "Day 1" in diagram
        assert "Netflix" in diagram  # 사례 기업명
        assert "통합 사례" in diagram
        assert "End-to-End" in diagram
        
        # 관련 일차 포함 확인
        config = DAILY_TOPICS[1]
        for related_day in config["related_days"][:3]:
            assert f"Day {related_day}" in diagram
    
    def test_architecture_evolution_diagram_generation(self, generator):
        """아키텍처 진화 경로 다이어그램 생성 테스트"""
        # Day 8 (S3) - Dropbox 사례
        diagram = generator.generate_architecture_evolution_diagram(8)
        
        assert diagram, "Architecture evolution diagram should be generated"
        assert "```mermaid" in diagram
        assert "graph LR" in diagram
        assert "Stage 1: 기본 구성" in diagram
        assert "Stage 2: 서비스 확장" in diagram
        assert "Stage 3: 완전한 통합" in diagram
        assert "Day 8" in diagram
        
        # 진화 경로 연결 확인
        assert "==>|확장|" in diagram
        assert "==>|최적화|" in diagram
        
        # 스타일 적용 확인
        assert "fill:#E8F5E9" in diagram
        assert "fill:#FFF9C4" in diagram
        assert "fill:#E1F5FE" in diagram
    
    def test_end_to_end_flow_diagram_generation(self, generator):
        """End-to-End 플로우 다이어그램 생성 테스트"""
        # Day 18 (Lambda) - Coca-Cola 사례
        diagram = generator.generate_end_to_end_flow_diagram(18)
        
        assert diagram, "End-to-end flow diagram should be generated"
        assert "```mermaid" in diagram
        assert "sequenceDiagram" in diagram
        assert "participant User" in diagram
        assert "participant D18" in diagram
        assert "participant Monitor" in diagram
        
        # 플로우 단계 확인
        assert "초기 요청" in diagram
        assert "데이터 처리 요청" in diagram
        assert "처리 결과" in diagram
        assert "최종 응답" in diagram
        assert "메트릭 전송" in diagram
        
        # 노트 확인
        assert "총" in diagram and "단계 처리" in diagram
        assert "여러 일차 서비스 통합" in diagram
    
    def test_cross_day_diagrams_for_all_days(self, generator):
        """모든 일차에 대한 크로스 데이 다이어그램 생성 테스트"""
        for day in range(1, 29):
            config = DAILY_TOPICS[day]
            related_days = config.get("related_days", [])
            
            if related_days:
                # 관련 일차가 있는 경우 모든 크로스 데이 다이어그램 생성 가능
                multi_day = generator.generate_multi_day_integration_scenario(day)
                evolution = generator.generate_architecture_evolution_diagram(day)
                e2e_flow = generator.generate_end_to_end_flow_diagram(day)
                
                assert multi_day, f"Day {day} should have multi-day integration scenario"
                assert evolution, f"Day {day} should have architecture evolution diagram"
                assert e2e_flow, f"Day {day} should have end-to-end flow diagram"
                
                # Mermaid 구문 검증
                assert "```mermaid" in multi_day
                assert "```mermaid" in evolution
                assert "```mermaid" in e2e_flow
    
    def test_diagram_file_saving(self, generator, tmp_path):
        """다이어그램 파일 저장 테스트"""
        # 임시 경로로 변경
        original_path = generator.output_base_path
        generator.output_base_path = tmp_path
        
        try:
            # Day 1 다이어그램 생성
            results = generator.generate_diagrams_for_day(1)
            
            # 새로운 크로스 데이 다이어그램 파일 확인
            assert "multi-day-integration-scenario" in results
            assert "architecture-evolution" in results
            assert "end-to-end-flow" in results
            
            # 파일 존재 확인
            for diagram_type, filepath in results.items():
                assert filepath.exists(), f"{diagram_type} file should exist"
                assert filepath.suffix == ".mmd"
                
                # 파일 내용 확인
                content = filepath.read_text(encoding='utf-8')
                assert "```mermaid" in content
                assert "```" in content
        
        finally:
            generator.output_base_path = original_path
    
    def test_multi_day_scenario_with_company_case(self, generator):
        """기업 사례가 포함된 멀티 데이 시나리오 테스트"""
        test_cases = [
            (1, "Netflix"),      # 글로벌 인프라
            (8, "Dropbox"),      # S3 스토리지
            (18, "Coca-Cola"),   # Lambda 서버리스
        ]
        
        for day, company in test_cases:
            diagram = generator.generate_multi_day_integration_scenario(day)
            assert company in diagram, f"Day {day} should include {company} case study"
            assert "통합 사례" in diagram
    
    def test_evolution_stages_progression(self, generator):
        """아키텍처 진화 단계 진행 테스트"""
        # Day 18 (Lambda) - 3단계 진화 확인
        diagram = generator.generate_architecture_evolution_diagram(18)
        
        # Stage 1: 기본 (Lambda만)
        assert "Stage 1: 기본 구성" in diagram
        assert "Day 18" in diagram
        
        # Stage 2: 확장 (Lambda + DynamoDB)
        assert "Stage 2: 서비스 확장" in diagram
        assert "Day 18 +" in diagram
        
        # Stage 3: 완전한 통합 (Lambda + DynamoDB + SQS)
        assert "Stage 3: 완전한 통합" in diagram
        
        # 진화 경로 확인
        assert "확장" in diagram
        assert "최적화" in diagram
    
    def test_e2e_flow_participant_count(self, generator):
        """End-to-End 플로우의 참여자 수 테스트"""
        # Day 1 (관련 일차 2개: 16, 17)
        diagram = generator.generate_end_to_end_flow_diagram(1)
        
        # 최소 참여자: User, Day1, Monitor + 관련 일차들
        assert "participant User" in diagram
        assert "participant D1" in diagram
        assert "participant Monitor" in diagram
        
        # 관련 일차 참여자 (최대 3개)
        config = DAILY_TOPICS[1]
        related_days = config["related_days"][:3]
        for related_day in related_days:
            assert f"participant D{related_day}" in diagram
    
    def test_diagram_mermaid_syntax_validity(self, generator):
        """Mermaid 다이어그램 구문 유효성 테스트"""
        for day in [1, 8, 18]:
            multi_day = generator.generate_multi_day_integration_scenario(day)
            evolution = generator.generate_architecture_evolution_diagram(day)
            e2e_flow = generator.generate_end_to_end_flow_diagram(day)
            
            # 모든 다이어그램이 올바른 Mermaid 구문으로 시작하고 끝나는지 확인
            for diagram in [multi_day, evolution, e2e_flow]:
                assert diagram.startswith("```mermaid\n")
                assert diagram.endswith("```\n")
                
                # 다이어그램 타입 확인
                if "graph TB" in diagram or "graph LR" in diagram:
                    # 그래프 다이어그램
                    assert "subgraph" in diagram or "[" in diagram
                elif "sequenceDiagram" in diagram:
                    # 시퀀스 다이어그램
                    assert "participant" in diagram
                    assert "->>" in diagram or "-->>" in diagram
    
    def test_cross_day_integration_count(self, generator):
        """생성된 크로스 데이 통합 다이어그램 수 테스트"""
        # Day 1 전체 다이어그램 생성
        results = generator.generate_diagrams_for_day(1)
        
        # Task 6.3에서 추가된 3개의 새로운 다이어그램 확인
        new_diagram_types = [
            "multi-day-integration-scenario",
            "architecture-evolution",
            "end-to-end-flow"
        ]
        
        for diagram_type in new_diagram_types:
            assert diagram_type in results, f"{diagram_type} should be generated"
        
        # 총 다이어그램 수 확인 (기존 5개 + 새로운 3개 = 8개)
        assert len(results) >= 6, "Should generate at least 6 diagrams including new cross-day diagrams"


class TestCrossDayIntegrationRequirements:
    """Requirements 5.3, 5.4 검증 테스트"""
    
    @pytest.fixture
    def generator(self):
        return ArchitectureDiagramGenerator()
    
    def test_requirement_5_3_multi_layer_architecture(self, generator):
        """Requirement 5.3: 다층 아키텍처 다이어그램 생성"""
        # 멀티 데이 통합 시나리오는 여러 계층을 보여줌
        diagram = generator.generate_multi_day_integration_scenario(1)
        
        # 여러 subgraph (계층) 확인
        assert diagram.count("subgraph") >= 3, "Should have multiple layers"
        assert "사용자 요청 플로우" in diagram
        assert "통합 사례" in diagram
    
    def test_requirement_5_4_before_after_comparison(self, generator):
        """Requirement 5.4: Before/After 아키텍처 비교 (진화 경로)"""
        # 아키텍처 진화 다이어그램은 Stage 1 → Stage 2 → Stage 3 비교를 보여줌
        diagram = generator.generate_architecture_evolution_diagram(8)
        
        # 3단계 진화 확인
        assert "Stage 1" in diagram
        assert "Stage 2" in diagram
        assert "Stage 3" in diagram
        
        # 진화 경로 (migration path) 확인
        assert "==>" in diagram, "Should show evolution arrows"
        
        # 시각적 구분 (색상 스타일) 확인
        assert "fill:#E8F5E9" in diagram  # Stage 1 색상
        assert "fill:#FFF9C4" in diagram  # Stage 2 색상
        assert "fill:#E1F5FE" in diagram  # Stage 3 색상
    
    def test_requirement_5_3_sequence_diagram(self, generator):
        """Requirement 5.3: 시퀀스 다이어그램으로 요청 플로우 시각화"""
        # End-to-End 플로우는 시퀀스 다이어그램 사용
        diagram = generator.generate_end_to_end_flow_diagram(18)
        
        assert "sequenceDiagram" in diagram
        assert "participant" in diagram
        assert "activate" in diagram
        assert "deactivate" in diagram
        
        # 여러 서비스 간 상호작용 확인
        assert "->>" in diagram or "-->>" in diagram


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
