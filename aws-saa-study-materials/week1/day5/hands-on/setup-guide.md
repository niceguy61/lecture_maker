# Day 5 실습: VPC 생성 및 서브넷 구성

## 실습 개요

이번 실습에서는 AWS Console을 사용하여 VPC를 생성하고, 퍼블릭 및 프라이빗 서브넷을 구성하는 방법을 학습합니다. 실제 3-tier 웹 애플리케이션을 위한 네트워크 인프라를 구축해보겠습니다.

## 실습 목표

- VPC 생성 및 기본 설정 이해
- 퍼블릭 서브넷과 프라이빗 서브넷 생성
- 인터넷 게이트웨이 연결
- 라우팅 테이블 구성
- 보안 그룹 생성 및 설정

## 사전 준비사항

- AWS 계정 (Free Tier 사용 가능)
- AWS Management Console 접근 권한
- 기본적인 네트워킹 지식

## 예상 소요 시간

약 45-60분

## 실습 아키텍처

이번 실습에서 구축할 VPC 아키텍처:

```
VPC (10.0.0.0/16)
├── 가용 영역 A (us-east-1a)
│   ├── 퍼블릭 서브넷 (10.0.1.0/24) - 웹 서버용
│   └── 프라이빗 서브넷 (10.0.2.0/24) - 애플리케이션 서버용
└── 가용 영역 B (us-east-1b)
    ├── 퍼블릭 서브넷 (10.0.3.0/24) - 웹 서버용
    └── 프라이빗 서브넷 (10.0.4.0/24) - 데이터베이스용
```

---

## 단계 1: VPC 생성

### 1.1 VPC 서비스 접근

1. AWS Management Console에 로그인합니다.
2. 상단 검색창에 "VPC"를 입력하고 **VPC** 서비스를 선택합니다.
3. 좌측 메뉴에서 **Your VPCs**를 클릭합니다.

### 1.2 VPC 생성

1. **Create VPC** 버튼을 클릭합니다.

2. **VPC settings** 섹션에서 다음과 같이 설정합니다:
   - **Resources to create**: `VPC only` 선택
   - **Name tag**: `MyStudyVPC`
   - **IPv4 CIDR block**: `10.0.0.0/16`
   - **IPv6 CIDR block**: `No IPv6 CIDR block` (기본값)
   - **Tenancy**: `Default` (기본값)

3. **Tags** 섹션에서 추가 태그를 설정합니다:
   - **Key**: `Environment`, **Value**: `Study`
   - **Key**: `Project`, **Value**: `SAA-C03-Lab`

4. **Create VPC** 버튼을 클릭합니다.

### 1.3 VPC 생성 확인

- VPC가 성공적으로 생성되면 VPC ID가 표시됩니다 (예: vpc-0123456789abcdef0).
- **State**가 `Available`인지 확인합니다.

---

## 단계 2: 인터넷 게이트웨이 생성 및 연결

### 2.1 인터넷 게이트웨이 생성

1. 좌측 메뉴에서 **Internet Gateways**를 클릭합니다.
2. **Create internet gateway** 버튼을 클릭합니다.
3. **Name tag**에 `MyStudyIGW`를 입력합니다.
4. **Create internet gateway** 버튼을 클릭합니다.

### 2.2 인터넷 게이트웨이를 VPC에 연결

1. 생성된 인터넷 게이트웨이를 선택합니다.
2. **Actions** 드롭다운에서 **Attach to VPC**를 선택합니다.
3. **Available VPCs** 드롭다운에서 앞서 생성한 `MyStudyVPC`를 선택합니다.
4. **Attach internet gateway** 버튼을 클릭합니다.

### 2.3 연결 확인

- **State**가 `Attached`로 변경되었는지 확인합니다.
- **VPC ID**가 올바른 VPC를 가리키는지 확인합니다.

---

## 단계 3: 서브넷 생성

### 3.1 첫 번째 퍼블릭 서브넷 생성 (가용 영역 A)

1. 좌측 메뉴에서 **Subnets**를 클릭합니다.
2. **Create subnet** 버튼을 클릭합니다.

3. **VPC ID**에서 `MyStudyVPC`를 선택합니다.

4. **Subnet settings**에서 다음과 같이 설정합니다:
   - **Subnet name**: `Public-Subnet-1A`
   - **Availability Zone**: `us-east-1a` (또는 사용 가능한 첫 번째 AZ)
   - **IPv4 CIDR block**: `10.0.1.0/24`

5. **Add new subnet** 버튼을 클릭하여 추가 서브넷을 생성합니다.

### 3.2 첫 번째 프라이빗 서브넷 생성 (가용 영역 A)

**Subnet settings**에서 다음과 같이 설정합니다:
- **Subnet name**: `Private-Subnet-1A`
- **Availability Zone**: `us-east-1a` (퍼블릭 서브넷과 동일한 AZ)
- **IPv4 CIDR block**: `10.0.2.0/24`

### 3.3 두 번째 퍼블릭 서브넷 생성 (가용 영역 B)

**Add new subnet** 버튼을 다시 클릭하고:
- **Subnet name**: `Public-Subnet-1B`
- **Availability Zone**: `us-east-1b` (다른 AZ 선택)
- **IPv4 CIDR block**: `10.0.3.0/24`

### 3.4 두 번째 프라이빗 서브넷 생성 (가용 영역 B)

**Add new subnet** 버튼을 다시 클릭하고:
- **Subnet name**: `Private-Subnet-1B`
- **Availability Zone**: `us-east-1b` (두 번째 퍼블릭 서브넷과 동일한 AZ)
- **IPv4 CIDR block**: `10.0.4.0/24`

### 3.5 서브넷 생성 완료

**Create subnet** 버튼을 클릭하여 모든 서브넷을 생성합니다.

---

## 단계 4: 퍼블릭 서브넷 설정

### 4.1 퍼블릭 IP 자동 할당 설정

1. **Subnets** 목록에서 `Public-Subnet-1A`를 선택합니다.
2. **Actions** 드롭다운에서 **Edit subnet settings**를 선택합니다.
3. **Auto-assign public IPv4 address** 옵션을 **Enable**로 설정합니다.
4. **Save** 버튼을 클릭합니다.

5. `Public-Subnet-1B`에 대해서도 동일한 과정을 반복합니다.

---

## 단계 5: 라우팅 테이블 구성

### 5.1 퍼블릭 라우팅 테이블 생성

1. 좌측 메뉴에서 **Route Tables**를 클릭합니다.
2. **Create route table** 버튼을 클릭합니다.
3. 다음과 같이 설정합니다:
   - **Name**: `Public-Route-Table`
   - **VPC**: `MyStudyVPC` 선택
4. **Create route table** 버튼을 클릭합니다.

### 5.2 퍼블릭 라우팅 테이블에 인터넷 게이트웨이 라우트 추가

1. 생성된 `Public-Route-Table`을 선택합니다.
2. 하단의 **Routes** 탭을 클릭합니다.
3. **Edit routes** 버튼을 클릭합니다.
4. **Add route** 버튼을 클릭합니다.
5. 다음과 같이 설정합니다:
   - **Destination**: `0.0.0.0/0`
   - **Target**: `Internet Gateway` 선택 후 `MyStudyIGW` 선택
6. **Save changes** 버튼을 클릭합니다.

### 5.3 퍼블릭 서브넷을 퍼블릭 라우팅 테이블에 연결

1. `Public-Route-Table`이 선택된 상태에서 **Subnet associations** 탭을 클릭합니다.
2. **Edit subnet associations** 버튼을 클릭합니다.
3. `Public-Subnet-1A`와 `Public-Subnet-1B`를 선택합니다.
4. **Save associations** 버튼을 클릭합니다.

### 5.4 프라이빗 라우팅 테이블 확인

1. **Route Tables** 목록에서 VPC의 기본 라우팅 테이블을 찾습니다.
2. 이름을 `Private-Route-Table`로 변경합니다:
   - 라우팅 테이블을 선택하고 **Name** 컬럼의 연필 아이콘을 클릭
   - `Private-Route-Table` 입력 후 저장

---

## 단계 6: 보안 그룹 생성

### 6.1 웹 서버용 보안 그룹 생성

1. 좌측 메뉴에서 **Security Groups**를 클릭합니다.
2. **Create security group** 버튼을 클릭합니다.
3. 다음과 같이 설정합니다:
   - **Security group name**: `WebServer-SG`
   - **Description**: `Security group for web servers`
   - **VPC**: `MyStudyVPC` 선택

4. **Inbound rules** 섹션에서 **Add rule** 버튼을 클릭하여 다음 규칙들을 추가합니다:

   **규칙 1 - HTTP 트래픽**:
   - **Type**: `HTTP`
   - **Protocol**: `TCP`
   - **Port range**: `80`
   - **Source**: `0.0.0.0/0`
   - **Description**: `Allow HTTP from anywhere`

   **규칙 2 - HTTPS 트래픽**:
   - **Type**: `HTTPS`
   - **Protocol**: `TCP`
   - **Port range**: `443`
   - **Source**: `0.0.0.0/0`
   - **Description**: `Allow HTTPS from anywhere`

   **규칙 3 - SSH 접근**:
   - **Type**: `SSH`
   - **Protocol**: `TCP`
   - **Port range**: `22`
   - **Source**: `My IP` (또는 특정 IP 주소)
   - **Description**: `Allow SSH from my IP`

5. **Create security group** 버튼을 클릭합니다.

### 6.2 애플리케이션 서버용 보안 그룹 생성

1. **Create security group** 버튼을 다시 클릭합니다.
2. 다음과 같이 설정합니다:
   - **Security group name**: `AppServer-SG`
   - **Description**: `Security group for application servers`
   - **VPC**: `MyStudyVPC` 선택

3. **Inbound rules**에서 다음 규칙을 추가합니다:

   **규칙 1 - 애플리케이션 포트**:
   - **Type**: `Custom TCP`
   - **Protocol**: `TCP`
   - **Port range**: `8080`
   - **Source**: `Custom` → `WebServer-SG` 선택
   - **Description**: `Allow app traffic from web servers`

   **규칙 2 - SSH 접근**:
   - **Type**: `SSH`
   - **Protocol**: `TCP`
   - **Port range**: `22`
   - **Source**: `Custom` → `WebServer-SG` 선택
   - **Description**: `Allow SSH from web servers`

4. **Create security group** 버튼을 클릭합니다.

### 6.3 데이터베이스용 보안 그룹 생성

1. **Create security group** 버튼을 다시 클릭합니다.
2. 다음과 같이 설정합니다:
   - **Security group name**: `Database-SG`
   - **Description**: `Security group for database servers`
   - **VPC**: `MyStudyVPC` 선택

3. **Inbound rules**에서 다음 규칙을 추가합니다:

   **규칙 1 - MySQL/Aurora**:
   - **Type**: `MYSQL/Aurora`
   - **Protocol**: `TCP`
   - **Port range**: `3306`
   - **Source**: `Custom` → `AppServer-SG` 선택
   - **Description**: `Allow MySQL from app servers`

4. **Create security group** 버튼을 클릭합니다.

---

## 단계 7: 구성 검증

### 7.1 VPC 구성 요약 확인

1. **Your VPCs**에서 생성한 VPC의 세부 정보를 확인합니다:
   - **Name**: MyStudyVPC
   - **State**: Available
   - **IPv4 CIDR**: 10.0.0.0/16

### 7.2 서브넷 구성 확인

**Subnets**에서 다음 서브넷들이 올바르게 생성되었는지 확인합니다:

| 서브넷 이름 | CIDR 블록 | 가용 영역 | 타입 |
|-------------|-----------|-----------|------|
| Public-Subnet-1A | 10.0.1.0/24 | us-east-1a | 퍼블릭 |
| Private-Subnet-1A | 10.0.2.0/24 | us-east-1a | 프라이빗 |
| Public-Subnet-1B | 10.0.3.0/24 | us-east-1b | 퍼블릭 |
| Private-Subnet-1B | 10.0.4.0/24 | us-east-1b | 프라이빗 |

### 7.3 라우팅 테이블 확인

1. **Route Tables**에서 `Public-Route-Table`을 선택합니다.
2. **Routes** 탭에서 다음 라우트가 있는지 확인합니다:
   - `10.0.0.0/16` → `local`
   - `0.0.0.0/0` → `MyStudyIGW`

3. **Subnet associations** 탭에서 퍼블릭 서브넷들이 연결되어 있는지 확인합니다.

### 7.4 보안 그룹 확인

**Security Groups**에서 생성한 3개의 보안 그룹이 올바른 규칙을 가지고 있는지 확인합니다.

---

## 단계 8: 테스트 (선택사항)

### 8.1 EC2 인스턴스로 연결 테스트

실제 연결을 테스트하려면:

1. 퍼블릭 서브넷에 EC2 인스턴스를 생성합니다.
2. `WebServer-SG` 보안 그룹을 적용합니다.
3. 인터넷에서 인스턴스에 접근할 수 있는지 확인합니다.

**주의**: EC2 인스턴스 생성은 비용이 발생할 수 있으므로, Free Tier 한도를 확인하고 사용 후 즉시 종료하세요.

---

## 실습 완료 후 정리

### 리소스 정리 (비용 절약)

실습 완료 후 다음 순서로 리소스를 정리합니다:

1. **EC2 인스턴스 종료** (생성한 경우)
2. **보안 그룹 삭제** (기본 보안 그룹 제외)
3. **서브넷 삭제**
4. **라우팅 테이블 삭제** (기본 라우팅 테이블 제외)
5. **인터넷 게이트웨이 분리 및 삭제**
6. **VPC 삭제**

### 정리 시 주의사항

- 의존성이 있는 리소스는 순서대로 삭제해야 합니다.
- 기본 보안 그룹과 기본 라우팅 테이블은 삭제할 수 없습니다.
- VPC를 삭제하기 전에 모든 연결된 리소스를 먼저 삭제해야 합니다.

---

## 문제 해결

### 일반적인 문제들

**문제 1**: 서브넷 생성 시 "CIDR block overlaps" 오류
- **해결**: CIDR 블록이 겹치지 않는지 확인하고, VPC CIDR 범위 내에 있는지 확인

**문제 2**: 인터넷 게이트웨이 연결 실패
- **해결**: VPC당 하나의 인터넷 게이트웨이만 연결 가능. 기존 연결을 확인

**문제 3**: 퍼블릭 서브넷에서 인터넷 접근 불가
- **해결**: 
  1. 인터넷 게이트웨이가 VPC에 연결되어 있는지 확인
  2. 라우팅 테이블에 0.0.0.0/0 → IGW 라우트가 있는지 확인
  3. 퍼블릭 IP 자동 할당이 활성화되어 있는지 확인

**문제 4**: 보안 그룹 규칙이 작동하지 않음
- **해결**: 
  1. 인바운드/아웃바운드 규칙을 모두 확인
  2. 소스/대상이 올바르게 설정되어 있는지 확인
  3. 포트 번호가 정확한지 확인

---

## 다음 단계

이번 실습에서 구축한 VPC 인프라를 바탕으로 내일(Day 6)에는 다음과 같은 고급 네트워킹 기능을 학습합니다:

- NAT Gateway 설정 (프라이빗 서브넷의 아웃바운드 인터넷 접근)
- VPC Endpoint 구성 (AWS 서비스에 대한 프라이빗 접근)
- VPC Flow Logs 설정 (네트워크 트래픽 모니터링)

## 실습 체크리스트

완료한 항목에 체크하세요:

- [ ] VPC 생성 (10.0.0.0/16)
- [ ] 인터넷 게이트웨이 생성 및 연결
- [ ] 4개 서브넷 생성 (퍼블릭 2개, 프라이빗 2개)
- [ ] 퍼블릭 IP 자동 할당 설정
- [ ] 퍼블릭 라우팅 테이블 생성 및 구성
- [ ] 서브넷-라우팅 테이블 연결
- [ ] 3개 보안 그룹 생성 (웹서버, 앱서버, 데이터베이스)
- [ ] 구성 검증 완료
- [ ] (선택사항) 리소스 정리 완료

축하합니다! VPC 기초 실습을 성공적으로 완료했습니다. 🎉