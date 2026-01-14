# Tests for Troubleshooting Flowchart Generator
"""
트러블슈팅 플로우차트 생성기 테스트
"""

import pytest
import os
from pathlib import Path
from src.generators.troubleshooting_flowchart_generator import TroubleshootingFlowchartGenerator
from src.config import STUDY_MATERIALS_ROOT


class TestTroubleshootingFlowchartGenerator:
    """트러블슈팅 플로우차트 생성기 기본 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 인스턴스 생성"""
        return TroubleshootingFlowchartGenerator()
    
    def test_generator_initialization(self, generator):
        """생성기가 올바르게 초기화되는지 확인"""
        assert generator.study_materials_root == STUDY_MATERIALS_ROOT
    
    def test_get_output_directory(self, generator):
        """출력 디렉토리 경로가 올바른지 확인"""
        output_dir = generator._get_output_directory(1)
        
        expected_path = (
            STUDY_MATERIALS_ROOT / 
            "week1" / 
            "day1" / 
            "advanced" / 
            "architecture-diagrams"
        )
        
        assert output_dir == expected_path
    
    def test_get_output_directory_different_weeks(self, generator):
        """다른 주차의 출력 디렉토리가 올바른지 확인"""
        # Day 8 (Week 2)
        output_dir_day8 = generator._get_output_directory(8)
        assert "week2" in str(output_dir_day8)
        assert "day8" in str(output_dir_day8)
        
        # Day 15 (Week 3)
        output_dir_day15 = generator._get_output_directory(15)
        assert "week3" in str(output_dir_day15)
        assert "day15" in str(output_dir_day15)


class TestFlowchartGeneration:
    """플로우차트 생성 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 인스턴스 생성"""
        return TroubleshootingFlowchartGenerator()
    
    def test_generate_diagnostic_flowchart(self, generator):
        """진단 플로우차트가 생성되는지 확인"""
        flowchart = generator.generate_diagnostic_flowchart(1)
        
        # Mermaid flowchart 구문 확인
        assert "flowchart TD" in flowchart
        assert "Start[" in flowchart
        assert "End[" in flowchart
        
        # 주요 진단 단계 포함 확인
        assert "CloudWatch" in flowchart
        assert "메트릭 확인" in flowchart
        assert "로그 확인" in flowchart
        assert "네트워크" in flowchart
        assert "비용" in flowchart
    
    def test_generate_performance_troubleshooting(self, generator):
        """성능 트러블슈팅 플로우차트가 생성되는지 확인"""
        flowchart = generator.generate_performance_troubleshooting(1)
        
        assert "flowchart TD" in flowchart
        assert "성능 저하 감지" in flowchart
        assert "지연 시간" in flowchart
        assert "처리량" in flowchart
        assert "에러율" in flowchart
    
    def test_generate_security_troubleshooting(self, generator):
        """보안 트러블슈팅 플로우차트가 생성되는지 확인"""
        flowchart = generator.generate_security_troubleshooting(1)
        
        assert "flowchart TD" in flowchart
        assert "보안 이슈 감지" in flowchart
        assert "CloudTrail" in flowchart
        assert "IAM" in flowchart
        assert "암호화" in flowchart
    
    def test_generate_cost_troubleshooting(self, generator):
        """비용 트러블슈팅 플로우차트가 생성되는지 확인"""
        flowchart = generator.generate_cost_troubleshooting(1)
        
        assert "flowchart TD" in flowchart
        assert "비용 급증 감지" in flowchart
        assert "Cost Explorer" in flowchart
        assert "컴퓨팅 비용" in flowchart
        assert "스토리지 비용" in flowchart
        assert "데이터 전송" in flowchart


class TestFlowchartContent:
    """플로우차트 콘텐츠 검증 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 인스턴스 생성"""
        return TroubleshootingFlowchartGenerator()
    
    def test_diagnostic_flowchart_has_console_paths(self, generator):
        """진단 플로우차트에 Console 경로가 포함되는지 확인"""
        flowchart = generator.generate_diagnostic_flowchart(3)
        
        # Console 경로 확인
        assert "Console:" in flowchart
        assert "CloudWatch" in flowchart
        assert "VPC" in flowchart or "Security Groups" in flowchart
    
    def test_flowchart_has_decision_points(self, generator):
        """플로우차트에 의사결정 지점이 포함되는지 확인"""
        flowchart = generator.generate_diagnostic_flowchart(1)
        
        # Mermaid 의사결정 노드 구문 확인 (중괄호)
        assert "{" in flowchart
        assert "}" in flowchart
    
    def test_flowchart_has_verification_step(self, generator):
        """플로우차트에 검증 단계가 포함되는지 확인"""
        flowchart = generator.generate_diagnostic_flowchart(1)
        
        assert "검증" in flowchart or "Verify" in flowchart
        assert "해결됨?" in flowchart or "Success" in flowchart
    
    def test_flowchart_has_escalation_path(self, generator):
        """플로우차트에 에스컬레이션 경로가 포함되는지 확인"""
        flowchart = generator.generate_diagnostic_flowchart(1)
        
        assert "AWS Support" in flowchart or "에스컬레이션" in flowchart


class TestFileSaving:
    """파일 저장 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 인스턴스 생성"""
        return TroubleshootingFlowchartGenerator()
    
    def test_save_flowchart_creates_file(self, generator, tmp_path):
        """플로우차트 파일이 생성되는지 확인"""
        # 임시 디렉토리 사용
        generator.study_materials_root = tmp_path
        
        flowchart_content = "flowchart TD\n    Start --> End"
        filepath = generator.save_flowchart(1, "diagnostic", flowchart_content)
        
        assert filepath.exists()
        assert filepath.suffix == ".mmd"
        assert "day1-troubleshooting-diagnostic" in filepath.name
    
    def test_save_flowchart_content_matches(self, generator, tmp_path):
        """저장된 플로우차트 내용이 일치하는지 확인"""
        generator.study_materials_root = tmp_path
        
        flowchart_content = "flowchart TD\n    Start --> End"
        filepath = generator.save_flowchart(1, "diagnostic", flowchart_content)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        
        assert saved_content == flowchart_content
    
    def test_save_flowchart_creates_directory(self, generator, tmp_path):
        """디렉토리가 자동으로 생성되는지 확인"""
        generator.study_materials_root = tmp_path
        
        flowchart_content = "flowchart TD\n    Start --> End"
        filepath = generator.save_flowchart(1, "diagnostic", flowchart_content)
        
        assert filepath.parent.exists()
        assert "architecture-diagrams" in str(filepath.parent)


class TestBatchGeneration:
    """배치 생성 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 인스턴스 생성"""
        return TroubleshootingFlowchartGenerator()
    
    def test_generate_flowcharts_for_day(self, generator, tmp_path):
        """특정 일차의 모든 플로우차트가 생성되는지 확인"""
        generator.study_materials_root = tmp_path
        
        flowcharts = generator.generate_flowcharts_for_day(1)
        
        # 4가지 유형의 플로우차트 생성 확인
        assert len(flowcharts) == 4
        assert 'diagnostic' in flowcharts
        assert 'performance' in flowcharts
        assert 'security' in flowcharts
        assert 'cost' in flowcharts
        
        # 모든 파일이 존재하는지 확인
        for filepath in flowcharts.values():
            assert filepath.exists()
    
    def test_generate_all_flowcharts_range(self, generator, tmp_path):
        """지정된 범위의 플로우차트가 생성되는지 확인"""
        generator.study_materials_root = tmp_path
        
        all_flowcharts = generator.generate_all_flowcharts(1, 3)
        
        # 3일치 플로우차트 생성 확인
        assert len(all_flowcharts) == 3
        assert 1 in all_flowcharts
        assert 2 in all_flowcharts
        assert 3 in all_flowcharts
        
        # 각 일차마다 4개의 플로우차트 확인
        for day, flowcharts in all_flowcharts.items():
            assert len(flowcharts) == 4


class TestServiceSpecificContent:
    """서비스별 콘텐츠 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 인스턴스 생성"""
        return TroubleshootingFlowchartGenerator()
    
    def test_ec2_flowchart_has_ec2_specific_content(self, generator):
        """EC2 플로우차트에 EC2 관련 내용이 포함되는지 확인"""
        # Day 3 is EC2
        flowchart = generator.generate_diagnostic_flowchart(3)
        
        assert "EC2" in flowchart
    
    def test_s3_flowchart_has_s3_specific_content(self, generator):
        """S3 플로우차트에 S3 관련 내용이 포함되는지 확인"""
        # Day 8 is S3
        flowchart = generator.generate_diagnostic_flowchart(8)
        
        assert "S3" in flowchart
    
    def test_rds_flowchart_has_rds_specific_content(self, generator):
        """RDS 플로우차트에 RDS 관련 내용이 포함되는지 확인"""
        # Day 10 is RDS
        flowchart = generator.generate_diagnostic_flowchart(10)
        
        assert "RDS" in flowchart


class TestMermaidSyntax:
    """Mermaid 구문 검증 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 인스턴스 생성"""
        return TroubleshootingFlowchartGenerator()
    
    def test_flowchart_starts_with_flowchart_td(self, generator):
        """플로우차트가 'flowchart TD'로 시작하는지 확인"""
        flowchart = generator.generate_diagnostic_flowchart(1)
        assert flowchart.strip().startswith("flowchart TD")
    
    def test_flowchart_has_valid_node_syntax(self, generator):
        """플로우차트에 유효한 노드 구문이 있는지 확인"""
        flowchart = generator.generate_diagnostic_flowchart(1)
        
        # 노드 정의 확인 (예: Start[텍스트])
        assert "[" in flowchart
        assert "]" in flowchart
    
    def test_flowchart_has_valid_edge_syntax(self, generator):
        """플로우차트에 유효한 엣지 구문이 있는지 확인"""
        flowchart = generator.generate_diagnostic_flowchart(1)
        
        # 엣지 연결 확인 (예: A --> B)
        assert "-->" in flowchart
    
    def test_flowchart_has_conditional_edges(self, generator):
        """플로우차트에 조건부 엣지가 있는지 확인"""
        flowchart = generator.generate_diagnostic_flowchart(1)
        
        # 조건부 엣지 확인 (예: A -->|조건| B)
        assert "-->|" in flowchart


class TestErrorHandling:
    """에러 처리 테스트"""
    
    @pytest.fixture
    def generator(self):
        """생성기 인스턴스 생성"""
        return TroubleshootingFlowchartGenerator()
    
    def test_invalid_day_number_raises_error(self, generator):
        """유효하지 않은 일차 번호로 예외 발생 확인"""
        with pytest.raises(ValueError):
            generator.generate_diagnostic_flowchart(0)
        
        with pytest.raises(ValueError):
            generator.generate_diagnostic_flowchart(29)
    
    def test_invalid_day_number_in_batch_generation(self, generator):
        """배치 생성 시 유효하지 않은 일차 번호로 예외 발생 확인"""
        with pytest.raises(ValueError):
            generator.generate_flowcharts_for_day(0)
        
        with pytest.raises(ValueError):
            generator.generate_flowcharts_for_day(29)
