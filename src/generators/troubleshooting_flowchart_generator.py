"""
Troubleshooting Flowchart Generator

각 일별 주제(Day 1-28)에 대한 트러블슈팅 플로우차트 생성
Console 기반 진단 단계를 Mermaid flowchart로 시각화
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from src.daily_topics import DAILY_TOPICS, get_topic_by_day
from src.config import STUDY_MATERIALS_ROOT


class TroubleshootingFlowchartGenerator:
    """트러블슈팅 플로우차트 생성기"""
    
    def __init__(self):
        self.study_materials_root = STUDY_MATERIALS_ROOT
        
    def _get_output_directory(self, day_number: int) -> Path:
        """일별 아키텍처 다이어그램 출력 디렉토리 경로 반환"""
        topic = get_topic_by_day(day_number)
        week_number = topic["week"]
        
        output_dir = (
            self.study_materials_root / 
            f"week{week_number}" / 
            f"day{day_number}" / 
            "advanced" / 
            "architecture-diagrams"
        )
        
        return output_dir
    
    def _ensure_directory_exists(self, directory: Path) -> None:
        """디렉토리가 존재하지 않으면 생성"""
        directory.mkdir(parents=True, exist_ok=True)
    
    def generate_diagnostic_flowchart(self, day_number: int) -> str:
        """
        일별 주요 서비스에 대한 진단 플로우차트 생성
        
        Args:
            day_number: 일차 (1-28)
            
        Returns:
            Mermaid flowchart 코드
        """
        topic = get_topic_by_day(day_number)
        primary_services = topic["primary_services"]
        service_name = primary_services[0] if primary_services else "AWS Service"
        
        flowchart = f"""flowchart TD
    Start[문제 발생:<br/>{service_name} 성능 저하] --> Check1{{CloudWatch<br/>메트릭 확인}}
    
    Check1 -->|비정상| Metric1[Console: CloudWatch > Metrics<br/>주요 메트릭 분석]
    Check1 -->|정상| Check2{{로그 확인}}
    
    Metric1 --> MetricAnalysis{{메트릭 유형?}}
    MetricAnalysis -->|CPU/메모리 높음| Fix1[리소스 스케일 업<br/>또는 스케일 아웃]
    MetricAnalysis -->|네트워크 지연| Fix2[네트워크 구성<br/>최적화]
    MetricAnalysis -->|에러율 증가| Check2
    
    Check2 -->|에러 발견| Log1[Console: CloudWatch > Log groups<br/>에러 패턴 분석]
    Check2 -->|정상| Check3{{네트워크<br/>연결 상태}}
    
    Log1 --> LogAnalysis{{에러 유형?}}
    LogAnalysis -->|애플리케이션 에러| Fix3[애플리케이션<br/>코드 수정]
    LogAnalysis -->|권한 에러| Fix4[IAM 권한<br/>검토 및 수정]
    LogAnalysis -->|리소스 부족| Fix1
    
    Check3 -->|연결 실패| Network1[Console: VPC > Security Groups<br/>보안 그룹 규칙 확인]
    Check3 -->|정상| Check4{{비용<br/>급증 확인}}
    
    Network1 --> NetworkFix{{문제 유형?}}
    NetworkFix -->|인바운드 규칙| Fix5[Security Group<br/>인바운드 규칙 수정]
    NetworkFix -->|아웃바운드 규칙| Fix6[Security Group<br/>아웃바운드 규칙 수정]
    NetworkFix -->|라우팅 문제| Fix7[Route Table<br/>라우팅 수정]
    
    Check4 -->|비용 급증| Cost1[Console: Billing > Cost Explorer<br/>비용 분석]
    Check4 -->|정상| Verify
    
    Cost1 --> CostAnalysis{{비용 원인?}}
    CostAnalysis -->|리소스 과다| Fix8[불필요한 리소스<br/>정리 및 최적화]
    CostAnalysis -->|데이터 전송| Fix9[데이터 전송<br/>최적화]
    CostAnalysis -->|스토리지| Fix10[스토리지 클래스<br/>최적화]
    
    Fix1 --> Verify[검증 및 모니터링]
    Fix2 --> Verify
    Fix3 --> Verify
    Fix4 --> Verify
    Fix5 --> Verify
    Fix6 --> Verify
    Fix7 --> Verify
    Fix8 --> Verify
    Fix9 --> Verify
    Fix10 --> Verify
    
    Verify --> Success{{해결됨?}}
    Success -->|Yes| Monitor[모니터링 강화<br/>알람 설정]
    Success -->|No| Escalate[AWS Support<br/>케이스 생성]
    
    Monitor --> End[완료]
    Escalate --> End
"""
        
        return flowchart
    
    def generate_performance_troubleshooting(self, day_number: int) -> str:
        """
        성능 문제 트러블슈팅 플로우차트 생성
        
        Args:
            day_number: 일차 (1-28)
            
        Returns:
            Mermaid flowchart 코드
        """
        topic = get_topic_by_day(day_number)
        primary_services = topic["primary_services"]
        service_name = primary_services[0] if primary_services else "AWS Service"
        
        flowchart = f"""flowchart TD
    Start[성능 저하 감지:<br/>{service_name}] --> Baseline{{기준선 메트릭<br/>확인}}
    
    Baseline -->|응답시간 증가| Latency[지연 시간 분석]
    Baseline -->|처리량 감소| Throughput[처리량 분석]
    Baseline -->|에러율 증가| ErrorRate[에러율 분석]
    
    Latency --> LatencyCheck{{지연 위치?}}
    LatencyCheck -->|네트워크| NetOpt[Console: VPC<br/>네트워크 최적화]
    LatencyCheck -->|컴퓨팅| CompOpt[Console: {service_name}<br/>리소스 증설]
    LatencyCheck -->|데이터베이스| DBOpt[Console: RDS/DynamoDB<br/>쿼리 최적화]
    
    Throughput --> ThroughputCheck{{병목 지점?}}
    ThroughputCheck -->|리소스 한계| Scale[Auto Scaling<br/>설정 조정]
    ThroughputCheck -->|동시성 제한| Concurrency[동시성 한도<br/>증가 요청]
    ThroughputCheck -->|큐 적체| Queue[Console: SQS<br/>큐 처리 최적화]
    
    ErrorRate --> ErrorCheck{{에러 유형?}}
    ErrorCheck -->|5xx 에러| ServerError[서버 리소스<br/>증설]
    ErrorCheck -->|4xx 에러| ClientError[클라이언트 요청<br/>검증 강화]
    ErrorCheck -->|타임아웃| Timeout[타임아웃 설정<br/>조정]
    
    NetOpt --> Implement[최적화 구현]
    CompOpt --> Implement
    DBOpt --> Implement
    Scale --> Implement
    Concurrency --> Implement
    Queue --> Implement
    ServerError --> Implement
    ClientError --> Implement
    Timeout --> Implement
    
    Implement --> Test[성능 테스트]
    Test --> Verify{{개선됨?}}
    
    Verify -->|Yes| Monitor[지속적 모니터링<br/>설정]
    Verify -->|No| RootCause[근본 원인<br/>재분석]
    
    RootCause --> Baseline
    Monitor --> End[완료]
"""
        
        return flowchart

    
    def generate_security_troubleshooting(self, day_number: int) -> str:
        """
        보안 문제 트러블슈팅 플로우차트 생성
        
        Args:
            day_number: 일차 (1-28)
            
        Returns:
            Mermaid flowchart 코드
        """
        topic = get_topic_by_day(day_number)
        primary_services = topic["primary_services"]
        service_name = primary_services[0] if primary_services else "AWS Service"
        
        flowchart = f"""flowchart TD
    Start[보안 이슈 감지:<br/>{service_name}] --> Identify{{이슈 유형?}}
    
    Identify -->|무단 접근 시도| Access[접근 로그 분석]
    Identify -->|권한 오류| Permission[권한 설정 검토]
    Identify -->|데이터 유출 위험| DataLeak[데이터 보호 검토]
    Identify -->|규정 위반| Compliance[컴플라이언스 검토]
    
    Access --> AccessCheck[Console: CloudTrail<br/>API 호출 기록 확인]
    AccessCheck --> AccessAnalysis{{접근 패턴?}}
    AccessAnalysis -->|비정상 IP| BlockIP[Console: Security Group<br/>IP 차단]
    AccessAnalysis -->|비정상 시간| Alert[CloudWatch 알람<br/>설정 강화]
    AccessAnalysis -->|무단 자격증명| RevokeKey[Console: IAM<br/>액세스 키 비활성화]
    
    Permission --> PermCheck[Console: IAM<br/>정책 및 역할 검토]
    PermCheck --> PermAnalysis{{권한 문제?}}
    PermAnalysis -->|과도한 권한| Restrict[최소 권한 원칙<br/>적용]
    PermAnalysis -->|부족한 권한| Grant[필요 권한<br/>추가]
    PermAnalysis -->|잘못된 정책| Fix[정책 수정<br/>및 테스트]
    
    DataLeak --> DataCheck[Console: Macie/GuardDuty<br/>데이터 보호 상태 확인]
    DataCheck --> DataAnalysis{{데이터 위험?}}
    DataAnalysis -->|암호화 미적용| Encrypt[Console: KMS<br/>암호화 활성화]
    DataAnalysis -->|공개 접근| Private[Console: S3/RDS<br/>퍼블릭 액세스 차단]
    DataAnalysis -->|로깅 부족| Logging[Console: CloudTrail<br/>로깅 활성화]
    
    Compliance --> CompCheck[Console: Config<br/>규정 준수 상태 확인]
    CompCheck --> CompAnalysis{{위반 항목?}}
    CompAnalysis -->|설정 위반| ConfigFix[Config Rules<br/>자동 수정 활성화]
    CompAnalysis -->|감사 로그 부족| AuditLog[감사 로깅<br/>강화]
    CompAnalysis -->|백업 부족| Backup[자동 백업<br/>설정]
    
    BlockIP --> Verify[보안 검증]
    Alert --> Verify
    RevokeKey --> Verify
    Restrict --> Verify
    Grant --> Verify
    Fix --> Verify
    Encrypt --> Verify
    Private --> Verify
    Logging --> Verify
    ConfigFix --> Verify
    AuditLog --> Verify
    Backup --> Verify
    
    Verify --> Success{{해결됨?}}
    Success -->|Yes| Document[보안 사고<br/>문서화]
    Success -->|No| Escalate[보안팀<br/>에스컬레이션]
    
    Document --> Prevent[예방 조치<br/>구현]
    Escalate --> Prevent
    Prevent --> End[완료]
"""
        
        return flowchart
    
    def generate_cost_troubleshooting(self, day_number: int) -> str:
        """
        비용 급증 트러블슈팅 플로우차트 생성
        
        Args:
            day_number: 일차 (1-28)
            
        Returns:
            Mermaid flowchart 코드
        """
        topic = get_topic_by_day(day_number)
        primary_services = topic["primary_services"]
        service_name = primary_services[0] if primary_services else "AWS Service"
        
        flowchart = f"""flowchart TD
    Start[비용 급증 감지:<br/>{service_name}] --> Alert[Console: Billing<br/>비용 알람 확인]
    
    Alert --> Analyze[Console: Cost Explorer<br/>비용 분석]
    Analyze --> Breakdown{{비용 항목?}}
    
    Breakdown -->|컴퓨팅 비용| Compute[컴퓨팅 리소스<br/>분석]
    Breakdown -->|스토리지 비용| Storage[스토리지<br/>분석]
    Breakdown -->|데이터 전송| Transfer[데이터 전송<br/>분석]
    Breakdown -->|기타 서비스| Other[기타 서비스<br/>분석]
    
    Compute --> ComputeCheck{{원인?}}
    ComputeCheck -->|과다 프로비저닝| Rightsize[Console: {service_name}<br/>리소스 사이징 최적화]
    ComputeCheck -->|미사용 리소스| Cleanup[미사용 리소스<br/>정리]
    ComputeCheck -->|스팟 미활용| Spot[Console: EC2<br/>스팟 인스턴스 활용]
    
    Storage --> StorageCheck{{원인?}}
    StorageCheck -->|불필요한 데이터| Delete[오래된 데이터<br/>삭제]
    StorageCheck -->|비효율적 클래스| Lifecycle[Console: S3<br/>Lifecycle 정책 설정]
    StorageCheck -->|과다 스냅샷| SnapClean[Console: EC2/RDS<br/>스냅샷 정리]
    
    Transfer --> TransferCheck{{원인?}}
    TransferCheck -->|리전 간 전송| Regional[리전 간 전송<br/>최소화]
    TransferCheck -->|인터넷 전송| CDN[Console: CloudFront<br/>CDN 활용]
    TransferCheck -->|VPC 엔드포인트 미사용| Endpoint[Console: VPC<br/>VPC 엔드포인트 설정]
    
    Other --> OtherCheck{{서비스?}}
    OtherCheck -->|로그 과다| LogRetention[Console: CloudWatch<br/>로그 보관 기간 조정]
    OtherCheck -->|API 호출 과다| APIOptimize[API 호출<br/>최적화]
    OtherCheck -->|백업 과다| BackupPolicy[백업 정책<br/>최적화]
    
    Rightsize --> Implement[최적화 구현]
    Cleanup --> Implement
    Spot --> Implement
    Delete --> Implement
    Lifecycle --> Implement
    SnapClean --> Implement
    Regional --> Implement
    CDN --> Implement
    Endpoint --> Implement
    LogRetention --> Implement
    APIOptimize --> Implement
    BackupPolicy --> Implement
    
    Implement --> Monitor[Console: Billing<br/>비용 모니터링 설정]
    Monitor --> Budget[Console: Budgets<br/>예산 알람 설정]
    Budget --> Verify{{비용 감소?}}
    
    Verify -->|Yes| Report[비용 최적화<br/>보고서 작성]
    Verify -->|No| Review[추가 최적화<br/>항목 검토]
    
    Review --> Analyze
    Report --> End[완료]
"""
        
        return flowchart
    
    def save_flowchart(
        self, 
        day_number: int, 
        flowchart_type: str, 
        content: str
    ) -> Path:
        """
        플로우차트를 파일로 저장
        
        Args:
            day_number: 일차 (1-28)
            flowchart_type: 플로우차트 유형 (diagnostic, performance, security, cost)
            content: Mermaid 플로우차트 코드
            
        Returns:
            저장된 파일 경로
        """
        output_dir = self._get_output_directory(day_number)
        self._ensure_directory_exists(output_dir)
        
        filename = f"day{day_number}-troubleshooting-{flowchart_type}.mmd"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def generate_flowcharts_for_day(self, day_number: int) -> Dict[str, Path]:
        """
        특정 일차에 대한 모든 트러블슈팅 플로우차트 생성
        
        Args:
            day_number: 일차 (1-28)
            
        Returns:
            플로우차트 유형별 파일 경로 딕셔너리
        """
        flowcharts = {}
        
        # 진단 플로우차트
        diagnostic = self.generate_diagnostic_flowchart(day_number)
        flowcharts['diagnostic'] = self.save_flowchart(
            day_number, 'diagnostic', diagnostic
        )
        
        # 성능 트러블슈팅
        performance = self.generate_performance_troubleshooting(day_number)
        flowcharts['performance'] = self.save_flowchart(
            day_number, 'performance', performance
        )
        
        # 보안 트러블슈팅
        security = self.generate_security_troubleshooting(day_number)
        flowcharts['security'] = self.save_flowchart(
            day_number, 'security', security
        )
        
        # 비용 트러블슈팅
        cost = self.generate_cost_troubleshooting(day_number)
        flowcharts['cost'] = self.save_flowchart(
            day_number, 'cost', cost
        )
        
        return flowcharts
    
    def generate_all_flowcharts(
        self, 
        start_day: int = 1, 
        end_day: int = 28
    ) -> Dict[int, Dict[str, Path]]:
        """
        지정된 범위의 모든 일차에 대한 플로우차트 생성
        
        Args:
            start_day: 시작 일차 (기본값: 1)
            end_day: 종료 일차 (기본값: 28)
            
        Returns:
            일차별 플로우차트 파일 경로 딕셔너리
        """
        all_flowcharts = {}
        
        for day in range(start_day, end_day + 1):
            print(f"Generating troubleshooting flowcharts for Day {day}...")
            flowcharts = self.generate_flowcharts_for_day(day)
            all_flowcharts[day] = flowcharts
            print(f"  ✓ Generated {len(flowcharts)} flowcharts")
        
        return all_flowcharts


def main():
    """CLI 인터페이스"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='트러블슈팅 플로우차트 생성기'
    )
    parser.add_argument(
        '--day',
        type=int,
        help='특정 일차의 플로우차트 생성 (1-28)'
    )
    parser.add_argument(
        '--start-day',
        type=int,
        default=1,
        help='시작 일차 (기본값: 1)'
    )
    parser.add_argument(
        '--end-day',
        type=int,
        default=28,
        help='종료 일차 (기본값: 28)'
    )
    parser.add_argument(
        '--type',
        choices=['diagnostic', 'performance', 'security', 'cost', 'all'],
        default='all',
        help='생성할 플로우차트 유형 (기본값: all)'
    )
    
    args = parser.parse_args()
    
    generator = TroubleshootingFlowchartGenerator()
    
    if args.day:
        # 특정 일차 생성
        print(f"\n=== Day {args.day} 트러블슈팅 플로우차트 생성 ===\n")
        
        if args.type == 'all':
            flowcharts = generator.generate_flowcharts_for_day(args.day)
            print(f"\n생성 완료: {len(flowcharts)}개 플로우차트")
            for ftype, fpath in flowcharts.items():
                print(f"  - {ftype}: {fpath}")
        else:
            # 특정 유형만 생성
            if args.type == 'diagnostic':
                content = generator.generate_diagnostic_flowchart(args.day)
            elif args.type == 'performance':
                content = generator.generate_performance_troubleshooting(args.day)
            elif args.type == 'security':
                content = generator.generate_security_troubleshooting(args.day)
            elif args.type == 'cost':
                content = generator.generate_cost_troubleshooting(args.day)
            
            filepath = generator.save_flowchart(args.day, args.type, content)
            print(f"\n생성 완료: {filepath}")
    else:
        # 범위 생성
        print(f"\n=== Day {args.start_day}-{args.end_day} 트러블슈팅 플로우차트 생성 ===\n")
        all_flowcharts = generator.generate_all_flowcharts(
            args.start_day, 
            args.end_day
        )
        
        total_count = sum(len(flowcharts) for flowcharts in all_flowcharts.values())
        print(f"\n전체 생성 완료: {len(all_flowcharts)}일차, {total_count}개 플로우차트")


if __name__ == '__main__':
    main()
