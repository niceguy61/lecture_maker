#!/usr/bin/env python3
"""
AWS 문서 연동 및 검증 시스템 데모
Task 9.1 & 9.2 구현 데모
"""

from src.generators.aws_docs_link_generator import AWSDocsLinkGenerator
from src.generators.content_validator import ContentValidator


def demo_aws_docs_link_generator():
    """AWS 문서 링크 생성기 데모"""
    print("=" * 80)
    print("AWS 문서 링크 생성기 데모")
    print("=" * 80)
    print()
    
    generator = AWSDocsLinkGenerator()
    
    # 1. 서비스 문서 링크 생성
    print("1. 서비스 문서 링크 생성")
    print("-" * 80)
    services = ["EC2", "S3", "RDS", "Lambda", "VPC"]
    for service in services:
        link = generator.generate_service_doc_link(service)
        print(f"  {service}: {link}")
    print()
    
    # 2. Well-Architected Framework 링크
    print("2. Well-Architected Framework 링크")
    print("-" * 80)
    pillars = [
        ("operational_excellence", "운영 우수성"),
        ("security", "보안"),
        ("reliability", "안정성"),
        ("performance_efficiency", "성능 효율성"),
        ("cost_optimization", "비용 최적화"),
        ("sustainability", "지속 가능성")
    ]
    for pillar_key, pillar_name in pillars:
        link = generator.generate_well_architected_link(pillar_key)
        print(f"  {pillar_name}: {link}")
    print()
    
    # 3. 포괄적인 링크 생성
    print("3. 포괄적인 링크 생성 (Netflix 사례)")
    print("-" * 80)
    services = ["EC2", "S3", "CloudFront"]
    links = generator.generate_comprehensive_links(
        service_names=services,
        company_name="Netflix"
    )
    
    print(f"  서비스 문서: {len(links.service_docs)}개")
    print(f"  API 레퍼런스: {len(links.api_references)}개")
    print(f"  Well-Architected: {len(links.well_architected)}개")
    print(f"  가격 정보: {len(links.pricing_links)}개")
    print(f"  화이트페이퍼: {len(links.whitepapers)}개")
    print(f"  사례 연구: {len(links.case_studies)}개")
    print()
    
    # 4. 마크다운 형식 출력
    print("4. 마크다운 형식 출력")
    print("-" * 80)
    markdown = generator.format_links_as_markdown(links)
    print(markdown[:500] + "...")
    print()


def demo_content_validator():
    """콘텐츠 검증기 데모"""
    print("=" * 80)
    print("콘텐츠 검증기 데모")
    print("=" * 80)
    print()
    
    validator = ContentValidator()
    
    # 샘플 마크다운 콘텐츠
    sample_content = """
# AWS EC2 실습 가이드

## 사전 요구사항
- AWS 계정
- IAM 사용자 권한

## 실습 단계

### 1. EC2 인스턴스 생성

Console 경로: Services > Compute > EC2

1. EC2 대시보드로 이동
2. "Launch Instance" 클릭
3. AMI 선택

### 2. 보안 그룹 설정

Console 경로: EC2 > Security Groups

보안 그룹 규칙을 설정합니다.

## 아키텍처 다이어그램

```mermaid
graph TD
    A[User] --> B[Internet Gateway]
    B --> C[Public Subnet]
    C --> D[EC2 Instance]
    D --> E[Private Subnet]
    E --> F[RDS Database]
```

## 데이터 플로우

```mermaid
sequenceDiagram
    User->>EC2: HTTP Request
    EC2->>RDS: Query Database
    RDS->>EC2: Return Data
    EC2->>User: HTTP Response
```

## 잘못된 예시 (테스트용)

Console 경로: 

```mermaid
invalidtype TD
    A --> B
```
"""
    
    # 검증 실행
    print("1. 마크다운 콘텐츠 검증")
    print("-" * 80)
    report = validator.validate_markdown_file("sample.md", sample_content)
    
    print(f"파일: {report.file_path}")
    print(f"총 검사 항목: {report.total_checks}")
    print(f"통과: {report.passed} ✓")
    print(f"실패: {report.failed} ✗")
    print(f"경고: {report.warnings} ⚠")
    print(f"성공률: {report.success_rate:.1f}%")
    print()
    
    # 에러 및 경고 출력
    if report.failed > 0 or report.warnings > 0:
        print("2. 검증 결과 상세")
        print("-" * 80)
        
        for result in report.results:
            if not result.is_valid or result.severity.value == "warning":
                severity_icon = {
                    "error": "✗",
                    "warning": "⚠",
                    "info": "ℹ"
                }.get(result.severity.value, "?")
                
                line_info = f" (Line {result.line_number})" if result.line_number else ""
                print(f"{severity_icon} {result.message}{line_info}")
                if result.suggestion:
                    print(f"  → {result.suggestion}")
        print()
    
    # Console 경로 검증 예시
    print("3. Console 경로 검증 예시")
    print("-" * 80)
    console_paths = [
        "Services > Compute > EC2",
        "IAM > Users",
        "VPC > Subnets",
        "Invalid > Path > Here"
    ]
    
    for path in console_paths:
        result = validator.console_validator.validate_console_path(path)
        status = "✓" if result.is_valid else "✗"
        print(f"{status} {path}")
    print()
    
    # Mermaid 다이어그램 검증 예시
    print("4. Mermaid 다이어그램 검증 예시")
    print("-" * 80)
    
    valid_diagram = """graph TD
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[End]
"""
    
    invalid_diagram = """graph XY
    A[Start --> B[Process
"""
    
    print("유효한 다이어그램:")
    results = validator.mermaid_validator.validate_mermaid_syntax(valid_diagram)
    for result in results:
        if result.is_valid:
            print(f"  ✓ {result.message}")
    print()
    
    print("유효하지 않은 다이어그램:")
    results = validator.mermaid_validator.validate_mermaid_syntax(invalid_diagram)
    for result in results:
        if not result.is_valid:
            print(f"  ✗ {result.message}")
            if result.suggestion:
                print(f"    → {result.suggestion}")
    print()


def main():
    """메인 함수"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "AWS 문서 연동 및 검증 시스템 데모" + " " * 24 + "║")
    print("║" + " " * 25 + "Task 9.1 & 9.2 구현" + " " * 33 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    # AWS 문서 링크 생성기 데모
    demo_aws_docs_link_generator()
    
    print("\n" + "=" * 80 + "\n")
    
    # 콘텐츠 검증기 데모
    demo_content_validator()
    
    print("\n")
    print("=" * 80)
    print("데모 완료!")
    print("=" * 80)
    print()
    print("구현된 기능:")
    print("  ✓ AWS 문서 링크 생성기 (60+ 서비스 지원)")
    print("  ✓ Well-Architected Framework 링크 (6개 기둥)")
    print("  ✓ 가격 계산기 및 화이트페이퍼 링크")
    print("  ✓ Console 경로 유효성 검증 (15+ 패턴)")
    print("  ✓ Mermaid 다이어그램 구문 검증 (13개 다이어그램 유형)")
    print("  ✓ 마크다운 콘텐츠 통합 검증")
    print()


if __name__ == "__main__":
    main()
