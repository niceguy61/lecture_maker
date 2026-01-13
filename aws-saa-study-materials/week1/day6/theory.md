# Day 6: VPC 고급 네트워킹

## 학습 목표
- NAT Gateway와 NAT Instance의 차이점과 사용 사례 이해
- VPC Endpoint의 종류와 활용 방법 학습
- VPC Peering과 Transit Gateway 개념 파악
- 네트워크 보안 그룹과 NACL의 고급 설정 방법 습득
- VPC Flow Logs를 통한 네트워크 트래픽 모니터링 이해

## 1. NAT Gateway vs NAT Instance

### NAT Gateway란?
NAT Gateway는 AWS에서 관리하는 완전 관리형 NAT 서비스입니다. 프라이빗 서브넷의 인스턴스들이 인터넷에 아웃바운드 연결을 할 수 있게 해주면서, 인바운드 연결은 차단합니다.

```mermaid
graph TB
    subgraph "VPC (10.0.0.0/16)"
        subgraph "Public Subnet (10.0.1.0/24)"
            IGW[Internet Gateway]
            NAT[NAT Gateway]
        end
        
        subgraph "Private Subnet (10.0.2.0/24)"
            EC2[EC2 Instance]
        end
        
        RT1[Public Route Table]
        RT2[Private Route Table]
    end
    
    Internet((Internet))
    
    Internet --> IGW
    IGW --> NAT
    NAT --> EC2
    
    RT1 -.-> IGW
    RT2 -.-> NAT
    
    style NAT fill:#ff9999
    style EC2 fill:#99ccff
```

### NAT Gateway vs NAT Instance 비교

| 특징 | NAT Gateway | NAT Instance |
|------|-------------|--------------|
| 관리 | AWS 완전 관리 | 사용자 직접 관리 |
| 가용성 | 자동 고가용성 | 수동 설정 필요 |
| 대역폭 | 최대 45Gbps | 인스턴스 타입에 따라 제한 |
| 보안 그룹 | 지원 안함 | 지원함 |
| 포트 포워딩 | 지원 안함 | 지원함 |
| 비용 | 시간당 + 데이터 처리 비용 | 인스턴스 비용만 |

## 2. VPC Endpoint

### VPC Endpoint란?
VPC Endpoint는 VPC와 AWS 서비스 간의 프라이빗 연결을 제공합니다. 인터넷 게이트웨이, NAT 게이트웨이, VPN 연결 없이도 AWS 서비스에 접근할 수 있습니다.

### VPC Endpoint 종류

#### 1. Gateway Endpoint
S3와 DynamoDB에만 사용 가능한 무료 엔드포인트입니다.

```mermaid
graph LR
    subgraph "VPC"
        EC2[EC2 Instance]
        GWE[Gateway Endpoint]
        RT[Route Table]
    end
    
    S3[(S3 Bucket)]
    DDB[(DynamoDB)]
    
    EC2 --> GWE
    GWE --> S3
    GWE --> DDB
    RT -.-> GWE
    
    style GWE fill:#ffcc99
    style S3 fill:#ff6666
    style DDB fill:#66ff66
```

#### 2. Interface Endpoint (PrivateLink)
대부분의 AWS 서비스에 사용 가능한 ENI 기반 엔드포인트입니다.

```mermaid
graph TB
    subgraph "VPC (10.0.0.0/16)"
        subgraph "Private Subnet"
            EC2[EC2 Instance]
            ENI[Interface Endpoint<br/>ENI]
        end
    end
    
    subgraph "AWS Services"
        EC2SVC[EC2 Service]
        LAMBDA[Lambda Service]
        SNS[SNS Service]
    end
    
    EC2 --> ENI
    ENI --> EC2SVC
    ENI --> LAMBDA
    ENI --> SNS
    
    style ENI fill:#99ff99
    style EC2SVC fill:#ffcc99
    style LAMBDA fill:#ffcc99
    style SNS fill:#ffcc99
```

### VPC Endpoint 사용 사례
- **보안 강화**: 트래픽이 인터넷을 거치지 않음
- **성능 향상**: AWS 백본 네트워크 사용으로 지연 시간 감소
- **비용 절감**: NAT Gateway 데이터 처리 비용 절약

## 3. VPC Peering

### VPC Peering이란?
두 VPC 간의 프라이빗 네트워크 연결을 제공하는 서비스입니다. 같은 리전 또는 다른 리전, 심지어 다른 AWS 계정의 VPC와도 연결 가능합니다.

```mermaid
graph TB
    subgraph "Region A"
        subgraph "VPC A (10.0.0.0/16)"
            EC2A[EC2 Instance A]
        end
    end
    
    subgraph "Region B"
        subgraph "VPC B (10.1.0.0/16)"
            EC2B[EC2 Instance B]
        end
    end
    
    PEER[VPC Peering Connection]
    
    EC2A <--> PEER
    PEER <--> EC2B
    
    style PEER fill:#ff99cc
    style EC2A fill:#99ccff
    style EC2B fill:#99ccff
```

### VPC Peering 제한사항
- **전이적 라우팅 불가**: A-B, B-C가 연결되어도 A-C 직접 통신 불가
- **CIDR 중복 불가**: 연결하려는 VPC의 CIDR 블록이 겹치면 안됨
- **DNS 해상도**: 기본적으로 비활성화됨

## 4. Transit Gateway

### Transit Gateway란?
여러 VPC와 온프레미스 네트워크를 중앙 집중식으로 연결하는 네트워크 허브입니다.

```mermaid
graph TB
    subgraph "AWS Cloud"
        TGW[Transit Gateway]
        
        subgraph "VPC A"
            EC2A[EC2 A]
        end
        
        subgraph "VPC B"
            EC2B[EC2 B]
        end
        
        subgraph "VPC C"
            EC2C[EC2 C]
        end
        
        VPN[VPN Gateway]
        DX[Direct Connect Gateway]
    end
    
    OnPrem[On-Premises Network]
    
    EC2A <--> TGW
    EC2B <--> TGW
    EC2C <--> TGW
    TGW <--> VPN
    TGW <--> DX
    VPN <--> OnPrem
    DX <--> OnPrem
    
    style TGW fill:#ff6666
    style VPN fill:#66ff66
    style DX fill:#6666ff
```

### Transit Gateway 장점
- **확장성**: 최대 5,000개의 VPC 연결 가능
- **전이적 라우팅**: 모든 연결된 네트워크 간 통신 가능
- **중앙 관리**: 단일 지점에서 라우팅 정책 관리
- **멀티캐스트 지원**: 멀티캐스트 트래픽 라우팅 가능

## 5. 네트워크 보안 심화

### Security Groups vs NACLs 비교

```mermaid
graph TB
    subgraph "VPC"
        subgraph "Subnet"
            subgraph "EC2 Instance"
                SG[Security Group<br/>Stateful]
            end
            NACL[Network ACL<br/>Stateless]
        end
    end
    
    Internet((Internet))
    
    Internet --> NACL
    NACL --> SG
    
    style SG fill:#99ff99
    style NACL fill:#ff9999
```

| 특징 | Security Groups | Network ACLs |
|------|-----------------|--------------|
| 적용 레벨 | 인스턴스 레벨 | 서브넷 레벨 |
| 상태 | Stateful | Stateless |
| 규칙 | Allow만 가능 | Allow/Deny 모두 가능 |
| 규칙 평가 | 모든 규칙 평가 | 번호 순서대로 평가 |
| 기본 정책 | 모든 아웃바운드 허용 | 모든 트래픽 허용 |

### 다층 보안 전략

```mermaid
graph TB
    subgraph "Multi-Layer Security"
        subgraph "Layer 1: Network Level"
            NACL1[NACL - Subnet A]
            NACL2[NACL - Subnet B]
        end
        
        subgraph "Layer 2: Instance Level"
            SG1[Security Group - Web Tier]
            SG2[Security Group - App Tier]
            SG3[Security Group - DB Tier]
        end
        
        subgraph "Layer 3: Application Level"
            WAF[AWS WAF]
            SHIELD[AWS Shield]
        end
    end
    
    Internet((Internet)) --> WAF
    WAF --> SHIELD
    SHIELD --> NACL1
    NACL1 --> SG1
    SG1 --> SG2
    SG2 --> SG3
    
    style WAF fill:#ff6666
    style SHIELD fill:#66ff66
    style SG1 fill:#99ccff
    style SG2 fill:#99ccff
    style SG3 fill:#99ccff
```

## 6. VPC Flow Logs

### VPC Flow Logs란?
VPC의 네트워크 인터페이스에서 송수신되는 IP 트래픽에 대한 정보를 캡처하는 기능입니다.

### Flow Logs 레벨
- **VPC 레벨**: 전체 VPC의 모든 트래픽
- **서브넷 레벨**: 특정 서브넷의 트래픽
- **ENI 레벨**: 특정 네트워크 인터페이스의 트래픽

```mermaid
graph TB
    subgraph "VPC Flow Logs Architecture"
        subgraph "VPC"
            subgraph "Subnet A"
                EC2A[EC2 Instance A]
                ENIA[ENI A]
            end
            
            subgraph "Subnet B"
                EC2B[EC2 Instance B]
                ENIB[ENI B]
            end
        end
        
        FLOWLOGS[VPC Flow Logs]
        
        subgraph "Destinations"
            CW[CloudWatch Logs]
            S3[S3 Bucket]
            KINESIS[Kinesis Data Firehose]
        end
    end
    
    ENIA --> FLOWLOGS
    ENIB --> FLOWLOGS
    FLOWLOGS --> CW
    FLOWLOGS --> S3
    FLOWLOGS --> KINESIS
    
    style FLOWLOGS fill:#ffcc99
    style CW fill:#ff6666
    style S3 fill:#66ff66
    style KINESIS fill:#6666ff
```

### Flow Logs 활용 사례
- **보안 분석**: 비정상적인 트래픽 패턴 탐지
- **네트워크 문제 해결**: 연결 실패 원인 분석
- **비용 최적화**: 불필요한 데이터 전송 식별
- **규정 준수**: 네트워크 트래픽 감사

## 7. 실제 아키텍처 예시

### 엔터프라이즈 네트워킹 아키텍처

```mermaid
graph TB
    subgraph "Production VPC (10.0.0.0/16)"
        subgraph "Public Subnets"
            ALB[Application Load Balancer]
            NAT1[NAT Gateway AZ-A]
            NAT2[NAT Gateway AZ-B]
        end
        
        subgraph "Private Subnets"
            WEB1[Web Server AZ-A]
            WEB2[Web Server AZ-B]
            APP1[App Server AZ-A]
            APP2[App Server AZ-B]
        end
        
        subgraph "Database Subnets"
            RDS1[RDS Primary]
            RDS2[RDS Standby]
        end
        
        VPCE[VPC Endpoint for S3]
    end
    
    subgraph "Development VPC (10.1.0.0/16)"
        DEV[Dev Environment]
    end
    
    subgraph "Management VPC (10.2.0.0/16)"
        BASTION[Bastion Host]
        MONITORING[Monitoring Tools]
    end
    
    TGW[Transit Gateway]
    S3[(S3 Bucket)]
    OnPrem[On-Premises]
    
    Internet((Internet)) --> ALB
    ALB --> WEB1
    ALB --> WEB2
    WEB1 --> APP1
    WEB2 --> APP2
    APP1 --> RDS1
    APP2 --> RDS1
    RDS1 --> RDS2
    
    WEB1 --> NAT1
    WEB2 --> NAT2
    APP1 --> VPCE
    APP2 --> VPCE
    VPCE --> S3
    
    TGW <--> DEV
    TGW <--> BASTION
    TGW <--> OnPrem
    
    style TGW fill:#ff6666
    style ALB fill:#99ff99
    style VPCE fill:#ffcc99
    style RDS1 fill:#6666ff
    style RDS2 fill:#6666ff
```

## 8. 네트워킹 모범 사례

### 1. 보안 모범 사례
- **최소 권한 원칙**: 필요한 최소한의 포트와 프로토콜만 허용
- **다층 보안**: NACL과 Security Group을 함께 사용
- **정기적인 검토**: 보안 규칙의 정기적인 감사 및 정리

### 2. 성능 최적화
- **가용 영역 분산**: 고가용성을 위한 다중 AZ 배치
- **VPC Endpoint 활용**: AWS 서비스 접근 시 인터넷 우회
- **적절한 인스턴스 타입**: 네트워크 성능 요구사항에 맞는 선택

### 3. 비용 최적화
- **NAT Gateway 최적화**: 필요한 AZ에만 배치
- **VPC Endpoint 활용**: 데이터 전송 비용 절감
- **Flow Logs 필터링**: 필요한 트래픽만 로깅

## 9. 문제 해결 가이드

### 일반적인 네트워킹 문제들

#### 1. 인터넷 연결 불가
- Route Table 확인
- Internet Gateway 연결 상태 확인
- Security Group 아웃바운드 규칙 확인
- NACL 규칙 확인

#### 2. VPC 간 통신 불가
- VPC Peering 상태 확인
- Route Table에 피어링 경로 추가 확인
- Security Group 규칙 확인
- CIDR 블록 중복 여부 확인

#### 3. VPC Endpoint 연결 실패
- Endpoint 정책 확인
- Route Table 설정 확인
- DNS 설정 확인 (Interface Endpoint의 경우)

## 요약

Day 6에서는 VPC의 고급 네트워킹 기능들을 학습했습니다:

- **NAT Gateway**: 프라이빗 서브넷의 아웃바운드 인터넷 연결
- **VPC Endpoint**: AWS 서비스와의 프라이빗 연결
- **VPC Peering**: VPC 간 프라이빗 네트워크 연결
- **Transit Gateway**: 중앙 집중식 네트워크 허브
- **고급 보안**: Security Groups와 NACLs의 조합
- **VPC Flow Logs**: 네트워크 트래픽 모니터링

이러한 고급 기능들을 적절히 조합하면 확장 가능하고 안전한 클라우드 네트워크 아키텍처를 구축할 수 있습니다.

## 다음 학습 내용
내일(Day 7)은 Week 1의 마지막 날로, 지금까지 학습한 내용을 종합하여 실제 3-tier 아키텍처를 구축하는 실습을 진행할 예정입니다.