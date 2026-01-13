# Day 16 실습: CloudFront Distribution 생성 및 설정

## 실습 개요
이번 실습에서는 AWS CloudFront를 사용하여 S3 정적 웹사이트를 가속화하는 CDN을 구축해보겠습니다. S3 버킷에 정적 웹사이트를 호스팅하고, CloudFront Distribution을 생성하여 전 세계 사용자에게 빠른 콘텐츠 전송을 제공하는 방법을 학습합니다.

## 학습 목표
- CloudFront Distribution 생성 및 구성
- S3와 CloudFront 연동 설정
- Origin Access Control (OAC) 구성
- 캐시 동작 및 TTL 설정
- CloudFront 도메인을 통한 콘텐츠 접근 확인

## 사전 준비사항
- AWS 계정 및 Console 접근 권한
- 기본적인 HTML/CSS 지식
- S3 서비스에 대한 기본 이해

## 예상 소요 시간
약 45-60분

---

## 단계 1: S3 버킷 생성 및 정적 웹사이트 설정

### 1.1 S3 버킷 생성

1. **AWS Management Console**에 로그인합니다.

2. **Services** 메뉴에서 **S3**를 선택합니다.

3. **Create bucket** 버튼을 클릭합니다.

4. 버킷 설정을 다음과 같이 구성합니다:
   - **Bucket name**: `cloudfront-demo-[your-name]-[random-number]`
     - 예: `cloudfront-demo-john-12345`
   - **AWS Region**: `US East (N. Virginia) us-east-1`
   - **Object Ownership**: `ACLs disabled (recommended)`

5. **Block Public Access settings for this bucket** 섹션에서:
   - 모든 체크박스를 **체크 해제**합니다 (나중에 CloudFront를 통해서만 접근하도록 설정할 예정)

6. **Bucket Versioning**: `Disable`

7. **Default encryption**: `Server-side encryption with Amazon S3 managed keys (SSE-S3)`

8. **Create bucket** 버튼을 클릭하여 버킷을 생성합니다.

### 1.2 정적 웹사이트 파일 업로드

1. 생성된 버킷을 클릭하여 들어갑니다.

2. **Upload** 버튼을 클릭합니다.

3. 다음 HTML 파일을 생성하여 업로드합니다:

**index.html**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudFront Demo</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>CloudFront CDN Demo</h1>
        <p>이 페이지는 Amazon CloudFront를 통해 전송되고 있습니다!</p>
        <div class="info">
            <h2>CDN 장점</h2>
            <ul>
                <li>빠른 콘텐츠 로딩</li>
                <li>전 세계 Edge Location 활용</li>
                <li>Origin 서버 부하 감소</li>
                <li>향상된 사용자 경험</li>
            </ul>
        </div>
        <img src="aws-logo.png" alt="AWS Logo" class="logo">
    </div>
</body>
</html>
```

**style.css**
```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    padding: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

h1 {
    font-size: 2.5em;
    margin-bottom: 20px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.info {
    background: rgba(255, 255, 255, 0.2);
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

ul {
    text-align: left;
    display: inline-block;
}

li {
    margin: 10px 0;
    font-size: 1.1em;
}

.logo {
    max-width: 200px;
    margin-top: 20px;
    border-radius: 10px;
}
```

4. AWS 로고 이미지 파일도 함께 업로드합니다 (또는 다른 이미지 파일 사용).

5. **Upload** 버튼을 클릭하여 파일들을 업로드합니다.

### 1.3 정적 웹사이트 호스팅 활성화

1. 버킷의 **Properties** 탭을 클릭합니다.

2. 하단의 **Static website hosting** 섹션을 찾아 **Edit** 버튼을 클릭합니다.

3. 다음과 같이 설정합니다:
   - **Static website hosting**: `Enable`
   - **Hosting type**: `Host a static website`
   - **Index document**: `index.html`
   - **Error document**: `index.html` (선택사항)

4. **Save changes** 버튼을 클릭합니다.

5. **Static website hosting** 섹션에서 **Bucket website endpoint** URL을 복사해 둡니다.
   - 예: `http://cloudfront-demo-john-12345.s3-website-us-east-1.amazonaws.com`

---

## 단계 2: CloudFront Distribution 생성

### 2.1 CloudFront 서비스 접근

1. AWS Management Console에서 **Services** 메뉴를 클릭합니다.

2. **Networking & Content Delivery** 섹션에서 **CloudFront**를 선택합니다.

3. **Create distribution** 버튼을 클릭합니다.

### 2.2 Origin 설정

1. **Origin** 섹션에서 다음과 같이 설정합니다:

   **Origin domain**:
   - 드롭다운에서 앞서 생성한 S3 버킷을 선택합니다
   - 예: `cloudfront-demo-john-12345.s3.us-east-1.amazonaws.com`

   **Origin path**: 비워둡니다

   **Name**: 자동으로 생성된 이름을 그대로 사용합니다

   **Origin access**: `Origin access control settings (recommended)` 선택

   **Origin access control**:
   - **Create control setting** 버튼을 클릭합니다
   - **Name**: 기본값 사용
   - **Description**: 기본값 사용
   - **Signing behavior**: `Sign requests (recommended)`
   - **Origin type**: `S3`
   - **Create** 버튼을 클릭합니다

### 2.3 Default Cache Behavior 설정

1. **Default cache behavior** 섹션에서:

   **Path pattern**: `Default (*)`

   **Compress objects automatically**: `Yes` (체크)

   **Viewer protocol policy**: `Redirect HTTP to HTTPS`

   **Allowed HTTP methods**: `GET, HEAD`

   **Restrict viewer access**: `No`

### 2.4 Cache Key and Origin Requests 설정

1. **Cache key and origin requests** 섹션에서:

   **Cache policy**: `Managed-CachingOptimized`

   **Origin request policy**: `None`

### 2.5 Function Associations (선택사항)

이 섹션은 기본값으로 두고 넘어갑니다.

### 2.6 Settings 설정

1. **Settings** 섹션에서:

   **Price class**: `Use all edge locations (best performance)`

   **Alternate domain name (CNAME)**: 비워둡니다

   **Custom SSL certificate**: 기본값 사용

   **Supported HTTP versions**: `HTTP/2 and HTTP/1.1`

   **Default root object**: `index.html`

   **Standard logging**: `Off`

   **IPv6**: `On` (체크)

2. **Create distribution** 버튼을 클릭합니다.

### 2.7 Distribution 배포 대기

1. Distribution이 생성되면 **Status**가 `Deploying`으로 표시됩니다.

2. 배포가 완료될 때까지 5-15분 정도 기다립니다.

3. **Status**가 `Enabled`로 변경되면 배포가 완료된 것입니다.

4. **Distribution domain name**을 복사해 둡니다.
   - 예: `d1234567890123.cloudfront.net`

---

## 단계 3: S3 버킷 정책 업데이트

### 3.1 버킷 정책 복사

1. CloudFront Distribution 페이지에서 **Origins** 탭을 클릭합니다.

2. 생성한 Origin을 선택하고 **Edit** 버튼을 클릭합니다.

3. 페이지 상단에 **Copy policy** 버튼이 표시됩니다. 클릭하여 정책을 복사합니다.

### 3.2 S3 버킷에 정책 적용

1. S3 서비스로 돌아가서 생성한 버킷을 선택합니다.

2. **Permissions** 탭을 클릭합니다.

3. **Bucket policy** 섹션에서 **Edit** 버튼을 클릭합니다.

4. 복사한 정책을 붙여넣습니다. 정책은 다음과 유사합니다:

```json
{
    "Version": "2008-10-17",
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::cloudfront-demo-john-12345/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::123456789012:distribution/E1234567890123"
                }
            }
        }
    ]
}
```

5. **Save changes** 버튼을 클릭합니다.

---

## 단계 4: CloudFront 동작 확인

### 4.1 CloudFront URL 접근

1. 웹 브라우저에서 CloudFront Distribution domain name으로 접근합니다.
   - 예: `https://d1234567890123.cloudfront.net`

2. 정적 웹사이트가 정상적으로 로드되는지 확인합니다.

3. 개발자 도구(F12)를 열고 **Network** 탭에서 응답 헤더를 확인합니다:
   - `x-cache: Miss from cloudfront` (첫 번째 요청)
   - `x-cache: Hit from cloudfront` (두 번째 요청)

### 4.2 S3 직접 접근 차단 확인

1. S3 정적 웹사이트 endpoint URL로 직접 접근을 시도합니다.
   - 예: `http://cloudfront-demo-john-12345.s3-website-us-east-1.amazonaws.com`

2. 접근이 차단되는지 확인합니다 (403 Forbidden 오류).

### 4.3 캐시 동작 확인

1. 브라우저에서 CloudFront URL을 여러 번 새로고침합니다.

2. 개발자 도구의 Network 탭에서 응답 시간이 줄어드는 것을 확인합니다.

3. `x-cache` 헤더가 `Hit from cloudfront`로 변경되는 것을 확인합니다.

---

## 단계 5: 추가 설정 및 최적화

### 5.1 캐시 무효화 (Invalidation) 테스트

1. S3 버킷에서 `index.html` 파일을 수정합니다:
   - 제목을 "CloudFront CDN Demo - Updated!"로 변경

2. CloudFront Console에서 **Invalidations** 탭을 클릭합니다.

3. **Create invalidation** 버튼을 클릭합니다.

4. **Object paths**에 `/*`를 입력합니다.

5. **Create invalidation** 버튼을 클릭합니다.

6. 무효화가 완료된 후 CloudFront URL을 새로고침하여 변경사항이 반영되는지 확인합니다.

### 5.2 압축 설정 확인

1. 개발자 도구의 Network 탭에서 CSS 파일을 확인합니다.

2. Response Headers에서 `content-encoding: gzip`이 있는지 확인합니다.

3. 파일 크기가 압축되어 전송되는지 확인합니다.

### 5.3 HTTPS 리디렉션 확인

1. HTTP URL로 접근을 시도합니다:
   - `http://d1234567890123.cloudfront.net`

2. 자동으로 HTTPS로 리디렉션되는지 확인합니다.

---

## 단계 6: 모니터링 및 분석

### 6.1 CloudWatch 메트릭 확인

1. CloudFront Console에서 생성한 Distribution을 선택합니다.

2. **Monitoring** 탭을 클릭합니다.

3. 다음 메트릭들을 확인합니다:
   - **Requests**: 총 요청 수
   - **Bytes downloaded**: 다운로드된 바이트 수
   - **Error rate**: 오류율

### 6.2 실시간 로그 (선택사항)

1. **Logs** 탭을 클릭합니다.

2. **Real-time logs**에서 실시간 로그 스트림을 확인할 수 있습니다.

---

## 문제 해결 가이드

### 일반적인 문제들

**1. 403 Forbidden 오류**
- S3 버킷 정책이 올바르게 설정되었는지 확인
- Origin Access Control 설정 확인
- 버킷의 Block Public Access 설정 확인

**2. 콘텐츠가 업데이트되지 않음**
- 캐시 무효화(Invalidation) 실행
- TTL 설정 확인
- 브라우저 캐시 삭제

**3. 느린 로딩 속도**
- 압축 설정 확인
- 적절한 캐시 정책 설정
- 파일 크기 최적화

**4. SSL/TLS 인증서 오류**
- CloudFront 기본 인증서 사용 확인
- 사용자 정의 도메인 설정 시 ACM 인증서 확인

---

## 실습 완료 체크리스트

- [ ] S3 버킷 생성 및 정적 웹사이트 설정
- [ ] HTML, CSS 파일 업로드
- [ ] CloudFront Distribution 생성
- [ ] Origin Access Control (OAC) 설정
- [ ] S3 버킷 정책 업데이트
- [ ] CloudFront URL을 통한 웹사이트 접근 확인
- [ ] S3 직접 접근 차단 확인
- [ ] 캐시 동작 확인 (Hit/Miss)
- [ ] 캐시 무효화 테스트
- [ ] 압축 및 HTTPS 리디렉션 확인
- [ ] CloudWatch 메트릭 확인

---

## 정리 및 리소스 삭제

실습 완료 후 비용 절약을 위해 다음 리소스들을 삭제합니다:

1. **CloudFront Distribution 삭제**:
   - Distribution을 선택하고 **Disable** 후 **Delete**

2. **S3 버킷 삭제**:
   - 버킷 내 모든 객체 삭제 후 버킷 삭제

3. **Origin Access Control 삭제** (선택사항):
   - CloudFront Console에서 OAC 설정 삭제

---

## 다음 단계

이번 실습을 통해 CloudFront의 기본적인 설정과 동작 원리를 이해했습니다. 다음 학습에서는:

- Route 53과 CloudFront 연동
- 사용자 정의 도메인 설정
- AWS WAF와 CloudFront 통합
- Lambda@Edge 활용

등의 고급 기능들을 학습하게 됩니다.

## 참고 자료

- [Amazon CloudFront 개발자 가이드](https://docs.aws.amazon.com/cloudfront/)
- [CloudFront 가격 정보](https://aws.amazon.com/cloudfront/pricing/)
- [CloudFront 모범 사례](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/best-practices.html)