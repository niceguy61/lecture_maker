# Exercise Guide Generator
"""
AWS Console 기반 Exercise 가이드 생성기
각 일별(Day 1-28) hands-on-console/ 폴더에 1-2개의 exercise 파일을 생성
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from src.daily_topics import DAILY_TOPICS, get_topic_by_day
from src.config import (
    TEMPLATES_ROOT, STUDY_MATERIALS_ROOT, AWS_DOCS_BASE_URL
)


class ExerciseGuideGenerator:
    """AWS Console 기반 Exercise 가이드 생성기"""
    
    def __init__(self):
        self.template_path = TEMPLATES_ROOT / "exercise-template.md"
        self.output_base_path = STUDY_MATERIALS_ROOT
        
    def load_template(self) -> str:
        """템플릿 파일 로드"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_daily_config(self, day_number: int) -> Dict:
        """일별 주제 설정 가져오기"""
        return get_topic_by_day(day_number)
    
    def _determine_exercise_count(self, day_number: int) -> int:
        """일차별 exercise 개수 결정 (1-2개)"""
        config = self.get_daily_config(day_number)
        services_count = len(config["primary_services"])
        
        # 복잡도에 따라 exercise 개수 결정
        if day_number in [7, 14, 21, 28]:  # 주차 복습
            return 2
        elif services_count >= 3:  # 여러 서비스 통합
            return 2
        elif day_number in [5, 6, 10, 11, 20, 23, 24, 25, 26]:  # 복잡한 서비스
            return 2
        else:
            return 1

    def _generate_exercise_content(self, day_number: int, exercise_number: int) -> Dict:
        """Exercise 콘텐츠 생성"""
        config = self.get_daily_config(day_number)
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        if exercise_number == 1:
            # Exercise 1: 기본 리소스 생성 및 설정
            return self._generate_exercise_1(day_number, config, primary_service)
        else:
            # Exercise 2: 통합 및 고급 기능
            return self._generate_exercise_2(day_number, config, primary_service)
    
    def _generate_exercise_1(self, day_number: int, config: Dict, primary_service: str) -> Dict:
        """Exercise 1: 기본 리소스 생성 및 설정"""
        service_slug = primary_service.lower().replace(" ", "-")
        
        # 서비스별 카테고리 결정
        category = self._get_service_category(primary_service)
        
        # 단계별 가이드 생성
        steps = self._generate_basic_setup_steps(day_number, primary_service, category)
        
        # 검증 체크리스트
        verification = self._generate_verification_checklist(primary_service, "basic")
        
        # 문제 해결 가이드
        troubleshooting = self._generate_troubleshooting_guide(primary_service, "creation")
        
        # 정리 단계
        cleanup = self._generate_cleanup_steps(primary_service, day_number, "basic")
        
        return {
            "number": 1,
            "title": f"{primary_service} 생성 및 기본 설정",
            "objective": f"AWS Console을 통해 {primary_service}를 생성하고 기본 설정을 구성합니다.",
            "estimated_time": "15-20",
            "region": "ap-northeast-2",
            "previous_exercise_check": "",
            "architecture_diagram": self._generate_exercise_diagram(day_number, 1),
            "architecture_components": self._generate_architecture_components(primary_service, 1),
            "steps_content": steps,
            "verification_checklist": verification,
            "functional_tests": self._generate_functional_tests(primary_service, 1),
            "performance_checks": self._generate_performance_checks(primary_service),
            "log_verification": self._generate_log_verification(primary_service),
            "common_issues": troubleshooting,
            "debugging_tips": self._generate_debugging_tips(primary_service),
            "cleanup_steps": cleanup,
            "cleanup_verification": self._generate_cleanup_verification(primary_service),
            "learning_points": self._generate_learning_points(primary_service, 1),
            "next_steps": self._generate_next_steps(day_number, 1)
        }

    def _generate_exercise_2(self, day_number: int, config: Dict, primary_service: str) -> Dict:
        """Exercise 2: 통합 및 고급 기능"""
        related_service = config["primary_services"][1] if len(config["primary_services"]) > 1 else "CloudWatch"
        
        # 단계별 가이드 생성
        steps = self._generate_integration_steps(day_number, primary_service, related_service)
        
        # 검증 체크리스트
        verification = self._generate_verification_checklist(primary_service, "integration")
        
        # 문제 해결 가이드
        troubleshooting = self._generate_troubleshooting_guide(primary_service, "integration")
        
        # 정리 단계
        cleanup = self._generate_cleanup_steps(primary_service, day_number, "integration")
        
        return {
            "number": 2,
            "title": f"{primary_service}와 {related_service} 통합",
            "objective": f"{primary_service}를 {related_service}와 통합하여 고급 기능을 구성합니다.",
            "estimated_time": "15-20",
            "region": "ap-northeast-2",
            "previous_exercise_check": f"- [ ] Exercise 1 완료 (day{day_number}-{primary_service.lower().replace(' ', '-')} 생성됨)",
            "architecture_diagram": self._generate_exercise_diagram(day_number, 2),
            "architecture_components": self._generate_architecture_components(primary_service, 2, related_service),
            "steps_content": steps,
            "verification_checklist": verification,
            "functional_tests": self._generate_functional_tests(primary_service, 2),
            "performance_checks": self._generate_performance_checks(primary_service),
            "log_verification": self._generate_log_verification(primary_service),
            "common_issues": troubleshooting,
            "debugging_tips": self._generate_debugging_tips(primary_service),
            "cleanup_steps": cleanup,
            "cleanup_verification": self._generate_cleanup_verification(primary_service),
            "learning_points": self._generate_learning_points(primary_service, 2),
            "next_steps": self._generate_next_steps(day_number, 2)
        }
    
    def _get_service_category(self, service: str) -> str:
        """서비스 카테고리 결정"""
        if "EC2" in service or "Auto Scaling" in service:
            return "Compute"
        elif "S3" in service or "EBS" in service or "EFS" in service:
            return "Storage"
        elif "RDS" in service or "DynamoDB" in service or "ElastiCache" in service:
            return "Database"
        elif "VPC" in service or "Route 53" in service or "CloudFront" in service:
            return "Networking"
        elif "Lambda" in service or "API Gateway" in service:
            return "Application Integration"
        elif "CloudWatch" in service or "CloudTrail" in service:
            return "Management & Governance"
        elif "IAM" in service:
            return "Security, Identity, & Compliance"
        else:
            return "AWS Services"

    def _generate_basic_setup_steps(self, day_number: int, service: str, category: str) -> str:
        """기본 설정 단계 생성"""
        service_slug = service.lower().replace(" ", "-")
        resource_name = service.split()[0].lower()
        
        steps = f"""### Step 1: {service} 생성

**Console 경로**: `Services > {category} > {service}`

1. AWS Console 상단의 **Services** 메뉴 클릭
2. **{category}** 카테고리에서 **{service}** 선택
3. 화면 상단의 **"Create {resource_name}"** 또는 **"Launch {resource_name}"** 버튼 클릭

**참고**: 리전이 `ap-northeast-2` (서울)로 설정되어 있는지 확인하세요.

---

### Step 2: 기본 설정 구성

**리소스 이름 설정**:
- **Name**: `day{day_number}-{service_slug}`
- 명명 규칙: `day번호-서비스명`
- 예시: `day{day_number}-my-{resource_name}`

**리전 설정**:
- **Region**: `ap-northeast-2` (서울)
- 선택 이유: 낮은 지연시간, 한국 사용자 대상

**기본 구성**:
{self._generate_service_specific_config(service)}

---

### Step 3: 태그 추가

**Console 경로**: 설정 화면 하단의 **"Tags"** 섹션

다음 태그를 추가하세요:

| Key | Value | 설명 |
|-----|-------|------|
| Name | day{day_number}-{service_slug} | 리소스 식별 |
| Environment | learning | 환경 구분 |
| Project | aws-saa-study | 프로젝트 구분 |
| Day | {day_number} | 학습 일차 |

**태그 추가 방법**:
1. "Add tag" 버튼 클릭
2. Key와 Value 입력
3. 필요한 만큼 반복

---

### Step 4: 보안 설정

{self._generate_security_settings(service)}

---

### Step 5: 생성 확인

1. 모든 설정 검토
2. **"Create"** 또는 **"Launch"** 버튼 클릭
3. 생성 진행 상황 확인
4. 생성 완료까지 대기 (약 2-5분)

**상태 확인 방법**:
- Console 경로: `{service} > Resources` 또는 `{service} > Dashboard`
- 상태 컬럼에서 "Available", "Active", 또는 "Running" 확인
"""
        return steps

    def _generate_service_specific_config(self, service: str) -> str:
        """서비스별 특화 설정"""
        if "EC2" in service:
            return """- **Instance Type**: `t2.micro` (Free Tier)
- **AMI**: Amazon Linux 2023
- **Key Pair**: 새로 생성 또는 기존 키 선택
- **Network**: Default VPC
- **Subnet**: 기본 서브넷 (ap-northeast-2a)"""
        elif "S3" in service:
            return """- **Bucket Name**: `day{day_number}-{your-name}-bucket` (전역 고유 이름)
- **Region**: ap-northeast-2
- **Block Public Access**: 모든 옵션 활성화 (권장)
- **Versioning**: Disabled (기본값)
- **Encryption**: Disabled (기본값)"""
        elif "RDS" in service:
            return """- **Engine**: MySQL 또는 PostgreSQL
- **Version**: 최신 버전
- **Template**: Free tier
- **DB Instance Class**: db.t3.micro (Free Tier)
- **Storage**: 20 GB (Free Tier)
- **Multi-AZ**: No (비용 절감)"""
        elif "DynamoDB" in service:
            return """- **Table Name**: `day{day_number}-table`
- **Partition Key**: `id` (String)
- **Table Settings**: Default settings
- **Capacity Mode**: On-demand (권장)"""
        elif "VPC" in service:
            return """- **VPC Name**: `day{day_number}-vpc`
- **IPv4 CIDR**: `10.0.0.0/16`
- **IPv6 CIDR**: No IPv6 CIDR block
- **Tenancy**: Default"""
        elif "Lambda" in service:
            return """- **Function Name**: `day{day_number}-function`
- **Runtime**: Python 3.12 또는 Node.js 20.x
- **Architecture**: x86_64
- **Permissions**: Create new role with basic Lambda permissions"""
        else:
            return """- **Configuration**: Default settings
- **Options**: Standard configuration
- **Settings**: Recommended values"""
    
    def _generate_security_settings(self, service: str) -> str:
        """보안 설정 생성"""
        if "EC2" in service:
            return """**Security Group 설정**:
- **Security Group Name**: `day{day_number}-sg`
- **Inbound Rules**:
  - Type: SSH, Port: 22, Source: My IP
  - Type: HTTP, Port: 80, Source: 0.0.0.0/0 (선택사항)
- **Outbound Rules**: All traffic (기본값)"""
        elif "RDS" in service:
            return """**Security Group 설정**:
- **VPC Security Group**: Create new
- **Security Group Name**: `day{day_number}-db-sg`
- **Inbound Rules**:
  - Type: MySQL/PostgreSQL, Port: 3306/5432, Source: My IP"""
        elif "S3" in service:
            return """**Bucket Policy** (선택사항):
- 기본적으로 모든 퍼블릭 액세스 차단
- 필요시 특정 IAM 사용자/역할에만 액세스 허용"""
        else:
            return """**IAM 권한 설정**:
- 최소 권한 원칙 적용
- 필요한 권한만 부여
- 정기적인 권한 검토"""

    def _generate_integration_steps(self, day_number: int, primary_service: str, related_service: str) -> str:
        """통합 단계 생성"""
        return f"""### Step 1: {related_service} 설정

**Console 경로**: `Services > {self._get_service_category(related_service)} > {related_service}`

1. {related_service} 콘솔로 이동
2. 새 리소스 생성 또는 기존 리소스 선택
3. {primary_service}와의 통합 옵션 찾기

---

### Step 2: {primary_service}와 연결

**통합 설정**:
1. {primary_service} 콘솔로 이동
2. 생성한 리소스 선택 (`day{day_number}-{primary_service.lower().replace(' ', '-')}`)
3. "Integrations" 또는 "Connections" 탭 선택
4. "Add integration" 또는 "Connect" 버튼 클릭
5. {related_service} 선택 및 설정

**연결 옵션**:
- **Auto-enable**: Yes (자동 활성화)
- **Permissions**: Create new IAM role (권장)
- **Configuration**: Default settings

---

### Step 3: IAM 역할 구성

**Console 경로**: `IAM > Roles`

1. "Create role" 버튼 클릭
2. **Trusted entity**: AWS service
3. **Use case**: {primary_service}
4. **Permissions**: 
   - {primary_service}FullAccess
   - {related_service}FullAccess
5. **Role name**: `day{day_number}-integration-role`
6. "Create role" 클릭

---

### Step 4: 통합 테스트

**테스트 방법**:
1. {primary_service} 콘솔에서 테스트 기능 실행
2. {related_service}에서 데이터 확인
3. 로그 및 메트릭 확인

**예상 결과**:
- 연결 상태: Connected
- 데이터 전송: Success
- 에러: None

---

### Step 5: 모니터링 설정

**CloudWatch 설정**:
1. CloudWatch 콘솔로 이동
2. "Dashboards" > "Create dashboard"
3. 대시보드 이름: `day{day_number}-integration-monitoring`
4. 위젯 추가:
   - {primary_service} 메트릭
   - {related_service} 메트릭
   - 통합 상태 메트릭
"""

    def _generate_verification_checklist(self, service: str, type: str) -> str:
        """검증 체크리스트 생성"""
        if type == "basic":
            return f"""- [ ] {service} 리소스가 "Available" 또는 "Active" 상태인가?
- [ ] 리소스 이름이 올바르게 설정되었는가?
- [ ] 리전이 `ap-northeast-2`로 설정되었는가?
- [ ] 모든 필수 태그가 추가되었는가?
- [ ] 보안 설정이 올바르게 구성되었는가?
- [ ] 리소스에 접근할 수 있는가?"""
        else:  # integration
            return f"""- [ ] {service} 통합이 완료되었는가?
- [ ] 연결 상태가 "Connected"인가?
- [ ] IAM 역할이 올바르게 설정되었는가?
- [ ] 테스트가 성공적으로 완료되었는가?
- [ ] CloudWatch 메트릭이 수집되고 있는가?
- [ ] 에러 로그가 없는가?"""
    
    def _generate_functional_tests(self, service: str, exercise_num: int) -> str:
        """기능 테스트 생성"""
        if exercise_num == 1:
            return f"""### 테스트 1: 기본 기능 확인

**테스트 방법**:
1. {service} 콘솔에서 생성한 리소스 선택
2. 기본 작업 수행 (예: 데이터 업로드, 연결 테스트)
3. 결과 확인

**예상 결과**:
- 작업 성공
- 에러 없음
- 정상 응답 시간

### 테스트 2: 설정 확인

**테스트 방법**:
1. 리소스 설정 페이지 확인
2. 모든 설정값 검증
3. 태그 확인

**예상 결과**:
- 모든 설정이 의도한 대로 구성됨
- 태그가 올바르게 적용됨"""
        else:
            return f"""### 테스트 1: 통합 기능 확인

**테스트 방법**:
1. {service}에서 작업 수행
2. 연결된 서비스에서 결과 확인
3. 데이터 플로우 검증

**예상 결과**:
- 통합이 정상 작동
- 데이터가 올바르게 전달됨
- 지연 시간이 허용 범위 내

### 테스트 2: 장애 복구 테스트

**테스트 방법**:
1. 일시적으로 연결 중단
2. 자동 복구 확인
3. 재연결 후 정상 작동 확인

**예상 결과**:
- 자동 재연결 성공
- 데이터 손실 없음"""

    def _generate_performance_checks(self, service: str) -> str:
        """성능 확인 생성"""
        return f"""**Console 경로**: `CloudWatch > Dashboards`

확인할 메트릭:

1. **응답 시간**
   - 메트릭: Latency 또는 ResponseTime
   - 예상 값: < 100ms
   - 확인 방법: CloudWatch 그래프에서 평균값 확인

2. **처리량**
   - 메트릭: RequestCount 또는 Throughput
   - 예상 값: 테스트 요청 수와 일치
   - 확인 방법: 총 요청 수 카운트

3. **에러율**
   - 메트릭: ErrorCount 또는 FailureRate
   - 예상 값: 0% 또는 < 1%
   - 확인 방법: 에러 카운트 확인

4. **리소스 사용률**
   - 메트릭: CPUUtilization, MemoryUtilization
   - 예상 값: < 80%
   - 확인 방법: 평균 사용률 확인"""
    
    def _generate_log_verification(self, service: str) -> str:
        """로그 검증 생성"""
        return f"""**Console 경로**: `CloudWatch > Log groups`

1. **로그 그룹 찾기**
   - 검색: `/aws/{service.lower().replace(' ', '/')}`
   - 또는 리소스 이름으로 검색

2. **최근 로그 스트림 선택**
   - 가장 최근 타임스탬프의 로그 스트림 클릭

3. **로그 내용 확인**
   - [ ] 에러 메시지 없음
   - [ ] 성공 로그 확인
   - [ ] 처리 시간 확인
   - [ ] 예상치 못한 경고 없음

4. **로그 필터링** (선택사항)
   - Filter pattern: `ERROR` 또는 `WARN`
   - 에러/경고 로그 분석"""
    
    def _generate_troubleshooting_guide(self, service: str, type: str) -> str:
        """문제 해결 가이드 생성"""
        if type == "creation":
            return f"""#### 문제 1: 리소스 생성 실패

**증상**: "Failed to create" 에러 메시지

**원인**:
- IAM 권한 부족
- 리전 제한
- 리소스 한도 초과
- 잘못된 설정값

**해결 방법**:
1. IAM 권한 확인: `IAM > Users > Permissions`
2. 리전 제한 확인: 다른 리전에서 시도
3. 서비스 한도 확인: `Service Quotas`
4. 설정값 재확인: 필수 필드 누락 확인

#### 문제 2: 리소스 접근 불가

**증상**: "Access Denied" 또는 연결 실패

**원인**:
- Security Group 설정 오류
- IAM 역할 미설정
- 네트워크 설정 문제

**해결 방법**:
1. Security Group 인바운드 규칙 확인
2. IAM 역할 및 정책 확인
3. VPC 및 서브넷 설정 확인"""
        else:  # integration
            return f"""#### 문제 1: 통합 연결 실패

**증상**: "Connection failed" 에러

**원인**:
- IAM 역할 권한 부족
- 네트워크 연결 문제
- 서비스 엔드포인트 오류

**해결 방법**:
1. IAM 역할에 필요한 정책 추가
2. VPC 엔드포인트 설정 확인
3. Security Group 규칙 검토

#### 문제 2: 데이터 전송 실패

**증상**: 데이터가 전달되지 않음

**원인**:
- 잘못된 설정
- 권한 문제
- 네트워크 지연

**해결 방법**:
1. 통합 설정 재확인
2. CloudWatch Logs에서 에러 확인
3. 네트워크 연결 테스트"""

    def _generate_debugging_tips(self, service: str) -> str:
        """디버깅 팁 생성"""
        return f"""1. **CloudWatch Logs 활용**
   - 모든 작업은 로그에 기록됨
   - 에러 메시지에서 근본 원인 파악
   - 타임스탬프로 문제 발생 시점 추적

2. **AWS Console 이벤트 확인**
   - Console 경로: `{service} > Events`
   - 최근 이벤트 및 상태 변경 확인
   - 실패한 작업의 상세 정보 확인

3. **IAM Policy Simulator 사용**
   - Console 경로: `IAM > Policy Simulator`
   - 권한 문제 진단
   - 필요한 권한 식별

4. **AWS Support Center 활용**
   - Console 경로: `Support > Support Center`
   - 케이스 생성 및 기술 지원 요청
   - 커뮤니티 포럼 검색"""
    
    def _generate_cleanup_steps(self, service: str, day_number: int, type: str) -> str:
        """정리 단계 생성"""
        service_slug = service.lower().replace(" ", "-")
        
        if type == "basic":
            return f"""#### 1. {service} 리소스 삭제

**Console 경로**: `{service} > Resources`

1. 생성한 리소스 선택: `day{day_number}-{service_slug}`
2. **Actions** > **Delete** 클릭
3. 확인 메시지 입력 (필요시): `delete` 또는 리소스 이름
4. **Delete** 버튼 클릭
5. 삭제 완료 대기 (약 2-5분)

**확인**:
- [ ] 리소스 목록에서 사라짐
- [ ] 상태가 "Deleted" 또는 "Terminated"

#### 2. 연결된 리소스 정리

**Security Group 삭제** (필요시):
- Console 경로: `VPC > Security Groups`
- 선택: `day{day_number}-sg`
- Actions > Delete security group

**IAM 역할 삭제** (필요시):
- Console 경로: `IAM > Roles`
- 선택: `day{day_number}-*-role`
- Delete

#### 3. CloudWatch 로그 삭제 (선택사항)

**Console 경로**: `CloudWatch > Log groups`

1. 검색: `day{day_number}` 또는 `{service_slug}`
2. 선택: 관련 로그 그룹
3. Actions > Delete log group(s)
4. 확인: "Delete" 클릭"""
        else:  # integration
            return f"""#### 1. 통합 연결 해제

**Console 경로**: `{service} > Integrations`

1. 생성한 통합 선택
2. **Disconnect** 또는 **Remove** 클릭
3. 확인: "Yes, disconnect" 클릭

#### 2. CloudWatch 대시보드 삭제

**Console 경로**: `CloudWatch > Dashboards`

1. 선택: `day{day_number}-integration-monitoring`
2. Delete dashboard
3. 확인: "Delete" 클릭

#### 3. IAM 역할 삭제

**Console 경로**: `IAM > Roles`

1. 선택: `day{day_number}-integration-role`
2. Delete
3. 확인: 역할 이름 입력 후 Delete

#### 4. 관련 리소스 정리

- Exercise 1에서 생성한 리소스도 함께 정리
- 모든 연결된 리소스 확인 및 삭제"""

    def _generate_cleanup_verification(self, service: str) -> str:
        """정리 확인 생성"""
        return f"""- [ ] 모든 {service} 리소스가 삭제되었는가?
- [ ] Security Group이 정리되었는가?
- [ ] IAM 역할이 삭제되었는가?
- [ ] CloudWatch 로그 그룹이 삭제되었는가? (선택사항)
- [ ] Billing Dashboard에서 비용 확인
- [ ] 예상 비용 범위 내인가?

**비용 확인 방법**:
1. Console 경로: `Billing > Bills`
2. 현재 월 비용 확인
3. {service} 관련 항목 확인
4. 예상 비용과 비교"""
    
    def _generate_learning_points(self, service: str, exercise_num: int) -> str:
        """학습 포인트 생성"""
        if exercise_num == 1:
            return f"""1. **{service} 기본 개념**
   - {service}의 핵심 기능 및 사용 사례
   - AWS Console을 통한 리소스 생성 방법
   - 기본 설정 및 구성 옵션

2. **보안 베스트 프랙티스**
   - 최소 권한 원칙 적용
   - Security Group 설정
   - 태그를 통한 리소스 관리

3. **비용 관리**
   - Free Tier 활용
   - 리소스 정리의 중요성
   - 비용 모니터링 방법

4. **Console 탐색**
   - AWS Console 효율적 사용법
   - 리전 선택의 중요성
   - 리소스 상태 확인 방법"""
        else:
            return f"""1. **서비스 통합**
   - {service}와 다른 서비스의 통합 방법
   - IAM 역할을 통한 권한 관리
   - 서비스 간 데이터 플로우

2. **모니터링 및 로깅**
   - CloudWatch를 통한 메트릭 수집
   - 로그 분석 및 문제 진단
   - 대시보드 구성

3. **고급 설정**
   - 통합 옵션 및 최적화
   - 성능 튜닝
   - 장애 복구 전략

4. **실무 적용**
   - 프로덕션 환경 고려사항
   - 확장성 및 가용성
   - 비용 최적화 전략"""
    
    def _generate_next_steps(self, day_number: int, exercise_num: int) -> str:
        """다음 단계 생성"""
        exercise_count = self._determine_exercise_count(day_number)
        
        if exercise_num < exercise_count:
            return f"""- [ ] **Exercise {exercise_num + 1}** 진행
- [ ] 이전 Exercise에서 생성한 리소스 활용
- [ ] 통합 기능 테스트

**준비사항**:
- Exercise {exercise_num}에서 생성한 리소스 유지
- 추가 설정 준비"""
        else:
            return f"""- [ ] [Case Study](../case-study.md) 읽기
  - 실제 기업의 {self.get_daily_config(day_number)['primary_services'][0]} 활용 사례
  
- [ ] [Best Practices](../best-practices.md) 학습
  - 프로덕션 환경 구성 방법
  - 보안 및 비용 최적화
  
- [ ] [Troubleshooting](../troubleshooting.md) 검토
  - 일반적인 문제 및 해결 방법
  - 고급 디버깅 기법

- [ ] 리소스 정리
  - 모든 Exercise에서 생성한 리소스 삭제
  - 비용 확인"""

    def _generate_exercise_diagram(self, day_number: int, exercise_num: int) -> str:
        """Exercise 다이어그램 생성"""
        config = self.get_daily_config(day_number)
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        if exercise_num == 1:
            return f"""graph TB
    subgraph "사용자"
        User[실습 참가자]
    end
    
    subgraph "AWS Console - Exercise 1"
        Service[{primary_service}]
        SG[Security Group]
        IAM[IAM Role]
    end
    
    subgraph "모니터링"
        CW[CloudWatch]
    end
    
    User -->|생성 및 설정| Service
    Service --> SG
    Service --> IAM
    Service --> CW
    
    style Service fill:#FF9900
    style User fill:#232F3E
    style CW fill:#FF4F8B"""
        else:
            related_service = config["primary_services"][1] if len(config["primary_services"]) > 1 else "CloudWatch"
            return f"""graph TB
    subgraph "사용자"
        User[실습 참가자]
    end
    
    subgraph "AWS Console - Exercise 2"
        Service1[{primary_service}]
        Service2[{related_service}]
        IAM[IAM Integration Role]
    end
    
    subgraph "모니터링"
        CW[CloudWatch Dashboard]
        Logs[CloudWatch Logs]
    end
    
    User -->|통합 설정| Service1
    Service1 <-->|연결| Service2
    Service1 --> IAM
    Service2 --> IAM
    Service1 --> CW
    Service2 --> CW
    Service1 --> Logs
    Service2 --> Logs
    
    style Service1 fill:#FF9900
    style Service2 fill:#FF9900
    style User fill:#232F3E
    style CW fill:#FF4F8B"""
    
    def _generate_architecture_components(self, primary_service: str, exercise_num: int, related_service: str = None) -> str:
        """아키텍처 구성 요소 설명"""
        if exercise_num == 1:
            return f"""- **{primary_service}**: 메인 리소스
- **Security Group**: 네트워크 접근 제어
- **IAM Role**: 권한 관리
- **CloudWatch**: 메트릭 및 로그 수집"""
        else:
            return f"""- **{primary_service}**: 메인 리소스
- **{related_service}**: 통합 서비스
- **IAM Integration Role**: 서비스 간 권한 관리
- **CloudWatch Dashboard**: 통합 모니터링
- **CloudWatch Logs**: 통합 로그 수집"""

    def populate_template(self, day_number: int, exercise_number: int, template: str) -> str:
        """템플릿 플레이스홀더 치환"""
        exercise_content = self._generate_exercise_content(day_number, exercise_number)
        
        # 기본 정보 치환
        replacements = {
            "{exercise_number}": str(exercise_content["number"]),
            "{exercise_title}": exercise_content["title"],
            "{exercise_objective}": exercise_content["objective"],
            "{estimated_time}": exercise_content["estimated_time"],
            "{region}": exercise_content["region"],
            "{previous_exercise_check}": exercise_content["previous_exercise_check"],
            "{architecture_diagram}": exercise_content["architecture_diagram"],
            "{architecture_components}": exercise_content["architecture_components"],
            "{steps_content}": exercise_content["steps_content"],
            "{verification_checklist}": exercise_content["verification_checklist"],
            "{functional_tests}": exercise_content["functional_tests"],
            "{performance_checks}": exercise_content["performance_checks"],
            "{log_verification}": exercise_content["log_verification"],
            "{common_issues}": exercise_content["common_issues"],
            "{debugging_tips}": exercise_content["debugging_tips"],
            "{cleanup_steps}": exercise_content["cleanup_steps"],
            "{cleanup_verification}": exercise_content["cleanup_verification"],
            "{learning_points}": exercise_content["learning_points"],
            "{next_steps}": exercise_content["next_steps"],
            "{date}": datetime.now().strftime("%Y-%m-%d"),
        }
        
        # 템플릿 치환
        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, str(value))
        
        return result
    
    def generate_exercise_file(self, day_number: int, exercise_number: int, output_path: Optional[Path] = None) -> str:
        """특정 일차의 Exercise 파일 생성
        
        Args:
            day_number: 일차 번호 (1-28)
            exercise_number: Exercise 번호 (1-2)
            output_path: 출력 파일 경로 (None이면 자동 생성)
            
        Returns:
            생성된 콘텐츠 문자열
        """
        # 템플릿 로드
        template = self.load_template()
        
        # 템플릿 치환
        content = self.populate_template(day_number, exercise_number, template)
        
        # 출력 경로 결정
        if output_path is None:
            config = self.get_daily_config(day_number)
            week_number = config["week"]
            
            # Exercise 파일명 생성
            exercise_content = self._generate_exercise_content(day_number, exercise_number)
            title_slug = exercise_content["title"].lower().replace(" ", "-").replace("(", "").replace(")", "")
            filename = f"exercise-{exercise_number}-{title_slug}.md"
            
            output_path = (
                self.output_base_path / 
                f"week{week_number}" / 
                f"day{day_number}" / 
                "hands-on-console" / 
                filename
            )
        
        # 디렉토리 생성
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 파일 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Generated exercise {exercise_number} for Day {day_number}: {output_path}")
        
        return content

    def generate_all_exercises_for_day(self, day_number: int) -> Dict[int, str]:
        """특정 일차의 모든 Exercise 파일 생성
        
        Args:
            day_number: 일차 번호 (1-28)
            
        Returns:
            Exercise 번호별 생성된 파일 경로 딕셔너리
        """
        exercise_count = self._determine_exercise_count(day_number)
        results = {}
        
        for exercise_num in range(1, exercise_count + 1):
            try:
                config = self.get_daily_config(day_number)
                week_number = config["week"]
                
                # Exercise 파일명 생성
                exercise_content = self._generate_exercise_content(day_number, exercise_num)
                title_slug = exercise_content["title"].lower().replace(" ", "-").replace("(", "").replace(")", "")
                filename = f"exercise-{exercise_num}-{title_slug}.md"
                
                output_path = (
                    self.output_base_path / 
                    f"week{week_number}" / 
                    f"day{day_number}" / 
                    "hands-on-console" / 
                    filename
                )
                
                self.generate_exercise_file(day_number, exercise_num, output_path)
                results[exercise_num] = str(output_path)
                
            except Exception as e:
                print(f"✗ Error generating exercise {exercise_num} for Day {day_number}: {e}")
                results[exercise_num] = f"Error: {e}"
        
        return results
    
    def generate_all_exercises(self, start_day: int = 1, end_day: int = 28) -> Dict[int, Dict[int, str]]:
        """모든 일차의 Exercise 파일 생성
        
        Args:
            start_day: 시작 일차 (기본값: 1)
            end_day: 종료 일차 (기본값: 28)
            
        Returns:
            일차별, Exercise 번호별 생성된 파일 경로 딕셔너리
        """
        results = {}
        
        print(f"\n{'='*60}")
        print(f"Exercise Guide Generator - Generating Days {start_day} to {end_day}")
        print(f"{'='*60}\n")
        
        for day in range(start_day, end_day + 1):
            try:
                print(f"\n--- Day {day} ---")
                results[day] = self.generate_all_exercises_for_day(day)
                
            except Exception as e:
                print(f"✗ Error generating exercises for Day {day}: {e}")
                results[day] = {"error": str(e)}
        
        print(f"\n{'='*60}")
        print(f"Generation Complete!")
        
        # 통계 계산
        total_exercises = sum(
            len([v for v in day_results.values() if not str(v).startswith('Error')])
            for day_results in results.values()
            if isinstance(day_results, dict) and 'error' not in day_results
        )
        total_days = sum(
            1 for day_results in results.values()
            if isinstance(day_results, dict) and 'error' not in day_results
        )
        
        print(f"Successfully generated: {total_exercises} exercises across {total_days} days")
        print(f"{'='*60}\n")
        
        return results


# CLI 실행을 위한 메인 함수
def main():
    """CLI 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS SAA Exercise Guide Generator")
    parser.add_argument(
        "--day",
        type=int,
        help="Generate exercises for specific day (1-28)"
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
    
    args = parser.parse_args()
    
    generator = ExerciseGuideGenerator()
    
    if args.day:
        # 단일 일차 생성
        generator.generate_all_exercises_for_day(args.day)
    else:
        # 배치 생성
        generator.generate_all_exercises(args.start, args.end)


if __name__ == "__main__":
    main()
