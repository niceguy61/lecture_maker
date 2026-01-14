# Tests for Content Validator
"""
콘텐츠 검증기 테스트
Console 경로 유효성 검증 및 Mermaid 다이어그램 구문 검증
"""

import pytest
from src.generators.content_validator import (
    ConsolePathValidator,
    MermaidValidator,
    ContentValidator,
    ValidationResult,
    ValidationSeverity,
    ContentValidationReport
)


class TestConsolePathValidator:
    """Console 경로 검증기 테스트"""
    
    @pytest.fixture
    def validator(self):
        """검증기 인스턴스"""
        return ConsolePathValidator()
    
    def test_valid_services_pattern(self, validator):
        """유효한 Services 패턴"""
        path = "Services > Compute > EC2"
        result = validator.validate_console_path(path)
        
        assert result.is_valid
        assert result.severity == ValidationSeverity.INFO
    
    def test_valid_iam_pattern(self, validator):
        """유효한 IAM 패턴"""
        paths = [
            "IAM > Users",
            "IAM > Roles",
            "IAM > Policies",
            "IAM > Groups"
        ]
        
        for path in paths:
            result = validator.validate_console_path(path)
            assert result.is_valid
    
    def test_valid_vpc_pattern(self, validator):
        """유효한 VPC 패턴"""
        paths = [
            "VPC > Subnets",
            "VPC > Route Tables",
            "VPC > Internet Gateways",
            "VPC > Security Groups"
        ]
        
        for path in paths:
            result = validator.validate_console_path(path)
            assert result.is_valid
    
    def test_valid_ec2_pattern(self, validator):
        """유효한 EC2 패턴"""
        paths = [
            "EC2 > Instances",
            "EC2 > Volumes",
            "EC2 > Security Groups",
            "EC2 > Load Balancers"
        ]
        
        for path in paths:
            result = validator.validate_console_path(path)
            assert result.is_valid
    
    def test_empty_path(self, validator):
        """빈 경로 검증"""
        result = validator.validate_console_path("")
        
        assert not result.is_valid
        assert result.severity == ValidationSeverity.ERROR
        assert "비어있습니다" in result.message
    
    def test_unknown_pattern(self, validator):
        """알 수 없는 패턴"""
        path = "Unknown > Pattern > Here"
        result = validator.validate_console_path(path)
        
        assert not result.is_valid
        assert result.severity == ValidationSeverity.WARNING
        assert "알 수 없는" in result.message
    
    def test_line_number_tracking(self, validator):
        """라인 번호 추적"""
        path = "Services > Compute > EC2"
        result = validator.validate_console_path(path, line_number=42)
        
        assert result.line_number == 42
    
    def test_extract_console_paths_from_markdown(self, validator):
        """마크다운에서 Console 경로 추출"""
        markdown = """
# 실습 가이드

Console 경로: Services > Compute > EC2

다른 내용...

Console path: IAM > Users
"""
        
        paths = validator.extract_console_paths_from_markdown(markdown)
        
        assert len(paths) == 2
        assert paths[0][0] == "Services > Compute > EC2"
        assert paths[1][0] == "IAM > Users"
        assert paths[0][1] == 4  # Line number (첫 빈 줄 포함)
        assert paths[1][1] == 8


class TestMermaidValidator:
    """Mermaid 다이어그램 검증기 테스트"""
    
    @pytest.fixture
    def validator(self):
        """검증기 인스턴스"""
        return MermaidValidator()
    
    def test_valid_graph_diagram(self, validator):
        """유효한 graph 다이어그램"""
        mermaid = """graph TD
    A[Start] --> B[Process]
    B --> C[End]
"""
        
        results = validator.validate_mermaid_syntax(mermaid)
        
        # 다이어그램 유형과 방향 검증 결과
        assert len(results) >= 2
        assert any(r.is_valid and "graph" in r.message.lower() for r in results)
    
    def test_valid_flowchart_diagram(self, validator):
        """유효한 flowchart 다이어그램"""
        mermaid = """flowchart LR
    A --> B
    B --> C
"""
        
        results = validator.validate_mermaid_syntax(mermaid)
        
        assert len(results) >= 2
        assert any(r.is_valid and "flowchart" in r.message.lower() for r in results)
    
    def test_valid_sequence_diagram(self, validator):
        """유효한 sequenceDiagram"""
        mermaid = """sequenceDiagram
    Alice->>Bob: Hello
    Bob->>Alice: Hi
"""
        
        results = validator.validate_mermaid_syntax(mermaid)
        
        assert len(results) >= 1
        assert any(r.is_valid and "sequencediagram" in r.message.lower() for r in results)
    
    def test_invalid_diagram_type(self, validator):
        """유효하지 않은 다이어그램 유형"""
        mermaid = """invalidtype TD
    A --> B
"""
        
        results = validator.validate_mermaid_syntax(mermaid)
        
        assert len(results) >= 1
        assert any(not r.is_valid and r.severity == ValidationSeverity.ERROR for r in results)
    
    def test_invalid_graph_direction(self, validator):
        """유효하지 않은 그래프 방향"""
        mermaid = """graph XY
    A --> B
"""
        
        results = validator.validate_mermaid_syntax(mermaid)
        
        # 다이어그램 유형은 유효하지만 방향이 유효하지 않음
        assert any(r.severity == ValidationSeverity.WARNING for r in results)
    
    def test_empty_mermaid_code(self, validator):
        """빈 Mermaid 코드"""
        results = validator.validate_mermaid_syntax("")
        
        assert len(results) == 1
        assert not results[0].is_valid
        assert results[0].severity == ValidationSeverity.ERROR
    
    def test_bracket_balance_valid(self, validator):
        """괄호 균형 - 유효"""
        mermaid = """graph TD
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[End]
"""
        
        results = validator.validate_mermaid_syntax(mermaid)
        
        # 괄호 불균형 에러가 없어야 함
        assert not any(not r.is_valid and "불균형" in r.message for r in results)
    
    def test_bracket_balance_invalid(self, validator):
        """괄호 균형 - 유효하지 않음"""
        mermaid = """graph TD
    A[Start --> B[Process
    B --> C[End]
"""
        
        results = validator.validate_mermaid_syntax(mermaid)
        
        # 괄호 불균형 에러가 있어야 함
        assert any(not r.is_valid and "불균형" in r.message for r in results)
    
    def test_extract_mermaid_diagrams_from_markdown(self, validator):
        """마크다운에서 Mermaid 다이어그램 추출"""
        markdown = """
# 아키텍처

```mermaid
graph TD
    A --> B
```

다른 내용...

```mermaid
sequenceDiagram
    Alice->>Bob: Hello
```
"""
        
        diagrams = validator.extract_mermaid_diagrams_from_markdown(markdown)
        
        assert len(diagrams) == 2
        assert "graph TD" in diagrams[0][0]
        assert "sequenceDiagram" in diagrams[1][0]


class TestContentValidator:
    """통합 콘텐츠 검증기 테스트"""
    
    @pytest.fixture
    def validator(self):
        """검증기 인스턴스"""
        return ContentValidator()
    
    def test_validate_markdown_with_console_paths(self, validator):
        """Console 경로가 있는 마크다운 검증"""
        content = """
# 실습 가이드

Console 경로: Services > Compute > EC2

## 단계

1. EC2 인스턴스 생성
"""
        
        report = validator.validate_markdown_file("test.md", content)
        
        assert report.file_path == "test.md"
        assert report.total_checks >= 1
        assert report.passed >= 1
    
    def test_validate_markdown_with_mermaid(self, validator):
        """Mermaid 다이어그램이 있는 마크다운 검증"""
        content = """
# 아키텍처

```mermaid
graph TD
    A[Start] --> B[End]
```
"""
        
        report = validator.validate_markdown_file("test.md", content)
        
        assert report.total_checks >= 2  # 다이어그램 유형 + 방향
        assert report.passed >= 2
    
    def test_validate_markdown_with_errors(self, validator):
        """에러가 있는 마크다운 검증"""
        content = """
# 실습 가이드

Console 경로: 

```mermaid
invalidtype TD
    A --> B
```
"""
        
        report = validator.validate_markdown_file("test.md", content)
        
        assert report.failed >= 2  # 빈 경로 + 유효하지 않은 다이어그램 유형
    
    def test_validation_report_statistics(self, validator):
        """검증 리포트 통계"""
        content = """
Console 경로: Services > Compute > EC2
Console path: IAM > Users

```mermaid
graph TD
    A --> B
```
"""
        
        report = validator.validate_markdown_file("test.md", content)
        
        assert report.total_checks > 0
        assert report.success_rate >= 0.0
        assert report.success_rate <= 100.0
    
    def test_empty_content(self, validator):
        """빈 콘텐츠 검증"""
        report = validator.validate_markdown_file("empty.md", "")
        
        assert report.total_checks == 0
        assert report.passed == 0
        assert report.failed == 0


class TestValidationResult:
    """ValidationResult 데이터클래스 테스트"""
    
    def test_validation_result_creation(self):
        """ValidationResult 생성"""
        result = ValidationResult(
            is_valid=True,
            severity=ValidationSeverity.INFO,
            message="Test message",
            line_number=10,
            suggestion="Test suggestion"
        )
        
        assert result.is_valid
        assert result.severity == ValidationSeverity.INFO
        assert result.message == "Test message"
        assert result.line_number == 10
        assert result.suggestion == "Test suggestion"
    
    def test_validation_result_optional_fields(self):
        """ValidationResult 선택적 필드"""
        result = ValidationResult(
            is_valid=False,
            severity=ValidationSeverity.ERROR,
            message="Error message"
        )
        
        assert not result.is_valid
        assert result.line_number is None
        assert result.suggestion is None


class TestContentValidationReport:
    """ContentValidationReport 데이터클래스 테스트"""
    
    def test_report_creation(self):
        """리포트 생성"""
        results = [
            ValidationResult(True, ValidationSeverity.INFO, "Pass 1"),
            ValidationResult(True, ValidationSeverity.INFO, "Pass 2"),
            ValidationResult(False, ValidationSeverity.ERROR, "Fail 1"),
            ValidationResult(False, ValidationSeverity.WARNING, "Warn 1")
        ]
        
        report = ContentValidationReport(
            file_path="test.md",
            total_checks=4,
            passed=2,
            failed=1,
            warnings=1,
            results=results
        )
        
        assert report.file_path == "test.md"
        assert report.total_checks == 4
        assert report.passed == 2
        assert report.failed == 1
        assert report.warnings == 1
        assert len(report.results) == 4
    
    def test_success_rate_calculation(self):
        """성공률 계산"""
        report = ContentValidationReport(
            file_path="test.md",
            total_checks=10,
            passed=8,
            failed=2,
            warnings=0,
            results=[]
        )
        
        assert report.success_rate == 80.0
    
    def test_success_rate_zero_checks(self):
        """체크가 0개일 때 성공률"""
        report = ContentValidationReport(
            file_path="test.md",
            total_checks=0,
            passed=0,
            failed=0,
            warnings=0,
            results=[]
        )
        
        assert report.success_rate == 0.0


class TestValidationSeverity:
    """ValidationSeverity Enum 테스트"""
    
    def test_severity_values(self):
        """심각도 값"""
        assert ValidationSeverity.ERROR.value == "error"
        assert ValidationSeverity.WARNING.value == "warning"
        assert ValidationSeverity.INFO.value == "info"
    
    def test_severity_comparison(self):
        """심각도 비교"""
        error = ValidationSeverity.ERROR
        warning = ValidationSeverity.WARNING
        info = ValidationSeverity.INFO
        
        assert error != warning
        assert warning != info
        assert error != info


class TestConsolePathPatterns:
    """Console 경로 패턴 테스트"""
    
    @pytest.fixture
    def validator(self):
        return ConsolePathValidator()
    
    def test_s3_pattern(self, validator):
        """S3 패턴"""
        result = validator.validate_console_path("S3 > Buckets")
        assert result.is_valid
    
    def test_rds_pattern(self, validator):
        """RDS 패턴"""
        paths = [
            "RDS > Databases",
            "RDS > Snapshots",
            "RDS > Parameter Groups"
        ]
        
        for path in paths:
            result = validator.validate_console_path(path)
            assert result.is_valid
    
    def test_cloudwatch_pattern(self, validator):
        """CloudWatch 패턴"""
        paths = [
            "CloudWatch > Metrics",
            "CloudWatch > Alarms",
            "CloudWatch > Logs"
        ]
        
        for path in paths:
            result = validator.validate_console_path(path)
            assert result.is_valid
    
    def test_lambda_pattern(self, validator):
        """Lambda 패턴"""
        result = validator.validate_console_path("Lambda > Functions")
        assert result.is_valid


class TestMermaidDiagramTypes:
    """Mermaid 다이어그램 유형 테스트"""
    
    @pytest.fixture
    def validator(self):
        return MermaidValidator()
    
    def test_all_valid_diagram_types(self, validator):
        """모든 유효한 다이어그램 유형"""
        diagram_types = [
            "graph TD",
            "flowchart LR",
            "sequenceDiagram",
            "classDiagram",
            "stateDiagram",
            "erDiagram",
            "gantt",
            "pie",
            "journey"
        ]
        
        for dtype in diagram_types:
            mermaid = f"{dtype}\n    A --> B"
            results = validator.validate_mermaid_syntax(mermaid)
            
            # 다이어그램 유형이 유효해야 함
            assert any(r.is_valid for r in results)
    
    def test_graph_directions(self, validator):
        """그래프 방향"""
        directions = ["TB", "TD", "BT", "RL", "LR"]
        
        for direction in directions:
            mermaid = f"graph {direction}\n    A --> B"
            results = validator.validate_mermaid_syntax(mermaid)
            
            # 방향이 유효해야 함
            assert any(r.is_valid and direction in r.message for r in results)
