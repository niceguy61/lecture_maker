# Day 15 실습: Application Load Balancer와 Auto Scaling Group 구성

## 실습 개요

이번 실습에서는 AWS Console을 사용하여 Application Load Balancer(ALB)와 Auto Scaling Group을 구성하고 연동하는 방법을 학습합니다. 실제 웹 애플리케이션 환경에서 고가용성과 확장성을 구현하는 실무 경험을 쌓을 수 있습니다.

## 실습 목표

- Application Load Balancer 생성 및 구성
- Launch Template 생성
- Auto Scaling Group 생성 및 정책 설정
- ALB와 ASG 연동 확인
- 부하 테스트를 통한 Auto Scaling 동작 검증

## 사전 준비사항

### 필요한 리소스
- AWS 계정 (Free Tier 사용 가능)
- 기본 VPC 또는 사용자 정의 VPC
- 최소 2개의 가용 영역 (AZ)
- EC2 Key Pair

### 예상 비용
- ALB: 시간당 약 $0.0225 (Free Tier 750시간/월 제공)
- EC2 인스턴스: t2.micro 시간당 약 $0.0116 (Free Tier 750시간/월 제공)
- 데이터 전송: 15GB/월까지 무료

## 실습 1: Launch Template 생성

### 1.1 EC2 콘솔 접속

1. AWS Management Console에 로그인
2. 서비스 메뉴에서 **EC2** 선택
3. 좌측 메뉴에서 **Launch Templates** 클릭

### 1.2 Launch Template 생성

1. **Create launch template** 버튼 클릭

2. **Launch template name and description** 섹션:
   ```
   Launch template name: web-server-template
   Template version description: Web server template for ALB demo
   ```

3. **Application and OS Images (Amazon Machine Image)** 섹션:
   - **Quick Start** 탭 선택
   - **Amazon Linux** 선택
   - **Amazon Linux 2023 AMI** 선택 (Free tier eligible)

4. **Instance type** 섹션:
   - **t2.micro** 선택 (Free tier eligible)

5. **Key pair (login)** 섹션:
   - 기존 Key pair 선택 또는 새로 생성
   - 새로 생성하는 경우: **Create new key pair** 클릭

6. **Network settings** 섹션:
   - **Subnet**: Don't include in launch template (ASG에서 지정)
   - **Firewall (security groups)**: Create security group
   - **Security group name**: web-server-sg
   - **Description**: Security group for web servers
   - **Inbound Security Group Rules**:
     ```
     Type: HTTP
     Protocol: TCP
     Port Range: 80
     Source: 0.0.0.0/0
     
     Type: SSH
     Protocol: TCP
     Port Range: 22
     Source: My IP
     ```

7. **Advanced details** 섹션 확장:
   - **User data** 필드에 다음 스크립트 입력:
   ```bash
   #!/bin/bash
   yum update -y
   yum install -y httpd
   systemctl start httpd
   systemctl enable httpd
   
   # 간단한 웹 페이지 생성
   cat > /var/www/html/index.html << 'EOF'
   <!DOCTYPE html>
   <html>
   <head>
       <title>Web Server</title>
       <style>
           body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
           .container { max-width: 600px; margin: 0 auto; padding: 20px; }
           .server-info { background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }
       </style>
   </head>
   <body>
       <div class="container">
           <h1>🚀 AWS Load Balancer Demo</h1>
           <div class="server-info">
               <h3>Server Information</h3>
               <p><strong>Instance ID:</strong> <span id="instance-id">Loading...</span></p>
               <p><strong>Availability Zone:</strong> <span id="az">Loading...</span></p>
               <p><strong>Local IP:</strong> <span id="local-ip">Loading...</span></p>
               <p><strong>Timestamp:</strong> <span id="timestamp"></span></p>
           </div>
           <button onclick="location.reload()">🔄 Refresh</button>
       </div>
       
       <script>
           // 서버 정보 가져오기
           fetch('http://169.254.169.254/latest/meta-data/instance-id')
               .then(response => response.text())
               .then(data => document.getElementById('instance-id').textContent = data);
               
           fetch('http://169.254.169.254/latest/meta-data/placement/availability-zone')
               .then(response => response.text())
               .then(data => document.getElementById('az').textContent = data);
               
           fetch('http://169.254.169.254/latest/meta-data/local-ipv4')
               .then(response => response.text())
               .then(data => document.getElementById('local-ip').textContent = data);
               
           document.getElementById('timestamp').textContent = new Date().toLocaleString();
       </script>
   </body>
   </html>
   EOF
   
   # 부하 테스트용 엔드포인트 생성
   cat > /var/www/html/load.html << 'EOF'
   <!DOCTYPE html>
   <html>
   <head><title>Load Test</title></head>
   <body>
       <h1>Load Test Page</h1>
       <p>This page simulates CPU load for testing Auto Scaling.</p>
       <script>
           // CPU 부하 생성 (테스트용)
           function generateLoad() {
               const start = Date.now();
               while (Date.now() - start < 1000) {
                   Math.random();
               }
           }
           
           // 10초간 부하 생성
           for (let i = 0; i < 10; i++) {
               setTimeout(generateLoad, i * 1000);
           }
       </script>
   </body>
   </html>
   EOF
   ```

8. **Create launch template** 버튼 클릭

### 1.3 Launch Template 확인

생성된 Launch Template의 세부 정보를 확인하고 **Actions** > **View details**로 설정을 검토합니다.

## 실습 2: Application Load Balancer 생성

### 2.1 Load Balancer 생성 시작

1. EC2 콘솔 좌측 메뉴에서 **Load Balancers** 클릭
2. **Create Load Balancer** 버튼 클릭
3. **Application Load Balancer** 섹션에서 **Create** 버튼 클릭

### 2.2 기본 구성

1. **Load balancer name**: `web-app-alb`
2. **Scheme**: Internet-facing
3. **IP address type**: IPv4

### 2.3 네트워크 매핑

1. **VPC**: 기본 VPC 선택
2. **Mappings**: 최소 2개의 가용 영역 선택
   - 각 AZ에서 public subnet 선택
   - 예: us-east-1a, us-east-1b

### 2.4 보안 그룹

1. **Security groups** 섹션:
   - **Create new security group** 선택
   - **Security group name**: `alb-sg`
   - **Description**: `Security group for ALB`
   - **Inbound rules**:
     ```
     Type: HTTP
     Protocol: TCP
     Port: 80
     Source: 0.0.0.0/0
     
     Type: HTTPS
     Protocol: TCP
     Port: 443
     Source: 0.0.0.0/0
     ```

### 2.5 리스너 및 라우팅

1. **Listeners and routing** 섹션:
   - **Protocol**: HTTP
   - **Port**: 80
   - **Default action**: Create target group

2. **Create target group** 창에서:
   ```
   Target type: Instances
   Target group name: web-servers-tg
   Protocol: HTTP
   Port: 80
   VPC: (기본 VPC 선택)
   ```

3. **Health checks** 섹션:
   ```
   Health check protocol: HTTP
   Health check path: /
   Health check port: Traffic port
   Healthy threshold: 2
   Unhealthy threshold: 2
   Timeout: 5 seconds
   Interval: 30 seconds
   Success codes: 200
   ```

4. **Create target group** 버튼 클릭

5. ALB 생성 페이지로 돌아가서 **Refresh** 버튼 클릭 후 생성한 target group 선택

### 2.6 ALB 생성 완료

1. **Create load balancer** 버튼 클릭
2. 생성 완료까지 약 2-3분 대기
3. **State**가 **Active**가 될 때까지 기다림

## 실습 3: Auto Scaling Group 생성

### 3.1 Auto Scaling Group 생성 시작

1. EC2 콘솔 좌측 메뉴에서 **Auto Scaling Groups** 클릭
2. **Create Auto Scaling group** 버튼 클릭

### 3.2 Step 1: Launch template 선택

1. **Auto Scaling group name**: `web-servers-asg`
2. **Launch template**: 앞서 생성한 `web-server-template` 선택
3. **Version**: Default (1)
4. **Next** 버튼 클릭

### 3.3 Step 2: 인스턴스 시작 옵션 선택

1. **Network** 섹션:
   - **VPC**: 기본 VPC 선택
   - **Availability Zones and subnets**: ALB와 동일한 AZ의 public subnet 선택

2. **Instance type requirements** (선택사항):
   - **Override launch template**: 체크하지 않음

3. **Next** 버튼 클릭

### 3.4 Step 3: 고급 옵션 구성

1. **Load balancing** 섹션:
   - **Attach to an existing load balancer** 선택
   - **Choose from your load balancer target groups** 선택
   - **Existing load balancer target groups**: `web-servers-tg` 선택

2. **Health checks** 섹션:
   - **Health check type**: ELB
   - **Health check grace period**: 300 seconds

3. **Additional settings** 섹션:
   - **Enable group metrics collection within CloudWatch** 체크

4. **Next** 버튼 클릭

### 3.5 Step 4: 그룹 크기 및 확장 정책 구성

1. **Group size** 섹션:
   ```
   Desired capacity: 2
   Minimum capacity: 1
   Maximum capacity: 6
   ```

2. **Scaling policies** 섹션:
   - **Target tracking scaling policy** 선택
   - **Scaling policy name**: `cpu-target-tracking`
   - **Metric type**: Average CPU utilization
   - **Target value**: 70
   - **Instance warmup**: 300 seconds

3. **Instance scale-in protection**: 체크하지 않음

4. **Next** 버튼 클릭

### 3.6 Step 5: 알림 추가 (선택사항)

1. 이번 실습에서는 건너뛰기
2. **Next** 버튼 클릭

### 3.7 Step 6: 태그 추가

1. **Add tag** 버튼 클릭:
   ```
   Key: Name
   Value: WebServer-ASG
   Tag new instances: 체크
   ```

2. **Next** 버튼 클릭

### 3.8 Step 7: 검토 및 생성

1. 모든 설정 검토
2. **Create Auto Scaling group** 버튼 클릭

## 실습 4: 동작 확인 및 테스트

### 4.1 인스턴스 시작 확인

1. **Auto Scaling Groups** 페이지에서 생성한 ASG 선택
2. **Instance management** 탭에서 인스턴스 상태 확인
3. **Activity** 탭에서 활동 로그 확인

### 4.2 Load Balancer 동작 확인

1. **Load Balancers** 페이지에서 생성한 ALB 선택
2. **Description** 탭에서 **DNS name** 복사
3. 웹 브라우저에서 DNS name으로 접속
4. 새로고침할 때마다 다른 인스턴스로 연결되는지 확인

### 4.3 Target Group 상태 확인

1. **Target Groups** 페이지에서 `web-servers-tg` 선택
2. **Targets** 탭에서 인스턴스 상태 확인
3. 모든 인스턴스가 **healthy** 상태인지 확인

## 실습 5: Auto Scaling 테스트

### 5.1 CloudWatch 메트릭 확인

1. CloudWatch 콘솔로 이동
2. **Metrics** > **All metrics** 선택
3. **AWS/ApplicationELB** 메트릭 확인:
   - RequestCount
   - TargetResponseTime
   - HealthyHostCount

4. **AWS/AutoScaling** 메트릭 확인:
   - GroupDesiredCapacity
   - GroupInServiceInstances

### 5.2 부하 테스트 수행

#### 방법 1: 간단한 부하 테스트

1. 터미널에서 다음 명령어 실행 (ALB DNS 이름으로 교체):
```bash
# 반복적으로 요청 보내기
for i in {1..1000}; do
  curl -s http://your-alb-dns-name.region.elb.amazonaws.com/ > /dev/null
  echo "Request $i completed"
  sleep 0.1
done
```

#### 방법 2: 웹 브라우저 부하 테스트

1. ALB DNS 주소에 `/load.html` 추가하여 접속
2. 여러 브라우저 탭에서 동시에 접속
3. 각 탭에서 페이지를 여러 번 새로고침

### 5.3 Auto Scaling 동작 확인

1. **Auto Scaling Groups** 페이지에서 ASG 선택
2. **Monitoring** 탭에서 CPU 사용률 그래프 확인
3. **Activity** 탭에서 스케일링 활동 모니터링
4. CPU 사용률이 70%를 초과하면 인스턴스가 추가되는지 확인

### 5.4 스케일링 정책 테스트

부하 테스트 후 다음을 확인합니다:

1. **인스턴스 증가**: CPU 사용률 > 70%일 때 인스턴스 추가
2. **인스턴스 감소**: CPU 사용률 < 70%일 때 인스턴스 제거 (약 5-10분 후)
3. **Target Group 업데이트**: 새 인스턴스가 자동으로 Target Group에 등록

## 실습 6: 고급 설정 실습

### 6.1 다중 Target Group 설정

1. 새로운 Target Group 생성:
   ```
   Name: api-servers-tg
   Protocol: HTTP
   Port: 8080
   Health check path: /health
   ```

2. ALB에 새로운 리스너 규칙 추가:
   - **Path**: `/api/*`
   - **Action**: Forward to `api-servers-tg`

### 6.2 Scheduled Scaling 설정

1. ASG 선택 > **Automatic scaling** 탭
2. **Create scheduled action** 클릭:
   ```
   Name: morning-scale-up
   Desired capacity: 4
   Recurrence: 0 9 * * MON-FRI (매일 오전 9시)
   ```

3. 저녁 스케일 다운 액션도 생성:
   ```
   Name: evening-scale-down
   Desired capacity: 2
   Recurrence: 0 18 * * MON-FRI (매일 오후 6시)
   ```

### 6.3 Connection Draining 설정

1. **Target Groups** > `web-servers-tg` 선택
2. **Attributes** 탭 > **Edit** 버튼 클릭
3. **Deregistration delay**: 60 seconds로 설정
4. **Save changes** 클릭

## 문제 해결 가이드

### 일반적인 문제들

#### 1. 인스턴스가 Target Group에 등록되지 않음

**증상**: Target Group에서 인스턴스가 "unhealthy" 상태

**해결 방법**:
1. Security Group 확인:
   - ALB Security Group에서 인스턴스로의 HTTP(80) 트래픽 허용
   - 인스턴스 Security Group에서 ALB로부터의 HTTP(80) 트래픽 허용

2. Health Check 설정 확인:
   - Health check path가 올바른지 확인 (`/`)
   - 웹 서버가 정상적으로 실행 중인지 확인

3. 인스턴스 로그 확인:
```bash
# SSH로 인스턴스 접속 후
sudo systemctl status httpd
sudo tail -f /var/log/httpd/access_log
```

#### 2. Auto Scaling이 동작하지 않음

**증상**: CPU 사용률이 높아도 인스턴스가 추가되지 않음

**해결 방법**:
1. CloudWatch 에이전트 설치 확인
2. Scaling Policy 설정 재확인
3. Cooldown 기간 확인 (기본 300초)

#### 3. 웹 페이지에 접속할 수 없음

**증상**: ALB DNS로 접속 시 타임아웃 또는 502 에러

**해결 방법**:
1. ALB Security Group에서 인터넷(0.0.0.0/0)으로부터 HTTP(80) 허용 확인
2. 인스턴스가 public subnet에 있는지 확인
3. Internet Gateway가 VPC에 연결되어 있는지 확인

## 비용 관리

### 실습 후 리소스 정리

**중요**: 실습 완료 후 다음 순서로 리소스를 삭제하여 불필요한 비용을 방지하세요.

1. **Auto Scaling Group 삭제**:
   - ASG 선택 > **Actions** > **Delete**
   - 모든 인스턴스가 자동으로 종료됨

2. **Load Balancer 삭제**:
   - ALB 선택 > **Actions** > **Delete**

3. **Target Group 삭제**:
   - Target Group 선택 > **Actions** > **Delete**

4. **Launch Template 삭제**:
   - Launch Template 선택 > **Actions** > **Delete template**

5. **Security Groups 삭제**:
   - 사용자 정의 Security Group들 삭제

### 비용 모니터링

1. **AWS Cost Explorer**에서 일일 비용 확인
2. **CloudWatch Billing Alarms** 설정으로 예산 초과 방지
3. **AWS Budgets**으로 월별 예산 관리

## 추가 학습 리소스

### AWS 공식 문서
- [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/)
- [Amazon EC2 Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/ec2/)

### 실습 확장 아이디어
1. **HTTPS 설정**: ACM 인증서를 사용한 SSL/TLS 구성
2. **Multi-AZ 배포**: 3개 이상의 가용 영역에 걸친 배포
3. **Blue/Green 배포**: CodeDeploy를 사용한 무중단 배포
4. **Container 기반**: ECS와 ALB 연동

## 실습 완료 체크리스트

- [ ] Launch Template 생성 완료
- [ ] Application Load Balancer 생성 완료
- [ ] Target Group 생성 및 설정 완료
- [ ] Auto Scaling Group 생성 완료
- [ ] ALB와 ASG 연동 확인
- [ ] 웹 페이지 접속 및 로드 밸런싱 동작 확인
- [ ] Auto Scaling 정책 테스트 완료
- [ ] CloudWatch 메트릭 모니터링 확인
- [ ] 부하 테스트 수행 및 결과 분석
- [ ] 리소스 정리 완료

---

**실습 소요 시간**: 약 60-90분  
**난이도**: ⭐⭐⭐⭐☆  
**Free Tier 적용**: 가능 (월 750시간 한도 내)

이번 실습을 통해 AWS의 핵심 서비스인 Load Balancing과 Auto Scaling을 실제로 구성하고 테스트해보았습니다. 이는 실제 프로덕션 환경에서 고가용성과 확장성을 구현하는 기본적인 패턴입니다!