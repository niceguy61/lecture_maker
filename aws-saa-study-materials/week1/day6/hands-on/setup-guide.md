# Day 6 실습: NAT Gateway와 VPC Endpoint 설정

## 실습 개요
이번 실습에서는 VPC의 고급 네트워킹 기능인 NAT Gateway와 VPC Endpoint를 직접 설정해보겠습니다. 프라이빗 서브넷의 EC2 인스턴스가 인터넷에 안전하게 접근하고, AWS 서비스와 프라이빗하게 통신하는 방법을 학습합니다.

## 실습 목표
- NAT Gateway를 생성하여 프라이빗 서브넷의 아웃바운드 인터넷 연결 구성
- VPC Endpoint를 설정하여 S3와 프라이빗 연결 구성
- 네트워크 보안 그룹과 라우팅 테이블 고급 설정
- VPC Flow Logs를 활용한 네트워크 트래픽 모니터링

## 사전 준비사항
- AWS 계정 및 Console 접근 권한
- Day 5에서 생성한 VPC 환경 (또는 새로운 VPC 생성)
- 기본적인 VPC 개념 이해

## 예상 소요 시간
약 90분

## 실습 아키텍처

```
Internet Gateway
       |
   Public Subnet (10.0.1.0/24)
       |
   NAT Gateway
       |
   Private Subnet (10.0.2.0/24)
       |
   EC2 Instance -----> VPC Endpoint -----> S3
```

---

## 실습 1: NAT Gateway 설정

### 1.1 VPC 환경 준비

#### Step 1: VPC 생성 (기존 VPC가 없는 경우)
1. **AWS Console**에 로그인
2. **VPC** 서비스로 이동
3. **Create VPC** 클릭
4. 다음 설정으로 VPC 생성:
   - **Name**: `Day6-VPC`
   - **IPv4 CIDR**: `10.0.0.0/16`
   - **IPv6 CIDR**: 없음
   - **Tenancy**: Default

#### Step 2: 서브넷 생성
1. **Subnets** 메뉴 선택
2. **Create subnet** 클릭

**퍼블릭 서브넷 생성:**
- **VPC**: Day6-VPC 선택
- **Subnet name**: `Public-Subnet-1`
- **Availability Zone**: us-east-1a (또는 사용 가능한 첫 번째 AZ)
- **IPv4 CIDR**: `10.0.1.0/24`

**프라이빗 서브넷 생성:**
- **Add new subnet** 클릭
- **Subnet name**: `Private-Subnet-1`
- **Availability Zone**: us-east-1a (퍼블릭 서브넷과 동일)
- **IPv4 CIDR**: `10.0.2.0/24`

3. **Create subnet** 클릭

#### Step 3: Internet Gateway 생성 및 연결
1. **Internet Gateways** 메뉴 선택
2. **Create internet gateway** 클릭
3. **Name**: `Day6-IGW`
4. **Create internet gateway** 클릭
5. 생성된 IGW 선택 후 **Actions** → **Attach to VPC**
6. **VPC**: Day6-VPC 선택 후 **Attach internet gateway**

### 1.2 NAT Gateway 생성

#### Step 1: Elastic IP 할당
1. **EC2** 서비스로 이동
2. 좌측 메뉴에서 **Elastic IPs** 선택
3. **Allocate Elastic IP address** 클릭
4. **Network Border Group**: 기본값 유지
5. **Allocate** 클릭
6. 할당된 EIP 주소를 메모해둡니다

#### Step 2: NAT Gateway 생성
1. **VPC** 서비스로 돌아가기
2. **NAT Gateways** 메뉴 선택
3. **Create NAT gateway** 클릭
4. 다음 설정 입력:
   - **Name**: `Day6-NAT-Gateway`
   - **Subnet**: Public-Subnet-1 선택
   - **Connectivity type**: Public
   - **Elastic IP allocation ID**: 앞서 생성한 EIP 선택
5. **Create NAT gateway** 클릭

> **💡 참고**: NAT Gateway 생성에는 몇 분이 소요됩니다. 상태가 "Available"이 될 때까지 기다려주세요.

### 1.3 라우팅 테이블 설정

#### Step 1: 퍼블릭 라우팅 테이블 설정
1. **Route Tables** 메뉴 선택
2. **Create route table** 클릭
3. **Name**: `Public-Route-Table`
4. **VPC**: Day6-VPC 선택
5. **Create route table** 클릭

6. 생성된 라우팅 테이블 선택
7. **Routes** 탭에서 **Edit routes** 클릭
8. **Add route** 클릭:
   - **Destination**: `0.0.0.0/0`
   - **Target**: Internet Gateway → Day6-IGW 선택
9. **Save changes** 클릭

10. **Subnet associations** 탭에서 **Edit subnet associations** 클릭
11. **Public-Subnet-1** 선택 후 **Save associations** 클릭

#### Step 2: 프라이빗 라우팅 테이블 설정
1. **Create route table** 클릭
2. **Name**: `Private-Route-Table`
3. **VPC**: Day6-VPC 선택
4. **Create route table** 클릭

5. 생성된 라우팅 테이블 선택
6. **Routes** 탭에서 **Edit routes** 클릭
7. **Add route** 클릭:
   - **Destination**: `0.0.0.0/0`
   - **Target**: NAT Gateway → Day6-NAT-Gateway 선택
8. **Save changes** 클릭

9. **Subnet associations** 탭에서 **Edit subnet associations** 클릭
10. **Private-Subnet-1** 선택 후 **Save associations** 클릭

---

## 실습 2: EC2 인스턴스 생성 및 테스트

### 2.1 프라이빗 서브넷에 EC2 인스턴스 생성

#### Step 1: EC2 인스턴스 시작
1. **EC2** 서비스로 이동
2. **Launch Instance** 클릭
3. 다음 설정으로 인스턴스 구성:

**기본 설정:**
- **Name**: `Private-Instance`
- **AMI**: Amazon Linux 2023 (Free tier eligible)
- **Instance type**: t2.micro (Free tier eligible)

**네트워크 설정:**
- **VPC**: Day6-VPC
- **Subnet**: Private-Subnet-1
- **Auto-assign public IP**: Disable
- **Security group**: 새로 생성
  - **Name**: `Private-Instance-SG`
  - **Description**: Security group for private instance
  - **Inbound rules**: SSH (22) from 10.0.0.0/16

**키 페어:**
- 기존 키 페어 선택 또는 새로 생성

4. **Launch instance** 클릭

### 2.2 Bastion Host 생성 (접근용)

#### Step 1: 퍼블릭 서브넷에 Bastion Host 생성
1. **Launch Instance** 클릭
2. 다음 설정으로 구성:
   - **Name**: `Bastion-Host`
   - **AMI**: Amazon Linux 2023
   - **Instance type**: t2.micro
   - **VPC**: Day6-VPC
   - **Subnet**: Public-Subnet-1
   - **Auto-assign public IP**: Enable
   - **Security group**: 새로 생성
     - **Name**: `Bastion-SG`
     - **Inbound rules**: SSH (22) from My IP

3. **Launch instance** 클릭

### 2.3 NAT Gateway 연결 테스트

#### Step 1: Bastion Host를 통해 프라이빗 인스턴스 접근
1. Bastion Host의 퍼블릭 IP 확인
2. 로컬 터미널에서 Bastion Host에 SSH 연결:
```bash
ssh -i your-key.pem ec2-user@<bastion-public-ip>
```

3. Bastion Host에서 프라이빗 인스턴스로 SSH 연결:
```bash
ssh -i your-key.pem ec2-user@<private-instance-private-ip>
```

#### Step 2: 인터넷 연결 테스트
프라이빗 인스턴스에서 다음 명령어 실행:

```bash
# 인터넷 연결 테스트
ping -c 4 8.8.8.8

# 패키지 업데이트 (인터넷 연결 필요)
sudo yum update -y

# 외부 웹사이트 접근 테스트
curl -I https://www.google.com
```

> **✅ 성공 기준**: 모든 명령어가 정상적으로 실행되면 NAT Gateway가 올바르게 설정된 것입니다.

---

## 실습 3: VPC Endpoint 설정

### 3.1 S3 Gateway Endpoint 생성

#### Step 1: S3 버킷 생성 (테스트용)
1. **S3** 서비스로 이동
2. **Create bucket** 클릭
3. **Bucket name**: `day6-vpc-endpoint-test-[random-number]` (고유한 이름)
4. **Region**: VPC와 동일한 리전 선택
5. 나머지 설정은 기본값 유지
6. **Create bucket** 클릭

#### Step 2: Gateway Endpoint 생성
1. **VPC** 서비스로 이동
2. **Endpoints** 메뉴 선택
3. **Create endpoint** 클릭
4. 다음 설정 입력:
   - **Name**: `S3-Gateway-Endpoint`
   - **Service category**: AWS services
   - **Service name**: `com.amazonaws.us-east-1.s3` (리전에 맞게 조정)
   - **VPC**: Day6-VPC 선택
   - **Route tables**: Private-Route-Table 선택
   - **Policy**: Full access (기본값)

5. **Create endpoint** 클릭

### 3.2 Interface Endpoint 생성 (EC2 서비스용)

#### Step 1: Interface Endpoint 생성
1. **Create endpoint** 클릭
2. 다음 설정 입력:
   - **Name**: `EC2-Interface-Endpoint`
   - **Service category**: AWS services
   - **Service name**: `com.amazonaws.us-east-1.ec2`
   - **VPC**: Day6-VPC 선택
   - **Subnets**: Private-Subnet-1 선택
   - **Security groups**: 새로 생성
     - **Name**: `VPC-Endpoint-SG`
     - **Inbound rules**: HTTPS (443) from 10.0.0.0/16
   - **Policy**: Full access

3. **Create endpoint** 클릭

### 3.3 VPC Endpoint 테스트

#### Step 1: S3 Gateway Endpoint 테스트
프라이빗 인스턴스에서 다음 명령어 실행:

```bash
# AWS CLI 설치 (아직 설치되지 않은 경우)
sudo yum install -y aws-cli

# S3 버킷 목록 조회 (VPC Endpoint를 통해 접근)
aws s3 ls

# 테스트 파일 생성 및 업로드
echo "VPC Endpoint Test" > test-file.txt
aws s3 cp test-file.txt s3://your-bucket-name/

# 파일 다운로드 테스트
aws s3 cp s3://your-bucket-name/test-file.txt downloaded-file.txt
cat downloaded-file.txt
```

#### Step 2: Interface Endpoint 테스트
```bash
# EC2 인스턴스 목록 조회 (Interface Endpoint를 통해 접근)
aws ec2 describe-instances --region us-east-1

# VPC 정보 조회
aws ec2 describe-vpcs --region us-east-1
```

#### Step 3: 네트워크 경로 확인
```bash
# S3 엔드포인트로의 경로 추적
traceroute s3.amazonaws.com

# EC2 엔드포인트로의 경로 추적  
traceroute ec2.us-east-1.amazonaws.com
```

---

## 실습 4: VPC Flow Logs 설정

### 4.1 CloudWatch Logs 그룹 생성

#### Step 1: CloudWatch Logs 그룹 생성
1. **CloudWatch** 서비스로 이동
2. 좌측 메뉴에서 **Logs** → **Log groups** 선택
3. **Create log group** 클릭
4. **Log group name**: `VPC-Flow-Logs`
5. **Retention setting**: 1 week
6. **Create** 클릭

### 4.2 IAM 역할 생성

#### Step 1: Flow Logs용 IAM 역할 생성
1. **IAM** 서비스로 이동
2. **Roles** 메뉴 선택
3. **Create role** 클릭
4. **Trusted entity type**: AWS service
5. **Service**: VPC Flow Logs
6. **Next** 클릭
7. **Role name**: `VPC-Flow-Logs-Role`
8. **Create role** 클릭

### 4.3 VPC Flow Logs 활성화

#### Step 1: Flow Logs 생성
1. **VPC** 서비스로 이동
2. **Your VPCs** 메뉴 선택
3. Day6-VPC 선택
4. **Actions** → **Create flow log** 클릭
5. 다음 설정 입력:
   - **Name**: `Day6-VPC-Flow-Logs`
   - **Filter**: All
   - **Maximum aggregation interval**: 1 minute
   - **Destination**: Send to CloudWatch Logs
   - **Destination log group**: VPC-Flow-Logs
   - **IAM role**: VPC-Flow-Logs-Role

6. **Create flow log** 클릭

### 4.4 Flow Logs 모니터링

#### Step 1: 트래픽 생성 및 로그 확인
1. 프라이빗 인스턴스에서 몇 가지 네트워크 활동 수행:
```bash
# 다양한 네트워크 트래픽 생성
ping -c 10 8.8.8.8
curl -I https://www.amazon.com
aws s3 ls
```

2. **CloudWatch** → **Logs** → **Log groups** → **VPC-Flow-Logs** 이동
3. 로그 스트림 선택하여 Flow Logs 데이터 확인

#### Step 2: Flow Logs 데이터 분석
Flow Logs 레코드 형식 이해:
```
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes windowstart windowend action flowlogstatus
```

예시 레코드:
```
2 123456789012 eni-1235b8ca 172.31.16.139 172.31.16.21 20641 22 6 20 4249 1418530010 1418530070 ACCEPT OK
```

---

## 실습 5: 네트워크 보안 강화

### 5.1 Security Groups 고급 설정

#### Step 1: 웹 서버용 Security Group 생성
1. **EC2** → **Security Groups** 이동
2. **Create security group** 클릭
3. 다음 설정 입력:
   - **Name**: `Web-Server-SG`
   - **Description**: Security group for web servers
   - **VPC**: Day6-VPC

**Inbound rules:**
- HTTP (80) from 0.0.0.0/0
- HTTPS (443) from 0.0.0.0/0
- SSH (22) from Bastion-SG

**Outbound rules:**
- All traffic to 0.0.0.0/0 (기본값)

#### Step 2: 데이터베이스용 Security Group 생성
1. **Create security group** 클릭
2. 다음 설정 입력:
   - **Name**: `Database-SG`
   - **Description**: Security group for database servers
   - **VPC**: Day6-VPC

**Inbound rules:**
- MySQL/Aurora (3306) from Web-Server-SG
- PostgreSQL (5432) from Web-Server-SG

### 5.2 Network ACLs 설정

#### Step 1: 커스텀 Network ACL 생성
1. **VPC** → **Network ACLs** 이동
2. **Create network ACL** 클릭
3. **Name**: `Private-Subnet-NACL`
4. **VPC**: Day6-VPC 선택
5. **Create network ACL** 클릭

#### Step 2: NACL 규칙 설정
**Inbound rules:**
1. **Edit inbound rules** 클릭
2. 다음 규칙 추가:
   - Rule 100: HTTP (80) from 0.0.0.0/0 - ALLOW
   - Rule 110: HTTPS (443) from 0.0.0.0/0 - ALLOW
   - Rule 120: SSH (22) from 10.0.1.0/24 - ALLOW
   - Rule 130: Custom TCP (1024-65535) from 0.0.0.0/0 - ALLOW (임시 포트)

**Outbound rules:**
1. **Edit outbound rules** 클릭
2. 다음 규칙 추가:
   - Rule 100: HTTP (80) to 0.0.0.0/0 - ALLOW
   - Rule 110: HTTPS (443) to 0.0.0.0/0 - ALLOW
   - Rule 120: Custom TCP (1024-65535) to 0.0.0.0/0 - ALLOW

#### Step 3: 서브넷에 NACL 연결
1. **Subnet associations** 탭 선택
2. **Edit subnet associations** 클릭
3. **Private-Subnet-1** 선택
4. **Save changes** 클릭

---

## 실습 6: 성능 및 비용 최적화

### 6.1 VPC Endpoint 정책 최적화

#### Step 1: S3 Endpoint 정책 수정
1. **VPC** → **Endpoints** 이동
2. S3-Gateway-Endpoint 선택
3. **Policy** 탭에서 **Edit policy** 클릭
4. 다음 정책으로 수정:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::day6-vpc-endpoint-test-*",
        "arn:aws:s3:::day6-vpc-endpoint-test-*/*"
      ]
    }
  ]
}
```

5. **Save changes** 클릭

### 6.2 비용 모니터링 설정

#### Step 1: Cost Explorer에서 VPC 비용 확인
1. **AWS Cost Management** → **Cost Explorer** 이동
2. **Create report** 클릭
3. **Service** 필터에서 "Amazon Virtual Private Cloud" 선택
4. 지난 30일간의 VPC 관련 비용 확인

#### Step 2: 예산 알림 설정
1. **AWS Budgets** 이동
2. **Create budget** 클릭
3. **Cost budget** 선택
4. 월 $10 예산으로 VPC 서비스 모니터링 설정

---

## 검증 및 테스트

### 최종 검증 체크리스트

#### ✅ NAT Gateway 검증
- [ ] 프라이빗 인스턴스에서 인터넷 접근 가능
- [ ] 외부에서 프라이빗 인스턴스로 직접 접근 불가
- [ ] NAT Gateway 상태가 "Available"

#### ✅ VPC Endpoint 검증
- [ ] S3 Gateway Endpoint를 통한 S3 접근 가능
- [ ] Interface Endpoint를 통한 EC2 API 접근 가능
- [ ] VPC Endpoint 정책이 올바르게 적용됨

#### ✅ 보안 검증
- [ ] Security Groups 규칙이 올바르게 설정됨
- [ ] Network ACLs가 적절히 구성됨
- [ ] 불필요한 포트가 차단됨

#### ✅ 모니터링 검증
- [ ] VPC Flow Logs가 정상적으로 수집됨
- [ ] CloudWatch에서 로그 데이터 확인 가능
- [ ] 네트워크 트래픽 패턴 분석 가능

---

## 문제 해결 가이드

### 일반적인 문제들

#### 1. NAT Gateway 연결 실패
**증상**: 프라이빗 인스턴스에서 인터넷 접근 불가

**해결 방법**:
- NAT Gateway 상태 확인 (Available인지)
- 프라이빗 라우팅 테이블에 0.0.0.0/0 → NAT Gateway 경로 확인
- Security Group 아웃바운드 규칙 확인
- Elastic IP가 NAT Gateway에 올바르게 할당되었는지 확인

#### 2. VPC Endpoint 접근 실패
**증상**: AWS 서비스 접근 시 타임아웃 또는 연결 거부

**해결 방법**:
- VPC Endpoint 상태 확인
- 라우팅 테이블에 Endpoint 경로 확인
- Security Group에서 HTTPS (443) 포트 허용 확인
- VPC Endpoint 정책 확인

#### 3. Flow Logs 데이터 없음
**증상**: CloudWatch에서 Flow Logs 데이터가 보이지 않음

**해결 방법**:
- IAM 역할 권한 확인
- Flow Logs 상태 확인 (Active인지)
- CloudWatch Logs 그룹 이름 확인
- 네트워크 트래픽이 실제로 발생했는지 확인

---

## 정리 및 리소스 삭제

### 실습 완료 후 정리 작업

#### 중요: 비용 절약을 위한 리소스 정리
실습 완료 후 다음 순서로 리소스를 삭제하세요:

1. **EC2 인스턴스 종료**
   - Private-Instance 종료
   - Bastion-Host 종료

2. **VPC Endpoint 삭제**
   - S3-Gateway-Endpoint 삭제
   - EC2-Interface-Endpoint 삭제

3. **NAT Gateway 삭제**
   - Day6-NAT-Gateway 삭제
   - Elastic IP 릴리스

4. **VPC Flow Logs 삭제**
   - Flow Logs 삭제
   - CloudWatch Logs 그룹 삭제

5. **네트워크 리소스 삭제**
   - 라우팅 테이블 삭제 (기본 테이블 제외)
   - 서브넷 삭제
   - Internet Gateway 분리 및 삭제
   - VPC 삭제

6. **S3 버킷 삭제**
   - 버킷 내 모든 객체 삭제
   - 버킷 삭제

---

## 실습 요약

이번 실습에서 학습한 내용:

### 🎯 주요 성과
- **NAT Gateway**: 프라이빗 서브넷의 안전한 아웃바운드 인터넷 연결 구성
- **VPC Endpoint**: AWS 서비스와의 프라이빗 연결로 보안 및 성능 향상
- **고급 보안**: Security Groups와 NACLs를 활용한 다층 보안 구현
- **모니터링**: VPC Flow Logs를 통한 네트워크 트래픽 가시성 확보

### 🔧 실무 적용 포인트
- 프로덕션 환경에서의 네트워크 보안 강화 방법
- AWS 서비스 간 프라이빗 통신을 통한 비용 최적화
- 네트워크 트래픽 모니터링 및 분석 기법
- 확장 가능한 네트워크 아키텍처 설계 원칙

### 📚 다음 단계
내일(Day 7)은 Week 1의 마지막 날로, 지금까지 학습한 모든 내용을 종합하여 실제 3-tier 웹 애플리케이션 아키텍처를 구축하는 종합 실습을 진행할 예정입니다.

---

## 추가 학습 자료

### 📖 참고 문서
- [AWS NAT Gateway 사용 설명서](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [AWS VPC Endpoints 가이드](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html)
- [VPC Flow Logs 사용 설명서](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)

### 🎥 추천 동영상
- AWS re:Invent - Advanced VPC Networking
- AWS Well-Architected Framework - Security Pillar

### 🛠️ 실습 도구
- AWS CLI 명령어 참조
- VPC 아키텍처 다이어그램 도구
- 네트워크 트러블슈팅 가이드