# Day 26 종합 실습 프로젝트 체크리스트

## 📋 개요

이 체크리스트는 엔터프라이즈급 3-Tier 웹 애플리케이션 구축 실습의 모든 단계를 체계적으로 관리하기 위한 도구입니다. 각 단계를 완료할 때마다 체크박스를 표시하여 진행 상황을 추적하세요.

## ⏱️ 시간 관리

- **총 예상 시간**: 4-6시간
- **권장 진행 방식**: 2-3시간씩 나누어 진행
- **휴식 시간**: 각 Phase 완료 후 10-15분 휴식

---

## 🚀 Phase 1: 네트워크 인프라 구축 (60분)

### ✅ Step 1.1: VPC 및 서브넷 생성

- [ ] **VPC 생성 완료**
  - [ ] VPC 이름: `enterprise-webapp-vpc`
  - [ ] CIDR 블록: `10.0.0.0/16`
  - [ ] DNS 호스트 이름 활성화
  - [ ] DNS 확인 활성화

- [ ] **서브넷 생성 완료 (총 6개)**
  - [ ] Public Subnet A: `10.0.1.0/24` (us-east-1a)
  - [ ] Public Subnet B: `10.0.2.0/24` (us-east-1b)
  - [ ] Private Subnet A: `10.0.11.0/24` (us-east-1a)
  - [ ] Private Subnet B: `10.0.12.0/24` (us-east-1b)
  - [ ] Database Subnet A: `10.0.21.0/24` (us-east-1a)
  - [ ] Database Subnet B: `10.0.22.0/24` (us-east-1b)

- [ ] **인터넷 게이트웨이 생성 및 연결**
  - [ ] IGW 생성: `enterprise-webapp-igw`
  - [ ] VPC에 연결 완료

### ✅ Step 1.2: 라우팅 테이블 구성

- [ ] **Public Route Table 설정**
  - [ ] 이름: `enterprise-webapp-public-rt`
  - [ ] 라우트 추가: `0.0.0.0/0` → Internet Gateway
  - [ ] Public Subnet A, B 연결

- [ ] **Private Route Table A 설정**
  - [ ] 이름: `enterprise-webapp-private-rt-a`
  - [ ] Private Subnet A 연결
  - [ ] NAT Gateway A 라우트 추가 (Step 1.3 완료 후)

- [ ] **Private Route Table B 설정**
  - [ ] 이름: `enterprise-webapp-private-rt-b`
  - [ ] Private Subnet B 연결
  - [ ] NAT Gateway B 라우트 추가 (Step 1.3 완료 후)

### ✅ Step 1.3: NAT Gateway 생성

- [ ] **NAT Gateway A 생성**
  - [ ] 서브넷: Public Subnet A
  - [ ] Elastic IP 할당
  - [ ] 이름: `enterprise-webapp-nat-a`

- [ ] **NAT Gateway B 생성**
  - [ ] 서브넷: Public Subnet B
  - [ ] Elastic IP 할당
  - [ ] 이름: `enterprise-webapp-nat-b`

- [ ] **Private Route Tables 업데이트**
  - [ ] Private RT A에 NAT Gateway A 라우트 추가
  - [ ] Private RT B에 NAT Gateway B 라우트 추가

### 🔍 Phase 1 검증

- [ ] **연결성 테스트**
  - [ ] Public 서브넷에서 인터넷 접근 가능
  - [ ] Private 서브넷에서 NAT Gateway를 통한 인터넷 접근 가능
  - [ ] 모든 서브넷 간 통신 가능

---

## 🔒 Phase 2: 보안 그룹 및 IAM 설정 (45분)

### ✅ Step 2.1: 보안 그룹 생성

- [ ] **ALB Security Group**
  - [ ] 이름: `enterprise-webapp-alb-sg`
  - [ ] 인바운드: HTTP (80) from 0.0.0.0/0
  - [ ] 인바운드: HTTPS (443) from 0.0.0.0/0
  - [ ] 아웃바운드: All traffic

- [ ] **Web Server Security Group**
  - [ ] 이름: `enterprise-webapp-web-sg`
  - [ ] 인바운드: HTTP (80) from ALB SG
  - [ ] 인바운드: HTTPS (443) from ALB SG
  - [ ] 인바운드: SSH (22) from Bastion SG (선택사항)
  - [ ] 아웃바운드: All traffic

- [ ] **Database Security Group**
  - [ ] 이름: `enterprise-webapp-db-sg`
  - [ ] 인바운드: MySQL (3306) from Web Server SG
  - [ ] 인바운드: MySQL (3306) from Lambda SG
  - [ ] 아웃바운드: None

- [ ] **Cache Security Group**
  - [ ] 이름: `enterprise-webapp-cache-sg`
  - [ ] 인바운드: Redis (6379) from Web Server SG
  - [ ] 인바운드: Redis (6379) from Lambda SG
  - [ ] 아웃바운드: None

### ✅ Step 2.2: IAM 역할 생성

- [ ] **EC2 Instance Role**
  - [ ] 역할 이름: `EnterpriseWebAppEC2Role`
  - [ ] 신뢰 관계: EC2 서비스
  - [ ] 정책: S3 읽기/쓰기, CloudWatch 메트릭, 로그 권한
  - [ ] 인스턴스 프로파일 생성

- [ ] **Lambda Execution Role**
  - [ ] 역할 이름: `EnterpriseWebAppLambdaRole`
  - [ ] 신뢰 관계: Lambda 서비스
  - [ ] 정책: RDS 연결, ElastiCache 접근, 로그 권한
  - [ ] 기본 Lambda 실행 역할 포함

### 🔍 Phase 2 검증

- [ ] **보안 그룹 검증**
  - [ ] 모든 보안 그룹 생성 완료
  - [ ] 인바운드/아웃바운드 규칙 정확성 확인
  - [ ] 최소 권한 원칙 적용 확인

- [ ] **IAM 역할 검증**
  - [ ] 역할 생성 완료
  - [ ] 정책 연결 확인
  - [ ] 신뢰 관계 설정 확인

---

## 💾 Phase 3: 데이터베이스 및 캐시 구축 (60분)

### ✅ Step 3.1: RDS 서브넷 그룹 생성

- [ ] **DB Subnet Group 생성**
  - [ ] 이름: `enterprise-webapp-db-subnet-group`
  - [ ] VPC: enterprise-webapp-vpc
  - [ ] 서브넷: Database Subnet A, B 포함
  - [ ] 설명 추가

### ✅ Step 3.2: RDS MySQL 인스턴스 생성

- [ ] **Primary Database 설정**
  - [ ] 엔진: MySQL 8.0
  - [ ] 템플릿: 프로덕션 (또는 개발/테스트)
  - [ ] DB 인스턴스 식별자: `enterprise-webapp-db`
  - [ ] 마스터 사용자 이름: `admin`
  - [ ] 강력한 마스터 암호 설정 (기록 보관)

- [ ] **인스턴스 구성**
  - [ ] DB 인스턴스 클래스: db.t3.micro
  - [ ] 스토리지: 20GB gp2
  - [ ] Multi-AZ 배포 활성화
  - [ ] VPC: enterprise-webapp-vpc
  - [ ] 서브넷 그룹: enterprise-webapp-db-subnet-group
  - [ ] 보안 그룹: enterprise-webapp-db-sg

- [ ] **백업 및 모니터링**
  - [ ] 백업 보존 기간: 7일
  - [ ] 백업 윈도우 설정
  - [ ] 유지 관리 윈도우 설정
  - [ ] 성능 인사이트 활성화
  - [ ] 향상된 모니터링 활성화

### ✅ Step 3.3: ElastiCache Redis 클러스터 생성

- [ ] **Redis Cluster 설정**
  - [ ] 클러스터 이름: `enterprise-webapp-cache`
  - [ ] 엔진: Redis 7.0
  - [ ] 노드 유형: cache.t3.micro
  - [ ] 복제본 수: 1 (Multi-AZ)

- [ ] **네트워크 구성**
  - [ ] 서브넷 그룹 생성 (Private Subnet A, B)
  - [ ] 보안 그룹: enterprise-webapp-cache-sg
  - [ ] 암호화 활성화 (전송 중, 저장 시)

- [ ] **백업 및 유지 관리**
  - [ ] 자동 백업 활성화
  - [ ] 백업 보존 기간: 5일
  - [ ] 유지 관리 윈도우 설정

### 🔍 Phase 3 검증

- [ ] **RDS 연결 테스트**
  - [ ] RDS 인스턴스 상태: Available
  - [ ] 엔드포인트 정보 기록
  - [ ] 보안 그룹 규칙으로 접근 제한 확인

- [ ] **ElastiCache 연결 테스트**
  - [ ] Redis 클러스터 상태: Available
  - [ ] 엔드포인트 정보 기록
  - [ ] 복제 그룹 정상 작동 확인

---

## 🖥️ Phase 4: 컴퓨팅 리소스 구축 (90분)

### ✅ Step 4.1: Launch Template 생성

- [ ] **Launch Template 기본 설정**
  - [ ] 이름: `enterprise-webapp-lt`
  - [ ] AMI: Amazon Linux 2023 (최신)
  - [ ] 인스턴스 유형: t3.micro
  - [ ] 키 페어 선택 (기존 또는 새로 생성)

- [ ] **네트워크 및 보안**
  - [ ] 보안 그룹: enterprise-webapp-web-sg
  - [ ] IAM 인스턴스 프로파일: EnterpriseWebAppEC2Role

- [ ] **User Data 스크립트**
  - [ ] 웹 서버 설치 (Apache, PHP, MySQL 클라이언트)
  - [ ] CloudWatch Agent 설치
  - [ ] 샘플 애플리케이션 배포
  - [ ] RDS 엔드포인트 정보 업데이트

### ✅ Step 4.2: Auto Scaling Group 생성

- [ ] **ASG 기본 설정**
  - [ ] 이름: `enterprise-webapp-asg`
  - [ ] Launch Template: enterprise-webapp-lt
  - [ ] VPC: enterprise-webapp-vpc
  - [ ] 서브넷: Private Subnet A, B

- [ ] **용량 설정**
  - [ ] 최소 용량: 2
  - [ ] 원하는 용량: 2
  - [ ] 최대 용량: 6

- [ ] **상태 확인**
  - [ ] 상태 확인 유형: ELB
  - [ ] 상태 확인 유예 기간: 300초
  - [ ] 인스턴스 워밍업 시간: 300초

- [ ] **Scaling Policy 생성**
  - [ ] Scale Out: CPU > 70% for 2 minutes → Add 1 instance
  - [ ] Scale In: CPU < 30% for 5 minutes → Remove 1 instance

### ✅ Step 4.3: Application Load Balancer 생성

- [ ] **ALB 기본 설정**
  - [ ] 이름: `enterprise-webapp-alb`
  - [ ] 스키마: Internet-facing
  - [ ] IP 주소 유형: IPv4
  - [ ] VPC: enterprise-webapp-vpc
  - [ ] 서브넷: Public Subnet A, B
  - [ ] 보안 그룹: enterprise-webapp-alb-sg

- [ ] **Target Group 생성**
  - [ ] 이름: `enterprise-webapp-tg`
  - [ ] 프로토콜: HTTP, 포트: 80
  - [ ] VPC: enterprise-webapp-vpc
  - [ ] 상태 확인 경로: `/index.php`
  - [ ] 상태 확인 설정 최적화

- [ ] **Listener 구성**
  - [ ] 프로토콜: HTTP, 포트: 80
  - [ ] 기본 작업: Forward to enterprise-webapp-tg
  - [ ] Auto Scaling Group과 Target Group 연결

### 🔍 Phase 4 검증

- [ ] **인스턴스 상태 확인**
  - [ ] ASG에서 2개 인스턴스 실행 중
  - [ ] 모든 인스턴스 상태: InService
  - [ ] Target Group에서 Healthy 상태 확인

- [ ] **로드 밸런서 테스트**
  - [ ] ALB DNS 이름으로 웹 페이지 접근 가능
  - [ ] 여러 번 새로고침하여 로드 밸런싱 확인
  - [ ] 데이터베이스 연결 상태 확인

---

## ☁️ Phase 5: 서버리스 및 스토리지 구성 (60분)

### ✅ Step 5.1: S3 버킷 생성

- [ ] **Static Assets Bucket**
  - [ ] 버킷 이름: `enterprise-webapp-static-[random-suffix]`
  - [ ] 리전: us-east-1
  - [ ] 퍼블릭 액세스 설정 (CloudFront용)
  - [ ] 버전 관리 활성화
  - [ ] 서버 측 암호화: AES-256

- [ ] **Backup Bucket**
  - [ ] 버킷 이름: `enterprise-webapp-backups-[random-suffix]`
  - [ ] 모든 퍼블릭 액세스 차단
  - [ ] 버전 관리 활성화
  - [ ] 서버 측 암호화: KMS
  - [ ] 수명 주기 정책: 30일 후 IA, 90일 후 Glacier

### ✅ Step 5.2: Lambda 함수 생성

- [ ] **Database Health Check Function**
  - [ ] 함수 이름: `enterprise-webapp-db-health`
  - [ ] 런타임: Python 3.11
  - [ ] 실행 역할: EnterpriseWebAppLambdaRole
  - [ ] VPC 구성: Private Subnet A, B
  - [ ] 보안 그룹: Lambda용 보안 그룹 생성

- [ ] **함수 코드 배포**
  - [ ] pymysql 라이브러리 포함
  - [ ] RDS 연결 코드 구현
  - [ ] CloudWatch 메트릭 전송 코드
  - [ ] 에러 처리 로직 포함

- [ ] **EventBridge Rule 생성**
  - [ ] 규칙 이름: `enterprise-webapp-health-check`
  - [ ] 스케줄: rate(5 minutes)
  - [ ] 대상: Lambda function

### 🔍 Phase 5 검증

- [ ] **S3 버킷 테스트**
  - [ ] 버킷 생성 완료
  - [ ] 정책 및 권한 설정 확인
  - [ ] 암호화 설정 확인

- [ ] **Lambda 함수 테스트**
  - [ ] 함수 실행 성공
  - [ ] CloudWatch 로그 확인
  - [ ] 메트릭 전송 확인
  - [ ] EventBridge 스케줄 작동 확인

---

## 🌐 Phase 6: CDN 및 DNS 구성 (45분)

### ✅ Step 6.1: CloudFront Distribution 생성

- [ ] **Distribution 기본 설정**
  - [ ] Origin Domain: ALB DNS 이름
  - [ ] Origin Protocol Policy: HTTP Only
  - [ ] Viewer Protocol Policy: Redirect HTTP to HTTPS
  - [ ] Allowed HTTP Methods: GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE

- [ ] **캐시 동작 설정**
  - [ ] Cache Policy: Managed-CachingOptimized
  - [ ] Origin Request Policy: Managed-CORS-S3Origin
  - [ ] TTL 설정 최적화

- [ ] **Additional Origins (S3)**
  - [ ] S3 Static Assets Origin 추가
  - [ ] Origin Access Control 생성 및 연결
  - [ ] Behavior Pattern: `/static/*`

### ✅ Step 6.2: Route 53 구성 (선택사항)

- [ ] **Hosted Zone 생성**
  - [ ] 도메인 이름 입력
  - [ ] Public Hosted Zone 선택
  - [ ] NS 레코드 확인

- [ ] **A Record 생성**
  - [ ] 레코드 이름: www
  - [ ] 레코드 유형: A
  - [ ] 별칭: Yes
  - [ ] 별칭 대상: CloudFront Distribution

### 🔍 Phase 6 검증

- [ ] **CloudFront 테스트**
  - [ ] Distribution 상태: Deployed
  - [ ] CloudFront URL로 웹사이트 접근 가능
  - [ ] HTTPS 리디렉션 작동 확인
  - [ ] 캐시 동작 확인

- [ ] **Route 53 테스트 (선택사항)**
  - [ ] 도메인으로 웹사이트 접근 가능
  - [ ] DNS 전파 완료 확인

---

## 📊 Phase 7: 모니터링 및 로깅 설정 (60분)

### ✅ Step 7.1: CloudWatch 대시보드 생성

- [ ] **Enterprise Dashboard 생성**
  - [ ] 대시보드 이름: `Enterprise-WebApp-Dashboard`
  - [ ] 위젯 추가: ALB Request Count (5분)
  - [ ] 위젯 추가: ALB Response Time (5분)
  - [ ] 위젯 추가: EC2 CPU Utilization (5분)
  - [ ] 위젯 추가: RDS CPU Utilization (5분)
  - [ ] 위젯 추가: RDS Database Connections (5분)
  - [ ] 위젯 추가: ElastiCache CPU Utilization (5분)
  - [ ] 위젯 추가: Lambda Invocations (5분)
  - [ ] 위젯 추가: Lambda Errors (5분)
  - [ ] 위젯 추가: Custom Database Health Metric (5분)

### ✅ Step 7.2: CloudWatch Alarms 생성

- [ ] **Critical Alarms 설정**
  - [ ] ALB High Response Time (> 2초, 2/10분)
  - [ ] RDS High CPU (> 80%, 2/10분)
  - [ ] Database Health Check Failed (= 0, 1/5분)
  - [ ] EC2 High CPU (> 80%, 2/10분)
  - [ ] Lambda Error Rate (> 5%, 2/10분)

- [ ] **SNS Topic 생성**
  - [ ] 토픽 이름: `enterprise-webapp-alerts`
  - [ ] 이메일 구독 추가
  - [ ] 구독 확인 완료

### ✅ Step 7.3: AWS Config 설정

- [ ] **Configuration Recorder**
  - [ ] 이름: `enterprise-webapp-config`
  - [ ] 서비스 역할 생성
  - [ ] S3 버킷 지정
  - [ ] 모든 지원 리소스 기록

- [ ] **Config Rules 추가**
  - [ ] ec2-security-group-attached-to-eni
  - [ ] rds-multi-az-support
  - [ ] s3-bucket-ssl-requests-only
  - [ ] cloudtrail-enabled

### ✅ Step 7.4: CloudTrail 설정

- [ ] **Trail 생성**
  - [ ] 이름: `enterprise-webapp-trail`
  - [ ] S3 버킷 생성 또는 선택
  - [ ] 로그 파일 암호화 활성화
  - [ ] CloudWatch Logs 통합
  - [ ] Management events 기록
  - [ ] Data events 기록 (S3, Lambda)

### 🔍 Phase 7 검증

- [ ] **대시보드 확인**
  - [ ] 모든 위젯에서 데이터 표시
  - [ ] 메트릭 정확성 확인
  - [ ] 시간 범위 설정 확인

- [ ] **알람 테스트**
  - [ ] 알람 상태 확인
  - [ ] SNS 알림 수신 확인
  - [ ] 임계값 설정 검증

---

## 🔐 Phase 8: 보안 강화 (45분)

### ✅ Step 8.1: AWS WAF 설정

- [ ] **Web ACL 생성**
  - [ ] 이름: `enterprise-webapp-waf`
  - [ ] 리소스 유형: CloudFront distributions
  - [ ] CloudFront Distribution 연결

- [ ] **관리형 규칙 추가**
  - [ ] AWS Managed Rules - Core Rule Set
  - [ ] AWS Managed Rules - Known Bad Inputs
  - [ ] AWS Managed Rules - SQL Injection
  - [ ] Rate Limiting: 2000 requests per 5 minutes

### ✅ Step 8.2: Secrets Manager 설정

- [ ] **Database Credentials**
  - [ ] 시크릿 이름: `enterprise-webapp/db/credentials`
  - [ ] 시크릿 유형: RDS database credentials
  - [ ] 데이터베이스 선택: enterprise-webapp-db
  - [ ] 자동 로테이션: 30일 설정

### ✅ Step 8.3: Systems Manager Parameter Store

- [ ] **Application Parameters 생성**
  - [ ] `/enterprise-webapp/db/endpoint`: RDS 엔드포인트
  - [ ] `/enterprise-webapp/cache/endpoint`: ElastiCache 엔드포인트
  - [ ] `/enterprise-webapp/s3/static-bucket`: S3 버킷 이름
  - [ ] 모든 파라미터 SecureString 타입으로 설정

### 🔍 Phase 8 검증

- [ ] **WAF 규칙 테스트**
  - [ ] 정상 요청 통과 확인
  - [ ] 악성 요청 차단 확인
  - [ ] Rate limiting 작동 확인

- [ ] **Secrets Manager 테스트**
  - [ ] 시크릿 검색 가능
  - [ ] 자동 로테이션 설정 확인
  - [ ] 애플리케이션에서 시크릿 사용 가능

---

## 🧪 Phase 9: 테스트 및 검증 (60분)

### ✅ Step 9.1: 기능 테스트

- [ ] **웹 애플리케이션 접근 테스트**
  - [ ] CloudFront URL로 접근 성공
  - [ ] ALB URL로 직접 접근 성공
  - [ ] HTTPS 리디렉션 작동
  - [ ] 응답 시간 2초 이하 확인

- [ ] **데이터베이스 연결 테스트**
  - [ ] 웹 페이지에서 DB 연결 상태 확인
  - [ ] 데이터 읽기/쓰기 테스트
  - [ ] 연결 풀링 작동 확인

- [ ] **Auto Scaling 테스트**
  - [ ] 부하 테스트 도구로 트래픽 생성
  - [ ] CPU 사용률 증가 확인
  - [ ] 새 인스턴스 자동 생성 확인
  - [ ] 부하 감소 후 인스턴스 자동 제거 확인

### ✅ Step 9.2: 보안 테스트

- [ ] **보안 그룹 검증**
  - [ ] 불필요한 포트 차단 확인
  - [ ] 소스 IP 제한 확인
  - [ ] 최소 권한 원칙 적용 확인

- [ ] **WAF 규칙 테스트**
  - [ ] SQL Injection 시도 차단 확인
  - [ ] XSS 공격 차단 확인
  - [ ] Rate Limiting 작동 확인

- [ ] **암호화 확인**
  - [ ] 전송 중 암호화 (HTTPS) 확인
  - [ ] 저장 시 암호화 (RDS, S3) 확인
  - [ ] 시크릿 관리 확인

### ✅ Step 9.3: 성능 테스트

- [ ] **응답 시간 측정**
  - [ ] 첫 번째 요청 (캐시 미스)
  - [ ] 두 번째 요청 (캐시 히트)
  - [ ] 평균 응답 시간 2초 이하 확인

- [ ] **캐시 성능 확인**
  - [ ] CloudFront 캐시 히트율 확인
  - [ ] ElastiCache 히트율 확인
  - [ ] 데이터베이스 쿼리 최적화 확인

- [ ] **확장성 테스트**
  - [ ] 동시 사용자 100명 테스트
  - [ ] 시스템 안정성 확인
  - [ ] 리소스 사용률 모니터링

### 🔍 Phase 9 검증

- [ ] **전체 시스템 상태 확인**
  - [ ] 모든 서비스 정상 작동
  - [ ] 모니터링 대시보드 정상 표시
  - [ ] 알람 설정 정상 작동
  - [ ] 로그 수집 정상 작동

---

## 📈 Phase 10: 최적화 및 비용 관리 (30분)

### ✅ Step 10.1: 비용 최적화

- [ ] **Reserved Instances 검토**
  - [ ] RDS 인스턴스 RI 구매 고려사항 검토
  - [ ] EC2 인스턴스 Savings Plans 검토
  - [ ] 비용 계산기로 절약 효과 계산

- [ ] **S3 Intelligent Tiering 설정**
  - [ ] Static Assets 버킷에 적용
  - [ ] 모든 객체에 대해 활성화
  - [ ] 모니터링 및 자동화 요금 확인

- [ ] **CloudWatch Logs 보존 기간 설정**
  - [ ] Lambda 로그 그룹: 30일
  - [ ] EC2 로그 그룹: 7일
  - [ ] ALB 액세스 로그: 30일

### ✅ Step 10.2: 성능 최적화

- [ ] **ElastiCache 설정 최적화**
  - [ ] 파라미터 그룹 생성
  - [ ] maxmemory-policy: allkeys-lru
  - [ ] timeout: 300초
  - [ ] 클러스터에 적용

- [ ] **RDS 파라미터 그룹 최적화**
  - [ ] 사용자 정의 파라미터 그룹 생성
  - [ ] innodb_buffer_pool_size 최적화
  - [ ] query_cache_size 설정
  - [ ] DB 인스턴스에 적용

- [ ] **CloudFront 최적화**
  - [ ] 캐시 정책 최적화
  - [ ] 압축 활성화
  - [ ] HTTP/2 지원 확인

### 🔍 Phase 10 검증

- [ ] **비용 모니터링 설정**
  - [ ] Cost Explorer에서 현재 비용 확인
  - [ ] 예산 알림 설정
  - [ ] 비용 이상 탐지 활성화

- [ ] **성능 개선 확인**
  - [ ] 응답 시간 개선 측정
  - [ ] 캐시 히트율 향상 확인
  - [ ] 데이터베이스 성능 개선 확인

---

## 🧹 정리 및 리소스 삭제

### ⚠️ 중요: 비용 발생 방지

실습 완료 후 다음 순서로 리소스를 삭제하세요:

- [ ] **1단계: CloudFront Distribution**
  - [ ] Distribution 비활성화
  - [ ] 완전 비활성화 대기 (15-20분)
  - [ ] Distribution 삭제

- [ ] **2단계: Auto Scaling Group**
  - [ ] 원하는 용량을 0으로 설정
  - [ ] 모든 인스턴스 종료 확인
  - [ ] ASG 삭제

- [ ] **3단계: Load Balancer**
  - [ ] Target Group에서 모든 대상 제거
  - [ ] ALB 삭제
  - [ ] Target Group 삭제

- [ ] **4단계: 데이터베이스**
  - [ ] RDS 인스턴스 삭제 (최종 스냅샷 생성)
  - [ ] ElastiCache 클러스터 삭제
  - [ ] DB 서브넷 그룹 삭제

- [ ] **5단계: Lambda 및 서버리스**
  - [ ] EventBridge 규칙 삭제
  - [ ] Lambda 함수 삭제
  - [ ] CloudWatch 로그 그룹 삭제

- [ ] **6단계: 스토리지**
  - [ ] S3 버킷 비우기
  - [ ] S3 버킷 삭제
  - [ ] EBS 스냅샷 삭제

- [ ] **7단계: 네트워킹**
  - [ ] NAT Gateway 삭제
  - [ ] Elastic IP 해제
  - [ ] 인터넷 게이트웨이 분리 및 삭제
  - [ ] 라우팅 테이블 삭제
  - [ ] 서브넷 삭제
  - [ ] VPC 삭제

- [ ] **8단계: 보안 및 모니터링**
  - [ ] WAF Web ACL 삭제
  - [ ] CloudTrail 삭제
  - [ ] Config 규칙 및 레코더 삭제
  - [ ] CloudWatch 알람 삭제
  - [ ] SNS 토픽 삭제
  - [ ] 보안 그룹 삭제
  - [ ] IAM 역할 및 정책 삭제

### 🔍 최종 검증

- [ ] **비용 확인**
  - [ ] Cost Explorer에서 삭제 후 비용 확인
  - [ ] 예상치 못한 요금 발생 여부 확인
  - [ ] 모든 리소스 삭제 완료 확인

---

## 🎓 학습 성과 체크리스트

### ✅ 기술적 성과

- [ ] **아키텍처 설계**
  - [ ] 3-tier 아키텍처 완전 구현
  - [ ] Multi-AZ 고가용성 설계
  - [ ] Auto Scaling 및 Load Balancing
  - [ ] 마이크로서비스 패턴 이해

- [ ] **보안 구현**
  - [ ] 네트워크 보안 (VPC, 보안 그룹)
  - [ ] 애플리케이션 보안 (WAF, HTTPS)
  - [ ] 데이터 보안 (암호화, Secrets Manager)
  - [ ] 접근 제어 (IAM, 최소 권한)

- [ ] **운영 및 모니터링**
  - [ ] 종합 모니터링 대시보드 구축
  - [ ] 알람 및 알림 시스템 구현
  - [ ] 로깅 및 추적 시스템 구축
  - [ ] 백업 및 재해 복구 계획

- [ ] **성능 최적화**
  - [ ] CDN을 통한 콘텐츠 전송 최적화
  - [ ] 데이터베이스 성능 튜닝
  - [ ] 캐싱 전략 구현
  - [ ] 비용 최적화 전략 적용

### ✅ SAA-C03 시험 준비

- [ ] **도메인 1: 복원력 있는 아키텍처 설계**
  - [ ] Multi-AZ 배포 경험
  - [ ] 장애 조치 메커니즘 구현
  - [ ] 백업 및 복구 전략 수립

- [ ] **도메인 2: 고성능 아키텍처 설계**
  - [ ] 확장 가능한 컴퓨팅 솔루션 구현
  - [ ] 고성능 스토리지 솔루션 선택
  - [ ] 네트워크 솔루션 최적화

- [ ] **도메인 3: 보안 애플리케이션 및 아키텍처 설계**
  - [ ] 보안 액세스 제어 구현
  - [ ] 보안 애플리케이션 계층 설계
  - [ ] 적절한 데이터 보안 옵션 선택

- [ ] **도메인 4: 비용 최적화 아키텍처 설계**
  - [ ] 비용 효율적인 스토리지 솔루션 구현
  - [ ] 비용 효율적인 컴퓨팅 솔루션 구현
  - [ ] 비용 최적화 데이터베이스 솔루션 설계

## 📝 실습 완료 인증

### 최종 체크리스트

- [ ] **모든 Phase 완료** (1-10)
- [ ] **기능 테스트 통과**
- [ ] **보안 테스트 통과**
- [ ] **성능 테스트 통과**
- [ ] **리소스 정리 완료**
- [ ] **학습 성과 달성**

### 🏆 축하합니다!

이 종합 실습을 완료하셨다면, AWS Solutions Architect Associate 시험에 필요한 실무 경험을 충분히 쌓으셨습니다. 

**다음 단계:**
1. Day 27: 모의고사 및 최종 복습
2. Day 28: 시험 준비 및 등록
3. 실제 SAA-C03 시험 응시

**실습 완료 시간:** ___________  
**총 소요 시간:** ___________  
**어려웠던 부분:** ___________  
**추가 학습이 필요한 영역:** ___________

이 체크리스트를 통해 체계적이고 완전한 엔터프라이즈급 AWS 아키텍처 구축 경험을 쌓으시기 바랍니다!