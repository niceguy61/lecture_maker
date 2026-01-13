# Day 13 실습: 백업 정책 설정 및 스냅샷 관리

## 실습 개요
이번 실습에서는 AWS Console을 통해 백업 정책을 설정하고 스냅샷을 관리하는 방법을 학습합니다. EBS 스냅샷, RDS 백업, 그리고 AWS Backup 서비스를 실제로 사용해보겠습니다.

## 실습 목표
- EBS 스냅샷 생성 및 관리
- RDS 자동 백업 설정
- AWS Backup을 이용한 통합 백업 정책 구성
- 백업 복원 프로세스 이해

## 사전 준비사항
- AWS 계정 및 Console 액세스
- 이전 실습에서 생성한 EC2 인스턴스 (없다면 새로 생성)
- 기본 VPC 환경

## 실습 1: EBS 스냅샷 생성 및 관리

### 1.1 EBS 볼륨 확인

1. **EC2 Console 접속**
   - AWS Console → Services → EC2
   - 좌측 메뉴에서 "Instances" 클릭

2. **인스턴스의 EBS 볼륨 확인**
   - 실행 중인 인스턴스 선택
   - 하단 "Storage" 탭 클릭
   - Root device와 연결된 EBS 볼륨 ID 확인 (예: vol-1234567890abcdef0)

3. **EBS 볼륨 상세 정보 확인**
   - 좌측 메뉴에서 "Volumes" 클릭
   - 해당 볼륨 선택하여 상세 정보 확인

### 1.2 수동 스냅샷 생성

1. **스냅샷 생성**
   - EBS 볼륨 선택
   - Actions → Create snapshot 클릭

2. **스냅샷 설정**
   ```
   Description: Manual snapshot for backup practice - [현재날짜]
   Tags:
     - Key: Name, Value: backup-practice-snapshot
     - Key: Purpose, Value: Learning
   ```

3. **스냅샷 생성 확인**
   - "Create snapshot" 버튼 클릭
   - 좌측 메뉴에서 "Snapshots" 클릭하여 생성 상태 확인

### 1.3 Data Lifecycle Manager (DLM) 설정

1. **DLM 정책 생성**
   - EC2 Console → Elastic Block Store → Lifecycle Manager
   - "Create lifecycle policy" 클릭

2. **정책 기본 설정**
   ```
   Policy type: EBS snapshot policy
   Description: Daily backup policy for practice
   Policy tags:
     - Key: Name, Value: daily-backup-policy
   ```

3. **대상 리소스 설정**
   ```
   Target resource type: Volume
   Target resource tags:
     - Key: Environment, Value: Practice
   ```

4. **스케줄 설정**
   ```
   Schedule name: DailyBackup
   Frequency: Daily
   Starting at: 03:00 UTC
   Retention type: Count
   Retain: 7 snapshots
   ```

5. **정책 생성 완료**
   - "Create policy" 클릭
   - 정책 상태가 "Enabled"인지 확인

### 1.4 스냅샷에서 볼륨 복원

1. **스냅샷 선택**
   - EC2 Console → Snapshots
   - 앞서 생성한 스냅샷 선택

2. **볼륨 생성**
   - Actions → Create volume from snapshot

3. **볼륨 설정**
   ```
   Volume type: gp3
   Size: 기본값 유지
   Availability Zone: 기존 인스턴스와 동일한 AZ 선택
   Tags:
     - Key: Name, Value: restored-from-snapshot
   ```

4. **볼륨 생성 확인**
   - "Create volume" 클릭
   - Volumes 페이지에서 새 볼륨 확인

## 실습 2: RDS 백업 설정

### 2.1 RDS 인스턴스 생성 (백업 설정 포함)

1. **RDS Console 접속**
   - AWS Console → Services → RDS
   - "Create database" 클릭

2. **데이터베이스 엔진 선택**
   ```
   Engine type: MySQL
   Version: 8.0.35 (최신 버전)
   Templates: Free tier
   ```

3. **DB 인스턴스 설정**
   ```
   DB instance identifier: backup-practice-db
   Master username: admin
   Master password: [안전한 비밀번호 설정]
   ```

4. **백업 설정**
   ```
   Backup retention period: 7 days
   Backup window: 03:00-04:00 UTC
   Enable automatic backups: 체크
   ```

5. **추가 설정**
   ```
   Initial database name: practicedb
   Enable deletion protection: 체크 해제 (실습용)
   ```

### 2.2 수동 스냅샷 생성

1. **DB 인스턴스 선택**
   - RDS Console → Databases
   - 생성한 DB 인스턴스 선택

2. **스냅샷 생성**
   - Actions → Take snapshot

3. **스냅샷 설정**
   ```
   Snapshot identifier: backup-practice-manual-snapshot
   ```

4. **스냅샷 생성 확인**
   - "Take snapshot" 클릭
   - Snapshots 페이지에서 생성 상태 확인

### 2.3 Point-in-Time Recovery 테스트

1. **복원 시점 확인**
   - DB 인스턴스 선택
   - Configuration 탭에서 "Latest restorable time" 확인

2. **Point-in-Time 복원**
   - Actions → Restore to point in time

3. **복원 설정**
   ```
   Restore time: Latest restorable time 선택
   DB instance identifier: backup-practice-db-restored
   ```

4. **복원 실행**
   - "Restore DB instance" 클릭
   - 복원 진행 상황 모니터링

## 실습 3: AWS Backup 통합 백업 설정

### 3.1 AWS Backup Console 접속

1. **AWS Backup 서비스 접속**
   - AWS Console → Services → AWS Backup
   - "Get started" 클릭 (처음 사용하는 경우)

### 3.2 백업 볼트 생성

1. **백업 볼트 생성**
   - 좌측 메뉴 → Backup vaults → Create backup vault

2. **볼트 설정**
   ```
   Backup vault name: practice-backup-vault
   Encryption: AWS managed key 선택
   ```

3. **볼트 생성 완료**
   - "Create backup vault" 클릭

### 3.3 백업 계획 생성

1. **백업 계획 생성**
   - 좌측 메뉴 → Backup plans → Create backup plan

2. **계획 생성 방식 선택**
   - "Build a new plan" 선택

3. **백업 계획 기본 설정**
   ```
   Backup plan name: daily-backup-plan
   ```

4. **백업 규칙 설정**
   ```
   Backup rule name: DailyBackupRule
   Backup vault: practice-backup-vault
   Backup frequency: Daily
   Backup window: Use default
   Lifecycle: 
     - Delete after: 30 days
   ```

5. **계획 생성 완료**
   - "Create plan" 클릭

### 3.4 리소스 할당

1. **리소스 할당 생성**
   - 생성된 백업 계획에서 "Assign resources" 클릭

2. **할당 설정**
   ```
   Resource assignment name: ec2-backup-assignment
   IAM role: Default role 선택 또는 새로 생성
   ```

3. **리소스 선택**
   ```
   Resource selection: Include specific resource types
   Resource type: EC2
   ```

4. **태그 기반 선택 (선택사항)**
   ```
   Key: Environment
   Value: Practice
   ```

5. **할당 완료**
   - "Assign resources" 클릭

### 3.5 백업 작업 모니터링

1. **백업 작업 확인**
   - 좌측 메뉴 → Backup jobs
   - 생성된 백업 작업 상태 확인

2. **백업 복구 포인트 확인**
   - 좌측 메뉴 → Recovery points
   - 생성된 복구 포인트 목록 확인

## 실습 4: 백업 복원 테스트

### 4.1 EBS 스냅샷에서 복원

1. **새 인스턴스 생성 준비**
   - EC2 Console → Launch instance

2. **AMI에서 인스턴스 생성**
   - 스냅샷에서 생성한 볼륨을 사용하여 새 인스턴스 생성
   - 또는 기존 인스턴스에 추가 볼륨으로 연결

### 4.2 RDS 스냅샷에서 복원

1. **스냅샷 선택**
   - RDS Console → Snapshots
   - 생성한 수동 스냅샷 선택

2. **DB 인스턴스 복원**
   - Actions → Restore snapshot

3. **복원 설정**
   ```
   DB instance identifier: restored-from-snapshot-db
   DB instance class: db.t3.micro
   ```

### 4.3 AWS Backup에서 복원

1. **복구 포인트 선택**
   - AWS Backup Console → Recovery points
   - 복원할 복구 포인트 선택

2. **복원 작업 시작**
   - Actions → Restore

3. **복원 설정**
   - 복원 대상 설정 (새 리소스 또는 기존 리소스 교체)
   - 복원 매개변수 설정

## 실습 5: 교차 리전 백업 설정

### 5.1 교차 리전 스냅샷 복사

1. **스냅샷 선택**
   - EC2 Console → Snapshots
   - 복사할 스냅샷 선택

2. **교차 리전 복사**
   - Actions → Copy snapshot

3. **복사 설정**
   ```
   Destination region: 다른 리전 선택 (예: us-west-2)
   Description: Cross-region backup copy
   Encryption: Enable encryption 체크
   ```

### 5.2 RDS 교차 리전 백업

1. **자동 백업 교차 리전 복사 설정**
   - RDS Console → Automated backups
   - Cross-Region automated backups 설정

2. **설정 구성**
   ```
   Source region: 현재 리전
   Destination region: 백업을 저장할 다른 리전
   KMS key: 암호화 키 선택
   ```

## 실습 정리 및 리소스 정리

### 정리해야 할 리소스들

1. **생성한 EBS 볼륨 삭제**
   - 실습용으로 생성한 추가 볼륨들

2. **RDS 인스턴스 삭제**
   - 백업 실습용 DB 인스턴스들
   - 최종 스냅샷 생성 여부 선택

3. **AWS Backup 리소스 정리**
   - 백업 계획 비활성화
   - 불필요한 복구 포인트 삭제

4. **DLM 정책 삭제**
   - 생성한 라이프사이클 정책 삭제

### 비용 절약 팁

```
⚠️ 중요: 실습 후 반드시 리소스 정리
- EBS 볼륨: 사용하지 않는 볼륨은 즉시 삭제
- RDS 인스턴스: 실습 완료 후 삭제
- 스냅샷: 필요 없는 스냅샷은 정기적으로 삭제
- 교차 리전 백업: 추가 비용 발생하므로 주의
```

## 실습 검증 체크리스트

- [ ] EBS 스냅샷 수동 생성 완료
- [ ] DLM 정책을 통한 자동 백업 설정 완료
- [ ] 스냅샷에서 새 볼륨 생성 완료
- [ ] RDS 자동 백업 설정 완료
- [ ] RDS 수동 스냅샷 생성 완료
- [ ] Point-in-Time Recovery 테스트 완료
- [ ] AWS Backup 볼트 생성 완료
- [ ] AWS Backup 계획 및 리소스 할당 완료
- [ ] 교차 리전 백업 설정 완료
- [ ] 백업에서 복원 테스트 완료
- [ ] 실습 리소스 정리 완료

## 문제 해결 가이드

### 일반적인 문제들

1. **스냅샷 생성이 오래 걸리는 경우**
   - 볼륨 크기에 따라 시간이 오래 걸릴 수 있음
   - 첫 번째 스냅샷은 전체 백업이므로 시간이 더 소요됨

2. **DLM 정책이 작동하지 않는 경우**
   - 태그 설정이 정확한지 확인
   - IAM 권한이 올바른지 확인

3. **RDS 백업 복원이 실패하는 경우**
   - 서브넷 그룹 설정 확인
   - 보안 그룹 설정 확인

4. **AWS Backup 권한 오류**
   - IAM 역할에 필요한 권한이 있는지 확인
   - 서비스 연결 역할이 생성되었는지 확인

## 다음 단계

이번 실습을 통해 AWS의 다양한 백업 서비스를 실제로 사용해보았습니다. 내일은 Week 2의 마지막 날로, 이번 주에 학습한 모든 스토리지와 데이터베이스 서비스들을 종합하여 실제 프로젝트를 구축해보겠습니다.

## 추가 실습 아이디어

1. **백업 자동화 스크립트 작성**
   - AWS CLI를 사용한 백업 스크립트
   - Lambda 함수를 이용한 자동화

2. **재해 복구 시나리오 테스트**
   - 다른 리전에서 전체 환경 복원
   - RTO/RPO 측정

3. **비용 최적화**
   - 다양한 스토리지 클래스 활용
   - 백업 보존 정책 최적화