# AWS 글로벌 인프라 시각화 자료

## 1. AWS 글로벌 인프라 전체 구조

```mermaid
graph TB
    subgraph "AWS 글로벌 인프라 계층"
        A[AWS 글로벌 인프라] --> B[리전<br/>33개 리전]
        A --> C[가용 영역<br/>105개 AZ]
        A --> D[엣지 로케이션<br/>400+ 위치]
        A --> E[로컬 존<br/>대도시 근처]
        
        B --> B1["지리적으로 분리된<br/>독립적인 데이터센터 클러스터"]
        C --> C1["리전 내 물리적으로<br/>분리된 데이터센터"]
        D --> D1["CDN 캐시 서버<br/>콘텐츠 배포 네트워크"]
        E --> E1["초저지연 애플리케이션<br/>지원 인프라"]
    end
```

## 2. 리전과 가용 영역 관계

```mermaid
graph TB
    subgraph "AWS 리전 구조"
        subgraph "Region: ap-northeast-2 (서울)"
            AZ1["AZ-2a<br/>📍 데이터센터 A<br/>독립 전력/냉각/네트워킹"]
            AZ2["AZ-2b<br/>📍 데이터센터 B<br/>독립 전력/냉각/네트워킹"]
            AZ3["AZ-2c<br/>📍 데이터센터 C<br/>독립 전력/냉각/네트워킹"]
            AZ4["AZ-2d<br/>📍 데이터센터 D<br/>독립 전력/냉각/네트워킹"]
        end
        
        AZ1 <--> AZ2
        AZ2 <--> AZ3
        AZ3 <--> AZ4
        AZ1 <--> AZ3
        AZ1 <--> AZ4
        AZ2 <--> AZ4
    end
    
    subgraph "연결 특성"
        CONN1["🔗 고속 네트워크<br/>지연시간 < 10ms"]
        CONN2["🔒 암호화된 연결<br/>높은 대역폭"]
        CONN3["⚡ 실시간 데이터 복제<br/>고가용성 보장"]
    end
```

## 3. 전 세계 주요 리전 분포

```mermaid
graph TB
    subgraph "북미 (North America)"
        NA1["🇺🇸 us-east-1<br/>버지니아 북부<br/>6개 AZ"]
        NA2["🇺🇸 us-west-2<br/>오레곤<br/>4개 AZ"]
        NA3["🇨🇦 ca-central-1<br/>캐나다 중부<br/>3개 AZ"]
    end
    
    subgraph "아시아 태평양 (Asia Pacific)"
        AP1["🇰🇷 ap-northeast-2<br/>서울<br/>4개 AZ"]
        AP2["🇯🇵 ap-northeast-1<br/>도쿄<br/>3개 AZ"]
        AP3["🇸🇬 ap-southeast-1<br/>싱가포르<br/>3개 AZ"]
        AP4["🇦🇺 ap-southeast-2<br/>시드니<br/>3개 AZ"]
    end
    
    subgraph "유럽 (Europe)"
        EU1["🇮🇪 eu-west-1<br/>아일랜드<br/>3개 AZ"]
        EU2["🇩🇪 eu-central-1<br/>프랑크푸르트<br/>3개 AZ"]
        EU3["🇬🇧 eu-west-2<br/>런던<br/>3개 AZ"]
    end
    
    subgraph "남미 (South America)"
        SA1["🇧🇷 sa-east-1<br/>상파울루<br/>3개 AZ"]
    end
```

## 4. 엣지 로케이션 네트워크

```mermaid
graph TB
    subgraph "CloudFront 엣지 네트워크"
        subgraph "아시아"
            EDGE_ASIA["🌏 아시아 엣지<br/>서울, 도쿄, 싱가포르<br/>홍콩, 뭄바이, 시드니"]
        end
        
        subgraph "북미"
            EDGE_NA["🌎 북미 엣지<br/>뉴욕, 시애틀, 댈러스<br/>로스앤젤레스, 토론토"]
        end
        
        subgraph "유럽"
            EDGE_EU["🌍 유럽 엣지<br/>런던, 프랑크푸르트<br/>파리, 암스테르담, 밀라노"]
        end
        
        subgraph "기타 지역"
            EDGE_OTHER["🌐 기타 지역<br/>상파울루, 케이프타운<br/>텔아비브, 자카르타"]
        end
    end
    
    USER1["👤 한국 사용자"] --> EDGE_ASIA
    USER2["👤 미국 사용자"] --> EDGE_NA
    USER3["👤 유럽 사용자"] --> EDGE_EU
    USER4["👤 기타 지역 사용자"] --> EDGE_OTHER
    
    EDGE_ASIA -.-> ORIGIN1["📦 오리진 서버<br/>S3, EC2 등"]
    EDGE_NA -.-> ORIGIN1
    EDGE_EU -.-> ORIGIN1
    EDGE_OTHER -.-> ORIGIN1
```

## 5. 고가용성 아키텍처 예시

```mermaid
graph TB
    subgraph "Multi-AZ 고가용성 설계"
        subgraph "AZ-2a (Primary)"
            WEB1["🌐 웹 서버<br/>EC2 인스턴스"]
            APP1["⚙️ 애플리케이션 서버<br/>EC2 인스턴스"]
            DB1["🗄️ 데이터베이스<br/>RDS Primary"]
        end
        
        subgraph "AZ-2b (Secondary)"
            WEB2["🌐 웹 서버<br/>EC2 인스턴스"]
            APP2["⚙️ 애플리케이션 서버<br/>EC2 인스턴스"]
            DB2["🗄️ 데이터베이스<br/>RDS Standby"]
        end
        
        subgraph "AZ-2c (Tertiary)"
            WEB3["🌐 웹 서버<br/>EC2 인스턴스"]
            APP3["⚙️ 애플리케이션 서버<br/>EC2 인스턴스"]
            BACKUP["💾 백업 스토리지<br/>S3"]
        end
    end
    
    LB["⚖️ 로드 밸런서<br/>Application Load Balancer"]
    
    USER["👤 사용자"] --> LB
    LB --> WEB1
    LB --> WEB2
    LB --> WEB3
    
    WEB1 --> APP1
    WEB2 --> APP2
    WEB3 --> APP3
    
    APP1 --> DB1
    APP2 --> DB1
    APP3 --> DB1
    
    DB1 -.-> DB2
    DB1 -.-> BACKUP
```

## 6. 데이터 복제 및 백업 전략

```mermaid
graph LR
    subgraph "Primary Region: ap-northeast-2"
        PRIMARY["🏢 운영 환경<br/>실시간 서비스"]
        PRIMARY_BACKUP["💾 로컬 백업<br/>스냅샷, 로그"]
    end
    
    subgraph "Secondary Region: ap-northeast-1"
        SECONDARY["🏢 재해복구 환경<br/>대기 상태"]
        SECONDARY_BACKUP["💾 원격 백업<br/>교차 리전 복제"]
    end
    
    subgraph "Global Services"
        S3_GLOBAL["🌐 S3 Cross-Region<br/>자동 복제"]
        CLOUDFRONT["🚀 CloudFront<br/>글로벌 캐시"]
    end
    
    PRIMARY --> PRIMARY_BACKUP
    PRIMARY -.-> SECONDARY
    PRIMARY_BACKUP -.-> SECONDARY_BACKUP
    
    PRIMARY --> S3_GLOBAL
    SECONDARY --> S3_GLOBAL
    
    S3_GLOBAL --> CLOUDFRONT
    
    USERS["👥 전 세계 사용자"] --> CLOUDFRONT
```

## 7. 리전 선택 의사결정 트리

```mermaid
graph TD
    START["🤔 리전 선택 시작"] --> Q1{"📍 사용자 위치는?"}
    
    Q1 -->|한국/동아시아| ASIA["🇰🇷 ap-northeast-2<br/>🇯🇵 ap-northeast-1"]
    Q1 -->|북미| NA["🇺🇸 us-east-1<br/>🇺🇸 us-west-2"]
    Q1 -->|유럽| EU["🇮🇪 eu-west-1<br/>🇩🇪 eu-central-1"]
    
    ASIA --> Q2{"💰 비용 vs 성능?"}
    NA --> Q3{"🔧 필요한 서비스<br/>모두 제공?"}
    EU --> Q4{"⚖️ 데이터 규정<br/>준수 필요?"}
    
    Q2 -->|성능 우선| SEOUL["✅ ap-northeast-2<br/>서울 리전 선택"]
    Q2 -->|비용 우선| TOKYO["✅ ap-northeast-1<br/>도쿄 리전 선택"]
    
    Q3 -->|예| VIRGINIA["✅ us-east-1<br/>버지니아 리전 선택"]
    Q3 -->|아니오| OREGON["✅ us-west-2<br/>오레곤 리전 선택"]
    
    Q4 -->|GDPR 준수| IRELAND["✅ eu-west-1<br/>아일랜드 리전 선택"]
    Q4 -->|독일 법규| FRANKFURT["✅ eu-central-1<br/>프랑크푸르트 리전 선택"]
```

## 8. AWS 서비스별 글로벌 vs 리전별 분류

```mermaid
graph TB
    subgraph "글로벌 서비스 (Global Services)"
        GLOBAL1["🌐 IAM<br/>사용자 및 권한 관리"]
        GLOBAL2["🌐 Route 53<br/>DNS 서비스"]
        GLOBAL3["🌐 CloudFront<br/>CDN 서비스"]
        GLOBAL4["🌐 WAF<br/>웹 애플리케이션 방화벽"]
    end
    
    subgraph "리전별 서비스 (Regional Services)"
        REGIONAL1["🏢 EC2<br/>가상 서버"]
        REGIONAL2["🏢 S3<br/>객체 스토리지"]
        REGIONAL3["🏢 RDS<br/>관리형 데이터베이스"]
        REGIONAL4["🏢 VPC<br/>가상 사설 클라우드"]
    end
    
    subgraph "AZ별 서비스 (AZ-specific Services)"
        AZ1["📍 EBS<br/>블록 스토리지"]
        AZ2["📍 서브넷<br/>네트워크 세그먼트"]
        AZ3["📍 EC2 인스턴스<br/>특정 AZ에 배치"]
    end
    
    GLOBAL1 -.-> REGIONAL1
    GLOBAL2 -.-> REGIONAL2
    REGIONAL1 --> AZ1
    REGIONAL4 --> AZ2
    REGIONAL1 --> AZ3
```

## 9. 네트워크 지연시간 비교

```mermaid
graph LR
    subgraph "지연시간 비교 (한국 기준)"
        KOREA["🇰🇷 한국 사용자"]
        
        SEOUL["ap-northeast-2<br/>서울<br/>⚡ ~5ms"]
        TOKYO["ap-northeast-1<br/>도쿄<br/>⚡ ~30ms"]
        SINGAPORE["ap-southeast-1<br/>싱가포르<br/>⚡ ~80ms"]
        VIRGINIA["us-east-1<br/>버지니아<br/>⚡ ~180ms"]
        IRELAND["eu-west-1<br/>아일랜드<br/>⚡ ~280ms"]
    end
    
    KOREA --> SEOUL
    KOREA --> TOKYO
    KOREA --> SINGAPORE
    KOREA --> VIRGINIA
    KOREA --> IRELAND
    
    style SEOUL fill:#90EE90
    style TOKYO fill:#FFE4B5
    style SINGAPORE fill:#FFB6C1
    style VIRGINIA fill:#FFA07A
    style IRELAND fill:#F08080
```

## 10. 재해 복구 전략 시각화

```mermaid
graph TB
    subgraph "재해 복구 시나리오"
        subgraph "정상 운영"
            NORMAL["🟢 Primary Region<br/>ap-northeast-2<br/>100% 트래픽"]
        end
        
        subgraph "재해 발생"
            DISASTER["🔴 Primary Region<br/>ap-northeast-2<br/>서비스 중단"]
            FAILOVER["🟡 Secondary Region<br/>ap-northeast-1<br/>자동 전환"]
        end
        
        subgraph "복구 완료"
            RECOVERY["🟢 Primary Region<br/>ap-northeast-2<br/>서비스 복구"]
            FAILBACK["🔄 트래픽 복귀<br/>정상 운영 재개"]
        end
    end
    
    NORMAL -->|재해 발생| DISASTER
    DISASTER -->|자동 전환| FAILOVER
    FAILOVER -->|복구 작업| RECOVERY
    RECOVERY -->|트래픽 복귀| FAILBACK
    FAILBACK -->|정상 운영| NORMAL
```

---

**참고사항**: 이 시각화 자료들은 AWS 글로벌 인프라의 핵심 개념을 이해하기 위한 교육용 다이어그램입니다. 실제 AWS 인프라는 더욱 복잡하고 정교한 구조를 가지고 있습니다.