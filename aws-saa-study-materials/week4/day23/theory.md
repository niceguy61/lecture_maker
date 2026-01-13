# Day 23: CloudTrail & AWS 보안 서비스

## 학습 목표
- AWS CloudTrail의 역할과 중요성 이해
- AWS 보안 서비스들의 특징과 사용 사례 파악
- 보안 모니터링 및 컴플라이언스 전략 수립
- 보안 사고 대응 및 감사 로그 분석 방법 학습

## 1. AWS CloudTrail 개요

### CloudTrail이란?
AWS CloudTrail은 AWS 계정의 거버넌스, 컴플라이언스, 운영 감사, 위험 감사를 지원하는 서비스입니다. CloudTrail을 사용하면 AWS 인프라 전반에서 계정 활동과 관련된 작업을 기록, 지속적으로 모니터링 및 보관할 수 있습니다.

### CloudTrail의 핵심 기능

```mermaid
graph TB
    A[AWS CloudTrail] --> B[API 호출 로깅]
    A --> C[이벤트 기록]
    A --> D[보안 분석]
    A --> E[컴플라이언스 지원]
    
    B --> B1[모든 AWS API 호출 추적]
    B --> B2[사용자 및 역할 식별]
    B --> B3[소스 IP 주소 기록]
    
    C --> C1[관리 이벤트]
    C --> C2[데이터 이벤트]
    C --> C3[인사이트 이벤트]
    
    D --> D1[비정상적인 활동 탐지]
    D --> D2[보안 사고 조사]
    D --> D3[액세스 패턴 분석]
    
    E --> E1[감사 로그 제공]
    E --> E2[규정 준수 보고서]
    E --> E3[장기 보관]
```

### CloudTrail 이벤트 유형

**1. 관리 이벤트 (Management Events)**
- AWS 리소스에 대한 관리 작업
- 예: EC2 인스턴스 생성, IAM 정책 변경, VPC 설정 수정

**2. 데이터 이벤트 (Data Events)**
- 리소스 내부의 데이터 액세스 작업
- 예: S3 객체 읽기/쓰기, Lambda 함수 실행

**3. 인사이트 이벤트 (Insight Events)**
- 비정상적인 활동 패턴 탐지
- 예: 평소보다 많은 API 호출, 비정상적인 오류율

## 2. CloudTrail 아키텍처

```mermaid
graph LR
    A[AWS Services] --> B[CloudTrail]
    B --> C[S3 Bucket]
    B --> D[CloudWatch Logs]
    B --> E[EventBridge]
    
    C --> F[Log Files]
    D --> G[Real-time Monitoring]
    E --> H[Automated Response]
    
    F --> I[Long-term Storage]
    F --> J[Compliance Archive]
    
    G --> K[CloudWatch Alarms]
    G --> L[SNS Notifications]
    
    H --> M[Lambda Functions]
    H --> N[Security Automation]
```

### CloudTrail 로그 구조

```json
{
  "eventVersion": "1.08",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AIDACKCEVSQ6C2EXAMPLE",
    "arn": "arn:aws:iam::123456789012:user/johndoe",
    "accountId": "123456789012",
    "userName": "johndoe"
  },
  "eventTime": "2023-01-01T12:00:00Z",
  "eventSource": "ec2.amazonaws.com",
  "eventName": "RunInstances",
  "awsRegion": "us-east-1",
  "sourceIPAddress": "203.0.113.12",
  "userAgent": "aws-cli/2.0.0",
  "requestParameters": {
    "instanceType": "t3.micro",
    "imageId": "ami-0abcdef1234567890"
  },
  "responseElements": {
    "instancesSet": {
      "items": [
        {
          "instanceId": "i-1234567890abcdef0"
        }
      ]
    }
  }
}
```

## 3. AWS 보안 서비스 생태계

### 보안 서비스 전체 구조

```mermaid
graph TB
    A[AWS Security Services] --> B[Identity & Access]
    A --> C[Detection & Response]
    A --> D[Data Protection]
    A --> E[Infrastructure Protection]
    A --> F[Compliance & Governance]
    
    B --> B1[IAM]
    B --> B2[AWS SSO]
    B --> B3[Cognito]
    B --> B4[Directory Service]
    
    C --> C1[GuardDuty]
    C --> C2[Security Hub]
    C --> C3[Detective]
    C --> C4[Macie]
    
    D --> D1[KMS]
    D --> D2[CloudHSM]
    D --> D3[Certificate Manager]
    D --> D4[Secrets Manager]
    
    E --> E1[WAF]
    E --> E2[Shield]
    E --> E3[Firewall Manager]
    E --> E4[Network Firewall]
    
    F --> F1[CloudTrail]
    F --> F2[Config]
    F --> F3[Audit Manager]
    F --> F4[Control Tower]
```

## 4. 핵심 보안 서비스 상세

### AWS GuardDuty
지능형 위협 탐지 서비스로, 머신러닝을 사용하여 악의적인 활동을 탐지합니다.

```mermaid
graph LR
    A[Data Sources] --> B[GuardDuty]
    A1[CloudTrail Events] --> B
    A2[DNS Logs] --> B
    A3[VPC Flow Logs] --> B
    A4[S3 Data Events] --> B
    
    B --> C[Threat Intelligence]
    B --> D[Machine Learning]
    B --> E[Anomaly Detection]
    
    C --> F[Findings]
    D --> F
    E --> F
    
    F --> G[Security Hub]
    F --> H[EventBridge]
    F --> I[SNS/Email]
```

**GuardDuty 탐지 유형:**
- 악성 IP 통신
- 암호화폐 채굴
- 데이터 유출 시도
- 권한 상승 공격
- 봇넷 활동

### AWS Security Hub
중앙 집중식 보안 관리 대시보드로, 여러 보안 서비스의 결과를 통합합니다.

```mermaid
graph TB
    A[Security Hub] --> B[Security Standards]
    A --> C[Findings Aggregation]
    A --> D[Compliance Monitoring]
    
    B --> B1[AWS Foundational]
    B --> B2[CIS Benchmarks]
    B --> B3[PCI DSS]
    B --> B4[AWS Control Tower]
    
    C --> C1[GuardDuty]
    C --> C2[Inspector]
    C --> C3[Macie]
    C --> C4[Config]
    C --> C5[Third-party Tools]
    
    D --> D1[Compliance Score]
    D --> D2[Failed Checks]
    D --> D3[Remediation Actions]
```

### AWS Config
AWS 리소스 구성을 지속적으로 모니터링하고 평가하는 서비스입니다.

```mermaid
graph LR
    A[AWS Resources] --> B[Config]
    B --> C[Configuration Items]
    B --> D[Configuration History]
    B --> E[Config Rules]
    
    C --> F[Current State]
    D --> G[Change Timeline]
    E --> H[Compliance Evaluation]
    
    F --> I[Configuration Snapshots]
    G --> J[Change Notifications]
    H --> K[Non-compliant Resources]
    
    I --> L[S3 Storage]
    J --> M[SNS Topics]
    K --> N[Remediation Actions]
```

## 5. 데이터 보호 서비스

### AWS KMS (Key Management Service)

```mermaid
graph TB
    A[AWS KMS] --> B[Customer Master Keys]
    A --> C[Data Keys]
    A --> D[Key Policies]
    
    B --> B1[AWS Managed Keys]
    B --> B2[Customer Managed Keys]
    B --> B3[AWS Owned Keys]
    
    C --> C1[Envelope Encryption]
    C --> C2[Data Key Generation]
    C --> C3[Local Encryption]
    
    D --> D1[Key Usage Permissions]
    D --> D2[Administrative Permissions]
    D --> D3[Cross-account Access]
    
    B1 --> E[AWS Services Integration]
    B2 --> F[Custom Applications]
    B3 --> G[Service-to-Service]
```

**KMS 암호화 프로세스:**

```mermaid
sequenceDiagram
    participant App as Application
    participant KMS as AWS KMS
    participant S3 as Amazon S3
    
    App->>KMS: GenerateDataKey(CMK-ID)
    KMS->>App: PlaintextKey + EncryptedKey
    App->>App: Encrypt data with PlaintextKey
    App->>S3: Store encrypted data + EncryptedKey
    App->>App: Delete PlaintextKey from memory
    
    Note over App,S3: Decryption Process
    App->>S3: Retrieve encrypted data + EncryptedKey
    App->>KMS: Decrypt(EncryptedKey)
    KMS->>App: PlaintextKey
    App->>App: Decrypt data with PlaintextKey
    App->>App: Delete PlaintextKey from memory
```

### AWS Secrets Manager
데이터베이스 자격 증명, API 키 및 기타 보안 정보를 안전하게 저장하고 관리합니다.

```mermaid
graph LR
    A[Applications] --> B[Secrets Manager]
    B --> C[Encrypted Storage]
    B --> D[Automatic Rotation]
    B --> E[Fine-grained Access]
    
    C --> C1[Database Credentials]
    C --> C2[API Keys]
    C --> C3[OAuth Tokens]
    C --> C4[Custom Secrets]
    
    D --> D1[Lambda Functions]
    D --> D2[Rotation Schedules]
    D --> D3[Version Management]
    
    E --> E1[IAM Policies]
    E --> E2[Resource Policies]
    E --> E3[VPC Endpoints]
```

## 6. 네트워크 보안

### AWS WAF (Web Application Firewall)

```mermaid
graph TB
    A[Internet Traffic] --> B[AWS WAF]
    B --> C[Web ACLs]
    B --> D[Rules]
    B --> E[Rate Limiting]
    
    C --> F[Allow/Block/Count]
    D --> G[IP Conditions]
    D --> H[String Matching]
    D --> I[SQL Injection Protection]
    D --> J[XSS Protection]
    
    E --> K[Request Rate Limits]
    E --> L[Geographic Restrictions]
    
    F --> M[CloudFront]
    F --> N[Application Load Balancer]
    F --> O[API Gateway]
```

**WAF 규칙 예시:**
- SQL 인젝션 공격 차단
- 크로스 사이트 스크립팅(XSS) 방지
- 특정 국가에서의 접근 차단
- 비정상적인 요청 패턴 탐지

### AWS Shield
DDoS 공격으로부터 보호하는 관리형 서비스입니다.

```mermaid
graph LR
    A[DDoS Attack] --> B[AWS Shield]
    B --> C[Shield Standard]
    B --> D[Shield Advanced]
    
    C --> C1[Layer 3/4 Protection]
    C --> C2[Always-on Detection]
    C --> C3[Automatic Mitigation]
    
    D --> D1[Enhanced Protection]
    D --> D2[24/7 DRT Support]
    D --> D3[Cost Protection]
    D --> D4[Advanced Reporting]
    
    C1 --> E[CloudFront]
    C1 --> F[Route 53]
    
    D1 --> G[EC2]
    D1 --> H[ELB]
    D1 --> I[Global Accelerator]
```

## 7. 보안 모니터링 및 대응

### 보안 이벤트 대응 워크플로우

```mermaid
graph TB
    A[Security Event] --> B[Detection]
    B --> C[Analysis]
    C --> D[Classification]
    D --> E[Response]
    E --> F[Recovery]
    F --> G[Lessons Learned]
    
    B --> B1[GuardDuty Findings]
    B --> B2[CloudTrail Anomalies]
    B --> B3[Config Rule Violations]
    
    C --> C1[Event Correlation]
    C --> C2[Impact Assessment]
    C --> C3[Root Cause Analysis]
    
    D --> D1[False Positive]
    D --> D2[Low Severity]
    D --> D3[Medium Severity]
    D --> D4[High Severity]
    D --> D5[Critical]
    
    E --> E1[Automated Response]
    E --> E2[Manual Investigation]
    E --> E3[Containment Actions]
    
    F --> F1[System Restoration]
    F --> F2[Security Hardening]
    F --> F3[Monitoring Enhancement]
```

### 자동화된 보안 대응

```mermaid
graph LR
    A[Security Finding] --> B[EventBridge]
    B --> C[Lambda Function]
    C --> D[Automated Actions]
    
    D --> D1[Isolate Instance]
    D --> D2[Block IP Address]
    D --> D3[Revoke Credentials]
    D --> D4[Create Snapshot]
    
    C --> E[Notifications]
    E --> E1[SNS Topic]
    E --> E2[Slack/Teams]
    E --> E3[Email Alert]
    E --> E4[Ticket Creation]
```

## 8. 컴플라이언스 및 거버넌스

### AWS Control Tower
멀티 계정 환경을 위한 거버넌스 및 컴플라이언스 서비스입니다.

```mermaid
graph TB
    A[Control Tower] --> B[Landing Zone]
    A --> C[Guardrails]
    A --> D[Account Factory]
    A --> E[Dashboard]
    
    B --> B1[Multi-account Structure]
    B --> B2[Centralized Logging]
    B --> B3[Cross-account Access]
    
    C --> C1[Preventive Guardrails]
    C --> C2[Detective Guardrails]
    C --> C3[Mandatory Guardrails]
    C --> C4[Strongly Recommended]
    
    D --> D1[Automated Provisioning]
    D --> D2[Baseline Configuration]
    D --> D3[Service Catalog Integration]
    
    E --> E1[Compliance Status]
    E --> E2[Account Overview]
    E --> E3[Guardrail Violations]
```

### 컴플라이언스 프레임워크 매핑

```mermaid
graph LR
    A[Compliance Requirements] --> B[AWS Services]
    
    A1[SOC 2] --> B1[CloudTrail + Config]
    A2[PCI DSS] --> B2[WAF + Shield + KMS]
    A3[HIPAA] --> B3[KMS + VPC + IAM]
    A4[GDPR] --> B4[Macie + KMS + CloudTrail]
    A5[ISO 27001] --> B5[Security Hub + GuardDuty]
    
    B1 --> C1[Audit Logging]
    B2 --> C2[Data Protection]
    B3 --> C3[Access Control]
    B4 --> C4[Data Discovery]
    B5 --> C5[Security Monitoring]
```

## 9. 보안 모범 사례

### 1. 최소 권한 원칙 (Principle of Least Privilege)
```mermaid
graph TB
    A[User/Role] --> B[Minimum Required Permissions]
    B --> C[Regular Review]
    C --> D[Permission Adjustment]
    D --> B
    
    B --> B1[Specific Actions Only]
    B --> B2[Limited Resources]
    B --> B3[Time-bound Access]
    
    C --> C1[Access Analyzer]
    C --> C2[CloudTrail Analysis]
    C --> C3[Unused Permission Detection]
```

### 2. 심층 방어 (Defense in Depth)
```mermaid
graph LR
    A[Internet] --> B[WAF/Shield]
    B --> C[VPC/Security Groups]
    C --> D[IAM/RBAC]
    D --> E[Application Security]
    E --> F[Data Encryption]
    F --> G[Monitoring/Logging]
    
    B --> B1[DDoS Protection]
    C --> C1[Network Isolation]
    D --> D1[Access Control]
    E --> E1[Input Validation]
    F --> F1[Data at Rest/Transit]
    G --> G1[Threat Detection]
```

### 3. 지속적인 모니터링
```mermaid
graph TB
    A[Continuous Monitoring] --> B[Real-time Detection]
    A --> C[Automated Response]
    A --> D[Regular Assessment]
    
    B --> B1[GuardDuty]
    B --> B2[CloudWatch]
    B --> B3[Security Hub]
    
    C --> C1[Lambda Functions]
    C --> C2[Systems Manager]
    C --> C3[EventBridge Rules]
    
    D --> D1[Security Reviews]
    D --> D2[Penetration Testing]
    D --> D3[Compliance Audits]
```

## 10. 실제 사용 사례

### 사례 1: 데이터 유출 탐지 및 대응
```mermaid
sequenceDiagram
    participant User as Malicious User
    participant S3 as Amazon S3
    participant CT as CloudTrail
    participant GD as GuardDuty
    participant SH as Security Hub
    participant SOC as Security Team
    
    User->>S3: Unusual data download
    S3->>CT: Log API calls
    CT->>GD: Analyze patterns
    GD->>GD: Detect anomaly
    GD->>SH: Generate finding
    SH->>SOC: Alert security team
    SOC->>S3: Block suspicious access
    SOC->>User: Investigate user account
```

### 사례 2: 컴플라이언스 자동화
```mermaid
graph LR
    A[New Resource] --> B[Config Rule]
    B --> C[Compliance Check]
    C --> D{Compliant?}
    
    D -->|Yes| E[Continue]
    D -->|No| F[Remediation]
    
    F --> F1[Auto-fix]
    F --> F2[Notification]
    F --> F3[Quarantine]
    
    F1 --> G[Re-check]
    F2 --> H[Manual Review]
    F3 --> I[Isolate Resource]
```

## 요약

AWS CloudTrail과 보안 서비스들은 클라우드 환경에서 포괄적인 보안 전략을 구현하는 데 필수적입니다:

1. **CloudTrail**: 모든 API 활동을 기록하여 감사 및 컴플라이언스 지원
2. **GuardDuty**: 지능형 위협 탐지로 실시간 보안 모니터링
3. **Security Hub**: 중앙 집중식 보안 관리 및 컴플라이언스 대시보드
4. **KMS**: 강력한 암호화 키 관리로 데이터 보호
5. **WAF/Shield**: 웹 애플리케이션 및 DDoS 공격 방어
6. **Config**: 리소스 구성 모니터링 및 컴플라이언스 확인

이러한 서비스들을 조합하여 사용하면 클라우드 환경에서 강력하고 포괄적인 보안 체계를 구축할 수 있습니다.

## 다음 학습 예고
내일은 **비용 최적화 및 관리**에 대해 학습합니다. AWS Cost Explorer, 예산 관리, 비용 최적화 전략 등을 다룰 예정입니다.