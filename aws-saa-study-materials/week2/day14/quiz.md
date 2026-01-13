# Week 2 종합 퀴즈: 스토리지 및 데이터베이스 서비스

## 📋 퀴즈 정보
- **문제 수**: 15문제
- **제한 시간**: 30분
- **합격 점수**: 105점 (70% 이상, 11문제 이상 정답)
- **난이도**: 중급
- **범위**: Week 2 전체 내용 (Day 8-13)
- **선택지**: 각 문제당 5개 선택지 (A, B, C, D, E)
- **복수 정답**: 4문제 (문제 3, 4, 13, 15) - 전체의 약 27%

---

## 문제 1
**주제**: S3 스토리지 클래스 (Day 8)

한 회사에서 다음과 같은 데이터 액세스 패턴을 가지고 있습니다:
- 웹 애플리케이션 로그: 매일 생성, 30일간 자주 액세스, 이후 1년간 가끔 액세스
- 규정 준수 문서: 생성 후 즉시 아카이브, 필요시 12시간 내 복구 가능해야 함

각각에 가장 적합한 S3 스토리지 클래스 조합은?

A) Standard → Standard-IA → Glacier Instant Retrieval  
B) Standard → One Zone-IA → Glacier Flexible Retrieval  
C) Standard → Standard-IA → Glacier Deep Archive  
D) Standard → Glacier Instant Retrieval → Glacier Deep Archive  
E) Intelligent-Tiering → Glacier Flexible Retrieval → Deep Archive  

<details>
<summary>정답 및 해설</summary>

**정답: C) Standard → Standard-IA → Glacier Deep Archive**

**해설:**
- 웹 애플리케이션 로그: Standard (30일) → Standard-IA (1년) 
  - 30일간 자주 액세스하므로 Standard 적합
  - 이후 가끔 액세스하므로 Standard-IA 적합
- 규정 준수 문서: Glacier Deep Archive
  - 즉시 아카이브하고 12시간 내 복구 가능 (Deep Archive는 12시간 복구 지원)
  - 가장 저렴한 장기 아카이브 솔루션

**오답 분석:**
- A) Glacier Instant Retrieval은 즉시 액세스가 필요한 아카이브용
- B) One Zone-IA는 단일 AZ로 내구성이 낮음
- D) 웹 로그를 바로 Glacier로 보내는 것은 비효율적
</details>

---

## 문제 2
**주제**: EBS 볼륨 타입 (Day 9)

다음 워크로드에 가장 적합한 EBS 볼륨 타입은?

**시나리오**: 고성능 데이터베이스 서버
- 지속적으로 높은 IOPS 필요 (20,000 IOPS)
- 낮은 지연시간 중요
- 99.999% 내구성 필요
- 비용보다 성능 우선

A) gp3 (General Purpose SSD)  
B) io2 (Provisioned IOPS SSD)  
C) st1 (Throughput Optimized HDD)  
D) sc1 (Cold HDD)  

<details>
<summary>정답 및 해설</summary>

**정답: B) io2 (Provisioned IOPS SSD)**

**해설:**
- 20,000 IOPS 요구사항을 만족하려면 Provisioned IOPS SSD 필요
- io2는 최대 64,000 IOPS 지원 가능
- 99.999% 내구성 제공 (gp3는 99.8~99.9%)
- 일관된 성능과 낮은 지연시간 보장

**EBS 볼륨 타입 비교:**
- gp3: 최대 16,000 IOPS, 99.8~99.9% 내구성
- io2: 최대 64,000 IOPS, 99.999% 내구성
- st1/sc1: HDD 기반, 높은 IOPS 부적합
</details>

---

## 문제 3
**주제**: RDS vs DynamoDB (Day 10-11)

다음 중 DynamoDB를 선택해야 하는 시나리오는?

A) 복잡한 조인 쿼리가 필요한 재무 시스템  
B) ACID 트랜잭션이 중요한 주문 관리 시스템  
C) 초당 수만 건의 읽기/쓰기가 필요한 게임 리더보드  
D) 복잡한 분석 쿼리가 필요한 데이터 웨어하우스  
E) 실시간 채팅 애플리케이션의 메시지 저장  

<details>
<summary>정답 및 해설</summary>

**정답: C, E**

**해설:**
DynamoDB가 적합한 시나리오들:
- **C) 게임 리더보드**: 높은 확장성, 낮은 지연시간, 자동 확장으로 초당 수만 건 처리 가능
- **E) 실시간 채팅**: 빠른 읽기/쓰기, 단순한 키-값 구조로 메시지 저장에 적합

**다른 선택지 분석:**
- A) 복잡한 조인 → RDS/Aurora 적합
- B) ACID 트랜잭션 → RDS 적합  
- D) 복잡한 분석 쿼리 → Redshift 적합
</details>

---

## 문제 4
**주제**: 데이터 마이그레이션 (Day 12)

온프레미스 Oracle 데이터베이스를 AWS로 마이그레이션하려고 합니다. 다음 중 가장 적절한 전략은?

**요구사항:**
- 최소 다운타임
- 이종 데이터베이스 마이그레이션 (Oracle → PostgreSQL)
- 마이그레이션 중 데이터 일관성 보장

A) AWS DataSync 사용  
B) AWS DMS (Database Migration Service) 사용  
C) AWS Storage Gateway 사용  
D) AWS Snowball 사용  
E) AWS Database Migration Service + Schema Conversion Tool 사용  

<details>
<summary>정답 및 해설</summary>

**정답: B, E**

**해설:**
이종 데이터베이스 마이그레이션에 적합한 솔루션들:
- **B) AWS DMS**: 최소 다운타임으로 지속적인 데이터 복제 (CDC) 지원, 데이터 일관성 보장
- **E) DMS + SCT**: 스키마 변환(SCT)과 데이터 마이그레이션(DMS)을 함께 사용하는 완전한 솔루션

**다른 서비스 용도:**
- A) DataSync: 파일 시스템 동기화
- C) Storage Gateway: 하이브리드 스토리지
- D) Snowball: 대용량 데이터 물리적 전송
</details>

---

## 문제 5
**주제**: S3 보안 및 액세스 제어 (Day 8)

S3 버킷에 대한 다음 설명 중 올바른 것은?

A) 버킷 정책과 IAM 정책이 충돌하면 항상 버킷 정책이 우선한다  
B) S3 버킷은 기본적으로 퍼블릭 액세스가 허용된다  
C) 버킷 정책에서 Deny가 있으면 IAM의 Allow보다 우선한다  
D) 같은 AWS 계정 내에서는 모든 S3 객체에 자동으로 액세스할 수 있다  

<details>
<summary>정답 및 해설</summary>

**정답: C) 버킷 정책에서 Deny가 있으면 IAM의 Allow보다 우선한다**

**해설:**
AWS 권한 평가 순서:
1. 명시적 Deny가 있으면 항상 거부
2. 명시적 Allow가 있으면 허용
3. 기본적으로 모든 것은 거부

**다른 선택지 분석:**
- A) 잘못됨: Deny는 항상 우선하지만, Allow의 경우 IAM과 버킷 정책 모두 필요
- B) 잘못됨: S3 버킷은 기본적으로 프라이빗
- D) 잘못됨: 명시적 권한이 필요함
</details>

---

## 문제 6
**주제**: EFS vs EBS (Day 9)

다음 시나리오에 가장 적합한 스토리지 솔루션은?

**시나리오**: 여러 EC2 인스턴스에서 동시에 액세스해야 하는 공유 파일 시스템이 필요합니다. 파일 시스템은 자동으로 확장되어야 하고, POSIX 호환이어야 합니다.

A) EBS Multi-Attach  
B) EFS (Elastic File System)  
C) S3 with FUSE  
D) Instance Store  

<details>
<summary>정답 및 해설</summary>

**정답: B) EFS (Elastic File System)**

**해설:**
EFS가 적합한 이유:
- 여러 EC2 인스턴스에서 동시 액세스 지원
- 자동 확장/축소 (페타바이트까지)
- POSIX 호환 파일 시스템
- NFS v4.1 프로토콜 사용

**다른 선택지 분석:**
- A) EBS Multi-Attach: 제한된 인스턴스 수, 클러스터 파일 시스템 필요
- C) S3 with FUSE: 객체 스토리지, POSIX 완전 호환 아님
- D) Instance Store: 임시 스토리지, 인스턴스 종료 시 데이터 손실
</details>

---

## 문제 7
**주제**: DynamoDB 성능 최적화 (Day 11)

DynamoDB 테이블에서 "hot partition" 문제가 발생했습니다. 가장 효과적인 해결 방법은?

A) 더 많은 RCU/WCU 프로비저닝  
B) 파티션 키 설계 개선  
C) Global Secondary Index 추가  
D) DynamoDB Accelerator (DAX) 사용  

<details>
<summary>정답 및 해설</summary>

**정답: B) 파티션 키 설계 개선**

**해설:**
Hot Partition 문제의 근본 원인:
- 특정 파티션에 트래픽 집중
- 파티션 키의 카디널리티 부족
- 순차적 키 사용 (타임스탬프 등)

**해결 방법:**
- 높은 카디널리티의 파티션 키 사용
- 복합 키 구조 활용
- 랜덤 접미사 추가

**다른 선택지:**
- A) 용량 증가는 임시 해결책
- C) GSI는 쿼리 패턴 개선용
- D) DAX는 읽기 성능 개선용
</details>

---

## 문제 8
**주제**: 백업 및 재해 복구 (Day 13)

다음 중 RDS의 자동 백업에 대한 설명으로 올바른 것은?

A) 자동 백업은 최대 35일까지 보관 가능하다  
B) 자동 백업은 다른 리전에 자동으로 복사된다  
C) 자동 백업 중에는 데이터베이스 성능이 크게 저하된다  
D) Multi-AZ 배포에서는 Standby에서 백업이 수행된다

<details>
<summary>정답 및 해설</summary>

**정답: D**

**해설:**
RDS Multi-AZ 백업 특징:
- Standby 인스턴스에서 백업 수행
- Primary 인스턴스의 I/O 영향 최소화
- 일관된 백업 보장

**다른 선택지 분석:**
- A) 잘못됨: 최대 35일이 아닌 7일 (기본 1일)
- B) 잘못됨: 교차 리전 백업은 수동 설정 필요
- C) 잘못됨: Multi-AZ에서는 성능 영향 최소화
</details>

---

## 문제 9
**주제**: 스토리지 비용 최적화 (Day 8-9)

다음 시나리오에서 가장 비용 효율적인 스토리지 전략은?

**시나리오**: 
- 로그 파일: 처음 30일간 자주 액세스, 이후 90일간 가끔 액세스, 그 후 7년간 보관 (규정 준수)
- 예측 불가능한 액세스 패턴

A) S3 Standard → Standard-IA → Glacier → Deep Archive  
B) S3 Intelligent-Tiering 사용  
C) 모든 데이터를 S3 Standard에 보관  
D) S3 One Zone-IA → Glacier Flexible Retrieval  

<details>
<summary>정답 및 해설</summary>

**정답: B) S3 Intelligent-Tiering 사용**

**해설:**
S3 Intelligent-Tiering이 적합한 이유:
- 예측 불가능한 액세스 패턴에 최적화
- 자동으로 가장 비용 효율적인 티어로 이동
- 검색 비용 없음
- Archive 및 Deep Archive 티어 포함

**비용 구조:**
- 모니터링 비용: 객체당 $0.0025/월
- 자동 티어링으로 최대 68% 비용 절감 가능

**다른 선택지:**
- A) 수동 관리 필요, 예측 불가능한 패턴에 부적합
- C) 비용 비효율적
- D) One Zone-IA는 내구성 낮음
</details>

---

## 문제 10
**주제**: 데이터베이스 성능 및 확장성 (Day 10-11)

다음 중 Aurora의 특징으로 올바르지 않은 것은?

A) 스토리지가 자동으로 확장된다 (최대 128TB)  
B) 최대 15개의 Read Replica를 지원한다  
C) 쓰기 작업은 모든 Read Replica에서 가능하다  
D) 6개의 데이터 복사본을 3개 AZ에 저장한다  

<details>
<summary>정답 및 해설</summary>

**정답: C**

**해설:**
Aurora 아키텍처:
- 단일 Writer 인스턴스만 쓰기 작업 수행
- Read Replica는 읽기 전용
- Writer 장애 시 Read Replica가 Writer로 승격 가능

**올바른 Aurora 특징:**
- A) 스토리지 자동 확장 (10GB → 128TB)
- B) 최대 15개 Read Replica 지원
- D) 3개 AZ에 각각 2개씩 총 6개 복사본

**Aurora vs 일반 RDS:**
- 5배 빠른 MySQL 성능
- 3배 빠른 PostgreSQL 성능
- 클러스터 볼륨으로 스토리지 공유
</details>

---


## 문제 11
**주제**: AWS Glue와 데이터 카탈로그 (Day 12)

AWS Glue 크롤러의 주요 기능은 무엇입니까?

A) 데이터를 다른 형식으로 변환한다  
B) 데이터 소스를 스캔하여 스키마를 자동으로 발견한다  
C) 데이터베이스 간 실시간 복제를 수행한다  
D) 데이터 품질을 자동으로 검증한다  

<details>
<summary>정답 및 해설</summary>

**정답: B) 데이터 소스를 스캔하여 스키마를 자동으로 발견한다**

**해설:**
AWS Glue 크롤러의 핵심 기능:
- 데이터 소스 (S3, RDS, DynamoDB 등) 스캔
- 스키마 자동 발견 및 추론
- AWS Glue Data Catalog에 메타데이터 저장
- 테이블 정의 자동 생성

**크롤러 작동 과정:**
1. 지정된 데이터 소스 스캔
2. 데이터 형식 및 스키마 분석
3. 파티션 구조 발견
4. Data Catalog에 테이블 메타데이터 저장

**다른 선택지:**
- A) 데이터 변환은 Glue ETL Job의 역할
- C) 실시간 복제는 DMS의 역할
- D) 데이터 품질 검증은 Glue DataBrew의 역할
</details>

---

## 문제 12
**주제**: S3 Cross-Region Replication (Day 8)

S3 Cross-Region Replication (CRR)에 대한 설명으로 올바른 것은?

A) 기존 객체들도 자동으로 복제된다  
B) 소스와 대상 버킷의 버전 관리가 모두 활성화되어야 한다  
C) 같은 리전 내에서도 사용할 수 있다  
D) 복제된 객체는 원본과 다른 스토리지 클래스를 가질 수 없다  

<details>
<summary>정답 및 해설</summary>

**정답: B**

**해설:**
S3 CRR 요구사항:
- 소스 및 대상 버킷 모두 버전 관리 활성화 필수
- 서로 다른 AWS 리전에 위치
- 적절한 IAM 권한 설정
- 복제 규칙 구성

**CRR 특징:**
- 비동기 복제 (몇 분 내 완료)
- 객체 메타데이터 및 ACL도 복제
- 암호화된 객체 복제 지원

**다른 선택지 분석:**
- A) 기존 객체는 S3 Batch Replication으로 별도 복제 필요
- C) 같은 리전 내는 SRR (Same-Region Replication)
- D) 대상에서 다른 스토리지 클래스 지정 가능
</details>

---

## 문제 13
**주제**: DynamoDB Global Tables (Day 11)

DynamoDB Global Tables의 특징으로 올바르지 않은 것은?

A) 여러 AWS 리전에 걸쳐 완전 관리형 다중 마스터 복제를 제공한다  
B) 강력한 일관성(Strong Consistency) 읽기를 모든 리전에서 보장한다  
C) 자동 장애 조치 기능을 제공한다  
D) DynamoDB Streams가 활성화되어야 한다  
E) 모든 리전에서 동일한 테이블 이름을 사용해야 한다  

<details>
<summary>정답 및 해설</summary>

**정답: B, E**

**해설:**
DynamoDB Global Tables의 잘못된 특징들:
- **B) 강력한 일관성**: 최종 일관성(Eventual Consistency)만 제공, 강력한 일관성은 로컬 리전에서만 가능
- **E) 테이블 이름**: 각 리전에서 다른 테이블 이름 사용 가능, 동일한 이름 필수 아님

**올바른 Global Tables 특징:**
- A) 다중 마스터 복제 (모든 리전에서 읽기/쓰기 가능)
- C) 자동 장애 조치 기능 제공
- D) DynamoDB Streams 기반 복제 (활성화 필수)

**Global Tables 특징:**
- 일반적으로 1초 이내 전파
- 충돌 해결 메커니즘 (Last Writer Wins)
- 글로벌 애플리케이션 및 재해 복구에 적합
</details>

---

## 문제 14
**주제**: EBS 스냅샷 및 AMI (Day 9)

EBS 스냅샷에 대한 설명으로 올바른 것은?

A) 스냅샷은 항상 전체 볼륨을 복사한다  
B) 스냅샷은 동일한 AZ 내에서만 사용할 수 있다  
C) 첫 번째 스냅샷은 전체 복사, 이후는 증분 백업이다  
D) 암호화된 볼륨의 스냅샷은 암호화되지 않는다  

<details>
<summary>정답 및 해설</summary>

**정답: C) 첫 번째 스냅샷은 전체 복사, 이후는 증분 백업이다**

**해설:**
EBS 스냅샷 메커니즘:
- 첫 번째 스냅샷: 전체 볼륨 데이터 복사
- 후속 스냅샷: 변경된 블록만 증분 저장
- S3에 저장되어 높은 내구성 보장
- 리전 간 복사 가능

**스냅샷 특징:**
- 블록 레벨 증분 백업
- 압축 및 중복 제거 적용
- 암호화된 볼륨 → 암호화된 스냅샷

**다른 선택지 분석:**
- A) 증분 백업으로 효율성 제공
- B) 다른 AZ, 다른 리전에서도 사용 가능
- D) 암호화 상태 유지됨
</details>

---

## 문제 15
**주제**: 데이터베이스 백업 전략 (Day 13)

다음 중 RDS 자동 백업과 수동 스냅샷의 차이점으로 올바른 것은?

A) 자동 백업은 암호화를 지원하지 않는다  
B) 수동 스냅샷은 DB 인스턴스 삭제 시 함께 삭제된다  
C) 자동 백업은 Point-in-Time Recovery를 지원하지만 수동 스냅샷은 지원하지 않는다  
D) 수동 스냅샷은 보관 기간 제한이 없다  
E) 자동 백업은 다른 리전으로 복사할 수 없다  

<details>
<summary>정답 및 해설</summary>

**정답: C, D**

**해설:**
RDS 자동 백업과 수동 스냅샷의 올바른 차이점들:
- **C) Point-in-Time Recovery**: 자동 백업만 지원, 수동 스냅샷은 특정 시점 복구만 가능
- **D) 보관 기간**: 수동 스냅샷은 무제한, 자동 백업은 0-35일 제한

**RDS 백업 유형 비교:**

**자동 백업:**
- 보관 기간: 0-35일 (기본 7일)
- Point-in-Time Recovery 지원
- DB 인스턴스 삭제 시 함께 삭제

**수동 스냅샷:**
- 보관 기간: 무제한 (명시적 삭제 전까지)
- 특정 시점 복구만 가능
- DB 인스턴스 삭제 후에도 유지

**공통 특징:**
- 둘 다 암호화 지원
- 다른 리전으로 복사 가능
</details>

---

## 📊 최종 채점 기준 (15문제)

| 점수 | 등급 | 평가 |
|------|------|------|
| 135-150점 | A | 우수 - Week 3 진행 준비 완료 |
| 120-134점 | B | 양호 - 일부 복습 후 진행 |
| 105-119점 | C | 보통 - 취약 부분 집중 복습 필요 |
| 90-104점 | D | 미흡 - Week 2 전체 재학습 권장 |
| 90점 미만 | F | 불합격 - 기초부터 다시 학습 |

**합격 기준**: 105점 이상 (70% 이상, 11문제 이상 정답)

## 🔍 오답 분석 가이드

### 60점 미만인 경우
- Week 2 전체 내용 재학습
- 각 서비스별 핵심 개념 정리
- 실습 다시 수행

### 60-79점인 경우
- 틀린 문제 관련 Day 재학습
- 해당 서비스 AWS 문서 참조
- 추가 실습 수행

### 80점 이상인 경우
- Week 3 진행 준비 완료
- 틀린 부분만 간단히 복습
- 심화 학습 자료 참조

## 📚 추가 학습 자료

### AWS 공식 문서
- [S3 사용자 가이드](https://docs.aws.amazon.com/s3/)
- [RDS 사용자 가이드](https://docs.aws.amazon.com/rds/)
- [DynamoDB 개발자 가이드](https://docs.aws.amazon.com/dynamodb/)

### 실습 환경
- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Hands-on Tutorials](https://aws.amazon.com/getting-started/hands-on/)

### 시험 준비
- [AWS SAA-C03 시험 가이드](https://aws.amazon.com/certification/certified-solutions-architect-associate/)
- [AWS 샘플 문제](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Sample-Questions.pdf)

---

**퀴즈 완료 후 다음 단계:**
1. 점수 확인 및 오답 분석
2. 부족한 부분 복습
3. Week 3 Day 15 학습 준비
4. 스토리지 서비스 치트 시트 활용