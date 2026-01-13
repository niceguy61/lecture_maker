# Day 8 퀴즈: Amazon S3 (Simple Storage Service)

## 퀴즈 개요
- **총 문제 수**: 5문제
- **예상 소요 시간**: 10-15분
- **난이도**: 중급
- **주제**: Amazon S3 핵심 개념, 스토리지 클래스, 보안, 성능 최적화

---

## 문제 1: S3 스토리지 클래스 선택 (시나리오 기반)

**상황**: 한 회사에서 다음과 같은 데이터 저장 요구사항이 있습니다:
- 매일 생성되는 로그 파일 (즉시 액세스 필요, 30일 후 가끔 액세스)
- 월별 백업 파일 (1년에 2-3번 액세스, 즉시 검색 필요)
- 법적 보관 문서 (7년 보관, 거의 액세스하지 않음, 12시간 검색 시간 허용)

각 데이터 유형에 가장 적합한 S3 스토리지 클래스 조합은?

**A)** Standard → Standard-IA → Glacier Flexible Retrieval  
**B)** Standard → Glacier Instant Retrieval → Glacier Deep Archive  
**C)** Standard-IA → Glacier Flexible Retrieval → Glacier Deep Archive  
**D)** Intelligent-Tiering → Standard-IA → Glacier Flexible Retrieval  

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B) Standard → Glacier Instant Retrieval → Glacier Deep Archive**

**해설:**
- **로그 파일**: 매일 생성되어 즉시 액세스가 필요하므로 **Standard** 클래스가 적합. 30일 후 가끔 액세스하는 패턴은 라이프사이클 정책으로 Standard-IA로 전환 가능.

- **월별 백업 파일**: 1년에 2-3번만 액세스하지만 즉시 검색이 필요하므로 **Glacier Instant Retrieval**이 최적. 비용은 저렴하면서도 밀리초 단위 검색 가능.

- **법적 보관 문서**: 거의 액세스하지 않고 12시간 검색 시간을 허용하므로 **Glacier Deep Archive**가 가장 비용 효율적.

**오답 분석:**
- A) Glacier Flexible Retrieval은 1-5분 검색 시간이므로 백업 파일의 즉시 검색 요구사항에 부적합
- C) 로그 파일의 즉시 액세스 요구사항에 Standard-IA는 부적합 (검색 요금 발생)
- D) Intelligent-Tiering은 최소 128KB 객체에만 적용되며, 모니터링 비용 발생
</details>

---

## 문제 2: S3 보안 정책 분석

다음 S3 버킷 정책을 분석하세요:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpecificIP",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::company-docs/*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        }
      }
    },
    {
      "Sid": "DenyInsecureConnections",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::company-docs",
        "arn:aws:s3:::company-docs/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

이 정책의 효과는?

**A)** 특정 IP 대역에서만 HTTPS를 통해 객체를 읽을 수 있음  
**B)** 모든 사용자가 HTTP/HTTPS로 객체를 읽을 수 있음  
**C)** 특정 IP 대역에서 HTTP로만 객체를 읽을 수 있음  
**D)** HTTPS 연결만 허용하고 IP 제한은 적용되지 않음  

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: A) 특정 IP 대역에서만 HTTPS를 통해 객체를 읽을 수 있음**

**해설:**
이 정책은 두 개의 Statement로 구성되어 있습니다:

1. **첫 번째 Statement (AllowSpecificIP)**:
   - `203.0.113.0/24` IP 대역에서 `s3:GetObject` 액션을 허용
   - 하지만 이것만으로는 충분하지 않음

2. **두 번째 Statement (DenyInsecureConnections)**:
   - `aws:SecureTransport`가 `false`인 경우 모든 액션을 거부
   - 즉, HTTP 연결을 차단하고 HTTPS만 허용

**정책 평가 순서:**
- AWS에서 Deny는 Allow보다 우선순위가 높음
- 따라서 HTTP 연결은 IP가 맞아도 차단됨
- 결과적으로 특정 IP 대역에서 HTTPS로만 접근 가능

**실무 적용:**
- 기업 내부 네트워크에서만 접근 허용
- 보안 연결 강제로 데이터 보호 강화
- 일반적인 기업 보안 정책 패턴
</details>

---

## 문제 3: S3 성능 최적화

대용량 파일을 S3에 업로드하는 애플리케이션의 성능을 최적화하려고 합니다. 다음 중 가장 효과적인 방법들의 조합은?

**A)** 멀티파트 업로드 + 순차적 키 네이밍 + Transfer Acceleration  
**B)** 멀티파트 업로드 + 랜덤 프리픽스 키 네이밍 + Transfer Acceleration  
**C)** 단일 파트 업로드 + 랜덤 프리픽스 키 네이밍 + CloudFront  
**D)** 멀티파트 업로드 + 날짜 기반 키 네이밍 + CloudFront  

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B) 멀티파트 업로드 + 랜덤 프리픽스 키 네이밍 + Transfer Acceleration**

**해설:**

**올바른 최적화 방법들:**

1. **멀티파트 업로드**:
   - 100MB 이상 파일에 권장 (5GB 이상은 필수)
   - 병렬 업로드로 속도 향상
   - 네트워크 오류 시 부분 재시도 가능
   - 최대 10,000개 파트까지 지원

2. **랜덤 프리픽스 키 네이밍**:
   - 핫스팟 방지로 성능 향상
   - 예: `a1b2c3d4/2024/01/15/file.jpg` (랜덤 프리픽스)
   - 프리픽스당 초당 3,500 PUT/COPY/POST/DELETE 요청 지원

3. **Transfer Acceleration**:
   - CloudFront 엣지 로케이션 활용
   - 전 세계에서 S3로의 업로드 속도 향상
   - 특히 원거리 업로드에 효과적

**오답 분석:**
- A) 순차적 키 네이밍은 핫스팟을 생성하여 성능 저하
- C) 대용량 파일에 단일 파트 업로드는 비효율적
- D) 날짜 기반 키 네이밍도 순차적 패턴으로 핫스팟 발생

**실무 팁:**
- 업로드 성능 테스트를 통해 최적 파트 크기 결정 (일반적으로 16-64MB)
- 동시 업로드 스레드 수 조정 (CPU와 네트워크 대역폭 고려)
</details>

---

## 문제 4: S3 버전 관리 및 라이프사이클

S3 버킷에서 버전 관리가 활성화된 상태에서 다음 라이프사이클 정책이 적용되었습니다:

```
- Current versions: 30일 후 Standard-IA로 전환, 90일 후 Glacier로 전환
- Noncurrent versions: 30일 후 Standard-IA로 전환, 60일 후 삭제
- Incomplete multipart uploads: 7일 후 삭제
```

2024년 1월 1일에 `document.pdf` 파일을 업로드하고, 1월 15일에 같은 이름으로 새 버전을 업로드했습니다. 2024년 3월 20일 현재 각 버전의 상태는?

**A)** 현재 버전: Standard-IA, 이전 버전: 삭제됨  
**B)** 현재 버전: Standard-IA, 이전 버전: Standard-IA  
**C)** 현재 버전: Glacier, 이전 버전: 삭제됨  
**D)** 현재 버전: Standard-IA, 이전 버전: 삭제됨  

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: D) 현재 버전: Standard-IA, 이전 버전: 삭제됨**

**해설:**

**타임라인 분석:**
- **2024년 1월 1일**: `document.pdf` 첫 번째 버전 업로드
- **2024년 1월 15일**: `document.pdf` 두 번째 버전 업로드 (첫 번째 버전은 noncurrent가 됨)
- **2024년 3월 20일**: 현재 시점 (약 78일 경과)

**현재 버전 (1월 15일 업로드) 상태:**
- 업로드 후 64일 경과 (1월 15일 → 3월 20일)
- 30일 후 Standard-IA 전환 규칙 적용 → **Standard-IA**
- 90일 후 Glacier 전환은 아직 미적용

**이전 버전 (1월 1일 업로드) 상태:**
- 1월 15일부터 noncurrent 버전이 됨
- Noncurrent 버전은 30일 후 Standard-IA, 60일 후 삭제
- 1월 15일 + 60일 = 3월 15일경 삭제 → **삭제됨**

**라이프사이클 정책 이해:**
- Current versions: 현재 활성 버전에 적용
- Noncurrent versions: 새 버전 업로드로 비활성화된 이전 버전들에 적용
- 각각 독립적인 타이머로 관리

**실무 고려사항:**
- 버전 관리 시 스토리지 비용 증가 주의
- 중요한 데이터는 noncurrent 버전 삭제 기간을 충분히 설정
- 규정 준수 요구사항에 따른 보관 기간 설정
</details>

---

## 문제 5: S3 Cross-Region Replication (CRR) 시나리오

글로벌 서비스를 운영하는 회사에서 다음 요구사항을 만족하는 S3 설정을 구현하려고 합니다:

**요구사항:**
- 서울 리전의 원본 버킷에서 버지니아 리전으로 자동 복제
- 복제된 객체는 원본과 다른 스토리지 클래스 사용 (비용 절약)
- 원본 버킷의 삭제 마커는 복제하지 않음
- 특정 프리픽스(`logs/`)를 가진 객체만 복제

이를 위해 필요한 설정은?

**A)** 버전 관리 비활성화 + CRR 규칙 + IAM 역할 + 프리픽스 필터  
**B)** 버전 관리 활성화 + CRR 규칙 + IAM 역할 + 프리픽스 필터 + 삭제 마커 복제 비활성화  
**C)** 버전 관리 활성화 + CRR 규칙 + S3 버킷 정책 + 프리픽스 필터  
**D)** 버전 관리 활성화 + SRR 규칙 + IAM 역할 + 프리픽스 필터  

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B) 버전 관리 활성화 + CRR 규칙 + IAM 역할 + 프리픽스 필터 + 삭제 마커 복제 비활성화**

**해설:**

**CRR 필수 요구사항:**
1. **버전 관리 활성화**: 원본과 대상 버킷 모두 필수
2. **IAM 역할**: S3가 복제 작업을 수행할 권한 필요
3. **CRR 규칙**: Cross-Region Replication 설정

**추가 설정 요소:**

1. **프리픽스 필터**:
   ```json
   "Filter": {
     "Prefix": "logs/"
   }
   ```
   - 특정 프리픽스를 가진 객체만 복제

2. **삭제 마커 복제 비활성화**:
   ```json
   "DeleteMarkerReplication": {
     "Status": "Disabled"
   }
   ```
   - 원본에서 객체 삭제 시 대상에는 삭제 마커 복제하지 않음

3. **스토리지 클래스 변경**:
   ```json
   "Destination": {
     "Bucket": "arn:aws:s3:::destination-bucket",
     "StorageClass": "STANDARD_IA"
   }
   ```

**오답 분석:**
- A) 버전 관리는 CRR의 필수 요구사항
- C) S3 버킷 정책이 아닌 IAM 역할이 필요
- D) SRR(Same-Region Replication)이 아닌 CRR이 필요

**실무 적용:**
- 재해 복구: 다른 리전에 데이터 백업
- 지연 시간 최적화: 사용자와 가까운 리전에서 데이터 제공
- 규정 준수: 특정 지역에 데이터 보관 요구사항 충족

**비용 고려사항:**
- 복제 요청 비용
- 대상 리전 스토리지 비용
- 리전 간 데이터 전송 비용
</details>

---

## 퀴즈 완료 후 학습 정리

### 점수 계산
- **5문제 정답**: 우수 (S3 개념을 잘 이해하고 있습니다)
- **4문제 정답**: 양호 (몇 가지 세부사항을 더 학습하면 좋겠습니다)
- **3문제 정답**: 보통 (기본 개념은 이해했지만 추가 학습이 필요합니다)
- **2문제 이하**: 복습 필요 (이론 내용을 다시 검토해보세요)

### 틀린 문제가 있다면...

**문제 1번을 틀렸다면**: 
- S3 스토리지 클래스별 특성과 비용 구조 복습
- 액세스 패턴에 따른 최적 클래스 선택 기준 학습

**문제 2번을 틀렸다면**: 
- S3 버킷 정책 문법과 조건부 액세스 제어 복습
- IAM 정책과 버킷 정책의 차이점 이해

**문제 3번을 틀렸다면**: 
- S3 성능 최적화 방법론 복습
- 멀티파트 업로드와 키 네이밍 전략 학습

**문제 4번을 틀렸다면**: 
- S3 버전 관리와 라이프사이클 정책 상호작용 복습
- Current vs Noncurrent 버전 개념 정리

**문제 5번을 틀렸다면**: 
- Cross-Region Replication 설정 요구사항 복습
- 복제 규칙과 필터링 옵션 학습

### 다음 학습 준비
내일 Day 9에서는 EBS, EFS, FSx 등 다른 스토리지 서비스들을 학습합니다. 오늘 학습한 S3와의 차이점을 비교하며 각 서비스의 최적 사용 사례를 이해해보겠습니다.

### 추가 학습 자료
- [AWS S3 FAQs](https://aws.amazon.com/s3/faqs/)
- [S3 스토리지 클래스 성능 비교](https://docs.aws.amazon.com/s3/latest/userguide/storage-class-intro.html)
- [S3 보안 모범 사례](https://docs.aws.amazon.com/s3/latest/userguide/security-best-practices.html)

---

**퀴즈 완료 시간**: 약 10-15분  
**복습 권장 시간**: 20-30분 (틀린 문제가 있는 경우)