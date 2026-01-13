# Day 6 퀴즈: VPC 고급 네트워킹

## 퀴즈 개요
- **주제**: VPC 고급 네트워킹 (NAT Gateway, VPC Endpoint, VPC Peering, Transit Gateway)
- **문제 수**: 5문제
- **예상 소요 시간**: 15분
- **난이도**: 중급

---

## 문제 1: NAT Gateway vs NAT Instance

**시나리오**: 회사에서 프라이빗 서브넷의 EC2 인스턴스들이 인터넷에 아웃바운드 연결을 해야 하는 상황입니다. 고가용성과 관리 편의성을 고려할 때 NAT Gateway와 NAT Instance 중 어떤 것을 선택해야 할까요?

다음 중 NAT Gateway의 장점으로 **올바르지 않은** 것은?

A) AWS에서 완전 관리되어 패치나 업데이트가 자동으로 처리됩니다
B) 자동으로 고가용성을 제공하며 단일 장애점이 없습니다
C) 보안 그룹을 적용하여 세밀한 트래픽 제어가 가능합니다
D) 최대 45Gbps의 대역폭을 지원합니다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: C**

**해설**: 
NAT Gateway는 보안 그룹을 지원하지 않습니다. 이는 NAT Instance와의 주요 차이점 중 하나입니다.

- **A (올바름)**: NAT Gateway는 AWS 완전 관리형 서비스로 자동 패치/업데이트가 제공됩니다
- **B (올바름)**: NAT Gateway는 가용 영역 내에서 자동 고가용성을 제공합니다
- **C (틀림)**: NAT Gateway는 보안 그룹을 지원하지 않습니다. 보안 그룹은 NAT Instance에서만 사용 가능합니다
- **D (올바름)**: NAT Gateway는 최대 45Gbps의 대역폭을 지원합니다

**추가 설명**: 
NAT Gateway는 관리 편의성과 성능 면에서 우수하지만, 세밀한 보안 제어나 포트 포워딩이 필요한 경우에는 NAT Instance를 고려해야 합니다.
</details>

---

## 문제 2: VPC Endpoint 종류와 사용 사례

**시나리오**: 프라이빗 서브넷의 애플리케이션이 S3와 Lambda 서비스에 접근해야 합니다. 보안을 강화하고 데이터 전송 비용을 절약하기 위해 VPC Endpoint를 사용하려고 합니다.

다음 중 VPC Endpoint에 대한 설명으로 **올바른** 것은?

A) S3와 Lambda 모두 Gateway Endpoint를 사용해야 합니다
B) S3는 Interface Endpoint, Lambda는 Gateway Endpoint를 사용해야 합니다
C) S3는 Gateway Endpoint, Lambda는 Interface Endpoint를 사용해야 합니다
D) S3와 Lambda 모두 Interface Endpoint를 사용해야 합니다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: C**

**해설**: 
VPC Endpoint는 두 가지 유형이 있으며, 각각 지원하는 서비스가 다릅니다.

**Gateway Endpoint**:
- S3와 DynamoDB만 지원
- 무료로 제공
- 라우팅 테이블을 통해 트래픽 라우팅

**Interface Endpoint (PrivateLink)**:
- 대부분의 AWS 서비스 지원 (Lambda 포함)
- ENI(Elastic Network Interface) 기반
- 시간당 요금과 데이터 처리 요금 발생

따라서:
- **S3**: Gateway Endpoint 사용 (무료이고 성능이 우수)
- **Lambda**: Interface Endpoint 사용 (Gateway Endpoint 미지원)

**비용 최적화 팁**: 
S3의 경우 Gateway Endpoint를 사용하면 무료이므로, Interface Endpoint보다 Gateway Endpoint를 우선 고려해야 합니다.
</details>

---

## 문제 3: VPC Peering 제한사항

**시나리오**: 다음과 같은 VPC 구성에서 VPC Peering을 설정하려고 합니다:
- VPC A (10.0.0.0/16) ↔ VPC B (10.1.0.0/16)
- VPC B (10.1.0.0/16) ↔ VPC C (10.2.0.0/16)

VPC A의 인스턴스가 VPC C의 인스턴스와 통신하려고 할 때 발생할 수 있는 문제는?

A) CIDR 블록이 중복되어 통신이 불가능합니다
B) 전이적 라우팅이 지원되지 않아 직접 통신이 불가능합니다
C) 서로 다른 리전에 있어 통신이 불가능합니다
D) DNS 해상도가 활성화되지 않아 통신이 불가능합니다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B**

**해설**: 
VPC Peering의 주요 제한사항 중 하나는 **전이적 라우팅(Transitive Routing)**을 지원하지 않는다는 것입니다.

**전이적 라우팅이란?**
- A-B, B-C가 연결되어 있을 때, A가 C와 자동으로 통신할 수 있는 기능
- VPC Peering에서는 이를 지원하지 않음

**시나리오 분석**:
- VPC A ↔ VPC B: 직접 피어링으로 통신 가능
- VPC B ↔ VPC C: 직접 피어링으로 통신 가능
- VPC A ↔ VPC C: 직접 피어링이 없으므로 통신 불가능

**해결 방법**:
1. VPC A와 VPC C 간에 직접 VPC Peering 연결 생성
2. Transit Gateway 사용 (전이적 라우팅 지원)

**다른 선택지 분석**:
- A: CIDR 블록이 중복되지 않음 (10.0.0.0/16, 10.1.0.0/16, 10.2.0.0/16)
- C: VPC Peering은 교차 리전 연결을 지원함
- D: DNS 해상도는 별도 설정 가능한 옵션임
</details>

---

## 문제 4: Transit Gateway 활용

**시나리오**: 대기업에서 다음과 같은 네트워크 환경을 구축하려고 합니다:
- 5개의 프로덕션 VPC
- 3개의 개발 VPC  
- 2개의 온프레미스 데이터센터
- 1개의 공유 서비스 VPC

모든 네트워크 간 통신이 가능해야 하고, 중앙에서 라우팅 정책을 관리하고 싶습니다.

이 요구사항을 가장 효율적으로 만족하는 AWS 서비스는?

A) VPC Peering을 사용하여 모든 VPC를 메시 형태로 연결
B) Transit Gateway를 사용하여 중앙 집중식 연결
C) Direct Connect Gateway를 사용하여 모든 연결 관리
D) VPN Gateway를 각 VPC에 설치하여 연결

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B**

**해설**: 
Transit Gateway는 이런 복잡한 네트워크 환경에 최적화된 서비스입니다.

**Transit Gateway의 장점**:
- **중앙 집중식 관리**: 단일 지점에서 모든 라우팅 정책 관리
- **확장성**: 최대 5,000개의 VPC 연결 가능
- **전이적 라우팅**: 모든 연결된 네트워크 간 통신 가능
- **온프레미스 연결**: VPN과 Direct Connect 모두 지원
- **라우팅 테이블**: 세밀한 트래픽 제어 가능

**다른 선택지의 문제점**:

**A) VPC Peering 메시 연결**:
- 필요한 연결 수: n(n-1)/2 = 11×10/2 = 55개 연결
- 관리 복잡성 증가
- 전이적 라우팅 미지원

**C) Direct Connect Gateway**:
- 온프레미스 연결에만 특화
- VPC 간 연결은 별도 솔루션 필요

**D) VPN Gateway**:
- 각 VPC마다 별도 설정 필요
- 중앙 집중식 관리 어려움
- 성능 제한

**실제 아키텍처**:
```
온프레미스 DC1 ─┐
온프레미스 DC2 ─┤
프로덕션 VPC1 ─┤
프로덕션 VPC2 ─┤
프로덕션 VPC3 ─┼─ Transit Gateway ─ 중앙 집중식 라우팅
프로덕션 VPC4 ─┤
프로덕션 VPC5 ─┤
개발 VPC1 ─────┤
개발 VPC2 ─────┤
개발 VPC3 ─────┤
공유 서비스 VPC ─┘
```
</details>

---

## 문제 5: VPC Flow Logs 분석

**시나리오**: 보안팀에서 네트워크 트래픽을 모니터링하기 위해 VPC Flow Logs를 활성화했습니다. 다음은 수집된 Flow Logs 레코드의 일부입니다:

```
2 123456789012 eni-1235b8ca 10.0.1.100 203.0.113.12 443 80 6 25 4000 1609459200 1609459260 REJECT OK
2 123456789012 eni-1235b8ca 10.0.1.100 10.0.2.50 22 1024 6 10 800 1609459200 1609459260 ACCEPT OK
```

이 로그를 분석할 때, 첫 번째 레코드에 대한 **올바른** 해석은?

A) 내부 서버(10.0.1.100)에서 외부 웹서버(203.0.113.12)로의 HTTPS 연결이 성공했습니다
B) 외부에서 내부 서버로의 HTTP 연결 시도가 보안 정책에 의해 차단되었습니다  
C) 내부 서버에서 외부로의 HTTPS 연결 시도가 방화벽에 의해 거부되었습니다
D) 로드밸런서에서 백엔드 서버로의 헬스체크가 실패했습니다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B**

**해설**: 
VPC Flow Logs 레코드 형식을 정확히 이해해야 합니다.

**Flow Logs 레코드 형식**:
```
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes windowstart windowend action flowlogstatus
```

**첫 번째 레코드 분석**:
```
2 123456789012 eni-1235b8ca 10.0.1.100 203.0.113.12 443 80 6 25 4000 1609459200 1609459260 REJECT OK
```

- **srcaddr**: 10.0.1.100 (내부 IP)
- **dstaddr**: 203.0.113.12 (외부 IP)  
- **srcport**: 443 (HTTPS 포트)
- **dstport**: 80 (HTTP 포트)
- **protocol**: 6 (TCP)
- **action**: REJECT (거부됨)

**올바른 해석**:
외부 IP(203.0.113.12)에서 내부 서버(10.0.1.100)의 80번 포트(HTTP)로 연결을 시도했지만, 보안 정책(Security Group 또는 NACL)에 의해 차단되었습니다.

**주의사항**: 
Flow Logs에서 srcaddr과 dstaddr은 트래픽의 실제 방향을 나타냅니다. srcport가 443인 것은 외부 서버가 HTTPS 서비스를 제공하고 있음을 의미하며, 실제 연결 시도는 외부에서 내부로 향하는 것입니다.

**보안 관점**:
이런 REJECT 로그는 다음을 의미할 수 있습니다:
- 외부에서의 무단 접근 시도
- 잘못 구성된 보안 그룹 규칙
- 포트 스캔 시도

**두 번째 레코드 참고**:
```
2 123456789012 eni-1235b8ca 10.0.1.100 10.0.2.50 22 1024 6 10 800 1609459200 1609459260 ACCEPT OK
```
이는 내부 서버(10.0.1.100)에서 다른 내부 서버(10.0.2.50)로의 SSH 연결이 성공한 것을 보여줍니다.
</details>

---

## 퀴즈 완료

### 점수 계산
- 5문제 중 맞힌 개수: ___/5
- 점수: ___/100점

### 성취도 평가
- **90-100점**: 우수 - VPC 고급 네트워킹 개념을 완벽히 이해하고 있습니다
- **70-89점**: 양호 - 대부분의 개념을 이해하고 있으나, 일부 세부사항 복습 필요
- **50-69점**: 보통 - 기본 개념은 이해하고 있으나, 추가 학습이 필요합니다
- **50점 미만**: 미흡 - Day 6 이론 내용과 실습을 다시 복습해주세요

### 오답 노트
틀린 문제가 있다면 해당 문제의 해설을 다시 읽어보고, 관련 이론 내용을 복습하세요.

**복습이 필요한 주제별 참고 자료**:
- **NAT Gateway**: Day 6 이론 - 섹션 1
- **VPC Endpoint**: Day 6 이론 - 섹션 2  
- **VPC Peering**: Day 6 이론 - 섹션 3
- **Transit Gateway**: Day 6 이론 - 섹션 4
- **VPC Flow Logs**: Day 6 이론 - 섹션 6

### 다음 단계
- 점수가 70점 이상이면 Day 7(주간 복습 및 종합 실습)으로 진행
- 점수가 70점 미만이면 Day 6 내용을 다시 복습한 후 퀴즈 재응시 권장

---

## 추가 학습 자료

### 📚 심화 학습 주제
1. **VPC Endpoint 정책 고급 설정**
2. **Transit Gateway 라우팅 테이블 최적화**
3. **VPC Flow Logs를 활용한 보안 분석**
4. **네트워크 성능 최적화 기법**

### 🔗 유용한 링크
- [AWS VPC 사용 설명서](https://docs.aws.amazon.com/vpc/)
- [VPC 네트워킹 모범 사례](https://aws.amazon.com/vpc/best-practices/)
- [AWS Well-Architected Framework - 보안 원칙](https://aws.amazon.com/architecture/well-architected/)

### 💡 실무 팁
- 프로덕션 환경에서는 항상 다중 AZ NAT Gateway 구성을 고려하세요
- VPC Endpoint 사용 시 비용과 보안 이점을 함께 고려하세요
- Flow Logs 데이터는 보안 분석뿐만 아니라 비용 최적화에도 활용할 수 있습니다