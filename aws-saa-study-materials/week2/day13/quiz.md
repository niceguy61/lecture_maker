# Day 13 퀴즈: 백업 및 재해 복구

## 문제 1
**회사에서 RTO 4시간, RPO 1시간 요구사항을 가진 중요한 애플리케이션을 AWS에서 운영하고 있습니다. 이 요구사항을 만족하는 가장 적절한 재해 복구 전략은 무엇입니까?**

A) Backup and Restore  
B) Pilot Light  
C) Warm Standby  
D) Multi-Site Active/Active  

<details>
<summary>정답 및 해설</summary>

**정답: C) Warm Standby**

**해설:**
- RTO 4시간, RPO 1시간은 중간 수준의 요구사항입니다
- **Backup and Restore**: RTO가 너무 길어서 4시간 요구사항을 만족하기 어려움
- **Pilot Light**: 복구 시간이 길어 4시간 RTO를 만족하기 어려울 수 있음
- **Warm Standby**: 축소된 환경을 다른 리전에서 실행하여 빠른 확장 가능, RTO 4시간 만족 가능
- **Multi-Site Active/Active**: 요구사항보다 과도한 솔루션으로 비용이 많이 듦

Warm Standby는 중간 비용으로 중간 수준의 RTO/RPO 요구사항을 만족하는 최적의 선택입니다.
</details>

---

## 문제 2
**AWS Backup을 사용하여 여러 AWS 서비스의 백업을 중앙에서 관리하려고 합니다. 다음 중 AWS Backup에서 지원하지 않는 서비스는 무엇입니까?**

A) Amazon EC2  
B) Amazon RDS  
C) Amazon Redshift  
D) Amazon EFS  

<details>
<summary>정답 및 해설</summary>

**정답: C) Amazon Redshift**

**해설:**
AWS Backup에서 지원하는 주요 서비스들:
- **EC2**: EBS 볼륨 백업 지원
- **RDS**: 데이터베이스 백업 지원
- **EFS**: 파일 시스템 백업 지원
- **DynamoDB, FSx, Storage Gateway, DocumentDB, Neptune** 등도 지원

**Amazon Redshift**는 AWS Backup에서 직접 지원하지 않습니다. Redshift는 자체적인 스냅샷 기능을 제공하며, 자동 스냅샷과 수동 스냅샷을 통해 백업을 관리합니다.

AWS Backup은 통합 백업 서비스이지만 모든 AWS 서비스를 지원하지는 않으므로, 각 서비스별 백업 기능을 확인해야 합니다.
</details>

---

## 문제 3
**EBS 스냅샷에 대한 설명 중 올바른 것은 무엇입니까?**

A) 스냅샷은 EBS 볼륨과 동일한 가용 영역에만 저장됩니다  
B) 첫 번째 스냅샷은 증분 백업이고, 이후 스냅샷들은 전체 백업입니다  
C) 스냅샷은 Amazon S3에 저장되며 자동으로 여러 가용 영역에 복제됩니다  
D) 스냅샷에서 새 볼륨을 생성할 때는 반드시 원본과 같은 크기여야 합니다  

<details>
<summary>정답 및 해설</summary>

**정답: C) 스냅샷은 Amazon S3에 저장되며 자동으로 여러 가용 영역에 복제됩니다**

**해설:**
각 선택지 분석:

**A) 틀림**: 스냅샷은 S3에 저장되어 리전 전체에서 사용 가능하며, 다른 리전으로도 복사할 수 있습니다.

**B) 틀림**: 첫 번째 스냅샷은 전체 백업이고, 이후 스냅샷들은 증분 백업입니다. 변경된 블록만 저장하여 비용과 시간을 절약합니다.

**C) 정답**: EBS 스냅샷은 Amazon S3에 저장되며, S3의 내구성을 활용하여 자동으로 여러 가용 영역에 복제됩니다.

**D) 틀림**: 스냅샷에서 새 볼륨을 생성할 때 원본보다 큰 크기로 생성할 수 있습니다. 단, 작게는 만들 수 없습니다.

EBS 스냅샷의 S3 저장과 자동 복제는 높은 내구성과 가용성을 제공하는 핵심 특징입니다.
</details>

---

## 문제 4
**AWS Storage Gateway의 세 가지 유형에 대한 설명 중 올바른 것은 무엇입니까?**

A) File Gateway는 iSCSI 프로토콜을 사용하여 S3에 연결합니다  
B) Volume Gateway의 Stored Volumes는 주 데이터를 S3에 저장하고 자주 액세스하는 데이터만 로컬에 캐시합니다  
C) Tape Gateway는 가상 테이프 라이브러리를 제공하여 기존 백업 소프트웨어와 호환됩니다  
D) Volume Gateway는 NFS와 SMB 프로토콜을 지원합니다  

<details>
<summary>정답 및 해설</summary>

**정답: C) Tape Gateway는 가상 테이프 라이브러리를 제공하여 기존 백업 소프트웨어와 호환됩니다**

**해설:**
각 Storage Gateway 유형의 특징:

**A) 틀림**: File Gateway는 NFS/SMB 프로토콜을 사용하여 S3에 파일을 저장합니다. iSCSI는 Volume Gateway에서 사용됩니다.

**B) 틀림**: 이는 Cached Volumes의 설명입니다. Stored Volumes는 주 데이터를 로컬에 저장하고 비동기적으로 S3에 백업합니다.

**C) 정답**: Tape Gateway (VTL - Virtual Tape Library)는 가상 테이프 라이브러리를 제공하여 Veeam, NetBackup 등 기존 백업 소프트웨어와 호환됩니다.

**D) 틀림**: Volume Gateway는 iSCSI 프로토콜을 사용합니다. NFS/SMB는 File Gateway에서 사용됩니다.

Tape Gateway는 기존 테이프 기반 백업 인프라를 클라우드로 마이그레이션할 때 유용한 솔루션입니다.
</details>

---

## 문제 5
**RDS 데이터베이스의 백업에 대한 설명 중 올바른 것은 무엇입니까?**

A) 자동 백업의 보존 기간은 최대 30일까지 설정할 수 있습니다  
B) Point-in-Time Recovery는 1분 단위로 복구 시점을 선택할 수 있습니다  
C) 수동 스냅샷은 DB 인스턴스를 삭제하면 자동으로 함께 삭제됩니다  
D) Multi-AZ 배포에서는 백업이 Primary DB에서 수행되어 성능에 영향을 줍니다  

<details>
<summary>정답 및 해설</summary>

**정답: B) Point-in-Time Recovery는 1분 단위로 복구 시점을 선택할 수 있습니다**

**해설:**
각 선택지 분석:

**A) 틀림**: RDS 자동 백업의 보존 기간은 0-35일까지 설정할 수 있습니다. 0일로 설정하면 자동 백업이 비활성화됩니다.

**B) 정답**: RDS의 Point-in-Time Recovery는 트랜잭션 로그를 사용하여 최대 5분 전까지, 실제로는 1분 단위로 정확한 시점으로 복구할 수 있습니다.

**C) 틀림**: 수동 스냅샷은 DB 인스턴스를 삭제해도 유지됩니다. 자동 백업만 DB 인스턴스와 함께 삭제됩니다.

**D) 틀림**: Multi-AZ 배포에서는 백업이 Standby DB에서 수행되어 Primary DB의 성능에 영향을 주지 않습니다.

Point-in-Time Recovery의 정밀한 복구 기능은 RDS의 중요한 장점 중 하나입니다.
</details>

---

## 퀴즈 완료!

### 점수 계산
- 5문제 중 맞힌 개수: ___/5
- 백분율 점수: ___% 

### 복습이 필요한 영역
점수에 따른 복습 권장사항:

**5점 (100%)**: 완벽합니다! 백업과 재해 복구 개념을 잘 이해하고 있습니다.

**4점 (80%)**: 우수합니다! 틀린 문제 영역을 한 번 더 복습해보세요.

**3점 (60%)**: 양호합니다! 다음 영역들을 중점적으로 복습하세요:
- RTO/RPO 개념과 재해 복구 전략
- AWS Backup 지원 서비스
- EBS 스냅샷 특징

**2점 이하 (40% 이하)**: 오늘 학습한 내용을 다시 한 번 정리해보세요:
- 백업과 재해 복구 기본 개념
- AWS 백업 서비스들의 특징과 차이점
- Storage Gateway 유형별 특징
- RDS 백업 메커니즘

### 오답 노트
틀린 문제들을 다시 정리해보세요:

1. **문제 번호**: ___
   - **선택한 답**: ___
   - **정답**: ___
   - **핵심 개념**: ___

2. **문제 번호**: ___
   - **선택한 답**: ___
   - **정답**: ___
   - **핵심 개념**: ___

### 추가 학습 자료
- [AWS Backup 개발자 가이드](https://docs.aws.amazon.com/aws-backup/)
- [Amazon EBS 스냅샷](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)
- [RDS 백업 및 복원](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html)
- [AWS Storage Gateway 사용 설명서](https://docs.aws.amazon.com/storagegateway/)

내일은 Week 2의 마지막 날로, 이번 주에 학습한 스토리지와 데이터베이스 서비스들을 종합하여 실습 프로젝트를 진행하겠습니다!