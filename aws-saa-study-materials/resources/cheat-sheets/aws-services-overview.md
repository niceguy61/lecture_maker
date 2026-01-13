# AWS 서비스별 치트 시트

## 컴퓨팅 서비스 (Compute)

### Amazon EC2 (Elastic Compute Cloud)
- **목적**: 클라우드에서 확장 가능한 컴퓨팅 용량 제공
- **주요 기능**:
  - 다양한 인스턴스 타입 (t3, m5, c5, r5, etc.)
  - Auto Scaling 지원
  - Spot 인스턴스로 비용 절약
- **가격 모델**: On-Demand, Reserved, Spot
- **사용 사례**: 웹 서버, 애플리케이션 서버, 배치 처리
- **시험 포인트**: 인스턴스 타입 선택, 보안 그룹, 키 페어

### AWS Lambda
- **목적**: 서버리스 컴퓨팅 서비스
- **주요 기능**:
  - 이벤트 기반 실행
  - 자동 스케일링
  - 15분 최대 실행 시간
- **가격 모델**: 요청 수 + 실행 시간
- **사용 사례**: API 백엔드, 데이터 처리, IoT 백엔드
- **시험 포인트**: 트리거 유형, 메모리/시간 제한, VPC 연결

### Amazon ECS/EKS
- **ECS**: Docker 컨테이너 오케스트레이션
- **EKS**: 관리형 Kubernetes 서비스
- **Fargate**: 서버리스 컨테이너 실행
- **사용 사례**: 마이크로서비스, 컨테이너화된 애플리케이션
- **시험 포인트**: EC2 vs Fargate 런치 타입

## 스토리지 서비스 (Storage)

### Amazon S3 (Simple Storage Service)
- **목적**: 객체 스토리지 서비스
- **스토리지 클래스**:
  - Standard: 자주 액세스하는 데이터
  - IA (Infrequent Access): 가끔 액세스
  - Glacier: 아카이브용 (분~시간 검색)
  - Deep Archive: 장기 아카이브 (12시간 검색)
- **주요 기능**: 버전 관리, 암호화, 정적 웹사이트 호스팅
- **시험 포인트**: 스토리지 클래스 선택, 수명 주기 정책

### Amazon EBS (Elastic Block Store)
- **목적**: EC2용 블록 스토리지
- **볼륨 타입**:
  - gp3/gp2: 범용 SSD
  - io2/io1: 프로비저닝된 IOPS SSD
  - st1: 처리량 최적화 HDD
  - sc1: 콜드 HDD
- **주요 기능**: 스냅샷, 암호화, 다중 연결
- **시험 포인트**: 볼륨 타입 선택, 스냅샷 전략

### Amazon EFS (Elastic File System)
- **목적**: 완전 관리형 NFS 파일 시스템
- **주요 기능**: 다중 AZ 액세스, 자동 스케일링
- **성능 모드**: General Purpose, Max I/O
- **처리량 모드**: Provisioned, Bursting
- **시험 포인트**: EBS vs EFS 차이점

## 데이터베이스 서비스 (Database)

### Amazon RDS (Relational Database Service)
- **지원 엔진**: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora
- **주요 기능**:
  - 자동 백업 및 패치
  - Multi-AZ 배포 (고가용성)
  - Read Replica (읽기 성능 향상)
- **Aurora**: AWS 클라우드 네이티브 DB
- **시험 포인트**: Multi-AZ vs Read Replica, Aurora 특징

### Amazon DynamoDB
- **목적**: NoSQL 데이터베이스
- **주요 기능**:
  - 완전 관리형
  - 자동 스케일링
  - Global Tables (다중 리전)
- **일관성**: Eventually Consistent, Strongly Consistent
- **시험 포인트**: RDS vs DynamoDB 선택 기준

## 네트워킹 서비스 (Networking)

### Amazon VPC (Virtual Private Cloud)
- **목적**: 격리된 가상 네트워크 환경
- **구성 요소**:
  - 서브넷 (Public/Private)
  - 인터넷 게이트웨이
  - NAT 게이트웨이/인스턴스
  - 라우팅 테이블
- **보안**: Security Groups, NACLs
- **시험 포인트**: 서브넷 설계, 라우팅 구성

### Elastic Load Balancer (ELB)
- **타입**:
  - ALB (Application): HTTP/HTTPS (Layer 7)
  - NLB (Network): TCP/UDP (Layer 4)
  - CLB (Classic): 레거시
- **주요 기능**: 헬스 체크, SSL 종료, 스티키 세션
- **시험 포인트**: 로드 밸런서 타입 선택

### Amazon CloudFront
- **목적**: 글로벌 CDN 서비스
- **주요 기능**:
  - 엣지 로케이션 캐싱
  - Origin Shield
  - Lambda@Edge
- **사용 사례**: 정적 콘텐츠 배포, API 가속화
- **시험 포인트**: 캐싱 전략, Origin 설정

### Amazon Route 53
- **목적**: DNS 웹 서비스
- **라우팅 정책**:
  - Simple: 단일 리소스
  - Weighted: 가중치 기반
  - Latency: 지연 시간 기반
  - Failover: 장애 조치
  - Geolocation: 지리적 위치 기반
- **시험 포인트**: 라우팅 정책 선택

## 보안 서비스 (Security)

### AWS IAM (Identity and Access Management)
- **구성 요소**:
  - Users: 개별 사용자
  - Groups: 사용자 그룹
  - Roles: 임시 권한
  - Policies: 권한 정의
- **원칙**: 최소 권한 원칙
- **시험 포인트**: Role vs User, Policy 작성

### AWS KMS (Key Management Service)
- **목적**: 암호화 키 관리
- **키 타입**: Customer Managed, AWS Managed
- **주요 기능**: 키 회전, 감사 로깅
- **시험 포인트**: 암호화 at-rest, in-transit

## 모니터링 서비스 (Monitoring)

### Amazon CloudWatch
- **목적**: 모니터링 및 관찰 가능성
- **구성 요소**:
  - Metrics: 성능 지표
  - Logs: 로그 수집 및 분석
  - Alarms: 임계값 기반 알림
  - Events/EventBridge: 이벤트 기반 자동화
- **시험 포인트**: 커스텀 메트릭, 로그 그룹

### AWS CloudTrail
- **목적**: API 호출 감사 로깅
- **주요 기능**: 관리 이벤트, 데이터 이벤트 추적
- **사용 사례**: 보안 감사, 규정 준수
- **시험 포인트**: CloudWatch vs CloudTrail 차이

## 애플리케이션 서비스 (Application)

### Amazon API Gateway
- **목적**: API 생성, 배포, 관리
- **타입**: REST API, HTTP API, WebSocket API
- **주요 기능**: 인증, 스로틀링, 캐싱
- **시험 포인트**: Lambda와 통합

### Amazon SQS (Simple Queue Service)
- **목적**: 완전 관리형 메시지 큐
- **타입**: Standard Queue, FIFO Queue
- **주요 기능**: Dead Letter Queue, 가시성 타임아웃
- **시험 포인트**: SQS vs SNS 차이

### Amazon SNS (Simple Notification Service)
- **목적**: 게시-구독 메시징 서비스
- **주요 기능**: 다중 프로토콜 지원 (SMS, 이메일, HTTP)
- **사용 사례**: 알림, 팬아웃 패턴
- **시험 포인트**: Push vs Pull 모델

## 관리 도구 (Management)

### AWS CloudFormation
- **목적**: 인프라스트럭처 as Code
- **주요 기능**: 스택 관리, 롤백, 드리프트 감지
- **템플릿**: JSON/YAML 형식
- **시험 포인트**: 스택 업데이트 정책

### AWS Systems Manager
- **목적**: 운영 데이터 중앙 집중화
- **주요 기능**: Parameter Store, Session Manager, Patch Manager
- **사용 사례**: 구성 관리, 패치 관리
- **시험 포인트**: Parameter Store vs Secrets Manager

## 비용 관리 (Cost Management)

### AWS Cost Explorer
- **목적**: 비용 분석 및 예측
- **주요 기능**: 비용 시각화, 예산 설정
- **사용 사례**: 비용 최적화, 예산 관리

### AWS Trusted Advisor
- **목적**: 모범 사례 권장사항 제공
- **카테고리**: 비용 최적화, 성능, 보안, 내결함성
- **시험 포인트**: Support 플랜별 기능 차이

---

## 시험 팁

### 서비스 선택 기준
1. **컴퓨팅**: 워크로드 특성에 따른 선택
2. **스토리지**: 액세스 패턴과 성능 요구사항
3. **데이터베이스**: 데이터 구조와 일관성 요구사항
4. **네트워킹**: 트래픽 패턴과 보안 요구사항

### 자주 나오는 시나리오
- 고가용성 아키텍처 설계
- 비용 최적화 전략
- 보안 모범 사례 적용
- 성능 최적화 방법
- 재해 복구 계획

### 핵심 개념
- **Well-Architected Framework**: 5개 기둥
- **Shared Responsibility Model**: 보안 책임 분담
- **CAP Theorem**: 일관성, 가용성, 분할 내성
- **RTO/RPO**: 복구 목표 시간/지점