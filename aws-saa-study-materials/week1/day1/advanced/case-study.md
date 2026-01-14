# Netflix - 글로벌 스트리밍을 위한 멀티 리전 아키텍처

> **Day 1: AWS 개요 및 글로벌 인프라**  
> **주요 AWS 서비스**: CloudFront, Regions, Availability Zones, Edge Locations

---

## 📋 사례 개요

- **기업명**: Netflix
- **업종**: 미디어 & 엔터테인먼트
- **규모**: Enterprise <!-- Startup/Medium/Enterprise -->
- **주요 AWS 서비스**: CloudFront, Regions, Availability Zones, Edge Locations
- **사례 출처**: https://aws.amazon.com/architecture/customers/netflix <!-- 공개 자료 링크 또는 "AWS Well-Architected Framework 기반" -->
- **사례 유형**: 실제 기업 사례 <!-- "실제 기업 사례" 또는 "Best Practice 기반 가상 사례" -->

---

## 🎯 비즈니스 도전과제

### 문제 상황

글로벌 스트리밍을 위한 멀티 리전 아키텍처를 위한 확장 가능하고 안정적인 인프라 구축

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
    
    subgraph "AWS 인프라 - Day 1"
        A[CloudFront]
        B1[Regions]
        B2[Availability Zones]
    end

    Users --> A
    A --> B1
    A --> B2

```

> 📁 **상세 다이어그램**: [architecture-diagrams/main-architecture.mmd](./architecture-diagrams/main-architecture.mmd)

### 핵심 서비스 구성

#### CloudFront (Day 1 주요 서비스)

**선택 이유**:
- 높은 가용성 및 확장성 제공
- 관리형 서비스로 운영 부담 감소

**구성 방법** (AWS Console 기준):
1. **Console 경로**: Services > Networking & Content Delivery > CloudFront
2. **주요 설정**:
   - Origin Domain: netflix-content.s3.amazonaws.com
   - Viewer Protocol Policy: Redirect HTTP to HTTPS
   - Price Class: Use All Edge Locations

**다른 서비스와의 연계**:
- **SNS** (Day 16): Day 16의 SNS (Simple Notification Service) 및 CloudFront와 연계
- **Route 53** (Day 17): Day 17의 Route 53와 연계

#### Regions

**역할**: 지리적으로 분리된 AWS 데이터센터 위치 - 지연시간 최소화, 규정 준수, 재해 복구를 위한 리전 선택

**구성 방법**:
- 비즈니스 요구사항(지연시간, 규정 준수, 비용)에 따라 최적의 리전 선택

**연계 방식**: Direct Integration

### 서비스 간 데이터 플로우

```mermaid
sequenceDiagram
    participant User as 사용자
    participant Service as CloudFront
    participant Storage as 데이터 저장소
    
    User->>Service: 요청 전송
    Service->>Storage: 데이터 조회/저장
    Storage-->>Service: 응답
    Service-->>User: 결과 반환

```

**플로우 설명**:
1. **사용자 요청** → CloudFront
   - 사용자 요청을 받아 처리 시작
   
2. **CloudFront** → **Regions** (Day 1의 주요 서비스)
   - 비즈니스 로직 처리 및 데이터 변환
   
3. **Regions** → **Data Storage**
   - 데이터 저장 및 영속화

4. **응답 반환** → 사용자
   - 처리 결과를 사용자에게 반환

---

## 💻 구현 세부사항

### AWS Console 기반 설정

#### 1단계: CloudFront 생성

**Console 경로**: Services > Networking & Content Delivery > CloudFront > Create Distribution

**기본 설정**:
- **Name/ID**: `netflix-cdn-distribution`
- **Region**: `Global (CloudFront는 글로벌 서비스)` (예: ap-northeast-2 - 서울)
- **Origin Domain**: netflix-content.s3.amazonaws.com
- **Viewer Protocol Policy**: Redirect HTTP to HTTPS

**고급 설정**:
- **Cache Behavior**: CachingOptimized
  - 설명: 최적화된 캐싱 정책 적용
- **Compress Objects**: Yes (Gzip 압축)
  - 설명: 자동 압축으로 전송 속도 향상

**생성 확인**:
- 상태가 "Available" 또는 "Active"로 변경될 때까지 대기 (약 15-20분)
- Console에서 리소스 상세 정보 확인

#### 2단계: CloudWatch 연계 구성

**Console 경로**: Services > Networking & Content Delivery > CloudFront

**연결 설정**:
1. CloudFront에서 생성한 리소스 선택
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
# netflix-cdn-distribution-stack.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Netflix - 글로벌 스트리밍을 위한 멀티 리전 아키텍처 - CloudFront 구성'

Resources:
  NetflixCDNDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      Origins: [{DomainName: netflix-content.s3.amazonaws.com}]
      Enabled: true
      Tags:
        - Key: Project
          Value: day1-project
        - Key: Environment
          Value: production
```

#### Terraform 예시 (선택사항)

```hcl
# main.tf
resource "aws_cloudfront" "netflix-cdn-distribution" {
  name = "day1-resource"
  type = "standard"
  
  tags = {
    Project     = "day1-project"
    Environment = "production"
  }
}
```

### 모니터링 설정

#### CloudWatch 메트릭 구성

**Console 경로**: CloudWatch > Metrics > AWS/CloudFront

**핵심 메트릭**:
- **응답 시간**: CloudFront 요청 수 측정
  - 정상 범위: > 1000 requests/min
  - 경고 임계값: < 100 requests/min
  
- **처리량**: 4xx 에러율 모니터링
  - 정상 범위: < 5%
  - 경고 임계값: > 10%

#### 알람 설정

**Console 경로**: CloudWatch > Alarms > Create alarm

**알람 구성**:
```yaml
알람명: day1-cloudfront-error-alarm
메트릭: 4xxErrorRate
조건: >= (예: >= 80%)
기간: 5분 (예: 5분)
평가 기간: 2회 연속 (예: 2회 연속)
알림: arn:aws:sns:ap-northeast-2:123456789012:alerts
```

#### 대시보드 구성

**Console 경로**: CloudWatch > Dashboards > Create dashboard

**위젯 구성**:
- 요청 수 그래프: 시계열 라인 차트
- 에러율 그래프: 시계열 라인 차트
- 데이터 전송량 그래프: 시계열 라인 차트

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

#### Day 16: SNS
**연계 방식**: Day 16의 SNS (Simple Notification Service) 및 CloudFront와 연계

**이 사례에서의 활용**:
- 멀티 리전 배포 기반
- 글로벌 사용자 대응

**학습 포인트**:
- 리전 선택의 중요성

#### Day 17: Route 53
**연계 방식**: Day 17의 Route 53와 연계

**이 사례에서의 활용**:
- 역할 기반 접근 제어

### 향후 학습 내용 예고

#### Day 6: 고급 서비스
**확장 방향**: 추가 기능 통합

**이 사례의 진화**:
- 성능 최적화
- 비용 효율성 향상

**기대 효과**:
- 운영 효율성 증대

#### Day 8: 모니터링 서비스
**확장 방향**: 고급 모니터링 통합

**추가 통합 시나리오**:
- 실시간 알람 및 대시보드

### 전체 아키텍처에서의 역할

```mermaid
graph LR
    D1[Day 1: AWS 개요 및 글로벌 인프라]
    D16[Day 16 SNS 및 CloudFront]
    D17[Day 17 Route 53]

    D1 -.확장.-> D16
    D1 -.확장.-> D17

```

**통합 시나리오 설명**:
- Day 1의 서비스들이 전체 아키텍처에서 핵심 역할 수행

**서비스 의존성**:
- Day 1 (CloudFront) → Day 16 (SNS)
- Day 16 (SNS) → Day 17 (Route 53)

---

## 📚 참고 자료

### AWS 공식 문서
- [CloudFront 사용 설명서](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
- [CloudFront API 레퍼런스](https://docs.aws.amazon.com/cloudfront/latest/APIReference/Welcome.html)
- [AWS Well-Architected Framework - Operational Excellence](https://docs.aws.amazon.com/wellarchitected/latest/framework/)

### 아키텍처 및 베스트 프랙티스
- [AWS 아키텍처 센터 - 글로벌 스트리밍을 위한 멀티 리전 아키텍처](https://aws.amazon.com/architecture/)
- [보안 베스트 프랙티스 - IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

### 비용 최적화
- [AWS 요금 계산기](https://calculator.aws/)
- [CloudFront 요금 안내](https://aws.amazon.com/pricing)
- [비용 최적화 가이드](https://docs.aws.amazon.com/cost-management/)

### 기업 사례 및 발표 자료
- [Netflix 공식 블로그 포스트](https://aws.amazon.com/ko/blogs/korea/adventures-in-scaling-in-changing-times/)
- [AWS re:Invent 발표: Netflix - 글로벌 스트리밍을 위한 멀티 리전 아키텍처](https://reinvent.awsevents.com/)
- [AWS 고객 사례 연구](https://aws.amazon.com/ko/blogs/korea/2024-customer-cases/)

### 화이트페이퍼
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/whitepapers/)

---

## 🎓 학습 포인트

### 1. CloudFront의 실제 활용 방법
- CloudFront의 핵심 기능 이해
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
- Day 16: SNS
- Day 17: Route 53
- Day 4: 심화 주제