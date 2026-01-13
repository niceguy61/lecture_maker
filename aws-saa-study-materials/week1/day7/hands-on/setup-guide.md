# Week 1 종합 실습: 3-Tier 웹 애플리케이션 아키텍처 구축

## 🎯 실습 목표
이번 실습에서는 Week 1에서 학습한 모든 AWS 서비스를 활용하여 실제 운영 환경에서 사용되는 3-Tier 아키텍처를 구축합니다.

### 학습 성과
- VPC 설계 및 구현 능력 향상
- 다중 AZ를 활용한 고가용성 아키텍처 구축
- 보안 그룹과 NACL을 통한 네트워크 보안 구현
- IAM을 통한 최소 권한 원칙 적용

## 📋 사전 준비사항

### 필요한 지식
- VPC 및 서브넷 개념
- EC2 인스턴스 생성 및 관리
- 보안 그룹 설정
- IAM 역할 및 정책

### 예상 소요 시간
- **총 소요 시간**: 2-3시간
- **단계별 시간**: 각 단계당 20-30분

### 비용 안내
- 이 실습은 AWS Free Tier 범위 내에서 진행됩니다
- 실습 완료 후 리소스를 삭제하면 추가 비용이 발생하지 않습니다

## 🏗️ 아키텍처 개요

우리가 구축할 3-Tier 아키텍처는 다음과 같습니다:

```
Internet Gateway
       |
   [Web Tier]     - Public Subnet (Multi-AZ)
       |
   [App Tier]     - Private Subnet (Multi-AZ)  
       |
   [DB Tier]      - Private Subnet (Multi-AZ)
```

### 아키텍처 구성 요소

**1. Presentation Tier (Web Tier)**
- 퍼블릭 서브넷에 배치
- 웹 서버 (Apache/Nginx)
- 인터넷에서 직접 접근 가능

**2. Application Tier (App Tier)**
- 프라이빗 서브넷에 배치
- 애플리케이션 로직 처리
- NAT Gateway를 통해 인터넷 접근

**3. Data Tier (DB Tier)**
- 프라이빗 서브넷에 배치
- 데이터베이스 서버
- 외부 인터넷 접근 불가

## 🚀 단계별 구축 가이드

### Step 1: VPC 및 기본 네트워크 구성

#### 1.1 VPC 생성
1. **AWS Console 접속**
   - VPC 서비스로 이동
   - "Create VPC" 클릭

2. **VPC 설정**
   ```
   Name tag: MyApp-VPC
   IPv4 CIDR block: 10.0.0.0/16
   IPv6 CIDR block: No IPv6 CIDR block
   Tenancy: Default
   ```

3. **생성 확인**
   - VPC가 성공적으로 생성되었는지 확인
   - VPC ID를 메모해 둡니다

#### 1.2 인터넷 게이트웨이 생성 및 연결
1. **인터넷 게이트웨이 생성**
   - 좌측 메뉴에서 "Internet Gateways" 선택
   - "Create internet gateway" 클릭
   - Name tag: `MyApp-IGW`

2. **VPC에 연결**
   - 생성된 IGW 선택
   - "Actions" → "Attach to VPC"
   - 앞서 생성한 VPC 선택

### Step 2: 서브넷 생성 (Multi-AZ 구성)

#### 2.1 퍼블릭 서브넷 생성 (Web Tier)
1. **첫 번째 퍼블릭 서브넷**
   ```
   Name tag: MyApp-Public-Subnet-1A
   VPC: MyApp-VPC
   Availability Zone: us-east-1a (또는 사용 가능한 첫 번째 AZ)
   IPv4 CIDR block: 10.0.1.0/24
   ```

2. **두 번째 퍼블릭 서브넷**
   ```
   Name tag: MyApp-Public-Subnet-1B
   VPC: MyApp-VPC
   Availability Zone: us-east-1b (또는 사용 가능한 두 번째 AZ)
   IPv4 CIDR block: 10.0.2.0/24
   ```

#### 2.2 프라이빗 서브넷 생성 (App Tier)
1. **첫 번째 앱 서브넷**
   ```
   Name tag: MyApp-Private-App-Subnet-1A
   VPC: MyApp-VPC
   Availability Zone: us-east-1a
   IPv4 CIDR block: 10.0.11.0/24
   ```

2. **두 번째 앱 서브넷**
   ```
   Name tag: MyApp-Private-App-Subnet-1B
   VPC: MyApp-VPC
   Availability Zone: us-east-1b
   IPv4 CIDR block: 10.0.12.0/24
   ```

#### 2.3 프라이빗 서브넷 생성 (DB Tier)
1. **첫 번째 DB 서브넷**
   ```
   Name tag: MyApp-Private-DB-Subnet-1A
   VPC: MyApp-VPC
   Availability Zone: us-east-1a
   IPv4 CIDR block: 10.0.21.0/24
   ```

2. **두 번째 DB 서브넷**
   ```
   Name tag: MyApp-Private-DB-Subnet-1B
   VPC: MyApp-VPC
   Availability Zone: us-east-1b
   IPv4 CIDR block: 10.0.22.0/24
   ```

### Step 3: NAT Gateway 구성

#### 3.1 Elastic IP 할당
1. **Elastic IP 생성**
   - 좌측 메뉴에서 "Elastic IPs" 선택
   - "Allocate Elastic IP address" 클릭
   - "Allocate" 클릭

#### 3.2 NAT Gateway 생성
1. **NAT Gateway 설정**
   ```
   Name: MyApp-NAT-Gateway-1A
   Subnet: MyApp-Public-Subnet-1A
   Connectivity type: Public
   Elastic IP allocation ID: 앞서 생성한 EIP 선택
   ```

### Step 4: 라우팅 테이블 구성

#### 4.1 퍼블릭 라우팅 테이블
1. **라우팅 테이블 생성**
   ```
   Name tag: MyApp-Public-RT
   VPC: MyApp-VPC
   ```

2. **라우팅 규칙 추가**
   - "Routes" 탭 선택
   - "Edit routes" 클릭
   - "Add route" 클릭
   ```
   Destination: 0.0.0.0/0
   Target: Internet Gateway (MyApp-IGW)
   ```

3. **서브넷 연결**
   - "Subnet associations" 탭 선택
   - "Edit subnet associations" 클릭
   - 두 개의 퍼블릭 서브넷 선택

#### 4.2 프라이빗 라우팅 테이블 (App Tier)
1. **라우팅 테이블 생성**
   ```
   Name tag: MyApp-Private-App-RT
   VPC: MyApp-VPC
   ```

2. **라우팅 규칙 추가**
   ```
   Destination: 0.0.0.0/0
   Target: NAT Gateway (MyApp-NAT-Gateway-1A)
   ```

3. **서브넷 연결**
   - 두 개의 App Tier 프라이빗 서브넷 연결

#### 4.3 프라이빗 라우팅 테이블 (DB Tier)
1. **라우팅 테이블 생성**
   ```
   Name tag: MyApp-Private-DB-RT
   VPC: MyApp-VPC
   ```

2. **서브넷 연결**
   - 두 개의 DB Tier 프라이빗 서브넷 연결
   - 인터넷 라우팅 규칙은 추가하지 않음 (완전 격리)

### Step 5: 보안 그룹 생성

#### 5.1 웹 서버 보안 그룹
1. **보안 그룹 생성**
   ```
   Security group name: MyApp-Web-SG
   Description: Security group for web servers
   VPC: MyApp-VPC
   ```

2. **인바운드 규칙**
   ```
   Type: HTTP, Port: 80, Source: 0.0.0.0/0
   Type: HTTPS, Port: 443, Source: 0.0.0.0/0
   Type: SSH, Port: 22, Source: Your IP
   ```

#### 5.2 애플리케이션 서버 보안 그룹
1. **보안 그룹 생성**
   ```
   Security group name: MyApp-App-SG
   Description: Security group for application servers
   VPC: MyApp-VPC
   ```

2. **인바운드 규칙**
   ```
   Type: Custom TCP, Port: 8080, Source: MyApp-Web-SG
   Type: SSH, Port: 22, Source: MyApp-Web-SG
   ```

#### 5.3 데이터베이스 보안 그룹
1. **보안 그룹 생성**
   ```
   Security group name: MyApp-DB-SG
   Description: Security group for database servers
   VPC: MyApp-VPC
   ```

2. **인바운드 규칙**
   ```
   Type: MySQL/Aurora, Port: 3306, Source: MyApp-App-SG
   Type: SSH, Port: 22, Source: MyApp-App-SG
   ```

### Step 6: IAM 역할 생성

#### 6.1 EC2 인스턴스용 IAM 역할
1. **역할 생성**
   - IAM 서비스로 이동
   - "Roles" → "Create role"
   - Trusted entity type: AWS service
   - Use case: EC2

2. **정책 연결**
   ```
   AmazonSSMManagedInstanceCore (Systems Manager 접근용)
   CloudWatchAgentServerPolicy (모니터링용)
   ```

3. **역할 이름**
   ```
   Role name: MyApp-EC2-Role
   ```

### Step 7: EC2 인스턴스 배포

#### 7.1 웹 서버 인스턴스 (Web Tier)
1. **인스턴스 설정**
   ```
   Name: MyApp-Web-Server-1A
   AMI: Amazon Linux 2023
   Instance type: t2.micro
   Key pair: 기존 키 페어 또는 새로 생성
   ```

2. **네트워크 설정**
   ```
   VPC: MyApp-VPC
   Subnet: MyApp-Public-Subnet-1A
   Auto-assign public IP: Enable
   Security groups: MyApp-Web-SG
   ```

3. **고급 설정**
   ```
   IAM instance profile: MyApp-EC2-Role
   ```

4. **User Data 스크립트**
   ```bash
   #!/bin/bash
   yum update -y
   yum install -y httpd
   systemctl start httpd
   systemctl enable httpd
   echo "<h1>Web Tier - Server 1A</h1>" > /var/www/html/index.html
   echo "<p>This is the presentation tier of our 3-tier architecture</p>" >> /var/www/html/index.html
   ```

#### 7.2 애플리케이션 서버 인스턴스 (App Tier)
1. **인스턴스 설정**
   ```
   Name: MyApp-App-Server-1A
   AMI: Amazon Linux 2023
   Instance type: t2.micro
   Key pair: 동일한 키 페어 사용
   ```

2. **네트워크 설정**
   ```
   VPC: MyApp-VPC
   Subnet: MyApp-Private-App-Subnet-1A
   Auto-assign public IP: Disable
   Security groups: MyApp-App-SG
   ```

3. **User Data 스크립트**
   ```bash
   #!/bin/bash
   yum update -y
   yum install -y java-11-amazon-corretto
   echo "Application Tier Server - Ready" > /tmp/app-status.txt
   ```

#### 7.3 데이터베이스 서버 인스턴스 (DB Tier)
1. **인스턴스 설정**
   ```
   Name: MyApp-DB-Server-1A
   AMI: Amazon Linux 2023
   Instance type: t2.micro
   Key pair: 동일한 키 페어 사용
   ```

2. **네트워크 설정**
   ```
   VPC: MyApp-VPC
   Subnet: MyApp-Private-DB-Subnet-1A
   Auto-assign public IP: Disable
   Security groups: MyApp-DB-SG
   ```

3. **User Data 스크립트**
   ```bash
   #!/bin/bash
   yum update -y
   yum install -y mariadb-server
   systemctl start mariadb
   systemctl enable mariadb
   echo "Database Tier Server - Ready" > /tmp/db-status.txt
   ```

### Step 8: 연결성 테스트

#### 8.1 웹 서버 접근 테스트
1. **퍼블릭 IP 확인**
   - EC2 콘솔에서 웹 서버의 퍼블릭 IP 확인

2. **웹 브라우저 테스트**
   - `http://[웹서버-퍼블릭-IP]`로 접속
   - "Web Tier - Server 1A" 메시지 확인

#### 8.2 내부 연결성 테스트
1. **웹 서버에 SSH 접속**
   ```bash
   ssh -i your-key.pem ec2-user@[웹서버-퍼블릭-IP]
   ```

2. **앱 서버 연결 테스트**
   ```bash
   ping [앱서버-프라이빗-IP]
   ssh ec2-user@[앱서버-프라이빗-IP]
   ```

3. **앱 서버에서 DB 서버 연결 테스트**
   ```bash
   ping [DB서버-프라이빗-IP]
   ssh ec2-user@[DB서버-프라이빗-IP]
   ```

## 🔍 아키텍처 검증

### 보안 검증
1. **외부에서 직접 접근 불가 확인**
   - 앱 서버와 DB 서버에 인터넷에서 직접 접근 시도
   - 접근이 차단되는지 확인

2. **보안 그룹 규칙 검증**
   - 각 티어 간 필요한 포트만 개방되어 있는지 확인
   - 불필요한 포트가 열려있지 않은지 점검

### 네트워크 검증
1. **라우팅 확인**
   - 각 서브넷의 라우팅 테이블 설정 확인
   - 트래픽이 의도한 경로로 흐르는지 검증

2. **NAT Gateway 동작 확인**
   - 앱 서버에서 인터넷 접근 가능한지 테스트
   ```bash
   curl -I http://www.google.com
   ```

## 🎉 실습 완료 체크리스트

### 인프라 구성 완료
- [ ] VPC 생성 및 CIDR 블록 설정
- [ ] 6개 서브넷 생성 (퍼블릭 2개, 프라이빗 4개)
- [ ] 인터넷 게이트웨이 연결
- [ ] NAT Gateway 구성
- [ ] 라우팅 테이블 설정

### 보안 구성 완료
- [ ] 3개 보안 그룹 생성 및 규칙 설정
- [ ] IAM 역할 생성 및 정책 연결
- [ ] 키 페어 생성 및 관리

### 인스턴스 배포 완료
- [ ] 웹 서버 인스턴스 배포 및 테스트
- [ ] 앱 서버 인스턴스 배포 및 연결 확인
- [ ] DB 서버 인스턴스 배포 및 격리 확인

### 연결성 테스트 완료
- [ ] 웹 서버 인터넷 접근 확인
- [ ] 티어 간 내부 통신 확인
- [ ] 보안 규칙 동작 검증

## 🧹 리소스 정리

실습 완료 후 비용 발생을 방지하기 위해 다음 순서로 리소스를 삭제합니다:

### 1. EC2 인스턴스 종료
- 모든 EC2 인스턴스 선택 후 "Terminate"

### 2. NAT Gateway 삭제
- NAT Gateway 선택 후 "Delete"

### 3. Elastic IP 해제
- Elastic IP 선택 후 "Release"

### 4. VPC 삭제
- VPC 선택 후 "Delete VPC"
- 연관된 모든 리소스가 함께 삭제됩니다

## 📚 추가 학습 과제

### 고급 구성 도전
1. **로드 밸런서 추가**
   - Application Load Balancer를 웹 티어 앞에 배치
   - 다중 웹 서버 인스턴스 구성

2. **Auto Scaling 구현**
   - 웹 티어와 앱 티어에 Auto Scaling Group 적용
   - CloudWatch 메트릭 기반 스케일링 정책 설정

3. **데이터베이스 고가용성**
   - RDS Multi-AZ 배포로 DB 티어 업그레이드
   - 읽기 전용 복제본 추가

### 보안 강화
1. **VPC Flow Logs 활성화**
   - 네트워크 트래픽 모니터링
   - CloudWatch Logs와 연동

2. **AWS Systems Manager 활용**
   - Session Manager를 통한 안전한 인스턴스 접근
   - SSH 키 없이 인스턴스 관리

이번 실습을 통해 AWS의 핵심 네트워킹 서비스들을 활용한 실제 운영 환경 수준의 아키텍처를 구축해보았습니다. 이는 Week 2에서 학습할 스토리지와 데이터베이스 서비스의 기반이 됩니다.