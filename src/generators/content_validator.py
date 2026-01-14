# Content Validator
"""
콘텐츠 검증기
Console 경로 유효성 검증 및 Mermaid 다이어그램 구문 검증
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ValidationSeverity(Enum):
    """검증 심각도"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    """검증 결과"""
    is_valid: bool
    severity: ValidationSeverity
    message: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class ContentValidationReport:
    """콘텐츠 검증 리포트"""
    file_path: str
    total_checks: int
    passed: int
    failed: int
    warnings: int
    results: List[ValidationResult]
    
    @property
    def success_rate(self) -> float:
        """성공률 계산"""
        if self.total_checks == 0:
            return 0.0
        return (self.passed / self.total_checks) * 100


class ConsolePathValidator:
    """AWS Console 경로 검증기"""
    
    # 유효한 AWS Console 경로 패턴
    VALID_CONSOLE_PATTERNS = [
        # 기본 패턴: Services > Category > Service
        r"^Services\s*>\s*[\w\s&]+\s*>\s*[\w\s&]+",
        # IAM 패턴
        r"^IAM\s*>\s*(Users|Roles|Policies|Groups)",
        # VPC 패턴
        r"^VPC\s*>\s*(Subnets|Route Tables|Internet Gateways|NAT Gateways|Security Groups|Network ACLs)",
        # EC2 패턴
        r"^EC2\s*>\s*(Instances|AMIs|Volumes|Snapshots|Security Groups|Key Pairs|Load Balancers)",
        # S3 패턴
        r"^S3\s*>\s*Buckets",
        # RDS 패턴
        r"^RDS\s*>\s*(Databases|Snapshots|Parameter Groups|Subnet Groups)",
        # CloudWatch 패턴
        r"^CloudWatch\s*>\s*(Metrics|Alarms|Logs|Dashboards|Events)",
        # Lambda 패턴
        r"^Lambda\s*>\s*(Functions|Layers|Applications)",
        # API Gateway 패턴
        r"^API Gateway\s*>\s*(APIs|Custom Domain Names|API Keys)",
        # DynamoDB 패턴
        r"^DynamoDB\s*>\s*(Tables|Backups|Reserved Capacity)",
        # CloudFormation 패턴
        r"^CloudFormation\s*>\s*(Stacks|StackSets)",
        # CloudTrail 패턴
        r"^CloudTrail\s*>\s*(Trails|Event History)",
        # Config 패턴
        r"^Config\s*>\s*(Rules|Conformance Packs|Aggregators)",
        # Systems Manager 패턴
        r"^Systems Manager\s*>\s*(Parameter Store|Session Manager|Patch Manager|State Manager)",
        # Billing 패턴
        r"^Billing\s*>\s*(Bills|Cost Explorer|Budgets|Cost Allocation Tags)",
    ]
    
    # 알려진 AWS 서비스 카테고리
    KNOWN_CATEGORIES = [
        "Compute", "Storage", "Database", "Networking & Content Delivery",
        "Security, Identity, & Compliance", "Management & Governance",
        "Analytics", "Application Integration", "Developer Tools",
        "Machine Learning", "Migration & Transfer", "Mobile"
    ]
    
    # 알려진 AWS 서비스
    KNOWN_SERVICES = [
        "EC2", "S3", "RDS", "Lambda", "DynamoDB", "VPC", "IAM",
        "CloudWatch", "CloudFront", "Route 53", "ELB", "Auto Scaling",
        "CloudFormation", "CloudTrail", "Config", "Systems Manager",
        "API Gateway", "SQS", "SNS", "EventBridge", "Step Functions",
        "ECS", "EKS", "Fargate", "Elastic Beanstalk", "Kinesis",
        "Athena", "Glue", "EMR", "SageMaker", "Rekognition"
    ]
    
    def validate_console_path(self, path: str, line_number: Optional[int] = None) -> ValidationResult:
        """Console 경로 검증
        
        Args:
            path: Console 경로 문자열
            line_number: 라인 번호 (선택사항)
            
        Returns:
            ValidationResult 객체
        """
        # 빈 경로 체크
        if not path or not path.strip():
            return ValidationResult(
                is_valid=False,
                severity=ValidationSeverity.ERROR,
                message="Console 경로가 비어있습니다",
                line_number=line_number,
                suggestion="유효한 Console 경로를 입력하세요 (예: Services > Compute > EC2)"
            )
        
        # 패턴 매칭
        path_clean = path.strip()
        for pattern in self.VALID_CONSOLE_PATTERNS:
            if re.match(pattern, path_clean, re.IGNORECASE):
                return ValidationResult(
                    is_valid=True,
                    severity=ValidationSeverity.INFO,
                    message=f"유효한 Console 경로: {path_clean}",
                    line_number=line_number
                )
        
        # 패턴에 매칭되지 않으면 경고
        return ValidationResult(
            is_valid=False,
            severity=ValidationSeverity.WARNING,
            message=f"알 수 없는 Console 경로 형식: {path_clean}",
            line_number=line_number,
            suggestion="표준 Console 경로 형식을 사용하세요 (예: Services > Category > Service)"
        )
    
    def extract_console_paths_from_markdown(self, content: str) -> List[Tuple[str, int]]:
        """마크다운 콘텐츠에서 Console 경로 추출
        
        Args:
            content: 마크다운 콘텐츠
            
        Returns:
            (경로, 라인번호) 튜플 리스트
        """
        paths = []
        lines = content.split('\n')
        
        # "Console 경로:" 또는 "Console path:" 패턴 찾기
        console_path_pattern = r"(?:Console\s+(?:경로|path)):\s*(.+)"
        
        for i, line in enumerate(lines, 1):
            match = re.search(console_path_pattern, line, re.IGNORECASE)
            if match:
                path = match.group(1).strip()
                paths.append((path, i))
        
        return paths


class MermaidValidator:
    """Mermaid 다이어그램 구문 검증기"""
    
    # 유효한 Mermaid 다이어그램 유형
    VALID_DIAGRAM_TYPES = [
        "graph", "flowchart", "sequenceDiagram", "classDiagram",
        "stateDiagram", "erDiagram", "gantt", "pie", "journey",
        "gitGraph", "mindmap", "timeline", "sankey-beta"
    ]
    
    # 그래프 방향
    VALID_GRAPH_DIRECTIONS = ["TB", "TD", "BT", "RL", "LR"]
    
    def validate_mermaid_syntax(self, mermaid_code: str, line_number: Optional[int] = None) -> List[ValidationResult]:
        """Mermaid 구문 검증
        
        Args:
            mermaid_code: Mermaid 다이어그램 코드
            line_number: 시작 라인 번호 (선택사항)
            
        Returns:
            ValidationResult 리스트
        """
        results = []
        
        # 빈 코드 체크
        if not mermaid_code or not mermaid_code.strip():
            results.append(ValidationResult(
                is_valid=False,
                severity=ValidationSeverity.ERROR,
                message="Mermaid 코드가 비어있습니다",
                line_number=line_number
            ))
            return results
        
        lines = mermaid_code.strip().split('\n')
        
        # 첫 줄에서 다이어그램 유형 확인
        first_line = lines[0].strip()
        diagram_type = None
        
        for dtype in self.VALID_DIAGRAM_TYPES:
            if first_line.startswith(dtype):
                diagram_type = dtype
                break
        
        if not diagram_type:
            results.append(ValidationResult(
                is_valid=False,
                severity=ValidationSeverity.ERROR,
                message=f"알 수 없는 다이어그램 유형: {first_line}",
                line_number=line_number,
                suggestion=f"유효한 다이어그램 유형: {', '.join(self.VALID_DIAGRAM_TYPES)}"
            ))
            return results
        
        results.append(ValidationResult(
            is_valid=True,
            severity=ValidationSeverity.INFO,
            message=f"유효한 다이어그램 유형: {diagram_type}",
            line_number=line_number
        ))
        
        # 그래프/플로우차트 방향 검증
        if diagram_type in ["graph", "flowchart"]:
            direction_match = re.search(r"(graph|flowchart)\s+(\w+)", first_line)
            if direction_match:
                direction = direction_match.group(2)
                if direction not in self.VALID_GRAPH_DIRECTIONS:
                    results.append(ValidationResult(
                        is_valid=False,
                        severity=ValidationSeverity.WARNING,
                        message=f"알 수 없는 그래프 방향: {direction}",
                        line_number=line_number,
                        suggestion=f"유효한 방향: {', '.join(self.VALID_GRAPH_DIRECTIONS)}"
                    ))
                else:
                    results.append(ValidationResult(
                        is_valid=True,
                        severity=ValidationSeverity.INFO,
                        message=f"유효한 그래프 방향: {direction}",
                        line_number=line_number
                    ))
        
        # 기본 구문 검증
        self._validate_basic_syntax(lines, results, line_number)
        
        return results
    
    def _validate_basic_syntax(self, lines: List[str], results: List[ValidationResult], start_line: Optional[int]):
        """기본 구문 검증
        
        Args:
            lines: 코드 라인 리스트
            results: 결과 리스트 (수정됨)
            start_line: 시작 라인 번호
        """
        # 괄호 균형 체크
        open_brackets = 0
        open_parens = 0
        open_braces = 0
        
        for i, line in enumerate(lines, 1):
            line_num = (start_line or 0) + i
            
            # 주석 제거
            if '%' in line:
                line = line[:line.index('%')]
            
            # 괄호 카운트
            open_brackets += line.count('[') - line.count(']')
            open_parens += line.count('(') - line.count(')')
            open_braces += line.count('{') - line.count('}')
            
            # 화살표 구문 체크 (graph/flowchart)
            if '-->' in line or '---' in line or '==>' in line or '-.>' in line:
                # 유효한 화살표 구문
                pass
            
            # subgraph 구문 체크
            if 'subgraph' in line.lower():
                if not re.search(r'subgraph\s+["\w]', line, re.IGNORECASE):
                    results.append(ValidationResult(
                        is_valid=False,
                        severity=ValidationSeverity.WARNING,
                        message=f"subgraph 구문이 올바르지 않을 수 있습니다: {line.strip()}",
                        line_number=line_num,
                        suggestion="subgraph 다음에 이름을 지정하세요 (예: subgraph \"Name\")"
                    ))
        
        # 최종 괄호 균형 체크
        if open_brackets != 0:
            results.append(ValidationResult(
                is_valid=False,
                severity=ValidationSeverity.ERROR,
                message=f"대괄호 불균형: {abs(open_brackets)}개 {'열림' if open_brackets > 0 else '닫힘'}",
                suggestion="모든 대괄호가 올바르게 닫혔는지 확인하세요"
            ))
        
        if open_parens != 0:
            results.append(ValidationResult(
                is_valid=False,
                severity=ValidationSeverity.ERROR,
                message=f"소괄호 불균형: {abs(open_parens)}개 {'열림' if open_parens > 0 else '닫힘'}",
                suggestion="모든 소괄호가 올바르게 닫혔는지 확인하세요"
            ))
        
        if open_braces != 0:
            results.append(ValidationResult(
                is_valid=False,
                severity=ValidationSeverity.ERROR,
                message=f"중괄호 불균형: {abs(open_braces)}개 {'열림' if open_braces > 0 else '닫힘'}",
                suggestion="모든 중괄호가 올바르게 닫혔는지 확인하세요"
            ))
    
    def extract_mermaid_diagrams_from_markdown(self, content: str) -> List[Tuple[str, int]]:
        """마크다운 콘텐츠에서 Mermaid 다이어그램 추출
        
        Args:
            content: 마크다운 콘텐츠
            
        Returns:
            (다이어그램 코드, 시작 라인번호) 튜플 리스트
        """
        diagrams = []
        lines = content.split('\n')
        
        in_mermaid_block = False
        current_diagram = []
        start_line = 0
        
        for i, line in enumerate(lines, 1):
            if '```mermaid' in line.lower():
                in_mermaid_block = True
                start_line = i + 1
                current_diagram = []
            elif in_mermaid_block and '```' in line:
                in_mermaid_block = False
                if current_diagram:
                    diagrams.append(('\n'.join(current_diagram), start_line))
                current_diagram = []
            elif in_mermaid_block:
                current_diagram.append(line)
        
        return diagrams


class ContentValidator:
    """통합 콘텐츠 검증기"""
    
    def __init__(self):
        self.console_validator = ConsolePathValidator()
        self.mermaid_validator = MermaidValidator()
    
    def validate_markdown_file(self, file_path: str, content: str) -> ContentValidationReport:
        """마크다운 파일 전체 검증
        
        Args:
            file_path: 파일 경로
            content: 파일 콘텐츠
            
        Returns:
            ContentValidationReport 객체
        """
        all_results = []
        
        # Console 경로 검증
        console_paths = self.console_validator.extract_console_paths_from_markdown(content)
        for path, line_num in console_paths:
            result = self.console_validator.validate_console_path(path, line_num)
            all_results.append(result)
        
        # Mermaid 다이어그램 검증
        mermaid_diagrams = self.mermaid_validator.extract_mermaid_diagrams_from_markdown(content)
        for diagram, line_num in mermaid_diagrams:
            results = self.mermaid_validator.validate_mermaid_syntax(diagram, line_num)
            all_results.extend(results)
        
        # 통계 계산
        total_checks = len(all_results)
        passed = sum(1 for r in all_results if r.is_valid and r.severity == ValidationSeverity.INFO)
        failed = sum(1 for r in all_results if not r.is_valid and r.severity == ValidationSeverity.ERROR)
        warnings = sum(1 for r in all_results if r.severity == ValidationSeverity.WARNING)
        
        return ContentValidationReport(
            file_path=file_path,
            total_checks=total_checks,
            passed=passed,
            failed=failed,
            warnings=warnings,
            results=all_results
        )
    
    def validate_case_study_content(self, content: str) -> bool:
        """사례 연구 콘텐츠 검증
        
        Args:
            content: 사례 연구 마크다운 콘텐츠
            
        Returns:
            검증 성공 여부
        """
        # 필수 섹션 확인
        required_sections = [
            "사례 개요",
            "비즈니스 도전과제",
            "AWS 솔루션 아키텍처",
            "구현 세부사항",
            "비즈니스 임팩트"
        ]
        
        for section in required_sections:
            if section not in content:
                return False
        
        # 최소 길이 확인
        if len(content) < 500:
            return False
        
        return True
    
    def print_validation_report(self, report: ContentValidationReport):
        """검증 리포트 출력
        
        Args:
            report: ContentValidationReport 객체
        """
        print(f"\n{'='*60}")
        print(f"Content Validation Report: {report.file_path}")
        print(f"{'='*60}\n")
        
        print(f"Total Checks: {report.total_checks}")
        print(f"Passed: {report.passed} ✓")
        print(f"Failed: {report.failed} ✗")
        print(f"Warnings: {report.warnings} ⚠")
        print(f"Success Rate: {report.success_rate:.1f}%\n")
        
        # 에러 출력
        errors = [r for r in report.results if r.severity == ValidationSeverity.ERROR]
        if errors:
            print(f"{'='*60}")
            print("ERRORS:")
            print(f"{'='*60}")
            for result in errors:
                line_info = f" (Line {result.line_number})" if result.line_number else ""
                print(f"✗ {result.message}{line_info}")
                if result.suggestion:
                    print(f"  → Suggestion: {result.suggestion}")
                print()
        
        # 경고 출력
        warnings = [r for r in report.results if r.severity == ValidationSeverity.WARNING]
        if warnings:
            print(f"{'='*60}")
            print("WARNINGS:")
            print(f"{'='*60}")
            for result in warnings:
                line_info = f" (Line {result.line_number})" if result.line_number else ""
                print(f"⚠ {result.message}{line_info}")
                if result.suggestion:
                    print(f"  → Suggestion: {result.suggestion}")
                print()
        
        print(f"{'='*60}\n")


def main():
    """CLI 실행 예시"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python content_validator.py <markdown_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        validator = ContentValidator()
        report = validator.validate_markdown_file(file_path, content)
        validator.print_validation_report(report)
        
        # 에러가 있으면 종료 코드 1 반환
        sys.exit(1 if report.failed > 0 else 0)
        
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
