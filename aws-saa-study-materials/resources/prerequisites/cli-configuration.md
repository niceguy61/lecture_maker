# AWS CLI 설정 가이드

## 📋 개요

이 가이드는 AWS Command Line Interface (CLI)를 설치하고 설정하는 과정을 안내합니다. AWS CLI를 사용하면 터미널에서 명령어로 AWS 서비스를 관리할 수 있습니다.

> 💡 **참고**: AWS CLI 설정은 **선택사항**입니다. AWS Management Console만으로도 모든 학습을 진행할 수 있습니다. CLI는 자동화, 스크립팅, 빠른 작업 수행에 유용합니다.

## 🎯 학습 목표

- AWS CLI 설치 및 설정
- AWS 자격 증명 구성
- 기본 AWS CLI 명령어 사용법 학습
- AWS CLI 프로파일 관리

## ⏱️ 예상 소요 시간

약 15-20분

## 💰 예상 비용

$0.00 (AWS CLI는 무료 도구)

## 📚 사전 요구사항

- ✅ [AWS 계정 설정](./aws-account-setup.md) 완료
- ✅ [IAM 사용자 설정](./iam-user-setup.md) 완료
- ✅ IAM 사용자 액세스 키 생성 완료

---

## 🔧 AWS CLI란?

### Command Line Interface (CLI)

AWS CLI는 명령줄에서 AWS 서비스를 관리할 수 있는 통합 도구입니다.

### 주요 기능

- **서비스 관리**: EC2, S3, RDS 등 모든 AWS 서비스 제어
- **자동화**: 스크립트를 통한 반복 작업 자동화
- **빠른 작업**: Console보다 빠른 리소스 생성/관리
- **Infrastructure as Code**: CloudFormation, Terraform과 통합

### AWS CLI vs AWS Management Console

| 특징 | AWS CLI | AWS Console |
|------|---------|-------------|
| 인터페이스 | 명령줄 | 웹 브라우저 |
| 학습 곡선 | 높음 | 낮음 |
| 자동화 | 쉬움 | 어려움 |
| 속도 | 빠름 | 느림 |
| 시각화 | 없음 | 있음 |

---

## 1️⃣ AWS CLI 설치

운영체제에 따라 설치 방법이 다릅니다.

### Windows 설치

#### 방법 1: MSI 설치 프로그램 (권장)

1. **AWS CLI 설치 파일 다운로드**
   - [AWS CLI MSI 설치 프로그램 (64비트)](https://awscli.amazonaws.com/AWSCLIV2.msi) 다운로드

2. **설치 프로그램 실행**
   - 다운로드한 `AWSCLIV2.msi` 파일 더블클릭
   - 설치 마법사 지시에 따라 진행
   - **"Next"** > **"Next"** > **"Install"** > **"Finish"**

3. **설치 확인**
   - **명령 프롬프트(CMD)** 또는 **PowerShell** 열기
   - 다음 명령어 실행:
   ```cmd
   aws --version
   ```
   - 출력 예시: `aws-cli/2.15.0 Python/3.11.6 Windows/10 exe/AMD64`

#### 방법 2: PowerShell (관리자 권한 필요)

```powershell
# PowerShell을 관리자 권한으로 실행
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

### macOS 설치

#### 방법 1: PKG 설치 프로그램 (권장)

1. **AWS CLI 설치 파일 다운로드**
   - [AWS CLI PKG 설치 프로그램](https://awscli.amazonaws.com/AWSCLIV2.pkg) 다운로드

2. **설치 프로그램 실행**
   - 다운로드한 `AWSCLIV2.pkg` 파일 더블클릭
   - 설치 마법사 지시에 따라 진행

3. **설치 확인**
   - **터미널** 열기
   - 다음 명령어 실행:
   ```bash
   aws --version
   ```

#### 방법 2: Homebrew

```bash
# Homebrew가 설치되어 있는 경우
brew install awscli
```

### Linux 설치

#### Ubuntu/Debian

```bash
# 1. 필요한 패키지 설치
sudo apt-get update
sudo apt-get install -y unzip curl

# 2. AWS CLI 다운로드
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# 3. 압축 해제
unzip awscliv2.zip

# 4. 설치
sudo ./aws/install

# 5. 설치 확인
aws --version
```

#### Amazon Linux 2 / CentOS / RHEL

```bash
# 1. 필요한 패키지 설치
sudo yum install -y unzip curl

# 2. AWS CLI 다운로드
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# 3. 압축 해제
unzip awscliv2.zip

# 4. 설치
sudo ./aws/install

# 5. 설치 확인
aws --version
```

---

## 2️⃣ AWS CLI 설정

### Step 1: 액세스 키 준비

IAM 사용자 설정 시 생성한 액세스 키 정보를 준비하세요:

- **액세스 키 ID**: `AKIAIOSFODNN7EXAMPLE`
- **비밀 액세스 키**: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

> ⚠️ **주의**: 위 예시는 샘플입니다. 실제 본인의 액세스 키를 사용하세요!

### Step 2: AWS Configure 실행

터미널 또는 명령 프롬프트에서 다음 명령어 실행:

```bash
aws configure
```

### Step 3: 자격 증명 입력

프롬프트에 따라 정보를 입력하세요:

```
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: ap-northeast-2
Default output format [None]: json
```

#### 입력 항목 설명

1. **AWS Access Key ID**
   - IAM 사용자의 액세스 키 ID 입력

2. **AWS Secret Access Key**
   - IAM 사용자의 비밀 액세스 키 입력

3. **Default region name**
   - 기본 리전 설정
   - 권장: `ap-northeast-2` (서울)
   - 다른 리전: `us-east-1` (버지니아), `us-west-2` (오레곤)

4. **Default output format**
   - 출력 형식 선택
   - 옵션: `json` (권장), `yaml`, `text`, `table`

### Step 4: 설정 확인

#### 자격 증명 파일 확인

**Windows**:
```cmd
type %USERPROFILE%\.aws\credentials
```

**macOS/Linux**:
```bash
cat ~/.aws/credentials
```

출력 예시:
```ini
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

#### 설정 파일 확인

**Windows**:
```cmd
type %USERPROFILE%\.aws\config
```

**macOS/Linux**:
```bash
cat ~/.aws/config
```

출력 예시:
```ini
[default]
region = ap-northeast-2
output = json
```

---

## 3️⃣ AWS CLI 테스트

### 기본 명령어 테스트

#### 1. 현재 사용자 확인

```bash
aws sts get-caller-identity
```

출력 예시:
```json
{
    "UserId": "AIDAI23HXS2RU2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/admin-user"
}
```

#### 2. S3 버킷 목록 조회

```bash
aws s3 ls
```

출력 예시 (버킷이 없는 경우 빈 출력):
```
2024-01-15 10:30:45 my-first-bucket
2024-01-16 14:20:30 my-second-bucket
```

#### 3. EC2 인스턴스 목록 조회

```bash
aws ec2 describe-instances
```

#### 4. 리전 목록 조회

```bash
aws ec2 describe-regions --output table
```

---

## 4️⃣ AWS CLI 프로파일 관리

여러 AWS 계정 또는 IAM 사용자를 사용하는 경우 프로파일을 설정할 수 있습니다.

### 새 프로파일 생성

```bash
aws configure --profile work
```

프롬프트에 따라 다른 자격 증명 입력:
```
AWS Access Key ID [None]: AKIAI44QH8DHBEXAMPLE
AWS Secret Access Key [None]: je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: json
```

### 프로파일 사용

#### 명령어에서 프로파일 지정

```bash
aws s3 ls --profile work
```

#### 환경 변수로 프로파일 설정

**Windows (CMD)**:
```cmd
set AWS_PROFILE=work
aws s3 ls
```

**Windows (PowerShell)**:
```powershell
$env:AWS_PROFILE="work"
aws s3 ls
```

**macOS/Linux**:
```bash
export AWS_PROFILE=work
aws s3 ls
```

### 프로파일 목록 확인

**Windows**:
```cmd
type %USERPROFILE%\.aws\credentials
```

**macOS/Linux**:
```bash
cat ~/.aws/credentials
```

출력 예시:
```ini
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[work]
aws_access_key_id = AKIAI44QH8DHBEXAMPLE
aws_secret_access_key = je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY
```

---

## 5️⃣ 유용한 AWS CLI 명령어

### 도움말 보기

```bash
# 전체 도움말
aws help

# 서비스별 도움말
aws s3 help

# 명령어별 도움말
aws s3 ls help
```

### 출력 형식 변경

```bash
# JSON 형식 (기본)
aws ec2 describe-instances --output json

# 테이블 형식
aws ec2 describe-instances --output table

# 텍스트 형식
aws ec2 describe-instances --output text

# YAML 형식
aws ec2 describe-instances --output yaml
```

### 필터링 및 쿼리

```bash
# JMESPath 쿼리 사용
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name]' --output table

# 특정 리전 지정
aws ec2 describe-instances --region us-west-2

# 태그로 필터링
aws ec2 describe-instances --filters "Name=tag:Environment,Values=production"
```

### 자주 사용하는 명령어

#### S3 작업

```bash
# 버킷 생성
aws s3 mb s3://my-bucket-name

# 파일 업로드
aws s3 cp myfile.txt s3://my-bucket-name/

# 파일 다운로드
aws s3 cp s3://my-bucket-name/myfile.txt ./

# 버킷 내용 동기화
aws s3 sync ./local-folder s3://my-bucket-name/
```

#### EC2 작업

```bash
# 인스턴스 목록
aws ec2 describe-instances

# 인스턴스 시작
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# 인스턴스 중지
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
```

#### IAM 작업

```bash
# 사용자 목록
aws iam list-users

# 그룹 목록
aws iam list-groups

# 정책 목록
aws iam list-policies --scope Local
```

---

## 6️⃣ AWS CLI 보안 베스트 프랙티스

### ✅ 해야 할 것

1. **자격 증명 파일 보호**
   - 파일 권한 제한 (읽기 전용)
   - 공유 컴퓨터에서 사용 금지

2. **MFA 사용** (고급)
   - MFA가 필요한 작업에 임시 자격 증명 사용
   ```bash
   aws sts get-session-token --serial-number arn:aws:iam::123456789012:mfa/admin-user --token-code 123456
   ```

3. **최소 권한 원칙**
   - 필요한 권한만 가진 IAM 사용자 사용
   - AdministratorAccess는 학습 목적으로만 사용

4. **정기적인 액세스 키 로테이션**
   - 90일마다 액세스 키 교체
   - 이전 키는 비활성화 후 삭제

### ❌ 하지 말아야 할 것

1. **자격 증명을 코드에 하드코딩**
   - 환경 변수 또는 자격 증명 파일 사용

2. **공개 저장소에 자격 증명 업로드**
   - `.gitignore`에 `.aws/` 폴더 추가

3. **루트 계정 액세스 키 사용**
   - 루트 계정은 액세스 키 생성 금지

4. **자격 증명 공유**
   - 각 사용자는 자신의 자격 증명 사용

---

## 7️⃣ 문제 해결

### "aws: command not found" 오류

**원인**: AWS CLI가 설치되지 않았거나 PATH에 없음

**해결**:
1. AWS CLI 재설치
2. 터미널 재시작
3. PATH 환경 변수 확인

### "Unable to locate credentials" 오류

**원인**: 자격 증명이 설정되지 않음

**해결**:
```bash
aws configure
```

### "An error occurred (UnauthorizedOperation)" 오류

**원인**: IAM 권한 부족

**해결**:
1. IAM 사용자 권한 확인
2. 필요한 정책 연결
3. 자격 증명이 올바른지 확인

### "An error occurred (InvalidClientTokenId)" 오류

**원인**: 액세스 키가 유효하지 않음

**해결**:
1. 액세스 키 ID 확인
2. 비밀 액세스 키 확인
3. 필요시 새 액세스 키 생성

---

## ✅ 완료 체크리스트

설정이 완료되었는지 확인하세요:

- [ ] AWS CLI 설치 완료
- [ ] `aws --version` 명령어 실행 성공
- [ ] `aws configure` 설정 완료
- [ ] 자격 증명 파일 생성 확인
- [ ] `aws sts get-caller-identity` 테스트 성공
- [ ] 기본 AWS CLI 명령어 사용법 이해
- [ ] AWS CLI 보안 베스트 프랙티스 숙지

---

## 🔗 다음 단계

AWS CLI 설정이 완료되었습니다! 이제 다음 단계로 진행하세요:

1. **[Console 탐색 가이드](./console-navigation.md)** - AWS Console 기본 사용법
2. **일별 학습 시작** - Day 1부터 AWS 서비스 학습 시작
3. **CLI 실습** - 각 일별 학습에서 CLI 명령어 연습

---

## 📚 참고 자료

- [AWS CLI 공식 문서](https://docs.aws.amazon.com/cli/latest/userguide/)
- [AWS CLI 명령어 레퍼런스](https://docs.aws.amazon.com/cli/latest/reference/)
- [AWS CLI 설치 가이드](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS CLI 설정 가이드](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [JMESPath 쿼리 튜토리얼](https://jmespath.org/tutorial.html)

---

## 💡 추가 팁

### AWS CLI 자동 완성 설정

#### Bash (Linux/macOS)

```bash
# ~/.bashrc 또는 ~/.bash_profile에 추가
complete -C '/usr/local/bin/aws_completer' aws
```

#### Zsh (macOS)

```bash
# ~/.zshrc에 추가
autoload bashcompinit && bashcompinit
autoload -Uz compinit && compinit
complete -C '/usr/local/bin/aws_completer' aws
```

### AWS CLI 별칭 설정

자주 사용하는 명령어에 별칭 설정:

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
alias awswho='aws sts get-caller-identity'
alias awsregion='aws configure get region'
alias awsprofile='echo $AWS_PROFILE'
```

---

**마지막 업데이트**: 2024년 1월
