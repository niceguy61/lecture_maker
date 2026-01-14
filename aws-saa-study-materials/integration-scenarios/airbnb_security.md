# Airbnb IAM 보안 아키텍처

> **통합 시나리오**: airbnb_security
> **사용 사례**: 엔터프라이즈 보안 관리

---

## 📋 시나리오 개요

- **시나리오 ID**: `airbnb_security`
- **시나리오명**: Airbnb IAM 보안 아키텍처
- **설명**: 대규모 조직의 보안 및 규정 준수
- **관련 일차**: Day 2, Day 5, Day 23
- **주요 일차**: Day 2
- **핵심 서비스**: IAM, VPC, CloudTrail
- **통합 패턴**: Identity + Network + Audit
- **사용 사례**: 엔터프라이즈 보안 관리

---

## 📅 관련 일차

### Day 2: IAM (Identity and Access Management) **(주요)**

**주요 서비스**: IAM Users, Groups, Roles, Policies, MFA

**역할**: 이 시나리오의 핵심 서비스를 제공합니다.

**학습 링크**: [Day 2 학습 자료](../week1/day2/README.md)

### Day 5: VPC (Virtual Private Cloud) 기초

**주요 서비스**: VPC, Subnets, Route Tables, Internet Gateway

**역할**: 통합 아키텍처의 지원 서비스를 제공합니다.

**학습 링크**: [Day 5 학습 자료](../week1/day5/README.md)

### Day 23: CloudTrail 및 보안 서비스

**주요 서비스**: CloudTrail, GuardDuty, Inspector, Macie

**역할**: 통합 아키텍처의 지원 서비스를 제공합니다.

**학습 링크**: [Day 23 학습 자료](../week4/day23/README.md)


---

## 🏗️ 서비스 아키텍처

```mermaid
graph TB
    subgraph "사용자 계층"
        Users[전 세계 사용자]
    end

    subgraph "Day 2: IAM (Identity and Access Management)"
        D2S0[IAM Users]
        D2S1[Groups]
    end

    subgraph "Day 5: VPC (Virtual Private Cloud) 기초"
        D5S0[VPC]
        D5S1[Subnets]
    end

    subgraph "Day 23: CloudTrail 및 보안 서비스"
        D23S0[CloudTrail]
        D23S1[GuardDuty]
    end

    Users --> D2S0
    D2S0 --> D5S0
    D5S0 --> D23S0
```

---

## 🔄 서비스 플로우

### End-to-End 요청 처리 흐름

1. **사용자 인증**
   - 서비스: IAM (Day 2)
   - 처리: 사용자 자격 증명 및 권한 확인
   - 다음 단계: 네트워크 접근 제어

2. **네트워크 격리**
   - 서비스: VPC (Day 5)
   - 처리: 프라이빗 서브넷에서 안전한 통신
   - 다음 단계: 감사 로깅

3. **활동 감사**
   - 서비스: CloudTrail (Day 23)
   - 처리: 모든 API 호출 및 활동 기록
   - 다음 단계: 완료

### 시퀀스 다이어그램

```mermaid
sequenceDiagram
    participant User as 사용자
    participant S2 as IAM Users
    participant S5 as VPC
    participant S23 as CloudTrail

    User->>S2: 요청 전송
    S2->>S5: 데이터 전달
    S5->>S23: 데이터 전달
    S23-->>User: 응답 반환
```

---

## 💻 구현 가이드

### 단계별 구현 방법

#### 단계 1: Day 2 - IAM (Identity and Access Management) 구성

**주요 서비스**: IAM Users, Groups, Roles, Policies, MFA

**구현 방법**:
1. AWS Console에서 IAM Users 생성
2. 기본 설정 구성 (Region: ap-northeast-2)
3. 보안 및 접근 제어 설정
4. 모니터링 및 알람 구성

**검증**:
- 리소스 상태 확인
- 연결 테스트 수행

**상세 가이드**: [Day 2 실습 자료](../week1/day2/hands-on-console/README.md)

#### 단계 2: Day 5 - VPC (Virtual Private Cloud) 기초 구성

**주요 서비스**: VPC, Subnets, Route Tables, Internet Gateway

**구현 방법**:
1. AWS Console에서 VPC 생성
2. 기본 설정 구성 (Region: ap-northeast-2)
3. 보안 및 접근 제어 설정
4. 모니터링 및 알람 구성

**검증**:
- 리소스 상태 확인
- 연결 테스트 수행

**상세 가이드**: [Day 5 실습 자료](../week1/day5/hands-on-console/README.md)

#### 단계 3: Day 23 - CloudTrail 및 보안 서비스 구성

**주요 서비스**: CloudTrail, GuardDuty, Inspector, Macie

**구현 방법**:
1. AWS Console에서 CloudTrail 생성
2. 기본 설정 구성 (Region: ap-northeast-2)
3. 보안 및 접근 제어 설정
4. 모니터링 및 알람 구성

**검증**:
- 리소스 상태 확인
- 연결 테스트 수행

**상세 가이드**: [Day 23 실습 자료](../week4/day23/hands-on-console/README.md)

### 통합 검증

**End-to-End 테스트**:
1. 사용자 시나리오 기반 테스트 수행
2. 각 서비스 간 연결 확인
3. 성능 및 응답 시간 측정
4. 에러 처리 및 장애 조치 테스트


---

## 🎓 학습 경로

### 권장 학습 순서

1. **Day 2: IAM (Identity and Access Management) **(핵심)****
   - 학습 내용: IAM Users, Groups, Roles, Policies, MFA
   - 예상 시간: 2-3시간
   - 학습 자료: [Day 2 README](../week1/day2/README.md)

2. **Day 5: VPC (Virtual Private Cloud) 기초**
   - 학습 내용: VPC, Subnets, Route Tables, Internet Gateway
   - 예상 시간: 2-3시간
   - 학습 자료: [Day 5 README](../week1/day5/README.md)

3. **Day 23: CloudTrail 및 보안 서비스**
   - 학습 내용: CloudTrail, GuardDuty, Inspector, Macie
   - 예상 시간: 2-3시간
   - 학습 자료: [Day 23 README](../week4/day23/README.md)

### 실습 순서

1. **개별 서비스 실습**: 각 일차의 hands-on-console 실습 완료
2. **서비스 통합 실습**: 서비스 간 연결 및 통합 구성
3. **End-to-End 테스트**: 전체 시나리오 검증
4. **최적화 및 튜닝**: 성능 및 비용 최적화

### 학습 목표

이 통합 시나리오를 완료하면 다음을 이해하게 됩니다:

- 엔터프라이즈 보안 관리를 위한 AWS 아키텍처 설계
- Identity + Network + Audit 통합 패턴 구현
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

- [IAM Users 사용 설명서](https://docs.aws.amazon.com/)
- [VPC 사용 설명서](https://docs.aws.amazon.com/)
- [CloudTrail 사용 설명서](https://docs.aws.amazon.com/)

### 아키텍처 패턴

- [AWS 아키텍처 센터 - Identity + Network + Audit](https://aws.amazon.com/architecture/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS 솔루션 라이브러리](https://aws.amazon.com/solutions/)

### 관련 학습 자료

- [Day 2: IAM (Identity and Access Management)](../week1/day2/README.md)
- [Day 5: VPC (Virtual Private Cloud) 기초](../week1/day5/README.md)
- [Day 23: CloudTrail 및 보안 서비스](../week4/day23/README.md)


---

**생성일**: 2026-01-14
**버전**: 1.0
