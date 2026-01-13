# Day 23 실습: CloudTrail 및 보안 정책 설정

## 실습 개요
이번 실습에서는 AWS CloudTrail을 설정하고 주요 보안 서비스들을 구성해보겠습니다. 실제 보안 모니터링 환경을 구축하여 AWS 계정의 활동을 추적하고 보안 위협을 탐지하는 방법을 학습합니다.

## 실습 목표
- AWS CloudTrail 설정 및 구성
- AWS GuardDuty 활성화 및 설정
- AWS Security Hub 구성
- AWS Config 규칙 설정
- 보안 알림 및 자동화 구성

## 사전 준비사항
- AWS 계정 (Free Tier 사용 가능)
- 관리자 권한 또는 적절한 IAM 권한
- 이전 실습에서 생성한 VPC 및 EC2 인스턴스 (있는 경우)

⚠️ **비용 주의사항**: 
- CloudTrail: 첫 번째 트레일은 무료, 추가 트레일은 유료
- GuardDuty: 30일 무료 체험 후 유료
- Security Hub: 30일 무료 체험 후 유료
- Config: 구성 항목당 요금 부과

## 실습 1: AWS CloudTrail 설정

### 1.1 CloudTrail 콘솔 접근
1. AWS Management Console에 로그인
2. 서비스 검색에서 "CloudTrail" 입력
3. **AWS CloudTrail** 선택

### 1.2 새 트레일 생성
1. **Create trail** 버튼 클릭
2. **Trail name**: `my-security-trail` 입력
3. **Apply trail to all regions**: ✅ 체크 (권장)
4. **Apply trail to all accounts in my organization**: ❌ 체크 해제

### 1.3 S3 버킷 설정
1. **Create new S3 bucket**: ✅ 선택
2. **S3 bucket name**: `cloudtrail-logs-[your-account-id]-[random]` 
   - 예: `cloudtrail-logs-123456789012-abc123`
3. **Log file prefix**: `cloudtrail-logs/` (선택사항)
4. **Encrypt log files**: ✅ 체크
5. **KMS key**: **New** 선택
6. **KMS key alias**: `alias/cloudtrail-key` 입력

### 1.4 CloudWatch Logs 설정 (선택사항)
1. **CloudWatch Logs**: ✅ 체크
2. **Log group name**: `CloudTrail/SecurityLogs`
3. **Role name**: `CloudTrail_CloudWatchLogs_Role` (자동 생성)

### 1.5 이벤트 유형 설정
1. **Management events**: ✅ 체크
   - **Read**: ✅ 체크
   - **Write**: ✅ 체크
2. **Data events**: ❌ 체크 해제 (비용 절약)
3. **Insight events**: ❌ 체크 해제 (비용 절약)

### 1.6 트레일 생성 완료
1. **Next** 클릭
2. 설정 검토 후 **Create trail** 클릭
3. 트레일이 생성되고 로깅이 시작됨을 확인

## 실습 2: AWS GuardDuty 설정

### 2.1 GuardDuty 콘솔 접근
1. 서비스 검색에서 "GuardDuty" 입력
2. **Amazon GuardDuty** 선택

### 2.2 GuardDuty 활성화
1. **Get Started** 버튼 클릭
2. **Enable GuardDuty** 클릭
3. 30일 무료 체험 안내 확인
4. GuardDuty가 활성화되고 대시보드 표시

### 2.3 GuardDuty 설정 확인
1. **Settings** 메뉴 클릭
2. **General** 탭에서 다음 확인:
   - **Finding export options**: CloudWatch Events 활성화 확인
   - **S3 protection**: 활성화 상태 확인
   - **Malware protection**: 필요시 활성화

### 2.4 샘플 Findings 생성 (테스트용)
1. **Settings** → **Sample findings** 클릭
2. **Generate sample findings** 버튼 클릭
3. **Findings** 메뉴로 이동하여 샘플 결과 확인

## 실습 3: AWS Security Hub 설정

### 3.1 Security Hub 콘솔 접근
1. 서비스 검색에서 "Security Hub" 입력
2. **AWS Security Hub** 선택

### 3.2 Security Hub 활성화
1. **Go to Security Hub** 버튼 클릭
2. **Enable Security Hub** 클릭
3. 보안 표준 선택:
   - ✅ **AWS Foundational Security Standard**
   - ✅ **CIS AWS Foundations Benchmark**
   - ❌ **PCI DSS** (필요한 경우만 선택)

### 3.3 통합 설정
1. **Integrations** 메뉴 클릭
2. 다음 서비스들이 자동으로 통합되었는지 확인:
   - Amazon GuardDuty
   - AWS Config
   - Amazon Inspector (있는 경우)

### 3.4 대시보드 확인
1. **Summary** 메뉴에서 보안 점수 확인
2. **Findings** 메뉴에서 보안 결과 검토
3. **Compliance** 메뉴에서 컴플라이언스 상태 확인

## 실습 4: AWS Config 설정

### 4.1 Config 콘솔 접근
1. 서비스 검색에서 "Config" 입력
2. **AWS Config** 선택

### 4.2 Config 설정 (처음 사용하는 경우)
1. **Get started** 버튼 클릭
2. **Settings** 구성:
   - **Resource types to record**: **All resources** 선택
   - **Include global resource types**: ✅ 체크
3. **Delivery channel**:
   - **S3 bucket name**: 새 버킷 생성 또는 기존 버킷 선택
   - **SNS topic**: 선택사항

### 4.3 Config Rules 추가
1. **Rules** 메뉴 클릭
2. **Add rule** 버튼 클릭
3. 다음 규칙들을 추가:

#### 4.3.1 Root Access Key Check
1. **AWS managed rules** 탭
2. 검색: `root-access-key-check`
3. **root-access-key-check** 선택
4. **Next** → **Add rule**

#### 4.3.2 MFA Enabled for Root
1. **Add rule** 클릭
2. 검색: `mfa-enabled-for-iam-console-access`
3. **mfa-enabled-for-iam-console-access** 선택
4. **Next** → **Add rule**

#### 4.3.3 S3 Bucket Public Read Prohibited
1. **Add rule** 클릭
2. 검색: `s3-bucket-public-read-prohibited`
3. **s3-bucket-public-read-prohibited** 선택
4. **Next** → **Add rule**

### 4.4 Config Rules 결과 확인
1. **Rules** 메뉴에서 규칙 상태 확인
2. 각 규칙을 클릭하여 세부 결과 검토
3. 비준수 리소스가 있는 경우 수정 방법 확인

## 실습 5: 보안 알림 설정

### 5.1 SNS 토픽 생성
1. 서비스 검색에서 "SNS" 입력
2. **Simple Notification Service** 선택
3. **Topics** → **Create topic** 클릭
4. **Type**: Standard 선택
5. **Name**: `security-alerts` 입력
6. **Create topic** 클릭

### 5.2 이메일 구독 추가
1. 생성된 토픽 클릭
2. **Create subscription** 버튼 클릭
3. **Protocol**: Email 선택
4. **Endpoint**: 본인 이메일 주소 입력
5. **Create subscription** 클릭
6. 이메일에서 구독 확인

### 5.3 CloudWatch 알람 생성
1. 서비스 검색에서 "CloudWatch" 입력
2. **Amazon CloudWatch** 선택
3. **Alarms** → **Create alarm** 클릭

#### 5.3.1 Root 계정 사용 알람
1. **Select metric** 클릭
2. **CloudTrailMetrics** → **Root Usage** 선택
3. **Metric name**: `RootAccountUsage`
4. **Statistic**: Sum
5. **Period**: 5 minutes
6. **Threshold**: Greater than 0
7. **Actions**: SNS topic `security-alerts` 선택
8. **Alarm name**: `RootAccountUsageAlarm`
9. **Create alarm** 클릭

### 5.4 EventBridge 규칙 생성 (GuardDuty 연동)
1. 서비스 검색에서 "EventBridge" 입력
2. **Amazon EventBridge** 선택
3. **Rules** → **Create rule** 클릭
4. **Name**: `GuardDutyFindings`
5. **Event pattern**:
   - **Service Name**: GuardDuty
   - **Event Type**: GuardDuty Finding
6. **Target**: SNS topic `security-alerts` 선택
7. **Create rule** 클릭

## 실습 6: 보안 테스트 및 검증

### 6.1 CloudTrail 로그 확인
1. CloudTrail 콘솔에서 **Event history** 클릭
2. 최근 활동 로그 확인
3. 특정 이벤트 클릭하여 상세 정보 검토

### 6.2 S3 버킷에서 로그 파일 확인
1. S3 콘솔로 이동
2. CloudTrail 로그 버킷 선택
3. 로그 파일 다운로드하여 내용 확인

### 6.3 GuardDuty Findings 검토
1. GuardDuty 콘솔에서 **Findings** 확인
2. 샘플 findings의 세부 정보 검토
3. 각 finding의 심각도 및 권장 조치 확인

### 6.4 Security Hub 대시보드 검토
1. Security Hub에서 전체 보안 점수 확인
2. 실패한 보안 검사 항목 검토
3. 우선순위가 높은 findings 확인

## 실습 7: 자동화된 보안 대응 (고급)

### 7.1 Lambda 함수 생성 (자동 대응)
1. 서비스 검색에서 "Lambda" 입력
2. **AWS Lambda** 선택
3. **Create function** 클릭
4. **Function name**: `SecurityAutoResponse`
5. **Runtime**: Python 3.9
6. **Create function** 클릭

### 7.2 Lambda 함수 코드 작성
```python
import json
import boto3

def lambda_handler(event, context):
    # GuardDuty finding 처리
    if 'source' in event and event['source'] == 'aws.guardduty':
        finding = event['detail']
        severity = finding['severity']
        
        if severity >= 7.0:  # High severity
            # 자동 대응 로직
            print(f"High severity finding detected: {finding['type']}")
            
            # 예: 의심스러운 인스턴스 격리
            if 'instanceId' in finding['service']['resourceRole']:
                instance_id = finding['service']['resourceRole']['instanceId']
                isolate_instance(instance_id)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Security response executed')
    }

def isolate_instance(instance_id):
    ec2 = boto3.client('ec2')
    
    # 보안 그룹 생성 (모든 트래픽 차단)
    try:
        response = ec2.create_security_group(
            GroupName=f'quarantine-{instance_id}',
            Description='Quarantine security group'
        )
        sg_id = response['GroupId']
        
        # 인스턴스에 격리 보안 그룹 적용
        ec2.modify_instance_attribute(
            InstanceId=instance_id,
            Groups=[sg_id]
        )
        
        print(f"Instance {instance_id} isolated with security group {sg_id}")
    except Exception as e:
        print(f"Error isolating instance: {str(e)}")
```

### 7.3 Lambda 권한 설정
1. **Configuration** → **Permissions** 클릭
2. **Execution role** 클릭
3. IAM 콘솔에서 다음 정책 추가:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateSecurityGroup",
                "ec2:ModifyInstanceAttribute",
                "ec2:DescribeInstances",
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        }
    ]
}
```

### 7.4 EventBridge와 Lambda 연동
1. EventBridge 콘솔로 이동
2. 이전에 생성한 GuardDuty 규칙 편집
3. **Target** 추가: Lambda function `SecurityAutoResponse`
4. 규칙 업데이트

## 실습 8: 보안 대시보드 구성

### 8.1 CloudWatch 대시보드 생성
1. CloudWatch 콘솔에서 **Dashboards** 클릭
2. **Create dashboard** 클릭
3. **Dashboard name**: `Security-Dashboard`

### 8.2 위젯 추가
1. **Add widget** 클릭
2. **Number** 위젯 선택
3. **CloudTrailMetrics** → **ErrorCount** 선택
4. 위젯 제목: "CloudTrail Errors"

### 8.3 GuardDuty 메트릭 추가
1. **Add widget** 클릭
2. **Line** 위젯 선택
3. **GuardDuty** 메트릭 선택
4. Finding 수 및 심각도별 분포 표시

## 검증 및 테스트

### 1. CloudTrail 로깅 확인
- [ ] CloudTrail이 활성화되어 로그를 기록하고 있는가?
- [ ] S3 버킷에 로그 파일이 생성되고 있는가?
- [ ] 로그 파일이 암호화되어 저장되고 있는가?

### 2. GuardDuty 탐지 확인
- [ ] GuardDuty가 활성화되어 있는가?
- [ ] 샘플 findings가 생성되었는가?
- [ ] 각 finding의 세부 정보를 확인할 수 있는가?

### 3. Security Hub 통합 확인
- [ ] Security Hub가 활성화되어 있는가?
- [ ] 다른 보안 서비스들과 통합되어 있는가?
- [ ] 보안 표준 검사가 실행되고 있는가?

### 4. Config 규칙 확인
- [ ] Config가 리소스를 모니터링하고 있는가?
- [ ] 설정한 규칙들이 정상 작동하는가?
- [ ] 비준수 리소스가 식별되고 있는가?

### 5. 알림 시스템 확인
- [ ] SNS 토픽이 생성되고 구독되어 있는가?
- [ ] CloudWatch 알람이 설정되어 있는가?
- [ ] EventBridge 규칙이 작동하는가?

## 문제 해결

### 일반적인 문제들

**1. CloudTrail 로그가 생성되지 않음**
- 트레일이 활성화되어 있는지 확인
- S3 버킷 권한 확인
- KMS 키 권한 확인

**2. GuardDuty findings가 표시되지 않음**
- GuardDuty가 활성화되어 있는지 확인
- 데이터 소스(CloudTrail, DNS logs, VPC Flow Logs)가 활성화되어 있는지 확인
- 실제 위협이 없을 수 있음 (정상 상황)

**3. Security Hub에서 서비스 통합 실패**
- 각 서비스가 같은 리전에서 활성화되어 있는지 확인
- IAM 권한 확인
- 서비스별 활성화 순서 확인

**4. Config 규칙이 작동하지 않음**
- Config가 활성화되어 있는지 확인
- 리소스 기록이 활성화되어 있는지 확인
- 규칙 매개변수가 올바른지 확인

## 정리 및 비용 절약

실습 완료 후 비용을 절약하려면:

1. **GuardDuty 비활성화** (30일 후 과금 시작)
   - GuardDuty 콘솔 → Settings → Suspend GuardDuty

2. **Security Hub 비활성화** (30일 후 과금 시작)
   - Security Hub 콘솔 → Settings → Disable Security Hub

3. **Config 비활성화** (구성 항목당 과금)
   - Config 콘솔 → Settings → Stop recording

4. **CloudTrail 유지** (첫 번째 트레일 무료)
   - 기본 관리 이벤트는 무료로 유지 가능

5. **S3 버킷 정리**
   - 불필요한 로그 파일 삭제
   - 라이프사이클 정책 설정

## 다음 단계

이번 실습을 통해 AWS의 핵심 보안 서비스들을 설정하고 통합하는 방법을 학습했습니다. 다음 단계로는:

1. **고급 보안 자동화** 구현
2. **컴플라이언스 프레임워크** 적용
3. **보안 사고 대응 플레이북** 개발
4. **정기적인 보안 검토** 프로세스 구축

내일은 **비용 최적화 및 관리**에 대해 실습하며, Cost Explorer와 예산 관리 도구들을 활용해보겠습니다.