# Day 17 실습: Route 53 호스팅 영역 및 레코드 설정

## 실습 개요
이번 실습에서는 Amazon Route 53을 사용하여 호스팅 영역을 생성하고, 다양한 DNS 레코드를 설정하는 방법을 학습합니다. 또한 헬스 체크와 라우팅 정책을 구성하여 고가용성 DNS 서비스를 구축해보겠습니다.

## 실습 목표
- Route 53 호스팅 영역 생성 및 관리
- 다양한 DNS 레코드 타입 설정
- 헬스 체크 구성 및 모니터링
- 라우팅 정책 적용 및 테스트
- Route 53과 다른 AWS 서비스 연동

## 사전 준비사항
- AWS 계정 및 적절한 권한
- 테스트용 도메인 (선택사항, 없어도 실습 가능)
- 이전 실습에서 생성한 EC2 인스턴스 또는 ALB
- 기본적인 DNS 개념 이해

## 예상 소요 시간
약 60-90분

## 실습 단계

### 1단계: Route 53 서비스 접근

1. **AWS Management Console 로그인**
   - AWS 계정으로 로그인합니다.

2. **Route 53 서비스 접근**
   - 서비스 검색창에 "Route 53"을 입력합니다.
   - Route 53 서비스를 클릭합니다.

3. **Route 53 대시보드 확인**
   - 대시보드에서 다음 항목들을 확인합니다:
     - Hosted zones (호스팅 영역)
     - Health checks (헬스 체크)
     - Domain registration (도메인 등록)
     - Traffic flow (트래픽 플로우)

### 2단계: 호스팅 영역 생성

1. **호스팅 영역 생성 시작**
   - 좌측 메뉴에서 "Hosted zones"를 클릭합니다.
   - "Create hosted zone" 버튼을 클릭합니다.

2. **호스팅 영역 설정**
   ```
   Domain name: example-lab.com (실제 도메인이 없다면 테스트용 이름 사용)
   Description: SAA-C03 실습용 호스팅 영역
   Type: Public hosted zone (퍼블릭 호스팅 영역)
   ```

3. **호스팅 영역 생성 완료**
   - "Create hosted zone" 버튼을 클릭합니다.
   - 생성된 호스팅 영역의 세부 정보를 확인합니다.

4. **네임서버 정보 확인**
   - 생성된 호스팅 영역에서 NS 레코드를 확인합니다.
   - 4개의 네임서버 주소가 표시됩니다.
   - 실제 도메인이 있다면 이 네임서버를 도메인 등록 대행자에 설정해야 합니다.

### 3단계: 기본 DNS 레코드 생성

#### 3-1. A 레코드 생성

1. **A 레코드 생성 시작**
   - 호스팅 영역 내에서 "Create record" 버튼을 클릭합니다.

2. **A 레코드 설정**
   ```
   Record name: www
   Record type: A
   Value: 203.0.113.1 (예시 IP 주소, 실제 서버 IP 사용)
   TTL: 300 seconds
   Routing policy: Simple routing
   ```

3. **레코드 생성 완료**
   - "Create records" 버튼을 클릭합니다.

#### 3-2. CNAME 레코드 생성

1. **CNAME 레코드 생성**
   ```
   Record name: blog
   Record type: CNAME
   Value: www.example-lab.com
   TTL: 300 seconds
   ```

2. **레코드 생성 완료**
   - "Create records" 버튼을 클릭합니다.

#### 3-3. MX 레코드 생성

1. **MX 레코드 생성**
   ```
   Record name: (비워둠 - 루트 도메인용)
   Record type: MX
   Value: 10 mail.example-lab.com
   TTL: 300 seconds
   ```

2. **레코드 생성 완료**
   - "Create records" 버튼을 클릭합니다.

### 4단계: 헬스 체크 설정

#### 4-1. HTTP 헬스 체크 생성

1. **헬스 체크 메뉴 접근**
   - 좌측 메뉴에서 "Health checks"를 클릭합니다.
   - "Create health check" 버튼을 클릭합니다.

2. **헬스 체크 기본 설정**
   ```
   Name: www-health-check
   What to monitor: Endpoint
   Specify endpoint by: IP address
   Protocol: HTTP
   IP address: 203.0.113.1 (A 레코드에서 사용한 IP)
   Port: 80
   Path: /health (또는 /)
   ```

3. **고급 설정**
   ```
   Request interval: Standard (30 seconds)
   Failure threshold: 3
   String matching: 비활성화
   Latency graphs: 활성화
   ```

4. **알림 설정 (선택사항)**
   - "Get notified when health check fails" 체크
   - SNS 토픽 생성 또는 기존 토픽 선택
   - 이메일 주소 입력

5. **헬스 체크 생성 완료**
   - "Create health check" 버튼을 클릭합니다.

#### 4-2. 헬스 체크 상태 확인

1. **헬스 체크 목록에서 상태 확인**
   - 생성된 헬스 체크의 상태를 확인합니다.
   - Success/Failure 상태와 응답 시간을 모니터링합니다.

2. **헬스 체크 세부 정보 확인**
   - 헬스 체크를 클릭하여 세부 정보를 확인합니다.
   - "Health checkers" 탭에서 전 세계 체크 포인트 상태를 확인합니다.

### 5단계: 가중치 기반 라우팅 설정

#### 5-1. 추가 A 레코드 생성 (가중치용)

1. **첫 번째 가중치 레코드**
   ```
   Record name: app
   Record type: A
   Value: 203.0.113.1
   TTL: 60 seconds
   Routing policy: Weighted
   Weight: 70
   Set ID: primary-server
   Health check: www-health-check (앞서 생성한 헬스 체크)
   ```

2. **두 번째 가중치 레코드**
   ```
   Record name: app
   Record type: A
   Value: 203.0.113.2 (다른 서버 IP)
   TTL: 60 seconds
   Routing policy: Weighted
   Weight: 30
   Set ID: secondary-server
   Health check: 새로운 헬스 체크 생성 또는 기존 사용
   ```

#### 5-2. 가중치 라우팅 테스트

1. **DNS 조회 테스트**
   - 터미널에서 다음 명령어로 테스트:
   ```bash
   nslookup app.example-lab.com
   # 또는
   dig app.example-lab.com
   ```

2. **여러 번 조회하여 가중치 확인**
   - 여러 번 조회하여 70:30 비율로 다른 IP가 반환되는지 확인합니다.

### 6단계: 장애 조치 라우팅 설정

#### 6-1. 장애 조치 레코드 생성

1. **기본(Primary) 레코드**
   ```
   Record name: failover
   Record type: A
   Value: 203.0.113.1
   TTL: 60 seconds
   Routing policy: Failover
   Failover record type: Primary
   Set ID: primary-failover
   Health check: www-health-check
   ```

2. **보조(Secondary) 레코드**
   ```
   Record name: failover
   Record type: A
   Value: 203.0.113.2
   TTL: 60 seconds
   Routing policy: Failover
   Failover record type: Secondary
   Set ID: secondary-failover
   Health check: 보조 서버용 헬스 체크
   ```

#### 6-2. 장애 조치 테스트

1. **정상 상태 테스트**
   ```bash
   nslookup failover.example-lab.com
   ```
   - 기본 서버 IP가 반환되는지 확인합니다.

2. **장애 시뮬레이션**
   - 기본 서버의 헬스 체크를 실패하도록 설정하거나
   - 헬스 체크 설정을 임시로 잘못된 경로로 변경합니다.

3. **장애 조치 확인**
   - 몇 분 후 DNS 조회 시 보조 서버 IP가 반환되는지 확인합니다.

### 7단계: 지리적 위치 기반 라우팅 설정

#### 7-1. 지리적 라우팅 레코드 생성

1. **아시아 사용자용 레코드**
   ```
   Record name: geo
   Record type: A
   Value: 203.0.113.10 (아시아 서버 IP)
   TTL: 300 seconds
   Routing policy: Geolocation
   Location: Asia
   Set ID: asia-server
   ```

2. **북미 사용자용 레코드**
   ```
   Record name: geo
   Record type: A
   Value: 203.0.113.20 (북미 서버 IP)
   TTL: 300 seconds
   Routing policy: Geolocation
   Location: North America
   Set ID: north-america-server
   ```

3. **기본 레코드 (Default)**
   ```
   Record name: geo
   Record type: A
   Value: 203.0.113.30 (기본 서버 IP)
   TTL: 300 seconds
   Routing policy: Geolocation
   Location: Default
   Set ID: default-server
   ```

### 8단계: Route 53과 CloudFront 연동

#### 8-1. CloudFront 배포와 연동 (선택사항)

1. **CNAME 레코드로 CloudFront 연동**
   ```
   Record name: cdn
   Record type: CNAME
   Value: d1234567890.cloudfront.net (CloudFront 도메인)
   TTL: 300 seconds
   ```

2. **Alias 레코드로 CloudFront 연동**
   ```
   Record name: (비워둠 - 루트 도메인용)
   Record type: A
   Alias: Yes
   Alias target: CloudFront distribution 선택
   ```

### 9단계: 프라이빗 호스팅 영역 생성 (선택사항)

#### 9-1. 프라이빗 호스팅 영역 생성

1. **프라이빗 호스팅 영역 설정**
   ```
   Domain name: internal.example.com
   Description: 내부 서비스용 프라이빗 DNS
   Type: Private hosted zone
   VPCs to associate: 기존 VPC 선택
   ```

2. **내부 서비스 레코드 생성**
   ```
   Record name: database
   Record type: A
   Value: 10.0.1.100 (내부 데이터베이스 서버 IP)
   TTL: 300 seconds
   ```

### 10단계: DNS 쿼리 로그 설정

#### 10-1. 쿼리 로깅 활성화

1. **쿼리 로깅 설정**
   - 호스팅 영역에서 "Query logging" 탭을 클릭합니다.
   - "Configure query logging" 버튼을 클릭합니다.

2. **CloudWatch Logs 그룹 설정**
   ```
   Log group name: /aws/route53/example-lab.com
   ```

3. **로그 확인**
   - CloudWatch Logs에서 DNS 쿼리 로그를 확인합니다.

### 11단계: 모니터링 및 알림 설정

#### 11-1. CloudWatch 메트릭 확인

1. **Route 53 메트릭 확인**
   - CloudWatch 콘솔에서 Route 53 메트릭을 확인합니다.
   - 헬스 체크 상태, 쿼리 수 등을 모니터링합니다.

2. **알람 설정**
   ```
   Metric: HealthCheckStatus
   Condition: < 1 (헬스 체크 실패 시)
   Action: SNS 알림 발송
   ```

### 12단계: 테스트 및 검증

#### 12-1. DNS 전파 확인

1. **DNS 전파 테스트 도구 사용**
   - 온라인 DNS 전파 체크 도구를 사용하여 전 세계 DNS 서버에서의 전파 상태를 확인합니다.

2. **다양한 도구로 테스트**
   ```bash
   # nslookup 사용
   nslookup www.example-lab.com
   
   # dig 사용
   dig www.example-lab.com
   
   # 특정 네임서버 쿼리
   dig @8.8.8.8 www.example-lab.com
   ```

#### 12-2. 라우팅 정책 테스트

1. **가중치 라우팅 테스트**
   - 여러 번 DNS 조회를 수행하여 가중치에 따른 응답 확인

2. **장애 조치 테스트**
   - 헬스 체크 실패 시나리오 테스트

3. **지리적 라우팅 테스트**
   - VPN을 사용하여 다른 지역에서 접속 테스트

### 13단계: 비용 모니터링

#### 13-1. Route 53 비용 확인

1. **Billing 대시보드 확인**
   - AWS Billing 콘솔에서 Route 53 관련 비용을 확인합니다.

2. **비용 구성 요소 이해**
   - 호스팅 영역 비용: $0.50/월
   - DNS 쿼리 비용: 백만 쿼리당 $0.40
   - 헬스 체크 비용: $0.50/월

### 14단계: 정리 작업

#### 14-1. 리소스 정리

1. **테스트용 레코드 삭제**
   - 실습에서 생성한 불필요한 DNS 레코드들을 삭제합니다.

2. **헬스 체크 삭제**
   - 테스트용 헬스 체크를 삭제합니다.

3. **호스팅 영역 유지 또는 삭제**
   - 계속 사용할 예정이면 유지, 그렇지 않으면 삭제합니다.
   - **주의**: 호스팅 영역을 삭제하면 모든 DNS 레코드가 함께 삭제됩니다.

## 실습 완료 체크리스트

- [ ] Route 53 호스팅 영역 생성 완료
- [ ] A, CNAME, MX 레코드 생성 완료
- [ ] 헬스 체크 설정 및 모니터링 완료
- [ ] 가중치 기반 라우팅 설정 완료
- [ ] 장애 조치 라우팅 설정 완료
- [ ] 지리적 위치 기반 라우팅 설정 완료
- [ ] DNS 쿼리 테스트 완료
- [ ] CloudWatch 모니터링 설정 완료
- [ ] 비용 모니터링 확인 완료
- [ ] 불필요한 리소스 정리 완료

## 문제 해결 가이드

### 일반적인 문제들

1. **DNS 전파 지연**
   - 문제: DNS 변경사항이 즉시 반영되지 않음
   - 해결: TTL 시간만큼 기다리거나, DNS 캐시 플러시

2. **헬스 체크 실패**
   - 문제: 헬스 체크가 계속 실패 상태
   - 해결: 대상 서버의 방화벽 설정 확인, 경로 확인

3. **라우팅 정책이 작동하지 않음**
   - 문제: 설정한 라우팅 정책이 적용되지 않음
   - 해결: Set ID 중복 확인, 헬스 체크 상태 확인

4. **높은 DNS 쿼리 비용**
   - 문제: 예상보다 높은 DNS 쿼리 비용 발생
   - 해결: TTL 값 증가, 불필요한 쿼리 최적화

## 추가 학습 리소스

- [AWS Route 53 개발자 가이드](https://docs.aws.amazon.com/route53/)
- [Route 53 라우팅 정책 상세 가이드](https://docs.aws.amazon.com/route53/latest/developerguide/routing-policy.html)
- [DNS 모범 사례](https://docs.aws.amazon.com/route53/latest/developerguide/best-practices-dns.html)

## 다음 단계

이번 실습을 통해 Route 53의 핵심 기능들을 실제로 구성해보았습니다. 다음 실습에서는 API Gateway와 Lambda를 사용한 서버리스 아키텍처를 구축해보겠습니다.

실습 중 궁금한 점이나 문제가 발생하면 언제든지 질문해주세요!