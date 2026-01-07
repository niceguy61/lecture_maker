# Day 3 실습 가이드: EC2 관리

## 실습 개요

이 실습에서는 Python과 boto3를 사용하여 EC2 인스턴스를 생성, 관리, 모니터링하는 방법을 학습합니다.

## 학습 목표

- EC2 인스턴스 생성 및 설정
- 보안 그룹과 키 페어 관리
- 인스턴스 생명주기 관리
- CloudWatch를 통한 모니터링
- Python boto3 라이브러리 활용

## 사전 준비사항

### 1. AWS 계정 및 자격 증명 설정

#### AWS CLI 설치 및 설정
```bash
# AWS CLI 설치 (이미 설치되어 있다면 생략)
pip install awscli

# AWS 자격 증명 설정
aws configure
```

설정 시 입력할 정보:
- **AWS Access Key ID**: IAM 사용자의 액세스 키
- **AWS Secret Access Key**: IAM 사용자의 시크릿 키
- **Default region name**: `us-east-1` (또는 선호하는 리전)
- **Default output format**: `json`

#### 필요한 IAM 권한

실습을 위해 다음 권한이 필요합니다:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:*",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:ListMetrics"
            ],
            "Resource": "*"
        }
    ]
}
```

### 2. Python 환경 설정

#### Python 가상환경 생성 (권장)
```bash
# 가상환경 생성
python -m venv ec2-lab-env

# 가상환경 활성화
# Windows:
ec2-lab-env\Scripts\activate
# macOS/Linux:
source ec2-lab-env/bin/activate
```

#### 필요한 패키지 설치
```bash
# requirements.txt를 사용한 설치
pip install -r requirements.txt

# 또는 개별 설치
pip install boto3 colorama python-dotenv tabulate
```

### 3. 환경 변수 설정 (선택사항)

`.env` 파일을 생성하여 환경 변수를 설정할 수 있습니다:

```bash
# .env 파일 생성
cat > .env << EOF
AWS_DEFAULT_REGION=us-east-1
AWS_PROFILE=default
LAB_KEY_NAME=day3-lab-key
LAB_SECURITY_GROUP=day3-web-server-sg
EOF
```

## 실습 단계

### 1단계: 환경 확인

실습 스크립트를 실행하기 전에 AWS 연결을 확인합니다:

```bash
# AWS 자격 증명 확인
aws sts get-caller-identity

# EC2 서비스 접근 확인
aws ec2 describe-regions --region us-east-1
```

### 2단계: 실습 스크립트 실행

```bash
# 실습 스크립트 실행
python ec2-management.py
```

### 3단계: 실습 진행

스크립트가 실행되면 다음 단계가 자동으로 진행됩니다:

1. **키 페어 생성**: SSH 접속용 키 페어 생성
2. **보안 그룹 생성**: 웹 서버용 보안 그룹 및 규칙 설정
3. **AMI 조회**: 최신 Amazon Linux AMI 검색
4. **인스턴스 시작**: t3.micro 인스턴스 생성 및 웹 서버 설치
5. **상태 확인**: 인스턴스 시작 완료 대기
6. **관리 메뉴**: 대화형 인스턴스 관리

### 4단계: 웹 서버 접속 확인

인스턴스가 시작되면 다음과 같이 접속할 수 있습니다:

#### 웹 브라우저 접속
```
http://[퍼블릭-IP-주소]
```

#### SSH 접속
```bash
# 키 파일 권한 설정 (Linux/Mac)
chmod 400 day3-lab-key.pem

# SSH 접속
ssh -i day3-lab-key.pem ec2-user@[퍼블릭-IP-주소]
```

## 실습 내용 상세 설명

### 1. 키 페어 관리

```python
# 키 페어 생성
key_info = ec2_manager.create_key_pair("my-key")

# 생성된 개인 키는 자동으로 .pem 파일로 저장됩니다
# 파일 권한도 자동으로 400으로 설정됩니다
```

**주요 학습 포인트:**
- 키 페어는 EC2 인스턴스에 안전하게 접속하기 위한 암호화 키
- 개인 키(.pem 파일)는 안전하게 보관해야 함
- 키를 분실하면 인스턴스에 접속할 수 없음

### 2. 보안 그룹 설정

```python
# 웹 서버용 보안 그룹 규칙
rules = [
    {
        'IpProtocol': 'tcp',
        'FromPort': 80,
        'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # HTTP 접속 허용
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 443,
        'ToPort': 443,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # HTTPS 접속 허용
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # SSH 접속 허용 (주의!)
    }
]
```

**보안 주의사항:**
- SSH 포트(22)는 특정 IP에서만 접속하도록 제한하는 것이 좋습니다
- 실제 운영 환경에서는 `0.0.0.0/0` 대신 관리자 IP만 허용

### 3. 사용자 데이터 스크립트

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# 웹 페이지 생성
echo "<h1>Hello from EC2!</h1>" > /var/www/html/index.html
```

**주요 학습 포인트:**
- 사용자 데이터는 인스턴스 시작 시 자동으로 실행되는 스크립트
- 소프트웨어 설치, 설정, 서비스 시작 등을 자동화할 수 있음
- 인스턴스 메타데이터를 활용하여 동적 정보 표시 가능

### 4. 인스턴스 모니터링

```python
# CPU 사용률 조회
metrics = ec2_manager.get_instance_metrics(instance_id, 'CPUUtilization')

# 네트워크 I/O 조회
network_in = ec2_manager.get_instance_metrics(instance_id, 'NetworkIn')
network_out = ec2_manager.get_instance_metrics(instance_id, 'NetworkOut')
```

**사용 가능한 메트릭:**
- `CPUUtilization`: CPU 사용률
- `NetworkIn`: 네트워크 입력 바이트
- `NetworkOut`: 네트워크 출력 바이트
- `DiskReadOps`: 디스크 읽기 작업 수
- `DiskWriteOps`: 디스크 쓰기 작업 수

## 문제 해결

### 일반적인 오류와 해결 방법

#### 1. 자격 증명 오류
```
NoCredentialsError: Unable to locate credentials
```

**해결 방법:**
```bash
# AWS CLI 재설정
aws configure

# 또는 환경 변수 설정
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

#### 2. 권한 부족 오류
```
AccessDenied: User is not authorized to perform: ec2:RunInstances
```

**해결 방법:**
- IAM 사용자에게 필요한 EC2 권한 부여
- 관리자에게 권한 요청

#### 3. 인스턴스 시작 실패
```
InvalidAMIID.NotFound: The image id '[ami-xxxxx]' does not exist
```

**해결 방법:**
- 다른 리전의 AMI ID를 사용했을 가능성
- 스크립트에서 자동으로 최신 AMI를 조회하므로 일반적으로 발생하지 않음

#### 4. 보안 그룹 중복 오류
```
InvalidGroup.Duplicate: The security group 'day3-web-server-sg' already exists
```

**해결 방법:**
- 기존 보안 그룹을 삭제하거나 다른 이름 사용
- 스크립트에서 자동으로 처리됨

### 디버깅 팁

#### 1. 상세 로깅 활성화
```python
import logging
boto3.set_stream_logger('boto3', logging.DEBUG)
```

#### 2. 인스턴스 로그 확인
```bash
# 시스템 로그 확인 (AWS 콘솔에서)
# 또는 SSH 접속 후
sudo tail -f /var/log/cloud-init-output.log
```

#### 3. 메타데이터 서비스 확인
```bash
# 인스턴스 내부에서 실행
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/user-data/
```

## 실습 후 정리

### 리소스 정리 (중요!)

실습 완료 후 비용 발생을 방지하기 위해 다음 리소스를 정리하세요:

1. **인스턴스 종료**
   ```bash
   # 스크립트 메뉴에서 '7. 인스턴스 종료' 선택
   # 또는 AWS CLI 사용
   aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
   ```

2. **보안 그룹 삭제** (선택사항)
   ```bash
   aws ec2 delete-security-group --group-name day3-web-server-sg
   ```

3. **키 페어 삭제** (선택사항)
   ```bash
   aws ec2 delete-key-pair --key-name day3-lab-key
   rm day3-lab-key.pem
   ```

### 비용 확인

- AWS 콘솔의 Billing Dashboard에서 현재 사용량 확인
- t3.micro 인스턴스는 프리 티어에 포함되어 월 750시간까지 무료
- 프리 티어를 초과하면 시간당 약 $0.0104 과금

## 추가 학습 자료

### AWS 공식 문서
- [EC2 사용자 가이드](https://docs.aws.amazon.com/ec2/latest/userguide/)
- [boto3 EC2 문서](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)

### 실습 확장 아이디어
1. **로드 밸런서 추가**: 여러 인스턴스에 트래픽 분산
2. **Auto Scaling 설정**: 트래픽에 따른 자동 확장/축소
3. **CloudWatch 알람**: CPU 사용률 기반 알림 설정
4. **EBS 볼륨 관리**: 추가 스토리지 연결 및 관리
5. **Elastic IP 할당**: 고정 IP 주소 사용

## 마무리

이 실습을 통해 다음을 학습했습니다:

✅ EC2 인스턴스 생성 및 설정  
✅ 보안 그룹과 키 페어 관리  
✅ 사용자 데이터를 통한 자동화  
✅ 인스턴스 생명주기 관리  
✅ CloudWatch 모니터링  
✅ Python boto3 라이브러리 활용  

다음 실습(Day 4)에서는 EC2의 고급 기능과 스토리지 옵션에 대해 더 자세히 알아보겠습니다!

---

**💡 팁**: 실습 중 문제가 발생하면 AWS 콘솔에서도 동일한 작업을 수행해보며 비교 학습하세요. 이를 통해 CLI/SDK와 콘솔 간의 차이점을 이해할 수 있습니다.