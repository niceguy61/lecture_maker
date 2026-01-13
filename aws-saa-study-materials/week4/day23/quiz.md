# Day 23 퀴즈: CloudTrail & AWS 보안 서비스

## 퀴즈 개요
- **주제**: AWS CloudTrail 및 보안 서비스
- **문제 수**: 5문제
- **시간 제한**: 10분
- **합격 점수**: 80% (4문제 이상 정답)

---

## 문제 1: CloudTrail 기본 개념
**난이도**: ⭐⭐☆☆☆

AWS CloudTrail의 주요 목적은 무엇입니까?

A) EC2 인스턴스의 성능 모니터링  
B) AWS API 호출 및 계정 활동 로깅  
C) 네트워크 트래픽 분석  
D) 애플리케이션 로그 수집  

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B) AWS API 호출 및 계정 활동 로깅**

**해설:**
AWS CloudTrail은 AWS 계정의 거버넌스, 컴플라이언스, 운영 감사, 위험 감사를 지원하는 서비스입니다. 주요 목적은 다음과 같습니다:

- **API 호출 로깅**: 모든 AWS API 호출을 기록
- **계정 활동 추적**: 사용자, 역할, AWS 서비스의 활동 모니터링
- **보안 분석**: 비정상적인 활동 패턴 탐지
- **컴플라이언스**: 감사 로그 제공 및 규정 준수 지원

다른 선택지들:
- A) EC2 성능 모니터링은 CloudWatch의 역할
- C) 네트워크 트래픽 분석은 VPC Flow Logs의 역할
- D) 애플리케이션 로그 수집은 CloudWatch Logs의 역할

**관련 개념**: CloudTrail 이벤트 유형, 관리 이벤트, 데이터 이벤트
</details>

---

## 문제 2: GuardDuty 위협 탐지
**난이도**: ⭐⭐⭐☆☆

다음 중 AWS GuardDuty가 탐지할 수 있는 보안 위협이 **아닌** 것은?

A) 암호화폐 채굴 활동  
B) 악성 IP 주소와의 통신  
C) 애플리케이션 코드의 취약점  
D) 비정상적인 API 호출 패턴  

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: C) 애플리케이션 코드의 취약점**

**해설:**
AWS GuardDuty는 머신러닝을 사용한 지능형 위협 탐지 서비스로, 다음과 같은 위협들을 탐지할 수 있습니다:

**GuardDuty가 탐지하는 위협들:**
- **암호화폐 채굴**: 비정상적인 네트워크 활동 패턴으로 탐지
- **악성 IP 통신**: 알려진 악성 IP 주소와의 통신 탐지
- **비정상적인 API 호출**: CloudTrail 로그 분석을 통한 이상 행동 탐지
- **데이터 유출 시도**: 대량 데이터 전송 패턴 탐지
- **권한 상승 공격**: 비정상적인 권한 사용 패턴 탐지

**GuardDuty가 탐지하지 않는 것:**
- **애플리케이션 코드 취약점**: 이는 Amazon Inspector나 정적 코드 분석 도구의 영역
- **애플리케이션 레벨 보안 이슈**: WAF나 애플리케이션 보안 도구 필요

**관련 개념**: GuardDuty 데이터 소스, 위협 인텔리전스, 머신러닝 기반 탐지
</details>

---

## 문제 3: Security Hub 통합
**난이도**: ⭐⭐⭐☆☆

회사에서 AWS Security Hub를 사용하여 중앙 집중식 보안 관리를 구현하려고 합니다. Security Hub와 자동으로 통합되는 AWS 서비스는 무엇입니까?

A) CloudTrail, GuardDuty, Config  
B) CloudWatch, Lambda, SNS  
C) EC2, S3, RDS  
D) VPC, IAM, KMS  

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: A) CloudTrail, GuardDuty, Config**

**해설:**
AWS Security Hub는 여러 AWS 보안 서비스의 결과를 중앙에서 통합 관리하는 서비스입니다.

**Security Hub와 자동 통합되는 주요 서비스들:**
- **AWS GuardDuty**: 위협 탐지 결과를 Security Hub로 전송
- **AWS Config**: 리소스 구성 규정 준수 결과 통합
- **Amazon Inspector**: 취약점 평가 결과 통합
- **Amazon Macie**: 데이터 보안 및 프라이버시 결과 통합
- **AWS Systems Manager Patch Manager**: 패치 컴플라이언스 상태
- **AWS Firewall Manager**: 방화벽 정책 준수 상태

**Security Hub의 주요 기능:**
- **보안 표준 준수 모니터링**: AWS Foundational, CIS Benchmarks, PCI DSS
- **중앙 집중식 대시보드**: 모든 보안 결과를 한 곳에서 확인
- **자동화된 대응**: EventBridge와 연동하여 자동 대응 가능
- **우선순위 지정**: 심각도에 따른 결과 분류

다른 선택지들은 보안 서비스가 아니거나 Security Hub와 직접 통합되지 않습니다.

**관련 개념**: Security Hub 표준, 보안 결과 통합, 컴플라이언스 모니터링
</details>

---

## 문제 4: KMS 암호화 시나리오
**난이도**: ⭐⭐⭐⭐☆

한 회사에서 S3 버킷에 저장된 민감한 데이터를 암호화하려고 합니다. 다음 중 AWS KMS를 사용한 S3 서버 측 암호화에 대한 설명으로 **올바른** 것은?

A) 모든 S3 객체는 동일한 데이터 키로 암호화됩니다  
B) 각 S3 객체는 고유한 데이터 키로 암호화되며, 이 데이터 키는 CMK로 암호화됩니다  
C) S3 객체는 CMK로 직접 암호화됩니다  
D) KMS는 S3 암호화에 사용할 수 없습니다  

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B) 각 S3 객체는 고유한 데이터 키로 암호화되며, 이 데이터 키는 CMK로 암호화됩니다**

**해설:**
AWS KMS는 **Envelope Encryption** 방식을 사용하여 S3 객체를 암호화합니다.

**Envelope Encryption 프로세스:**

1. **데이터 키 생성**: 각 S3 객체마다 고유한 데이터 키 생성
2. **객체 암호화**: 생성된 데이터 키로 S3 객체 암호화
3. **데이터 키 암호화**: CMK(Customer Master Key)로 데이터 키 암호화
4. **저장**: 암호화된 객체와 암호화된 데이터 키를 함께 저장

**장점:**
- **성능**: 대용량 데이터를 빠르게 암호화 (대칭키 사용)
- **보안**: 각 객체마다 다른 키 사용으로 보안 강화
- **확장성**: CMK 하나로 무제한 데이터 암호화 가능

**다른 선택지 분석:**
- A) 틀림: 각 객체마다 고유한 데이터 키 사용
- C) 틀림: CMK는 데이터 키를 암호화하는 데 사용, 직접 데이터 암호화 안 함
- D) 틀림: KMS는 S3의 주요 암호화 옵션 중 하나

**관련 개념**: Envelope Encryption, CMK, 데이터 키, S3 서버 측 암호화
</details>

---

## 문제 5: 보안 자동화 시나리오
**난이도**: ⭐⭐⭐⭐☆

다음 시나리오를 읽고 가장 적절한 자동화 솔루션을 선택하세요.

**시나리오**: 
회사에서 GuardDuty가 높은 심각도의 보안 위협을 탐지했을 때, 자동으로 다음 작업을 수행하고 싶습니다:
1. 보안팀에 즉시 알림 전송
2. 의심스러운 EC2 인스턴스를 네트워크에서 격리
3. 사고 대응 티켓 자동 생성

이를 구현하기 위한 가장 적절한 AWS 서비스 조합은?

A) CloudWatch Alarms + SNS + Lambda  
B) EventBridge + Lambda + SNS + Systems Manager  
C) Config Rules + CloudFormation + SQS  
D) Step Functions + API Gateway + DynamoDB  

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B) EventBridge + Lambda + SNS + Systems Manager**

**해설:**
이 시나리오는 GuardDuty 이벤트를 트리거로 한 자동화된 보안 대응을 구현하는 것입니다.

**최적의 아키텍처:**

```
GuardDuty Finding → EventBridge → Lambda → [SNS + Systems Manager + Ticket API]
```

**각 서비스의 역할:**

1. **EventBridge (Amazon EventBridge)**:
   - GuardDuty findings를 실시간으로 수신
   - 이벤트 패턴 매칭으로 높은 심각도 이벤트만 필터링
   - Lambda 함수를 트리거

2. **Lambda**:
   - 중앙 오케스트레이션 역할
   - GuardDuty finding 분석 및 대응 로직 실행
   - 여러 서비스 호출 조정

3. **SNS (Simple Notification Service)**:
   - 보안팀에 즉시 알림 전송 (이메일, SMS, Slack 등)
   - 다중 채널 알림 지원

4. **Systems Manager**:
   - EC2 인스턴스 격리 작업 수행
   - 보안 그룹 변경, 인스턴스 중지 등
   - 안전한 원격 명령 실행

**구현 예시:**
```python
# Lambda 함수 예시
def lambda_handler(event, context):
    finding = event['detail']
    severity = finding['severity']
    
    if severity >= 7.0:  # High severity
        # 1. 알림 전송
        send_alert_to_security_team(finding)
        
        # 2. 인스턴스 격리
        if 'instanceId' in finding:
            isolate_instance(finding['instanceId'])
        
        # 3. 티켓 생성
        create_incident_ticket(finding)
```

**다른 선택지 분석:**
- A) CloudWatch Alarms는 GuardDuty 이벤트를 직접 처리하기 어려움
- C) Config Rules는 리소스 구성 변경에 대한 것으로 부적절
- D) 과도하게 복잡한 구성으로 이 시나리오에 부적합

**관련 개념**: 이벤트 기반 아키텍처, 보안 자동화, 사고 대응 자동화
</details>

---

## 퀴즈 완료

### 점수 계산
- 5문제 중 맞힌 개수: ___/5
- 백분율 점수: ___% 

### 평가 기준
- **90-100%**: 우수 - CloudTrail과 보안 서비스에 대한 깊은 이해
- **80-89%**: 양호 - 핵심 개념을 잘 이해하고 있음
- **70-79%**: 보통 - 기본 개념은 이해했으나 복습 필요
- **60-69%**: 미흡 - 추가 학습과 실습 필요
- **60% 미만**: 부족 - 이론 내용 재학습 권장

### 오답 노트
틀린 문제가 있다면 해당 문제의 해설을 다시 읽고, 관련 개념을 복습하세요.

**복습이 필요한 주제들:**
- [ ] CloudTrail 기본 개념 및 이벤트 유형
- [ ] GuardDuty 위협 탐지 메커니즘
- [ ] Security Hub 서비스 통합
- [ ] KMS Envelope Encryption
- [ ] 보안 자동화 아키텍처

### 추가 학습 자료
- [AWS CloudTrail 사용 설명서](https://docs.aws.amazon.com/cloudtrail/)
- [Amazon GuardDuty 사용 설명서](https://docs.aws.amazon.com/guardduty/)
- [AWS Security Hub 사용 설명서](https://docs.aws.amazon.com/securityhub/)
- [AWS KMS 개발자 안내서](https://docs.aws.amazon.com/kms/)

---

**다음 학습**: 내일은 **비용 최적화 및 관리**에 대해 학습합니다. Cost Explorer, 예산 관리, 비용 최적화 전략 등을 다룰 예정입니다.