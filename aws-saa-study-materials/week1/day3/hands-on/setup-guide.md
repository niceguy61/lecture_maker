# Day 3 실습: EC2 인스턴스 생성 및 관리

## 실습 개요

이 실습에서는 AWS Console을 사용하여 EC2 인스턴스를 생성하고, 웹 서버를 설치하여 실제 동작하는 웹사이트를 만들어보겠습니다. 또한 인스턴스 관리의 기본적인 작업들을 경험해보겠습니다.

## 실습 목표

- EC2 인스턴스 생성 과정 이해
- 보안 그룹 설정 및 관리
- 키 페어 생성 및 SSH 접속
- 웹 서버 설치 및 설정
- 인스턴스 모니터링 및 관리
- 인스턴스 중지 및 종료

## 사전 준비사항

### 필요한 도구
- AWS 계정 (Free Tier 권장)
- SSH 클라이언트
  - **Windows**: PuTTY 또는 Windows Terminal
  - **macOS/Linux**: 터미널 (기본 제공)
- 웹 브라우저

### 예상 비용
- t3.micro 인스턴스: 시간당 약 $0.0104 (Free Tier 대상)
- EBS 볼륨 8GB: 월 약 $0.80 (Free Tier에서 30GB까지 무료)
- 데이터 전송: 월 1GB까지 무료

### 주의사항
⚠️ **중요**: 실습 완료 후 반드시 인스턴스를 중지하거나 종료하여 불필요한 비용을 방지하세요.

---

## 실습 1: EC2 인스턴스 생성

### 1.1 AWS Console 접속 및 EC2 서비스 이동

1. **AWS Management Console 접속**
   - https://console.aws.amazon.com 접속
   - IAM 사용자로 로그인 (Day 2에서 생성한 계정)

2. **EC2 서비스 찾기**
   - 상단 검색창에 "EC2" 입력
   - "EC2" 서비스 클릭
   - 또는 "서비스" → "컴퓨팅" → "EC2" 선택

3. **리전 확인**
   - 우상단에서 현재 리전 확인 (예: 서울 - ap-northeast-2)
   - 필요시 원하는 리전으로 변경

### 1.2 인스턴스 시작하기

1. **인스턴스 시작 버튼 클릭**
   - EC2 대시보드에서 "인스턴스 시작" 버튼 클릭
   - 또는 좌측 메뉴에서 "인스턴스" → "인스턴스 시작"

2. **이름 및 태그 설정**
   ```
   이름: MyFirstWebServer
   ```
   - 태그는 리소스 관리에 중요하므로 의미있는 이름 사용

### 1.3 AMI (Amazon Machine Image) 선택

1. **Amazon Linux 2023 선택**
   - "빠른 시작" 탭에서 "Amazon Linux" 선택
   - "Amazon Linux 2023 AMI" 선택 (최신 버전)
   - 아키텍처: 64비트 (x86) 선택

2. **AMI 정보 확인**
   - Free tier eligible 표시 확인
   - AMI ID 및 설명 확인

### 1.4 인스턴스 유형 선택

1. **t3.micro 선택**
   - 인스턴스 유형: `t3.micro` 선택
   - vCPU: 2, 메모리: 1 GiB 확인
   - "프리 티어 사용 가능" 표시 확인

2. **인스턴스 유형 비교** (참고용)
   | 유형 | vCPU | 메모리 | 네트워크 성능 | 시간당 요금 |
   |------|------|--------|---------------|-------------|
   | t3.nano | 2 | 0.5 GiB | 최대 5 Gbps | $0.0052 |
   | t3.micro | 2 | 1 GiB | 최대 5 Gbps | $0.0104 |
   | t3.small | 2 | 2 GiB | 최대 5 Gbps | $0.0208 |

### 1.5 키 페어 생성

1. **새 키 페어 생성**
   - "새 키 페어 생성" 클릭
   - 키 페어 이름: `my-ec2-keypair`
   - 키 페어 유형: RSA
   - 프라이빗 키 파일 형식: .pem (Linux/macOS) 또는 .ppk (Windows/PuTTY)

2. **키 페어 다운로드**
   - "키 페어 생성" 클릭
   - 자동으로 다운로드되는 .pem 파일을 안전한 위치에 저장
   - **중요**: 이 파일을 분실하면 인스턴스에 접속할 수 없습니다!

3. **키 파일 권한 설정** (Linux/macOS)
   ```bash
   chmod 400 ~/Downloads/my-ec2-keypair.pem
   ```

### 1.6 네트워크 설정

1. **VPC 및 서브넷**
   - VPC: 기본 VPC 사용
   - 서브넷: 기본 서브넷 사용 (퍼블릭 서브넷)
   - 퍼블릭 IP 자동 할당: 활성화

2. **보안 그룹 생성**
   - "보안 그룹 생성" 선택
   - 보안 그룹 이름: `web-server-sg`
   - 설명: `Security group for web server`

3. **인바운드 보안 그룹 규칙 설정**
   
   **SSH 규칙 (기본으로 있음)**
   - 유형: SSH
   - 포트: 22
   - 소스: 내 IP (권장) 또는 0.0.0.0/0 (모든 IP)
   
   **HTTP 규칙 추가**
   - "보안 그룹 규칙 추가" 클릭
   - 유형: HTTP
   - 포트: 80
   - 소스: 0.0.0.0/0 (모든 곳에서 접근 가능)
   
   **HTTPS 규칙 추가** (선택사항)
   - "보안 그룹 규칙 추가" 클릭
   - 유형: HTTPS
   - 포트: 443
   - 소스: 0.0.0.0/0

### 1.7 스토리지 구성

1. **루트 볼륨 설정**
   - 볼륨 유형: gp3 (범용 SSD)
   - 크기: 8 GiB (Free Tier 기본값)
   - 종료 시 삭제: 활성화 (기본값)

2. **추가 볼륨** (선택사항)
   - 이번 실습에서는 추가 볼륨 생성하지 않음

### 1.8 고급 세부 정보 (선택사항)

1. **사용자 데이터 스크립트**
   - 인스턴스 시작 시 자동으로 실행할 스크립트
   - 이번 실습에서는 수동으로 설치할 예정이므로 비워둠

2. **기타 설정**
   - 모니터링: 기본 모니터링 (5분 간격)
   - 테넌시: 공유 (기본값)

### 1.9 인스턴스 시작

1. **설정 검토**
   - 우측 요약 패널에서 설정 내용 확인
   - 예상 비용 확인

2. **인스턴스 시작**
   - "인스턴스 시작" 버튼 클릭
   - 성공 메시지 확인

3. **인스턴스 보기**
   - "모든 인스턴스 보기" 클릭
   - 인스턴스 상태가 "Pending"에서 "Running"으로 변경될 때까지 대기 (약 1-2분)

---

## 실습 2: 인스턴스 연결 및 웹 서버 설치

### 2.1 인스턴스 정보 확인

1. **인스턴스 선택**
   - 생성한 인스턴스 선택 (체크박스 클릭)
   - 하단 세부 정보 탭에서 정보 확인

2. **중요 정보 기록**
   ```
   인스턴스 ID: i-xxxxxxxxxxxxxxxxx
   퍼블릭 IPv4 주소: x.x.x.x
   프라이빗 IPv4 주소: x.x.x.x
   퍼블릭 IPv4 DNS: ec2-x-x-x-x.region.compute.amazonaws.com
   ```

### 2.2 SSH 연결 (Linux/macOS)

1. **터미널 열기**
   - macOS: Spotlight에서 "터미널" 검색
   - Linux: Ctrl+Alt+T

2. **SSH 연결 명령어**
   ```bash
   ssh -i ~/Downloads/my-ec2-keypair.pem ec2-user@YOUR_PUBLIC_IP
   ```
   
   예시:
   ```bash
   ssh -i ~/Downloads/my-ec2-keypair.pem ec2-user@54.180.123.45
   ```

3. **첫 연결 시 확인**
   - "Are you sure you want to continue connecting?" → `yes` 입력
   - 성공적으로 연결되면 Amazon Linux 환영 메시지 표시

### 2.3 SSH 연결 (Windows - PuTTY)

1. **PuTTY 설정**
   - Host Name: ec2-user@YOUR_PUBLIC_IP
   - Port: 22
   - Connection type: SSH

2. **키 파일 설정**
   - Connection → SSH → Auth → Credentials
   - "Private key file for authentication"에서 .ppk 파일 선택

3. **연결**
   - "Open" 클릭
   - 보안 경고 시 "Accept" 클릭

### 2.4 시스템 업데이트

1. **패키지 업데이트**
   ```bash
   sudo yum update -y
   ```

2. **업데이트 완료 확인**
   - 업데이트 과정 관찰 (약 1-2분 소요)
   - "Complete!" 메시지 확인

### 2.5 Apache 웹 서버 설치

1. **Apache 설치**
   ```bash
   sudo yum install -y httpd
   ```

2. **Apache 서비스 시작**
   ```bash
   sudo systemctl start httpd
   ```

3. **부팅 시 자동 시작 설정**
   ```bash
   sudo systemctl enable httpd
   ```

4. **서비스 상태 확인**
   ```bash
   sudo systemctl status httpd
   ```
   - "active (running)" 상태 확인

### 2.6 웹 페이지 생성

1. **기본 HTML 파일 생성**
   ```bash
   sudo nano /var/www/html/index.html
   ```

2. **HTML 내용 입력**
   ```html
   <!DOCTYPE html>
   <html lang="ko">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>내 첫 번째 EC2 웹 서버</title>
       <style>
           body {
               font-family: Arial, sans-serif;
               max-width: 800px;
               margin: 0 auto;
               padding: 20px;
               background-color: #f0f0f0;
           }
           .container {
               background-color: white;
               padding: 30px;
               border-radius: 10px;
               box-shadow: 0 2px 10px rgba(0,0,0,0.1);
           }
           h1 {
               color: #232F3E;
               text-align: center;
           }
           .info {
               background-color: #E8F4FD;
               padding: 15px;
               border-radius: 5px;
               margin: 20px 0;
           }
           .success {
               color: #28a745;
               font-weight: bold;
           }
       </style>
   </head>
   <body>
       <div class="container">
           <h1>🎉 EC2 웹 서버 성공!</h1>
           <div class="info">
               <h3>서버 정보</h3>
               <p><strong>인스턴스 유형:</strong> t3.micro</p>
               <p><strong>운영체제:</strong> Amazon Linux 2023</p>
               <p><strong>웹 서버:</strong> Apache HTTP Server</p>
               <p><strong>생성 일시:</strong> <span id="datetime"></span></p>
           </div>
           <p class="success">✅ AWS EC2 인스턴스에서 웹 서버가 정상적으로 실행 중입니다!</p>
           <p>이 페이지는 AWS EC2 인스턴스에서 호스팅되고 있으며, Apache 웹 서버를 통해 제공됩니다.</p>
           
           <h3>실습 완료 항목</h3>
           <ul>
               <li>✅ EC2 인스턴스 생성</li>
               <li>✅ 보안 그룹 설정</li>
               <li>✅ SSH 키 페어 생성</li>
               <li>✅ 인스턴스 SSH 접속</li>
               <li>✅ Apache 웹 서버 설치</li>
               <li>✅ 웹 페이지 생성</li>
           </ul>
       </div>
       
       <script>
           document.getElementById('datetime').textContent = new Date().toLocaleString('ko-KR');
       </script>
   </body>
   </html>
   ```

3. **파일 저장 및 종료**
   - Ctrl+X → Y → Enter (nano 에디터)

4. **파일 권한 확인**
   ```bash
   ls -la /var/www/html/
   ```

### 2.7 웹 서버 테스트

1. **로컬에서 테스트**
   ```bash
   curl localhost
   ```
   - HTML 내용이 출력되면 성공

2. **웹 브라우저에서 테스트**
   - 브라우저에서 `http://YOUR_PUBLIC_IP` 접속
   - 생성한 웹 페이지가 표시되면 성공

3. **문제 해결**
   - 접속이 안 되는 경우:
     - 보안 그룹에서 HTTP (포트 80) 규칙 확인
     - Apache 서비스 상태 확인: `sudo systemctl status httpd`
     - 방화벽 상태 확인: `sudo systemctl status firewalld`

---

## 실습 3: 인스턴스 모니터링

### 3.1 CloudWatch 메트릭 확인

1. **EC2 Console에서 모니터링**
   - EC2 인스턴스 선택
   - "모니터링" 탭 클릭
   - CPU 사용률, 네트워크 트래픽 등 확인

2. **CloudWatch 대시보드 접속**
   - 서비스 → CloudWatch
   - "메트릭" → "모든 메트릭"
   - "EC2" → "인스턴스별 메트릭" 선택

3. **주요 메트릭 확인**
   - CPUUtilization: CPU 사용률
   - NetworkIn/NetworkOut: 네트워크 트래픽
   - StatusCheckFailed: 상태 확인 실패

### 3.2 인스턴스 상태 확인

1. **상태 확인**
   - EC2 인스턴스 선택
   - "상태 확인" 탭 클릭
   - 시스템 상태 확인: AWS 인프라 상태
   - 인스턴스 상태 확인: 인스턴스 소프트웨어 상태

2. **로그 확인**
   ```bash
   # 시스템 로그 확인
   sudo journalctl -u httpd
   
   # Apache 액세스 로그
   sudo tail -f /var/log/httpd/access_log
   
   # Apache 에러 로그
   sudo tail -f /var/log/httpd/error_log
   ```

### 3.3 인스턴스 메타데이터 확인

1. **메타데이터 서비스 테스트**
   ```bash
   # 인스턴스 ID 확인
   curl http://169.254.169.254/latest/meta-data/instance-id
   
   # 퍼블릭 IP 확인
   curl http://169.254.169.254/latest/meta-data/public-ipv4
   
   # 인스턴스 유형 확인
   curl http://169.254.169.254/latest/meta-data/instance-type
   
   # 보안 그룹 확인
   curl http://169.254.169.254/latest/meta-data/security-groups
   ```

---

## 실습 4: 인스턴스 관리

### 4.1 인스턴스 중지 및 시작

1. **인스턴스 중지**
   - EC2 Console에서 인스턴스 선택
   - "인스턴스 상태" → "인스턴스 중지"
   - 확인 대화상자에서 "중지" 클릭
   - 상태가 "stopping" → "stopped"로 변경 확인

2. **중지된 인스턴스 특징**
   - 퍼블릭 IP 주소 해제 (재시작 시 새 IP 할당)
   - EBS 볼륨은 유지됨
   - 컴퓨팅 요금 부과 중단

3. **인스턴스 재시작**
   - "인스턴스 상태" → "인스턴스 시작"
   - 새로운 퍼블릭 IP 주소 할당 확인
   - 웹 서버 자동 시작 확인 (enable 설정했으므로)

### 4.2 인스턴스 재부팅

1. **재부팅 실행**
   - "인스턴스 상태" → "인스턴스 재부팅"
   - 확인 대화상자에서 "재부팅" 클릭

2. **재부팅 특징**
   - 퍼블릭 IP 주소 유지
   - 빠른 재시작 (중지/시작보다 빠름)
   - 메모리 내용 초기화

### 4.3 보안 그룹 수정

1. **보안 그룹 편집**
   - 인스턴스 선택 → "보안" 탭
   - 보안 그룹 링크 클릭
   - "인바운드 규칙 편집" 클릭

2. **새 규칙 추가 예시**
   - 유형: 사용자 지정 TCP
   - 포트: 8080
   - 소스: 내 IP
   - 설명: "테스트용 포트"

3. **규칙 저장**
   - "규칙 저장" 클릭
   - 즉시 적용됨 (재부팅 불필요)

### 4.4 태그 관리

1. **태그 추가**
   - 인스턴스 선택 → "태그" 탭
   - "태그 관리" 클릭
   - "태그 추가" 클릭

2. **유용한 태그 예시**
   ```
   Environment: Development
   Project: WebServerLab
   Owner: YourName
   Purpose: Learning
   ```

3. **태그 활용**
   - 비용 추적
   - 리소스 그룹화
   - 자동화 스크립트에서 활용

---

## 실습 5: 정리 및 종료

### 5.1 데이터 백업 (선택사항)

1. **스냅샷 생성**
   - EC2 → "볼륨" 메뉴
   - 인스턴스의 루트 볼륨 선택
   - "작업" → "스냅샷 생성"
   - 설명: "WebServer Lab Snapshot"

2. **AMI 생성** (선택사항)
   - 인스턴스 선택
   - "작업" → "이미지 및 템플릿" → "이미지 생성"
   - 이미지 이름: "WebServer-Lab-AMI"

### 5.2 인스턴스 종료

⚠️ **주의**: 종료하면 인스턴스와 데이터가 영구적으로 삭제됩니다.

1. **종료 보호 해제** (설정된 경우)
   - 인스턴스 선택
   - "작업" → "인스턴스 설정" → "종료 보호 변경"
   - "비활성화" 선택

2. **인스턴스 종료**
   - "인스턴스 상태" → "인스턴스 종료"
   - 확인 대화상자에서 "종료" 클릭
   - 상태가 "shutting-down" → "terminated"로 변경

3. **관련 리소스 정리**
   - 보안 그룹: 다른 인스턴스에서 사용하지 않으면 삭제
   - 키 페어: 재사용 가능하므로 보관
   - 스냅샷: 필요없으면 삭제 (비용 발생)

---

## 문제 해결 가이드

### 일반적인 문제들

**1. SSH 연결 실패**
```
Permission denied (publickey)
```
**해결방법:**
- 키 파일 권한 확인: `chmod 400 keypair.pem`
- 올바른 사용자명 사용: `ec2-user` (Amazon Linux)
- 보안 그룹에서 SSH (포트 22) 허용 확인

**2. 웹 페이지 접속 실패**
```
This site can't be reached
```
**해결방법:**
- 보안 그룹에서 HTTP (포트 80) 허용 확인
- Apache 서비스 상태 확인: `sudo systemctl status httpd`
- 퍼블릭 IP 주소 정확성 확인

**3. 패키지 설치 실패**
```
No package httpd available
```
**해결방법:**
- 패키지 목록 업데이트: `sudo yum update -y`
- 올바른 패키지 관리자 사용 (Amazon Linux: yum, Ubuntu: apt)

**4. 권한 부족 오류**
```
Permission denied
```
**해결방법:**
- sudo 사용: `sudo command`
- 파일 권한 확인: `ls -la filename`
- 소유자 변경: `sudo chown user:group filename`

### 비용 관리 팁

**1. 인스턴스 사용 후 중지**
- 개발/테스트 완료 후 즉시 중지
- 중지 시 컴퓨팅 요금 부과 중단

**2. Free Tier 한도 모니터링**
- AWS Billing Dashboard에서 사용량 확인
- 750시간/월 한도 (t2.micro 또는 t3.micro)

**3. 불필요한 리소스 정리**
- 사용하지 않는 EBS 볼륨 삭제
- 오래된 스냅샷 정리
- 미사용 보안 그룹 삭제

---

## 실습 완료 체크리스트

### 필수 완료 항목
- [ ] EC2 인스턴스 성공적으로 생성
- [ ] SSH를 통한 인스턴스 접속 성공
- [ ] Apache 웹 서버 설치 및 실행
- [ ] 웹 브라우저에서 웹 페이지 접속 확인
- [ ] 인스턴스 중지/시작 테스트
- [ ] CloudWatch 메트릭 확인
- [ ] 실습 완료 후 인스턴스 정리

### 추가 학습 항목 (선택사항)
- [ ] 다른 인스턴스 유형으로 테스트
- [ ] 사용자 데이터 스크립트 활용
- [ ] 탄력적 IP 주소 할당
- [ ] 인스턴스 메타데이터 활용
- [ ] 보안 그룹 규칙 고급 설정

---

## 다음 단계

### Day 4 준비사항
- EBS 볼륨과 스냅샷 개념 복습
- 인스턴스 스토어 vs EBS 차이점 학습
- AMI 생성 및 활용 방법 예습

### 추가 실습 아이디어
1. **로드 밸런서 연결**: 여러 인스턴스에 트래픽 분산
2. **Auto Scaling 설정**: 트래픽에 따른 자동 확장
3. **데이터베이스 연결**: RDS와 EC2 연동
4. **모니터링 강화**: CloudWatch 알람 설정

---

**실습 완료 시간**: 약 2-3시간  
**난이도**: 초급-중급  
**예상 비용**: $0.50 이하 (Free Tier 활용 시)

🎉 **축하합니다!** EC2의 기본 기능을 성공적으로 실습했습니다. 이제 AWS의 핵심 컴퓨팅 서비스를 직접 다룰 수 있게 되었습니다!