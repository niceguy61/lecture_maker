# AWS 글로벌 인프라 시각화 자료

## 1. AWS 글로벌 인프라 개요

```mermaid
graph TB
    subgraph "AWS 글로벌 인프라"
        A[AWS 글로벌 인프라] --> B[리전<br/>Regions]
        A --> C[엣지 로케이션<br/>Edge Locations]
        A --> D[리전별 엣지 캐시<br/>Regional Edge Caches]
        
        B --> B1[33개 리전<br/>전 세계 분산]
        B --> B2[지리적으로 분리]
        B --> B3[독립적 운영]
        
        C --> C1[400개 이상]
        C --> C2[콘텐츠 캐싱]
        C --> C3[CloudFront CDN]
        
        D --> D1[중간 캐시 계층]
        D --> D2[캐시 적중률 향상]
    end
    
    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#ffcc99
```

## 2. 리전과 가용 영역 구조

```mermaid
graph TB
    subgraph "AWS 리전 (예: ap-northeast-2)"
        subgraph "가용 영역 A"
            AZ1[ap-northeast-2a]
            DC1[데이터 센터 1]
            DC2[데이터 센터 2]
            AZ1 --> DC1
            AZ1 --> DC2
        end
        
        subgraph "가용 영역 B"
            AZ2[ap-northeast-2b]
            DC3[데이터 센터 3]
            DC4[데이터 센터 4]
            AZ2 --> DC3
            AZ2 --> DC4
        end
        
        subgraph "가용 영역 C"
            AZ3[ap-northeast-2c]
            DC5[데이터 센터 5]
            DC6[데이터 센터 6]
            AZ3 --> DC5
            AZ3 --> DC6
        end
        
        subgraph "가용 영역 D"
            AZ4[ap-northeast-2d]
            DC7[데이터 센터 7]
            DC8[데이터 센터 8]
            AZ4 --> DC7
            AZ4 --> DC8
        end
    end
    
    AZ1 -.->|고속 네트워크<br/>지연시간 < 1ms| AZ2
    AZ2 -.->|고속 네트워크<br/>지연시간 < 1ms| AZ3
    AZ3 -.->|고속 네트워크<br/>지연시간 < 1ms| AZ4
    AZ1 -.->|고속 네트워크<br/>지연시간 < 1ms| AZ3
    
    style AZ1 fill:#e1f5fe
    style AZ2 fill:#e8f5e8
    style AZ3 fill:#fff3e0
    style AZ4 fill:#fce4ec
```

## 3. 고가용성 아키텍처 설계

```mermaid
graph TB
    subgraph "단일 AZ 배포 (권장하지 않음)"
        U1[사용자] --> LB1[로드 밸런서]
        LB1 --> AZ1_APP[애플리케이션 서버]
        AZ1_APP --> AZ1_DB[데이터베이스]
        
        AZ1_FAIL[❌ AZ 장애 시<br/>전체 서비스 중단]
    end
    
    subgraph "다중 AZ 배포 (권장)"
        U2[사용자] --> LB2[로드 밸런서<br/>다중 AZ]
        
        LB2 --> AZ2A_APP[애플리케이션 서버<br/>AZ-A]
        LB2 --> AZ2B_APP[애플리케이션 서버<br/>AZ-B]
        
        AZ2A_APP --> DB_PRIMARY[Primary DB<br/>AZ-A]
        AZ2B_APP --> DB_PRIMARY
        
        DB_PRIMARY -.->|동기 복제| DB_STANDBY[Standby DB<br/>AZ-B]
        
        AZ2_SUCCESS[✅ 한 AZ 장애 시에도<br/>서비스 지속]
    end
    
    style AZ1_FAIL fill:#ffcdd2
    style AZ2_SUCCESS fill:#c8e6c9
```

## 4. 엣지 로케이션과 CloudFront

```mermaid
graph TB
    subgraph "글로벌 콘텐츠 배송"
        USER1[사용자 - 서울] --> EDGE1[엣지 로케이션<br/>서울]
        USER2[사용자 - 도쿄] --> EDGE2[엣지 로케이션<br/>도쿄]
        USER3[사용자 - 싱가포르] --> EDGE3[엣지 로케이션<br/>싱가포르]
        
        EDGE1 --> CACHE1{캐시 확인}
        EDGE2 --> CACHE2{캐시 확인}
        EDGE3 --> CACHE3{캐시 확인}
        
        CACHE1 -->|캐시 미스| REGIONAL[리전별 엣지 캐시<br/>ap-northeast-2]
        CACHE2 -->|캐시 미스| REGIONAL
        CACHE3 -->|캐시 미스| REGIONAL
        
        REGIONAL --> ORIGIN_CHECK{캐시 확인}
        ORIGIN_CHECK -->|캐시 미스| ORIGIN[오리진 서버<br/>S3 버킷]
        
        CACHE1 -->|캐시 히트| CONTENT1[콘텐츠 반환<br/>빠른 응답]
        CACHE2 -->|캐시 히트| CONTENT2[콘텐츠 반환<br/>빠른 응답]
        CACHE3 -->|캐시 히트| CONTENT3[콘텐츠 반환<br/>빠른 응답]
    end
    
    style CONTENT1 fill:#c8e6c9
    style CONTENT2 fill:#c8e6c9
    style CONTENT3 fill:#c8e6c9
```

## 5. AWS 서비스 카테고리 맵

```mermaid
mindmap
  root((AWS 서비스))
    컴퓨팅
      EC2
        인스턴스
        Auto Scaling
        Elastic Load Balancing
      Lambda
        서버리스 함수
        이벤트 기반
      ECS/EKS
        컨테이너 오케스트레이션
      Batch
        배치 작업
    스토리지
      S3
        객체 스토리지
        정적 웹사이트
      EBS
        블록 스토리지
        EC2 연결
      EFS
        파일 스토리지
        NFS 프로토콜
      Glacier
        아카이브 스토리지
        장기 보관
    데이터베이스
      RDS
        관계형 DB
        MySQL, PostgreSQL
      DynamoDB
        NoSQL DB
        키-값 저장소
      ElastiCache
        인메모리 캐시
        Redis, Memcached
      Redshift
        데이터 웨어하우스
        분석용 DB
    네트워킹
      VPC
        가상 네트워크
        서브넷, 라우팅
      CloudFront
        CDN 서비스
        콘텐츠 배송
      Route 53
        DNS 서비스
        도메인 관리
      Direct Connect
        전용 연결
        온프레미스 연동
    보안
      IAM
        자격증명 관리
        권한 제어
      KMS
        키 관리
        암호화
      CloudTrail
        API 로깅
        감사 추적
      GuardDuty
        위협 탐지
        보안 모니터링
    관리도구
      CloudWatch
        모니터링
        로그 수집
      CloudFormation
        인프라 코드
        템플릿 배포
      Systems Manager
        시스템 관리
        패치 관리
      Config
        구성 관리
        규정 준수
```

## 6. AWS 공동 책임 모델

```mermaid
graph TB
    subgraph "AWS 책임 영역 (클라우드의 보안)"
        AWS1[물리적 보안]
        AWS2[하드웨어 인프라]
        AWS3[네트워크 인프라]
        AWS4[가상화 인프라]
        AWS5[관리형 서비스 구성]
    end
    
    subgraph "공유 제어"
        SHARED1[패치 관리]
        SHARED2[구성 관리]
        SHARED3[인식 및 교육]
    end
    
    subgraph "고객 책임 영역 (클라우드에서의 보안)"
        CUSTOMER1[게스트 OS 및 업데이트]
        CUSTOMER2[애플리케이션 소프트웨어]
        CUSTOMER3[보안 그룹 구성]
        CUSTOMER4[방화벽 구성]
        CUSTOMER5[네트워크 및 플랫폼 자격증명]
        CUSTOMER6[데이터 암호화]
    end
    
    subgraph "서비스 유형별 책임"
        IaaS[IaaS<br/>EC2, VPC<br/>고객 책임 ↑]
        PaaS[PaaS<br/>RDS, Lambda<br/>공유 책임]
        SaaS[SaaS<br/>WorkMail<br/>AWS 책임 ↑]
    end
    
    style AWS1 fill:#ff9999
    style AWS2 fill:#ff9999
    style AWS3 fill:#ff9999
    style AWS4 fill:#ff9999
    style AWS5 fill:#ff9999
    
    style SHARED1 fill:#ffeb3b
    style SHARED2 fill:#ffeb3b
    style SHARED3 fill:#ffeb3b
    
    style CUSTOMER1 fill:#4caf50
    style CUSTOMER2 fill:#4caf50
    style CUSTOMER3 fill:#4caf50
    style CUSTOMER4 fill:#4caf50
    style CUSTOMER5 fill:#4caf50
    style CUSTOMER6 fill:#4caf50
```

## 7. 리전 선택 기준

```mermaid
flowchart TD
    START[리전 선택 시작] --> COMPLIANCE{규정 준수<br/>요구사항 있음?}
    
    COMPLIANCE -->|예| LEGAL[법적 요구사항<br/>충족 리전 선택]
    COMPLIANCE -->|아니오| LATENCY{지연 시간<br/>중요함?}
    
    LATENCY -->|예| PROXIMITY[사용자와 가장<br/>가까운 리전 선택]
    LATENCY -->|아니오| SERVICE{필요한 서비스<br/>제공됨?}
    
    SERVICE -->|예| COST{비용<br/>고려사항?}
    SERVICE -->|아니오| ALTERNATIVE[대체 서비스<br/>또는 다른 리전 검토]
    
    COST -->|예| COMPARE[리전별 가격<br/>비교 분석]
    COST -->|아니오| DECISION[리전 결정]
    
    LEGAL --> DECISION
    PROXIMITY --> SERVICE
    COMPARE --> DECISION
    ALTERNATIVE --> START
    
    DECISION --> FINAL[최종 리전 선택 완료]
    
    style START fill:#e3f2fd
    style DECISION fill:#c8e6c9
    style FINAL fill:#4caf50
    style ALTERNATIVE fill:#ffcdd2
```

## 8. AWS Well-Architected Framework 5 Pillars

```mermaid
graph LR
    subgraph "AWS Well-Architected Framework"
        PILLAR1[운영 우수성<br/>Operational Excellence]
        PILLAR2[보안<br/>Security]
        PILLAR3[안정성<br/>Reliability]
        PILLAR4[성능 효율성<br/>Performance Efficiency]
        PILLAR5[비용 최적화<br/>Cost Optimization]
        
        PILLAR1 --> P1_1[시스템 운영 및 모니터링]
        PILLAR1 --> P1_2[지속적인 개선]
        PILLAR1 --> P1_3[자동화]
        
        PILLAR2 --> P2_1[정보 및 시스템 보호]
        PILLAR2 --> P2_2[위험 평가 및 완화]
        PILLAR2 --> P2_3[다층 보안]
        
        PILLAR3 --> P3_1[장애 복구 능력]
        PILLAR3 --> P3_2[동적 수요 충족]
        PILLAR3 --> P3_3[자동 복구]
        
        PILLAR4 --> P4_1[효율적 리소스 사용]
        PILLAR4 --> P4_2[기술 발전 활용]
        PILLAR4 --> P4_3[성능 모니터링]
        
        PILLAR5 --> P5_1[불필요한 비용 방지]
        PILLAR5 --> P5_2[최적 가격 달성]
        PILLAR5 --> P5_3[비용 투명성]
    end
    
    style PILLAR1 fill:#e3f2fd
    style PILLAR2 fill:#ffebee
    style PILLAR3 fill:#e8f5e8
    style PILLAR4 fill:#fff3e0
    style PILLAR5 fill:#f3e5f5
```

이러한 시각화 자료들은 AWS의 복잡한 개념들을 이해하기 쉽게 도식화한 것입니다. 각 다이어그램을 통해 AWS 글로벌 인프라의 구조와 서비스 관계를 명확히 파악할 수 있습니다.