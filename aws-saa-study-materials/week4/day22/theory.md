# Day 22: CloudWatch & 모니터링

## 학습 목표
- AWS CloudWatch의 핵심 개념과 기능 이해
- 메트릭, 로그, 이벤트의 차이점과 활용 방법 학습
- CloudWatch 대시보드와 알람 설정 방법 습득
- 모니터링 모범 사례와 비용 최적화 전략 이해

## 1. AWS CloudWatch 개요

AWS CloudWatch는 AWS 리소스와 애플리케이션을 실시간으로 모니터링하는 서비스입니다. 시스템 성능을 추적하고, 문제를 조기에 발견하며, 자동화된 대응을 가능하게 합니다.

### CloudWatch의 주요 구성 요소

```mermaid
graph TB
    A[AWS CloudWatch] --> B[CloudWatch Metrics]
    A --> C[CloudWatch Logs]
    A --> D[CloudWatch Events/EventBridge]
    A --> E[CloudWatch Alarms]
    A --> F[CloudWatch Dashboards]
    
    B --> B1[기본 메트릭]
    B --> B2[사용자 정의 메트릭]
    
    C --> C1[로그 그룹]
    C --> C2[로그 스트림]
    C --> C3[로그 인사이트]
    
    D --> D1[스케줄 기반 이벤트]
    D --> D2[AWS 서비스 이벤트]
    
    E --> E1[메트릭 알람]
    E --> E2[복합 알람]
    
    F --> F1[위젯]
    F --> F2[사용자 정의 대시보드]
```

## 2. CloudWatch Metrics (메트릭)

### 2.1 기본 메트릭 vs 사용자 정의 메트릭

**기본 메트릭 (Default Metrics)**
- AWS 서비스에서 자동으로 제공
- 무료로 제공 (5분 간격)
- 예: EC2 CPU 사용률, RDS 연결 수, S3 요청 수

**사용자 정의 메트릭 (Custom Metrics)**
- 애플리케이션에서 직접 전송
- 비용 발생 (메트릭당 과금)
- 1초 단위까지 세밀한 모니터링 가능

### 2.2 주요 AWS 서비스별 메트릭

```mermaid
graph LR
    A[AWS Services] --> B[EC2]
    A --> C[RDS]
    A --> D[ELB]
    A --> E[Lambda]
    A --> F[S3]
    
    B --> B1[CPUUtilization]
    B --> B2[NetworkIn/Out]
    B --> B3[DiskReadOps]
    
    C --> C1[DatabaseConnections]
    C --> C2[ReadLatency]
    C --> C3[WriteLatency]
    
    D --> D1[RequestCount]
    D --> D2[TargetResponseTime]
    D --> D3[HealthyHostCount]
    
    E --> E1[Duration]
    E --> E2[Invocations]
    E --> E3[Errors]
    
    F --> F1[NumberOfObjects]
    F --> F2[BucketSizeBytes]
    F --> F3[AllRequests]
```

### 2.3 메트릭 해상도와 보존 기간

| 해상도 | 보존 기간 | 용도 |
|--------|-----------|------|
| 1분 | 15일 | 상세 모니터링 |
| 5분 | 63일 | 기본 모니터링 |
| 1시간 | 455일 | 장기 트렌드 분석 |

## 3. CloudWatch Logs

### 3.1 로그 구조

```mermaid
graph TB
    A[CloudWatch Logs] --> B[로그 그룹]
    B --> C[로그 스트림 1]
    B --> D[로그 스트림 2]
    B --> E[로그 스트림 N]
    
    C --> F[로그 이벤트 1]
    C --> G[로그 이벤트 2]
    C --> H[로그 이벤트 N]
    
    F --> I[타임스탬프]
    F --> J[메시지]
```

### 3.2 로그 수집 방법

**1. CloudWatch Logs Agent**
- EC2 인스턴스에 설치
- 로그 파일을 자동으로 CloudWatch로 전송
- 구버전 에이전트 (레거시)

**2. CloudWatch Unified Agent**
- 로그와 메트릭을 모두 수집
- 더 많은 시스템 메트릭 제공
- 권장되는 최신 에이전트

**3. AWS SDK/CLI**
- 애플리케이션에서 직접 로그 전송
- 프로그래밍 방식으로 로그 관리

### 3.3 CloudWatch Logs Insights

로그 데이터를 쿼리하고 분석하는 서비스입니다.

```sql
-- 예시 쿼리: 에러 로그 검색
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 100

-- 예시 쿼리: Lambda 함수 실행 시간 분석
fields @timestamp, @duration
| filter @type = "REPORT"
| stats avg(@duration), max(@duration), min(@duration) by bin(5m)
```

## 4. CloudWatch Alarms (알람)

### 4.1 알람 유형

```mermaid
graph TB
    A[CloudWatch Alarms] --> B[메트릭 알람]
    A --> C[복합 알람]
    
    B --> B1[정적 임계값]
    B --> B2[이상 탐지]
    
    C --> C1[여러 알람 조합]
    C --> C2[논리 연산자 사용]
    
    B1 --> D[알람 상태]
    B2 --> D
    C1 --> D
    C2 --> D
    
    D --> E[OK]
    D --> F[ALARM]
    D --> G[INSUFFICIENT_DATA]
```

### 4.2 알람 작업 (Actions)

알람이 트리거될 때 수행할 수 있는 작업들:

1. **SNS 알림**: 이메일, SMS, HTTP 엔드포인트로 알림
2. **Auto Scaling 작업**: EC2 인스턴스 자동 확장/축소
3. **EC2 작업**: 인스턴스 중지, 종료, 재부팅, 복구
4. **Systems Manager 작업**: 자동화된 문제 해결

### 4.3 이상 탐지 (Anomaly Detection)

```mermaid
graph LR
    A[Historical Data] --> B[Machine Learning Model]
    B --> C[Expected Values Band]
    C --> D[Anomaly Detection]
    
    D --> E[Normal Behavior]
    D --> F[Anomalous Behavior]
    
    F --> G[Alarm Triggered]
```

## 5. CloudWatch Dashboards

### 5.1 대시보드 구성 요소

```mermaid
graph TB
    A[CloudWatch Dashboard] --> B[위젯 1: 라인 차트]
    A --> C[위젯 2: 숫자 표시]
    A --> D[위젯 3: 게이지]
    A --> E[위젯 4: 로그 테이블]
    
    B --> F[메트릭 데이터]
    C --> G[단일 값]
    D --> H[임계값 비교]
    E --> I[로그 쿼리 결과]
```

### 5.2 위젯 유형

| 위젯 유형 | 용도 | 데이터 소스 |
|-----------|------|-------------|
| Line | 시간별 트렌드 | 메트릭 |
| Stacked area | 누적 데이터 | 메트릭 |
| Number | 현재 값 | 메트릭 |
| Gauge | 임계값 대비 현재 상태 | 메트릭 |
| Pie | 비율 표시 | 메트릭 |
| Log table | 로그 검색 결과 | 로그 |

## 6. CloudWatch Events / EventBridge

### 6.1 이벤트 기반 아키텍처

```mermaid
graph LR
    A[Event Source] --> B[EventBridge]
    B --> C[Event Rule]
    C --> D[Target 1: Lambda]
    C --> E[Target 2: SNS]
    C --> F[Target 3: SQS]
    
    A1[EC2 State Change] --> B
    A2[S3 Object Created] --> B
    A3[Custom Application] --> B
```

### 6.2 이벤트 패턴 예시

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["terminated"]
  }
}
```

## 7. 모니터링 모범 사례

### 7.1 계층별 모니터링 전략

```mermaid
graph TB
    A[모니터링 계층] --> B[인프라 계층]
    A --> C[애플리케이션 계층]
    A --> D[비즈니스 계층]
    
    B --> B1[CPU, 메모리, 디스크]
    B --> B2[네트워크 트래픽]
    B --> B3[시스템 가용성]
    
    C --> C1[응답 시간]
    C --> C2[에러율]
    C --> C3[처리량]
    
    D --> D1[사용자 경험]
    D --> D2[비즈니스 KPI]
    D --> D3[수익 지표]
```

### 7.2 알람 설정 가이드라인

**DO (권장사항)**
- 비즈니스에 중요한 메트릭에만 알람 설정
- 알람 피로도를 방지하기 위해 적절한 임계값 설정
- 복합 알람을 사용하여 거짓 양성 줄이기
- 알람 설명에 대응 방법 포함

**DON'T (피해야 할 것)**
- 너무 많은 알람 설정 (알람 피로도)
- 너무 민감한 임계값 설정
- 대응 계획 없는 알람 설정
- 중복된 알람 설정

### 7.3 비용 최적화

```mermaid
graph TB
    A[CloudWatch 비용 최적화] --> B[메트릭 관리]
    A --> C[로그 관리]
    A --> D[대시보드 관리]
    
    B --> B1[불필요한 사용자 정의 메트릭 제거]
    B --> B2[메트릭 해상도 조정]
    
    C --> C1[로그 보존 기간 설정]
    C --> C2[로그 필터링]
    C --> C3[S3로 아카이브]
    
    D --> D1[공유 대시보드 활용]
    D --> D2[불필요한 위젯 제거]
```

## 8. 실제 사용 시나리오

### 8.1 웹 애플리케이션 모니터링

```mermaid
graph TB
    A[사용자] --> B[CloudFront]
    B --> C[ALB]
    C --> D[EC2 Instances]
    D --> E[RDS]
    
    F[CloudWatch] --> G[ALB 메트릭]
    F --> H[EC2 메트릭]
    F --> I[RDS 메트릭]
    F --> J[애플리케이션 로그]
    
    G --> K[응답 시간 알람]
    H --> L[CPU 사용률 알람]
    I --> M[DB 연결 수 알람]
    J --> N[에러 로그 알람]
```

### 8.2 서버리스 애플리케이션 모니터링

```mermaid
graph LR
    A[API Gateway] --> B[Lambda]
    B --> C[DynamoDB]
    
    D[CloudWatch] --> E[API Gateway 메트릭]
    D --> F[Lambda 메트릭]
    D --> G[DynamoDB 메트릭]
    
    E --> H[4XX/5XX 에러 알람]
    F --> I[Duration/Error 알람]
    G --> J[Throttle 알람]
```

## 9. 고급 기능

### 9.1 Container Insights
- ECS, EKS, Fargate 컨테이너 모니터링
- 컨테이너 수준의 메트릭 제공
- 성능 로그 자동 수집

### 9.2 Lambda Insights
- Lambda 함수 성능 모니터링
- 메모리 사용량, 초기화 시간 등 상세 메트릭
- 비용 최적화 권장사항 제공

### 9.3 Application Insights
- .NET 및 SQL Server 애플리케이션 자동 모니터링
- 애플리케이션 상태 자동 감지
- 문제 진단 및 해결 방안 제시

## 10. 다른 AWS 서비스와의 통합

### 10.1 AWS X-Ray
- 분산 추적 서비스
- CloudWatch와 연동하여 성능 분석
- 마이크로서비스 아키텍처 디버깅

### 10.2 AWS Systems Manager
- CloudWatch 알람과 연동
- 자동화된 문제 해결
- 패치 관리 및 구성 관리

### 10.3 AWS Config
- 리소스 구성 변경 추적
- CloudWatch Events와 연동
- 컴플라이언스 모니터링

## 요약

CloudWatch는 AWS 환경의 종합적인 모니터링 솔루션입니다. 메트릭, 로그, 이벤트를 통합 관리하며, 대시보드와 알람을 통해 실시간 모니터링과 자동화된 대응을 가능하게 합니다.

**핵심 포인트:**
- 메트릭: 성능 지표 수집 및 분석
- 로그: 애플리케이션 및 시스템 로그 중앙 관리
- 알람: 임계값 기반 자동 알림 및 대응
- 대시보드: 시각적 모니터링 인터페이스
- 이벤트: 이벤트 기반 자동화

다음 실습에서는 실제 CloudWatch 대시보드를 구성하고 알람을 설정해보겠습니다.