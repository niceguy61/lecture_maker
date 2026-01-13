# Day 20 실습: CodePipeline과 CodeDeploy를 이용한 CI/CD 파이프라인 구축

## 실습 개요
이번 실습에서는 AWS CodePipeline과 CodeDeploy를 사용하여 완전한 CI/CD 파이프라인을 구축합니다. 간단한 웹 애플리케이션을 EC2 인스턴스에 자동으로 배포하는 과정을 경험해보겠습니다.

## 실습 목표
- CodeCommit 저장소 생성 및 소스 코드 업로드
- EC2 인스턴스 준비 및 CodeDeploy Agent 설치
- CodeDeploy 애플리케이션 및 배포 그룹 설정
- CodePipeline을 통한 완전한 CI/CD 파이프라인 구축
- 코드 변경 시 자동 배포 테스트

## 사전 준비사항
- AWS 계정 및 적절한 권한
- 기본적인 HTML/JavaScript 지식
- Git 사용법 숙지

## 예상 소요 시간
약 90분

---

## 단계 1: IAM 역할 생성

### 1.1 CodeDeploy 서비스 역할 생성

1. **AWS Management Console**에 로그인
2. **IAM** 서비스로 이동
3. 왼쪽 메뉴에서 **"역할"** 클릭
4. **"역할 만들기"** 버튼 클릭

**신뢰할 수 있는 엔터티 선택:**
- **"AWS 서비스"** 선택
- **"CodeDeploy"** 선택
- **"CodeDeploy"** (EC2/온프레미스용) 선택
- **"다음"** 클릭

**권한 정책 연결:**
- **"AWSCodeDeployRole"** 정책 선택
- **"다음"** 클릭

**역할 세부 정보:**
- **역할 이름**: `CodeDeployServiceRole`
- **설명**: `CodeDeploy service role for EC2 deployments`
- **"역할 만들기"** 클릭

### 1.2 EC2 인스턴스 역할 생성

1. **"역할 만들기"** 다시 클릭

**신뢰할 수 있는 엔터티 선택:**
- **"AWS 서비스"** 선택
- **"EC2"** 선택
- **"다음"** 클릭

**권한 정책 연결:**
- **"AmazonEC2RoleforAWSCodeDeploy"** 정책 선택
- **"AmazonS3ReadOnlyAccess"** 정책 선택 (배포 아티팩트 다운로드용)
- **"다음"** 클릭

**역할 세부 정보:**
- **역할 이름**: `EC2CodeDeployRole`
- **설명**: `EC2 instance role for CodeDeploy`
- **"역할 만들기"** 클릭

### 1.3 CodePipeline 서비스 역할 생성

1. **"역할 만들기"** 다시 클릭

**신뢰할 수 있는 엔터티 선택:**
- **"AWS 서비스"** 선택
- **"CodePipeline"** 선택
- **"다음"** 클릭

**권한 정책 연결:**
- **"AWSCodePipelineServiceRole"** 정책 선택
- **"다음"** 클릭

**역할 세부 정보:**
- **역할 이름**: `CodePipelineServiceRole`
- **설명**: `CodePipeline service role`
- **"역할 만들기"** 클릭

---

## 단계 2: EC2 인스턴스 준비

### 2.1 EC2 인스턴스 시작

1. **EC2** 서비스로 이동
2. **"인스턴스 시작"** 클릭

**인스턴스 구성:**
- **이름**: `CodeDeploy-WebServer`
- **AMI**: Amazon Linux 2023 AMI
- **인스턴스 유형**: t2.micro (프리 티어)
- **키 페어**: 기존 키 페어 선택 또는 새로 생성

**네트워크 설정:**
- **VPC**: 기본 VPC 사용
- **서브넷**: 퍼블릭 서브넷 선택
- **퍼블릭 IP 자동 할당**: 활성화

**보안 그룹 설정:**
- **보안 그룹 이름**: `CodeDeploy-WebServer-SG`
- **규칙 추가**:
  - SSH (포트 22): 내 IP
  - HTTP (포트 80): 0.0.0.0/0
  - HTTPS (포트 443): 0.0.0.0/0

**고급 세부 정보:**
- **IAM 인스턴스 프로파일**: `EC2CodeDeployRole` 선택

**사용자 데이터** (고급 세부 정보 섹션에서):
```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# CodeDeploy Agent 설치
yum install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
chmod +x ./install
./install auto

# CodeDeploy Agent 시작
service codedeploy-agent start
chkconfig codedeploy-agent on
```

3. **"인스턴스 시작"** 클릭

### 2.2 인스턴스 태그 설정

1. 생성된 인스턴스 선택
2. **"작업"** → **"인스턴스 설정"** → **"태그 관리"** 클릭
3. **"태그 추가"** 클릭:
   - **키**: `Environment`
   - **값**: `Development`
4. **"저장"** 클릭

---

## 단계 3: CodeCommit 저장소 생성

### 3.1 저장소 생성

1. **CodeCommit** 서비스로 이동
2. **"리포지토리 생성"** 클릭

**저장소 설정:**
- **리포지토리 이름**: `my-web-app`
- **설명**: `Simple web application for CodeDeploy demo`
- **"생성"** 클릭

### 3.2 로컬 Git 설정 (Cloud9 또는 로컬 환경)

**Git 자격 증명 설정:**
1. **IAM** → **사용자** → 본인 사용자 선택
2. **보안 자격 증명** 탭
3. **AWS CodeCommit에 대한 HTTPS Git 자격 증명** 섹션
4. **"자격 증명 생성"** 클릭
5. 생성된 사용자 이름과 암호 저장

**저장소 클론:**
```bash
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/my-web-app
cd my-web-app
```

### 3.3 샘플 애플리케이션 생성

**index.html 파일 생성:**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Web App</title>
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
            color: #333;
            text-align: center;
        }
        .version {
            background-color: #007bff;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Web App!</h1>
        <div class="version">Version 1.0</div>
        <p>이 애플리케이션은 AWS CodePipeline과 CodeDeploy를 통해 자동으로 배포되었습니다.</p>
        <p>배포 시간: <span id="deployTime"></span></p>
    </div>
    
    <script>
        document.getElementById('deployTime').textContent = new Date().toLocaleString('ko-KR');
    </script>
</body>
</html>
```

**appspec.yml 파일 생성 (CodeDeploy 배포 명세서):**
```yaml
version: 0.0
os: linux
files:
  - source: /
    destination: /var/www/html
    overwrite: yes
permissions:
  - object: /var/www/html
    owner: apache
    group: apache
    mode: 755
hooks:
  BeforeInstall:
    - location: scripts/install_dependencies.sh
      timeout: 300
      runas: root
  ApplicationStart:
    - location: scripts/start_server.sh
      timeout: 300
      runas: root
  ApplicationStop:
    - location: scripts/stop_server.sh
      timeout: 300
      runas: root
```

**scripts 디렉토리 및 스크립트 파일들 생성:**

```bash
mkdir scripts
```

**scripts/install_dependencies.sh:**
```bash
#!/bin/bash
yum update -y
yum install -y httpd
```

**scripts/start_server.sh:**
```bash
#!/bin/bash
systemctl start httpd
systemctl enable httpd
```

**scripts/stop_server.sh:**
```bash
#!/bin/bash
systemctl stop httpd
```

**스크립트 파일들에 실행 권한 부여:**
```bash
chmod +x scripts/*.sh
```

**Git에 커밋 및 푸시:**
```bash
git add .
git commit -m "Initial commit: Simple web application"
git push origin main
```

---

## 단계 4: CodeDeploy 애플리케이션 설정

### 4.1 애플리케이션 생성

1. **CodeDeploy** 서비스로 이동
2. **"애플리케이션 생성"** 클릭

**애플리케이션 설정:**
- **애플리케이션 이름**: `MyWebApp`
- **컴퓨팅 플랫폼**: `EC2/온프레미스`
- **"애플리케이션 생성"** 클릭

### 4.2 배포 그룹 생성

1. 생성된 애플리케이션에서 **"배포 그룹 생성"** 클릭

**배포 그룹 설정:**
- **배포 그룹 이름**: `MyWebApp-DeploymentGroup`
- **서비스 역할**: `CodeDeployServiceRole` 선택

**배포 유형:**
- **현재 위치** 선택 (In-place deployment)

**환경 구성:**
- **Amazon EC2 인스턴스** 선택
- **태그 그룹**:
  - **키**: `Environment`
  - **값**: `Development`

**배포 설정:**
- **배포 구성**: `CodeDeployDefault.AllAtOnce` 선택

**로드 밸런서:**
- **로드 밸런싱 활성화** 체크 해제

**고급 옵션:**
- **Amazon CloudWatch 알람**: 비활성화
- **자동 롤백**: 활성화
  - **배포 실패 시 롤백** 체크
  - **알람 임계값 충족 시 롤백** 체크 해제

2. **"배포 그룹 생성"** 클릭

---

## 단계 5: CodePipeline 생성

### 5.1 파이프라인 생성

1. **CodePipeline** 서비스로 이동
2. **"파이프라인 생성"** 클릭

**1단계: 파이프라인 설정 선택**
- **파이프라인 이름**: `MyWebApp-Pipeline`
- **서비스 역할**: `새 서비스 역할` 선택
- **역할 이름**: `AWSCodePipelineServiceRole-us-east-1-MyWebApp-Pipeline` (자동 생성)
- **고급 설정**:
  - **아티팩트 스토어**: `기본 위치` 선택
- **"다음"** 클릭

**2단계: 소스 스테이지 추가**
- **소스 공급자**: `AWS CodeCommit` 선택
- **리포지토리 이름**: `my-web-app` 선택
- **브랜치 이름**: `main`
- **변경 감지 옵션**: `Amazon CloudWatch Events` 선택 (권장)
- **"다음"** 클릭

**3단계: 빌드 스테이지 추가**
- **"빌드 스테이지 건너뛰기"** 클릭 (단순한 정적 웹사이트이므로)
- 확인 대화상자에서 **"건너뛰기"** 클릭

**4단계: 배포 스테이지 추가**
- **배포 공급자**: `AWS CodeDeploy` 선택
- **리전**: `US East (N. Virginia)` (현재 리전)
- **애플리케이션 이름**: `MyWebApp` 선택
- **배포 그룹**: `MyWebApp-DeploymentGroup` 선택
- **"다음"** 클릭

**5단계: 검토**
- 설정 내용 확인
- **"파이프라인 생성"** 클릭

### 5.2 첫 번째 배포 확인

파이프라인이 생성되면 자동으로 첫 번째 실행이 시작됩니다:

1. **소스** 스테이지: CodeCommit에서 소스 코드 가져오기
2. **배포** 스테이지: CodeDeploy를 통해 EC2 인스턴스에 배포

각 스테이지의 진행 상황을 실시간으로 확인할 수 있습니다.

---

## 단계 6: 배포 결과 확인

### 6.1 웹 애플리케이션 접속

1. **EC2** 콘솔로 이동
2. 인스턴스의 **퍼블릭 IPv4 주소** 복사
3. 웹 브라우저에서 `http://[퍼블릭-IP-주소]` 접속
4. "Welcome to My Web App!" 페이지가 표시되는지 확인

### 6.2 CodeDeploy 배포 상세 정보 확인

1. **CodeDeploy** 콘솔로 이동
2. **애플리케이션** → `MyWebApp` 클릭
3. **배포** 탭에서 최근 배포 클릭
4. 배포 세부 정보 및 로그 확인:
   - 배포 상태
   - 각 라이프사이클 이벤트 실행 결과
   - 인스턴스별 배포 상태

---

## 단계 7: 자동 배포 테스트

### 7.1 코드 변경

로컬 환경에서 `index.html` 파일 수정:

```html
<!-- Version 1.0을 Version 2.0으로 변경 -->
<div class="version">Version 2.0</div>

<!-- 새로운 기능 추가 -->
<div style="background-color: #28a745; color: white; padding: 10px; border-radius: 5px; margin: 20px 0; text-align: center;">
    🎉 새로운 기능이 추가되었습니다!
</div>
```

### 7.2 변경사항 커밋 및 푸시

```bash
git add index.html
git commit -m "Update to version 2.0 with new feature"
git push origin main
```

### 7.3 자동 배포 확인

1. **CodePipeline** 콘솔에서 파이프라인 실행 상태 확인
2. CloudWatch Events에 의해 자동으로 파이프라인이 트리거되는지 확인
3. 배포 완료 후 웹사이트에서 변경사항 확인

---

## 단계 8: 모니터링 및 로깅

### 8.1 CloudWatch 로그 확인

1. **CloudWatch** 서비스로 이동
2. **로그** → **로그 그룹** 클릭
3. CodeDeploy 관련 로그 그룹 확인:
   - `/aws/codedeploy-agent/codedeploy-agent.log`
   - `/aws/codepipeline/MyWebApp-Pipeline`

### 8.2 파이프라인 실행 기록

1. **CodePipeline** 콘솔에서 **실행 기록** 탭 확인
2. 각 실행의 세부 정보 및 소요 시간 분석
3. 실패한 실행이 있다면 오류 로그 확인

---

## 단계 9: 고급 기능 실습 (선택사항)

### 9.1 Blue/Green 배포 설정

1. **CodeDeploy** 애플리케이션에서 새 배포 그룹 생성
2. **배포 유형**: `Blue/Green` 선택
3. **환경 구성**: Auto Scaling 그룹 또는 EC2 태그 사용
4. **로드 밸런서**: Application Load Balancer 설정

### 9.2 승인 단계 추가

1. **CodePipeline** 편집
2. 배포 스테이지 전에 **수동 승인** 액션 추가
3. **SNS 주제** 설정으로 승인 요청 알림 구성

### 9.3 테스트 스테이지 추가

1. **CodeBuild** 프로젝트 생성
2. 간단한 테스트 스크립트 작성
3. 파이프라인에 테스트 스테이지 추가

---

## 문제 해결

### 일반적인 문제들

**1. CodeDeploy Agent가 설치되지 않음**
```bash
# EC2 인스턴스에 SSH 접속 후 확인
sudo service codedeploy-agent status

# 수동 설치
sudo yum install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent start
```

**2. 권한 오류**
- IAM 역할과 정책이 올바르게 설정되었는지 확인
- EC2 인스턴스에 올바른 IAM 역할이 연결되었는지 확인

**3. 배포 실패**
- appspec.yml 파일 구문 확인
- 스크립트 파일의 실행 권한 확인
- CodeDeploy 로그 확인: `/opt/codedeploy-agent/deployment-root/deployment-logs/`

**4. 파이프라인 실행 실패**
- 각 스테이지의 오류 로그 확인
- 서비스 역할 권한 확인
- 아티팩트 스토어 S3 버킷 권한 확인

---

## 정리 및 리소스 삭제

실습 완료 후 비용 절약을 위해 다음 리소스들을 삭제하세요:

1. **CodePipeline** 파이프라인 삭제
2. **CodeDeploy** 애플리케이션 삭제
3. **CodeCommit** 저장소 삭제
4. **EC2** 인스턴스 종료
5. **IAM** 역할 삭제 (다른 서비스에서 사용하지 않는 경우)
6. **S3** 아티팩트 버킷 삭제 (CodePipeline이 생성한 버킷)

---

## 실습 완료 체크리스트

- [ ] IAM 역할 3개 생성 완료
- [ ] EC2 인스턴스 생성 및 CodeDeploy Agent 설치 완료
- [ ] CodeCommit 저장소 생성 및 소스 코드 업로드 완료
- [ ] CodeDeploy 애플리케이션 및 배포 그룹 설정 완료
- [ ] CodePipeline 생성 및 첫 번째 배포 성공
- [ ] 웹 애플리케이션 정상 접속 확인
- [ ] 코드 변경 후 자동 배포 테스트 완료
- [ ] CloudWatch 로그 확인 완료
- [ ] 리소스 정리 완료

## 추가 학습 자료

- [AWS CodePipeline 사용자 가이드](https://docs.aws.amazon.com/codepipeline/)
- [AWS CodeDeploy 사용자 가이드](https://docs.aws.amazon.com/codedeploy/)
- [AWS CodeCommit 사용자 가이드](https://docs.aws.amazon.com/codecommit/)
- [CI/CD 모범 사례](https://aws.amazon.com/devops/continuous-integration/)

이번 실습을 통해 AWS의 완전 관리형 CI/CD 서비스들을 활용하여 자동화된 배포 파이프라인을 구축하는 방법을 학습했습니다. 이러한 도구들은 현대적인 소프트웨어 개발에서 필수적인 DevOps 문화를 구현하는 데 핵심적인 역할을 합니다.