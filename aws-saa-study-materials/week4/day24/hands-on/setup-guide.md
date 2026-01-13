# Day 24 실습: AWS Cost Explorer 및 예산 설정

## 실습 개요
이번 실습에서는 AWS Cost Explorer를 사용하여 비용을 분석하고, AWS Budgets를 통해 예산을 설정하는 방법을 학습합니다. 또한 비용 최적화 권장사항을 확인하고 적용하는 과정을 실습합니다.

## 사전 준비사항
- AWS 계정 (Free Tier 권장)
- 최소 1개월간의 AWS 사용 이력 (비용 데이터 확인을 위해)
- 관리자 권한 또는 Billing 권한이 있는 IAM 사용자

## 실습 1: Cost Explorer 설정 및 기본 분석

### 1.1 Cost Explorer 활성화

1. **AWS Management Console 접속**
   - AWS Console에 로그인
   - 우측 상단의 계정명 클릭 → "Billing and Cost Management" 선택

2. **Cost Explorer 활성화**
   ```
   📍 경로: Billing Dashboard → Cost Explorer
   ```
   - 좌측 메뉴에서 "Cost Explorer" 클릭
   - "Launch Cost Explorer" 버튼 클릭
   - 활성화까지 최대 24시간 소요 (이미 활성화된 경우 바로 사용 가능)

3. **Cost Explorer 대시보드 확인**
   - 기본 비용 및 사용량 차트 확인
   - 지난 12개월 비용 트렌드 분석
   - 서비스별 비용 분포 확인

### 1.2 비용 분석 실습

1. **월별 비용 분석**
   ```
   📍 설정 경로: Cost Explorer → Reports → Create report
   ```
   - "Create report" 버튼 클릭
   - Report type: "Cost and usage"
   - Time range: "Last 6 months"
   - Granularity: "Monthly"
   - Group by: "Service"
   - "Create report" 클릭

2. **서비스별 상세 분석**
   - 가장 비용이 많이 드는 서비스 3개 식별
   - 각 서비스의 월별 비용 변화 추이 분석
   - 비정상적인 비용 증가 구간 확인

3. **일별 비용 분석**
   ```
   📍 설정: Granularity를 "Daily"로 변경
   ```
   - 지난 30일간 일별 비용 변화 확인
   - 주말과 평일의 비용 패턴 비교
   - 특정 날짜의 비용 급증 원인 분석

### 1.3 고급 필터링 및 그룹화

1. **태그 기반 분석**
   ```
   📍 설정: Group by → Tag → Environment (또는 사용 중인 태그)
   ```
   - 환경별(Production, Development, Test) 비용 분석
   - 프로젝트별 비용 할당 확인
   - 부서별 비용 분포 분석

2. **지역별 비용 분석**
   ```
   📍 설정: Group by → Region
   ```
   - 사용 중인 AWS 리전별 비용 비교
   - 데이터 전송 비용 분석
   - 리전별 서비스 사용 패턴 확인

3. **계정별 분석 (Organizations 사용 시)**
   ```
   📍 설정: Group by → Linked Account
   ```
   - 연결된 계정별 비용 분석
   - 계정별 서비스 사용 패턴 비교
   - 비용 할당 및 차지백 데이터 확인

## 실습 2: AWS Budgets 설정

### 2.1 기본 비용 예산 생성

1. **Budgets 서비스 접속**
   ```
   📍 경로: Billing Dashboard → Budgets
   ```
   - 좌측 메뉴에서 "Budgets" 클릭
   - "Create budget" 버튼 클릭

2. **예산 유형 선택**
   ```
   📍 설정: Budget type → Cost budget
   ```
   - "Cost budget" 선택
   - "Next" 클릭

3. **예산 세부사항 설정**
   ```
   📍 예산 설정 예시:
   - Budget name: "Monthly-Total-Cost-Budget"
   - Period: Monthly
   - Budget renewal type: Recurring
   - Start month: 현재 월
   - Budgeted amount: $50 (또는 적절한 금액)
   ```

4. **필터 설정 (선택사항)**
   ```
   📍 필터 옵션:
   - Service: 특정 서비스만 포함
   - Linked Account: 특정 계정만 포함
   - Tag: 특정 태그가 있는 리소스만 포함
   ```

### 2.2 알림 설정

1. **알림 임계값 설정**
   ```
   📍 알림 설정 예시:
   - Alert 1: Actual cost > 80% of budgeted amount
   - Alert 2: Actual cost > 100% of budgeted amount  
   - Alert 3: Forecasted cost > 120% of budgeted amount
   ```

2. **알림 수신자 설정**
   ```
   📍 설정 항목:
   - Email recipients: 본인 이메일 주소 입력
   - SNS topic: (선택사항) SNS 토픽 생성 및 연결
   ```

3. **예산 생성 완료**
   - 설정 내용 검토
   - "Create budget" 클릭
   - 생성된 예산 확인

### 2.3 서비스별 예산 생성

1. **EC2 서비스 예산**
   ```
   📍 설정:
   - Budget name: "EC2-Monthly-Budget"
   - Service filter: Amazon Elastic Compute Cloud - Compute
   - Budgeted amount: $20
   ```

2. **S3 서비스 예산**
   ```
   📍 설정:
   - Budget name: "S3-Monthly-Budget"
   - Service filter: Amazon Simple Storage Service
   - Budgeted amount: $10
   ```

## 실습 3: 사용량 예산 설정

### 3.1 EC2 사용량 예산

1. **사용량 예산 생성**
   ```
   📍 경로: Create budget → Usage budget
   ```
   - Budget type: "Usage budget" 선택
   - Service: "Amazon Elastic Compute Cloud - Compute"
   - Usage type: "BoxUsage" (EC2 인스턴스 사용 시간)

2. **사용량 한도 설정**
   ```
   📍 설정 예시:
   - Budget name: "EC2-Usage-Budget"
   - Usage amount: 100 hours
   - Unit: Hrs (시간)
   ```

### 3.2 S3 스토리지 사용량 예산

1. **S3 스토리지 예산**
   ```
   📍 설정:
   - Service: Amazon Simple Storage Service
   - Usage type: TimedStorage-ByteHrs
   - Usage amount: 10 GB-Month
   ```

## 실습 4: Reserved Instance 권장사항 확인

### 4.1 RI 권장사항 분석

1. **RI 권장사항 접속**
   ```
   📍 경로: Cost Explorer → Reserved Instances → Recommendations
   ```
   - "Reserved Instances" 메뉴 클릭
   - "Recommendations" 탭 선택

2. **권장사항 분석**
   ```
   📍 확인 항목:
   - 권장되는 RI 유형 및 수량
   - 예상 절약 금액
   - 투자 회수 기간
   - 활용률 예측
   ```

3. **RI 구매 시뮬레이션**
   - 권장사항 중 하나 선택
   - 구매 옵션 비교 (전체 선불, 부분 선불, 무선불)
   - 절약 효과 계산

### 4.2 Savings Plans 권장사항

1. **Savings Plans 분석**
   ```
   📍 경로: Cost Explorer → Savings Plans → Recommendations
   ```
   - Compute Savings Plans vs EC2 Instance Savings Plans 비교
   - 약정 기간별 절약 효과 분석
   - 유연성 vs 할인율 트레이드오프 검토

## 실습 5: 비용 이상 탐지 설정

### 5.1 Cost Anomaly Detection 설정

1. **이상 탐지 서비스 접속**
   ```
   📍 경로: Billing Dashboard → Cost Anomaly Detection
   ```
   - "Cost Anomaly Detection" 메뉴 클릭
   - "Create monitor" 버튼 클릭

2. **모니터 설정**
   ```
   📍 설정 예시:
   - Monitor name: "Total-Cost-Anomaly-Monitor"
   - Monitor type: AWS services
   - Dimension: Service
   - Match options: All AWS services
   ```

3. **알림 설정**
   ```
   📍 알림 설정:
   - Threshold: $10 (이상 금액 임계값)
   - Frequency: Individual alerts
   - Recipients: 이메일 주소 입력
   ```

### 5.2 서비스별 이상 탐지

1. **EC2 이상 탐지**
   ```
   📍 설정:
   - Monitor name: "EC2-Anomaly-Monitor"
   - Service: Amazon Elastic Compute Cloud - Compute
   - Threshold: $5
   ```

2. **S3 이상 탐지**
   ```
   📍 설정:
   - Monitor name: "S3-Anomaly-Monitor"
   - Service: Amazon Simple Storage Service
   - Threshold: $3
   ```

## 실습 6: 비용 최적화 권장사항 확인

### 6.1 Trusted Advisor 활용

1. **Trusted Advisor 접속**
   ```
   📍 경로: Support → Trusted Advisor
   ```
   - AWS Support Center 접속
   - "Trusted Advisor" 메뉴 클릭

2. **비용 최적화 체크**
   ```
   📍 확인 항목:
   - Idle Load Balancers
   - Unassociated Elastic IP Addresses
   - Underutilized Amazon EBS Volumes
   - Underutilized Amazon EC2 Instances
   ```

3. **권장사항 적용**
   - 각 권장사항의 상세 내용 확인
   - 예상 절약 금액 검토
   - 안전하게 적용 가능한 항목 식별

### 6.2 Cost Optimization Hub

1. **최적화 허브 접속**
   ```
   📍 경로: Cost Explorer → Cost Optimization Hub
   ```
   - 통합된 비용 최적화 권장사항 확인
   - 우선순위별 권장사항 정렬
   - 예상 절약 효과 분석

## 실습 7: 비용 보고서 생성 및 공유

### 7.1 정기 보고서 설정

1. **보고서 생성**
   ```
   📍 설정:
   - Report name: "Monthly-Cost-Report"
   - Time range: Last month
   - Granularity: Monthly
   - Group by: Service
   ```

2. **보고서 저장 및 공유**
   - "Save as..." 버튼 클릭
   - 보고서 이름 지정
   - 팀원과 공유 설정

### 7.2 대시보드 생성

1. **커스텀 대시보드**
   ```
   📍 구성 요소:
   - 월별 총 비용 트렌드
   - 서비스별 비용 분포
   - 예산 대비 실제 비용
   - 비용 최적화 기회
   ```

## 실습 검증 및 정리

### 검증 체크리스트

- [ ] Cost Explorer가 활성화되고 비용 데이터를 확인할 수 있음
- [ ] 월별 비용 예산이 생성되고 알림이 설정됨
- [ ] 서비스별 예산이 최소 2개 이상 생성됨
- [ ] 사용량 예산이 1개 이상 생성됨
- [ ] Cost Anomaly Detection이 설정됨
- [ ] RI 또는 Savings Plans 권장사항을 확인함
- [ ] Trusted Advisor 비용 최적화 권장사항을 검토함
- [ ] 정기 비용 보고서가 생성됨

### 실습 후 정리

1. **테스트 리소스 정리**
   - 실습용으로 생성한 불필요한 예산 삭제
   - 테스트 알림 설정 정리
   - 임시 보고서 삭제

2. **실제 운영 설정**
   - 실제 비즈니스 요구사항에 맞는 예산 설정
   - 적절한 알림 임계값 조정
   - 정기적인 비용 리뷰 일정 수립

## 추가 학습 리소스

### AWS 문서
- [AWS Cost Explorer User Guide](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html)
- [AWS Budgets User Guide](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
- [AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/getting-started-ad.html)

### 모범 사례
- 월별 정기 비용 리뷰 실시
- 예산 임계값을 점진적으로 조정
- 팀 전체가 비용 인식을 가질 수 있도록 교육
- 자동화된 비용 최적화 도구 활용

## 다음 단계

내일은 AWS Well-Architected Framework를 학습하며, 비용 최적화를 포함한 5가지 핵심 원칙을 종합적으로 다룰 예정입니다. 오늘 학습한 비용 관리 지식이 Well-Architected Framework의 비용 최적화 원칙과 어떻게 연결되는지 확인해보세요.