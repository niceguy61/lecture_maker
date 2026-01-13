# AWS SAA-C03 모의고사 (65문제)

## 📋 시험 안내

- **문제 수**: 65문제
- **시험 시간**: 130분 (2시간 10분)
- **합격 점수**: 720점 (1000점 만점)
- **문제 유형**: 객관식 (단일 선택, 다중 선택)

## ⏰ 시간 관리 팁

- 문제당 평균 2분 배정
- 어려운 문제는 표시 후 나중에 재검토
- 마지막 10분은 답안 검토 시간으로 활용

---

## 문제 1-10: AWS 기초 및 글로벌 인프라

### 1. AWS 글로벌 인프라에 대한 설명으로 올바른 것은?
A) 가용 영역(AZ)은 하나의 데이터 센터로 구성됩니다
B) 리전은 최소 2개의 가용 영역으로 구성됩니다
C) 엣지 로케이션은 모든 AWS 서비스를 제공합니다
D) 로컬 영역은 가용 영역과 동일한 기능을 제공합니다

### 2. 다음 중 AWS 공동 책임 모델에서 고객의 책임에 해당하는 것은?
A) 물리적 보안
B) 하이퍼바이저 패치
C) 네트워크 인프라
D) 운영 체제 패치

### 3. AWS Well-Architected Framework의 5가지 기둥이 아닌 것은?
A) 보안 (Security)
B) 안정성 (Reliability)
C) 확장성 (Scalability)
D) 성능 효율성 (Performance Efficiency)

### 4. AWS 계정 간 리소스 공유를 위한 가장 적절한 서비스는?
A) AWS Organizations
B) AWS Resource Access Manager (RAM)
C) AWS IAM Cross-Account Roles
D) AWS Config

### 5. 다음 중 AWS 무료 계층에 포함되지 않는 서비스는?
A) Amazon EC2 t2.micro 인스턴스 (월 750시간)
B) Amazon S3 (5GB 스토리지)
C) Amazon RDS (20GB 스토리지)
D) Amazon Redshift (160GB 스토리지)

### 6. AWS 서비스의 API 호출을 모니터링하고 로깅하는 서비스는?
A) AWS CloudWatch
B) AWS CloudTrail
C) AWS Config
D) AWS X-Ray

### 7. AWS 리소스에 대한 태그 정책을 중앙에서 관리할 수 있는 서비스는?
A) AWS Resource Groups
B) AWS Tag Editor
C) AWS Organizations
D) AWS Systems Manager

### 8. 다음 중 AWS 서비스 한도 증가를 요청할 수 있는 방법은?
A) AWS Support Center
B) AWS Service Quotas
C) AWS CLI
D) 모든 답이 맞습니다

### 9. AWS 계정의 루트 사용자에 대한 설명으로 올바른 것은?
A) 일상적인 관리 작업에 사용해야 합니다
B) MFA를 설정할 수 없습니다
C) 계정 설정 변경 시에만 사용해야 합니다
D) IAM 사용자와 동일한 권한을 가집니다

### 10. AWS 서비스 상태를 실시간으로 확인할 수 있는 대시보드는?
A) AWS Personal Health Dashboard
B) AWS Service Health Dashboard
C) AWS CloudWatch Dashboard
D) AWS Systems Manager Dashboard

---

## 문제 11-20: IAM 및 보안

### 11. IAM 정책에서 명시적 거부(Explicit Deny)와 명시적 허용(Explicit Allow)이 충돌할 때의 결과는?
A) 명시적 허용이 우선됩니다
B) 명시적 거부가 우선됩니다
C) 먼저 작성된 정책이 우선됩니다
D) 오류가 발생합니다

### 12. 다음 중 IAM 역할(Role)의 특징으로 올바른 것은?
A) 영구적인 자격 증명을 가집니다
B) 임시 자격 증명을 제공합니다
C) 사용자만 역할을 맡을 수 있습니다
D) 패스워드가 필요합니다

### 13. AWS STS(Security Token Service)의 주요 기능은?
A) 영구적인 액세스 키 생성
B) 임시 보안 자격 증명 제공
C) IAM 사용자 생성
D) 패스워드 정책 관리

### 14. 다음 중 AWS 리소스에 대한 세밀한 액세스 제어를 제공하는 것은?
A) 보안 그룹
B) NACL (Network ACL)
C) IAM 정책
D) AWS WAF

### 15. Cross-Account Access를 구현하는 가장 안전한 방법은?
A) IAM 사용자 공유
B) 액세스 키 공유
C) IAM 역할 사용
D) 루트 계정 공유

### 16. AWS CloudHSM의 주요 용도는?
A) 네트워크 보안
B) 암호화 키 관리
C) 액세스 로깅
D) 취약점 스캔

### 17. AWS Secrets Manager와 AWS Systems Manager Parameter Store의 주요 차이점은?
A) 암호화 지원 여부
B) 자동 로테이션 기능
C) 비용
D) 지원하는 데이터 타입

### 18. 다음 중 AWS 계정 보안을 강화하는 방법이 아닌 것은?
A) MFA 활성화
B) 강력한 패스워드 정책 설정
C) 루트 계정 일상 사용
D) 정기적인 액세스 키 로테이션

### 19. AWS GuardDuty의 주요 기능은?
A) 웹 애플리케이션 방화벽
B) 위협 탐지 및 모니터링
C) 데이터 암호화
D) 네트워크 액세스 제어

### 20. IAM 정책의 조건(Condition) 요소를 사용하여 제어할 수 있는 것은?
A) 시간 기반 액세스
B) IP 주소 기반 액세스
C) MFA 요구사항
D) 모든 답이 맞습니다

---

## 문제 21-30: EC2 및 컴퓨팅

### 21. EC2 인스턴스의 사용자 데이터(User Data)에 대한 설명으로 올바른 것은?
A) 인스턴스 실행 중에 수정할 수 있습니다
B) 인스턴스 시작 시에만 실행됩니다
C) 최대 64KB까지 지원합니다
D) 암호화되어 저장됩니다

### 22. EC2 인스턴스 메타데이터에 액세스하는 URL은?
A) http://169.254.169.254/latest/meta-data/
B) http://192.168.1.1/meta-data/
C) http://localhost/meta-data/
D) http://10.0.0.1/meta-data/

### 23. 다음 중 EC2 인스턴스의 성능을 일시적으로 향상시킬 수 있는 기능은?
A) Burstable Performance
B) Enhanced Networking
C) Placement Groups
D) Dedicated Hosts

### 24. EC2 Spot 인스턴스에 대한 설명으로 올바른 것은?
A) 항상 사용 가능합니다
B) 온디맨드 가격보다 저렴합니다
C) 중단될 수 없습니다
D) 예약 인스턴스와 동일합니다

### 25. Auto Scaling 그룹에서 인스턴스 종료 정책의 기본 순서는?
A) 가장 오래된 인스턴스 먼저
B) 가장 새로운 인스턴스 먼저
C) 가장 오래된 시작 구성을 가진 인스턴스 먼저
D) 무작위 선택

### 26. EC2 인스턴스에서 EBS 볼륨을 암호화하는 방법은?
A) 인스턴스 생성 후 암호화 설정
B) 볼륨 생성 시 암호화 옵션 선택
C) 운영 체제에서 암호화 설정
D) 자동으로 암호화됩니다

### 27. 다음 중 EC2 인스턴스의 네트워크 성능을 향상시키는 기능은?
A) SR-IOV
B) Enhanced Networking
C) Placement Groups
D) 모든 답이 맞습니다

### 28. EC2 인스턴스 스토어(Instance Store)의 특징은?
A) 인스턴스 중지 시 데이터 보존
B) 네트워크를 통한 액세스
C) 임시 스토리지
D) 스냅샷 생성 가능

### 29. Lambda 함수의 최대 실행 시간은?
A) 5분
B) 15분
C) 30분
D) 1시간

### 30. 다음 중 서버리스 컴퓨팅 서비스가 아닌 것은?
A) AWS Lambda
B) AWS Fargate
C) Amazon EC2
D) AWS Step Functions

---

## 문제 31-40: 스토리지

### 31. S3 스토리지 클래스 중 가장 저렴한 장기 보관용 클래스는?
A) S3 Standard
B) S3 Glacier
C) S3 Glacier Deep Archive
D) S3 Intelligent-Tiering

### 32. S3 버킷 정책과 IAM 정책의 차이점은?
A) S3 버킷 정책은 리소스 기반 정책입니다
B) IAM 정책은 사용자 기반 정책입니다
C) 둘 다 JSON 형식을 사용합니다
D) 모든 답이 맞습니다

### 33. S3 Cross-Region Replication의 요구사항은?
A) 소스와 대상 버킷의 버전 관리 활성화
B) 동일한 AWS 계정
C) 동일한 리전
D) 특별한 설정 불필요

### 34. EBS 볼륨 타입 중 가장 높은 IOPS를 제공하는 것은?
A) gp2 (General Purpose SSD)
B) gp3 (General Purpose SSD)
C) io1 (Provisioned IOPS SSD)
D) io2 (Provisioned IOPS SSD)

### 35. EFS(Elastic File System)의 특징으로 올바른 것은?
A) 블록 스토리지입니다
B) 단일 인스턴스만 마운트 가능합니다
C) NFS 프로토콜을 사용합니다
D) Windows에서만 사용 가능합니다

### 36. S3 Transfer Acceleration의 작동 원리는?
A) 압축을 통한 전송 속도 향상
B) CloudFront 엣지 로케이션 활용
C) 멀티파트 업로드 자동화
D) 네트워크 대역폭 증가

### 37. 다음 중 S3 객체의 메타데이터를 수정하는 방법은?
A) 객체를 다시 업로드
B) PUT Object Copy 사용
C) 메타데이터 API 사용
D) A와 B 모두 가능

### 38. EBS 스냅샷에 대한 설명으로 올바른 것은?
A) 전체 볼륨을 매번 복사합니다
B) 증분 백업 방식을 사용합니다
C) 동일한 AZ에만 저장됩니다
D) 암호화할 수 없습니다

### 39. S3 Lifecycle 정책으로 할 수 있는 작업은?
A) 객체 자동 삭제
B) 스토리지 클래스 전환
C) 불완전한 멀티파트 업로드 정리
D) 모든 답이 맞습니다

### 40. AWS Storage Gateway의 종류가 아닌 것은?
A) File Gateway
B) Volume Gateway
C) Tape Gateway
D) Object Gateway

---

## 문제 41-50: 네트워킹

### 41. VPC의 기본 라우팅 테이블에 대한 설명으로 올바른 것은?
A) 삭제할 수 있습니다
B) 모든 서브넷과 자동으로 연결됩니다
C) 수정할 수 없습니다
D) 인터넷 게이트웨이가 기본으로 연결됩니다

### 42. NAT Gateway와 NAT Instance의 차이점으로 올바른 것은?
A) NAT Gateway는 관리형 서비스입니다
B) NAT Instance는 더 높은 가용성을 제공합니다
C) NAT Gateway는 보안 그룹을 사용합니다
D) NAT Instance가 더 비쌉니다

### 43. VPC Peering 연결에 대한 제한사항은?
A) 전이적 라우팅 지원
B) 중복되는 CIDR 블록 허용
C) 동일한 리전 내에서만 가능
D) 전이적 라우팅 미지원

### 44. 다음 중 Application Load Balancer의 특징이 아닌 것은?
A) Layer 7에서 작동
B) 경로 기반 라우팅 지원
C) 고정 IP 주소 제공
D) WebSocket 지원

### 45. CloudFront의 캐시 동작을 제어하는 방법은?
A) TTL 설정
B) 캐시 정책 사용
C) 헤더 기반 캐싱
D) 모든 답이 맞습니다

### 46. Route 53의 라우팅 정책 중 가중치 기반 라우팅의 용도는?
A) 지연 시간 최소화
B) 트래픽 분산
C) 장애 조치
D) 지리적 라우팅

### 47. VPC Endpoint의 종류는?
A) Gateway Endpoint만 있습니다
B) Interface Endpoint만 있습니다
C) Gateway와 Interface Endpoint 모두 있습니다
D) Network Endpoint만 있습니다

### 48. 보안 그룹과 NACL의 차이점으로 올바른 것은?
A) 보안 그룹은 상태 비저장입니다
B) NACL은 인스턴스 수준에서 작동합니다
C) 보안 그룹은 상태 저장입니다
D) NACL은 허용 규칙만 지원합니다

### 49. Direct Connect의 주요 이점은?
A) 더 높은 대역폭
B) 더 일관된 네트워크 성능
C) 더 낮은 네트워크 비용
D) 모든 답이 맞습니다

### 50. VPC Flow Logs로 캡처할 수 있는 정보는?
A) 네트워크 트래픽 메타데이터
B) 패킷 내용
C) 애플리케이션 로그
D) DNS 쿼리 결과

---

## 문제 51-60: 데이터베이스

### 51. RDS Multi-AZ 배포의 주요 목적은?
A) 읽기 성능 향상
B) 고가용성 제공
C) 비용 절감
D) 확장성 향상

### 52. RDS Read Replica의 특징으로 올바른 것은?
A) 동기식 복제를 사용합니다
B) 자동 장애 조치를 지원합니다
C) 읽기 전용 액세스를 제공합니다
D) 동일한 AZ에만 생성 가능합니다

### 53. DynamoDB의 일관성 모델은?
A) 강한 일관성만 지원
B) 최종 일관성만 지원
C) 강한 일관성과 최종 일관성 모두 지원
D) 일관성을 보장하지 않음

### 54. DynamoDB Global Secondary Index(GSI)의 특징은?
A) 테이블과 동일한 파티션 키를 사용해야 합니다
B) 다른 파티션 키를 사용할 수 있습니다
C) 생성 후 수정할 수 없습니다
D) 최대 5개까지만 생성 가능합니다

### 55. Amazon Aurora의 특징으로 올바른 것은?
A) MySQL과 PostgreSQL 호환
B) 자동 백업 및 복구
C) 최대 15개의 읽기 전용 복제본 지원
D) 모든 답이 맞습니다

### 56. ElastiCache의 엔진 종류는?
A) Redis만 지원
B) Memcached만 지원
C) Redis와 Memcached 모두 지원
D) MongoDB 지원

### 57. DynamoDB Auto Scaling의 기준은?
A) CPU 사용률
B) 메모리 사용률
C) 읽기/쓰기 용량 사용률
D) 네트워크 사용률

### 58. RDS 암호화에 대한 설명으로 올바른 것은?
A) 생성 후 암호화 설정 가능
B) 생성 시에만 암호화 설정 가능
C) 자동으로 암호화됩니다
D) 암호화를 지원하지 않습니다

### 59. Amazon Redshift의 주요 용도는?
A) OLTP 워크로드
B) OLAP 워크로드
C) 실시간 분석
D) 캐싱

### 60. DynamoDB Streams의 용도는?
A) 실시간 백업
B) 데이터 변경 이벤트 캡처
C) 성능 모니터링
D) 보안 감사

---

## 문제 61-65: 모니터링 및 관리

### 61. CloudWatch 사용자 지정 지표의 최대 차원 수는?
A) 5개
B) 10개
C) 15개
D) 20개

### 62. AWS Config의 주요 기능은?
A) 성능 모니터링
B) 리소스 구성 추적
C) 로그 분석
D) 비용 관리

### 63. CloudFormation 스택 업데이트 시 롤백이 발생하는 경우는?
A) 업데이트가 성공한 경우
B) 업데이트가 실패한 경우
C) 사용자가 요청한 경우
D) B와 C 모두

### 64. AWS Systems Manager Parameter Store의 계층적 파라미터 이름 예시는?
A) /myapp/database/username
B) myapp.database.username
C) myapp-database-username
D) myapp_database_username

### 65. Trusted Advisor의 권장사항 범주가 아닌 것은?
A) 비용 최적화
B) 성능
C) 보안
D) 규정 준수

---

## 📊 채점 기준

- **각 문제 1점** (총 65점)
- **합격 기준**: 52점 이상 (80% 정답률)
- **우수**: 58점 이상 (90% 정답률)

## 🔍 다음 단계

1. 시험 완료 후 [상세 해설](./hands-on/detailed-explanations.md) 확인
2. 틀린 문제 영역 [추가 학습](./hands-on/study-resources.md)
3. [시험 전략 가이드](./visuals/exam-strategy.md) 검토
4. [최종 복습 체크리스트](./quiz.md) 완료