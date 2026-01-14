#!/usr/bin/env python3
"""
통합 시나리오 생성기 데모 스크립트
Task 8.2: 통합 시나리오 생성기 구현 검증
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.generators.integration_scenario_generator import (
    IntegrationScenarioGenerator,
    generate_integration_scenario,
    generate_all_integration_scenarios
)


def main():
    """메인 함수"""
    print("=" * 80)
    print("통합 시나리오 생성기 데모")
    print("Task 8.2: 통합 시나리오 생성기")
    print("=" * 80)
    print()
    
    # 생성기 초기화
    print("1. 통합 시나리오 생성기 초기화...")
    generator = IntegrationScenarioGenerator()
    print(f"   ✓ 생성기 초기화 완료")
    print(f"   ✓ 총 {len(generator.scenarios)}개 시나리오 발견")
    print()
    
    # 시나리오 목록 출력
    print("2. 사용 가능한 통합 시나리오:")
    print()
    for i, scenario in enumerate(generator.scenarios, 1):
        print(f"   {i}. {scenario.name}")
        print(f"      - ID: {scenario.scenario_id}")
        print(f"      - 설명: {scenario.description}")
        print(f"      - 관련 일차: {', '.join([f'Day {d}' for d in scenario.involved_days])}")
        print(f"      - 사용 사례: {scenario.use_case}")
        print()
    
    # 모든 시나리오 문서 생성
    print("3. 모든 통합 시나리오 문서 생성...")
    output_dir = project_root / "aws-saa-study-materials" / "integration-scenarios"
    
    try:
        generated_files = generate_all_integration_scenarios(output_dir)
        print(f"   ✓ {len(generated_files)}개 파일 생성 완료")
        print()
        
        print("4. 생성된 파일 목록:")
        for file_path in generated_files:
            relative_path = file_path.relative_to(project_root)
            file_size = file_path.stat().st_size
            print(f"   - {relative_path} ({file_size:,} bytes)")
        print()
        
        # 샘플 시나리오 내용 미리보기
        print("5. 샘플 시나리오 미리보기 (Netflix 글로벌 스트리밍):")
        print()
        netflix_file = output_dir / "netflix_streaming.md"
        if netflix_file.exists():
            with open(netflix_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # 첫 30줄만 출력
                for line in lines[:30]:
                    print(f"   {line.rstrip()}")
                if len(lines) > 30:
                    print(f"   ... (총 {len(lines)}줄 중 30줄 표시)")
        print()
        
        # 통계 정보
        print("6. 생성 통계:")
        total_size = sum(f.stat().st_size for f in generated_files)
        print(f"   - 총 파일 수: {len(generated_files)}")
        print(f"   - 총 파일 크기: {total_size:,} bytes ({total_size / 1024:.2f} KB)")
        print(f"   - 출력 디렉토리: {output_dir.relative_to(project_root)}")
        print()
        
        print("=" * 80)
        print("✓ 통합 시나리오 생성 완료!")
        print("=" * 80)
        print()
        print("다음 단계:")
        print("1. 생성된 문서 검토: aws-saa-study-materials/integration-scenarios/")
        print("2. 각 시나리오의 학습 경로 확인")
        print("3. 관련 일차 학습 자료와 연계하여 학습")
        print()
        
        return 0
        
    except Exception as e:
        print(f"   ✗ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
