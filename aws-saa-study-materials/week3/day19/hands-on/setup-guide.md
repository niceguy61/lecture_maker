# Day 19 실습: ECS 클러스터 및 서비스 생성

## 🎯 실습 목표

이번 실습에서는 AWS ECS를 사용하여 컨테이너 기반 웹 애플리케이션을 배포해보겠습니다. Fargate를 사용하여 서버리스 방식으로 컨테이너를 실행하고, 로드 밸런서를 통해 외부에서 접근할 수 있도록 설정하겠습니다.

## 📋 사전 준비사항

- AWS 계정 및 적절한 권한
- 기본적인 Docker 개념 이해
- VPC 및 서브넷에 대한 기본 지식

## 🏗️ 실습 아키텍처

```
Internet Gateway
       |
   Public ALB
       |
   ECS Service (Fargate)
       |
   Private Subnets
```

## 📝 실습 단계

### 1단계: ECS 클러스터 생성

#### 1.1 ECS 콘솔 접속
1. AWS Management Console에 로그인
2. 서비스 검색에서 "ECS" 입력 후 선택
3. **"Elastic Container Service"** 클릭

#### 1.2 클러스터 생성
1. 좌측 메뉴에서 **"Clusters"** 클릭
2. **"Create Cluster"** 버튼 클릭
3. 클러스터 설정:
   - **Cluster name**: `day19-ecs-cluster`
   - **Infrastructure**: `AWS Fargate (serverless)` 선택
   - **Monitoring**: CloudWatch Container Insights 체크
4. **"Create"** 버튼 클릭

> 💡 **팁**: Fargate를 선택하면 EC2 인스턴스를 관리할 필요가 없어 더 간단합니다.

#### 1.3 클러스터 생성 확인
- 클러스터 상태가 **"ACTIVE"**가 될 때까지 대기 (약 1-2분)
- 클러스터 세부 정보에서 **"Infrastructure"** 탭 확인

### 2단계: Task Definition 생성

#### 2.1 Task Definition 생성 시작
1. 좌측 메뉴에서 **"Task definitions"** 클릭
2. **"Create new task definition"** 버튼 클릭

#### 2.2 기본 설정
1. **Task definition family**: `day19-web-app`
2. **Launch type**: `AWS Fargate` 선택
3. **Operating system/Architecture**: `Linux/X86_64`
4. **Task size**:
   - **CPU**: `0.25 vCPU`
   - **Memory**: `0.5 GB`

#### 2.3 컨테이너 정의
1. **Container details** 섹션에서:
   - **Name**: `web-container`
   - **Image URI**: `nginx:latest`
   - **Port mappings**:
     - **Container port**: `80`
     - **Protocol**: `TCP`
     - **Port name**: `web-port`
     - **App protocol**: `HTTP`

#### 2.4 환경 설정
1. **Environment variables** (선택사항):
   - **Key**: `ENV`
   - **Value**: `production`

2. **Logging** 설정:
   - **Log driver**: `awslogs` (기본값)
   - **Log group**: 자동 생성 허용

#### 2.5 Task Definition 생성 완료
1. 설정 검토 후 **"Create"** 버튼 클릭
2. 생성 완료 메시지 확인

### 3단계: Application Load Balancer 생성

#### 3.1 EC2 콘솔로 이동
1. 서비스 검색에서 **"EC2"** 입력 후 선택
2. 좌측 메뉴에서 **"Load Balancers"** 클릭

#### 3.2 로드 밸런서 생성
1. **"Create Load Balancer"** 버튼 클릭
2. **"Application Load Balancer"** 선택 후 **"Create"** 클릭

#### 3.3 기본 설정
1. **Load balancer name**: `day19-alb`
2. **Scheme**: `Internet-facing`
3. **IP address type**: `IPv4`

#### 3.4 네트워크 매핑
1. **VPC**: 기본 VPC 선택
2. **Mappings**: 최소 2개의 가용 영역 선택
   - 각 AZ에서 퍼블릭 서브넷 선택

#### 3.5 보안 그룹 설정
1. **Security groups**:
   - 새 보안 그룹 생성 또는 기존 그룹 선택
   - HTTP (포트 80) 인바운드 규칙 확인

#### 3.6 리스너 및 라우팅
1. **Listeners and routing**:
   - **Protocol**: `HTTP`
   - **Port**: `80`
2. **Default action**:
   - **"Create target group"** 클릭
   - **Target group name**: `day19-tg`
   - **Target type**: `IP addresses`
   - **Protocol**: `HTTP`
   - **Port**: `80`
   - **VPC**: 기본 VPC 선택
   - **Health check path**: `/`

#### 3.7 로드 밸런서 생성 완료
1. 설정 검토 후 **"Create load balancer"** 클릭
2. 생성 완료까지 대기 (약 2-3분)

### 4단계: ECS 서비스 생성

#### 4.1 ECS 콘솔로 돌아가기
1. ECS 콘솔로 이동
2. 생성한 클러스터 (`day19-ecs-cluster`) 클릭

#### 4.2 서비스 생성 시작
1. **"Services"** 탭 클릭
2. **"Create"** 버튼 클릭

#### 4.3 환경 설정
1. **Environment**:
   - **Compute options**: `Launch type`
   - **Launch type**: `FARGATE`
   - **Platform version**: `LATEST`

#### 4.4 배포 설정
1. **Deployment configuration**:
   - **Application type**: `Service`
   - **Family**: `day19-web-app` (앞서 생성한 Task Definition)
   - **Revision**: `LATEST`
   - **Service name**: `day19-web-service`
   - **Desired tasks**: `2`

#### 4.5 네트워킹 설정
1. **Networking**:
   - **VPC**: 기본 VPC 선택
   - **Subnets**: 프라이빗 서브넷 선택 (가능한 경우)
   - **Security group**: 새로 생성
     - **Security group name**: `day19-ecs-sg`
     - **Inbound rules**: HTTP (80) from ALB 보안 그룹
   - **Public IP**: `ENABLED` (프라이빗 서브넷이 없는 경우)

#### 4.6 로드 밸런싱 설정
1. **Load balancing**:
   - **Load balancer type**: `Application Load Balancer`
   - **Load balancer**: `day19-alb` (앞서 생성한 ALB)
   - **Listener**: `80:HTTP`
   - **Target group**: `day19-tg`

#### 4.7 서비스 자동 스케일링 (선택사항)
1. **Service auto scaling**:
   - **Use service auto scaling**: 체크
   - **Minimum number of tasks**: `1`
   - **Maximum number of tasks**: `4`
   - **Target tracking scaling policies**:
     - **Policy name**: `cpu-scaling`
     - **ECS service metric**: `ECSServiceAverageCPUUtilization`
     - **Target value**: `70`

#### 4.8 서비스 생성 완료
1. 설정 검토 후 **"Create"** 버튼 클릭
2. 서비스 생성 및 태스크 시작 대기 (약 3-5분)

### 5단계: 배포 확인 및 테스트

#### 5.1 서비스 상태 확인
1. ECS 서비스 페이지에서 **"Tasks"** 탭 확인
2. 모든 태스크가 **"RUNNING"** 상태인지 확인
3. **"Health status"**가 **"HEALTHY"**인지 확인

#### 5.2 로드 밸런서 DNS 확인
1. EC2 콘솔의 Load Balancers로 이동
2. `day19-alb` 선택
3. **"DNS name"** 복사

#### 5.3 애플리케이션 접속 테스트
1. 웹 브라우저에서 ALB DNS 주소 접속
2. Nginx 기본 페이지 확인
3. 여러 번 새로고침하여 로드 밸런싱 동작 확인

### 6단계: 모니터링 설정

#### 6.1 CloudWatch 대시보드 확인
1. CloudWatch 콘솔로 이동
2. **"Container Insights"** 메뉴 클릭
3. **"Performance monitoring"** 선택
4. 클러스터: `day19-ecs-cluster` 선택

#### 6.2 주요 메트릭 확인
- **CPU Utilization**
- **Memory Utilization**
- **Network I/O**
- **Task count**

#### 6.3 로그 확인
1. CloudWatch Logs로 이동
2. 로그 그룹: `/ecs/day19-web-app` 확인
3. 컨테이너 로그 스트림 확인

### 7단계: 스케일링 테스트 (선택사항)

#### 7.1 수동 스케일링
1. ECS 서비스 페이지로 이동
2. **"Update service"** 클릭
3. **"Desired tasks"**를 `4`로 변경
4. 업데이트 후 태스크 증가 확인

#### 7.2 자동 스케일링 테스트
1. 부하 테스트 도구 사용 (예: Apache Bench)
```bash
# 로컬에서 실행 (선택사항)
ab -n 1000 -c 10 http://[ALB-DNS-NAME]/
```
2. CloudWatch에서 CPU 사용률 증가 확인
3. 자동 스케일링 동작 확인

## 🧹 리소스 정리

실습 완료 후 비용 절약을 위해 다음 순서로 리소스를 삭제하세요:

### 1. ECS 서비스 삭제
1. ECS 콘솔에서 서비스 선택
2. **"Delete"** 클릭
3. 확인 후 삭제

### 2. ECS 클러스터 삭제
1. 모든 서비스가 삭제된 후 클러스터 삭제
2. **"Delete Cluster"** 클릭

### 3. 로드 밸런서 삭제
1. EC2 콘솔에서 로드 밸런서 선택
2. **"Actions"** → **"Delete"**

### 4. 타겟 그룹 삭제
1. 타겟 그룹 선택 후 삭제

### 5. 보안 그룹 정리
1. 사용하지 않는 보안 그룹 삭제

## 🔍 트러블슈팅

### 일반적인 문제와 해결방법

#### 1. 태스크가 시작되지 않는 경우
- **원인**: 보안 그룹 설정 문제
- **해결**: ECS 태스크 보안 그룹에서 필요한 포트 허용

#### 2. 로드 밸런서에서 503 오류
- **원인**: 타겟 그룹 헬스 체크 실패
- **해결**: 헬스 체크 경로 및 포트 설정 확인

#### 3. 인터넷 접속 불가
- **원인**: 퍼블릭 IP 미할당 또는 라우팅 문제
- **해결**: 퍼블릭 서브넷 사용 또는 NAT Gateway 설정

#### 4. 컨테이너 이미지 풀 실패
- **원인**: ECR 권한 또는 네트워크 문제
- **해결**: Task Role에 ECR 권한 추가

## 📊 실습 결과 확인

### 성공 기준
- [ ] ECS 클러스터가 ACTIVE 상태
- [ ] Task Definition이 정상 생성
- [ ] ECS 서비스가 원하는 태스크 수 유지
- [ ] 모든 태스크가 RUNNING 상태
- [ ] ALB를 통한 웹 페이지 접속 가능
- [ ] CloudWatch에서 메트릭 확인 가능

### 학습 포인트
1. **ECS 구성 요소 이해**: 클러스터, 서비스, 태스크의 관계
2. **Fargate 활용**: 서버리스 컨테이너 실행
3. **로드 밸런싱**: ALB와 ECS 서비스 연동
4. **모니터링**: CloudWatch Container Insights 활용
5. **스케일링**: 수동 및 자동 스케일링 설정

## 🎯 추가 실습 아이디어

### 1. 커스텀 애플리케이션 배포
- 간단한 Node.js 또는 Python 웹 앱 컨테이너화
- ECR에 이미지 푸시 후 ECS에서 실행

### 2. 블루/그린 배포
- CodeDeploy를 사용한 무중단 배포 설정

### 3. 서비스 디스커버리
- AWS Cloud Map을 사용한 서비스 간 통신

### 4. 시크릿 관리
- AWS Secrets Manager와 ECS 통합

이번 실습을 통해 AWS ECS의 핵심 개념과 실제 운영 방법을 익혔습니다. 다음 단계로는 더 복잡한 마이크로서비스 아키텍처나 CI/CD 파이프라인 구축을 시도해보세요!