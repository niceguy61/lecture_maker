# Day 2 실습: IAM 사용자 및 정책 관리

## 실습 개요
이 실습에서는 AWS Console을 통해 IAM의 핵심 기능들을 직접 체험해봅니다. 사용자 생성, 그룹 관리, 정책 연결, 그리고 역할 생성까지 단계별로 진행합니다.

## 실습 목표
- IAM 사용자 생성 및 관리
- IAM 그룹 생성 및 사용자 할당
- 정책 생성 및 연결
- IAM 역할 생성 및 구성
- MFA(Multi-Factor Authentication) 설정

## 사전 준비사항
- AWS 계정 (Free Tier 사용 가능)
- 관리자 권한 또는 IAM 전체 액세스 권한
- 스마트폰 (MFA 설정용)

---

## 실습 1: IAM 대시보드 탐색

### 1.1 IAM 콘솔 접속
1. AWS Management Console에 로그인
2. 서비스 검색창에 "IAM" 입력
3. "IAM" 서비스 클릭

### 1.2 IAM 대시보드 확인
**확인할 항목들:**
- Security recommendations (보안 권장사항)
- AWS account ID
- Account Alias (계정 별칭)
- Users, Groups, Roles, Policies 개수

**📸 스크린샷 위치:** IAM 대시보드 메인 화면

### 1.3 보안 권장사항 검토
대시보드에서 다음 항목들을 확인하세요:
- ✅ Root access keys (루트 액세스 키 삭제)
- ✅ MFA for root account (루트 계정 MFA 활성화)
- ✅ Individual IAM users (개별 IAM 사용자 생성)
- ✅ Strong password policy (강력한 비밀번호 정책)
- ✅ Rotate access keys (액세스 키 정기 교체)

---

## 실습 2: IAM 사용자 생성

### 2.1 첫 번째 사용자 생성 (개발자)
1. 왼쪽 메뉴에서 **"Users"** 클릭
2. **"Create user"** 버튼 클릭
3. 사용자 세부 정보 입력:
   - User name: `developer-alice`
   - ✅ Provide user access to the AWS Management Console
   - Console password: `Custom password` 선택
   - Password: `TempPassword123!` (실제로는 더 강력한 비밀번호 사용)
   - ✅ Users must create a new password at next sign-in

**📸 스크린샷 위치:** 사용자 생성 1단계 화면

### 2.2 권한 설정 (임시로 건너뛰기)
1. **"Next"** 클릭
2. 권한 설정 페이지에서 **"Next"** 클릭 (나중에 그룹을 통해 권한 부여)
3. 검토 페이지에서 **"Create user"** 클릭

### 2.3 두 번째 사용자 생성 (관리자)
같은 방식으로 관리자 사용자를 생성합니다:
- User name: `admin-bob`
- Console password: `AdminPass456!`
- ✅ Users must create a new password at next sign-in

---

## 실습 3: IAM 그룹 생성 및 관리

### 3.1 개발자 그룹 생성
1. 왼쪽 메뉴에서 **"User groups"** 클릭
2. **"Create group"** 버튼 클릭
3. 그룹 세부 정보:
   - Group name: `Developers`
   - Description: `Development team with limited AWS access`

### 3.2 개발자 그룹에 사용자 추가
1. **"Add users to group"** 섹션에서
2. `developer-alice` 체크박스 선택
3. **"Next"** 클릭

**📸 스크린샷 위치:** 그룹에 사용자 추가 화면

### 3.3 개발자 그룹에 정책 연결
1. **"Attach permissions policies"** 섹션에서
2. 다음 정책들을 검색하여 선택:
   - `AmazonEC2ReadOnlyAccess`
   - `AmazonS3ReadOnlyAccess`
   - `CloudWatchReadOnlyAccess`
3. **"Create group"** 클릭

### 3.4 관리자 그룹 생성
같은 방식으로 관리자 그룹을 생성합니다:
- Group name: `Administrators`
- User: `admin-bob`
- Policy: `AdministratorAccess` (⚠️ 실제 환경에서는 주의해서 사용)

---

## 실습 4: 커스텀 정책 생성

### 4.1 S3 특정 버킷 접근 정책 생성
1. 왼쪽 메뉴에서 **"Policies"** 클릭
2. **"Create policy"** 버튼 클릭
3. **"JSON"** 탭 선택
4. 다음 정책을 입력:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::my-dev-bucket/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": "arn:aws:s3:::my-dev-bucket"
        }
    ]
}
```

**📸 스크린샷 위치:** JSON 정책 편집기 화면

### 4.2 정책 세부 정보 입력
1. **"Next"** 클릭
2. Policy details:
   - Policy name: `S3-DevBucket-Access`
   - Description: `Allows read/write access to development S3 bucket`
3. **"Create policy"** 클릭

### 4.3 사용자에게 커스텀 정책 연결
1. **"Users"** → `developer-alice` 클릭
2. **"Permissions"** 탭 → **"Add permissions"** 클릭
3. **"Attach policies directly"** 선택
4. `S3-DevBucket-Access` 정책 검색 및 선택
5. **"Add permissions"** 클릭

---

## 실습 5: IAM 역할 생성

### 5.1 EC2용 S3 접근 역할 생성
1. 왼쪽 메뉴에서 **"Roles"** 클릭
2. **"Create role"** 버튼 클릭
3. **"Trusted entity type"**: AWS service
4. **"Use case"**: EC2 선택
5. **"Next"** 클릭

**📸 스크린샷 위치:** 역할 생성 - 신뢰할 수 있는 엔터티 선택

### 5.2 역할에 정책 연결
1. 다음 정책들을 검색하여 선택:
   - `AmazonS3ReadOnlyAccess`
   - `CloudWatchAgentServerPolicy`
2. **"Next"** 클릭

### 5.3 역할 세부 정보 입력
1. Role details:
   - Role name: `EC2-S3-ReadOnly-Role`
   - Description: `Allows EC2 instances to read from S3 buckets`
2. **"Create role"** 클릭

---

## 실습 6: MFA(Multi-Factor Authentication) 설정

### 6.1 가상 MFA 디바이스 설정
1. **"Users"** → `developer-alice` 클릭
2. **"Security credentials"** 탭 클릭
3. **"Multi-factor authentication (MFA)"** 섹션에서 **"Assign MFA device"** 클릭
4. **"Virtual MFA device"** 선택 → **"Continue"**

### 6.2 MFA 앱 설정
1. 스마트폰에 Google Authenticator 또는 Authy 앱 설치
2. QR 코드를 앱으로 스캔
3. 연속된 두 개의 MFA 코드 입력
4. **"Assign MFA"** 클릭

**📸 스크린샷 위치:** MFA QR 코드 화면

---

## 실습 7: 권한 테스트

### 7.1 개발자 계정으로 로그인 테스트
1. 새 시크릿 브라우저 창 열기
2. AWS Console 로그인 페이지 접속
3. Account ID 입력 (IAM 대시보드에서 확인)
4. Username: `developer-alice`
5. Password: `TempPassword123!`
6. 새 비밀번호 설정
7. MFA 코드 입력

### 7.2 권한 확인
개발자 계정으로 다음을 테스트해보세요:
- ✅ EC2 대시보드 조회 (읽기 전용)
- ✅ S3 버킷 목록 조회 (읽기 전용)
- ❌ EC2 인스턴스 생성 시도 (권한 없음 오류 확인)
- ❌ IAM 사용자 생성 시도 (권한 없음 오류 확인)

**📸 스크린샷 위치:** 권한 거부 오류 메시지

---

## 실습 8: 액세스 키 생성 및 관리

### 8.1 프로그래밍 방식 액세스를 위한 액세스 키 생성
1. 관리자 계정으로 다시 로그인
2. **"Users"** → `developer-alice` 클릭
3. **"Security credentials"** 탭
4. **"Access keys"** 섹션에서 **"Create access key"** 클릭
5. **"Use case"**: Command Line Interface (CLI) 선택
6. 확인 체크박스 선택 → **"Next"**
7. Description: `CLI access for development`
8. **"Create access key"** 클릭

### 8.2 액세스 키 안전하게 저장
⚠️ **중요**: 액세스 키는 한 번만 표시됩니다!
1. **"Download .csv file"** 클릭하여 안전한 위치에 저장
2. 또는 Access Key ID와 Secret Access Key를 별도로 복사하여 안전하게 보관

**📸 스크린샷 위치:** 액세스 키 생성 완료 화면

---

## 실습 9: 정책 시뮬레이터 사용

### 9.1 IAM 정책 시뮬레이터 접속
1. IAM 대시보드에서 **"Policy simulator"** 링크 클릭
2. 또는 직접 URL 접속: https://policysim.aws.amazon.com/

### 9.2 권한 시뮬레이션 테스트
1. **"Users, Groups, or Roles"**: `developer-alice` 선택
2. **"AWS Service"**: Amazon S3 선택
3. **"Actions"**: `GetObject` 선택
4. **"Resource"**: `arn:aws:s3:::my-dev-bucket/test.txt` 입력
5. **"Run Simulation"** 클릭

결과를 확인하여 권한이 올바르게 설정되었는지 검증합니다.

**📸 스크린샷 위치:** 정책 시뮬레이터 결과 화면

---

## 실습 10: 리소스 정리

### 10.1 테스트용 리소스 정리
실습이 완료되면 다음 리소스들을 정리합니다:

1. **액세스 키 삭제**:
   - Users → developer-alice → Security credentials
   - Access keys에서 생성한 키 **"Delete"**

2. **MFA 디바이스 제거** (선택사항):
   - Security credentials → MFA → **"Remove"**

3. **사용자 삭제** (선택사항):
   - Users에서 테스트 사용자들 선택 후 **"Delete"**

⚠️ **주의**: 실제 운영 환경에서는 리소스 삭제 시 신중하게 검토하세요.

---

## 실습 완료 체크리스트

다음 항목들을 완료했는지 확인하세요:

- [ ] IAM 대시보드 탐색 및 보안 권장사항 확인
- [ ] 2명의 IAM 사용자 생성 (developer-alice, admin-bob)
- [ ] 2개의 IAM 그룹 생성 (Developers, Administrators)
- [ ] 사용자를 적절한 그룹에 할당
- [ ] 커스텀 정책 생성 (S3-DevBucket-Access)
- [ ] IAM 역할 생성 (EC2-S3-ReadOnly-Role)
- [ ] MFA 설정 및 테스트
- [ ] 권한 테스트 (읽기 전용 권한 확인)
- [ ] 액세스 키 생성 및 관리
- [ ] 정책 시뮬레이터를 통한 권한 검증
- [ ] 테스트 리소스 정리

---

## 문제 해결 가이드

### 자주 발생하는 문제들

**1. "You are not authorized to perform this operation" 오류**
- 현재 사용자에게 해당 작업을 수행할 권한이 없음
- 관리자 권한으로 로그인했는지 확인
- 필요한 정책이 연결되어 있는지 확인

**2. MFA 설정 시 "Invalid MFA code" 오류**
- 스마트폰의 시간이 정확한지 확인
- 연속된 두 개의 서로 다른 코드를 입력했는지 확인
- MFA 앱이 올바르게 설정되었는지 확인

**3. 정책 JSON 구문 오류**
- JSON 형식이 올바른지 확인 (중괄호, 쉼표, 따옴표)
- AWS 정책 생성기 사용 고려
- 정책 검증 도구 활용

**4. 사용자 로그인 실패**
- 계정 ID가 정확한지 확인
- 사용자명과 비밀번호가 정확한지 확인
- 비밀번호 정책 요구사항을 충족하는지 확인

---

## 다음 단계

이 실습을 통해 IAM의 기본 개념과 실제 사용법을 익혔습니다. 내일은 EC2 인스턴스를 생성하면서 오늘 만든 IAM 역할을 실제로 연결해보는 실습을 진행합니다.

### 예습 과제
- EC2 인스턴스 유형별 특징 조사
- 보안 그룹과 네트워크 ACL의 차이점 학습
- 키 페어의 개념과 SSH 연결 방법 확인

**💡 실습 완료 후 기억할 점**
- IAM은 글로벌 서비스이며, 모든 리전에서 동일하게 적용됩니다
- 최소 권한 원칙을 항상 기억하세요
- 정기적인 권한 검토와 액세스 키 로테이션이 중요합니다
- MFA는 보안의 핵심이므로 가능한 모든 계정에 설정하세요