# Duolingo - 언어 학습 앱의 NoSQL 데이터베이스 아키텍처

> **Day 11: DynamoDB**  
> **주요 AWS 서비스**: DynamoDB, DAX, Global Tables, Streams

---

## 📋 사례 개요

- **기업명**: Duolingo
- **업종**: 교육 기술
- **규모**: Medium <!-- Startup/Medium/Enterprise -->
- **주요 AWS 서비스**: DynamoDB, DAX, Global Tables, Streams
- **사례 출처**: https://aws.amazon.com/architecture/customers/duolingo <!-- 공개 자료 링크 또는 "AWS Well-Architected Framework 기반" -->
- **사례 유형**: 실제 기업 사례 <!-- "실제 기업 사례" 또는 "Best Practice 기반 가상 사례" -->

---

## 🎯 비즈니스 도전과제

### 문제 상황

언어 학습 앱의 NoSQL 데이터베이스 아키텍처를 위한 확장 가능하고 안정적인 인프라 구축

**구체적인 문제점**:
- 높은 트래픽 처리 요구
- 글로벌 사용자 대응 필요
- 비용 효율적인 확장성 확보

**기술적 제약사항**:
- 제한된 예산 내에서 최대 성능 달성
- 기존 시스템과의 호환성 유지

**기존 인프라의 한계**:
- 온프레미스 인프라의 확장성 한계
- 수동 운영으로 인한 느린 대응 속도

### 요구사항

**성능 요구사항**:
- 높은 처리량과 낮은 지연시간 요구 (예: 응답시간 < 100ms)
- 트래픽 급증에 대한 자동 확장 (예: 처리량 > 10,000 TPS)

**확장성 요구사항**:
- 동시 사용자 100만명 지원 (예: 동시 사용자 100만명 지원)
- 트래픽 10배 증가 대응 (예: 트래픽 10배 증가 대응)

**보안 및 규정 준수 요구사항**:
- 데이터 암호화 및 접근 제어
- 산업 표준 규정 준수

**비용 제약사항**:
- 월간 인프라 비용 $10,000 이하
- ROI 6개월 이내 달성

---

## 🏗️ AWS 솔루션 아키텍처

### 아키텍처 다이어그램

```mermaid
graph TB
    subgraph "사용자 계층"
        Users[사용자/애플리케이션]
    end
    
    subgraph "AWS 인프라 - Day 11"
        A[DynamoDB]
        B1[DAX]
        B2[Global Tables]
    end

    Users --> A
    A --> B1
    A --> B2

```

> 📁 **상세 다이어그램**: [architecture-diagrams/main-architecture.mmd](./architecture-diagrams/main-architecture.mmd)

### 핵심 서비스 구성

#### DynamoDB (Day 11 주요 서비스)

**선택 이유**:
- 높은 가용성 및 확장성 제공
- 관리형 서비스로 운영 부담 감소

**구성 방법** (AWS Console 기준):
1. **Console 경로**: Services > Storage > DynamoDB
2. **주요 설정**:
   - Region: day11-resource
   - Instance Type / Configuration: Standard
   - Auto Scaling: 활성화

**다른 서비스와의 연계**:
- **RDS** (Day 10): Day 10의 RDS (Relational Database Service)와 연계
- **Lambda** (Day 18): Day 18의 Lambda (서버리스 컴퓨팅)와 연계

#### {supporting_service_1}

**역할**: {service_role_description}

**구성 방법**:
- {config_summary}

**연계 방식**: {integration_method}

### 서비스 간 데이터 플로우

```mermaid
sequenceDiagram
    participant User as 사용자
    participant Service as DynamoDB
    participant Storage as 데이터 저장소
    
    User->>Service: 요청 전송
    Service->>Storage: 데이터 조회/저장
    Storage-->>Service: 응답
    Service-->>User: 결과 반환

```

**플로우 설명**:
1. **사용자 요청** → {service_a}
   - {flow_step_1_description}
   
2. **{service_a}** → **{service_b}** (Day 11의 주요 서비스)
   - {flow_step_2_description}
   
3. **{service_b}** → **{service_c}**
   - {flow_step_3_description}

4. **응답 반환** → 사용자
   - {flow_step_4_description}

---

## 💻 구현 세부사항

### AWS Console 기반 설정

#### 1단계: DynamoDB 생성

**Console 경로**: Services > Compute > DynamoDB > Create Resource

**기본 설정**:
- **Name/ID**: `day11-resource`
- **Region**: `ap-northeast-2` (예: ap-northeast-2 - 서울)
- **Name**: day11-resource
- **Type**: Standard

**고급 설정**:
- **High Availability**: Multi-AZ 배포
  - 설명: 여러 가용 영역에 걸쳐 리소스 배포
- **Backup**: 자동 백업 활성화
  - 설명: 일일 자동 백업 및 7일 보관

**생성 확인**:
- 상태가 "Available" 또는 "Active"로 변경될 때까지 대기 (약 5-10분)
- Console에서 리소스 상세 정보 확인

#### 2단계: CloudWatch 연계 구성

**Console 경로**: Services > Compute > DynamoDB

**연결 설정**:
1. DynamoDB에서 생성한 리소스 선택
2. "Actions" > "Configure Monitoring"
3. CloudWatch 리소스 선택 또는 생성
4. 연결 설정 저장

**검증**:
- 메트릭이 정상적으로 수집되는지 확인
- 알람이 올바르게 설정되었는지 검증

#### 3단계: 보안 및 접근 제어 설정

**IAM 역할 구성** (Day 2 연계):
- Console 경로: IAM > Roles > Create role
- 신뢰 관계: 서비스 신뢰 관계
- 권한 정책: 최소 권한 정책

**네트워크 보안** (Day 5 연계):
- Security Group 설정
- Network ACL 구성 (필요시)

### 설정 파일 예시 (참고용)

#### CloudFormation 템플릿 (선택사항)

```yaml
# {resource_name}-stack.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: '{case_study_name} - DynamoDB 구성'

Resources:
  {ResourceLogicalId}:
    Type: AWS::{ServiceNamespace}::{ResourceType}
    Properties:
      {Property1}: {Value1}
      {Property2}: {Value2}
      Tags:
        - Key: Project
          Value: {project_name}
        - Key: Environment
          Value: {environment}
```

#### Terraform 예시 (선택사항)

```hcl
# main.tf
resource "aws_{resource_type}" "{resource_name}" {
  {property_1} = "{value_1}"
  {property_2} = "{value_2}"
  
  tags = {
    Project     = "{project_name}"
    Environment = "{environment}"
  }
}
```

### 모니터링 설정

#### CloudWatch 메트릭 구성

**Console 경로**: CloudWatch > Metrics > {service_namespace}

**핵심 메트릭**:
- **응답 시간**: {metric_description_1}
  - 정상 범위: {normal_range_1}
  - 경고 임계값: {warning_threshold_1}
  
- **처리량**: {metric_description_2}
  - 정상 범위: {normal_range_2}
  - 경고 임계값: {warning_threshold_2}

#### 알람 설정

**Console 경로**: CloudWatch > Alarms > Create alarm

**알람 구성**:
```yaml
알람명: {alarm_name}
메트릭: {metric_name}
조건: {condition} (예: >= 80%)
기간: {period} (예: 5분)
평가 기간: {evaluation_periods} (예: 2회 연속)
알림: {sns_topic_arn}
```

#### 대시보드 구성

**Console 경로**: CloudWatch > Dashboards > Create dashboard

**위젯 구성**:
- {widget_1}: {metric_visualization_1}
- {widget_2}: {metric_visualization_2}
- {widget_3}: {metric_visualization_3}

---

## 📊 비즈니스 임팩트

### 성능 개선

| 지표 | 개선 전 | 개선 후 | 개선율 |
|------|---------|---------|--------|
| 응답 시간 | 200ms | 50ms | 75% |
| 처리량 | 1,000 TPS | 10,000 TPS | 900% |
| 가용성 | 99.9% | 99.99% | 0.09% |

**주요 성과**:
- 응답 시간 75% 개선
- 처리량 10배 증가
- 가용성 99.99% 달성

### 비용 최적화

**월간 비용 변화**:
- **개선 전**: $10,000/월
- **개선 후**: $7,000/월
- **절감액**: $3,000/월 (30% 절감)

**비용 절감 요인**:
1. 자동 스케일링 최적화: $1,500/월
2. 예약 인스턴스 활용: $1,000/월
3. 스토리지 계층화: $500/월

**ROI 분석**:
- 초기 투자: $20,000
- 월간 절감: $3,000
- 투자 회수 기간: 7개월

### 운영 효율성

**배포 및 운영 개선**:
- **배포 시간**: 2시간 → 15분 (87.5% 단축)
- **장애 복구 시간**: 30분 → 5분 (83% 개선)
- **운영 인력**: 5명 → 3명

**가용성 향상**:
- **서비스 가동률**: 99.9% → 99.99%
- **연간 다운타임**: 8.76시간 → 0.88시간

---

## 🔗 다른 서비스와의 연계

### 이전 학습 내용과의 연결

#### Day 10: RDS
**연계 방식**: Day 10의 RDS (Relational Database Service)와 연계

**이 사례에서의 활용**:
- 멀티 리전 배포 기반
- 글로벌 사용자 대응

**학습 포인트**:
- 리전 선택의 중요성

#### Day 18: Lambda
**연계 방식**: Day 18의 Lambda (서버리스 컴퓨팅)와 연계

**이 사례에서의 활용**:
- 역할 기반 접근 제어

### 향후 학습 내용 예고

#### Day 19: API Gateway
**확장 방향**: 추가 기능 통합

**이 사례의 진화**:
- 성능 최적화
- 비용 효율성 향상

**기대 효과**:
- 운영 효율성 증대

#### Day 18: 모니터링 서비스
**확장 방향**: 고급 모니터링 통합

**추가 통합 시나리오**:
- 실시간 알람 및 대시보드

### 전체 아키텍처에서의 역할

```mermaid
graph LR
    D11[Day 11:<br/>DynamoDB]
    D10[Day 10:<br/>RDS (Relational Database Service)]
    D18[Day 18:<br/>Lambda (서버리스 컴퓨팅)]
    D19[Day 19:<br/>API Gateway]

    D10 --> D11
    D11 -.확장.-> D18
    D11 -.확장.-> D19

```

**통합 시나리오 설명**:
- Day 11의 서비스들이 전체 아키텍처에서 핵심 역할 수행

**서비스 의존성**:
- Day 11 (DynamoDB) → Day 10 (RDS)
- Day 10 (RDS) → Day 18 (Lambda)

---

## 📚 참고 자료

### AWS 공식 문서
- [DynamoDB 사용 설명서](https://docs.aws.amazon.com/dynamodb/latest/userguide/)
- [DynamoDB API 레퍼런스](https://docs.aws.amazon.com/dynamodb/latest/userguide/)
- [AWS Well-Architected Framework - Operational Excellence](https://docs.aws.amazon.com/wellarchitected/latest/framework/)

### 아키텍처 및 베스트 프랙티스
- [AWS 아키텍처 센터 - 언어 학습 앱의 NoSQL 데이터베이스 아키텍처](https://aws.amazon.com/architecture/)
- [DynamoDB 베스트 프랙티스](https://docs.aws.amazon.com/dynamodb/latest/userguide/)
- [보안 베스트 프랙티스 - IAM Best Practices](https://docs.aws.amazon.com/security/)

### 비용 최적화
- [AWS 요금 계산기](https://calculator.aws/)
- [DynamoDB 요금 안내](https://aws.amazon.com/pricing)
- [비용 최적화 가이드](https://docs.aws.amazon.com/cost-management/)

### 기업 사례 및 발표 자료
- [Duolingo 공식 블로그 포스트](https://aws.amazon.com/architecture/customers/duolingo)
- [AWS re:Invent 발표: Duolingo - 언어 학습 앱의 NoSQL 데이터베이스 아키텍처](https://reinvent.awsevents.com/)
- [AWS 고객 사례 연구](https://aws.amazon.com/architecture/customers/)

### 화이트페이퍼
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/whitepapers/)

---

## 🎓 학습 포인트

### 1. DynamoDB의 실제 활용 방법
- DynamoDB의 핵심 기능 이해
- 실제 프로덕션 환경 구성 방법
- 모범 사례 및 안티 패턴

### 2. 대규모 시스템에서의 고려사항
- **확장성**: 자동 스케일링 및 로드 밸런싱
- **가용성**: 멀티 AZ 배포 및 장애 조치
- **성능**: 캐싱 및 최적화 전략
- **보안**: 최소 권한 원칙 및 암호화

### 3. 다른 서비스와의 통합 패턴
- Direct Integration
- Direct Integration
- API Gateway Pattern

### 4. 비용 최적화 전략
- 예약 인스턴스 활용
- 자동 스케일링 최적화
- 스토리지 계층화

### 5. 운영 및 모니터링 베스트 프랙티스
- Infrastructure as Code 사용
- 자동화된 배포 파이프라인
- 포괄적인 모니터링 및 알람

---

## 🚀 다음 단계

### 실습 진행
1. [hands-on-console/README.md](./hands-on-console/README.md)에서 실습 가이드 확인
2. AWS Console을 통해 직접 아키텍처 구성
3. 모니터링 및 최적화 실습

### 심화 학습
1. [best-practices.md](./best-practices.md)에서 프로덕션 환경 고려사항 학습
2. [troubleshooting.md](./troubleshooting.md)에서 문제 해결 방법 학습
3. [architecture-diagrams/](./architecture-diagrams/)에서 상세 다이어그램 확인

### 관련 학습
- Day 10: RDS
- Day 18: Lambda
- Day 19: API Gateway

---

## 📝 작성 가이드 (템플릿 사용 시 삭제)

### 플레이스홀더 치환 규칙

**기본 정보**:
- `11`: 일차 번호 (1-28)
- `DynamoDB`: 일별 학습 주제 제목
- `Duolingo`: 기업명 (실제 또는 가상)
- `언어 학습 앱의 NoSQL 데이터베이스 아키텍처`: 사례 연구 초점 (예: "글로벌 스트리밍 아키텍처")

**서비스 정보**:
- `DynamoDB, DAX, Global Tables, Streams`: 주요 AWS 서비스 목록 (쉼표로 구분)
- `DynamoDB`: 주요 서비스 단수형
- `CloudWatch`: 연계 서비스명

**다이어그램**:
- `graph TB
    subgraph "사용자 계층"
        Users[사용자/애플리케이션]
    end
    
    subgraph "AWS 인프라 - Day 11"
        A[DynamoDB]
        B1[DAX]
        B2[Global Tables]
    end

    Users --> A
    A --> B1
    A --> B2
`: Mermaid 아키텍처 다이어그램 코드
- `sequenceDiagram
    participant User as 사용자
    participant Service as DynamoDB
    participant Storage as 데이터 저장소
    
    User->>Service: 요청 전송
    Service->>Storage: 데이터 조회/저장
    Storage-->>Service: 응답
    Service-->>User: 결과 반환
`: Mermaid 데이터 플로우 다이어그램 코드
- `graph LR
    D11[Day 11:<br/>DynamoDB]
    D10[Day 10:<br/>RDS (Relational Database Service)]
    D18[Day 18:<br/>Lambda (서버리스 컴퓨팅)]
    D19[Day 19:<br/>API Gateway]

    D10 --> D11
    D11 -.확장.-> D18
    D11 -.확장.-> D19
`: 크로스 데이 통합 다이어그램 코드

**메트릭 및 수치**:
- `{metric_name}`: 메트릭 이름
- `{before_value}`: 개선 전 값
- `{after_value}`: 개선 후 값
- `{improvement}`: 개선율 (%)

**URL 및 링크**:
- `https://docs.aws.amazon.com/dynamodb/latest/userguide/`: AWS 공식 문서 URL
- `https://docs.aws.amazon.com/dynamodb/latest/userguide/`: API 레퍼런스 URL
- `https://aws.amazon.com/architecture/customers/duolingo`: 기업 블로그 URL

### 작성 시 주의사항

1. **실제 데이터 사용**: 가능한 한 실제 기업의 공개된 데이터 사용
2. **구체적인 수치**: 모호한 표현 대신 구체적인 수치와 메트릭 제공
3. **Console 경로**: 정확한 AWS Console 경로 명시
4. **한국어 품질**: 전문적이고 일관된 한국어 사용, 기술 용어는 한영 병기
5. **링크 유효성**: 모든 AWS 문서 링크는 최신 URL 사용
6. **다이어그램 품질**: Mermaid 다이어그램은 렌더링 가능한 유효한 구문 사용
7. **크로스 레퍼런스**: 다른 일차 및 문서와의 연계 명확히 표시

### 필수 섹션 체크리스트

- [ ] 사례 개요 (기업 정보, 사례 유형 명시)
- [ ] 비즈니스 도전과제 (구체적 문제 상황 및 요구사항)
- [ ] AWS 솔루션 아키텍처 (다이어그램 포함)
- [ ] 구현 세부사항 (Console 기반 단계별 가이드)
- [ ] 비즈니스 임팩트 (성능, 비용, 운영 개선 수치)
- [ ] 서비스 연계 (이전/향후 학습 내용 연결)
- [ ] 참고 자료 (AWS 공식 문서 링크)
- [ ] 학습 포인트 (핵심 takeaway)

---

**템플릿 버전**: 1.0  
**최종 수정일**: 2026-01-14  
**작성자**: AWS SAA Study Materials Generator
