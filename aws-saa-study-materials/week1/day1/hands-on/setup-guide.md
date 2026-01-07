# Day 1 실습 가이드: AWS 계정 설정

## 실습 개요

이 실습에서는 AWS 계정을 설정하고 기본적인 구성을 확인하는 방법을 학습합니다. Python 스크립트를 사용하여 계정 정보, 리전, 가용 영역 등을 확인하고 보안 권장사항을 검토합니다.

## 사전 준비사항

### 1. AWS 계정 생성
1. [AWS 공식 웹사이트](https://aws.amazon.com)에 접속
2. "AWS 계정 생성" 클릭
3. 이메일 주소, 비밀번호, 계정 이름 입력
4. 연락처 정보 및 결제 정보 입력
5. 전화번호 인증 완료
6. 지원 플랜 선택 (기본 플랜 선택 권장)

### 2. AWS CLI 설치

#### Windows
```bash
# Chocolatey 사용 (권장)
choco install awscli

# 또는 MSI 인스톨러 다운로드
# https://awscli.amazonaws.com/AWSCLIV2.msi
```

#### macOS
```bash
# Homebrew 사용 (권장)
brew install awscli

# 또는 pkg 인스톨러 다운로드
# https://awscli.amazonaws.com/AWSCLIV2.pkg
```

#### Linux (Ubuntu/Debian)
```bash
# apt 패키지 매니저 사용
sudo apt update
sudo apt install awscli

# 또는 pip 사용
pip3 install awscli
```

### 3. Python 환경 설정

#### Python 3.7+ 설치 확인
```bash
python3 --version
# 또는
python --version
```

#### 가상 환경 생성 (권장)
```bash
# 가상 환경 생성
python3 -m venv aws-study-env

# 가상 환경 활성화
# Windows
aws-study-env\Scripts\activate

# macOS/Linux
source aws-study-env/bin/activate
```

## AWS 자격 증명 설정

### 방법 1: AWS CLI 구성 (권장)

1. **IAM 사용자 생성** (루트 계정 사용 지양)
   - AWS 콘솔 → IAM → 사용자 → 사용자 추가
   - 프로그래밍 방식 액세스 선택
   - 적절한 권한 정책 연결 (예: PowerUserAccess)
   - 액세스 키 ID와 비밀 액세스 키 저장

2. **AWS CLI 구성**
```bash
aws configure
```

입력 정보:
- AWS Access Key ID: [IAM 사용자의 액세스 키]
- AWS Secret Access Key: [IAM 사용자의 비밀 키]
- Default region name: ap-northeast-2 (서울 리전)
- Default output format: json

### 방법 2: 환경 변수 설정

```bash
# Windows (PowerShell)
$env:AWS_ACCESS_KEY_ID="your-access-key"
$env:AWS_SECRET_ACCESS_KEY="your-secret-key"
$env:AWS_DEFAULT_REGION="ap-northeast-2"

# macOS/Linux (Bash)
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="ap-northeast-2"
```

## 실습 실행

### 1. 의존성 설치

```bash
# 프로젝트 디렉토리로 이동
cd aws-saa-study-materials/week1/day1/hands-on

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 2. 실습 스크립트 실행

```bash
# 기본 실행
python aws-account-setup.py

# 또는 실행 권한 부여 후 직접 실행 (Linux/macOS)
chmod +x aws-account-setup.py
./aws-account-setup.py
```

### 3. 실행 결과 확인

스크립트 실행 시 다음과 같은 정보들이 출력됩니다:

1. **AWS 계정 정보**
   - 계정 ID
   - 사용자 ARN
   - 현재 리전

2. **사용 가능한 리전 목록**
   - 전 세계 AWS 리전 정보
   - 각 리전의 엔드포인트

3. **가용 영역 정보**
   - 현재 리전의 AZ 목록
   - 각 AZ의 상태 및 ID

4. **IAM 사용자 상태**
   - 현재 사용자 정보
   - 연결된 정책 및 그룹

5. **결제 정보** (권한이 있는 경우)
   - 최근 30일 비용 정보

6. **보안 권장사항**
   - AWS 보안 모범 사례

7. **설정 보고서**
   - JSON 형태의 상세 보고서 파일 생성

## 예상 출력 예시

```
AWS SAA-C03 Study Materials
Day 1 Hands-on Lab: AWS Account Setup
==================================================
✅ AWS 클라이언트 초기화 완료

==================================================
1. AWS 계정 정보 확인
==================================================
📋 계정 ID: 123456789012
👤 사용자 ARN: arn:aws:iam::123456789012:user/study-user
🆔 사용자 ID: AIDACKCEVSQ6C2EXAMPLE
🌍 현재 리전: ap-northeast-2

==================================================
2. 사용 가능한 AWS 리전 확인
==================================================
📍 총 33개 리전 사용 가능:
  • us-east-1: ec2.us-east-1.amazonaws.com
  • us-east-2: ec2.us-east-2.amazonaws.com
  • ap-northeast-2: ec2.ap-northeast-2.amazonaws.com
  ...

==================================================
3. 현재 리전의 가용 영역 확인
==================================================
🏢 ap-northeast-2 리전의 가용 영역:
  ✅ ap-northeast-2a (ID: apne2-az1, Type: availability-zone)
  ✅ ap-northeast-2b (ID: apne2-az2, Type: availability-zone)
  ✅ ap-northeast-2c (ID: apne2-az3, Type: availability-zone)
  ✅ ap-northeast-2d (ID: apne2-az4, Type: availability-zone)
```

## 문제 해결

### 자주 발생하는 오류

1. **NoCredentialsError**
   ```
   ❌ AWS 자격 증명이 설정되지 않았습니다.
   ```
   - 해결: AWS CLI 구성 또는 환경 변수 설정 확인

2. **AccessDenied**
   ```
   ❌ 권한이 없습니다.
   ```
   - 해결: IAM 사용자에게 적절한 권한 정책 연결

3. **RegionNotFound**
   ```
   ❌ 리전을 찾을 수 없습니다.
   ```
   - 해결: 올바른 리전 코드 사용 (예: ap-northeast-2)

### 권한 설정 가이드

실습을 위한 최소 권한 정책:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:GetCallerIdentity",
                "ec2:DescribeRegions",
                "ec2:DescribeAvailabilityZones",
                "iam:GetUser",
                "iam:ListAttachedUserPolicies",
                "iam:ListUserPolicies",
                "iam:GetGroupsForUser"
            ],
            "Resource": "*"
        }
    ]
}
```

## 실습 완료 후 확인사항

- [ ] AWS 계정 정보가 올바르게 출력되었는가?
- [ ] 현재 리전의 가용 영역이 표시되었는가?
- [ ] IAM 사용자 정보가 확인되었는가?
- [ ] 보안 권장사항을 검토했는가?
- [ ] 설정 보고서 파일이 생성되었는가?

## 다음 단계

1. **MFA 설정**: IAM 사용자에 다중 인증 활성화
2. **결제 알림 설정**: 예상치 못한 비용 방지
3. **CloudTrail 활성화**: API 호출 로깅
4. **Day 2 학습 준비**: IAM 심화 학습

## 추가 리소스

- [AWS 계정 설정 가이드](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)
- [AWS CLI 구성 가이드](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [IAM 모범 사례](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS 프리 티어](https://aws.amazon.com/free/)