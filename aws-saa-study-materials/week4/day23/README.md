# Day 23: CloudTrail & AWS 보안 서비스

## 📚 학습 개요
AWS CloudTrail과 주요 보안 서비스들을 학습하여 클라우드 환경에서 포괄적인 보안 모니터링 및 컴플라이언스 체계를 구축하는 방법을 익힙니다.

## 🎯 학습 목표
- AWS CloudTrail의 역할과 중요성 이해
- AWS 보안 서비스 생태계 파악
- 보안 모니터링 및 자동화 구현
- 컴플라이언스 및 거버넌스 전략 수립

## 📖 학습 내용

### 1. 이론 학습 (`theory.md`)
- **AWS CloudTrail 개요**
  - CloudTrail의 핵심 기능
  - 이벤트 유형 (관리, 데이터, 인사이트)
  - 로그 구조 및 분석

- **AWS 보안 서비스 생태계**
  - Identity & Access Management
  - Detection & Response 서비스
  - Data Protection 서비스
  - Infrastructure Protection
  - Compliance & Governance

- **핵심 보안 서비스**
  - AWS GuardDuty (지능형 위협 탐지)
  - AWS Security Hub (중앙 집중식 보안 관리)
  - AWS Config (리소스 구성 모니터링)
  - AWS KMS (키 관리 서비스)
  - AWS WAF & Shield (웹 애플리케이션 보호)

- **보안 자동화 및 대응**
  - 이벤트 기반 자동화
  - 보안 사고 대응 워크플로우
  - 컴플라이언스 자동화

### 2. 실습 (`hands-on/setup-guide.md`)
- **CloudTrail 설정**
  - 트레일 생성 및 구성
  - S3 버킷 및 암호화 설정
  - CloudWatch Logs 통합

- **GuardDuty 구성**
  - 위협 탐지 활성화
  - 샘플 findings 생성
  - 탐지 결과 분석

- **Security Hub 설정**
  - 보안 표준 활성화
  - 서비스 통합 구성
  - 컴플라이언스 모니터링

- **Config 규칙 설정**
  - 보안 규칙 구성
  - 컴플라이언스 검사
  - 자동 수정 설정

- **보안 알림 및 자동화**
  - SNS 알림 설정
  - EventBridge 규칙 생성
  - Lambda 자동 대응 구현

### 3. 퀴즈 (`quiz.md`)
5문제로 구성된 퀴즈를 통해 학습 내용을 점검합니다:
- CloudTrail 기본 개념
- GuardDuty 위협 탐지
- Security Hub 통합
- KMS 암호화 메커니즘
- 보안 자동화 시나리오

## ⏰ 예상 학습 시간
- **이론 학습**: 90분
- **실습**: 120분
- **퀴즈**: 15분
- **총 소요 시간**: 약 3.5시간

## 🔧 실습 준비사항
- AWS 계정 (Free Tier 사용 가능)
- 관리자 권한 또는 적절한 IAM 권한
- 이전 실습에서 생성한 리소스들 (선택사항)

## ⚠️ 비용 주의사항
- **CloudTrail**: 첫 번째 트레일은 무료
- **GuardDuty**: 30일 무료 체험 후 유료
- **Security Hub**: 30일 무료 체험 후 유료
- **Config**: 구성 항목당 요금 부과

## 📋 체크리스트

### 이론 학습 완료
- [ ] CloudTrail의 역할과 기능 이해
- [ ] AWS 보안 서비스 생태계 파악
- [ ] GuardDuty 위협 탐지 메커니즘 이해
- [ ] Security Hub 통합 개념 학습
- [ ] KMS 암호화 방식 이해
- [ ] 보안 자동화 아키텍처 학습

### 실습 완료
- [ ] CloudTrail 설정 및 로그 확인
- [ ] GuardDuty 활성화 및 findings 검토
- [ ] Security Hub 구성 및 대시보드 확인
- [ ] Config 규칙 설정 및 컴플라이언스 검사
- [ ] 보안 알림 시스템 구성
- [ ] 자동화된 보안 대응 구현

### 퀴즈 완료
- [ ] 5문제 퀴즈 응시
- [ ] 80% 이상 점수 달성
- [ ] 오답 노트 작성 및 복습

## 🔗 관련 링크
- [AWS CloudTrail 공식 문서](https://docs.aws.amazon.com/cloudtrail/)
- [Amazon GuardDuty 사용 설명서](https://docs.aws.amazon.com/guardduty/)
- [AWS Security Hub 사용 설명서](https://docs.aws.amazon.com/securityhub/)
- [AWS Config 개발자 안내서](https://docs.aws.amazon.com/config/)
- [AWS KMS 개발자 안내서](https://docs.aws.amazon.com/kms/)

## 📝 학습 노트
이 공간을 활용하여 학습 중 중요한 내용이나 궁금한 점을 기록하세요.

```
학습 날짜: ___________
주요 학습 내용:
- 
- 
- 

어려웠던 개념:
- 
- 

추가 학습이 필요한 부분:
- 
- 
```

## ➡️ 다음 학습
**Day 24: 비용 최적화 및 관리**
- AWS Cost Explorer 활용
- 예산 관리 및 알림 설정
- 비용 최적화 전략
- Reserved Instances 및 Savings Plans