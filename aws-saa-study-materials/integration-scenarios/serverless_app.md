# 서버리스 애플리케이션 아키텍처

> **통합 시나리오**: serverless_app
> **사용 사례**: 이벤트 기반 마이크로서비스

---

## 📋 시나리오 개요

- **시나리오 ID**: `serverless_app`
- **시나리오명**: 서버리스 애플리케이션 아키텍처
- **설명**: Lambda, API Gateway, DynamoDB 통합
- **관련 일차**: Day 18, Day 19, Day 11
- **주요 일차**: Day 18
- **핵심 서비스**: Lambda, API Gateway, DynamoDB
- **통합 패턴**: Serverless + API + NoSQL
- **사용 사례**: 이벤트 기반 마이크로서비스

---

## 📅 관련 일차

### Day 18: Lambda (서버리스 컴퓨팅) **(주요)**

**주요 서비스**: Lambda, Lambda Layers, Lambda@Edge, Event Sources

**역할**: 이 시나리오의 핵심 서비스를 제공합니다.

**학습 링크**: [Day 18 학습 자료](../week3/day18/README.md)

### Day 19: API Gateway

**주요 서비스**: API Gateway, REST API, WebSocket API, API Keys

**역할**: 통합 아키텍처의 지원 서비스를 제공합니다.

**학습 링크**: [Day 19 학습 자료](../week3/day19/README.md)

### Day 11: DynamoDB

**주요 서비스**: DynamoDB, DAX, Global Tables, Streams

**역할**: 통합 아키텍처의 지원 서비스를 제공합니다.

**학습 링크**: [Day 11 학습 자료](../week2/day11/README.md)


---

## 🏗️ 서비스 아키텍처

```mermaid
graph TB
    subgraph "사용자 계층"
        Users[전 세계 사용자]
    end

    subgraph "Day 18: Lambda (서버리스 컴퓨팅)"
        D18S0[Lambda]
        D18S1[Lambda Layers]
    end

    subgraph "Day 19: API Gateway"
        D19S0[API Gateway]
        D19S1[REST API]
    end

    subgraph "Day 11: DynamoDB"
        D11S0[DynamoDB]
        D11S1[DAX]
    end

    Users --> D18S0
    D18S0 --> D19S0
    D19S0 --> D11S0
```

---

## 🔄 서비스 플로우

### End-to-End 요청 처리 흐름

1. **API 요청**
   - 서비스: API Gateway (Day 19)
   - 처리: RESTful API 엔드포인트 호출
   - 다음 단계: Lambda 실행

2. **비즈니스 로직**
   - 서비스: Lambda (Day 18)
   - 처리: 서버리스 함수 실행
   - 다음 단계: 데이터베이스 조회

3. **데이터 저장/조회**
   - 서비스: DynamoDB (Day 11)
   - 처리: NoSQL 데이터베이스 작업
   - 다음 단계: 응답 반환

### 시퀀스 다이어그램

```mermaid
sequenceDiagram
    participant User as 사용자
    participant S18 as Lambda
    participant S19 as API Gateway
    participant S11 as DynamoDB

    User->>S18: 요청 전송
    S18->>S19: 데이터 전달
    S19->>S11: 데이터 전달
    S11-->>User: 응답 반환
```

---

## 💻 구현 가이드

### 단계별 구현 방법

#### 단계 1: Day 18 - Lambda (서버리스 컴퓨팅) 구성

**주요 서비스**: Lambda, Lambda Layers, Lambda@Edge, Event Sources

**구현 방법**:
1. AWS Console에서 Lambda 생성
2. 기본 설정 구성 (Region: ap-northeast-2)
3. 보안 및 접근 제어 설정
4. 모니터링 및 알람 구성

**검증**:
- 리소스 상태 확인
- 연결 테스트 수행

**상세 가이드**: [Day 18 실습 자료](../week3/day18/hands-on-console/README.md)

#### 단계 2: Day 19 - API Gateway 구성

**주요 서비스**: API Gateway, REST API, WebSocket API, API Keys

**구현 방법**:
1. AWS Console에서 API Gateway 생성
2. 기본 설정 구성 (Region: ap-northeast-2)
3. 보안 및 접근 제어 설정
4. 모니터링 및 알람 구성

**검증**:
- 리소스 상태 확인
- 연결 테스트 수행

**상세 가이드**: [Day 19 실습 자료](../week3/day19/hands-on-console/README.md)

#### 단계 3: Day 11 - DynamoDB 구성

**주요 서비스**: DynamoDB, DAX, Global Tables, Streams

**구현 방법**:
1. AWS Console에서 DynamoDB 생성
2. 기본 설정 구성 (Region: ap-northeast-2)
3. 보안 및 접근 제어 설정
4. 모니터링 및 알람 구성

**검증**:
- 리소스 상태 확인
- 연결 테스트 수행

**상세 가이드**: [Day 11 실습 자료](../week2/day11/hands-on-console/README.md)

### 통합 검증

**End-to-End 테스트**:
1. 사용자 시나리오 기반 테스트 수행
2. 각 서비스 간 연결 확인
3. 성능 및 응답 시간 측정
4. 에러 처리 및 장애 조치 테스트


---

## 🎓 학습 경로

### 권장 학습 순서

1. **Day 11: DynamoDB**
   - 학습 내용: DynamoDB, DAX, Global Tables, Streams
   - 예상 시간: 2-3시간
   - 학습 자료: [Day 11 README](../week2/day11/README.md)

2. **Day 18: Lambda (서버리스 컴퓨팅) **(핵심)****
   - 학습 내용: Lambda, Lambda Layers, Lambda@Edge, Event Sources
   - 예상 시간: 2-3시간
   - 학습 자료: [Day 18 README](../week3/day18/README.md)

3. **Day 19: API Gateway**
   - 학습 내용: API Gateway, REST API, WebSocket API, API Keys
   - 예상 시간: 2-3시간
   - 학습 자료: [Day 19 README](../week3/day19/README.md)

### 실습 순서

1. **개별 서비스 실습**: 각 일차의 hands-on-console 실습 완료
2. **서비스 통합 실습**: 서비스 간 연결 및 통합 구성
3. **End-to-End 테스트**: 전체 시나리오 검증
4. **최적화 및 튜닝**: 성능 및 비용 최적화

### 학습 목표

이 통합 시나리오를 완료하면 다음을 이해하게 됩니다:

- 이벤트 기반 마이크로서비스를 위한 AWS 아키텍처 설계
- Serverless + API + NoSQL 통합 패턴 구현
- 여러 AWS 서비스를 조합한 실제 솔루션 구축
- 프로덕션 환경 운영 및 모니터링


---

## ✅ 베스트 프랙티스

### 아키텍처 설계

- **고가용성**: 멀티 AZ 배포로 장애 대응
- **확장성**: Auto Scaling 및 로드 밸런싱 활용
- **보안**: 최소 권한 원칙 및 네트워크 격리
- **모니터링**: CloudWatch를 통한 포괄적 모니터링

### 비용 최적화

- 예약 인스턴스 및 Savings Plans 활용
- 자동 스케일링으로 리소스 최적화
- S3 Lifecycle 정책으로 스토리지 비용 절감
- CloudWatch 알람으로 비정상 비용 감지

### 운영 효율성

- Infrastructure as Code (CloudFormation/Terraform) 사용
- CI/CD 파이프라인 구축
- 자동화된 백업 및 복구 절차
- 정기적인 보안 감사 및 패치


---

## 🔧 트러블슈팅

### 일반적인 문제

#### 문제 1: 서비스 간 연결 실패

**증상**: 한 서비스에서 다른 서비스로 요청이 전달되지 않음

**진단**:
1. Security Group 규칙 확인
2. IAM 권한 검증
3. 네트워크 ACL 설정 확인

**해결**:
- 필요한 포트 및 프로토콜 허용
- 적절한 IAM 역할 및 정책 부여
- VPC 피어링 또는 엔드포인트 구성

#### 문제 2: 성능 저하

**증상**: 응답 시간 증가, 처리량 감소

**진단**:
1. CloudWatch 메트릭 확인 (CPU, 메모리, 네트워크)
2. 병목 지점 식별
3. 로그 분석

**해결**:
- 리소스 스케일 업/아웃
- 캐싱 전략 적용
- 데이터베이스 쿼리 최적화

#### 문제 3: 비용 급증

**증상**: 예상보다 높은 AWS 비용

**진단**:
1. Cost Explorer에서 비용 분석
2. 리소스 사용률 확인
3. 불필요한 리소스 식별

**해결**:
- 미사용 리소스 삭제
- 예약 인스턴스 구매
- Auto Scaling 정책 최적화


---

## 📚 참고 자료

### AWS 공식 문서

- [Lambda 사용 설명서](https://docs.aws.amazon.com/)
- [API Gateway 사용 설명서](https://docs.aws.amazon.com/)
- [DynamoDB 사용 설명서](https://docs.aws.amazon.com/)

### 아키텍처 패턴

- [AWS 아키텍처 센터 - Serverless + API + NoSQL](https://aws.amazon.com/architecture/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS 솔루션 라이브러리](https://aws.amazon.com/solutions/)

### 관련 학습 자료

- [Day 18: Lambda (서버리스 컴퓨팅)](../week3/day18/README.md)
- [Day 19: API Gateway](../week3/day19/README.md)
- [Day 11: DynamoDB](../week2/day11/README.md)


---

**생성일**: 2026-01-14
**버전**: 1.0
