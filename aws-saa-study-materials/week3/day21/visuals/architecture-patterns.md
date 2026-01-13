# Day 21: 애플리케이션 아키텍처 패턴 다이어그램

## 개요

Week 3에서 학습한 AWS 서비스들을 활용한 다양한 애플리케이션 아키텍처 패턴을 시각적으로 표현합니다. 실제 프로덕션 환경에서 사용되는 검증된 패턴들을 통해 서비스 간의 관계와 데이터 흐름을 이해할 수 있습니다.

---

## 1. 현대적인 3-Tier 웹 애플리케이션

### 아키텍처 다이어그램

```mermaid
graph TB
    subgraph "사용자 계층"
        U[👤 사용자]
        M[📱 모바일 앱]
    end
    
    subgraph "글로벌 CDN"
        CF[☁️ CloudFront<br/>전 세계 엣지 로케이션]
    end
    
    subgraph "DNS & 라우팅"
        R53[🌐 Route 53<br/>DNS 관리]
    end
    
    subgraph "AWS 리전: us-east-1"
        subgraph "가용 영역 A"
            subgraph "퍼블릭 서브넷 A"
                ALB[⚖️ Application Load Balancer]
                NAT1[🔄 NAT Gateway]
            end
            subgraph "프라이빗 서브넷 A"
                WEB1[🖥️ 웹 서버<br/>EC2 Auto Scaling]
                APP1[⚙️ 앱 서버<br/>ECS Fargate]
            end
        end
        
        subgraph "가용 영역 B"
            subgraph "퍼블릭 서브넷 B"
                NAT2[🔄 NAT Gateway]
            end
            subgraph "프라이빗 서브넷 B"
                WEB2[🖥️ 웹 서버<br/>EC2 Auto Scaling]
                APP2[⚙️ 앱 서버<br/>ECS Fargate]
            end
        end
        
        subgraph "데이터베이스 서브넷"
            RDS_M[🗄️ RDS Primary<br/>Multi-AZ]
            RDS_S[🗄️ RDS Standby<br/>Multi-AZ]
            REDIS[⚡ ElastiCache<br/>Redis Cluster]
        end
        
        subgraph "스토리지"
            S3[📦 S3 Bucket<br/>정적 자산]
        end
    end
    
    subgraph "모니터링 & 로깅"
        CW[📊 CloudWatch<br/>메트릭 & 로그]
        XR[🔍 X-Ray<br/>분산 추적]
    end
    
    %% 연결 관계
    U --> R53
    M --> R53
    R53 --> CF
    CF --> ALB
    CF --> S3
    
    ALB --> WEB1
    ALB --> WEB2
    
    WEB1 --> APP1
    WEB2 --> APP2
    
    APP1 --> RDS_M
    APP2 --> RDS_M
    APP1 --> REDIS
    APP2 --> REDIS
    
    RDS_M -.-> RDS_S
    
    WEB1 --> CW
    WEB2 --> CW
    APP1 --> CW
    APP2 --> CW
    APP1 --> XR
    APP2 --> XR
    
    %% 스타일링
    classDef userLayer fill:#e1f5fe
    classDef cdnLayer fill:#f3e5f5
    classDef computeLayer fill:#e8f5e8
    classDef dataLayer fill:#fff3e0
    classDef monitorLayer fill:#fce4ec
    
    class U,M userLayer
    class CF,R53 cdnLayer
    class ALB,WEB1,WEB2,APP1,APP2 computeLayer
    class RDS_M,RDS_S,REDIS,S3 dataLayer
    class CW,XR monitorLayer
```

### 특징 및 장점

- **고가용성**: Multi-AZ 배포로 단일 장애점 제거
- **확장성**: Auto Scaling Group을 통한 자동 확장
- **성능**: CloudFront CDN으로 글로벌 성능 최적화
- **보안**: 프라이빗 서브넷에 애플리케이션 서버 배치
- **모니터링**: CloudWatch와 X-Ray를 통한 종합 모니터링

---

## 2. 서버리스 마이크로서비스 아키텍처

### 아키텍처 다이어그램

```mermaid
graph TB
    subgraph "클라이언트 계층"
        WEB[🌐 웹 애플리케이션]
        MOBILE[📱 모바일 앱]
        IOT[🔌 IoT 디바이스]
    end
    
    subgraph "API 게이트웨이 계층"
        APIGW[🚪 API Gateway<br/>REST API]
        COGNITO[🔐 Cognito<br/>사용자 인증]
    end
    
    subgraph "서버리스 마이크로서비스"
        subgraph "사용자 서비스"
            USER_LAMBDA[⚡ Lambda<br/>사용자 관리]
            USER_DDB[📊 DynamoDB<br/>사용자 데이터]
        end
        
        subgraph "주문 서비스"
            ORDER_LAMBDA[⚡ Lambda<br/>주문 처리]
            ORDER_RDS[🗄️ RDS<br/>주문 데이터]
        end
        
        subgraph "결제 서비스"
            PAY_LAMBDA[⚡ Lambda<br/>결제 처리]
            PAY_DDB[📊 DynamoDB<br/>결제 로그]
        end
        
        subgraph "알림 서비스"
            NOTIF_LAMBDA[⚡ Lambda<br/>알림 발송]
            SES[📧 SES<br/>이메일]
            SNS[📢 SNS<br/>푸시 알림]
        end
    end
    
    subgraph "이벤트 기반 통신"
        SQS_ORDER[📬 SQS<br/>주문 큐]
        SQS_PAY[📬 SQS<br/>결제 큐]
        SQS_NOTIF[📬 SQS<br/>알림 큐]
        EVENTBRIDGE[🔄 EventBridge<br/>이벤트 라우팅]
    end
    
    subgraph "스토리지 & 캐싱"
        S3[📦 S3<br/>파일 저장소]
        ELASTICACHE[⚡ ElastiCache<br/>세션 캐시]
    end
    
    subgraph "모니터링 & 보안"
        CLOUDWATCH[📊 CloudWatch<br/>로그 & 메트릭]
        XRAY[🔍 X-Ray<br/>분산 추적]
        WAF[🛡️ WAF<br/>웹 방화벽]
    end
    
    %% 연결 관계
    WEB --> APIGW
    MOBILE --> APIGW
    IOT --> APIGW
    
    APIGW --> COGNITO
    APIGW --> WAF
    
    APIGW --> USER_LAMBDA
    APIGW --> ORDER_LAMBDA
    APIGW --> PAY_LAMBDA
    
    USER_LAMBDA --> USER_DDB
    USER_LAMBDA --> ELASTICACHE
    
    ORDER_LAMBDA --> ORDER_RDS
    ORDER_LAMBDA --> EVENTBRIDGE
    
    PAY_LAMBDA --> PAY_DDB
    PAY_LAMBDA --> EVENTBRIDGE
    
    EVENTBRIDGE --> SQS_ORDER
    EVENTBRIDGE --> SQS_PAY
    EVENTBRIDGE --> SQS_NOTIF
    
    SQS_NOTIF --> NOTIF_LAMBDA
    NOTIF_LAMBDA --> SES
    NOTIF_LAMBDA --> SNS
    
    USER_LAMBDA --> S3
    ORDER_LAMBDA --> S3
    
    USER_LAMBDA --> CLOUDWATCH
    ORDER_LAMBDA --> CLOUDWATCH
    PAY_LAMBDA --> CLOUDWATCH
    NOTIF_LAMBDA --> CLOUDWATCH
    
    USER_LAMBDA --> XRAY
    ORDER_LAMBDA --> XRAY
    PAY_LAMBDA --> XRAY
    
    %% 스타일링
    classDef clientLayer fill:#e3f2fd
    classDef apiLayer fill:#f1f8e9
    classDef serviceLayer fill:#fff8e1
    classDef eventLayer fill:#fce4ec
    classDef storageLayer fill:#f3e5f5
    classDef monitorLayer fill:#e8eaf6
    
    class WEB,MOBILE,IOT clientLayer
    class APIGW,COGNITO apiLayer
    class USER_LAMBDA,ORDER_LAMBDA,PAY_LAMBDA,NOTIF_LAMBDA serviceLayer
    class SQS_ORDER,SQS_PAY,SQS_NOTIF,EVENTBRIDGE eventLayer
    class S3,ELASTICACHE,USER_DDB,ORDER_RDS,PAY_DDB storageLayer
    class CLOUDWATCH,XRAY,WAF monitorLayer
```

### 특징 및 장점

- **완전 서버리스**: 서버 관리 부담 없음
- **이벤트 기반**: 느슨한 결합으로 확장성 극대화
- **비용 효율성**: 사용한 만큼만 과금
- **자동 확장**: 트래픽에 따른 자동 스케일링
- **개발 생산성**: 인프라 관리 최소화

---

## 3. 하이브리드 컨테이너 아키텍처

### 아키텍처 다이어그램

```mermaid
graph TB
    subgraph "로드 밸런싱 계층"
        ALB[⚖️ Application Load Balancer]
        NLB[⚖️ Network Load Balancer]
    end
    
    subgraph "컨테이너 오케스트레이션"
        subgraph "ECS Cluster"
            subgraph "Fargate 서비스"
                WEB_FARGATE[🐳 웹 서비스<br/>ECS Fargate]
                API_FARGATE[🐳 API 서비스<br/>ECS Fargate]
            end
            
            subgraph "EC2 서비스"
                BATCH_EC2[🐳 배치 처리<br/>ECS on EC2]
                ML_EC2[🐳 ML 워크로드<br/>ECS on EC2]
            end
        end
        
        subgraph "EKS Cluster"
            K8S_MASTER[☸️ EKS Control Plane<br/>관리형]
            
            subgraph "워커 노드"
                MANAGED_NG[☸️ Managed Node Group<br/>EC2 Auto Scaling]
                FARGATE_NG[☸️ Fargate Profile<br/>서버리스 파드]
            end
        end
    end
    
    subgraph "서비스 메시"
        APP_MESH[🕸️ AWS App Mesh<br/>서비스 메시]
    end
    
    subgraph "컨테이너 레지스트리"
        ECR[📦 ECR<br/>컨테이너 이미지]
    end
    
    subgraph "데이터 계층"
        RDS[🗄️ RDS<br/>관계형 DB]
        DOCUMENTDB[📄 DocumentDB<br/>MongoDB 호환]
        ELASTICACHE[⚡ ElastiCache<br/>인메모리 캐시]
    end
    
    subgraph "스토리지"
        EFS[📁 EFS<br/>공유 파일 시스템]
        S3[📦 S3<br/>객체 스토리지]
    end
    
    subgraph "CI/CD 파이프라인"
        CODECOMMIT[📝 CodeCommit<br/>소스 코드]
        CODEBUILD[🔨 CodeBuild<br/>빌드 & 테스트]
        CODEPIPELINE[🚀 CodePipeline<br/>배포 파이프라인]
    end
    
    subgraph "모니터링 & 로깅"
        CLOUDWATCH[📊 CloudWatch<br/>메트릭 & 로그]
        PROMETHEUS[📈 Prometheus<br/>Kubernetes 메트릭]
        GRAFANA[📊 Grafana<br/>대시보드]
    end
    
    %% 연결 관계
    ALB --> WEB_FARGATE
    ALB --> API_FARGATE
    NLB --> MANAGED_NG
    
    WEB_FARGATE --> API_FARGATE
    API_FARGATE --> RDS
    API_FARGATE --> ELASTICACHE
    
    BATCH_EC2 --> DOCUMENTDB
    ML_EC2 --> S3
    
    MANAGED_NG --> RDS
    FARGATE_NG --> DOCUMENTDB
    
    WEB_FARGATE --> EFS
    API_FARGATE --> EFS
    MANAGED_NG --> EFS
    
    APP_MESH --> WEB_FARGATE
    APP_MESH --> API_FARGATE
    APP_MESH --> MANAGED_NG
    
    CODECOMMIT --> CODEBUILD
    CODEBUILD --> ECR
    CODEBUILD --> CODEPIPELINE
    CODEPIPELINE --> WEB_FARGATE
    CODEPIPELINE --> MANAGED_NG
    
    WEB_FARGATE --> CLOUDWATCH
    API_FARGATE --> CLOUDWATCH
    MANAGED_NG --> PROMETHEUS
    PROMETHEUS --> GRAFANA
    
    %% 스타일링
    classDef lbLayer fill:#e8f5e8
    classDef containerLayer fill:#e3f2fd
    classDef dataLayer fill:#fff3e0
    classDef cicdLayer fill:#f1f8e9
    classDef monitorLayer fill:#fce4ec
    
    class ALB,NLB lbLayer
    class WEB_FARGATE,API_FARGATE,BATCH_EC2,ML_EC2,MANAGED_NG,FARGATE_NG,ECR containerLayer
    class RDS,DOCUMENTDB,ELASTICACHE,EFS,S3 dataLayer
    class CODECOMMIT,CODEBUILD,CODEPIPELINE cicdLayer
    class CLOUDWATCH,PROMETHEUS,GRAFANA monitorLayer
```

### 특징 및 장점

- **유연한 컴퓨팅**: Fargate와 EC2 혼합 사용
- **다중 오케스트레이션**: ECS와 EKS 동시 활용
- **서비스 메시**: App Mesh로 마이크로서비스 통신 관리
- **완전한 CI/CD**: 컨테이너 기반 자동화 파이프라인
- **통합 모니터링**: AWS와 오픈소스 도구 조합

---

## 4. 글로벌 멀티 리전 아키텍처

### 아키텍처 다이어그램

```mermaid
graph TB
    subgraph "글로벌 서비스"
        R53[🌐 Route 53<br/>글로벌 DNS]
        CF[☁️ CloudFront<br/>글로벌 CDN]
        WAF[🛡️ WAF<br/>글로벌 보안]
    end
    
    subgraph "미국 리전 (us-east-1)"
        subgraph "US 컴퓨팅"
            US_ALB[⚖️ ALB]
            US_ECS[🐳 ECS Fargate]
            US_LAMBDA[⚡ Lambda]
        end
        
        subgraph "US 데이터"
            US_RDS[🗄️ RDS Primary]
            US_DDB[📊 DynamoDB]
            US_S3[📦 S3 Bucket]
        end
    end
    
    subgraph "유럽 리전 (eu-west-1)"
        subgraph "EU 컴퓨팅"
            EU_ALB[⚖️ ALB]
            EU_ECS[🐳 ECS Fargate]
            EU_LAMBDA[⚡ Lambda]
        end
        
        subgraph "EU 데이터"
            EU_RDS[🗄️ RDS Primary]
            EU_DDB[📊 DynamoDB]
            EU_S3[📦 S3 Bucket]
        end
    end
    
    subgraph "아시아 리전 (ap-northeast-1)"
        subgraph "ASIA 컴퓨팅"
            ASIA_ALB[⚖️ ALB]
            ASIA_ECS[🐳 ECS Fargate]
            ASIA_LAMBDA[⚡ Lambda]
        end
        
        subgraph "ASIA 데이터"
            ASIA_RDS[🗄️ RDS Primary]
            ASIA_DDB[📊 DynamoDB]
            ASIA_S3[📦 S3 Bucket]
        end
    end
    
    subgraph "데이터 동기화"
        DDB_GLOBAL[🔄 DynamoDB<br/>Global Tables]
        S3_CRR[🔄 S3<br/>Cross-Region Replication]
        RDS_REPLICA[🔄 RDS<br/>Cross-Region Read Replica]
    end
    
    subgraph "글로벌 모니터링"
        CW_GLOBAL[📊 CloudWatch<br/>Cross-Region Dashboard]
        HEALTH_CHECK[❤️ Route 53<br/>Health Checks]
    end
    
    %% 사용자 연결
    R53 --> CF
    CF --> WAF
    
    %% 지역별 라우팅
    R53 -.->|"Geolocation: US"| US_ALB
    R53 -.->|"Geolocation: EU"| EU_ALB
    R53 -.->|"Geolocation: ASIA"| ASIA_ALB
    
    %% 리전 내 연결
    US_ALB --> US_ECS
    US_ECS --> US_RDS
    US_ECS --> US_DDB
    US_LAMBDA --> US_S3
    
    EU_ALB --> EU_ECS
    EU_ECS --> EU_RDS
    EU_ECS --> EU_DDB
    EU_LAMBDA --> EU_S3
    
    ASIA_ALB --> ASIA_ECS
    ASIA_ECS --> ASIA_RDS
    ASIA_ECS --> ASIA_DDB
    ASIA_LAMBDA --> ASIA_S3
    
    %% 데이터 동기화
    US_DDB -.-> DDB_GLOBAL
    EU_DDB -.-> DDB_GLOBAL
    ASIA_DDB -.-> DDB_GLOBAL
    
    US_S3 -.-> S3_CRR
    EU_S3 -.-> S3_CRR
    ASIA_S3 -.-> S3_CRR
    
    US_RDS -.-> RDS_REPLICA
    EU_RDS -.-> RDS_REPLICA
    ASIA_RDS -.-> RDS_REPLICA
    
    %% 헬스 체크
    HEALTH_CHECK --> US_ALB
    HEALTH_CHECK --> EU_ALB
    HEALTH_CHECK --> ASIA_ALB
    
    %% 모니터링
    US_ECS --> CW_GLOBAL
    EU_ECS --> CW_GLOBAL
    ASIA_ECS --> CW_GLOBAL
    
    %% 스타일링
    classDef globalLayer fill:#e1f5fe
    classDef usLayer fill:#e8f5e8
    classDef euLayer fill:#fff3e0
    classDef asiaLayer fill:#fce4ec
    classDef syncLayer fill:#f3e5f5
    classDef monitorLayer fill:#e8eaf6
    
    class R53,CF,WAF globalLayer
    class US_ALB,US_ECS,US_LAMBDA,US_RDS,US_DDB,US_S3 usLayer
    class EU_ALB,EU_ECS,EU_LAMBDA,EU_RDS,EU_DDB,EU_S3 euLayer
    class ASIA_ALB,ASIA_ECS,ASIA_LAMBDA,ASIA_RDS,ASIA_DDB,ASIA_S3 asiaLayer
    class DDB_GLOBAL,S3_CRR,RDS_REPLICA syncLayer
    class CW_GLOBAL,HEALTH_CHECK monitorLayer
```

### 특징 및 장점

- **글로벌 가용성**: 다중 리전으로 99.99% 이상 가용성
- **지연시간 최적화**: 사용자 근접 리전에서 서비스 제공
- **데이터 주권**: 지역별 데이터 규정 준수 (GDPR 등)
- **재해 복구**: 리전 장애 시 자동 페일오버
- **확장성**: 지역별 독립적인 확장 가능

---

## 5. 이벤트 기반 데이터 파이프라인

### 아키텍처 다이어그램

```mermaid
graph TB
    subgraph "데이터 소스"
        WEB_APP[🌐 웹 애플리케이션]
        MOBILE_APP[📱 모바일 앱]
        IOT_DEVICES[🔌 IoT 디바이스]
        THIRD_PARTY[🔗 외부 API]
    end
    
    subgraph "데이터 수집"
        KINESIS_STREAMS[🌊 Kinesis Data Streams<br/>실시간 스트리밍]
        KINESIS_FIREHOSE[🚰 Kinesis Data Firehose<br/>배치 전송]
        API_GATEWAY[🚪 API Gateway<br/>REST/WebSocket]
    end
    
    subgraph "실시간 처리"
        LAMBDA_PROCESSOR[⚡ Lambda<br/>실시간 처리]
        KINESIS_ANALYTICS[📊 Kinesis Analytics<br/>스트림 분석]
        MSK[📨 MSK<br/>Kafka 클러스터]
    end
    
    subgraph "배치 처리"
        EMR[🔥 EMR<br/>Spark/Hadoop]
        GLUE[🔧 Glue<br/>ETL 작업]
        BATCH[⚙️ AWS Batch<br/>대용량 처리]
    end
    
    subgraph "데이터 저장소"
        S3_RAW[📦 S3 Raw Data<br/>원시 데이터]
        S3_PROCESSED[📦 S3 Processed<br/>처리된 데이터]
        REDSHIFT[🏢 Redshift<br/>데이터 웨어하우스]
        DYNAMODB[📊 DynamoDB<br/>NoSQL DB]
        TIMESTREAM[⏰ Timestream<br/>시계열 DB]
    end
    
    subgraph "데이터 카탈로그"
        GLUE_CATALOG[📚 Glue Data Catalog<br/>메타데이터]
        LAKE_FORMATION[🏞️ Lake Formation<br/>데이터 레이크 관리]
    end
    
    subgraph "분석 & 시각화"
        ATHENA[🔍 Athena<br/>서버리스 쿼리]
        QUICKSIGHT[📈 QuickSight<br/>BI 대시보드]
        SAGEMAKER[🤖 SageMaker<br/>머신러닝]
    end
    
    subgraph "알림 & 모니터링"
        SNS[📢 SNS<br/>알림]
        CLOUDWATCH[📊 CloudWatch<br/>모니터링]
        EVENTBRIDGE[🔄 EventBridge<br/>이벤트 라우팅]
    end
    
    %% 데이터 흐름
    WEB_APP --> API_GATEWAY
    MOBILE_APP --> API_GATEWAY
    IOT_DEVICES --> KINESIS_STREAMS
    THIRD_PARTY --> KINESIS_FIREHOSE
    
    API_GATEWAY --> KINESIS_STREAMS
    KINESIS_STREAMS --> LAMBDA_PROCESSOR
    KINESIS_STREAMS --> KINESIS_ANALYTICS
    KINESIS_STREAMS --> MSK
    
    LAMBDA_PROCESSOR --> DYNAMODB
    LAMBDA_PROCESSOR --> TIMESTREAM
    LAMBDA_PROCESSOR --> EVENTBRIDGE
    
    KINESIS_FIREHOSE --> S3_RAW
    KINESIS_ANALYTICS --> S3_PROCESSED
    
    S3_RAW --> GLUE
    GLUE --> S3_PROCESSED
    S3_RAW --> EMR
    EMR --> S3_PROCESSED
    S3_RAW --> BATCH
    BATCH --> REDSHIFT
    
    S3_PROCESSED --> GLUE_CATALOG
    GLUE_CATALOG --> LAKE_FORMATION
    
    S3_PROCESSED --> ATHENA
    REDSHIFT --> QUICKSIGHT
    ATHENA --> QUICKSIGHT
    
    S3_PROCESSED --> SAGEMAKER
    DYNAMODB --> SAGEMAKER
    
    EVENTBRIDGE --> SNS
    LAMBDA_PROCESSOR --> CLOUDWATCH
    GLUE --> CLOUDWATCH
    
    %% 스타일링
    classDef sourceLayer fill:#e3f2fd
    classDef ingestionLayer fill:#e8f5e8
    classDef processingLayer fill:#fff8e1
    classDef storageLayer fill:#f3e5f5
    classDef catalogLayer fill:#fce4ec
    classDef analyticsLayer fill:#e8eaf6
    classDef monitorLayer fill:#fff3e0
    
    class WEB_APP,MOBILE_APP,IOT_DEVICES,THIRD_PARTY sourceLayer
    class KINESIS_STREAMS,KINESIS_FIREHOSE,API_GATEWAY ingestionLayer
    class LAMBDA_PROCESSOR,KINESIS_ANALYTICS,MSK,EMR,GLUE,BATCH processingLayer
    class S3_RAW,S3_PROCESSED,REDSHIFT,DYNAMODB,TIMESTREAM storageLayer
    class GLUE_CATALOG,LAKE_FORMATION catalogLayer
    class ATHENA,QUICKSIGHT,SAGEMAKER analyticsLayer
    class SNS,CLOUDWATCH,EVENTBRIDGE monitorLayer
```

### 특징 및 장점

- **실시간 처리**: Kinesis를 통한 스트리밍 데이터 처리
- **확장 가능한 배치**: EMR과 Glue를 통한 대용량 데이터 처리
- **서버리스 분석**: Athena를 통한 즉석 쿼리
- **통합 카탈로그**: Glue Data Catalog로 메타데이터 관리
- **머신러닝 통합**: SageMaker를 통한 AI/ML 파이프라인

---

## 6. 보안 강화 엔터프라이즈 아키텍처

### 아키텍처 다이어그램

```mermaid
graph TB
    subgraph "외부 접근"
        INTERNET[🌐 인터넷]
        CORPORATE[🏢 기업 네트워크]
    end
    
    subgraph "보안 경계"
        WAF[🛡️ WAF<br/>웹 방화벽]
        SHIELD[🛡️ Shield Advanced<br/>DDoS 보호]
        CLOUDFRONT[☁️ CloudFront<br/>CDN + 보안]
    end
    
    subgraph "네트워크 보안"
        VPC[🏠 VPC<br/>격리된 네트워크]
        
        subgraph "DMZ (퍼블릭 서브넷)"
            ALB[⚖️ ALB<br/>로드 밸런서]
            NAT[🔄 NAT Gateway]
            BASTION[🚪 Bastion Host<br/>점프 서버]
        end
        
        subgraph "애플리케이션 계층 (프라이빗 서브넷)"
            WEB_SERVERS[🖥️ 웹 서버<br/>Auto Scaling]
            APP_SERVERS[⚙️ 앱 서버<br/>ECS Fargate]
        end
        
        subgraph "데이터 계층 (DB 서브넷)"
            RDS[🗄️ RDS<br/>암호화된 DB]
            ELASTICACHE[⚡ ElastiCache<br/>암호화된 캐시]
        end
    end
    
    subgraph "ID 및 액세스 관리"
        COGNITO[🔐 Cognito<br/>사용자 인증]
        IAM[👤 IAM<br/>역할 기반 접근]
        DIRECTORY[📁 Directory Service<br/>AD 통합]
        SSO[🔑 SSO<br/>Single Sign-On]
    end
    
    subgraph "암호화 및 키 관리"
        KMS[🔐 KMS<br/>키 관리]
        SECRETS[🤫 Secrets Manager<br/>비밀 관리]
        PARAMETER[📋 Parameter Store<br/>구성 관리]
    end
    
    subgraph "보안 모니터링"
        GUARDDUTY[👁️ GuardDuty<br/>위협 탐지]
        INSPECTOR[🔍 Inspector<br/>취약점 평가]
        MACIE[🕵️ Macie<br/>데이터 보안]
        SECURITYHUB[🛡️ Security Hub<br/>보안 통합]
    end
    
    subgraph "규정 준수"
        CLOUDTRAIL[📝 CloudTrail<br/>API 감사]
        CONFIG[⚙️ Config<br/>구성 추적]
        TRUSTED_ADVISOR[✅ Trusted Advisor<br/>보안 권장사항]
    end
    
    subgraph "네트워크 연결"
        VPN[🔒 VPN Gateway<br/>사이트 간 VPN]
        DIRECT_CONNECT[⚡ Direct Connect<br/>전용 연결]
        TRANSIT_GW[🔄 Transit Gateway<br/>네트워크 허브]
    end
    
    %% 연결 관계
    INTERNET --> SHIELD
    SHIELD --> WAF
    WAF --> CLOUDFRONT
    CLOUDFRONT --> ALB
    
    CORPORATE --> VPN
    CORPORATE --> DIRECT_CONNECT
    VPN --> TRANSIT_GW
    DIRECT_CONNECT --> TRANSIT_GW
    TRANSIT_GW --> VPC
    
    ALB --> WEB_SERVERS
    WEB_SERVERS --> APP_SERVERS
    APP_SERVERS --> RDS
    APP_SERVERS --> ELASTICACHE
    
    BASTION --> WEB_SERVERS
    BASTION --> APP_SERVERS
    
    COGNITO --> IAM
    DIRECTORY --> SSO
    SSO --> IAM
    
    APP_SERVERS --> KMS
    RDS --> KMS
    APP_SERVERS --> SECRETS
    APP_SERVERS --> PARAMETER
    
    VPC --> GUARDDUTY
    WEB_SERVERS --> INSPECTOR
    RDS --> MACIE
    GUARDDUTY --> SECURITYHUB
    INSPECTOR --> SECURITYHUB
    MACIE --> SECURITYHUB
    
    ALB --> CLOUDTRAIL
    IAM --> CLOUDTRAIL
    VPC --> CONFIG
    SECURITYHUB --> TRUSTED_ADVISOR
    
    %% 스타일링
    classDef externalLayer fill:#ffebee
    classDef securityLayer fill:#e8f5e8
    classDef networkLayer fill:#e3f2fd
    classDef iamLayer fill:#fff3e0
    classDef cryptoLayer fill:#f3e5f5
    classDef monitorLayer fill:#fce4ec
    classDef complianceLayer fill:#e8eaf6
    classDef connectLayer fill:#f1f8e9
    
    class INTERNET,CORPORATE externalLayer
    class WAF,SHIELD,CLOUDFRONT securityLayer
    class VPC,ALB,NAT,BASTION,WEB_SERVERS,APP_SERVERS,RDS,ELASTICACHE networkLayer
    class COGNITO,IAM,DIRECTORY,SSO iamLayer
    class KMS,SECRETS,PARAMETER cryptoLayer
    class GUARDDUTY,INSPECTOR,MACIE,SECURITYHUB monitorLayer
    class CLOUDTRAIL,CONFIG,TRUSTED_ADVISOR complianceLayer
    class VPN,DIRECT_CONNECT,TRANSIT_GW connectLayer
```

### 특징 및 장점

- **다층 보안**: 네트워크부터 애플리케이션까지 전방위 보안
- **제로 트러스트**: 모든 접근에 대한 검증 및 암호화
- **통합 모니터링**: Security Hub를 통한 중앙집중식 보안 관리
- **규정 준수**: CloudTrail과 Config를 통한 감사 추적
- **하이브리드 연결**: 온프레미스와 안전한 연결

---

## 아키텍처 패턴 선택 가이드

### 1. 비즈니스 요구사항별 패턴 선택

| 요구사항 | 권장 패턴 | 주요 고려사항 |
|---------|----------|-------------|
| **전통적인 웹 애플리케이션** | 3-Tier 아키텍처 | 안정성, 예측 가능한 성능 |
| **빠른 개발 및 배포** | 서버리스 마이크로서비스 | 개발 속도, 운영 부담 최소화 |
| **복잡한 애플리케이션** | 하이브리드 컨테이너 | 유연성, 다양한 워크로드 지원 |
| **글로벌 서비스** | 멀티 리전 아키텍처 | 지연시간, 데이터 주권 |
| **데이터 중심 비즈니스** | 이벤트 기반 파이프라인 | 실시간 분석, 확장성 |
| **엔터프라이즈 환경** | 보안 강화 아키텍처 | 규정 준수, 보안 요구사항 |

### 2. 기술적 고려사항

#### 확장성 요구사항
- **수직 확장**: 전통적인 3-Tier
- **수평 확장**: 마이크로서비스, 컨테이너
- **자동 확장**: 서버리스, Fargate

#### 운영 복잡성
- **낮은 복잡성**: 서버리스
- **중간 복잡성**: 관리형 컨테이너 (Fargate)
- **높은 복잡성**: 자체 관리 EC2, Kubernetes

#### 비용 최적화
- **예측 가능한 워크로드**: Reserved Instance, Savings Plans
- **가변적인 워크로드**: 서버리스, Spot Instance
- **개발/테스트 환경**: Fargate, Lambda

### 3. 마이그레이션 전략

#### Lift and Shift
1. 기존 애플리케이션을 EC2로 이전
2. 점진적으로 관리형 서비스 도입
3. 마이크로서비스로 분해

#### Re-architecting
1. 서버리스 우선 접근
2. 컨테이너 기반 현대화
3. 이벤트 기반 아키텍처 도입

---

## 실습 권장사항

### 1. 단계별 학습 경로

1. **기초**: 3-Tier 아키텍처 구축
2. **중급**: 서버리스 마이크로서비스 구현
3. **고급**: 하이브리드 컨테이너 환경 구성
4. **전문가**: 글로벌 멀티 리전 배포

### 2. 핸즈온 프로젝트

- **Week 3 통합 실습**: Day 21 마이크로서비스 아키텍처
- **보안 강화**: WAF, GuardDuty 설정
- **모니터링 구성**: CloudWatch 대시보드 생성
- **CI/CD 파이프라인**: CodePipeline 구축

### 3. 성능 최적화

- **캐싱 전략**: CloudFront, ElastiCache 활용
- **데이터베이스 최적화**: Read Replica, 인덱싱
- **네트워크 최적화**: VPC Endpoint, Direct Connect

---

이러한 아키텍처 패턴들은 실제 프로덕션 환경에서 검증된 설계입니다. 각 패턴의 특징을 이해하고 비즈니스 요구사항에 맞는 최적의 조합을 선택하여 활용하시기 바랍니다! 🚀