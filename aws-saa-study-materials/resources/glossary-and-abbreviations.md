# AWS 용어집 및 약어 정리

## A

### ACL (Access Control List)
네트워크 액세스 제어 목록. VPC에서 서브넷 수준의 보안을 제공하는 선택적 보안 계층.

### AZ (Availability Zone)
가용 영역. AWS 리전 내의 하나 이상의 개별 데이터 센터로, 독립적인 전력, 냉각, 물리적 보안을 갖춤.

### ALB (Application Load Balancer)
애플리케이션 로드 밸런서. HTTP/HTTPS 트래픽을 위한 Layer 7 로드 밸런서.

### AMI (Amazon Machine Image)
아마존 머신 이미지. EC2 인스턴스를 시작하는 데 필요한 정보를 제공하는 템플릿.

### API (Application Programming Interface)
애플리케이션 프로그래밍 인터페이스. 소프트웨어 구성 요소 간의 통신을 위한 규약.

### ARN (Amazon Resource Name)
아마존 리소스 이름. AWS 리소스를 고유하게 식별하는 이름.

### Auto Scaling
수요에 따라 EC2 인스턴스를 자동으로 추가하거나 제거하는 서비스.

## B

### Bucket
S3에서 객체를 저장하는 컨테이너. 전역적으로 고유한 이름을 가져야 함.

### Bursting
EBS gp2 볼륨이나 EFS에서 기본 성능을 초과하여 일시적으로 높은 성능을 제공하는 기능.

## C

### CDN (Content Delivery Network)
콘텐츠 전송 네트워크. 전 세계에 분산된 서버를 통해 콘텐츠를 빠르게 전송하는 시스템.

### CIDR (Classless Inter-Domain Routing)
클래스리스 도메인 간 라우팅. IP 주소 할당 및 라우팅을 위한 방법.

### CLI (Command Line Interface)
명령줄 인터페이스. 텍스트 명령을 통해 AWS 서비스를 관리하는 도구.

### CloudFormation
AWS 리소스를 코드로 정의하고 관리하는 Infrastructure as Code 서비스.

### CloudFront
AWS의 글로벌 CDN 서비스.

### CloudTrail
AWS 계정의 API 호출을 기록하고 모니터링하는 서비스.

### CloudWatch
AWS 리소스와 애플리케이션을 모니터링하는 서비스.

### CORS (Cross-Origin Resource Sharing)
교차 출처 리소스 공유. 웹 페이지가 다른 도메인의 리소스에 액세스할 수 있게 하는 메커니즘.

## D

### DLQ (Dead Letter Queue)
처리에 실패한 메시지를 저장하는 큐.

### DNS (Domain Name System)
도메인 이름 시스템. 도메인 이름을 IP 주소로 변환하는 시스템.

### DynamoDB
AWS의 완전 관리형 NoSQL 데이터베이스 서비스.

## E

### EBS (Elastic Block Store)
EC2 인스턴스용 블록 수준 스토리지 볼륨.

### EC2 (Elastic Compute Cloud)
AWS의 가상 서버 서비스.

### ECS (Elastic Container Service)
Docker 컨테이너를 실행하고 관리하는 서비스.

### EFS (Elastic File System)
완전 관리형 NFS 파일 시스템.

### EKS (Elastic Kubernetes Service)
관리형 Kubernetes 서비스.

### ELB (Elastic Load Balancer)
들어오는 애플리케이션 트래픽을 여러 대상에 자동으로 분산하는 서비스.

### EMR (Elastic MapReduce)
빅데이터 처리를 위한 관리형 클러스터 플랫폼.

### Encryption at Rest
저장된 데이터의 암호화.

### Encryption in Transit
전송 중인 데이터의 암호화.

### Endpoint
네트워크를 통해 서비스에 연결하는 진입점.

### EventBridge
서버리스 이벤트 버스 서비스.

## F

### Fargate
서버리스 컨테이너 실행 엔진.

### FIFO (First In, First Out)
선입선출. SQS에서 메시지 순서를 보장하는 큐 타입.

## G

### Gateway
네트워크 간의 연결점 역할을 하는 장치나 소프트웨어.

### Glacier
장기 아카이브용 저비용 스토리지 클래스.

### Global Secondary Index (GSI)
DynamoDB에서 다른 파티션 키와 정렬 키를 사용하는 인덱스.

## H

### Health Check
리소스의 상태를 확인하는 프로세스.

### HDD (Hard Disk Drive)
하드 디스크 드라이브. 기계적 부품을 사용하는 스토리지 장치.

### HTTPS (HTTP Secure)
SSL/TLS를 사용하여 암호화된 HTTP 통신.

## I

### IAM (Identity and Access Management)
AWS 리소스에 대한 액세스를 안전하게 제어하는 서비스.

### IOPS (Input/Output Operations Per Second)
초당 입출력 작업 수. 스토리지 성능 측정 단위.

### Instance
EC2에서 실행되는 가상 서버.

### Internet Gateway
VPC와 인터넷 간의 연결을 제공하는 게이트웨이.

## J

### JSON (JavaScript Object Notation)
데이터 교환을 위한 경량 텍스트 형식.

## K

### KMS (Key Management Service)
암호화 키를 생성하고 관리하는 서비스.

### Kubernetes
컨테이너 오케스트레이션 플랫폼.

## L

### Lambda
서버리스 컴퓨팅 서비스.

### Launch Configuration
Auto Scaling 그룹에서 인스턴스를 시작하는 데 사용되는 템플릿.

### Launch Template
EC2 인스턴스 시작을 위한 향상된 템플릿.

### Load Balancer
들어오는 네트워크 트래픽을 여러 서버에 분산하는 장치.

### Local Secondary Index (LSI)
DynamoDB에서 같은 파티션 키를 사용하지만 다른 정렬 키를 사용하는 인덱스.

## M

### MFA (Multi-Factor Authentication)
다중 인증. 두 개 이상의 인증 요소를 사용하는 보안 방법.

### Multi-AZ
여러 가용 영역에 걸쳐 배포되는 구성.

## N

### NACL (Network Access Control List)
네트워크 액세스 제어 목록. 서브넷 수준의 보안 규칙.

### NAT (Network Address Translation)
네트워크 주소 변환. 프라이빗 IP를 퍼블릭 IP로 변환.

### NLB (Network Load Balancer)
네트워크 로드 밸런서. TCP/UDP 트래픽을 위한 Layer 4 로드 밸런서.

### NoSQL
관계형이 아닌 데이터베이스 시스템.

## O

### Object
S3에서 저장되는 기본 엔티티.

### On-Demand
사용한 만큼 지불하는 가격 모델.

### Origin
CloudFront가 콘텐츠를 가져오는 원본 서버.

## P

### Parameter Store
Systems Manager의 구성 데이터 관리 기능.

### Partition Key
DynamoDB에서 데이터를 분산하는 데 사용되는 기본 키.

### Policy
IAM에서 권한을 정의하는 JSON 문서.

### Private Subnet
인터넷에 직접 연결되지 않은 서브넷.

### Public Subnet
인터넷 게이트웨이를 통해 인터넷에 연결된 서브넷.

## Q

### Queue
메시지를 저장하고 전달하는 버퍼.

## R

### RDS (Relational Database Service)
관리형 관계형 데이터베이스 서비스.

### Read Replica
읽기 전용 데이터베이스 복제본.

### Region
AWS 인프라가 위치한 지리적 영역.

### Reserved Instance
1년 또는 3년 약정으로 할인된 가격의 EC2 인스턴스.

### Role
임시 보안 자격 증명을 제공하는 IAM 엔티티.

### Route 53
AWS의 확장 가능한 DNS 웹 서비스.

### Route Table
네트워크 트래픽이 전달되는 경로를 결정하는 규칙 집합.

### RTO (Recovery Time Objective)
복구 목표 시간. 재해 후 서비스 복구까지 허용되는 최대 시간.

### RPO (Recovery Point Objective)
복구 목표 지점. 재해 시 허용 가능한 최대 데이터 손실량.

## S

### S3 (Simple Storage Service)
객체 스토리지 서비스.

### SDK (Software Development Kit)
소프트웨어 개발 키트.

### Security Group
EC2 인스턴스를 위한 가상 방화벽.

### Serverless
서버 관리 없이 코드를 실행하는 컴퓨팅 모델.

### SNS (Simple Notification Service)
게시-구독 메시징 서비스.

### SQS (Simple Queue Service)
완전 관리형 메시지 큐 서비스.

### SSD (Solid State Drive)
플래시 메모리를 사용하는 스토리지 장치.

### SSL/TLS (Secure Sockets Layer/Transport Layer Security)
네트워크 통신을 암호화하는 프로토콜.

### Subnet
VPC 내의 IP 주소 범위.

## T

### Target Group
로드 밸런서가 요청을 라우팅하는 대상들의 그룹.

### Throughput
단위 시간당 처리할 수 있는 데이터량.

### TTL (Time To Live)
데이터나 DNS 레코드의 유효 시간.

## U

### User
IAM에서 AWS 서비스와 리소스에 액세스하는 엔티티.

## V

### VPC (Virtual Private Cloud)
AWS 클라우드에서 논리적으로 격리된 가상 네트워크.

### VPN (Virtual Private Network)
인터넷을 통해 안전한 연결을 제공하는 기술.

## W

### WAF (Web Application Firewall)
웹 애플리케이션을 보호하는 방화벽.

### Well-Architected Framework
AWS의 아키텍처 모범 사례 프레임워크.

## X

### X-Ray
분산 애플리케이션을 분석하고 디버그하는 서비스.

## Y

### YAML (YAML Ain't Markup Language)
사람이 읽기 쉬운 데이터 직렬화 표준.

---

## 자주 사용되는 약어 모음

| 약어 | 전체 이름 | 한국어 |
|------|-----------|--------|
| ACL | Access Control List | 액세스 제어 목록 |
| ALB | Application Load Balancer | 애플리케이션 로드 밸런서 |
| AMI | Amazon Machine Image | 아마존 머신 이미지 |
| API | Application Programming Interface | 애플리케이션 프로그래밍 인터페이스 |
| ARN | Amazon Resource Name | 아마존 리소스 이름 |
| AZ | Availability Zone | 가용 영역 |
| CDN | Content Delivery Network | 콘텐츠 전송 네트워크 |
| CIDR | Classless Inter-Domain Routing | 클래스리스 도메인 간 라우팅 |
| CLI | Command Line Interface | 명령줄 인터페이스 |
| CORS | Cross-Origin Resource Sharing | 교차 출처 리소스 공유 |
| DLQ | Dead Letter Queue | 배달 못한 편지 큐 |
| DNS | Domain Name System | 도메인 이름 시스템 |
| EBS | Elastic Block Store | 탄력적 블록 스토어 |
| EC2 | Elastic Compute Cloud | 탄력적 컴퓨팅 클라우드 |
| ECS | Elastic Container Service | 탄력적 컨테이너 서비스 |
| EFS | Elastic File System | 탄력적 파일 시스템 |
| EKS | Elastic Kubernetes Service | 탄력적 쿠버네티스 서비스 |
| ELB | Elastic Load Balancer | 탄력적 로드 밸런서 |
| EMR | Elastic MapReduce | 탄력적 맵리듀스 |
| FIFO | First In, First Out | 선입선출 |
| GSI | Global Secondary Index | 글로벌 보조 인덱스 |
| HDD | Hard Disk Drive | 하드 디스크 드라이브 |
| HTTPS | HTTP Secure | 보안 HTTP |
| IAM | Identity and Access Management | 자격 증명 및 액세스 관리 |
| IOPS | Input/Output Operations Per Second | 초당 입출력 작업 수 |
| JSON | JavaScript Object Notation | 자바스크립트 객체 표기법 |
| KMS | Key Management Service | 키 관리 서비스 |
| LSI | Local Secondary Index | 로컬 보조 인덱스 |
| MFA | Multi-Factor Authentication | 다중 인증 |
| NACL | Network Access Control List | 네트워크 액세스 제어 목록 |
| NAT | Network Address Translation | 네트워크 주소 변환 |
| NLB | Network Load Balancer | 네트워크 로드 밸런서 |
| RDS | Relational Database Service | 관계형 데이터베이스 서비스 |
| RTO | Recovery Time Objective | 복구 목표 시간 |
| RPO | Recovery Point Objective | 복구 목표 지점 |
| S3 | Simple Storage Service | 단순 스토리지 서비스 |
| SDK | Software Development Kit | 소프트웨어 개발 키트 |
| SNS | Simple Notification Service | 단순 알림 서비스 |
| SQS | Simple Queue Service | 단순 큐 서비스 |
| SSD | Solid State Drive | 솔리드 스테이트 드라이브 |
| SSL/TLS | Secure Sockets Layer/Transport Layer Security | 보안 소켓 계층/전송 계층 보안 |
| TTL | Time To Live | 생존 시간 |
| VPC | Virtual Private Cloud | 가상 사설 클라우드 |
| VPN | Virtual Private Network | 가상 사설망 |
| WAF | Web Application Firewall | 웹 애플리케이션 방화벽 |
| YAML | YAML Ain't Markup Language | YAML은 마크업 언어가 아니다 |

---

## 시험에서 자주 나오는 개념

### 보안 관련
- **Principle of Least Privilege**: 최소 권한 원칙
- **Defense in Depth**: 심층 방어
- **Shared Responsibility Model**: 공동 책임 모델

### 아키텍처 관련
- **Loose Coupling**: 느슨한 결합
- **Stateless**: 무상태
- **Idempotent**: 멱등성
- **Eventual Consistency**: 최종 일관성

### 성능 관련
- **Caching**: 캐싱
- **Throttling**: 스로틀링
- **Bursting**: 버스팅
- **Provisioned**: 프로비저닝된

### 비용 관련
- **Pay-as-you-go**: 사용한 만큼 지불
- **Reserved Capacity**: 예약 용량
- **Spot Pricing**: 스팟 가격
- **Right-sizing**: 적정 크기 조정