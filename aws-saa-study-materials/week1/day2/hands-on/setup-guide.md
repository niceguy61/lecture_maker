# Day 2 IAM 실습 환경 설정 가이드

## 개요
이 가이드는 AWS IAM (Identity and Access Management) 실습을 위한 환경 설정 방법을 안내합니다.

## 사전 준비사항

### 1. AWS 계정 및 자격 증명
- AWS 계정이 있어야 합니다 (Free Tier 사용 가능)
- AWS CLI가 설치되어 있어야 합니다
- 적절한 IAM 권한이 있는 사용자 자격 증명이 필요합니다

### 2. 필요한 IAM 권한
실습을 위해 다음 권한이 필요합니다:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateUser",
                "iam:CreateGroup",
                "iam:CreateRole",
                "iam:CreatePolicy",
                "iam:AttachUserPolicy",
                "iam:AttachGroupPolicy",
                "iam:AttachRolePolicy",
                "iam:AddUserToGroup",
                "iam:ListUsers",
                "iam:ListGroups",
                "iam:ListRoles",
                "iam:ListPolicies",
                "iam:DeleteUser",
                "iam:DeleteGroup",
                "iam:DeleteRole",
                "iam:DeletePolicy",
                "iam:DetachUserPolicy",
                "iam:DetachGroupPolicy",
                "iam:DetachRolePolicy",
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

## 환경 설정 단계

### 1. Python 환경 준비

#### Python 가상환경 생성 (권장)
```bash
# 가상환경 생성
python -m venv iam-lab-env

# 가상환경 활성화
# Windows
iam-lab-env\Scripts\activate
# macOS/Linux
source iam-lab-env/bin/activate
```

#### 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. AWS 자격 증명 설정

#### 방법 1: AWS CLI 설정 (권장)
```bash
aws configure
```
다음 정보를 입력합니다:
- AWS Access Key ID: [여러분의 액세스 키]
- AWS Secret Access Key: [여러분의 시크릿 키]
- Default region name: us-east-1
- Default output format: json

#### 방법 2: 환경 변수 설정
```bash
# Windows (Command Prompt)
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_DEFAULT_REGION=us-east-1

# Windows (PowerShell)
$env:AWS_ACCESS_KEY_ID="your_access_key"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key"
$env:AWS_DEFAULT_REGION="us-east-1"

# macOS/Linux
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

#### 방법 3: .env 파일 사용
프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

### 3. 자격 증명 확인
```bash
# AWS CLI로 확인
aws sts get-caller-identity

# Python으로 확인
python -c "import boto3; print(boto3.client('sts').get_caller_identity())"
```

## 실습 실행

### 1. 기본 실습 실행
```bash
python iam-management.py
```

### 2. 실습 내용
실습 스크립트는 다음 작업을 수행합니다:

1. **현재 사용자 정보 확인**
   - 현재 AWS 계정 및 사용자 정보 출력

2. **IAM 사용자 생성**
   - `study-developer`: 개발자용 사용자
   - `study-admin`: 관리자용 사용자

3. **IAM 그룹 생성**
   - `StudyDevelopers`: 개발자 그룹
   - `StudyAdmins`: 관리자 그룹

4. **IAM 정책 생성**
   - S3 읽기 전용 정책
   - EC2 읽기 전용 정책
   - 개발자용 제한적 권한 정책

5. **IAM 역할 생성**
   - EC2 인스턴스가 사용할 역할

6. **권한 연결**
   - 그룹에 정책 연결
   - 사용자를 그룹에 추가

7. **리소스 정리**
   - 실습 완료 후 생성된 리소스 정리

## 주의사항

### 보안 관련
- **절대로** 루트 계정으로 실습하지 마세요
- 실습용 IAM 사용자를 별도로 생성하여 사용하세요
- 실습 완료 후 반드시 생성된 리소스를 정리하세요
- 액세스 키를 코드에 하드코딩하지 마세요

### 비용 관련
- IAM 자체는 무료 서비스입니다
- 하지만 생성된 리소스가 많아지면 관리가 어려워질 수 있습니다
- 실습 후 정리를 권장합니다

### 권한 관련
- 실습용 사용자에게는 최소한의 권한만 부여하세요
- 실제 운영 환경에서는 더 엄격한 권한 관리가 필요합니다

## 문제 해결

### 자주 발생하는 오류

#### 1. 자격 증명 오류
```
NoCredentialsError: Unable to locate credentials
```
**해결방법**: AWS 자격 증명 설정을 다시 확인하세요.

#### 2. 권한 부족 오류
```
AccessDenied: User is not authorized to perform: iam:CreateUser
```
**해결방법**: IAM 권한을 확인하고 필요한 권한을 추가하세요.

#### 3. 리소스 이미 존재 오류
```
EntityAlreadyExists: User with name study-developer already exists
```
**해결방법**: 기존 리소스를 삭제하거나 다른 이름을 사용하세요.

### 디버깅 팁
1. AWS CloudTrail을 통해 API 호출 로그 확인
2. IAM 정책 시뮬레이터 사용
3. AWS CLI로 동일한 작업 시도해보기

## 추가 학습 자료

### AWS 공식 문서
- [IAM 사용 설명서](https://docs.aws.amazon.com/iam/)
- [IAM 모범 사례](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [IAM 정책 참조](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html)

### 실습 확장 아이디어
1. **MFA 설정**: 사용자에게 다중 인증 설정
2. **교차 계정 역할**: 다른 AWS 계정과의 역할 공유
3. **조건부 정책**: IP 주소나 시간 기반 접근 제어
4. **정책 시뮬레이션**: IAM 정책 시뮬레이터 사용

## 실습 완료 체크리스트

- [ ] Python 환경 설정 완료
- [ ] AWS 자격 증명 설정 완료
- [ ] 실습 스크립트 정상 실행
- [ ] IAM 사용자, 그룹, 역할, 정책 생성 확인
- [ ] 권한 연결 및 작동 확인
- [ ] 실습 리소스 정리 완료
- [ ] 보안 모범 사례 이해
- [ ] 다음 단계 (EC2) 준비

실습을 통해 IAM의 핵심 개념과 실제 사용법을 익혔다면, 내일 EC2 실습에서 IAM 역할이 어떻게 활용되는지 확인해보겠습니다!