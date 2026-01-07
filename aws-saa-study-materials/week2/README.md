# Week 2: 스토리지 및 데이터베이스

## 📚 주차 개요

AWS의 다양한 스토리지 서비스와 데이터베이스 솔루션을 학습하는 두 번째 주입니다.
S3부터 시작해서 블록 스토리지, 파일 시스템, 그리고 관계형/NoSQL 데이터베이스까지 데이터 관리의 모든 측면을 다룹니다.

## 🎯 주차 학습 목표

- AWS 스토리지 서비스별 특징과 사용 사례 이해
- 데이터베이스 서비스 선택 기준 및 설계 원칙 습득
- 데이터 백업, 마이그레이션, 재해 복구 전략 수립
- 비용 효율적인 데이터 관리 방안 학습

## 📅 일별 학습 계획

### [Day 8: S3 (Simple Storage Service)](./day8/README.md)
**학습 시간**: 3-4시간  
**핵심 주제**:
- S3 버킷 및 객체 관리
- 스토리지 클래스 및 생명주기 정책
- 버전 관리 및 MFA Delete
- S3 보안 및 액세스 제어

**실습**: S3 버킷 생성 및 정적 웹사이트 호스팅

### [Day 9: EBS, EFS, FSx](./day9/README.md)
**학습 시간**: 3시간  
**핵심 주제**:
- EBS 볼륨 유형 및 성능 특성
- EFS (Elastic File System) 구성
- FSx for Windows/Lustre
- 스토리지 성능 최적화

**실습**: EFS 마운트 및 다중 인스턴스 공유

### [Day 10: RDS (Relational Database Service)](./day10/README.md)
**학습 시간**: 3-4시간  
**핵심 주제**:
- RDS 엔진별 특징 (MySQL, PostgreSQL, Oracle 등)
- Multi-AZ 및 Read Replica
- 백업 및 복원 전략
- 성능 모니터링 및 튜닝

**실습**: RDS 인스턴스 생성 및 연결

### [Day 11: DynamoDB 및 NoSQL](./day11/README.md)
**학습 시간**: 3시간  
**핵심 주제**:
- DynamoDB 테이블 설계 원칙
- 파티션 키 및 정렬 키
- GSI/LSI (Global/Local Secondary Index)
- DynamoDB Streams 및 DAX

**실습**: DynamoDB 테이블 생성 및 쿼리

### [Day 12: 데이터 마이그레이션 서비스](./day12/README.md)
**학습 시간**: 2-3시간  
**핵심 주제**:
- AWS DMS (Database Migration Service)
- AWS DataSync
- Storage Gateway
- Snow 패밀리 (Snowball, Snowmobile)

**실습**: DMS를 활용한 데이터베이스 마이그레이션

### [Day 13: 백업 및 재해 복구](./day13/README.md)
**학습 시간**: 3시간  
**핵심 주제**:
- AWS Backup 서비스
- 교차 리전 복제
- RTO/RPO 개념 및 전략
- 재해 복구 아키텍처 패턴

**실습**: 자동화된 백업 정책 구성

### [Day 14: 주간 복습 및 실습 프로젝트](./day14/README.md)
**학습 시간**: 4-5시간  
**핵심 활동**:
- 2주차 내용 종합 복습
- 실습 프로젝트: 데이터 레이크 아키텍처 구축
- 주간 퀴즈 (35문제)
- 스토리지 비용 최적화 시나리오

## 📊 주차 진도 체크리스트

- [ ] Day 8: S3 스토리지 서비스 마스터
- [ ] Day 9: 블록/파일 스토리지 이해
- [ ] Day 10: 관계형 데이터베이스 설계
- [ ] Day 11: NoSQL 데이터베이스 활용
- [ ] Day 12: 데이터 마이그레이션 전략
- [ ] Day 13: 백업 및 재해 복구 계획
- [ ] Day 14: 주간 프로젝트 완성

## 🎯 주요 학습 성과

이 주를 마치면 다음을 할 수 있게 됩니다:

1. **스토리지 아키텍처 설계**: 요구사항에 맞는 최적의 스토리지 솔루션 선택
2. **데이터베이스 관리**: RDS와 DynamoDB를 활용한 확장 가능한 데이터베이스 구축
3. **데이터 보호**: 백업, 복제, 재해 복구 전략 수립 및 구현
4. **비용 최적화**: 스토리지 클래스와 생명주기 정책을 통한 비용 효율성 달성

## 📚 참고 자료

### AWS 공식 문서
- [S3 사용 설명서](https://docs.aws.amazon.com/s3/)
- [EBS 사용 설명서](https://docs.aws.amazon.com/ebs/)
- [RDS 사용 설명서](https://docs.aws.amazon.com/rds/)
- [DynamoDB 사용 설명서](https://docs.aws.amazon.com/dynamodb/)

### 아키텍처 가이드
- [데이터 레이크 아키텍처](https://aws.amazon.com/big-data/datalakes-and-analytics/)
- [데이터베이스 마이그레이션 가이드](https://aws.amazon.com/dms/)

## 💡 학습 팁

1. **비용 인식**: 스토리지 비용 계산기를 활용하여 비용 효율성 학습
2. **성능 테스트**: 다양한 스토리지 옵션의 성능 특성 직접 비교
3. **실제 시나리오**: 실무에서 자주 발생하는 데이터 관리 시나리오 중심 학습
4. **모니터링**: CloudWatch를 활용한 스토리지 및 데이터베이스 모니터링 습관화

## 🔗 네비게이션

- [← Week 1: AWS 기초 및 핵심 서비스](../week1/README.md)
- [Week 3: 애플리케이션 서비스 및 배포 →](../week3/README.md)

---

**💾 데이터는 현대 애플리케이션의 핵심입니다. 올바른 데이터 관리 전략을 학습해보세요!**