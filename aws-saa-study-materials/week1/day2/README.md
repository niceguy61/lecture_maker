# Day 2: AWS IAM (Identity and Access Management)

## 📚 학습 개요

AWS Identity and Access Management(IAM)는 AWS 서비스와 리소스에 대한 액세스를 안전하게 제어할 수 있는 웹 서비스입니다. 오늘은 IAM의 핵심 구성 요소와 보안 모범 사례를 학습합니다.

## 🎯 학습 목표

이 단원을 완료하면 다음을 할 수 있습니다:

- [ ] AWS IAM의 핵심 개념과 구성 요소 설명
- [ ] IAM 사용자, 그룹, 역할, 정책의 차이점과 사용법 이해
- [ ] IAM 정책의 구조와 작성 방법 학습
- [ ] IAM 보안 모범 사례 적용
- [ ] Python을 사용한 IAM 리소스 관리 실습

## 📖 학습 자료

### 1. 이론 학습
- **파일**: [theory.md](theory.md)
- **내용**: IAM 기본 개념, 구성 요소, 정책 구조, 보안 모범 사례
- **예상 시간**: 45분

### 2. 시각화 자료
- **파일**: [visuals/iam-architecture.md](visuals/iam-architecture.md)
- **내용**: IAM 아키텍처 다이어그램, 구성 요소 관계도, 정책 평가 흐름
- **예상 시간**: 20분

### 3. 실습
- **파일**: [hands-on/iam-management.py](hands-on/iam-management.py)
- **설정 가이드**: [hands-on/setup-guide.md](hands-on/setup-guide.md)
- **내용**: Python을 사용한 IAM 사용자, 그룹, 역할, 정책 생성 및 관리
- **예상 시간**: 60분

### 4. 퀴즈
- **파일**: [quiz.md](quiz.md)
- **내용**: IAM 핵심 개념 확인 (5문제)
- **예상 시간**: 15분

## 🗓️ 학습 일정 (권장)

| 시간 | 활동 | 내용 |
|------|------|------|
| 09:00-09:45 | 이론 학습 | IAM 기본 개념 및 구성 요소 |
| 09:45-10:05 | 시각화 자료 | 아키텍처 다이어그램 검토 |
| 10:05-10:15 | 휴식 | ☕ |
| 10:15-11:15 | 실습 | Python IAM 관리 스크립트 |
| 11:15-11:30 | 퀴즈 | 학습 내용 확인 |
| 11:30-11:45 | 복습 | 핵심 개념 정리 |

## 🔑 핵심 개념

### IAM 구성 요소
1. **사용자(Users)**: 실제 사람이나 애플리케이션
2. **그룹(Groups)**: 사용자들의 집합
3. **역할(Roles)**: 임시 권한을 부여받는 개체
4. **정책(Policies)**: 권한을 정의하는 JSON 문서

### 보안 모범 사례
- 최소 권한 원칙 적용
- 루트 계정 사용 금지
- MFA(다중 인증) 활성화
- 정기적인 권한 검토
- 그룹을 통한 권한 관리

## 🛠️ 실습 준비사항

### 필수 요구사항
- AWS 계정 (Free Tier 사용 가능)
- Python 3.7 이상
- AWS CLI 설치 및 설정
- 적절한 IAM 권한

### 설치할 패키지
```bash
pip install boto3 jsonschema python-dotenv
```

## 📋 체크리스트

### 학습 완료 확인
- [ ] IAM 이론 내용 학습 완료
- [ ] 시각화 자료 검토 완료
- [ ] 실습 환경 설정 완료
- [ ] Python 실습 스크립트 실행 완료
- [ ] 퀴즈 80점 이상 달성
- [ ] 핵심 개념 정리 완료

### 실습 완료 확인
- [ ] IAM 사용자 생성 및 관리
- [ ] IAM 그룹 생성 및 정책 연결
- [ ] IAM 역할 생성 및 신뢰 정책 설정
- [ ] 정책 생성 및 권한 테스트
- [ ] 실습 리소스 정리 완료

## 🔗 연관 학습

### 이전 학습 (Day 1)
- AWS 글로벌 인프라
- AWS 계정 및 기본 설정

### 다음 학습 (Day 3)
- EC2 (Elastic Compute Cloud)
- IAM 역할과 EC2의 연동

## 📚 추가 학습 자료

### AWS 공식 문서
- [IAM 사용 설명서](https://docs.aws.amazon.com/iam/)
- [IAM 모범 사례](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [IAM 정책 참조](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html)

### 실습 도구
- [IAM 정책 시뮬레이터](https://policysim.aws.amazon.com/)
- [IAM 정책 생성기](https://awspolicygen.s3.amazonaws.com/policygen.html)

## ❓ 문제 해결

### 자주 발생하는 문제
1. **자격 증명 오류**: AWS CLI 설정 확인
2. **권한 부족**: IAM 권한 검토
3. **리소스 중복**: 기존 리소스 확인 및 정리

### 도움이 필요한 경우
- AWS 공식 문서 참조
- AWS 커뮤니티 포럼 활용
- 실습 가이드의 문제 해결 섹션 확인

## 🎉 학습 완료 후

Day 2 학습을 완료했다면:
1. 핵심 개념을 자신의 언어로 정리해보세요
2. 실제 AWS 콘솔에서 IAM 리소스를 확인해보세요
3. 내일 EC2 학습을 위해 IAM 역할의 개념을 복습하세요

**다음 단계**: [Day 3 - EC2 기초](../day3/README.md)로 이동하여 IAM 역할이 EC2에서 어떻게 활용되는지 학습해보세요!