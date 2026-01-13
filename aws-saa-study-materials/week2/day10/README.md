# Day 10: Amazon RDS (Relational Database Service)

## 📚 학습 개요

Amazon RDS(Relational Database Service)는 클라우드에서 관계형 데이터베이스를 쉽게 설정, 운영, 확장할 수 있게 해주는 완전 관리형 서비스입니다. 이번 학습에서는 RDS의 핵심 개념부터 실제 운영까지 필요한 모든 내용을 다룹니다.

## 🎯 학습 목표

이 학습을 완료하면 다음을 할 수 있습니다:

- [ ] Amazon RDS의 핵심 개념과 장점 설명
- [ ] 6가지 RDS 엔진의 특징과 적합한 사용 사례 구분
- [ ] RDS 인스턴스 클래스와 스토리지 유형 선택
- [ ] Multi-AZ 배포와 Read Replica의 차이점과 활용법 이해
- [ ] RDS 백업 및 복원 메커니즘 활용
- [ ] RDS 보안 및 모니터링 기능 구성
- [ ] 실제 RDS 인스턴스 생성 및 관리

## 📖 학습 자료

### 1. 이론 학습
- **파일**: [theory.md](./theory.md)
- **소요 시간**: 45분
- **주요 내용**:
  - RDS 개요 및 장점
  - 지원 데이터베이스 엔진 (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora)
  - 인스턴스 클래스 및 스토리지 유형
  - Multi-AZ 배포 vs Read Replica
  - 백업 및 복원 전략
  - 보안 및 모니터링
  - 비용 최적화 방법

### 2. 실습
- **파일**: [hands-on/setup-guide.md](./hands-on/setup-guide.md)
- **소요 시간**: 90분
- **실습 내용**:
  - RDS MySQL 인스턴스 생성
  - VPC 보안 그룹 구성
  - 데이터베이스 연결 및 기본 작업
  - Multi-AZ 배포 설정
  - Read Replica 생성 및 테스트
  - 모니터링 및 백업 기능 확인

### 3. 퀴즈
- **파일**: [quiz.md](./quiz.md)
- **문제 수**: 5문제
- **소요 시간**: 10분
- **난이도**: 중급

## ⏰ 학습 일정

| 시간 | 활동 | 내용 |
|------|------|------|
| 09:00-09:45 | 이론 학습 | RDS 개념 및 핵심 기능 |
| 09:45-10:00 | 휴식 | |
| 10:00-11:30 | 실습 | RDS 인스턴스 생성 및 관리 |
| 11:30-11:40 | 퀴즈 | 학습 내용 확인 |
| 11:40-12:00 | 복습 | 핵심 개념 정리 |

## 🔧 사전 준비사항

### 필수 준비사항
- [ ] AWS 계정 (Free Tier 권장)
- [ ] MySQL 클라이언트 (MySQL Workbench 또는 CLI)
- [ ] 기본적인 SQL 지식
- [ ] 이전 실습의 VPC 및 서브넷 (또는 기본 VPC 사용)

### 권장 사항
- [ ] 데이터베이스 기본 개념 이해
- [ ] AWS CLI 설치 (선택사항)
- [ ] 네트워킹 기본 지식

## 🎯 핵심 개념

### 1. RDS vs 전통적인 데이터베이스
```
전통적인 DB          →    Amazon RDS
수동 설치/설정       →    자동 프로비저닝
수동 백업           →    자동 백업
수동 패치           →    자동 패치 관리
복잡한 HA 구성      →    Multi-AZ 간단 설정
하드웨어 관리       →    완전 관리형
```

### 2. RDS 엔진 선택 가이드
- **MySQL**: 웹 애플리케이션, 오픈소스
- **PostgreSQL**: 복잡한 쿼리, JSON 지원
- **MariaDB**: MySQL 호환, 향상된 성능
- **Oracle**: 엔터프라이즈, 복잡한 비즈니스 로직
- **SQL Server**: Microsoft 생태계
- **Aurora**: AWS 네이티브, 고성능

### 3. Multi-AZ vs Read Replica
| 구분 | Multi-AZ | Read Replica |
|------|----------|--------------|
| 목적 | 고가용성 | 읽기 성능 향상 |
| 복제 | 동기 | 비동기 |
| 사용 | 자동 장애조치 | 읽기 전용 쿼리 |
| 위치 | 같은 리전 | 같은/다른 리전 |

## 🚨 주의사항

### 비용 관련
- RDS 인스턴스는 시간당 과금
- Multi-AZ는 인스턴스 비용 2배
- 스토리지 및 백업 별도 과금
- 실습 후 반드시 리소스 정리

### 보안 관련
- 강력한 마스터 패스워드 설정
- 보안 그룹으로 접근 제한
- 가능하면 Private Subnet 사용
- SSL/TLS 연결 활용

### 성능 관련
- 적절한 인스턴스 클래스 선택
- 워크로드에 맞는 스토리지 유형 선택
- CloudWatch 메트릭 모니터링
- Performance Insights 활용

## 📝 실습 체크리스트

### 기본 설정
- [ ] RDS 서브넷 그룹 생성
- [ ] 보안 그룹 구성
- [ ] RDS MySQL 인스턴스 생성
- [ ] 데이터베이스 연결 확인

### 고급 기능
- [ ] Multi-AZ 배포 활성화
- [ ] Read Replica 생성
- [ ] 백업 및 스냅샷 테스트
- [ ] 모니터링 메트릭 확인

### 정리 작업
- [ ] Read Replica 삭제
- [ ] RDS 인스턴스 삭제
- [ ] 스냅샷 삭제
- [ ] 보안 그룹 정리

## 🔗 관련 AWS 서비스

- **Amazon Aurora**: RDS의 고성능 버전
- **Amazon DynamoDB**: NoSQL 데이터베이스
- **AWS Database Migration Service**: 데이터베이스 마이그레이션
- **Amazon ElastiCache**: 인메모리 캐싱
- **AWS Secrets Manager**: 데이터베이스 자격 증명 관리

## 📚 추가 학습 자료

### AWS 공식 문서
- [Amazon RDS User Guide](https://docs.aws.amazon.com/rds/)
- [RDS Best Practices](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)
- [RDS Security](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.html)

### 실습 확장
- Cross-Region Read Replica 생성
- RDS Proxy 설정
- Aurora 마이그레이션
- 자동화된 백업 정책

## ❓ 자주 묻는 질문

**Q: RDS와 EC2에 직접 설치한 데이터베이스의 차이는?**
A: RDS는 완전 관리형으로 백업, 패치, 모니터링이 자동화되지만, EC2는 모든 것을 직접 관리해야 합니다.

**Q: Multi-AZ와 Read Replica를 동시에 사용할 수 있나요?**
A: 네, 가능합니다. Multi-AZ로 고가용성을 확보하고 Read Replica로 읽기 성능을 향상시킬 수 있습니다.

**Q: RDS 인스턴스 크기를 나중에 변경할 수 있나요?**
A: 네, 언제든지 인스턴스 클래스를 변경할 수 있습니다. 다운타임이 발생할 수 있으므로 유지보수 시간에 수행하는 것이 좋습니다.

---

## 다음 학습

**Day 11**: [DynamoDB 및 NoSQL 데이터베이스](../day11/README.md)

---

**학습 완료 후 체크**: ✅ 이론 학습 ✅ 실습 완료 ✅ 퀴즈 통과 ✅ 리소스 정리