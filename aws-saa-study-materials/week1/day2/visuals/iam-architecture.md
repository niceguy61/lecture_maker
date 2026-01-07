# IAM 아키텍처 시각화 자료

## 1. IAM 전체 구조 개요

```mermaid
graph TB
    subgraph "AWS Account"
        subgraph "IAM Service (Global)"
            U[Users] 
            G[Groups]
            R[Roles]
            P[Policies]
        end
        
        subgraph "AWS Services"
            EC2[EC2 Instances]
            S3[S3 Buckets]
            RDS[RDS Databases]
            Lambda[Lambda Functions]
        end
    end
    
    U --> G
    G --> P
    U --> P
    R --> P
    
    U -.-> EC2
    U -.-> S3
    R --> EC2
    R --> Lambda
    
    style U fill:#e1f5fe
    style G fill:#f3e5f5
    style R fill:#fff3e0
    style P fill:#e8f5e8
```

## 2. IAM 구성 요소 관계도

```mermaid
graph LR
    subgraph "Identity (누가)"
        U1[User: 김개발자]
        U2[User: 이관리자]
        G1[Group: Developers]
        G2[Group: Admins]
        R1[Role: EC2-S3-Role]
    end
    
    subgraph "Permissions (무엇을)"
        P1[Policy: S3ReadOnly]
        P2[Policy: EC2FullAccess]
        P3[Policy: AdminAccess]
    end
    
    subgraph "Resources (어디에)"
        S3B[S3 Bucket]
        EC2I[EC2 Instance]
        RDS1[RDS Database]
    end
    
    U1 --> G1
    U2 --> G2
    G1 --> P1
    G1 --> P2
    G2 --> P3
    R1 --> P1
    
    P1 -.-> S3B
    P2 -.-> EC2I
    P3 -.-> S3B
    P3 -.-> EC2I
    P3 -.-> RDS1
    
    EC2I --> R1
    
    style U1 fill:#bbdefb
    style U2 fill:#bbdefb
    style G1 fill:#ce93d8
    style G2 fill:#ce93d8
    style R1 fill:#ffcc80
```

## 3. IAM 정책 작동 방식

```mermaid
flowchart TD
    A[API 요청] --> B{인증된 사용자?}
    B -->|No| C[액세스 거부]
    B -->|Yes| D[사용자 정책 확인]
    
    D --> E[그룹 정책 확인]
    E --> F[역할 정책 확인]
    F --> G{명시적 Deny 존재?}
    
    G -->|Yes| H[액세스 거부]
    G -->|No| I{Allow 권한 존재?}
    
    I -->|No| J[기본 거부]
    I -->|Yes| K[액세스 허용]
    
    style A fill:#e3f2fd
    style C fill:#ffebee
    style H fill:#ffebee
    style J fill:#ffebee
    style K fill:#e8f5e8
```

## 4. 사용자-그룹-정책 관계

```mermaid
graph TB
    subgraph "사용자 관리"
        U1[김개발자]
        U2[박개발자]
        U3[이관리자]
        U4[최관리자]
    end
    
    subgraph "그룹 관리"
        G1[Developers Group]
        G2[Admins Group]
        G3[ReadOnly Group]
    end
    
    subgraph "정책 관리"
        P1[EC2 개발 정책]
        P2[S3 읽기 정책]
        P3[관리자 정책]
        P4[읽기 전용 정책]
    end
    
    U1 --> G1
    U2 --> G1
    U2 --> G3
    U3 --> G2
    U4 --> G2
    
    G1 --> P1
    G1 --> P2
    G2 --> P3
    G3 --> P4
    
    style G1 fill:#c8e6c9
    style G2 fill:#ffcdd2
    style G3 fill:#fff9c4
```

## 5. IAM 역할 사용 시나리오

```mermaid
sequenceDiagram
    participant App as 애플리케이션
    participant EC2 as EC2 인스턴스
    participant IAM as IAM 서비스
    participant S3 as S3 서비스
    
    Note over EC2,IAM: 1. 역할 할당 (배포 시)
    EC2->>IAM: 역할 연결 요청
    IAM-->>EC2: 역할 할당 완료
    
    Note over App,S3: 2. 런타임 액세스
    App->>EC2: S3 파일 읽기 요청
    EC2->>IAM: 임시 자격증명 요청
    IAM-->>EC2: 임시 토큰 발급
    EC2->>S3: 토큰으로 파일 접근
    S3-->>EC2: 파일 데이터 반환
    EC2-->>App: 파일 데이터 전달
```

## 6. 교차 계정 액세스 패턴

```mermaid
graph TB
    subgraph "Account A (개발)"
        UA[개발자 사용자]
        RA[개발 역할]
    end
    
    subgraph "Account B (운영)"
        RB[운영 역할]
        TB[신뢰 정책]
        S3B[운영 S3 버킷]
    end
    
    UA --> RA
    RA -.->|AssumeRole| RB
    TB -.->|신뢰| RA
    RB --> S3B
    
    style UA fill:#e1f5fe
    style RA fill:#fff3e0
    style RB fill:#fff3e0
    style TB fill:#f3e5f5
    style S3B fill:#e8f5e8
```

## 7. IAM 보안 모범 사례 다이어그램

```mermaid
mindmap
  root((IAM 보안))
    최소 권한
      필요한 권한만
      정기적 검토
      임시 권한 사용
    
    루트 계정 보호
      MFA 활성화
      일상 사용 금지
      강력한 비밀번호
    
    모니터링
      CloudTrail 로깅
      액세스 분석
      이상 행동 탐지
    
    자격증명 관리
      정기적 키 교체
      임시 자격증명 선호
      하드코딩 금지
```

## 8. IAM 정책 평가 흐름

```mermaid
flowchart LR
    A[요청 시작] --> B[사용자 인증]
    B --> C[컨텍스트 수집]
    C --> D[정책 수집]
    
    D --> E[명시적 Deny?]
    E -->|Yes| F[거부]
    E -->|No| G[Allow 확인]
    
    G --> H[조건 평가]
    H --> I[최종 결정]
    
    subgraph "정책 유형"
        J[사용자 정책]
        K[그룹 정책]
        L[역할 정책]
        M[리소스 정책]
    end
    
    D --> J
    D --> K
    D --> L
    D --> M
    
    style F fill:#ffcdd2
    style I fill:#c8e6c9
```

## 9. 실제 환경 IAM 구조 예시

```mermaid
graph TB
    subgraph "Production Account"
        subgraph "IAM Users"
            PU1[운영팀장]
            PU2[시스템관리자]
        end
        
        subgraph "IAM Groups"
            PG1[ProductionAdmins]
            PG2[ReadOnlyUsers]
        end
        
        subgraph "IAM Roles"
            PR1[EC2-Production-Role]
            PR2[Lambda-Execution-Role]
            PR3[CrossAccount-Dev-Role]
        end
        
        subgraph "AWS Services"
            PEC2[Production EC2]
            PS3[Production S3]
            PRDS[Production RDS]
        end
    end
    
    PU1 --> PG1
    PU2 --> PG2
    
    PEC2 --> PR1
    PR1 --> PS3
    PR1 --> PRDS
    
    style PG1 fill:#ffcdd2
    style PG2 fill:#fff9c4
    style PR1 fill:#fff3e0
```

이러한 시각화 자료들은 IAM의 복잡한 개념들을 이해하기 쉽게 도와줍니다. 각 다이어그램은 특정 측면에 초점을 맞춰 IAM의 전체적인 작동 방식을 보여줍니다.