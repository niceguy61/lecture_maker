# Day 9 퀴즈: EBS, EFS, FSx

## 📝 일일 퀴즈 (5문제)

### 문제 1: EBS 볼륨 유형 선택
**시나리오:** 고성능 데이터베이스 워크로드를 위해 일관된 높은 IOPS가 필요한 상황입니다. 최대 64,000 IOPS와 높은 내구성이 요구됩니다.

다음 중 가장 적합한 EBS 볼륨 유형은?

A) gp3 (General Purpose SSD v3)  
B) gp2 (General Purpose SSD v2)  
C) io2 (Provisioned IOPS SSD)  
D) st1 (Throughput Optimized HDD)

<details>
<summary>정답 및 해설</summary>

**정답: C) io2 (Provisioned IOPS SSD)**

**해설:**
- io2는 최대 64,000 IOPS를 제공하며, 99.999%의 높은 내구성을 보장합니다
- 데이터베이스와 같은 미션 크리티컬 애플리케이션에 최적화되어 있습니다
- gp3는 최대 16,000 IOPS로 요구사항에 부족합니다
- st1은 HDD 기반으로 IOPS보다는 처리량에 최적화되어 있습니다

**관련 개념:** EBS 볼륨 유형, IOPS 성능, 데이터베이스 스토리지 요구사항
</details>

---

### 문제 2: EFS 성능 모드
**시나리오:** 수천 개의 EC2 인스턴스가 동시에 액세스하는 대규모 콘텐츠 배포 시스템을 구축하고 있습니다. 높은 동시 연결 수가 예상되며, 약간의 지연 시간 증가는 허용 가능합니다.

이 상황에 가장 적합한 EFS 성능 모드는?

A) General Purpose 모드  
B) Max I/O 모드  
C) Provisioned Throughput 모드  
D) Bursting Throughput 모드

<details>
<summary>정답 및 해설</summary>

**정답: B) Max I/O 모드**

**해설:**
- Max I/O 모드는 10,000개 이상의 파일 작업/초를 지원하여 대규모 동시 액세스에 적합합니다
- General Purpose 모드는 최대 7,000 파일 작업/초로 제한됩니다
- Provisioned/Bursting Throughput은 처리량 모드이며, 성능 모드와는 다른 개념입니다
- 약간의 지연 시간 증가를 허용할 수 있다면 Max I/O가 최적의 선택입니다

**관련 개념:** EFS 성능 모드, 동시 액세스, 파일 작업 처리량
</details>

---

### 문제 3: FSx 서비스 선택
**시나리오:** 머신러닝 훈련을 위한 고성능 컴퓨팅 환경을 구축하고 있습니다. S3에 저장된 대용량 데이터셋을 빠르게 로드하고, 수백 GB/s의 처리량이 필요합니다. 훈련 완료 후 결과를 다시 S3에 저장해야 합니다.

이 요구사항에 가장 적합한 FSx 서비스는?

A) FSx for Windows File Server  
B) FSx for Lustre  
C) FSx for NetApp ONTAP  
D) FSx for OpenZFS

<details>
<summary>정답 및 해설</summary>

**정답: B) FSx for Lustre**

**해설:**
- FSx for Lustre는 고성능 컴퓨팅(HPC)과 머신러닝 워크로드에 최적화되어 있습니다
- S3와의 긴밀한 통합을 제공하여 데이터 로딩과 결과 저장이 효율적입니다
- 수백 GB/s의 처리량과 수백만 IOPS를 지원합니다
- 병렬 파일 시스템으로 대규모 컴퓨팅 클러스터에 적합합니다

**관련 개념:** FSx for Lustre, 고성능 컴퓨팅, S3 통합, 머신러닝 인프라
</details>

---

### 문제 4: 스토리지 서비스 비교
**시나리오:** 다음과 같은 요구사항을 가진 애플리케이션을 설계하고 있습니다:
- 여러 EC2 인스턴스에서 동시 읽기/쓰기 액세스
- 표준 POSIX 파일 시스템 의미론 필요
- 자동 확장 및 고가용성
- Linux 기반 애플리케이션

이 요구사항에 가장 적합한 스토리지 서비스는?

A) Amazon S3  
B) Amazon EBS with Multi-Attach  
C) Amazon EFS  
D) Amazon FSx for Windows File Server

<details>
<summary>정답 및 해설</summary>

**정답: C) Amazon EFS**

**해설:**
- EFS는 여러 EC2 인스턴스에서 동시 액세스를 지원하는 완전 관리형 NFS 파일 시스템입니다
- POSIX 호환 파일 시스템으로 표준 파일 시스템 의미론을 제공합니다
- 자동으로 페타바이트까지 확장되며, 다중 AZ에 걸쳐 고가용성을 보장합니다
- Linux 기반 애플리케이션에 최적화되어 있습니다

**관련 개념:** 다중 인스턴스 액세스, POSIX 호환성, NFS 프로토콜, 자동 확장
</details>

---

### 문제 5: EBS 스냅샷 및 백업
**시나리오:** 중요한 데이터베이스가 저장된 EBS 볼륨의 백업 전략을 수립하고 있습니다. 비용 효율적이면서도 빠른 복구가 가능한 방법을 찾고 있으며, 다른 리전으로의 재해 복구도 고려해야 합니다.

EBS 스냅샷에 대한 다음 설명 중 올바른 것은?

A) 스냅샷은 EBS 볼륨과 동일한 가용 영역에만 저장됩니다  
B) 스냅샷은 매번 전체 볼륨을 복사하므로 스토리지 비용이 높습니다  
C) 스냅샷은 S3에 증분식으로 저장되며 다른 리전으로 복사할 수 있습니다  
D) 스냅샷에서 볼륨을 생성할 때 반드시 동일한 볼륨 유형을 사용해야 합니다

<details>
<summary>정답 및 해설</summary>

**정답: C) 스냅샷은 S3에 증분식으로 저장되며 다른 리전으로 복사할 수 있습니다**

**해설:**
- EBS 스냅샷은 S3에 저장되어 리전 전체에 걸쳐 내구성을 제공합니다
- 첫 번째 스냅샷은 전체 복사이지만, 이후 스냅샷은 변경된 블록만 저장하는 증분식 백업입니다
- 스냅샷은 다른 리전으로 복사하여 재해 복구에 활용할 수 있습니다
- 스냅샷에서 볼륨 생성 시 다른 볼륨 유형으로 변경 가능합니다 (예: gp2 → gp3)

**관련 개념:** EBS 스냅샷, 증분 백업, 재해 복구, 리전 간 복사
</details>

---

## 📊 퀴즈 결과 분석

### 점수 계산
- 각 문제당 20점 (총 100점)
- 80점 이상: 우수 (목표 달성)
- 60-79점: 보통 (추가 학습 권장)
- 60점 미만: 재학습 필요

### 학습 영역별 평가

| 영역 | 문제 번호 | 핵심 개념 |
|------|-----------|-----------|
| **EBS 볼륨 유형** | 1, 5 | 성능 특성, 사용 사례, 백업 전략 |
| **EFS 특징** | 2, 4 | 성능 모드, 다중 액세스, POSIX 호환성 |
| **FSx 서비스** | 3 | 서비스 유형별 특징, HPC 워크로드 |

### 추가 학습 권장사항

**80점 미만인 경우:**
- [ ] 이론 내용 재검토 (theory.md)
- [ ] 실습 가이드 재실행 (hands-on/setup-guide.md)
- [ ] AWS 공식 문서 추가 학습
- [ ] 다음 날 학습 전 복습 권장

**특정 영역 취약점:**
- **EBS 관련 문제 틀린 경우**: EBS 볼륨 유형별 성능 특성 재학습
- **EFS 관련 문제 틀린 경우**: 파일 시스템 개념과 성능 모드 복습
- **FSx 관련 문제 틀린 경우**: 각 FSx 서비스의 특징과 사용 사례 정리

## 🔗 추가 학습 자료

### 복습 자료
- [Day 9 이론 내용](./theory.md)
- [Day 9 실습 가이드](./hands-on/setup-guide.md)
- [AWS EBS 사용자 가이드](https://docs.aws.amazon.com/ebs/latest/userguide/)
- [AWS EFS 사용자 가이드](https://docs.aws.amazon.com/efs/latest/ug/)

### 심화 학습
- [EBS 성능 최적화 가이드](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-optimized.html)
- [EFS 성능 가이드](https://docs.aws.amazon.com/efs/latest/ug/performance.html)
- [FSx 서비스 비교](https://aws.amazon.com/fsx/)

---

**다음 학습:** [Day 10 - RDS (Relational Database Service)](../day10/README.md)