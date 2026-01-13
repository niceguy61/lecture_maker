# AWS SAA-C03 모의고사 상세 해설

## 📚 해설 가이드

각 문제의 정답, 해설, 그리고 추가 학습 자료를 제공합니다.
틀린 문제는 반드시 해설을 읽고 관련 AWS 문서를 확인하세요.

---

## 문제 1-10: AWS 기초 및 글로벌 인프라

### 1. AWS 글로벌 인프라
**정답: B) 리전은 최소 2개의 가용 영역으로 구성됩니다**

**해설:**
- 가용 영역(AZ)은 하나 이상의 데이터 센터로 구성됩니다 (A 틀림)
- AWS 리전은 최소 2개, 일반적으로 3개 이상의 AZ로 구성됩니다 (B 정답)
- 엣지 로케이션은 CloudFront와 Route 53 등 일부 서비스만 제공합니다 (C 틀림)
- 로컬 영역은 특정 지역의 최종 사용자에게 더 가까운 위치에 컴퓨팅과 스토리지를 제공하는 확장 기능입니다 (D 틀림)

**참조 링크:**
- [AWS 글로벌 인프라](https://aws.amazon.com/about-aws/global-infrastructure/)
- [가용 영역 및 리전](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html)

### 2. AWS 공동 책임 모델
**정답: D) 운영 체제 패치**

**해설:**
- AWS는 "클라우드의 보안"을 담당하고, 고객은 "클라우드에서의 보안"을 담당합니다
- 물리적 보안, 하이퍼바이저 패치, 네트워크 인프라는 AWS 책임입니다
- 운영 체제 패치, 애플리케이션 보안, 데이터 암호화는 고객 책임입니다

**참조 링크:**
- [AWS 공동 책임 모델](https://aws.amazon.com/compliance/shared-responsibility-model/)

### 3. AWS Well-Architected Framework
**정답: C) 확장성 (Scalability)**

**해설:**
Well-Architected Framework의 5가지 기둥:
1. 보안 (Security)
2. 안정성 (Reliability)
3. 성능 효율성 (Performance Efficiency)
4. 비용 최적화 (Cost Optimization)
5. 운영 우수성 (Operational Excellence)

확장성은 별도의 기둥이 아니라 다른 기둥들에 포함된 개념입니다.

**참조 링크:**
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### 4. AWS 계정 간 리소스 공유
**정답: B) AWS Resource Access Manager (RAM)**

**해설:**
- AWS RAM은 AWS 계정 간 또는 AWS Organizations 내에서 리소스를 안전하게 공유할 수 있게 해줍니다
- VPC 서브넷, Route 53 Resolver 규칙, License Manager 구성 등을 공유할 수 있습니다
- Organizations는 계정 관리용이고, IAM Cross-Account Roles는 권한 위임용입니다

**참조 링크:**
- [AWS Resource Access Manager](https://aws.amazon.com/ram/)

### 5. AWS 무료 계층
**정답: D) Amazon Redshift (160GB 스토리지)**

**해설:**
AWS 무료 계층에 포함되는 서비스:
- EC2: t2.micro 인스턴스 월 750시간
- S3: 5GB 표준 스토리지
- RDS: 20GB 스토리지, 750시간 db.t2.micro

Amazon Redshift는 무료 계층에 포함되지 않습니다.

**참조 링크:**
- [AWS 무료 계층](https://aws.amazon.com/free/)

### 6. API 호출 모니터링
**정답: B) AWS CloudTrail**

**해설:**
- CloudTrail은 AWS API 호출을 기록하고 로깅하는 서비스입니다
- CloudWatch는 메트릭 모니터링, Config는 리소스 구성 추적, X-Ray는 애플리케이션 추적용입니다

**참조 링크:**
- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/)

### 7. 태그 정책 중앙 관리
**정답: C) AWS Organizations**

**해설:**
- AWS Organizations의 태그 정책을 통해 조직 전체의 태그 표준을 정의하고 적용할 수 있습니다
- Resource Groups와 Tag Editor는 태그 관리 도구이지만 정책 적용 기능은 없습니다

**참조 링크:**
- [AWS Organizations 태그 정책](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html)

### 8. 서비스 한도 증가 요청
**정답: D) 모든 답이 맞습니다**

**해설:**
서비스 한도 증가를 요청하는 방법:
- AWS Support Center에서 케이스 생성
- AWS Service Quotas 콘솔에서 직접 요청
- AWS CLI를 통한 프로그래밍 방식 요청

**참조 링크:**
- [AWS Service Quotas](https://aws.amazon.com/servicequotas/)

### 9. 루트 사용자
**정답: C) 계정 설정 변경 시에만 사용해야 합니다**

**해설:**
- 루트 사용자는 계정 설정, 결제 정보 변경 등 특별한 작업에만 사용해야 합니다
- 일상적인 관리 작업에는 IAM 사용자를 사용해야 합니다
- 루트 사용자도 MFA를 설정할 수 있고 설정해야 합니다

**참조 링크:**
- [AWS 루트 사용자 보안 모범 사례](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#lock-away-credentials)

### 10. AWS 서비스 상태 대시보드
**정답: B) AWS Service Health Dashboard**

**해설:**
- AWS Service Health Dashboard는 모든 AWS 서비스의 현재 상태를 보여줍니다
- Personal Health Dashboard는 개별 계정에 영향을 주는 이벤트를 보여줍니다

**참조 링크:**
- [AWS Service Health Dashboard](https://status.aws.amazon.com/)

---

## 문제 11-20: IAM 및 보안

### 11. IAM 정책 평가
**정답: B) 명시적 거부가 우선됩니다**

**해설:**
IAM 정책 평가 순서:
1. 기본적으로 모든 요청은 거부됩니다
2. 명시적 허용이 있으면 허용됩니다
3. 명시적 거부가 있으면 항상 거부됩니다 (최우선)

**참조 링크:**
- [IAM 정책 평가 로직](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)

### 12. IAM 역할 특징
**정답: B) 임시 자격 증명을 제공합니다**

**해설:**
- IAM 역할은 임시 보안 자격 증명을 제공합니다
- 사용자, 애플리케이션, AWS 서비스가 역할을 맡을 수 있습니다
- 패스워드나 영구적인 액세스 키가 없습니다

**참조 링크:**
- [IAM 역할](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)

### 13. AWS STS 기능
**정답: B) 임시 보안 자격 증명 제공**

**해설:**
- STS(Security Token Service)는 임시 보안 자격 증명을 생성하고 제공합니다
- AssumeRole, GetSessionToken 등의 API를 제공합니다

**참조 링크:**
- [AWS STS](https://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html)

### 14. 세밀한 액세스 제어
**정답: C) IAM 정책**

**해설:**
- IAM 정책은 AWS 리소스에 대한 세밀한 액세스 제어를 제공합니다
- 보안 그룹과 NACL은 네트워크 수준 제어입니다
- WAF는 웹 애플리케이션 방화벽입니다

**참조 링크:**
- [IAM 정책](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)

### 15. Cross-Account Access
**정답: C) IAM 역할 사용**

**해설:**
- IAM 역할을 사용한 Cross-Account Access가 가장 안전한 방법입니다
- 자격 증명을 공유할 필요가 없고 임시 자격 증명을 사용합니다

**참조 링크:**
- [Cross-Account Access](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html)

### 16. AWS CloudHSM 용도
**정답: B) 암호화 키 관리**

**해설:**
- CloudHSM은 전용 하드웨어 보안 모듈에서 암호화 키를 생성하고 관리합니다
- FIPS 140-2 Level 3 인증을 받은 HSM을 제공합니다

**참조 링크:**
- [AWS CloudHSM](https://aws.amazon.com/cloudhsm/)

### 17. Secrets Manager vs Parameter Store
**정답: B) 자동 로테이션 기능**

**해설:**
- Secrets Manager는 자동 로테이션 기능을 제공합니다
- Parameter Store는 수동으로 값을 업데이트해야 합니다
- 둘 다 암호화를 지원하지만 Secrets Manager가 더 비쌉니다

**참조 링크:**
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)

### 18. 계정 보안 강화
**정답: C) 루트 계정 일상 사용**

**해설:**
- 루트 계정은 일상적으로 사용하면 안 됩니다
- MFA 활성화, 강력한 패스워드 정책, 정기적인 키 로테이션은 모두 보안 강화 방법입니다

**참조 링크:**
- [AWS 보안 모범 사례](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

### 19. AWS GuardDuty 기능
**정답: B) 위협 탐지 및 모니터링**

**해설:**
- GuardDuty는 머신러닝을 사용하여 악의적인 활동과 무단 동작을 탐지합니다
- VPC Flow Logs, DNS 로그, CloudTrail 이벤트를 분석합니다

**참조 링크:**
- [Amazon GuardDuty](https://aws.amazon.com/guardduty/)

### 20. IAM 정책 조건
**정답: D) 모든 답이 맞습니다**

**해설:**
IAM 정책의 조건 요소로 제어할 수 있는 것들:
- 시간 기반 액세스 (DateGreaterThan, DateLessThan)
- IP 주소 기반 액세스 (IpAddress, NotIpAddress)
- MFA 요구사항 (aws:MultiFactorAuthPresent)

**참조 링크:**
- [IAM 정책 조건](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html)

---

## 문제 21-30: EC2 및 컴퓨팅

### 21. EC2 사용자 데이터
**정답: B) 인스턴스 시작 시에만 실행됩니다**

**해설:**
- 사용자 데이터는 인스턴스 첫 부팅 시에만 실행됩니다
- 최대 16KB까지 지원합니다
- Base64로 인코딩되어 전달됩니다

**참조 링크:**
- [EC2 사용자 데이터](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)

### 22. EC2 메타데이터 URL
**정답: A) http://169.254.169.254/latest/meta-data/**

**해설:**
- 169.254.169.254는 링크 로컬 주소로 EC2 메타데이터 서비스에 액세스하는 데 사용됩니다
- 인스턴스 내부에서만 접근 가능합니다

**참조 링크:**
- [EC2 인스턴스 메타데이터](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html)

### 23. EC2 성능 향상 기능
**정답: A) Burstable Performance**

**해설:**
- Burstable Performance는 T 시리즈 인스턴스의 기능으로 CPU 크레딧을 사용하여 일시적으로 성능을 향상시킵니다
- Enhanced Networking과 Placement Groups는 네트워크 성능 향상 기능입니다

**참조 링크:**
- [Burstable Performance 인스턴스](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html)

### 24. EC2 Spot 인스턴스
**정답: B) 온디맨드 가격보다 저렴합니다**

**해설:**
- Spot 인스턴스는 온디맨드 가격보다 최대 90% 저렴합니다
- AWS가 용량이 필요할 때 2분 전 통지 후 중단될 수 있습니다
- 항상 사용 가능하지 않으며 중단될 수 있습니다

**참조 링크:**
- [EC2 Spot 인스턴스](https://aws.amazon.com/ec2/spot/)

### 25. Auto Scaling 종료 정책
**정답: C) 가장 오래된 시작 구성을 가진 인스턴스 먼저**

**해설:**
기본 종료 정책 순서:
1. 가장 오래된 시작 구성을 가진 인스턴스
2. 다음 결제 시간에 가장 가까운 인스턴스
3. 무작위 선택

**참조 링크:**
- [Auto Scaling 종료 정책](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-instance-termination.html)

### 26. EBS 볼륨 암호화
**정답: B) 볼륨 생성 시 암호화 옵션 선택**

**해설:**
- EBS 볼륨은 생성 시에 암호화를 설정해야 합니다
- 기존 볼륨은 스냅샷을 생성하고 암호화된 볼륨으로 복원해야 합니다

**참조 링크:**
- [EBS 암호화](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)

### 27. EC2 네트워크 성능 향상
**정답: D) 모든 답이 맞습니다**

**해설:**
- SR-IOV: 하드웨어 가상화를 통한 네트워크 성능 향상
- Enhanced Networking: 높은 대역폭, 낮은 지연 시간 제공
- Placement Groups: 인스턴스 간 네트워크 성능 최적화

**참조 링크:**
- [Enhanced Networking](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/enhanced-networking.html)

### 28. EC2 인스턴스 스토어
**정답: C) 임시 스토리지**

**해설:**
- 인스턴스 스토어는 임시 스토리지로 인스턴스 중지/종료 시 데이터가 손실됩니다
- 물리적으로 호스트 컴퓨터에 연결된 디스크입니다
- 스냅샷을 생성할 수 없습니다

**참조 링크:**
- [EC2 인스턴스 스토어](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html)

### 29. Lambda 최대 실행 시간
**정답: B) 15분**

**해설:**
- AWS Lambda 함수의 최대 실행 시간은 15분(900초)입니다
- 기본값은 3초이며 최대 15분까지 설정할 수 있습니다

**참조 링크:**
- [Lambda 제한](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)

### 30. 서버리스 컴퓨팅 서비스
**정답: C) Amazon EC2**

**해설:**
- EC2는 가상 서버를 제공하는 IaaS로 서버리스가 아닙니다
- Lambda, Fargate, Step Functions는 모두 서버리스 서비스입니다

**참조 링크:**
- [AWS 서버리스](https://aws.amazon.com/serverless/)

---

## 문제 31-40: 스토리지

### 31. S3 최저가 스토리지 클래스
**정답: C) S3 Glacier Deep Archive**

**해설:**
S3 스토리지 클래스별 비용 (낮은 순):
1. S3 Glacier Deep Archive (가장 저렴)
2. S3 Glacier
3. S3 Intelligent-Tiering
4. S3 Standard

**참조 링크:**
- [S3 스토리지 클래스](https://aws.amazon.com/s3/storage-classes/)

### 32. S3 버킷 정책 vs IAM 정책
**정답: D) 모든 답이 맞습니다**

**해설:**
- S3 버킷 정책: 리소스 기반 정책 (버킷에 연결)
- IAM 정책: 사용자 기반 정책 (사용자/역할에 연결)
- 둘 다 JSON 형식을 사용합니다

**참조 링크:**
- [S3 버킷 정책](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html)

### 33. S3 Cross-Region Replication 요구사항
**정답: A) 소스와 대상 버킷의 버전 관리 활성화**

**해설:**
CRR 요구사항:
- 소스와 대상 버킷 모두 버전 관리 활성화
- 서로 다른 리전에 위치
- 적절한 IAM 권한 설정

**참조 링크:**
- [S3 Cross-Region Replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)

### 34. 최고 IOPS EBS 볼륨
**정답: D) io2 (Provisioned IOPS SSD)**

**해설:**
EBS 볼륨 타입별 최대 IOPS:
- io2: 64,000 IOPS (최고)
- io1: 64,000 IOPS
- gp3: 16,000 IOPS
- gp2: 16,000 IOPS

**참조 링크:**
- [EBS 볼륨 타입](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)

### 35. EFS 특징
**정답: C) NFS 프로토콜을 사용합니다**

**해설:**
- EFS는 파일 스토리지 서비스입니다 (블록 스토리지 아님)
- 여러 인스턴스에서 동시 마운트 가능합니다
- NFS v4.1 프로토콜을 사용합니다
- Linux에서 사용 가능합니다

**참조 링크:**
- [Amazon EFS](https://aws.amazon.com/efs/)

### 36. S3 Transfer Acceleration
**정답: B) CloudFront 엣지 로케이션 활용**

**해설:**
- Transfer Acceleration은 CloudFront의 전 세계 엣지 로케이션을 활용합니다
- 엣지 로케이션에서 AWS 백본 네트워크를 통해 S3로 전송합니다

**참조 링크:**
- [S3 Transfer Acceleration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html)

### 37. S3 객체 메타데이터 수정
**정답: D) A와 B 모두 가능**

**해설:**
S3 객체 메타데이터 수정 방법:
- 객체를 다시 업로드 (새 메타데이터와 함께)
- PUT Object Copy API 사용 (동일한 키로 복사하면서 메타데이터 변경)

**참조 링크:**
- [S3 객체 메타데이터](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html)

### 38. EBS 스냅샷
**정답: B) 증분 백업 방식을 사용합니다**

**해설:**
- EBS 스냅샷은 증분 백업 방식을 사용합니다
- 첫 번째 스냅샷은 전체 복사, 이후는 변경된 블록만 저장합니다
- 리전 간 복사 가능하며 암호화할 수 있습니다

**참조 링크:**
- [EBS 스냅샷](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)

### 39. S3 Lifecycle 정책
**정답: D) 모든 답이 맞습니다**

**해설:**
S3 Lifecycle 정책으로 가능한 작업:
- 객체 자동 삭제 (만료일 설정)
- 스토리지 클래스 전환 (Standard → IA → Glacier)
- 불완전한 멀티파트 업로드 정리

**참조 링크:**
- [S3 Lifecycle 관리](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)

### 40. Storage Gateway 종류
**정답: D) Object Gateway**

**해설:**
AWS Storage Gateway 종류:
- File Gateway (NFS/SMB)
- Volume Gateway (iSCSI)
- Tape Gateway (VTL)

Object Gateway는 존재하지 않습니다.

**참조 링크:**
- [AWS Storage Gateway](https://aws.amazon.com/storagegateway/)

---

## 문제 41-50: 네트워킹

### 41. VPC 기본 라우팅 테이블
**정답: B) 모든 서브넷과 자동으로 연결됩니다**

**해설:**
- 기본 라우팅 테이블은 삭제할 수 없습니다
- 명시적으로 다른 라우팅 테이블과 연결되지 않은 모든 서브넷이 자동으로 연결됩니다
- 수정은 가능하지만 권장하지 않습니다

**참조 링크:**
- [VPC 라우팅 테이블](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)

### 42. NAT Gateway vs NAT Instance
**정답: A) NAT Gateway는 관리형 서비스입니다**

**해설:**
- NAT Gateway: AWS 관리형, 높은 가용성, 보안 그룹 미지원
- NAT Instance: 사용자 관리, 보안 그룹 지원, 더 저렴

**참조 링크:**
- [NAT Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)

### 43. VPC Peering 제한사항
**정답: D) 전이적 라우팅 미지원**

**해설:**
VPC Peering 제한사항:
- 전이적 라우팅 미지원 (A-B, B-C 연결되어도 A-C 직접 통신 불가)
- 중복되는 CIDR 블록 불허용
- 리전 간 피어링 지원

**참조 링크:**
- [VPC Peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html)

### 44. Application Load Balancer
**정답: C) 고정 IP 주소 제공**

**해설:**
ALB 특징:
- Layer 7에서 작동 ✓
- 경로 기반 라우팅 지원 ✓
- WebSocket 지원 ✓
- 고정 IP 주소 미제공 (Network Load Balancer가 제공)

**참조 링크:**
- [Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/)

### 45. CloudFront 캐시 제어
**정답: D) 모든 답이 맞습니다**

**해설:**
CloudFront 캐시 제어 방법:
- TTL 설정 (Cache-Control, Expires 헤더)
- 캐시 정책 사용
- 헤더, 쿠키, 쿼리 스트링 기반 캐싱

**참조 링크:**
- [CloudFront 캐싱](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html)

### 46. Route 53 가중치 기반 라우팅
**정답: B) 트래픽 분산**

**해설:**
- 가중치 기반 라우팅은 여러 리소스 간 트래픽을 비율로 분산합니다
- A/B 테스트, 점진적 배포에 유용합니다

**참조 링크:**
- [Route 53 라우팅 정책](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html)

### 47. VPC Endpoint 종류
**정답: C) Gateway와 Interface Endpoint 모두 있습니다**

**해설:**
VPC Endpoint 종류:
- Gateway Endpoint: S3, DynamoDB 지원
- Interface Endpoint: 대부분의 AWS 서비스 지원

**참조 링크:**
- [VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html)

### 48. 보안 그룹 vs NACL
**정답: C) 보안 그룹은 상태 저장입니다**

**해설:**
- 보안 그룹: 상태 저장, 인스턴스 수준, 허용 규칙만
- NACL: 상태 비저장, 서브넷 수준, 허용/거부 규칙

**참조 링크:**
- [보안 그룹과 NACL](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Security.html)

### 49. Direct Connect 이점
**정답: D) 모든 답이 맞습니다**

**해설:**
Direct Connect 이점:
- 더 높은 대역폭 (최대 100Gbps)
- 일관된 네트워크 성능
- 데이터 전송 비용 절감

**참조 링크:**
- [AWS Direct Connect](https://aws.amazon.com/directconnect/)

### 50. VPC Flow Logs
**정답: A) 네트워크 트래픽 메타데이터**

**해설:**
- VPC Flow Logs는 네트워크 트래픽의 메타데이터를 캡처합니다
- 소스/대상 IP, 포트, 프로토콜, 패킷 수 등을 기록합니다
- 패킷 내용은 캡처하지 않습니다

**참조 링크:**
- [VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)

---

## 문제 51-60: 데이터베이스

### 51. RDS Multi-AZ 목적
**정답: B) 고가용성 제공**

**해설:**
- Multi-AZ는 고가용성과 재해 복구를 위한 기능입니다
- 동기식 복제를 사용하여 자동 장애 조치를 제공합니다
- 읽기 성능 향상은 Read Replica의 목적입니다

**참조 링크:**
- [RDS Multi-AZ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)

### 52. RDS Read Replica
**정답: C) 읽기 전용 액세스를 제공합니다**

**해설:**
- Read Replica는 비동기식 복제를 사용합니다
- 읽기 전용 액세스만 제공합니다
- 자동 장애 조치를 지원하지 않습니다
- 다른 리전에도 생성 가능합니다

**참조 링크:**
- [RDS Read Replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)

### 53. DynamoDB 일관성 모델
**정답: C) 강한 일관성과 최종 일관성 모두 지원**

**해설:**
- DynamoDB는 기본적으로 최종 일관성을 제공합니다
- ConsistentRead 파라미터를 true로 설정하면 강한 일관성을 사용할 수 있습니다

**참조 링크:**
- [DynamoDB 일관성](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)

### 54. DynamoDB GSI
**정답: B) 다른 파티션 키를 사용할 수 있습니다**

**해설:**
- GSI는 테이블과 다른 파티션 키와 정렬 키를 사용할 수 있습니다
- 생성 후에도 수정 가능합니다
- 테이블당 최대 20개까지 생성 가능합니다

**참조 링크:**
- [DynamoDB GSI](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html)

### 55. Amazon Aurora 특징
**정답: D) 모든 답이 맞습니다**

**해설:**
Aurora 특징:
- MySQL과 PostgreSQL 호환 ✓
- 자동 백업 및 복구 ✓
- 최대 15개의 읽기 전용 복제본 지원 ✓

**참조 링크:**
- [Amazon Aurora](https://aws.amazon.com/rds/aurora/)

### 56. ElastiCache 엔진
**정답: C) Redis와 Memcached 모두 지원**

**해설:**
- ElastiCache는 Redis와 Memcached 두 엔진을 모두 지원합니다
- Redis: 데이터 지속성, 복제, 클러스터링 지원
- Memcached: 단순한 키-값 캐싱

**참조 링크:**
- [Amazon ElastiCache](https://aws.amazon.com/elasticache/)

### 57. DynamoDB Auto Scaling 기준
**정답: C) 읽기/쓰기 용량 사용률**

**해설:**
- DynamoDB Auto Scaling은 읽기/쓰기 용량 사용률을 기준으로 합니다
- 목표 사용률을 설정하고 자동으로 용량을 조정합니다

**참조 링크:**
- [DynamoDB Auto Scaling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html)

### 58. RDS 암호화
**정답: B) 생성 시에만 암호화 설정 가능**

**해설:**
- RDS 인스턴스는 생성 시에만 암호화를 설정할 수 있습니다
- 기존 인스턴스는 스냅샷을 생성하고 암호화된 인스턴스로 복원해야 합니다

**참조 링크:**
- [RDS 암호화](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html)

### 59. Amazon Redshift 용도
**정답: B) OLAP 워크로드**

**해설:**
- Redshift는 데이터 웨어하우스 서비스로 OLAP(Online Analytical Processing) 워크로드에 최적화되어 있습니다
- 대용량 데이터 분석과 복잡한 쿼리에 적합합니다

**참조 링크:**
- [Amazon Redshift](https://aws.amazon.com/redshift/)

### 60. DynamoDB Streams 용도
**정답: B) 데이터 변경 이벤트 캡처**

**해설:**
- DynamoDB Streams는 테이블의 데이터 변경 이벤트를 캡처합니다
- 실시간으로 데이터 변경사항을 다른 서비스로 전달할 수 있습니다

**참조 링크:**
- [DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)

---

## 문제 61-65: 모니터링 및 관리

### 61. CloudWatch 사용자 지정 지표 차원
**정답: B) 10개**

**해설:**
- CloudWatch 사용자 지정 지표는 최대 10개의 차원을 가질 수 있습니다
- 차원은 지표를 필터링하고 그룹화하는 데 사용됩니다

**참조 링크:**
- [CloudWatch 지표](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html)

### 62. AWS Config 기능
**정답: B) 리소스 구성 추적**

**해설:**
- AWS Config는 AWS 리소스의 구성 변경사항을 추적하고 기록합니다
- 규정 준수 모니터링과 구성 변경 감사에 사용됩니다

**참조 링크:**
- [AWS Config](https://aws.amazon.com/config/)

### 63. CloudFormation 롤백
**정답: D) B와 C 모두**

**해설:**
CloudFormation 롤백 발생 경우:
- 스택 업데이트가 실패한 경우 (자동 롤백)
- 사용자가 명시적으로 롤백을 요청한 경우

**참조 링크:**
- [CloudFormation 스택 업데이트](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks.html)

### 64. Parameter Store 계층적 이름
**정답: A) /myapp/database/username**

**해설:**
- Systems Manager Parameter Store는 슬래시(/)를 사용하여 계층적 파라미터 이름을 지원합니다
- 이를 통해 파라미터를 논리적으로 그룹화할 수 있습니다

**참조 링크:**
- [Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)

### 65. Trusted Advisor 범주
**정답: D) 규정 준수**

**해설:**
Trusted Advisor 권장사항 범주:
- 비용 최적화 ✓
- 성능 ✓
- 보안 ✓
- 내결함성
- 서비스 한도

규정 준수는 별도 범주가 아닙니다.

**참조 링크:**
- [AWS Trusted Advisor](https://aws.amazon.com/premiumsupport/technology/trusted-advisor/)

---

## 📊 점수 계산 및 분석

### 점수 계산 방법
- 각 문제: 1점
- 총점: 65점
- 합격 기준: 52점 이상 (80%)

### 영역별 분석
1. **AWS 기초 (1-10번)**: ___/10점
2. **IAM 및 보안 (11-20번)**: ___/10점
3. **EC2 및 컴퓨팅 (21-30번)**: ___/10점
4. **스토리지 (31-40번)**: ___/10점
5. **네트워킹 (41-50번)**: ___/10점
6. **데이터베이스 (51-60번)**: ___/10점
7. **모니터링 및 관리 (61-65번)**: ___/5점

### 취약점 분석 및 개선 방안
점수가 낮은 영역에 대해 추가 학습을 진행하세요:

- **70% 미만**: 해당 영역 전체 복습 필요
- **70-80%**: 틀린 문제 중심 복습
- **80% 이상**: 간단한 복습으로 충분

## 🔗 추가 학습 자료

### 공식 AWS 문서
- [AWS 아키텍처 센터](https://aws.amazon.com/architecture/)
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)
- [AWS 백서](https://aws.amazon.com/whitepapers/)

### 실습 환경
- [AWS 실습 랩](https://aws.amazon.com/training/hands-on-labs/)
- [AWS 솔루션 아키텍트 샘플 문제](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Sample-Questions.pdf)

이 해설을 통해 틀린 문제를 이해하고 취약한 영역을 보완하여 실제 시험에서 좋은 결과를 얻으시기 바랍니다!