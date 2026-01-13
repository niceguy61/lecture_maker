# Day 12 퀴즈: 데이터 마이그레이션 서비스

## 문제 1
**AWS DMS(Database Migration Service)의 주요 장점으로 가장 적절한 것은?**

A) 소스 데이터베이스를 완전히 중단해야만 마이그레이션이 가능하다
B) 소스 데이터베이스가 마이그레이션 중에도 완전히 작동할 수 있다
C) 동일한 데이터베이스 엔진 간에만 마이그레이션이 가능하다
D) 온프레미스 환경에서만 사용할 수 있다

<details>
<summary>정답 및 해설 보기</summary>

**정답: B**

**해설:** 
AWS DMS의 가장 큰 장점 중 하나는 소스 데이터베이스가 마이그레이션 중에도 완전히 작동할 수 있다는 점입니다. 이를 통해 비즈니스 중단 시간을 최소화하면서 데이터를 이전할 수 있습니다. DMS는 서로 다른 데이터베이스 엔진 간의 마이그레이션도 지원하며(이기종 마이그레이션), 클라우드와 온프레미스 환경 모두에서 사용 가능합니다.
</details>

---

## 문제 2
**DMS에서 지원하는 마이그레이션 유형이 아닌 것은?**

A) Full Load (전체 로드)
B) Change Data Capture (CDC)
C) Full Load + CDC
D) Incremental Backup

<details>
<summary>정답 및 해설 보기</summary>

**정답: D**

**해설:**
AWS DMS에서 지원하는 마이그레이션 유형은 다음과 같습니다:
- **Full Load**: 소스에서 타겟으로 모든 기존 데이터를 일괄 복사
- **Change Data Capture (CDC)**: 실시간으로 변경사항을 복제
- **Full Load + CDC**: 초기 전체 로드 후 지속적인 변경사항 복제

Incremental Backup은 DMS의 마이그레이션 유형이 아니라 백업 전략의 하나입니다.
</details>

---

## 문제 3
**다음 시나리오에서 가장 적합한 AWS 서비스는?**

*"회사에서 온프레미스 파일 서버의 100TB 데이터를 Amazon S3로 이전해야 합니다. 네트워크 대역폭이 제한적이고, 일회성 전송이 필요합니다."*

A) AWS DMS
B) AWS DataSync
C) AWS Snow Family
D) AWS Storage Gateway

<details>
<summary>정답 및 해설 보기</summary>

**정답: C**

**해설:**
100TB라는 대용량 데이터를 네트워크 대역폭이 제한적인 환경에서 일회성으로 전송해야 하는 경우, AWS Snow Family(Snowball Edge 또는 Snowmobile)가 가장 적합합니다. 물리적 디바이스를 통해 데이터를 전송하므로 네트워크 제약을 받지 않습니다. DMS는 데이터베이스 마이그레이션용, DataSync는 지속적인 동기화에 적합하며, Storage Gateway는 하이브리드 스토리지 솔루션입니다.
</details>

---

## 문제 4
**AWS DMS 복제 인스턴스(Replication Instance)에 대한 설명으로 올바른 것은?**

A) 소스와 타겟 데이터베이스 사이의 데이터 변환만 담당한다
B) 마이그레이션 작업을 실행하고 모니터링하는 EC2 인스턴스이다
C) 한 번에 하나의 마이그레이션 태스크만 실행할 수 있다
D) 퍼블릭 서브넷에만 배치할 수 있다

<details>
<summary>정답 및 해설 보기</summary>

**정답: B**

**해설:**
DMS 복제 인스턴스는 마이그레이션 작업을 실행하고 모니터링하는 관리형 EC2 인스턴스입니다. 데이터 변환뿐만 아니라 데이터 추출, 로드, 복제 등의 전체 마이그레이션 프로세스를 담당합니다. 하나의 복제 인스턴스에서 여러 마이그레이션 태스크를 동시에 실행할 수 있으며, 보안상 프라이빗 서브넷에 배치하는 것이 권장됩니다.
</details>

---

## 문제 5
**다음 중 AWS DMS를 사용한 Oracle에서 Amazon Aurora PostgreSQL로의 마이그레이션에서 필요한 추가 도구는?**

A) AWS CloudFormation
B) AWS Schema Conversion Tool (SCT)
C) AWS Config
D) AWS Systems Manager

<details>
<summary>정답 및 해설 보기</summary>

**정답: B**

**해설:**
Oracle에서 Amazon Aurora PostgreSQL로의 마이그레이션은 이기종(heterogeneous) 마이그레이션입니다. 이 경우 데이터베이스 스키마, 저장 프로시저, 함수 등을 타겟 데이터베이스 엔진에 맞게 변환해야 합니다. AWS Schema Conversion Tool (SCT)은 이러한 스키마 변환 작업을 자동화해주는 도구입니다. DMS는 실제 데이터 마이그레이션을 담당하고, SCT는 스키마 변환을 담당하여 함께 사용됩니다.
</details>

---

## 점수 계산
- 각 문제당 20점
- 총점: 100점
- 합격 기준: 60점 이상

## 추가 학습 자료
- [AWS DMS 사용 설명서](https://docs.aws.amazon.com/dms/)
- [AWS Schema Conversion Tool 사용 설명서](https://docs.aws.amazon.com/SchemaConversionTool/)
- [AWS 데이터베이스 마이그레이션 모범 사례](https://aws.amazon.com/dms/resources/)

## 오답 노트
틀린 문제가 있다면 해당 개념을 다시 복습해보세요:

- **문제 1-2**: DMS의 기본 개념과 마이그레이션 유형
- **문제 3**: 대용량 데이터 전송을 위한 적절한 서비스 선택
- **문제 4**: DMS 아키텍처 구성 요소의 역할
- **문제 5**: 이기종 마이그레이션에 필요한 도구

각 개념을 확실히 이해하고 넘어가는 것이 중요합니다!