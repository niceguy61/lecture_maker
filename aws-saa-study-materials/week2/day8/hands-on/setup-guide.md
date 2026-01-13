# Day 8 실습: Amazon S3 버킷 생성 및 정책 설정

## 실습 개요
이번 실습에서는 AWS Console을 통해 S3 버킷을 생성하고, 다양한 보안 정책을 설정하는 방법을 학습합니다. 실제 웹사이트 호스팅과 파일 공유 시나리오를 통해 S3의 핵심 기능을 체험해보겠습니다.

## 실습 목표
- S3 버킷 생성 및 기본 설정 이해
- 버킷 정책을 통한 액세스 제어 구현
- 정적 웹사이트 호스팅 설정
- S3 객체 업로드 및 관리
- 버전 관리 및 라이프사이클 정책 설정

## 사전 준비사항
- AWS 계정 및 Console 액세스
- 실습용 HTML 파일 (아래 제공)
- 테스트용 이미지 파일 (선택사항)

## 실습 1: S3 버킷 생성하기

### 1.1 AWS Console에서 S3 서비스 접근
1. AWS Management Console에 로그인
2. 서비스 검색창에 "S3" 입력 후 선택
3. S3 대시보드에서 **"Create bucket"** 클릭

### 1.2 버킷 기본 설정
1. **Bucket name**: `my-saa-study-bucket-[본인이름]-[날짜]`
   - 예: `my-saa-study-bucket-john-20240115`
   - ⚠️ 버킷 이름은 전역적으로 고유해야 함
   
2. **AWS Region**: `Asia Pacific (Seoul) ap-northeast-2` 선택
   - 지연 시간 최소화를 위해 가까운 리전 선택

3. **Object Ownership**: 
   - **ACLs disabled (recommended)** 선택
   - 버킷 정책과 IAM 정책으로 액세스 제어 권장

### 1.3 퍼블릭 액세스 설정
1. **Block Public Access settings for this bucket**:
   - 모든 체크박스 **해제** (실습 목적)
   - ⚠️ 프로덕션 환경에서는 신중하게 설정 필요

2. **Bucket Versioning**: 
   - **Enable** 선택 (버전 관리 활성화)

3. **Default encryption**:
   - **Server-side encryption with Amazon S3 managed keys (SSE-S3)** 선택

4. **Create bucket** 클릭하여 버킷 생성 완료

### 📸 스크린샷 포인트
- 버킷 생성 화면의 각 설정 옵션
- 생성 완료된 버킷 목록

## 실습 2: 정적 웹사이트 호스팅 설정

### 2.1 테스트용 HTML 파일 준비
다음 내용으로 `index.html` 파일을 생성하세요:

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My S3 Website</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #232f3e;
            text-align: center;
        }
        .aws-logo {
            color: #ff9900;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 My First <span class="aws-logo">AWS S3</span> Website!</h1>
        <p>축하합니다! S3 정적 웹사이트 호스팅이 성공적으로 설정되었습니다.</p>
        <h2>실습 완료 체크리스트:</h2>
        <ul>
            <li>✅ S3 버킷 생성</li>
            <li>✅ 정적 웹사이트 호스팅 활성화</li>
            <li>✅ 퍼블릭 액세스 정책 설정</li>
            <li>✅ HTML 파일 업로드</li>
        </ul>
        <p><strong>학습 날짜:</strong> Day 8 - Amazon S3</p>
        <p><strong>다음 학습:</strong> Day 9 - EBS, EFS, FSx</p>
    </div>
</body>
</html>
```

### 2.2 정적 웹사이트 호스팅 활성화
1. 생성한 버킷 클릭하여 상세 페이지 진입
2. **Properties** 탭 선택
3. 하단의 **Static website hosting** 섹션에서 **Edit** 클릭
4. **Static website hosting**: **Enable** 선택
5. **Hosting type**: **Host a static website** 선택
6. **Index document**: `index.html` 입력
7. **Error document**: `error.html` 입력 (선택사항)
8. **Save changes** 클릭

### 2.3 HTML 파일 업로드
1. 버킷 상세 페이지에서 **Objects** 탭 선택
2. **Upload** 버튼 클릭
3. **Add files**를 클릭하여 준비한 `index.html` 파일 선택
4. **Upload** 클릭하여 업로드 완료

### 📸 스크린샷 포인트
- Static website hosting 설정 화면
- 파일 업로드 완료 화면

## 실습 3: 버킷 정책 설정

### 3.1 퍼블릭 읽기 권한 정책 생성
1. 버킷 상세 페이지에서 **Permissions** 탭 선택
2. **Bucket policy** 섹션에서 **Edit** 클릭
3. 다음 JSON 정책을 입력:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-saa-study-bucket-[본인이름]-[날짜]/*"
        }
    ]
}
```

⚠️ **중요**: `Resource` 부분의 버킷 이름을 실제 생성한 버킷 이름으로 변경하세요!

4. **Save changes** 클릭

### 3.2 웹사이트 접근 테스트
1. **Properties** 탭으로 이동
2. **Static website hosting** 섹션에서 **Bucket website endpoint** URL 복사
3. 새 브라우저 탭에서 해당 URL 접속
4. HTML 페이지가 정상적으로 표시되는지 확인

### 📸 스크린샷 포인트
- 버킷 정책 편집 화면
- 웹사이트 엔드포인트 URL
- 브라우저에서 접속한 웹사이트 화면

## 실습 4: 객체 관리 및 메타데이터

### 4.1 추가 파일 업로드
1. 다음 내용으로 `error.html` 파일 생성:

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>페이지를 찾을 수 없습니다</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background-color: #f8f9fa;
        }
        .error-container {
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #dc3545;
            font-size: 3em;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <h1>404</h1>
        <h2>페이지를 찾을 수 없습니다</h2>
        <p>요청하신 페이지가 존재하지 않습니다.</p>
        <a href="index.html">홈으로 돌아가기</a>
    </div>
</body>
</html>
```

2. S3 버킷에 `error.html` 파일 업로드

### 4.2 객체 메타데이터 설정
1. 업로드된 `index.html` 파일 클릭
2. **Properties** 탭에서 **Metadata** 섹션 확인
3. **Edit** 클릭하여 사용자 정의 메타데이터 추가:
   - **Key**: `author`
   - **Value**: `[본인 이름]`
   - **Key**: `purpose`
   - **Value**: `SAA-C03 Study Lab`

### 4.3 객체 URL 및 액세스 테스트
1. 각 객체의 **Object URL** 복사
2. 브라우저에서 직접 접근 테스트
3. 존재하지 않는 페이지 접근하여 error.html 표시 확인

## 실습 5: 버전 관리 테스트

### 5.1 파일 수정 및 재업로드
1. `index.html` 파일을 수정:
   - 제목에 "Version 2" 추가
   - 새로운 내용 추가

```html
<h1>🚀 My First <span class="aws-logo">AWS S3</span> Website! (Version 2)</h1>
<p><strong>업데이트:</strong> 버전 관리 테스트를 위한 수정된 버전입니다.</p>
```

2. 수정된 파일을 같은 이름으로 다시 업로드

### 5.2 버전 확인
1. 버킷의 **Objects** 탭에서 **Show versions** 토글 활성화
2. `index.html` 파일의 여러 버전 확인
3. 이전 버전 클릭하여 상세 정보 확인
4. **Download** 또는 **Open**으로 이전 버전 내용 확인

### 📸 스크린샷 포인트
- 버전 관리 화면 (Show versions 활성화)
- 여러 버전이 표시된 객체 목록

## 실습 6: 라이프사이클 정책 설정

### 6.1 라이프사이클 규칙 생성
1. 버킷 상세 페이지에서 **Management** 탭 선택
2. **Lifecycle rules** 섹션에서 **Create lifecycle rule** 클릭
3. **Lifecycle rule name**: `test-lifecycle-rule` 입력
4. **Rule scope**: **Apply to all objects in the bucket** 선택

### 6.2 전환 규칙 설정
1. **Lifecycle rule actions**에서 다음 항목 체크:
   - ✅ **Transition current versions of objects between storage classes**
   - ✅ **Transition noncurrent versions of objects between storage classes**

2. **Transition current versions of objects between storage classes**:
   - **Storage class transitions**: **Standard-IA** 선택
   - **Days after object creation**: `30` 입력

3. **Transition noncurrent versions of objects between storage classes**:
   - **Storage class transitions**: **Standard-IA** 선택
   - **Days after objects become noncurrent**: `30` 입력

4. **Create rule** 클릭

### 📸 스크린샷 포인트
- 라이프사이클 규칙 생성 화면
- 완성된 라이프사이클 규칙 목록

## 실습 7: 모니터링 및 로깅

### 7.1 CloudWatch 메트릭 확인
1. 버킷 상세 페이지에서 **Metrics** 탭 선택
2. **Storage** 메트릭에서 다음 확인:
   - **BucketSizeBytes**: 버킷 총 크기
   - **NumberOfObjects**: 객체 수

3. **Requests** 메트릭에서 다음 확인:
   - **AllRequests**: 총 요청 수
   - **GetRequests**: GET 요청 수

### 7.2 서버 액세스 로깅 설정
1. **Properties** 탭에서 **Server access logging** 섹션 찾기
2. **Edit** 클릭
3. **Server access logging**: **Enable** 선택
4. **Target bucket**: 현재 버킷 선택 (또는 별도 로그 버킷)
5. **Target prefix**: `access-logs/` 입력
6. **Save changes** 클릭

## 실습 8: 보안 강화

### 8.1 CORS 설정 (Cross-Origin Resource Sharing)
1. **Permissions** 탭에서 **Cross-origin resource sharing (CORS)** 섹션 찾기
2. **Edit** 클릭
3. 다음 CORS 구성 입력:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": ["ETag"],
        "MaxAgeSeconds": 3000
    }
]
```

4. **Save changes** 클릭

### 8.2 암호화 설정 확인
1. **Properties** 탭에서 **Default encryption** 섹션 확인
2. 현재 설정된 암호화 방식 확인 (SSE-S3)
3. 필요시 **Edit**을 통해 KMS 암호화로 변경 가능

## 실습 9: 성능 테스트

### 9.1 대용량 파일 업로드 테스트
1. 10MB 이상의 테스트 파일 준비 (또는 생성)
2. S3 Console을 통해 업로드
3. 업로드 진행 상황 및 완료 시간 확인
4. 멀티파트 업로드 자동 적용 확인

### 9.2 Transfer Acceleration 테스트 (선택사항)
1. **Properties** 탭에서 **Transfer acceleration** 섹션 찾기
2. **Edit** 클릭하여 **Enable** 선택
3. 가속화된 엔드포인트 URL 확인
4. 일반 엔드포인트와 성능 비교

## 실습 10: 정리 및 비용 관리

### 10.1 비용 추정
1. AWS Pricing Calculator 접속
2. S3 서비스 선택하여 현재 사용량 기반 비용 계산
3. 다양한 스토리지 클래스별 비용 비교

### 10.2 리소스 정리 (실습 완료 후)
⚠️ **중요**: 불필요한 비용 발생을 방지하기 위해 실습 완료 후 정리하세요.

1. **버킷 비우기**:
   - 버킷 선택 후 **Empty** 클릭
   - 확인 문구 입력 후 실행

2. **버킷 삭제**:
   - 빈 버킷 선택 후 **Delete** 클릭
   - 버킷 이름 입력하여 삭제 확인

## 실습 완료 체크리스트

### 필수 완료 항목
- [ ] S3 버킷 생성 및 기본 설정
- [ ] 정적 웹사이트 호스팅 설정 및 테스트
- [ ] 버킷 정책을 통한 퍼블릭 액세스 설정
- [ ] HTML 파일 업로드 및 웹사이트 접근 확인
- [ ] 객체 메타데이터 설정
- [ ] 버전 관리 기능 테스트
- [ ] 라이프사이클 정책 생성
- [ ] CloudWatch 메트릭 확인

### 추가 도전 과제
- [ ] 서버 액세스 로깅 설정
- [ ] CORS 구성 설정
- [ ] Transfer Acceleration 테스트
- [ ] 다양한 스토리지 클래스 테스트
- [ ] 비용 계산 및 최적화 방안 검토

## 문제 해결 가이드

### 자주 발생하는 문제들

**1. 웹사이트에 접근할 수 없는 경우**
- 버킷 정책이 올바르게 설정되었는지 확인
- 퍼블릭 액세스 차단 설정 확인
- 정적 웹사이트 호스팅이 활성화되었는지 확인

**2. 403 Forbidden 오류**
- 버킷 정책의 Resource ARN이 정확한지 확인
- 객체에 대한 읽기 권한이 있는지 확인

**3. 404 Not Found 오류**
- 파일 이름과 경로가 정확한지 확인
- Index document 설정이 올바른지 확인

**4. 업로드 실패**
- 파일 크기 제한 확인 (5TB 이하)
- 네트워크 연결 상태 확인
- 브라우저 새로고침 후 재시도

## 실습 후 학습 포인트

### 핵심 개념 정리
1. **S3는 객체 스토리지**: 파일 시스템이 아닌 키-값 저장소
2. **버킷 정책의 중요성**: 세밀한 액세스 제어 가능
3. **정적 웹사이트 호스팅**: 간단하고 비용 효율적인 웹 호스팅
4. **버전 관리**: 데이터 보호 및 변경 추적
5. **라이프사이클 정책**: 자동화된 비용 최적화

### 실무 적용 시나리오
- **기업 웹사이트**: 정적 콘텐츠 호스팅
- **백업 솔루션**: 중요 데이터의 안전한 보관
- **데이터 아카이브**: 장기 보관이 필요한 데이터
- **콘텐츠 배포**: 글로벌 사용자 대상 파일 배포
- **로그 저장소**: 애플리케이션 로그 중앙 집중 관리

## 다음 단계
내일 Day 9에서는 EBS, EFS, FSx 등 다른 스토리지 서비스들을 학습하여 S3와의 차이점과 각각의 최적 사용 사례를 비교해보겠습니다.

---

**실습 완료 시간**: 약 60-90분  
**난이도**: 초급-중급  
**비용**: AWS Free Tier 범위 내 (정리 시 비용 없음)