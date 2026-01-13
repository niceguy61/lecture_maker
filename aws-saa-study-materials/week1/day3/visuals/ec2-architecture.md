# EC2 아키텍처 시각화 자료

## EC2 서비스 아키텍처 다이어그램

### 1. EC2 전체 아키텍처 개요

```mermaid
graph TB
    subgraph "AWS 클라우드"
        subgraph "리전 (Region)"
            subgraph "가용 영역 A (AZ-A)"
                subgraph "VPC"
                    subgraph "퍼블릭 서브넷"
                        EC2A[EC2 인스턴스]
                        ELB[로드 밸런서]
                    end
                    subgraph "프라이빗 서브넷"
                        EC2B[EC2 인스턴스]
                        RDS[RDS 데이터베이스]
                    end
                end
                EBS1[EBS 볼륨]
            end
            
            subgraph "가용 영역 B (AZ-B)"
                subgraph "VPC2"
                    subgraph "퍼블릭 서브넷2"
                        EC2C[EC2 인스턴스]
                    end
                    subgraph "프라이빗 서브넷2"
                        EC2D[EC2 인스턴스]
                    end
                end
                EBS2[EBS 볼륨]
            end
        end
    end
    
    subgraph "사용자"
        USER[인터넷 사용자]
        ADMIN[시스템 관리자]
    end
    
    USER --> ELB
    ELB --> EC2A
    ELB --> EC2C
    EC2A --> EC2B
    EC2C --> EC2D
    EC2B --> RDS
    EC2D --> RDS
    
    ADMIN --> |SSH/RDP| EC2A
    ADMIN --> |SSH/RDP| EC2C
    
    EC2A --> EBS1
    EC2B --> EBS1
    EC2C --> EBS2
    EC2D --> EBS2
```

### 2. EC2 인스턴스 유형별 특성

```mermaid
mindmap
  root((EC2 인스턴스 유형))
    범용 (General Purpose)
      T3/T4g
        버스터블 성능
        웹 서버
        소규모 DB
        개발 환경
      M5/M6i
        균형잡힌 성능
        웹 애플리케이션
        마이크로서비스
        엔터프라이즈 앱
    컴퓨팅 최적화 (Compute)
      C5/C6i
        고성능 CPU
        과학 계산
        게임 서버
        HPC
    메모리 최적화 (Memory)
      R5/R6i
        고메모리
        인메모리 DB
        빅데이터 분석
        캐싱
      X1e
        초고메모리
        SAP HANA
        Apache Spark
    스토리지 최적화 (Storage)
      I3/I4i
        고속 SSD
        NoSQL DB
        분산 파일시스템
      D2/D3
        고밀도 HDD
        분산 스토리지
        데이터 웨어하우스
    가속 컴퓨팅 (Accelerated)
      P3/P4
        GPU ML/AI
        머신러닝 훈련
        HPC
      G4
        GPU 그래픽
        게임 스트리밍
        비디오 처리
```

### 3. EC2 인스턴스 생명주기

```mermaid
stateDiagram-v2
    [*] --> Pending: 인스턴스 시작<br/>(Launch Instance)
    
    Pending --> Running: 부팅 완료<br/>(Boot Complete)
    
    Running --> Stopping: 중지 요청<br/>(Stop Instance)
    Running --> Shutting_down: 종료 요청<br/>(Terminate Instance)
    Running --> Rebooting: 재부팅<br/>(Reboot Instance)
    
    Stopping --> Stopped: 중지 완료<br/>(Stop Complete)
    
    Stopped --> Pending: 재시작<br/>(Start Instance)
    Stopped --> Shutting_down: 종료 요청<br/>(Terminate Instance)
    
    Shutting_down --> Terminated: 종료 완료<br/>(Terminate Complete)
    
    Rebooting --> Running: 재부팅 완료<br/>(Reboot Complete)
    
    Terminated --> [*]
    
    note right of Pending
        - 하드웨어 할당
        - 부팅 과정
        - 요금 부과 시작
    end note
    
    note right of Running
        - 정상 작동
        - SSH/RDP 접속 가능
        - 애플리케이션 실행
    end note
    
    note right of Stopped
        - 컴퓨팅 요금 중단
        - EBS 볼륨 유지
        - 퍼블릭 IP 해제
    end note
    
    note right of Terminated
        - 인스턴스 완전 삭제
        - 인스턴스 스토어 손실
        - EBS 루트 볼륨 삭제
    end note
```

### 4. 보안 그룹 작동 원리

```mermaid
graph LR
    subgraph "인터넷"
        INTERNET[인터넷 사용자<br/>🌐]
        ADMIN[관리자<br/>👨‍💻]
    end
    
    subgraph "AWS VPC"
        subgraph "보안 그룹 (Security Group)"
            direction TB
            INBOUND[인바운드 규칙<br/>📥]
            OUTBOUND[아웃바운드 규칙<br/>📤]
            
            subgraph "인바운드 규칙 예시"
                HTTP[HTTP: 80<br/>Source: 0.0.0.0/0]
                HTTPS[HTTPS: 443<br/>Source: 0.0.0.0/0]
                SSH[SSH: 22<br/>Source: My IP]
            end
            
            subgraph "아웃바운드 규칙"
                ALL_OUT[All Traffic<br/>Destination: 0.0.0.0/0]
            end
        end
        
        subgraph "EC2 인스턴스"
            WEB[웹 서버<br/>🖥️<br/>포트 80, 443]
        end
    end
    
    INTERNET --> |HTTP/HTTPS 요청| HTTP
    INTERNET --> |HTTP/HTTPS 요청| HTTPS
    ADMIN --> |SSH 접속| SSH
    
    HTTP --> WEB
    HTTPS --> WEB
    SSH --> WEB
    
    WEB --> |모든 아웃바운드| ALL_OUT
    ALL_OUT --> INTERNET
    
    style INBOUND fill:#e1f5fe
    style OUTBOUND fill:#f3e5f5
    style WEB fill:#e8f5e8
```

### 5. EC2 요금 모델 비교

```mermaid
graph TB
    subgraph "EC2 요금 모델 비교"
        subgraph "온디맨드 (On-Demand)"
            OD[💰 시간당 과금<br/>📋 약정 없음<br/>⚡ 즉시 사용<br/>💸 가장 비쌈]
        end
        
        subgraph "예약 인스턴스 (Reserved)"
            RI[💰 1-3년 약정<br/>💸 최대 75% 할인<br/>📦 용량 예약<br/>📊 예측 가능한 워크로드]
        end
        
        subgraph "스팟 인스턴스 (Spot)"
            SI[💰 경매 방식<br/>💸 최대 90% 할인<br/>⚠️ 중단 가능<br/>🔄 내결함성 필요]
        end
        
        subgraph "전용 호스트 (Dedicated)"
            DH[💰 물리 서버 전용<br/>🔒 라이선스 최적화<br/>📋 규정 준수<br/>💸 가장 비쌈]
        end
    end
    
    subgraph "사용 시나리오"
        OD --> OD_USE[개발/테스트<br/>예측 불가능한 워크로드<br/>단기 프로젝트]
        RI --> RI_USE[프로덕션 환경<br/>안정적인 워크로드<br/>장기 운영]
        SI --> SI_USE[배치 작업<br/>빅데이터 처리<br/>내결함성 애플리케이션]
        DH --> DH_USE[라이선스 제약<br/>규정 준수<br/>보안 요구사항]
    end
    
    style OD fill:#ffebee
    style RI fill:#e8f5e8
    style SI fill:#fff3e0
    style DH fill:#f3e5f5
```

### 6. EC2 모니터링 아키텍처

```mermaid
graph TB
    subgraph "EC2 인스턴스"
        APP[애플리케이션<br/>🚀]
        OS[운영체제<br/>🖥️]
        META[메타데이터 서비스<br/>169.254.169.254]
    end
    
    subgraph "CloudWatch"
        METRICS[메트릭 수집<br/>📊]
        ALARMS[알람<br/>🚨]
        DASHBOARD[대시보드<br/>📈]
        LOGS[로그<br/>📝]
    end
    
    subgraph "기본 메트릭 (5분 간격)"
        CPU[CPU 사용률<br/>💻]
        NETWORK[네트워크 I/O<br/>🌐]
        DISK[디스크 I/O<br/>💾]
    end
    
    subgraph "상세 모니터링 (1분 간격)"
        DETAILED[상세 메트릭<br/>⏱️<br/>추가 비용]
    end
    
    subgraph "사용자 액션"
        ADMIN[관리자<br/>👨‍💻]
        AUTO[Auto Scaling<br/>🔄]
    end
    
    OS --> METRICS
    APP --> LOGS
    
    METRICS --> CPU
    METRICS --> NETWORK
    METRICS --> DISK
    METRICS --> DETAILED
    
    METRICS --> ALARMS
    METRICS --> DASHBOARD
    
    ALARMS --> ADMIN
    ALARMS --> AUTO
    
    APP --> |HTTP 요청| META
    META --> |인스턴스 정보| APP
    
    style METRICS fill:#e3f2fd
    style ALARMS fill:#ffebee
    style DASHBOARD fill:#e8f5e8
```

### 7. 키 페어 인증 과정

```mermaid
sequenceDiagram
    participant User as 사용자 👨‍💻
    participant AWS as AWS 콘솔 ☁️
    participant EC2 as EC2 인스턴스 🖥️
    participant SSH as SSH 클라이언트 🔐
    
    Note over User,EC2: 키 페어 생성 과정
    User->>AWS: 키 페어 생성 요청
    AWS->>User: 프라이빗 키 (.pem) 다운로드
    AWS->>EC2: 퍼블릭 키 설치 (authorized_keys)
    
    Note over User,EC2: 인스턴스 시작
    User->>AWS: 인스턴스 시작 (키 페어 지정)
    AWS->>EC2: 인스턴스 생성 및 퍼블릭 키 설치
    
    Note over User,EC2: SSH 연결 과정
    User->>SSH: ssh -i private_key.pem ec2-user@public-ip
    SSH->>EC2: 연결 시도 (프라이빗 키 사용)
    EC2->>SSH: 퍼블릭 키로 검증
    SSH->>User: 인증 성공, 셸 접속
    
    Note over User,EC2: 보안 고려사항
    Note right of User: - 프라이빗 키 안전 보관<br/>- 적절한 권한 설정 (chmod 400)<br/>- 키 공유 금지<br/>- 정기적 키 교체
```

### 8. EC2 배치 전략

```mermaid
graph TB
    subgraph "배치 그룹 (Placement Groups)"
        subgraph "클러스터 (Cluster)"
            CLUSTER[🔗 클러스터 배치<br/>- 저지연, 고대역폭<br/>- 단일 AZ<br/>- HPC 워크로드]
        end
        
        subgraph "파티션 (Partition)"
            PARTITION[📦 파티션 배치<br/>- 대규모 분산 워크로드<br/>- 하드웨어 장애 격리<br/>- Hadoop, Cassandra]
        end
        
        subgraph "스프레드 (Spread)"
            SPREAD[🌐 스프레드 배치<br/>- 고가용성<br/>- 서로 다른 하드웨어<br/>- 중요한 인스턴스들]
        end
    end
    
    subgraph "가용 영역 A"
        subgraph "랙 1"
            C1[인스턴스 1]
            C2[인스턴스 2]
        end
        subgraph "랙 2"
            P1[파티션 1<br/>인스턴스들]
        end
        subgraph "랙 3"
            S1[인스턴스 A]
        end
    end
    
    subgraph "가용 영역 B"
        subgraph "랙 4"
            P2[파티션 2<br/>인스턴스들]
        end
        subgraph "랙 5"
            S2[인스턴스 B]
        end
    end
    
    CLUSTER --> C1
    CLUSTER --> C2
    PARTITION --> P1
    PARTITION --> P2
    SPREAD --> S1
    SPREAD --> S2
    
    style CLUSTER fill:#e3f2fd
    style PARTITION fill:#e8f5e8
    style SPREAD fill:#fff3e0
```

### 9. EC2 네트워킹 개요

```mermaid
graph TB
    subgraph "인터넷"
        IGW[인터넷 게이트웨이<br/>🌐]
    end
    
    subgraph "VPC (Virtual Private Cloud)"
        subgraph "퍼블릭 서브넷"
            subgraph "EC2 인스턴스 (웹 서버)"
                PUB_EC2[퍼블릭 IP: 54.180.1.1<br/>프라이빗 IP: 10.0.1.10<br/>🖥️]
                SG_PUB[보안 그룹<br/>HTTP: 80 (0.0.0.0/0)<br/>SSH: 22 (My IP)]
            end
        end
        
        subgraph "프라이빗 서브넷"
            subgraph "EC2 인스턴스 (앱 서버)"
                PRIV_EC2[프라이빗 IP: 10.0.2.10<br/>🖥️]
                SG_PRIV[보안 그룹<br/>App: 8080 (웹 서버 SG)<br/>SSH: 22 (Bastion)]
            end
        end
        
        subgraph "라우팅 테이블"
            PUB_RT[퍼블릭 라우팅 테이블<br/>0.0.0.0/0 → IGW]
            PRIV_RT[프라이빗 라우팅 테이블<br/>0.0.0.0/0 → NAT Gateway]
        end
        
        NAT[NAT Gateway<br/>🔄]
    end
    
    IGW --> PUB_EC2
    PUB_EC2 --> PRIV_EC2
    PRIV_EC2 --> NAT
    NAT --> IGW
    
    PUB_RT --> PUB_EC2
    PRIV_RT --> PRIV_EC2
    
    style PUB_EC2 fill:#e8f5e8
    style PRIV_EC2 fill:#fff3e0
    style SG_PUB fill:#e3f2fd
    style SG_PRIV fill:#e3f2fd
```

### 10. EC2 스토리지 옵션

```mermaid
graph TB
    subgraph "EC2 스토리지 옵션"
        subgraph "EBS (Elastic Block Store)"
            EBS_GP3[gp3 (범용 SSD)<br/>💾 균형잡힌 성능<br/>💰 비용 효율적]
            EBS_IO2[io2 (프로비저닝된 IOPS)<br/>⚡ 고성능<br/>💸 높은 비용]
            EBS_ST1[st1 (처리량 최적화 HDD)<br/>📊 빅데이터<br/>💰 저비용]
            EBS_SC1[sc1 (콜드 HDD)<br/>❄️ 아카이브<br/>💰 최저비용]
        end
        
        subgraph "인스턴스 스토어"
            INSTANCE[인스턴스 스토어<br/>⚡ 최고 성능<br/>⚠️ 임시 스토리지<br/>💰 추가 비용 없음]
        end
        
        subgraph "EFS (Elastic File System)"
            EFS[EFS<br/>🌐 다중 인스턴스 공유<br/>📈 자동 확장<br/>💸 사용량 기반 과금]
        end
    end
    
    subgraph "EC2 인스턴스들"
        EC2_1[EC2 인스턴스 1<br/>🖥️]
        EC2_2[EC2 인스턴스 2<br/>🖥️]
        EC2_3[EC2 인스턴스 3<br/>🖥️]
    end
    
    EC2_1 --> EBS_GP3
    EC2_1 --> INSTANCE
    EC2_2 --> EBS_IO2
    EC2_3 --> EBS_ST1
    
    EC2_1 --> EFS
    EC2_2 --> EFS
    EC2_3 --> EFS
    
    style EBS_GP3 fill:#e8f5e8
    style EBS_IO2 fill:#ffebee
    style INSTANCE fill:#fff3e0
    style EFS fill:#e3f2fd
```

---

## 시각화 자료 활용 가이드

### 학습 순서
1. **전체 아키텍처** → EC2의 전체적인 위치와 역할 이해
2. **인스턴스 유형** → 워크로드별 최적 선택 기준 학습
3. **생명주기** → 인스턴스 상태 관리 방법 이해
4. **보안 그룹** → 네트워크 보안 설정 방법 학습
5. **요금 모델** → 비용 최적화 전략 수립

### 실습 연계
- 각 다이어그램을 참조하여 실습 과정 이해
- 문제 발생 시 해당 다이어그램으로 문제 지점 파악
- 아키텍처 설계 시 참조 자료로 활용

### 시험 준비
- 각 다이어그램의 구성 요소와 관계 암기
- 시나리오 문제 해결 시 시각적 사고 활용
- 아키텍처 설계 문제에서 다이어그램 그리기 연습