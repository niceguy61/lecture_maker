"""
Troubleshooting Scenario Generator for AWS SAA Study Materials
각 일별 troubleshooting.md 파일 생성
"""

from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from src.daily_topics import DAILY_TOPICS
from src.config import (
    TEMPLATES_ROOT,
    STUDY_MATERIALS_ROOT,
    DEFAULT_AWS_REGION,
    AWS_DOCS_BASE_URL
)


class TroubleshootingGenerator:
    """트러블슈팅 시나리오 생성기"""
    
    def __init__(self, template_path: Optional[Path] = None, output_base_path: Optional[Path] = None):
        """
        Args:
            template_path: 템플릿 파일 경로 (기본값: templates/troubleshooting-template.md)
            output_base_path: 출력 기본 경로 (기본값: aws-saa-study-materials)
        """
        self.template_path = template_path or TEMPLATES_ROOT / "troubleshooting-template.md"
        self.output_base_path = output_base_path or STUDY_MATERIALS_ROOT
        self.template_content = self.load_template()
    
    def load_template(self) -> str:
        """템플릿 파일 로드"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_daily_config(self, day_number: int) -> Dict:
        """일별 설정 가져오기"""
        if day_number not in DAILY_TOPICS:
            raise ValueError(f"Day {day_number} not found in DAILY_TOPICS")
        
        return DAILY_TOPICS[day_number]
    
    def generate_common_problems(self, day_number: int, config: Dict) -> Dict[str, str]:
        """일반적인 문제 상황 생성 (성능, 보안, 비용)"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # 성능 문제
        performance_problem = self._generate_performance_problem(primary_service, day_number)
        
        # 보안 문제
        security_problem = self._generate_security_problem(primary_service, day_number)
        
        # 비용 문제
        cost_problem = self._generate_cost_problem(primary_service, day_number)
        
        return {
            "performance_problem": performance_problem,
            "security_problem": security_problem,
            "cost_problem": cost_problem
        }
    
    def _generate_performance_problem(self, service: str, day_number: int) -> str:
        """성능 문제 시나리오 생성"""
        problems = {
            "EC2": """**증상**:
- 웹 애플리케이션 응답 시간이 평소 200ms에서 5초 이상으로 증가
- CloudWatch 메트릭에서 CPU 사용률이 지속적으로 90% 이상 유지
- 사용자로부터 "페이지 로딩이 너무 느리다"는 불만 접수

**영향 범위**:
- 전체 사용자의 약 80%가 성능 저하 경험
- 피크 시간대(오후 2-4시)에 특히 심각
- 일부 사용자는 타임아웃 오류 발생

**발생 시점**:
- 최근 마케팅 캠페인 이후 트래픽 3배 증가
- 기존 t3.medium 인스턴스로는 부하 처리 불가""",
            
            "S3": """**증상**:
- S3 버킷에서 객체 다운로드 시 속도가 매우 느림 (평소 10MB/s → 1MB/s)
- 특정 리전의 사용자들이 더 심한 지연 경험
- CloudWatch 메트릭에서 GetObject 요청 지연 시간 증가

**영향 범위**:
- 글로벌 사용자 중 아시아 지역 사용자가 특히 영향 받음
- 대용량 파일(>100MB) 다운로드 시 더 심각
- 피크 시간대에 문제 악화

**발생 시점**:
- 버킷이 us-east-1에 위치하지만 주요 사용자는 아시아 태평양 지역
- CDN 없이 직접 S3에서 다운로드""",
            
            "RDS": """**증상**:
- 데이터베이스 쿼리 응답 시간이 평소 50ms에서 3초 이상으로 증가
- CloudWatch에서 DatabaseConnections 메트릭이 최대치에 근접
- 애플리케이션 로그에 "Too many connections" 오류 발생

**영향 범위**:
- 모든 데이터베이스 의존 기능 영향 받음
- 사용자 로그인, 데이터 조회, 트랜잭션 처리 지연
- 일부 요청은 타임아웃으로 실패

**발생 시점**:
- 동시 접속자 수가 평소 100명에서 500명으로 증가
- 연결 풀 설정이 부적절하게 구성됨""",
            
            "Lambda": """**증상**:
- Lambda 함수 실행 시간이 평소 500ms에서 5초 이상으로 증가
- CloudWatch Logs에서 "Task timed out" 오류 빈번히 발생
- 콜드 스타트 시 10초 이상 소요

**영향 범위**:
- API Gateway를 통한 모든 요청 영향
- 사용자는 간헐적인 타임아웃 경험
- 피크 시간대에 문제 더 심각

**발생 시점**:
- 함수 메모리가 128MB로 설정되어 있음
- 외부 API 호출 및 데이터베이스 쿼리 포함
- 동시 실행 수가 급증"""
        }
        
        return problems.get(service, f"""**증상**:
- {service} 서비스 응답 시간 증가
- CloudWatch 메트릭에서 리소스 사용률 상승
- 사용자 경험 저하 및 불만 증가

**영향 범위**:
- 주요 기능 성능 저하
- 피크 시간대 문제 악화

**발생 시점**:
- 트래픽 증가 또는 리소스 부족""")
    
    def _generate_security_problem(self, service: str, day_number: int) -> str:
        """보안 문제 시나리오 생성"""
        problems = {
            "EC2": """**증상**:
- AWS GuardDuty에서 "UnauthorizedAccess:EC2/SSHBruteForce" 알람 발생
- CloudTrail 로그에서 알 수 없는 IP 주소로부터의 SSH 접속 시도 기록
- 인스턴스의 CPU 사용률이 비정상적으로 높음 (암호화폐 채굴 의심)

**영향 범위**:
- 특정 EC2 인스턴스가 침해당한 것으로 의심
- 동일 VPC 내 다른 리소스로 확산 가능성
- 데이터 유출 또는 서비스 중단 위험

**발생 원인**:
- Security Group에서 SSH 포트(22)가 0.0.0.0/0으로 개방
- 약한 비밀번호 사용 또는 키 페어 관리 부실
- 최신 보안 패치 미적용""",
            
            "S3": """**증상**:
- AWS Trusted Advisor에서 "S3 Bucket Permissions" 경고 발생
- 버킷 정책이 퍼블릭 액세스 허용으로 설정됨
- CloudTrail에서 알 수 없는 AWS 계정의 GetObject 요청 기록

**영향 범위**:
- 민감한 데이터가 포함된 S3 버킷이 공개됨
- 잠재적 데이터 유출 및 규정 위반
- 무단 액세스로 인한 데이터 전송 비용 발생

**발생 원인**:
- 버킷 생성 시 "Block all public access" 옵션 비활성화
- 버킷 정책에서 Principal: "*" 사용
- 정기적인 보안 검토 미실시""",
            
            "RDS": """**증상**:
- RDS 인스턴스가 퍼블릭 서브넷에 배치되어 인터넷에서 접근 가능
- Security Group에서 MySQL 포트(3306)가 0.0.0.0/0으로 개방
- CloudWatch Logs에서 알 수 없는 IP로부터의 로그인 시도 기록

**영향 범위**:
- 데이터베이스가 무단 액세스에 노출
- 민감한 고객 데이터 유출 위험
- SQL 인젝션 공격 가능성

**발생 원인**:
- RDS 인스턴스를 퍼블릭 서브넷에 배치
- Security Group 규칙이 과도하게 개방
- 데이터베이스 암호화 미적용""",
            
            "IAM": """**증상**:
- IAM Access Analyzer에서 "External access to resources" 경고
- 특정 IAM 사용자가 AdministratorAccess 정책 보유
- CloudTrail에서 비정상적인 API 호출 패턴 감지 (예: 대량 리소스 삭제)

**영향 범위**:
- 과도한 권한으로 인한 보안 위험
- 실수 또는 악의적 행위로 인한 리소스 손상 가능
- 규정 준수 위반 (최소 권한 원칙)

**발생 원인**:
- IAM 사용자에게 과도한 권한 부여
- 정기적인 권한 검토 미실시
- MFA(다중 인증) 미적용"""
        }
        
        return problems.get(service, f"""**증상**:
- {service} 리소스에 대한 무단 액세스 시도
- 보안 그룹 또는 IAM 정책 설정 오류
- CloudTrail 또는 GuardDuty 알람 발생

**영향 범위**:
- 데이터 유출 또는 서비스 침해 위험
- 규정 준수 위반 가능성

**발생 원인**:
- 과도하게 개방된 보안 설정
- 최소 권한 원칙 미적용""")
    
    def _generate_cost_problem(self, service: str, day_number: int) -> str:
        """비용 문제 시나리오 생성"""
        problems = {
            "EC2": """**증상**:
- AWS Cost Explorer에서 EC2 비용이 전월 대비 300% 증가
- 예산 알람이 발생하여 월 예산 $500을 초과할 것으로 예상
- Billing Dashboard에서 특정 인스턴스 타입(m5.4xlarge)의 비용이 급증

**영향 범위**:
- 월 예산 초과로 인한 재정적 부담
- 불필요한 리소스 사용으로 인한 낭비
- 다른 프로젝트 예산 압박

**발생 원인**:
- 개발 환경 인스턴스를 24/7 실행 (업무 시간만 필요)
- 과도하게 큰 인스턴스 타입 선택 (실제 사용률 20%)
- 테스트 후 인스턴스 종료 미실시""",
            
            "S3": """**증상**:
- S3 스토리지 비용이 전월 대비 200% 증가
- Cost Explorer에서 S3 Standard 스토리지 클래스 비용이 대부분
- 버킷 크기가 10TB를 초과하지만 대부분 오래된 데이터

**영향 범위**:
- 월 스토리지 비용 $300 → $900으로 증가
- 불필요한 데이터 저장으로 인한 낭비
- 데이터 전송 비용도 함께 증가

**발생 원인**:
- 모든 데이터를 S3 Standard 클래스에 저장
- Lifecycle 정책 미설정
- 미완료 멀티파트 업로드 정리 안 됨
- 이전 버전 데이터 무한 보관""",
            
            "RDS": """**증상**:
- RDS 비용이 전월 대비 250% 증가
- Cost Explorer에서 db.r5.2xlarge 인스턴스 비용이 주요 원인
- CloudWatch 메트릭에서 평균 CPU 사용률 15%, 메모리 사용률 20%

**영향 범위**:
- 월 데이터베이스 비용 $400 → $1,000으로 증가
- 과도하게 프로비저닝된 리소스로 인한 낭비
- 예산 초과 및 비용 최적화 필요

**발생 원인**:
- 실제 워크로드에 비해 과도한 인스턴스 클래스 선택
- 개발/테스트 환경을 프로덕션과 동일한 사양으로 운영
- 예약 인스턴스 또는 Savings Plans 미활용
- 자동 백업 보관 기간이 35일로 설정 (필요 이상)""",
            
            "Lambda": """**증상**:
- Lambda 비용이 전월 대비 400% 증가
- Cost Explorer에서 Lambda 실행 시간 및 요청 수 급증
- CloudWatch Logs에서 무한 루프 또는 재귀 호출 의심

**영향 범위**:
- 월 Lambda 비용 $50 → $250으로 증가
- 비정상적인 함수 실행으로 인한 낭비
- 다른 서비스 비용도 연쇄적으로 증가 (API Gateway, DynamoDB)

**발생 원인**:
- 함수 코드에 무한 루프 또는 재귀 호출 버그
- 과도한 메모리 할당 (3GB 설정, 실제 사용 500MB)
- 불필요한 함수 호출 (예: 1초마다 실행되는 CloudWatch Events)
- 함수 타임아웃이 15분으로 설정 (실제 필요 시간 30초)"""
        }
        
        return problems.get(service, f"""**증상**:
- {service} 비용이 예상보다 크게 증가
- Cost Explorer에서 비정상적인 비용 패턴 감지
- 예산 알람 발생

**영향 범위**:
- 월 예산 초과
- 불필요한 리소스 사용

**발생 원인**:
- 리소스 과다 프로비저닝
- 비용 최적화 미실시""")

    
    def generate_diagnostic_steps(self, day_number: int, config: Dict) -> Dict[str, str]:
        """AWS Console 기반 진단 단계 생성"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # 성능 진단
        performance_diagnostic = self._generate_performance_diagnostic(primary_service)
        
        # 보안 진단
        security_diagnostic = self._generate_security_diagnostic(primary_service)
        
        # 비용 진단
        cost_diagnostic = self._generate_cost_diagnostic(primary_service)
        
        return {
            "performance_diagnostic": performance_diagnostic,
            "security_diagnostic": security_diagnostic,
            "cost_diagnostic": cost_diagnostic
        }
    
    def _generate_performance_diagnostic(self, service: str) -> str:
        """성능 진단 단계"""
        diagnostics = {
            "EC2": """1. **CloudWatch 메트릭 확인**
   - Console 경로: CloudWatch > Metrics > EC2
   - 확인 항목:
     - CPUUtilization: 평균, 최대값 확인
     - NetworkIn/NetworkOut: 네트워크 트래픽 패턴
     - DiskReadOps/DiskWriteOps: 디스크 I/O 부하
   - 기간: 최근 1시간, 1일, 1주일 비교

2. **인스턴스 상태 확인**
   - Console 경로: EC2 > Instances
   - Status Checks: System status, Instance status 확인
   - Instance Type: 현재 사양 vs 실제 필요 사양 비교

3. **애플리케이션 로그 분석**
   - Console 경로: CloudWatch > Log groups
   - 오류 메시지, 경고, 느린 쿼리 검색
   - 로그 패턴 분석으로 병목 지점 식별

4. **네트워크 성능 확인**
   - Security Group 규칙 검토
   - Network ACL 설정 확인
   - VPC Flow Logs로 트래픽 패턴 분석""",
            
            "S3": """1. **CloudWatch 메트릭 확인**
   - Console 경로: CloudWatch > Metrics > S3
   - 확인 항목:
     - GetObject 요청 수 및 지연 시간
     - BytesDownloaded: 다운로드 트래픽
     - 4xxErrors, 5xxErrors: 오류율
   - 리전별, 버킷별 메트릭 비교

2. **버킷 설정 검토**
   - Console 경로: S3 > Buckets > [버킷 선택]
   - 버킷 리전: 사용자와의 지리적 거리 확인
   - Transfer Acceleration: 활성화 여부 확인
   - Versioning: 불필요한 버전 누적 확인

3. **객체 크기 및 구조 분석**
   - S3 Inventory 리포트 활용
   - 대용량 객체 식별
   - 객체 수 및 크기 분포 확인

4. **액세스 패턴 분석**
   - S3 Access Logs 활성화 및 분석
   - 자주 액세스되는 객체 식별
   - CloudFront 통합 필요성 검토""",
            
            "RDS": """1. **CloudWatch 메트릭 확인**
   - Console 경로: CloudWatch > Metrics > RDS
   - 확인 항목:
     - CPUUtilization: 데이터베이스 부하
     - DatabaseConnections: 연결 수 추이
     - ReadLatency/WriteLatency: 쿼리 성능
     - FreeableMemory: 메모리 사용률
   - 기간별 추이 분석

2. **Performance Insights 활용**
   - Console 경로: RDS > Databases > [DB 선택] > Performance Insights
   - Top SQL: 가장 많은 리소스를 사용하는 쿼리 식별
   - Wait Events: 대기 이벤트 분석
   - Database Load: 전체 부하 패턴 확인

3. **슬로우 쿼리 로그 분석**
   - Console 경로: RDS > Databases > [DB 선택] > Logs & events
   - 느린 쿼리 식별 및 최적화 대상 선정
   - 인덱스 누락 여부 확인

4. **연결 풀 설정 검토**
   - 애플리케이션 연결 풀 설정 확인
   - max_connections 파라미터 검토
   - 연결 누수(leak) 여부 확인""",
            
            "Lambda": """1. **CloudWatch 메트릭 확인**
   - Console 경로: CloudWatch > Metrics > Lambda
   - 확인 항목:
     - Duration: 실행 시간 추이
     - Errors: 오류 발생 빈도
     - Throttles: 동시 실행 제한 도달 여부
     - ConcurrentExecutions: 동시 실행 수
   - 기간별 패턴 분석

2. **CloudWatch Logs 분석**
   - Console 경로: CloudWatch > Log groups > /aws/lambda/[함수명]
   - REPORT 라인 분석:
     - Duration: 실제 실행 시간
     - Billed Duration: 청구 시간
     - Memory Used: 메모리 사용량
     - Max Memory Used: 최대 메모리
   - 오류 메시지 및 스택 트레이스 확인

3. **함수 설정 검토**
   - Console 경로: Lambda > Functions > [함수 선택] > Configuration
   - Memory: 할당된 메모리 vs 실제 사용량
   - Timeout: 타임아웃 설정 적절성
   - Environment variables: 설정 오류 확인

4. **콜드 스타트 분석**
   - Init Duration 메트릭 확인
   - 패키지 크기 및 의존성 검토
   - Provisioned Concurrency 필요성 평가"""
        }
        
        return diagnostics.get(service, f"""1. **CloudWatch 메트릭 확인**
   - Console 경로: CloudWatch > Metrics > {service}
   - 주요 성능 지표 확인
   - 기간별 추이 분석

2. **서비스 상태 확인**
   - Console에서 리소스 상태 점검
   - 설정 오류 여부 확인

3. **로그 분석**
   - CloudWatch Logs에서 오류 메시지 검색
   - 패턴 분석으로 원인 파악""")
    
    def _generate_security_diagnostic(self, service: str) -> str:
        """보안 진단 단계"""
        diagnostics = {
            "EC2": """1. **Security Group 검토**
   - Console 경로: EC2 > Security Groups
   - 인바운드 규칙 확인:
     - 0.0.0.0/0으로 개방된 포트 식별
     - 불필요한 포트 개방 여부
   - 아웃바운드 규칙 확인

2. **CloudTrail 로그 분석**
   - Console 경로: CloudTrail > Event history
   - 필터: Event name = "RunInstances", "AuthorizeSecurityGroupIngress"
   - 알 수 없는 IP 주소 또는 사용자 식별
   - 비정상적인 API 호출 패턴 확인

3. **GuardDuty 알람 확인**
   - Console 경로: GuardDuty > Findings
   - 심각도별 필터링 (High, Medium, Low)
   - 각 Finding의 상세 정보 및 권장 조치 확인

4. **인스턴스 보안 상태 점검**
   - Systems Manager > Compliance
   - 패치 상태 확인
   - 보안 기준 준수 여부 평가""",
            
            "S3": """1. **버킷 퍼블릭 액세스 설정 확인**
   - Console 경로: S3 > Buckets > [버킷 선택] > Permissions
   - Block public access 설정 확인
   - Bucket policy 검토: Principal "*" 사용 여부
   - ACL 설정 확인

2. **Trusted Advisor 권장 사항**
   - Console 경로: Trusted Advisor > Security
   - "S3 Bucket Permissions" 항목 확인
   - 권장 조치 사항 검토

3. **CloudTrail 로그 분석**
   - Console 경로: CloudTrail > Event history
   - 필터: Event source = "s3.amazonaws.com"
   - 알 수 없는 AWS 계정의 액세스 시도 확인
   - GetObject, PutObject 이벤트 분석

4. **S3 Access Logs 분석**
   - Console 경로: S3 > Buckets > [로그 버킷]
   - 액세스 패턴 분석
   - 비정상적인 IP 주소 또는 User-Agent 식별""",
            
            "RDS": """1. **네트워크 설정 검토**
   - Console 경로: RDS > Databases > [DB 선택] > Connectivity & security
   - Publicly accessible: "No"로 설정되어야 함
   - Subnet group: 프라이빗 서브넷에 위치 확인
   - VPC security groups: 규칙 검토

2. **Security Group 규칙 확인**
   - Console 경로: VPC > Security Groups
   - 인바운드 규칙:
     - 소스가 특정 Security Group 또는 IP 범위로 제한되어야 함
     - 0.0.0.0/0 개방 여부 확인

3. **암호화 설정 확인**
   - Console 경로: RDS > Databases > [DB 선택] > Configuration
   - Encryption: "Enabled" 확인
   - KMS key: 적절한 키 사용 여부

4. **CloudTrail 로그 분석**
   - Console 경로: CloudTrail > Event history
   - 필터: Event source = "rds.amazonaws.com"
   - ModifyDBInstance, AuthorizeDBSecurityGroupIngress 이벤트 확인
   - 비정상적인 설정 변경 식별""",
            
            "IAM": """1. **IAM Access Analyzer 활용**
   - Console 경로: IAM > Access Analyzer
   - External access 검토
   - 의도하지 않은 외부 액세스 식별

2. **사용자 및 역할 권한 검토**
   - Console 경로: IAM > Users / Roles
   - AdministratorAccess 정책 보유자 확인
   - 최소 권한 원칙 준수 여부 평가
   - 90일 이상 미사용 권한 식별

3. **MFA 설정 확인**
   - Console 경로: IAM > Users
   - MFA 활성화 여부 확인
   - 루트 계정 MFA 필수 확인

4. **CloudTrail 로그 분석**
   - Console 경로: CloudTrail > Event history
   - 비정상적인 API 호출 패턴 확인
   - 실패한 인증 시도 분석
   - 권한 변경 이벤트 검토"""
        }
        
        return diagnostics.get(service, f"""1. **보안 설정 검토**
   - Console에서 {service} 보안 설정 확인
   - 액세스 제어 규칙 검토

2. **CloudTrail 로그 분석**
   - 비정상적인 API 호출 확인
   - 알 수 없는 사용자 또는 IP 식별

3. **보안 알람 확인**
   - GuardDuty, Security Hub 알람 검토
   - 권장 조치 사항 확인""")
    
    def _generate_cost_diagnostic(self, service: str) -> str:
        """비용 진단 단계"""
        diagnostics = {
            "EC2": """1. **Cost Explorer 분석**
   - Console 경로: Billing > Cost Explorer
   - 필터: Service = "Amazon Elastic Compute Cloud"
   - 그룹화: Instance Type, Usage Type
   - 기간: 지난 3개월 추이 확인
   - 비용 급증 시점 및 원인 식별

2. **인스턴스 사용률 분석**
   - Console 경로: CloudWatch > Metrics > EC2
   - CPUUtilization 평균값 확인 (목표: 70-80%)
   - 저사용률 인스턴스 식별 (<20%)
   - 기간: 최근 2주간 패턴 분석

3. **Compute Optimizer 권장 사항**
   - Console 경로: Compute Optimizer > EC2 instances
   - Under-provisioned, Over-provisioned 인스턴스 확인
   - 권장 인스턴스 타입 및 예상 절감액 검토

4. **Trusted Advisor 확인**
   - Console 경로: Trusted Advisor > Cost Optimization
   - "Low Utilization Amazon EC2 Instances" 항목
   - "Idle Load Balancers" 항목
   - 권장 조치 사항 검토""",
            
            "S3": """1. **Cost Explorer 분석**
   - Console 경로: Billing > Cost Explorer
   - 필터: Service = "Amazon Simple Storage Service"
   - 그룹화: Storage Class, Usage Type
   - 비용 구성 요소 분석:
     - Storage: 스토리지 클래스별 비용
     - Requests: API 요청 비용
     - Data Transfer: 데이터 전송 비용

2. **S3 Storage Lens 활용**
   - Console 경로: S3 > Storage Lens
   - 버킷별 스토리지 사용량 확인
   - 스토리지 클래스 분포 분석
   - 비용 최적화 기회 식별

3. **버킷 분석**
   - Console 경로: S3 > Buckets > [버킷 선택] > Metrics
   - 버킷 크기 및 객체 수 확인
   - 스토리지 클래스 분포
   - Lifecycle 정책 설정 여부

4. **미완료 멀티파트 업로드 확인**
   - Console 경로: S3 > Buckets > [버킷 선택] > Management > Lifecycle rules
   - 미완료 업로드로 인한 숨겨진 비용 식별
   - 정리 정책 설정 필요성 평가""",
            
            "RDS": """1. **Cost Explorer 분석**
   - Console 경로: Billing > Cost Explorer
   - 필터: Service = "Amazon Relational Database Service"
   - 그룹화: Instance Type, Database Engine
   - 비용 구성 요소:
     - Instance: 인스턴스 비용
     - Storage: 스토리지 비용
     - Backup: 백업 스토리지 비용
     - Data Transfer: 데이터 전송 비용

2. **인스턴스 사용률 분석**
   - Console 경로: CloudWatch > Metrics > RDS
   - CPUUtilization, DatabaseConnections 평균값
   - 저사용률 인스턴스 식별 (<30%)
   - 기간: 최근 2주간 패턴

3. **Trusted Advisor 권장 사항**
   - Console 경로: Trusted Advisor > Cost Optimization
   - "Amazon RDS Idle DB Instances" 확인
   - "Amazon RDS Reserved Instance Optimization" 검토

4. **백업 및 스냅샷 검토**
   - Console 경로: RDS > Snapshots
   - 수동 스냅샷 수 및 크기 확인
   - 불필요한 스냅샷 식별
   - 자동 백업 보관 기간 검토 (기본 7일)""",
            
            "Lambda": """1. **Cost Explorer 분석**
   - Console 경로: Billing > Cost Explorer
   - 필터: Service = "AWS Lambda"
   - 그룹화: Function Name
   - 비용 구성 요소:
     - Requests: 요청 수 기반 비용
     - Duration: 실행 시간 기반 비용
   - 비용 급증 함수 식별

2. **CloudWatch 메트릭 분석**
   - Console 경로: CloudWatch > Metrics > Lambda
   - Invocations: 함수 호출 빈도
   - Duration: 평균 실행 시간
   - Errors: 오류로 인한 재시도 비용
   - 비정상적인 패턴 식별

3. **함수 설정 검토**
   - Console 경로: Lambda > Functions
   - 각 함수의 Memory 설정 vs 실제 사용량
   - Timeout 설정 적절성
   - 과도한 메모리 할당 식별

4. **CloudWatch Logs Insights 쿼리**
   ```
   fields @timestamp, @billedDuration, @memorySize, @maxMemoryUsed
   | stats avg(@billedDuration), avg(@maxMemoryUsed), count() by bin(5m)
   ```
   - 실행 시간 및 메모리 사용 패턴 분석
   - 최적화 기회 식별"""
        }
        
        return diagnostics.get(service, f"""1. **Cost Explorer 분석**
   - Console 경로: Billing > Cost Explorer
   - 필터: Service = "{service}"
   - 비용 추이 및 급증 원인 분석

2. **리소스 사용률 확인**
   - CloudWatch 메트릭으로 실제 사용률 분석
   - 저사용률 리소스 식별

3. **Trusted Advisor 권장 사항**
   - Cost Optimization 카테고리 확인
   - 권장 조치 사항 검토""")

    
    def generate_solutions(self, day_number: int, config: Dict) -> Dict[str, str]:
        """해결 방법 생성 (즉각 조치, 근본 원인 해결, 예방 조치)"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # 성능 해결
        performance_solution = self._generate_performance_solution(primary_service)
        
        # 보안 해결
        security_solution = self._generate_security_solution(primary_service)
        
        # 비용 해결
        cost_solution = self._generate_cost_solution(primary_service)
        
        return {
            "performance_solution": performance_solution,
            "security_solution": security_solution,
            "cost_solution": cost_solution
        }
    
    def _generate_performance_solution(self, service: str) -> str:
        """성능 문제 해결 방법"""
        solutions = {
            "EC2": """**즉각 조치** (5-10분):
1. **인스턴스 타입 변경**
   - Console 경로: EC2 > Instances > [인스턴스 선택] > Actions > Instance settings > Change instance type
   - 현재: t3.medium → 권장: t3.large 또는 c5.large
   - 인스턴스 중지 → 타입 변경 → 시작
   - 예상 효과: CPU 부하 90% → 50%로 감소

2. **Auto Scaling 그룹 용량 증가** (이미 설정된 경우)
   - Console 경로: EC2 > Auto Scaling Groups
   - Desired capacity 증가 (예: 2 → 4)
   - 즉시 새 인스턴스 시작

**근본 원인 해결** (1-2시간):
1. **Auto Scaling 설정**
   - Console 경로: EC2 > Auto Scaling Groups > Create Auto Scaling group
   - Launch template 생성
   - 스케일링 정책 설정:
     - Target tracking: CPU 70% 유지
     - Min: 2, Max: 10, Desired: 2
   - 예상 효과: 트래픽 변동에 자동 대응

2. **Load Balancer 추가**
   - Console 경로: EC2 > Load Balancers > Create Load Balancer
   - Application Load Balancer 선택
   - 여러 AZ에 분산 배치
   - Health check 설정

**예방 조치**:
- CloudWatch 알람 설정: CPU > 80% 시 알림
- 정기적인 성능 테스트 및 용량 계획
- 애플리케이션 코드 최적화 (캐싱, 쿼리 최적화)""",
            
            "S3": """**즉각 조치** (10-15분):
1. **CloudFront 배포 생성**
   - Console 경로: CloudFront > Create Distribution
   - Origin: S3 버킷 선택
   - Cache behavior: 기본 설정 사용
   - 배포 완료 대기 (10-15분)
   - 예상 효과: 다운로드 속도 5-10배 향상

2. **Transfer Acceleration 활성화**
   - Console 경로: S3 > Buckets > [버킷 선택] > Properties > Transfer acceleration
   - Enable 선택
   - 새 엔드포인트 사용: bucket-name.s3-accelerate.amazonaws.com
   - 예상 효과: 장거리 전송 속도 50-500% 향상

**근본 원인 해결** (30분-1시간):
1. **멀티 리전 복제 설정**
   - Console 경로: S3 > Buckets > [버킷 선택] > Management > Replication rules
   - 대상 리전: 주요 사용자 위치 (예: ap-northeast-2)
   - IAM 역할 생성 및 연결
   - 예상 효과: 리전별 최적화된 액세스

2. **객체 크기 최적화**
   - 대용량 파일 압축 (gzip, brotli)
   - 이미지 최적화 (WebP 포맷, 적절한 해상도)
   - 예상 효과: 전송 시간 30-50% 단축

**예방 조치**:
- CloudWatch 알람: GetObject 지연 시간 > 500ms
- 정기적인 액세스 패턴 분석
- CDN 캐시 히트율 모니터링 (목표: >80%)""",
            
            "RDS": """**즉각 조치** (5-10분):
1. **읽기 복제본 생성**
   - Console 경로: RDS > Databases > [DB 선택] > Actions > Create read replica
   - 리전: 동일 리전 선택
   - 인스턴스 클래스: 마스터와 동일
   - 생성 완료 대기 (5-10분)
   - 애플리케이션에서 읽기 쿼리를 복제본으로 분산

2. **연결 수 제한 증가** (임시 조치)
   - Console 경로: RDS > Parameter groups > [파라미터 그룹 선택]
   - max_connections 값 증가 (예: 100 → 200)
   - DB 인스턴스 재부팅 필요

**근본 원인 해결** (1-2시간):
1. **인스턴스 클래스 업그레이드**
   - Console 경로: RDS > Databases > [DB 선택] > Modify
   - DB instance class: db.t3.medium → db.r5.large
   - Apply immediately 선택
   - 예상 효과: 연결 수 및 성능 향상

2. **연결 풀 최적화**
   - 애플리케이션 연결 풀 설정 조정
   - 최대 연결 수: DB max_connections의 70%
   - 연결 타임아웃 및 재사용 설정
   - 예상 효과: 연결 효율성 향상

**예방 조치**:
- CloudWatch 알람: DatabaseConnections > 80%
- Performance Insights 활성화 및 정기 검토
- 슬로우 쿼리 로그 분석 및 인덱스 최적화""",
            
            "Lambda": """**즉각 조치** (2-5분):
1. **메모리 증가**
   - Console 경로: Lambda > Functions > [함수 선택] > Configuration > General configuration > Edit
   - Memory: 128MB → 512MB 또는 1024MB
   - Save 클릭
   - 예상 효과: 실행 시간 50-70% 단축 (CPU도 비례 증가)

2. **타임아웃 증가**
   - 동일 경로에서 Timeout 설정
   - 현재: 3초 → 권장: 30초 (실제 필요 시간 + 버퍼)
   - 예상 효과: 타임아웃 오류 제거

**근본 원인 해결** (30분-1시간):
1. **코드 최적화**
   - 불필요한 라이브러리 제거
   - 외부 API 호출 최적화 (병렬 처리, 캐싱)
   - 데이터베이스 쿼리 최적화
   - 예상 효과: 실행 시간 30-50% 단축

2. **Provisioned Concurrency 설정** (콜드 스타트 문제)
   - Console 경로: Lambda > Functions > [함수 선택] > Configuration > Provisioned concurrency
   - 동시 실행 수 설정 (예: 5)
   - 예상 효과: 콜드 스타트 제거, 일관된 성능

**예방 조치**:
- CloudWatch 알람: Duration > 3000ms, Errors > 1%
- X-Ray 추적 활성화로 병목 지점 식별
- 정기적인 성능 테스트 및 부하 테스트"""}
        
        return solutions.get(service, f"""**즉각 조치**:
- 리소스 용량 증가
- 임시 설정 조정

**근본 원인 해결**:
- 아키텍처 최적화
- 자동 스케일링 설정

**예방 조치**:
- 모니터링 및 알람 설정
- 정기적인 성능 검토""")
    
    def _generate_security_solution(self, service: str) -> str:
        """보안 문제 해결 방법"""
        solutions = {
            "EC2": """**즉각 조치** (5-10분):
1. **Security Group 규칙 수정**
   - Console 경로: EC2 > Security Groups > [SG 선택] > Inbound rules > Edit
   - SSH (22) 규칙 수정:
     - 현재: 0.0.0.0/0
     - 변경: 회사 IP 범위 (예: 203.0.113.0/24) 또는 VPN IP
   - Save rules
   - 예상 효과: 무단 액세스 차단

2. **의심스러운 인스턴스 격리**
   - 새 Security Group 생성 (모든 트래픽 차단)
   - 인스턴스에 적용
   - 스냅샷 생성 (포렌식 분석용)

**근본 원인 해결** (30분-1시간):
1. **Systems Manager Session Manager 설정**
   - Console 경로: Systems Manager > Session Manager
   - IAM 역할 생성 및 인스턴스에 연결
   - SSH 포트 완전 차단 가능
   - 예상 효과: 안전한 원격 액세스

2. **침해된 인스턴스 교체**
   - 새 AMI로 인스턴스 재생성
   - 최신 보안 패치 적용
   - 강력한 키 페어 생성
   - 예상 효과: 완전한 보안 복구

**예방 조치**:
- GuardDuty 활성화 및 알람 설정
- Systems Manager Patch Manager로 자동 패치
- 정기적인 보안 감사 (월 1회)
- Security Group 변경 시 CloudTrail 알람""",
            
            "S3": """**즉각 조치** (2-5분):
1. **퍼블릭 액세스 차단**
   - Console 경로: S3 > Buckets > [버킷 선택] > Permissions > Block public access
   - "Block all public access" 체크
   - Save changes
   - 예상 효과: 즉시 퍼블릭 액세스 차단

2. **버킷 정책 수정**
   - Console 경로: S3 > Buckets > [버킷 선택] > Permissions > Bucket policy
   - Principal "*" 제거
   - 특정 IAM 역할 또는 계정만 허용
   - Save changes

**근본 원인 해결** (30분-1시간):
1. **IAM 역할 기반 액세스 설정**
   - Console 경로: IAM > Roles > Create role
   - EC2 또는 Lambda 서비스 선택
   - S3 액세스 정책 연결 (최소 권한)
   - 애플리케이션에서 IAM 역할 사용

2. **S3 Access Logs 활성화**
   - Console 경로: S3 > Buckets > [버킷 선택] > Properties > Server access logging
   - 로그 버킷 지정
   - 예상 효과: 모든 액세스 추적 가능

**예방 조치**:
- AWS Config 규칙: s3-bucket-public-read-prohibited
- CloudWatch Events로 버킷 정책 변경 알람
- 정기적인 버킷 권한 검토 (주 1회)
- Trusted Advisor 권장 사항 정기 확인""",
            
            "RDS": """**즉각 조치** (5-10분):
1. **퍼블릭 액세스 비활성화**
   - Console 경로: RDS > Databases > [DB 선택] > Modify
   - Connectivity > Public access: No 선택
   - Apply immediately
   - 예상 효과: 인터넷에서 직접 액세스 차단

2. **Security Group 규칙 수정**
   - Console 경로: VPC > Security Groups > [SG 선택]
   - Inbound rules 수정:
     - 현재: 0.0.0.0/0
     - 변경: 애플리케이션 Security Group만 허용
   - Save rules

**근본 원인 해결** (1-2시간):
1. **프라이빗 서브넷으로 이동**
   - 새 DB 서브넷 그룹 생성 (프라이빗 서브넷만)
   - 스냅샷 생성
   - 스냅샷에서 새 인스턴스 복원 (프라이빗 서브넷)
   - 애플리케이션 연결 문자열 업데이트
   - 예상 효과: 완전한 네트워크 격리

2. **암호화 활성화**
   - 기존 DB는 암호화 활성화 불가
   - 스냅샷 생성 → 암호화된 스냅샷 복사 → 복원
   - KMS 키 선택
   - 예상 효과: 저장 데이터 암호화

**예방 조치**:
- CloudTrail로 RDS 설정 변경 추적
- AWS Config 규칙: rds-instance-public-access-check
- 정기적인 보안 설정 검토
- IAM 데이터베이스 인증 사용 고려""",
            
            "IAM": """**즉각 조치** (5-10분):
1. **과도한 권한 제거**
   - Console 경로: IAM > Users > [사용자 선택] > Permissions
   - AdministratorAccess 정책 제거
   - 필요한 최소 권한만 부여
   - 예상 효과: 권한 남용 위험 감소

2. **의심스러운 액세스 키 비활성화**
   - Console 경로: IAM > Users > [사용자 선택] > Security credentials
   - Access keys > Make inactive
   - 예상 효과: 무단 API 호출 차단

**근본 원인 해결** (1-2시간):
1. **최소 권한 정책 생성**
   - Console 경로: IAM > Policies > Create policy
   - 필요한 서비스 및 작업만 허용
   - 리소스 ARN 명시 (와일드카드 최소화)
   - 사용자/역할에 연결

2. **MFA 강제 활성화**
   - Console 경로: IAM > Account settings > Password policy
   - "Require at least one MFA device" 활성화
   - 모든 사용자에게 MFA 설정 요구
   - 예상 효과: 계정 탈취 방지

**예방 조치**:
- IAM Access Analyzer 정기 검토 (주 1회)
- CloudTrail로 IAM 변경 추적 및 알람
- 90일마다 권한 검토 및 정리
- 루트 계정 사용 최소화 (MFA 필수)"""
        }
        
        return solutions.get(service, f"""**즉각 조치**:
- 보안 설정 강화
- 무단 액세스 차단

**근본 원인 해결**:
- 최소 권한 원칙 적용
- 암호화 및 로깅 활성화

**예방 조치**:
- 정기적인 보안 검토
- 자동화된 보안 모니터링""")
    
    def _generate_cost_solution(self, service: str) -> str:
        """비용 문제 해결 방법"""
        solutions = {
            "EC2": """**즉각 조치** (5-10분):
1. **불필요한 인스턴스 중지**
   - Console 경로: EC2 > Instances
   - 개발/테스트 환경 인스턴스 선택
   - Actions > Instance state > Stop
   - 예상 절감: 월 $200-400 (24/7 → 업무 시간만)

2. **인스턴스 타입 다운그레이드**
   - 저사용률 인스턴스 선택 (CPU <20%)
   - Actions > Instance settings > Change instance type
   - m5.4xlarge → m5.xlarge
   - 예상 절감: 월 $300-500

**근본 원인 해결** (1-2시간):
1. **예약 인스턴스 구매**
   - Console 경로: EC2 > Reserved Instances > Purchase Reserved Instances
   - 안정적으로 사용되는 인스턴스 식별
   - 1년 또는 3년 예약 선택
   - 예상 절감: 30-60% (연간 $2,000-4,000)

2. **Auto Scaling 스케줄 설정**
   - Console 경로: EC2 > Auto Scaling Groups > [ASG 선택] > Automatic scaling
   - Scheduled actions 생성:
     - 업무 시작 (오전 9시): Desired capacity = 4
     - 업무 종료 (오후 6시): Desired capacity = 1
   - 예상 절감: 월 $400-600

**예방 조치**:
- AWS Budgets 설정: 월 $500 예산, 80% 도달 시 알람
- 태그 기반 비용 추적 (Environment: dev/prod)
- 월간 비용 검토 회의
- Compute Optimizer 권장 사항 정기 확인""",
            
            "S3": """**즉각 조치** (10-15분):
1. **Lifecycle 정책 설정**
   - Console 경로: S3 > Buckets > [버킷 선택] > Management > Lifecycle rules
   - 규칙 생성:
     - 30일 후: Standard → Standard-IA
     - 90일 후: Standard-IA → Glacier
     - 365일 후: Glacier → Deep Archive
   - 예상 절감: 월 $200-400 (50-70% 스토리지 비용)

2. **미완료 멀티파트 업로드 정리**
   - 동일 경로에서 Lifecycle rule 추가
   - "Delete expired object delete markers or incomplete multipart uploads"
   - 7일 후 삭제 설정
   - 예상 절감: 월 $50-100

**근본 원인 해결** (30분-1시간):
1. **불필요한 버전 정리**
   - Console 경로: S3 > Buckets > [버킷 선택] > Management > Lifecycle rules
   - Noncurrent versions 정리 규칙:
     - 30일 후 이전 버전 삭제
   - 예상 절감: 월 $100-200

2. **Intelligent-Tiering 활성화**
   - 새 객체 업로드 시 스토리지 클래스 선택
   - S3 Intelligent-Tiering 선택
   - 자동으로 액세스 패턴에 따라 티어 이동
   - 예상 절감: 월 $150-300

**예방 조치**:
- S3 Storage Lens 대시보드 정기 검토
- CloudWatch 알람: 버킷 크기 > 5TB
- 월간 스토리지 사용 분석
- 데이터 보관 정책 수립 및 준수""",
            
            "RDS": """**즉각 조치** (10-15분):
1. **인스턴스 클래스 다운그레이드**
   - Console 경로: RDS > Databases > [DB 선택] > Modify
   - DB instance class: db.r5.2xlarge → db.r5.large
   - Apply immediately (또는 다음 유지 관리 기간)
   - 예상 절감: 월 $400-600

2. **백업 보관 기간 조정**
   - 동일 경로에서 Backup retention period 수정
   - 35일 → 7일
   - 예상 절감: 월 $50-100

**근본 원인 해결** (1-2시간):
1. **예약 인스턴스 구매**
   - Console 경로: RDS > Reserved instances > Purchase reserved DB instance
   - 프로덕션 DB 인스턴스 선택
   - 1년 또는 3년 예약
   - 예상 절감: 30-60% (연간 $3,000-6,000)

2. **개발 환경 스케줄링**
   - Lambda 함수 생성 (RDS 시작/중지)
   - CloudWatch Events로 스케줄 설정:
     - 평일 오전 9시: 시작
     - 평일 오후 6시: 중지
     - 주말: 중지 유지
   - 예상 절감: 월 $200-400

**예방 조치**:
- CloudWatch 알람: 월 RDS 비용 > $800
- 분기별 인스턴스 사이징 검토
- Performance Insights로 최적 사양 결정
- 불필요한 스냅샷 정기 정리""",
            
            "Lambda": """**즉각 조치** (5-10분):
1. **메모리 최적화**
   - Console 경로: Lambda > Functions > [함수 선택] > Configuration
   - Memory: 3GB → 512MB (실제 사용량 기반)
   - 예상 절감: 월 $100-200

2. **타임아웃 조정**
   - 동일 경로에서 Timeout 수정
   - 15분 → 30초 (실제 필요 시간)
   - 예상 절감: 월 $50-100 (오류 시 비용 감소)

**근본 원인 해결** (1-2시간):
1. **코드 버그 수정**
   - 무한 루프 또는 재귀 호출 제거
   - 불필요한 외부 API 호출 최소화
   - 예상 절감: 월 $150-300

2. **호출 빈도 최적화**
   - Console 경로: CloudWatch > Events > Rules
   - 불필요한 스케줄 제거 또는 간격 조정
   - 1초마다 → 5분마다
   - 예상 절감: 월 $100-200

**예방 조치**:
- CloudWatch 알람: Lambda 비용 > $100/월
- X-Ray로 함수 실행 추적 및 최적화
- 정기적인 코드 리뷰 및 성능 테스트
- Lambda Power Tuning 도구 활용"""
        }
        
        return solutions.get(service, f"""**즉각 조치**:
- 불필요한 리소스 중지 또는 삭제
- 리소스 사이징 조정

**근본 원인 해결**:
- 예약 인스턴스 또는 Savings Plans 활용
- 자동화된 비용 최적화

**예방 조치**:
- 예산 및 알람 설정
- 정기적인 비용 검토""")

    
    def generate_hands_on_scenarios(self, day_number: int, config: Dict) -> str:
        """실습 시나리오 생성"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        scenarios = {
            "EC2": """### 시나리오 1: 고부하 상황 시뮬레이션 및 대응

**목표**: EC2 인스턴스에 부하를 발생시키고 CloudWatch로 모니터링하며 Auto Scaling으로 대응

**단계**:
1. **부하 생성 도구 설치**
   - EC2 인스턴스에 SSH 접속
   - `sudo yum install stress -y` (Amazon Linux)
   - `stress --cpu 4 --timeout 300s` (5분간 CPU 부하)

2. **CloudWatch 메트릭 확인**
   - Console: CloudWatch > Metrics > EC2
   - CPUUtilization 그래프 확인
   - 부하 발생 전후 비교

3. **Auto Scaling 테스트**
   - Console: EC2 > Auto Scaling Groups
   - Target tracking 정책 확인 (CPU 70%)
   - 새 인스턴스 자동 시작 확인

**예상 결과**:
- CPU 사용률 90% 이상 도달
- 2-3분 후 Auto Scaling 트리거
- 새 인스턴스 시작 및 부하 분산

### 시나리오 2: Security Group 잘못된 설정 수정

**목표**: 과도하게 개방된 Security Group 식별 및 수정

**단계**:
1. **현재 설정 확인**
   - Console: EC2 > Security Groups
   - 인바운드 규칙에서 0.0.0.0/0 찾기

2. **위험 평가**
   - 개방된 포트 및 프로토콜 확인
   - 실제 필요한 액세스 범위 결정

3. **규칙 수정**
   - 불필요한 규칙 삭제
   - 필요한 규칙은 특정 IP 범위로 제한
   - 변경 사항 저장

**예상 결과**:
- 보안 위험 감소
- Trusted Advisor 경고 해소""",
            
            "S3": """### 시나리오 1: 퍼블릭 버킷 보안 강화

**목표**: 실수로 퍼블릭 액세스가 허용된 S3 버킷 보안 강화

**단계**:
1. **퍼블릭 액세스 확인**
   - Console: S3 > Buckets
   - "Public" 라벨이 있는 버킷 식별
   - Permissions 탭에서 설정 확인

2. **Block Public Access 활성화**
   - "Block all public access" 체크
   - 확인 메시지 입력 및 저장

3. **버킷 정책 검토**
   - Bucket policy 확인
   - Principal "*" 제거
   - IAM 역할 기반 액세스로 변경

**예상 결과**:
- 퍼블릭 액세스 완전 차단
- IAM 역할을 통한 안전한 액세스

### 시나리오 2: Lifecycle 정책으로 비용 절감

**목표**: 오래된 데이터를 자동으로 저렴한 스토리지 클래스로 이동

**단계**:
1. **현재 스토리지 분석**
   - Console: S3 > Buckets > [버킷] > Metrics
   - 스토리지 클래스 분포 확인
   - 모든 데이터가 Standard인지 확인

2. **Lifecycle 규칙 생성**
   - Management > Lifecycle rules > Create rule
   - 규칙 이름: "cost-optimization"
   - 범위: 전체 버킷
   - Transitions:
     - 30일 후: Standard-IA
     - 90일 후: Glacier
   - 규칙 저장

3. **효과 확인**
   - 30일 후 스토리지 클래스 분포 재확인
   - Cost Explorer에서 비용 절감 확인

**예상 결과**:
- 스토리지 비용 50-70% 절감
- 자동화된 데이터 관리""",
            
            "RDS": """### 시나리오 1: 슬로우 쿼리 식별 및 최적화

**목표**: Performance Insights로 느린 쿼리 찾고 최적화

**단계**:
1. **Performance Insights 활성화**
   - Console: RDS > Databases > [DB] > Modify
   - Performance Insights: Enable
   - 보관 기간: 7일 (무료)
   - 변경 사항 적용

2. **Top SQL 분석**
   - Console: RDS > Databases > [DB] > Performance Insights
   - Top SQL 탭에서 가장 많은 시간을 소비하는 쿼리 확인
   - 쿼리 텍스트 및 실행 계획 검토

3. **쿼리 최적화**
   - 인덱스 추가 필요성 확인
   - 쿼리 재작성 (JOIN 최적화, WHERE 조건 개선)
   - 변경 후 성능 재측정

**예상 결과**:
- 느린 쿼리 실행 시간 50-80% 단축
- 전체 데이터베이스 부하 감소

### 시나리오 2: 읽기 복제본으로 부하 분산

**목표**: 읽기 전용 쿼리를 복제본으로 분산하여 마스터 부하 감소

**단계**:
1. **읽기 복제본 생성**
   - Console: RDS > Databases > [DB] > Actions > Create read replica
   - 인스턴스 클래스: 마스터와 동일
   - Multi-AZ: No (비용 절감)
   - 생성 완료 대기 (5-10분)

2. **애플리케이션 설정 변경**
   - 읽기 전용 엔드포인트 확인
   - 애플리케이션 코드에서 읽기 쿼리를 복제본으로 라우팅
   - 쓰기 쿼리는 마스터 유지

3. **효과 확인**
   - CloudWatch에서 마스터 CPU 사용률 감소 확인
   - 복제본 메트릭 모니터링

**예상 결과**:
- 마스터 CPU 사용률 30-50% 감소
- 전체 쿼리 처리 용량 증가""",
            
            "Lambda": """### 시나리오 1: 메모리 최적화로 비용 절감

**목표**: Lambda 함수의 적정 메모리 크기 찾기

**단계**:
1. **현재 사용량 확인**
   - Console: CloudWatch > Log groups > /aws/lambda/[함수명]
   - 최근 실행 로그에서 "Max Memory Used" 확인
   - 여러 실행 결과 평균 계산

2. **메모리 조정**
   - Console: Lambda > Functions > [함수] > Configuration
   - 현재: 1024MB, 실제 사용: 300MB
   - 권장: 512MB (실제 사용량 + 50% 버퍼)
   - 변경 저장

3. **성능 및 비용 비교**
   - 함수 실행 시간 비교 (메모리 감소 시 약간 증가 가능)
   - Cost Explorer에서 비용 변화 확인 (1주일 후)

**예상 결과**:
- 월 Lambda 비용 30-50% 절감
- 성능 영향 최소화

### 시나리오 2: 타임아웃 오류 해결

**목표**: 외부 API 호출로 인한 타임아웃 문제 해결

**단계**:
1. **오류 로그 분석**
   - Console: CloudWatch > Log groups > /aws/lambda/[함수명]
   - "Task timed out" 메시지 검색
   - 타임아웃 발생 시점 및 패턴 확인

2. **타임아웃 증가 (임시 조치)**
   - Console: Lambda > Functions > [함수] > Configuration
   - Timeout: 3초 → 30초
   - 변경 저장 및 재테스트

3. **근본 원인 해결**
   - 외부 API 호출에 타임아웃 설정 추가
   - 재시도 로직 구현
   - 비동기 처리 고려 (SQS 활용)

**예상 결과**:
- 타임아웃 오류 제거
- 안정적인 함수 실행"""
        }
        
        return scenarios.get(primary_service, f"""### 시나리오 1: {primary_service} 성능 최적화

**목표**: CloudWatch 메트릭을 활용한 성능 분석 및 개선

**단계**:
1. 현재 성능 메트릭 확인
2. 병목 지점 식별
3. 최적화 적용 및 효과 측정

### 시나리오 2: {primary_service} 보안 강화

**목표**: 보안 설정 검토 및 개선

**단계**:
1. 현재 보안 설정 확인
2. 취약점 식별
3. 보안 강화 조치 적용""")
    
    def generate_monitoring_setup(self, day_number: int, config: Dict) -> Dict[str, str]:
        """모니터링 및 알람 설정 생성"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # CloudWatch 대시보드
        dashboard = self._generate_dashboard_config(primary_service, day_number)
        
        # 알람 설정
        alarms = self._generate_alarm_config(primary_service, day_number)
        
        return {
            "cloudwatch_dashboard": dashboard,
            "cloudwatch_alarms": alarms
        }
    
    def _generate_dashboard_config(self, service: str, day_number: int) -> str:
        """CloudWatch 대시보드 설정"""
        dashboards = {
            "EC2": f"""**대시보드 생성**:
- Console 경로: CloudWatch > Dashboards > Create dashboard
- 대시보드 이름: `day{day_number}-ec2-monitoring`

**위젯 구성**:

1. **CPU 사용률**
   - 위젯 타입: Line
   - 메트릭: EC2 > Per-Instance Metrics > CPUUtilization
   - 통계: Average
   - 기간: 5분

2. **네트워크 트래픽**
   - 위젯 타입: Line
   - 메트릭: NetworkIn, NetworkOut
   - 통계: Sum
   - 기간: 5분

3. **디스크 I/O**
   - 위젯 타입: Line
   - 메트릭: DiskReadOps, DiskWriteOps
   - 통계: Average
   - 기간: 5분

4. **Status Checks**
   - 위젯 타입: Number
   - 메트릭: StatusCheckFailed
   - 통계: Maximum
   - 기간: 1분

**대시보드 저장 및 공유**:
- Save dashboard
- Actions > Share dashboard (팀 공유)""",
            
            "S3": f"""**대시보드 생성**:
- Console 경로: CloudWatch > Dashboards > Create dashboard
- 대시보드 이름: `day{day_number}-s3-monitoring`

**위젯 구성**:

1. **요청 수**
   - 위젯 타입: Line
   - 메트릭: S3 > Storage Metrics > AllRequests
   - 통계: Sum
   - 기간: 5분

2. **다운로드 바이트**
   - 위젯 타입: Line
   - 메트릭: BytesDownloaded
   - 통계: Sum
   - 기간: 5분

3. **오류율**
   - 위젯 타입: Line
   - 메트릭: 4xxErrors, 5xxErrors
   - 통계: Sum
   - 기간: 5분

4. **지연 시간**
   - 위젯 타입: Line
   - 메트릭: FirstByteLatency
   - 통계: Average
   - 기간: 5분

**대시보드 저장**:
- Save dashboard
- 정기적으로 검토 (일 1회)""",
            
            "RDS": f"""**대시보드 생성**:
- Console 경로: CloudWatch > Dashboards > Create dashboard
- 대시보드 이름: `day{day_number}-rds-monitoring`

**위젯 구성**:

1. **CPU 및 메모리**
   - 위젯 타입: Line
   - 메트릭: CPUUtilization, FreeableMemory
   - 통계: Average
   - 기간: 5분

2. **데이터베이스 연결**
   - 위젯 타입: Line
   - 메트릭: DatabaseConnections
   - 통계: Average
   - 기간: 5분

3. **읽기/쓰기 지연 시간**
   - 위젯 타입: Line
   - 메트릭: ReadLatency, WriteLatency
   - 통계: Average
   - 기간: 5분

4. **IOPS**
   - 위젯 타입: Line
   - 메트릭: ReadIOPS, WriteIOPS
   - 통계: Average
   - 기간: 5분

**Performance Insights 통합**:
- 대시보드에 Performance Insights 링크 추가
- Top SQL 및 Wait Events 정기 검토""",
            
            "Lambda": f"""**대시보드 생성**:
- Console 경로: CloudWatch > Dashboards > Create dashboard
- 대시보드 이름: `day{day_number}-lambda-monitoring`

**위젯 구성**:

1. **호출 수 및 오류**
   - 위젯 타입: Line
   - 메트릭: Invocations, Errors
   - 통계: Sum
   - 기간: 5분

2. **실행 시간**
   - 위젯 타입: Line
   - 메트릭: Duration
   - 통계: Average, Maximum
   - 기간: 5분

3. **동시 실행**
   - 위젯 타입: Line
   - 메트릭: ConcurrentExecutions
   - 통계: Maximum
   - 기간: 1분

4. **Throttles**
   - 위젯 타입: Number
   - 메트릭: Throttles
   - 통계: Sum
   - 기간: 5분

**X-Ray 통합**:
- 대시보드에 X-Ray 서비스 맵 링크 추가
- 트레이스 분석으로 병목 지점 식별"""
        }
        
        return dashboards.get(service, f"""**대시보드 생성**:
- Console 경로: CloudWatch > Dashboards > Create dashboard
- 대시보드 이름: `day{day_number}-{service.lower()}-monitoring`

**위젯 구성**:
1. 주요 성능 메트릭
2. 오류 및 경고
3. 리소스 사용률

**대시보드 저장 및 공유**""")
    
    def _generate_alarm_config(self, service: str, day_number: int) -> str:
        """CloudWatch 알람 설정"""
        alarms = {
            "EC2": f"""**알람 1: 높은 CPU 사용률**
- Console 경로: CloudWatch > Alarms > Create alarm
- 메트릭: EC2 > Per-Instance Metrics > CPUUtilization
- 조건: Greater than 80%
- 기간: 5분 동안 2 데이터 포인트
- 작업: SNS 토픽으로 이메일 알림
- 알람 이름: `day{day_number}-ec2-high-cpu`

**알람 2: Status Check 실패**
- 메트릭: StatusCheckFailed
- 조건: Greater than or equal to 1
- 기간: 1분 동안 2 데이터 포인트
- 작업: SNS 토픽 + EC2 인스턴스 재부팅 (선택사항)
- 알람 이름: `day{day_number}-ec2-status-check-failed`

**알람 3: 높은 네트워크 트래픽**
- 메트릭: NetworkIn
- 조건: Greater than 1GB (1073741824 bytes)
- 기간: 5분 동안 1 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-ec2-high-network`

**SNS 토픽 설정**:
- Console: SNS > Topics > Create topic
- 토픽 이름: `day{day_number}-ec2-alerts`
- Subscription: Email 프로토콜, 이메일 주소 입력
- 이메일 확인 필수""",
            
            "S3": f"""**알람 1: 높은 4xx 오류율**
- Console 경로: CloudWatch > Alarms > Create alarm
- 메트릭: S3 > Storage Metrics > 4xxErrors
- 조건: Greater than 100
- 기간: 5분 동안 2 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-s3-4xx-errors`

**알람 2: 높은 지연 시간**
- 메트릭: FirstByteLatency
- 조건: Greater than 500ms
- 기간: 5분 동안 3 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-s3-high-latency`

**알람 3: 비정상적인 요청 수**
- 메트릭: AllRequests
- 조건: Greater than 10000 (평소 대비 3배)
- 기간: 5분 동안 1 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-s3-unusual-requests`

**SNS 토픽 설정**:
- 토픽 이름: `day{day_number}-s3-alerts`
- Email subscription 추가""",
            
            "RDS": f"""**알람 1: 높은 CPU 사용률**
- Console 경로: CloudWatch > Alarms > Create alarm
- 메트릭: RDS > Per-Database Metrics > CPUUtilization
- 조건: Greater than 80%
- 기간: 5분 동안 3 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-rds-high-cpu`

**알람 2: 높은 데이터베이스 연결 수**
- 메트릭: DatabaseConnections
- 조건: Greater than 80 (max_connections의 80%)
- 기간: 5분 동안 2 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-rds-high-connections`

**알람 3: 낮은 여유 메모리**
- 메트릭: FreeableMemory
- 조건: Less than 1GB (1073741824 bytes)
- 기간: 5분 동안 2 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-rds-low-memory`

**알람 4: 높은 읽기 지연 시간**
- 메트릭: ReadLatency
- 조건: Greater than 100ms (0.1 seconds)
- 기간: 5분 동안 3 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-rds-high-read-latency`

**SNS 토픽 설정**:
- 토픽 이름: `day{day_number}-rds-alerts`
- Email 및 SMS subscription 추가 (중요 알람)""",
            
            "Lambda": f"""**알람 1: 높은 오류율**
- Console 경로: CloudWatch > Alarms > Create alarm
- 메트릭: Lambda > Function Metrics > Errors
- 조건: Greater than 10
- 기간: 5분 동안 2 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-lambda-errors`

**알람 2: Throttles 발생**
- 메트릭: Throttles
- 조건: Greater than or equal to 1
- 기간: 1분 동안 1 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-lambda-throttles`

**알람 3: 높은 실행 시간**
- 메트릭: Duration
- 조건: Greater than 5000ms
- 기간: 5분 동안 3 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-lambda-high-duration`

**알람 4: 높은 동시 실행 수**
- 메트릭: ConcurrentExecutions
- 조건: Greater than 800 (계정 제한의 80%)
- 기간: 1분 동안 1 데이터 포인트
- 작업: SNS 토픽으로 알림
- 알람 이름: `day{day_number}-lambda-high-concurrency`

**SNS 토픽 설정**:
- 토픽 이름: `day{day_number}-lambda-alerts`
- Email subscription 추가"""
        }
        
        return alarms.get(service, f"""**알람 설정**:
- Console 경로: CloudWatch > Alarms > Create alarm
- 주요 메트릭에 대한 알람 생성
- SNS 토픽으로 알림 전송

**권장 알람**:
1. 리소스 사용률 (CPU, 메모리)
2. 오류 및 실패
3. 성능 지표 (지연 시간, 처리량)""")

    
    def generate_aws_links(self, day_number: int, config: Dict) -> str:
        """AWS 문서 링크 생성"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        service_slug = primary_service.lower().replace(" ", "-")
        
        links = f"""- [{primary_service} 트러블슈팅 가이드]({AWS_DOCS_BASE_URL}/ko_kr/{service_slug}/latest/userguide/troubleshooting.html)
- [CloudWatch 사용 설명서]({AWS_DOCS_BASE_URL}/ko_kr/AmazonCloudWatch/latest/monitoring/)
- [AWS Support 센터](https://console.aws.amazon.com/support/home)
- [AWS 상태 대시보드](https://status.aws.amazon.com/)
- [AWS Trusted Advisor](https://console.aws.amazon.com/trustedadvisor/)
- [AWS Well-Architected Tool](https://console.aws.amazon.com/wellarchitected/)"""
        
        return links
    
    def populate_template(self, day_number: int) -> str:
        """템플릿에 데이터 채우기"""
        config = self.get_daily_config(day_number)
        
        # primary_services를 문자열로 변환
        primary_services_str = ", ".join(config["primary_services"])
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # 기본 정보
        replacements = {
            "{day_number}": str(day_number),
            "{day_title}": config["title"],
            "{service_name}": primary_service,
            "{primary_services}": primary_services_str,
            "{current_date}": datetime.now().strftime("%Y-%m-%d")
        }
        
        # 일반적인 문제 상황
        problems = self.generate_common_problems(day_number, config)
        replacements.update(problems)
        
        # 진단 단계
        diagnostics = self.generate_diagnostic_steps(day_number, config)
        replacements.update(diagnostics)
        
        # 해결 방법
        solutions = self.generate_solutions(day_number, config)
        replacements.update(solutions)
        
        # 실습 시나리오
        replacements["{hands_on_scenarios}"] = self.generate_hands_on_scenarios(day_number, config)
        
        # 모니터링 설정
        monitoring = self.generate_monitoring_setup(day_number, config)
        replacements.update(monitoring)
        
        # AWS 문서 링크
        replacements["{aws_troubleshooting_links}"] = self.generate_aws_links(day_number, config)
        
        # 템플릿 치환
        content = self.template_content
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        return content
    
    def generate_troubleshooting(self, day_number: int, output_path: Optional[Path] = None) -> str:
        """특정 일차의 트러블슈팅 시나리오 생성
        
        Args:
            day_number: 일차 번호 (1-28)
            output_path: 출력 파일 경로 (선택사항)
            
        Returns:
            생성된 콘텐츠
        """
        # 설정 가져오기
        config = self.get_daily_config(day_number)
        week_number = config["week"]
        
        # 출력 경로 설정
        if output_path is None:
            output_path = (
                self.output_base_path / 
                f"week{week_number}" / 
                f"day{day_number}" / 
                "advanced" / 
                "troubleshooting.md"
            )
        
        # 콘텐츠 생성
        content = self.populate_template(day_number)
        
        # 디렉토리 생성
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 파일 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Generated troubleshooting for Day {day_number}: {output_path}")
        
        return content
    
    def generate_all_troubleshooting(self, start_day: int = 1, end_day: int = 28) -> Dict[int, str]:
        """모든 일차의 트러블슈팅 시나리오 생성
        
        Args:
            start_day: 시작 일차 (기본값: 1)
            end_day: 종료 일차 (기본값: 28)
            
        Returns:
            일차별 생성된 파일 경로 딕셔너리
        """
        results = {}
        
        print(f"\n{'='*60}")
        print(f"Troubleshooting Generator - Generating Days {start_day} to {end_day}")
        print(f"{'='*60}\n")
        
        for day in range(start_day, end_day + 1):
            try:
                config = self.get_daily_config(day)
                week_number = config["week"]
                output_path = (
                    self.output_base_path / 
                    f"week{week_number}" / 
                    f"day{day}" / 
                    "advanced" / 
                    "troubleshooting.md"
                )
                
                self.generate_troubleshooting(day, output_path)
                results[day] = str(output_path)
                
            except Exception as e:
                print(f"✗ Error generating troubleshooting for Day {day}: {e}")
                results[day] = f"Error: {e}"
        
        print(f"\n{'='*60}")
        print(f"Generation Complete!")
        print(f"Successfully generated: {sum(1 for v in results.values() if not v.startswith('Error'))} / {end_day - start_day + 1}")
        print(f"{'='*60}\n")
        
        return results


# CLI 실행을 위한 메인 함수
def main():
    """CLI 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS SAA Troubleshooting Scenario Generator")
    parser.add_argument(
        "--day",
        type=int,
        help="Generate troubleshooting for specific day (1-28)"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start day for batch generation (default: 1)"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=28,
        help="End day for batch generation (default: 28)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Custom output path (optional)"
    )
    
    args = parser.parse_args()
    
    generator = TroubleshootingGenerator()
    
    if args.day:
        # 단일 일차 생성
        output_path = Path(args.output) if args.output else None
        generator.generate_troubleshooting(args.day, output_path)
    else:
        # 배치 생성
        generator.generate_all_troubleshooting(args.start, args.end)


if __name__ == "__main__":
    main()
