# EC2 아키텍처 시각화 자료

## 1. EC2 전체 아키텍처 개요

```mermaid
graph TB
    subgraph "AWS Cloud"
        subgraph "Region: us-east-1"
            subgraph "Availability Zone A"
                subgraph "VPC"
                    subgraph "Public Subnet"
                        EC2A[EC2 Instance A<br/>Web Server]
                        SGA[Security Group A<br/>HTTP/HTTPS/SSH]
                    end
                    subgraph "Private Subnet"
                        EC2B[EC2 Instance B<br/>Database Server]
                        SGB[Security Group B<br/>MySQL/SSH]
                    end
                end
            end
            
            subgraph "Availability Zone B"
                subgraph "VPC2"
                    subgraph "Public Subnet 2"
                        EC2C[EC2 Instance C<br/>Web Server]
                        SGC[Security Group C<br/>HTTP/HTTPS/SSH]
                    end
                end
            end
        end
        
        subgraph "AWS Services"
            AMI[AMI Repository<br/>Amazon Machine Images]
            EBS[EBS Volumes<br/>Persistent Storage]
            CW[CloudWatch<br/>Monitoring]
        end
    end
    
    subgraph "Internet"
        USER[Users]
        ADMIN[Administrator]
    end
    
    USER --> EC2A
    USER --> EC2C
    ADMIN --> EC2A
    ADMIN --> EC2B
    ADMIN --> EC2C
    
    EC2A --> EC2B
    EC2A --> EBS
    EC2B --> EBS
    EC2C --> EBS
    
    AMI --> EC2A
    AMI --> EC2B
    AMI --> EC2C
    
    EC2A --> CW
    EC2B --> CW
    EC2C --> CW
    
    style EC2A fill:#e1f5fe
    style EC2B fill:#f3e5f5
    style EC2C fill:#e1f5fe
    style AMI fill:#fff3e0
    style EBS fill:#e8f5e8
    style CW fill:#fce4ec
```

## 2. EC2 인스턴스 구성 요소

```mermaid
graph LR
    subgraph "EC2 Instance"
        subgraph "Compute"
            CPU[vCPU<br/>Virtual Processors]
            MEM[Memory<br/>RAM]
            NET[Network<br/>Performance]
        end
        
        subgraph "Storage"
            ROOT[Root Volume<br/>EBS/Instance Store]
            ADD[Additional Volumes<br/>EBS]
        end
        
        subgraph "Network"
            ENI[Elastic Network Interface]
            PIP[Public IP<br/>Dynamic/Elastic]
            PRIP[Private IP<br/>VPC Internal]
        end
        
        subgraph "Security"
            SG[Security Groups<br/>Virtual Firewall]
            KP[Key Pairs<br/>SSH/RDP Access]
        end
    end
    
    subgraph "Instance Type"
        FAMILY[Instance Family<br/>t3, m5, c5, r5, etc.]
        SIZE[Instance Size<br/>nano, micro, small, large, etc.]
    end
    
    FAMILY --> CPU
    FAMILY --> MEM
    FAMILY --> NET
    SIZE --> CPU
    SIZE --> MEM
    
    style CPU fill:#ffcdd2
    style MEM fill:#c8e6c9
    style NET fill:#bbdefb
    style ROOT fill:#fff9c4
    style SG fill:#f8bbd9
```

## 3. 인스턴스 타입 패밀리 비교

```mermaid
graph TD
    subgraph "Instance Type Families"
        subgraph "General Purpose"
            T3[t3 Family<br/>Burstable Performance<br/>웹 서버, 소규모 DB]
            M5[m5 Family<br/>Balanced Compute<br/>웹 애플리케이션, 마이크로서비스]
        end
        
        subgraph "Compute Optimized"
            C5[c5 Family<br/>High Performance CPU<br/>과학 계산, 게임 서버]
        end
        
        subgraph "Memory Optimized"
            R5[r5 Family<br/>Memory Intensive<br/>인메모리 DB, 빅데이터]
            X1[x1 Family<br/>High Memory<br/>Apache Spark, 대용량 DB]
        end
        
        subgraph "Storage Optimized"
            I3[i3 Family<br/>High Sequential R/W<br/>분산 파일시스템, 데이터웨어하우스]
        end
        
        subgraph "Accelerated Computing"
            P3[p3 Family<br/>GPU Instances<br/>머신러닝, HPC]
        end
    end
    
    subgraph "Use Cases"
        WEB[Web Applications]
        DB[Databases]
        ML[Machine Learning]
        GAME[Gaming]
        ANALYTICS[Analytics]
    end
    
    T3 --> WEB
    M5 --> WEB
    C5 --> GAME
    R5 --> DB
    X1 --> DB
    I3 --> ANALYTICS
    P3 --> ML
    
    style T3 fill:#e3f2fd
    style M5 fill:#e8f5e8
    style C5 fill:#fff3e0
    style R5 fill:#fce4ec
    style X1 fill:#f3e5f5
    style I3 fill:#e0f2f1
    style P3 fill:#fff8e1
```

## 4. EC2 인스턴스 생명주기

```mermaid
stateDiagram-v2
    [*] --> Pending : Launch Instance
    Pending --> Running : Boot Complete
    Running --> Stopping : Stop Instance
    Stopping --> Stopped : Stop Complete
    Stopped --> Pending : Start Instance
    Running --> Rebooting : Reboot Instance
    Rebooting --> Running : Reboot Complete
    Running --> ShuttingDown : Terminate Instance
    Stopped --> ShuttingDown : Terminate Instance
    ShuttingDown --> Terminated : Termination Complete
    Terminated --> [*]
    
    note right of Pending
        인스턴스 시작 중
        하드웨어 할당
        부팅 프로세스
    end note
    
    note right of Running
        정상 실행 상태
        애플리케이션 서비스
        과금 진행 중
    end note
    
    note right of Stopped
        인스턴스 중지
        EBS 데이터 보존
        과금 중지 (EBS 제외)
    end note
    
    note right of Terminated
        완전 삭제
        모든 데이터 손실
        복구 불가능
    end note
```

## 5. 보안 그룹 아키텍처

```mermaid
graph TB
    subgraph "Internet"
        USER[Internet Users]
        ADMIN[System Admin]
    end
    
    subgraph "VPC"
        subgraph "Public Subnet"
            subgraph "Web Server"
                WEB[EC2 Web Instance]
                WEBSG[Web Security Group]
            end
        end
        
        subgraph "Private Subnet"
            subgraph "Database Server"
                DB[EC2 DB Instance]
                DBSG[DB Security Group]
            end
        end
    end
    
    USER -->|HTTP:80<br/>HTTPS:443| WEBSG
    ADMIN -->|SSH:22<br/>Source: Admin IP| WEBSG
    WEBSG --> WEB
    
    WEB -->|MySQL:3306<br/>Source: Web SG| DBSG
    ADMIN -->|SSH:22<br/>Source: Admin IP| DBSG
    DBSG --> DB
    
    subgraph "Security Group Rules"
        subgraph "Web SG Rules"
            WEBIN[Inbound Rules:<br/>HTTP: 0.0.0.0/0<br/>HTTPS: 0.0.0.0/0<br/>SSH: Admin IP]
            WEBOUT[Outbound Rules:<br/>All Traffic: 0.0.0.0/0]
        end
        
        subgraph "DB SG Rules"
            DBIN[Inbound Rules:<br/>MySQL: Web SG<br/>SSH: Admin IP]
            DBOUT[Outbound Rules:<br/>All Traffic: 0.0.0.0/0]
        end
    end
    
    style WEBSG fill:#e3f2fd
    style DBSG fill:#fce4ec
    style WEBIN fill:#e8f5e8
    style DBIN fill:#fff3e0
```

## 6. AMI (Amazon Machine Image) 구조

```mermaid
graph TD
    subgraph "AMI Components"
        subgraph "Root Volume Template"
            OS[Operating System<br/>Linux/Windows]
            APP[Pre-installed Applications<br/>Web Server, Database, etc.]
            CONFIG[System Configuration<br/>Users, Settings, etc.]
        end
        
        subgraph "Block Device Mapping"
            ROOT_MAP[Root Device Mapping<br/>/dev/sda1 or /dev/xvda]
            ADD_MAP[Additional Volume Mapping<br/>/dev/sdb, /dev/sdc, etc.]
        end
        
        subgraph "Permissions"
            OWNER[Owner Permissions<br/>Private/Public/Shared]
            LAUNCH[Launch Permissions<br/>Specific AWS Accounts]
        end
    end
    
    subgraph "AMI Types"
        subgraph "By Root Device"
            EBS_AMI[EBS-backed AMI<br/>Persistent Storage<br/>Fast Boot]
            STORE_AMI[Instance Store AMI<br/>Temporary Storage<br/>Lower Cost]
        end
        
        subgraph "By Source"
            AWS_AMI[AWS Provided<br/>Amazon Linux, Ubuntu]
            MARKET_AMI[AWS Marketplace<br/>Commercial Software]
            COMMUNITY_AMI[Community AMI<br/>User Shared]
            CUSTOM_AMI[Custom AMI<br/>User Created]
        end
    end
    
    subgraph "Instance Launch"
        LAUNCH_INST[Launch Instance]
        SELECT_AMI[Select AMI]
        BOOT[Boot Process]
        RUNNING[Running Instance]
    end
    
    OS --> EBS_AMI
    APP --> EBS_AMI
    CONFIG --> EBS_AMI
    
    EBS_AMI --> SELECT_AMI
    AWS_AMI --> SELECT_AMI
    MARKET_AMI --> SELECT_AMI
    CUSTOM_AMI --> SELECT_AMI
    
    SELECT_AMI --> LAUNCH_INST
    LAUNCH_INST --> BOOT
    BOOT --> RUNNING
    
    style EBS_AMI fill:#e3f2fd
    style AWS_AMI fill:#e8f5e8
    style CUSTOM_AMI fill:#fff3e0
```

## 7. EC2 스토리지 옵션

```mermaid
graph TB
    subgraph "EC2 Instance"
        INST[EC2 Instance]
    end
    
    subgraph "Storage Options"
        subgraph "Instance Store"
            TEMP[Temporary Storage<br/>물리적으로 연결<br/>높은 I/O 성능<br/>인스턴스 종료시 삭제]
        end
        
        subgraph "EBS (Elastic Block Store)"
            GP3[gp3: General Purpose SSD<br/>3,000-16,000 IOPS<br/>125-1,000 MB/s]
            GP2[gp2: General Purpose SSD<br/>Baseline 3 IOPS/GB<br/>Burst up to 3,000 IOPS]
            IO2[io2: Provisioned IOPS SSD<br/>Up to 64,000 IOPS<br/>High durability]
            ST1[st1: Throughput Optimized HDD<br/>500 IOPS<br/>500 MB/s throughput]
            SC1[sc1: Cold HDD<br/>250 IOPS<br/>250 MB/s throughput]
        end
        
        subgraph "EFS (Elastic File System)"
            EFS[Network File System<br/>다중 인스턴스 공유<br/>자동 확장]
        end
    end
    
    INST -.->|직접 연결| TEMP
    INST -->|네트워크 연결| GP3
    INST -->|네트워크 연결| GP2
    INST -->|네트워크 연결| IO2
    INST -->|네트워크 연결| ST1
    INST -->|네트워크 연결| SC1
    INST -->|NFS 마운트| EFS
    
    subgraph "Use Cases"
        WEB_USE[웹 애플리케이션<br/>→ gp3/gp2]
        DB_USE[고성능 데이터베이스<br/>→ io2]
        BIG_DATA[빅데이터 처리<br/>→ st1]
        ARCHIVE[아카이브<br/>→ sc1]
        SHARED[공유 스토리지<br/>→ EFS]
    end
    
    GP3 -.-> WEB_USE
    IO2 -.-> DB_USE
    ST1 -.-> BIG_DATA
    SC1 -.-> ARCHIVE
    EFS -.-> SHARED
    
    style TEMP fill:#ffcdd2
    style GP3 fill:#c8e6c9
    style IO2 fill:#bbdefb
    style ST1 fill:#fff9c4
    style EFS fill:#f8bbd9
```

## 8. EC2 네트워킹 개념

```mermaid
graph TB
    subgraph "Internet"
        IGW[Internet Gateway]
    end
    
    subgraph "VPC (10.0.0.0/16)"
        subgraph "Public Subnet (10.0.1.0/24)"
            EC2_PUB[EC2 Public Instance<br/>Private IP: 10.0.1.10<br/>Public IP: 54.123.45.67]
            EIP[Elastic IP<br/>52.123.45.89]
        end
        
        subgraph "Private Subnet (10.0.2.0/24)"
            EC2_PRIV[EC2 Private Instance<br/>Private IP: 10.0.2.10<br/>No Public IP]
        end
        
        subgraph "Network Components"
            RT_PUB[Public Route Table<br/>0.0.0.0/0 → IGW]
            RT_PRIV[Private Route Table<br/>10.0.0.0/16 → Local]
            NACL[Network ACL<br/>Subnet Level Firewall]
        end
    end
    
    IGW <--> EC2_PUB
    EIP -.-> EC2_PUB
    EC2_PUB <--> EC2_PRIV
    
    RT_PUB --> EC2_PUB
    RT_PRIV --> EC2_PRIV
    NACL --> EC2_PUB
    NACL --> EC2_PRIV
    
    subgraph "IP Address Types"
        PRIV_IP[Private IP<br/>• VPC 내부 통신<br/>• 인스턴스 재시작시 유지<br/>• 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16]
        PUB_IP[Public IP<br/>• 인터넷 통신<br/>• 인스턴스 재시작시 변경<br/>• 동적 할당]
        ELASTIC_IP[Elastic IP<br/>• 고정 퍼블릭 IP<br/>• 인스턴스간 이동 가능<br/>• 사용하지 않으면 과금]
    end
    
    style EC2_PUB fill:#e3f2fd
    style EC2_PRIV fill:#fce4ec
    style EIP fill:#fff3e0
    style PRIV_IP fill:#e8f5e8
    style PUB_IP fill:#f3e5f5
    style ELASTIC_IP fill:#fff8e1
```

## 9. EC2 모니터링 아키텍처

```mermaid
graph TB
    subgraph "EC2 Instances"
        EC2_1[EC2 Instance 1]
        EC2_2[EC2 Instance 2]
        EC2_3[EC2 Instance 3]
    end
    
    subgraph "CloudWatch"
        subgraph "Basic Monitoring (5분 간격)"
            CPU_UTIL[CPU Utilization]
            NET_IN[Network In]
            NET_OUT[Network Out]
            DISK_READ[Disk Read Ops]
            DISK_WRITE[Disk Write Ops]
        end
        
        subgraph "Detailed Monitoring (1분 간격)"
            DETAILED[상세 메트릭<br/>추가 비용 발생]
        end
        
        subgraph "Custom Metrics"
            MEMORY[Memory Usage<br/>CloudWatch Agent]
            DISK_SPACE[Disk Space<br/>CloudWatch Agent]
            APP_METRICS[Application Metrics<br/>Custom Scripts]
        end
    end
    
    subgraph "Health Checks"
        SYS_CHECK[System Status Check<br/>AWS 인프라 문제]
        INST_CHECK[Instance Status Check<br/>인스턴스 소프트웨어 문제]
    end
    
    subgraph "Alarms & Actions"
        ALARM[CloudWatch Alarms]
        SNS[SNS Notifications]
        AUTO_SCALE[Auto Scaling Actions]
        EC2_ACTION[EC2 Actions<br/>Stop/Terminate/Reboot]
    end
    
    EC2_1 --> CPU_UTIL
    EC2_1 --> NET_IN
    EC2_1 --> DISK_READ
    EC2_2 --> CPU_UTIL
    EC2_3 --> CPU_UTIL
    
    EC2_1 --> SYS_CHECK
    EC2_1 --> INST_CHECK
    
    CPU_UTIL --> ALARM
    MEMORY --> ALARM
    SYS_CHECK --> ALARM
    
    ALARM --> SNS
    ALARM --> AUTO_SCALE
    ALARM --> EC2_ACTION
    
    style CPU_UTIL fill:#e3f2fd
    style MEMORY fill:#e8f5e8
    style ALARM fill:#ffcdd2
    style SNS fill:#fff3e0
```

## 10. EC2 비용 최적화 전략

```mermaid
graph TD
    subgraph "구매 옵션별 비용 비교"
        subgraph "On-Demand"
            OD[온디맨드<br/>100% 비용<br/>유연성 최대]
        end
        
        subgraph "Reserved Instances"
            RI_1Y[1년 예약<br/>~30% 할인<br/>중간 약정]
            RI_3Y[3년 예약<br/>~50% 할인<br/>장기 약정]
        end
        
        subgraph "Spot Instances"
            SPOT[스팟 인스턴스<br/>~90% 할인<br/>중단 가능성]
        end
        
        subgraph "Savings Plans"
            SP_COMPUTE[Compute Savings Plans<br/>~66% 할인<br/>유연한 사용]
            SP_EC2[EC2 Instance Savings Plans<br/>~72% 할인<br/>특정 패밀리]
        end
    end
    
    subgraph "최적화 전략"
        subgraph "Right Sizing"
            MONITOR[모니터링<br/>CPU, 메모리 사용률 확인]
            RESIZE[크기 조정<br/>과소/과대 사용 인스턴스 조정]
        end
        
        subgraph "Scheduling"
            AUTO_STOP[자동 중지<br/>업무 시간 외 중지]
            SCHEDULE[스케줄링<br/>개발/테스트 환경 관리]
        end
        
        subgraph "Storage Optimization"
            EBS_OPT[EBS 최적화<br/>사용하지 않는 볼륨 삭제]
            SNAPSHOT[스냅샷 관리<br/>오래된 스냅샷 정리]
        end
    end
    
    subgraph "비용 모니터링"
        COST_EXPLORER[Cost Explorer<br/>비용 분석 및 예측]
        BUDGET[AWS Budgets<br/>예산 설정 및 알림]
        BILLING[Billing Dashboard<br/>실시간 비용 확인]
    end
    
    OD --> MONITOR
    RI_1Y --> MONITOR
    SPOT --> AUTO_STOP
    
    MONITOR --> COST_EXPLORER
    RESIZE --> COST_EXPLORER
    AUTO_STOP --> BUDGET
    
    style OD fill:#ffcdd2
    style RI_1Y fill:#c8e6c9
    style RI_3Y fill:#a5d6a7
    style SPOT fill:#bbdefb
    style SP_COMPUTE fill:#fff3e0
    style COST_EXPLORER fill:#f8bbd9
```

---

이러한 시각화 자료들은 EC2의 복잡한 개념들을 이해하기 쉽게 도와줍니다. 각 다이어그램을 참고하여 EC2 아키텍처의 전체적인 구조와 세부 구성 요소들의 관계를 파악해보세요.