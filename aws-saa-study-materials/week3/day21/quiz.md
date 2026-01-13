# Day 21 Quiz: Week 3 종합 복습 - 애플리케이션 서비스 및 배포

## 퀴즈 개요
- **주제**: Week 3 전체 내용 종합 (Load Balancing, CloudFront, Route 53, API Gateway, Lambda, ECS, 배포 도구)
- **문제 수**: 15문제
- **예상 소요 시간**: 25-30분
- **난이도**: 고급

---

## 문제 1: Load Balancer 선택 기준

다음 시나리오에서 가장 적합한 Load Balancer 조합은?

**시나리오**: 
- 게임 서버: 초저지연 UDP 트래픽, 고정 IP 필요
- 웹 API: HTTP/HTTPS, 경로 기반 라우팅 필요
- 스트리밍 서비스: TCP 연결, 높은 처리량 필요

A) 모든 서비스에 ALB 사용  
B) 게임 서버: NLB, 웹 API: ALB, 스트리밍: NLB  
C) 모든 서비스에 NLB 사용  
D) 게임 서버: CLB, 웹 API: ALB, 스트리밍: NLB  

### 정답: B

### 해설:
각 서비스의 특성에 맞는 Load Balancer를 선택해야 합니다.

- **게임 서버**: UDP 트래픽과 고정 IP가 필요하므로 **NLB**가 적합합니다. NLB는 Layer 4에서 동작하며 UDP를 지원하고 고정 IP를 제공합니다.
- **웹 API**: HTTP/HTTPS와 경로 기반 라우팅이 필요하므로 **ALB**가 적합합니다. ALB는 Layer 7에서 동작하며 URL 경로에 따른 라우팅을 지원합니다.
- **스트리밍 서비스**: TCP 연결과 높은 처리량이 필요하므로 **NLB**가 적합합니다. NLB는 초고성능과 낮은 지연시간을 제공합니다.

**관련 개념**: Load Balancer 유형별 특징, 서비스 요구사항 분석

---

## 문제 2: CloudFront 캐싱 전략

다음 중 CloudFront에서 동적 콘텐츠의 캐싱을 최적화하는 방법으로 **가장 적절한** 것은?

A) 모든 동적 콘텐츠의 TTL을 0으로 설정  
B) Cache-Control 헤더를 사용하여 콘텐츠별로 TTL 설정  
C) 모든 쿼리 스트링을 캐시 키에 포함  
D) Origin Request Policy를 사용하지 않음  

### 정답: B

### 해설:
동적 콘텐츠의 캐싱 최적화는 콘텐츠의 특성에 따라 세밀하게 제어해야 합니다.

- **A) 틀림**: 모든 동적 콘텐츠의 TTL을 0으로 설정하면 캐싱의 이점을 전혀 활용할 수 없습니다.
- **B) 정답**: Cache-Control 헤더를 사용하면 콘텐츠별로 적절한 TTL을 설정할 수 있습니다:
  - `Cache-Control: max-age=300` (5분 캐싱)
  - `Cache-Control: no-cache` (매번 재검증)
  - `Cache-Control: private` (CDN에서 캐싱 안함)
- **C) 틀림**: 모든 쿼리 스트링을 포함하면 캐시 적중률이 크게 떨어집니다.
- **D) 틀림**: Origin Request Policy는 Origin으로 전달할 헤더/쿼리를 제어하는 중요한 기능입니다.

**Best Practice**: 
- 사용자 프로필: `Cache-Control: private`
- API 응답: `Cache-Control: max-age=60`
- 정적 리소스: `Cache-Control: max-age=31536000`

**관련 개념**: CloudFront 캐싱 정책, Cache-Control 헤더, TTL 설정

---

## 문제 3: Route 53 라우팅 정책 시나리오

다음 요구사항을 만족하는 Route 53 라우팅 정책 조합은?

**요구사항**:
1. 평상시: 트래픽의 70%는 us-east-1, 30%는 eu-west-1로 분산
2. us-east-1 장애 시: 모든 트래픽을 eu-west-1로 자동 전환
3. 한국 사용자는 항상 ap-northeast-2로 라우팅

A) Weighted + Failover + Geolocation  
B) Latency + Failover + Weighted  
C) Geolocation + Weighted + Health Check  
D) Multivalue + Geoproximity + Failover  

### 정답: A

### 해설:
복합적인 요구사항을 만족하려면 여러 라우팅 정책을 조합해야 합니다.

**요구사항 분석**:
1. **트래픽 분산 (70:30)**: **Weighted Routing** 필요
2. **장애 시 자동 전환**: **Failover Routing** 필요
3. **지역별 라우팅**: **Geolocation Routing** 필요

**구현 방법**:
```
1. Geolocation 정책으로 한국(KR) → ap-northeast-2
2. Weighted 정책으로 기본 트래픽 분산:
   - us-east-1: Weight 70
   - eu-west-1: Weight 30
3. Failover 정책으로 us-east-1 장애 시 eu-west-1로 전환
```

**다른 선택지 분석**:
- **B)**: Latency는 지역 고정이 아닌 지연시간 기반 라우팅
- **C)**: Health Check는 정책이 아닌 기능
- **D)**: Multivalue는 여러 IP 반환, Geoproximity는 거리 기반

**관련 개념**: Route 53 라우팅 정책 조합, 복합 시나리오 설계

---

## 문제 4: API Gateway 인증 및 권한부여

다음 중 API Gateway에서 **가장 보안이 강화된** 인증 방식은?

A) API Key만 사용  
B) Lambda Authorizer + JWT 토큰  
C) Cognito User Pool + OAuth 2.0  
D) IAM 역할 기반 인증  

### 정답: C

### 해설:
보안 강화 측면에서 각 인증 방식을 비교해보겠습니다.

**보안 수준 비교**:
- **A) API Key**: 단순한 식별자로 인증보다는 사용량 제한 목적. 보안 수준이 낮음
- **B) Lambda Authorizer + JWT**: 커스텀 로직으로 유연하지만 구현 복잡도가 높고 보안 취약점 가능성
- **C) Cognito User Pool + OAuth 2.0**: AWS 관리형 서비스로 다음 기능 제공:
  - 표준 OAuth 2.0/OpenID Connect 프로토콜
  - MFA (Multi-Factor Authentication) 지원
  - 사용자 풀 관리 및 토큰 검증
  - 세밀한 권한 제어 (Scope 기반)
  - AWS 보안 모범 사례 적용
- **D) IAM 역할**: AWS 서비스 간 통신에는 적합하지만 외부 사용자 인증에는 부적절

**Cognito User Pool의 장점**:
- 토큰 자동 갱신
- 사용자 속성 기반 접근 제어
- 소셜 로그인 통합
- 규정 준수 (GDPR, HIPAA 등)

**관련 개념**: API Gateway 보안, Cognito User Pool, OAuth 2.0

---

## 문제 5: Lambda 함수 최적화

다음 Lambda 함수 설정 중 **성능과 비용을 모두 최적화**하는 조합은?

**시나리오**: 이미지 리사이징 함수, 평균 실행 시간 45초, 메모리 사용량 800MB

A) 메모리: 1024MB, 임시 스토리지: 512MB, 아키텍처: x86_64  
B) 메모리: 3008MB, 임시 스토리지: 10240MB, 아키텍처: arm64  
C) 메모리: 1792MB, 임시 스토리지: 1024MB, 아키텍처: arm64  
D) 메모리: 512MB, 임시 스토리지: 512MB, 아키텍처: x86_64  

### 정답: C

### 해설:
Lambda 최적화는 성능과 비용의 균형을 맞춰야 합니다.

**메모리 설정 분석**:
- 실제 사용량: 800MB
- **A) 1024MB**: 충분하지만 CPU 성능이 제한적
- **B) 3008MB**: 과도한 메모리 할당으로 비용 증가
- **C) 1792MB**: 적절한 여유분과 높은 CPU 성능 제공
- **D) 512MB**: 메모리 부족으로 성능 저하 또는 실행 실패

**아키텍처 선택**:
- **arm64 (Graviton2)**: x86_64 대비 최대 34% 비용 절감, 동등한 성능
- **x86_64**: 기존 아키텍처, 호환성은 좋지만 비용이 높음

**임시 스토리지**:
- 이미지 처리 시 원본과 변환된 파일 저장 공간 필요
- 1024MB면 대부분의 이미지 처리 작업에 충분

**성능 최적화 효과**:
- 메모리 증가 → CPU 성능 향상 → 실행 시간 단축
- arm64 → 비용 절감
- 적절한 임시 스토리지 → I/O 성능 향상

**관련 개념**: Lambda 성능 튜닝, 메모리-CPU 관계, 아키텍처 선택

---

## 문제 6: ECS 배포 전략

다음 시나리오에서 가장 적합한 ECS 배포 전략은?

**시나리오**: 
- 24/7 운영되는 전자상거래 사이트
- 배포 중 서비스 중단 불가
- 롤백이 빠르게 가능해야 함
- 리소스 비용 최적화 필요

A) Rolling Update  
B) Blue/Green Deployment  
C) Canary Deployment  
D) In-place Deployment  

### 정답: B

### 해설:
각 배포 전략의 특징을 시나리오 요구사항과 비교해보겠습니다.

**요구사항 분석**:
1. **무중단 배포**: 서비스 중단 불가
2. **빠른 롤백**: 문제 발생 시 즉시 복구
3. **비용 최적화**: 리소스 효율성

**배포 전략 비교**:

**A) Rolling Update**:
- ✅ 무중단 배포
- ❌ 롤백 시간이 오래 걸림 (점진적 롤백)
- ✅ 리소스 효율적
- ❌ 버전 혼재 상태 발생

**B) Blue/Green Deployment**:
- ✅ 완전한 무중단 배포
- ✅ 즉시 롤백 가능 (트래픽 스위칭만)
- ❌ 2배 리소스 필요 (일시적)
- ✅ 버전 일관성 보장

**C) Canary Deployment**:
- ✅ 무중단 배포
- ✅ 점진적 위험 관리
- ❌ 복잡한 모니터링 필요
- ❌ 완전 배포까지 시간 소요

**D) In-place Deployment**:
- ❌ 서비스 중단 발생
- ❌ 롤백 복잡

**Blue/Green이 최적인 이유**:
- 전자상거래의 높은 가용성 요구사항 만족
- ALB의 Target Group 스위칭으로 즉시 롤백
- ECS Fargate 사용 시 리소스 비용 부담 최소화

**관련 개념**: ECS 배포 전략, Blue/Green 배포, 무중단 배포

---

## 문제 7: Auto Scaling 정책 조합

다음 시나리오에 가장 적합한 Auto Scaling 정책 조합은?

**시나리오**:
- 온라인 교육 플랫폼
- 평일 오전 9시-오후 6시: 높은 트래픽 (수업 시간)
- 주말과 공휴일: 낮은 트래픽
- 갑작스러운 트래픽 증가에 대응 필요

A) Target Tracking Scaling만 사용  
B) Scheduled Scaling + Target Tracking Scaling  
C) Step Scaling + Simple Scaling  
D) Predictive Scaling + Scheduled Scaling  

### 정답: B

### 해설:
예측 가능한 패턴과 예측 불가능한 변화를 모두 고려해야 합니다.

**트래픽 패턴 분석**:
1. **예측 가능**: 평일/주말, 수업 시간대
2. **예측 불가능**: 갑작스러운 트래픽 증가

**정책 조합 분석**:

**A) Target Tracking만**: 
- 예측 가능한 패턴에 대한 사전 대응 불가
- 트래픽 증가 후 반응하므로 지연 발생

**B) Scheduled + Target Tracking**:
- ✅ **Scheduled Scaling**: 수업 시간 전 미리 인스턴스 증가
- ✅ **Target Tracking**: 예상치 못한 트래픽 변화에 자동 대응
- ✅ 비용 효율적: 필요한 시간에만 리소스 확보

**C) Step + Simple Scaling**:
- 예측 가능한 패턴 대응 불가
- Cooldown 기간으로 인한 반응 지연

**D) Predictive + Scheduled**:
- Predictive Scaling은 머신러닝 기반이지만 복잡함
- 갑작스러운 변화에 대한 실시간 대응 부족

**구현 예시**:
```
Scheduled Actions:
- 평일 08:30: Desired Capacity = 10
- 평일 18:30: Desired Capacity = 3
- 주말: Desired Capacity = 2

Target Tracking:
- CPU 사용률 70% 유지
- 응답 시간 200ms 이하 유지
```

**관련 개념**: Auto Scaling 정책 조합, 예측 가능한 워크로드 최적화

---

## 문제 8: CloudFront와 S3 보안

다음 중 CloudFront와 S3 간의 **가장 보안이 강화된** 구성은?

A) S3 버킷을 퍼블릭으로 설정하고 CloudFront에서 직접 접근  
B) Origin Access Identity (OAI) 사용  
C) Origin Access Control (OAC) 사용  
D) S3 버킷 정책으로만 CloudFront IP 허용  

### 정답: C

### 해설:
CloudFront와 S3 간 보안 구성의 발전 과정을 이해해야 합니다.

**보안 구성 비교**:

**A) 퍼블릭 버킷**:
- ❌ 가장 취약한 구성
- ❌ 직접 S3 URL 접근 가능
- ❌ CloudFront 우회 가능

**B) Origin Access Identity (OAI)**:
- ✅ S3 버킷을 프라이빗으로 유지
- ✅ CloudFront만 접근 가능
- ❌ 레거시 방식 (더 이상 권장되지 않음)
- ❌ 일부 S3 기능 제한

**C) Origin Access Control (OAC)**:
- ✅ **최신 권장 방식** (2022년 출시)
- ✅ 모든 S3 기능 지원 (SSE-KMS, SSE-S3 등)
- ✅ 더 강화된 보안
- ✅ AWS Signature Version 4 지원
- ✅ 세밀한 권한 제어

**D) IP 기반 제한**:
- ❌ CloudFront IP 범위가 자주 변경됨
- ❌ 관리 복잡성 증가
- ❌ 완전한 보안 보장 어려움

**OAC 설정 예시**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudfront.amazonaws.com"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::account:distribution/distribution-id"
        }
      }
    }
  ]
}
```

**관련 개념**: CloudFront 보안, OAC vs OAI, S3 버킷 정책

---

## 문제 9: API Gateway와 Lambda 통합

다음 중 API Gateway와 Lambda 통합에서 **Lambda Proxy Integration**의 장점이 **아닌** 것은?

A) 요청의 모든 정보를 Lambda 함수에서 접근 가능  
B) 응답 형식을 Lambda 함수에서 완전히 제어 가능  
C) API Gateway에서 자동으로 응답 변환 수행  
D) 개발 및 디버깅이 간편함  

### 정답: C

### 해설:
Lambda Proxy Integration과 Non-Proxy Integration의 차이점을 이해해야 합니다.

**Lambda Proxy Integration 특징**:

**A) 올바름**: 
- HTTP 메서드, 헤더, 쿼리 파라미터, 경로 파라미터 등 모든 요청 정보가 event 객체에 포함
- 개발자가 필요한 모든 정보에 접근 가능

**B) 올바름**:
- Lambda 함수에서 statusCode, headers, body를 직접 제어
- 커스텀 헤더, 상태 코드 설정 자유도 높음

**C) 틀림 (정답)**:
- **Proxy Integration에서는 자동 변환이 없음**
- Lambda 함수가 API Gateway 응답 형식에 맞춰 직접 반환해야 함
- Non-Proxy Integration에서만 매핑 템플릿을 통한 자동 변환 제공

**D) 올바름**:
- 설정이 간단함 (매핑 템플릿 불필요)
- 디버깅 시 전체 요청 정보 확인 가능

**응답 형식 예시**:
```python
# Proxy Integration 필수 응답 형식
return {
    'statusCode': 200,
    'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },
    'body': json.dumps({'message': 'success'})
}
```

**관련 개념**: Lambda Proxy Integration, API Gateway 통합 유형

---

## 문제 10: Route 53 Health Check

다음 시나리오에서 가장 적절한 Route 53 Health Check 구성은?

**시나리오**:
- 웹 애플리케이션이 us-east-1과 eu-west-1에 배포됨
- 각 리전에 ALB가 있음
- 데이터베이스 연결 실패 시에도 장애로 간주해야 함
- 30초 이내에 장애를 감지해야 함

A) HTTP Health Check로 ALB 엔드포인트만 확인  
B) HTTPS Health Check로 /health 엔드포인트 확인  
C) Calculated Health Check로 여러 조건 조합  
D) CloudWatch Alarm 기반 Health Check  

### 정답: C

### 해설:
복합적인 장애 조건을 모니터링하려면 Calculated Health Check가 필요합니다.

**요구사항 분석**:
1. **ALB 상태 확인**: 기본적인 서비스 가용성
2. **데이터베이스 연결 확인**: 애플리케이션 레벨 상태
3. **30초 이내 감지**: 빠른 장애 감지

**Health Check 유형 비교**:

**A) HTTP Health Check (ALB만)**:
- ❌ 데이터베이스 연결 상태 확인 불가
- ❌ 애플리케이션 레벨 문제 감지 어려움

**B) HTTPS Health Check (/health)**:
- ✅ 애플리케이션 상태 확인 가능
- ❌ 단일 체크로는 복합 조건 처리 제한적

**C) Calculated Health Check**:
- ✅ **여러 Health Check 조합 가능**
- ✅ 복잡한 로직 구현 (AND, OR, NOT)
- ✅ 세밀한 장애 조건 설정

**D) CloudWatch Alarm 기반**:
- ✅ 메트릭 기반 모니터링
- ❌ 실시간 응답성 부족 (최소 1분 간격)

**Calculated Health Check 구성 예시**:
```
Primary Health Check:
├── HTTP Check: ALB 엔드포인트 상태
├── HTTPS Check: /health (DB 연결 포함)
└── CloudWatch Alarm: 응답 시간 < 5초

Logic: (HTTP AND HTTPS AND CloudWatch) = Healthy
```

**장점**:
- 다층적 모니터링
- 세밀한 장애 조건 설정
- 빠른 장애 감지 (10초 간격 가능)

**관련 개념**: Route 53 Health Check 유형, Calculated Health Check

---

## 문제 11: ECS와 Fargate 비교

다음 시나리오에서 **ECS on EC2** 대신 **ECS Fargate**를 선택해야 하는 가장 중요한 이유는?

**시나리오**: 
- 마이크로서비스 아키텍처 (20개 서비스)
- 각 서비스의 리소스 요구사항이 다름
- 트래픽 패턴이 예측 불가능
- 운영팀 규모가 작음

A) 비용이 항상 더 저렴하기 때문  
B) 더 높은 성능을 제공하기 때문  
C) 서버 관리 부담이 없기 때문  
D) 더 많은 커스터마이징이 가능하기 때문  

### 정답: C

### 해설:
시나리오의 핵심은 "작은 운영팀"과 "복잡한 마이크로서비스 환경"입니다.

**시나리오 분석**:
- **20개 마이크로서비스**: 복잡한 운영 환경
- **다양한 리소스 요구사항**: 개별 최적화 필요
- **예측 불가능한 트래픽**: 동적 스케일링 필요
- **작은 운영팀**: 관리 부담 최소화 필요

**선택지 분석**:

**A) 비용**:
- ❌ Fargate가 항상 저렴하지는 않음
- 사용 패턴에 따라 EC2가 더 저렴할 수 있음

**B) 성능**:
- ❌ ECS on EC2가 일반적으로 더 높은 성능
- Fargate는 약간의 오버헤드 존재

**C) 서버 관리 부담 없음** ✅:
- **핵심 장점**: 인프라 관리 완전 자동화
- EC2 패치, 보안 업데이트, 클러스터 관리 불필요
- 작은 팀에게 매우 중요한 이점

**D) 커스터마이징**:
- ❌ ECS on EC2가 더 많은 커스터마이징 제공
- Fargate는 제한된 설정 옵션

**Fargate의 운영 이점**:
```
ECS on EC2 관리 작업:
- EC2 인스턴스 프로비저닝
- OS 패치 및 보안 업데이트
- 클러스터 용량 관리
- 인스턴스 모니터링
- 장애 시 인스턴스 교체

Fargate: 위 작업들이 모두 자동화됨
```

**관련 개념**: ECS 실행 모드, 서버리스 컨테이너, 운영 복잡성

---

## 문제 12: CodePipeline 스테이지 구성

다음 중 **가장 완전한** CI/CD 파이프라인 스테이지 구성은?

A) Source → Build → Deploy  
B) Source → Build → Test → Deploy  
C) Source → Build → Test → Security Scan → Deploy → Post-Deploy Test  
D) Source → Test → Build → Deploy → Rollback  

### 정답: C

### 해설:
현대적인 CI/CD 파이프라인은 품질과 보안을 모두 보장해야 합니다.

**각 스테이지의 중요성**:

**A) 기본 구성**:
- ❌ 테스트와 보안 검증 누락
- ❌ 프로덕션 배포 후 문제 발견 위험

**B) 테스트 추가**:
- ✅ 기본적인 품질 보장
- ❌ 보안 취약점 검증 누락
- ❌ 배포 후 검증 누락

**C) 완전한 파이프라인** ✅:
- ✅ **Source**: 코드 변경 감지
- ✅ **Build**: 컴파일 및 패키징
- ✅ **Test**: 단위/통합 테스트
- ✅ **Security Scan**: 취약점 검사 (SAST, DAST)
- ✅ **Deploy**: 스테이징/프로덕션 배포
- ✅ **Post-Deploy Test**: 배포 후 검증

**D) 순서 문제**:
- ❌ Test가 Build 전에 위치 (빌드된 아티팩트 테스트 불가)
- ❌ Rollback은 스테이지가 아닌 실패 시 액션

**Security Scan 단계의 중요성**:
```
SAST (Static Application Security Testing):
- 소스 코드 취약점 검사
- 의존성 라이브러리 보안 검사

DAST (Dynamic Application Security Testing):
- 실행 중인 애플리케이션 보안 테스트
- 런타임 취약점 검사
```

**Post-Deploy Test 예시**:
- 헬스 체크 확인
- 핵심 기능 스모크 테스트
- 성능 기준선 검증

**관련 개념**: CI/CD 파이프라인 설계, DevSecOps, 품질 게이트

---

## 문제 13: Lambda 동시성 관리

다음 시나리오에서 가장 적절한 Lambda 동시성 설정은?

**시나리오**:
- 주문 처리 Lambda 함수
- 평상시: 초당 100개 요청
- 피크 시간: 초당 1000개 요청
- 다운스트림 데이터베이스 연결 제한: 200개
- 중요한 비즈니스 로직으로 안정성 최우선

A) Reserved Concurrency: 200, Provisioned Concurrency: 100  
B) Reserved Concurrency: 1000, Provisioned Concurrency: 200  
C) Reserved Concurrency만 200으로 설정  
D) Provisioned Concurrency만 100으로 설정  

### 정답: A

### 해설:
Lambda 동시성 관리는 안정성과 성능을 모두 고려해야 합니다.

**시나리오 요구사항**:
1. **안정성 최우선**: 데이터베이스 연결 제한 준수
2. **성능 최적화**: 콜드 스타트 최소화
3. **비용 효율성**: 불필요한 리소스 방지

**동시성 유형 이해**:
- **Reserved Concurrency**: 최대 동시 실행 수 제한
- **Provisioned Concurrency**: 미리 준비된 실행 환경

**선택지 분석**:

**A) Reserved: 200, Provisioned: 100** ✅:
- ✅ **Reserved 200**: 데이터베이스 연결 제한 보호
- ✅ **Provisioned 100**: 평상시 트래픽 콜드 스타트 방지
- ✅ 안정성과 성능 균형

**B) Reserved: 1000, Provisioned: 200**:
- ❌ Reserved가 너무 높음 (DB 연결 제한 초과 위험)
- ❌ Provisioned가 과도함 (비용 증가)

**C) Reserved만 200**:
- ✅ 안정성 보장
- ❌ 콜드 스타트 문제 해결 안됨

**D) Provisioned만 100**:
- ❌ 최대 동시성 제한 없음 (DB 과부하 위험)
- ❌ 피크 시간 대응 부족

**동작 시나리오**:
```
평상시 (100 RPS):
- Provisioned 100개로 콜드 스타트 없이 처리

피크 시간 (1000 RPS):
- Provisioned 100개 + 추가 100개 (콜드 스타트)
- 총 200개로 제한되어 DB 보호
- 초과 요청은 스로틀링
```

**관련 개념**: Lambda 동시성, Reserved vs Provisioned Concurrency

---

## 문제 14: 마이크로서비스 통신 패턴

다음 중 마이크로서비스 간 **비동기 통신**에 가장 적합한 AWS 서비스 조합은?

A) API Gateway + Lambda + RDS  
B) SQS + SNS + Lambda  
C) ALB + ECS + ElastiCache  
D) CloudFront + S3 + DynamoDB  

### 정답: B

### 해설:
마이크로서비스의 비동기 통신은 느슨한 결합과 확장성을 제공합니다.

**비동기 통신의 특징**:
- 서비스 간 직접 의존성 제거
- 장애 격리 및 복원력 향상
- 독립적인 확장 가능

**선택지 분석**:

**A) API Gateway + Lambda + RDS**:
- ❌ **동기 통신 패턴**
- API Gateway는 실시간 요청-응답 방식
- 서비스 간 직접 호출

**B) SQS + SNS + Lambda** ✅:
- ✅ **완벽한 비동기 패턴**
- **SNS**: 이벤트 발행 (Pub/Sub)
- **SQS**: 메시지 큐잉 및 버퍼링
- **Lambda**: 이벤트 기반 처리

**C) ALB + ECS + ElastiCache**:
- ❌ **동기 통신 패턴**
- ALB를 통한 직접 HTTP 호출
- 캐싱은 성능 최적화용

**D) CloudFront + S3 + DynamoDB**:
- ❌ **정적 콘텐츠 배포 패턴**
- 서비스 간 통신과 무관

**비동기 통신 패턴 예시**:
```
주문 서비스 → SNS (주문 생성 이벤트)
              ↓
         ┌─── SQS (재고 관리) → Lambda (재고 차감)
         ├─── SQS (결제 처리) → Lambda (결제 진행)
         └─── SQS (배송 준비) → Lambda (배송 시작)
```

**장점**:
- 서비스 독립성 보장
- 장애 전파 방지
- 트래픽 버퍼링
- 자동 재시도 및 DLQ 지원

**관련 개념**: 마이크로서비스 통신 패턴, 이벤트 기반 아키텍처

---

## 문제 15: 종합 시나리오 - 글로벌 서비스 아키텍처

다음 요구사항을 만족하는 **가장 적절한** 아키텍처는?

**요구사항**:
- 글로벌 사용자 대상 (미국, 유럽, 아시아)
- 정적 콘텐츠와 동적 API 모두 제공
- 지역별 데이터 규정 준수 (GDPR 등)
- 99.99% 가용성 목표
- 지연시간 최소화

A) 단일 리전에 모든 서비스 배포 + CloudFront  
B) 각 리전에 완전한 서비스 스택 배포 + Route 53 Geolocation  
C) CloudFront + API Gateway + Lambda@Edge + 리전별 데이터 저장소  
D) Global Load Balancer + 단일 데이터베이스 + 다중 리전 캐시  

### 정답: B

### 해설:
글로벌 서비스에서 데이터 규정 준수와 고가용성을 동시에 만족하려면 리전별 완전 배포가 필요합니다.

**요구사항 분석**:
1. **글로벌 서비스**: 다중 리전 필요
2. **데이터 규정 준수**: 지역별 데이터 격리
3. **99.99% 가용성**: 리전 장애 대응
4. **지연시간 최소화**: 사용자 근접 배치

**아키텍처 비교**:

**A) 단일 리전 + CloudFront**:
- ❌ 데이터 규정 준수 불가 (모든 데이터가 한 리전)
- ❌ 리전 장애 시 전체 서비스 중단
- ❌ API 지연시간 높음

**B) 리전별 완전 스택 + Geolocation** ✅:
- ✅ **데이터 주권 보장**: 각 리전에 데이터 저장
- ✅ **고가용성**: 리전 장애 시 다른 리전으로 자동 전환
- ✅ **최적 성능**: 사용자 근접 서비스
- ✅ **규정 준수**: GDPR, 중국 사이버보안법 등 대응

**C) CloudFront + Lambda@Edge**:
- ❌ Lambda@Edge 제한사항 (실행 시간, 메모리)
- ❌ 복잡한 비즈니스 로직 처리 어려움
- ❌ 데이터베이스 직접 접근 불가

**D) Global Load Balancer + 단일 DB**:
- ❌ 데이터 규정 준수 불가
- ❌ 단일 장애점 (데이터베이스)
- ❌ 지연시간 최적화 어려움

**권장 아키텍처**:
```
미국 리전:
├── CloudFront (글로벌)
├── Route 53 (Geolocation: US → us-east-1)
├── ALB + ECS/Lambda
└── RDS (미국 사용자 데이터)

유럽 리전:
├── Route 53 (Geolocation: EU → eu-west-1)
├── ALB + ECS/Lambda
└── RDS (유럽 사용자 데이터)

아시아 리전:
├── Route 53 (Geolocation: AS → ap-northeast-1)
├── ALB + ECS/Lambda
└── RDS (아시아 사용자 데이터)
```

**데이터 동기화**:
- 사용자별 데이터: 지역 격리
- 글로벌 데이터: DynamoDB Global Tables 또는 교차 리전 복제

**관련 개념**: 글로벌 아키텍처, 데이터 주권, 지역별 규정 준수

---

## 퀴즈 결과 분석

### 점수별 평가

- **13-15점 (87-100%)**: 🎉 **탁월함!** Week 3 내용을 완벽하게 마스터했습니다. 실제 아키텍처 설계 능력이 뛰어납니다.
- **10-12점 (67-80%)**: 👍 **우수함!** 대부분의 개념을 잘 이해하고 있습니다. 틀린 문제를 복습해보세요.
- **7-9점 (47-60%)**: 📚 **양호함!** 기본 개념은 이해했지만 실무 적용 능력을 더 키워야 합니다.
- **6점 이하 (40% 이하)**: 💪 **추가 학습 필요!** Week 3 내용을 다시 복습한 후 퀴즈를 재도전해보세요.

### 영역별 분석

#### Load Balancing & Auto Scaling (문제 1, 6, 7)
- **3문제 모두 정답**: ALB/NLB 선택과 Auto Scaling 정책을 완벽히 이해
- **2문제 정답**: 기본 개념은 이해했으나 복합 시나리오 적용 연습 필요
- **1문제 이하**: Day 15 내용 재복습 권장

#### CloudFront & CDN (문제 2, 8)
- **2문제 모두 정답**: CDN 최적화와 보안 구성을 잘 이해
- **1문제 정답**: 캐싱 전략 또는 보안 구성 중 하나 보완 필요
- **0문제 정답**: Day 16 내용 재복습 권장

#### Route 53 & DNS (문제 3, 10)
- **2문제 모두 정답**: DNS 라우팅과 Health Check를 완벽히 이해
- **1문제 정답**: 복합 라우팅 정책 또는 Health Check 구성 연습 필요
- **0문제 정답**: Day 17 내용 재복습 권장

#### API Gateway & Lambda (문제 4, 5, 9, 13)
- **4문제 모두 정답**: 서버리스 아키텍처 전문가 수준
- **3문제 정답**: 서버리스 최적화 기법 추가 학습 권장
- **2문제 이하**: Day 18 내용 재복습 권장

#### ECS & 컨테이너 (문제 6, 11)
- **2문제 모두 정답**: 컨테이너 배포 전략을 잘 이해
- **1문제 정답**: ECS 실행 모드 또는 배포 전략 보완 필요
- **0문제 정답**: Day 19 내용 재복습 권장

#### 배포 & 관리 도구 (문제 12)
- **정답**: CI/CD 파이프라인 설계 능력 우수
- **오답**: Day 20 내용 재복습 권장

#### 통합 아키텍처 (문제 14, 15)
- **2문제 모두 정답**: 마이크로서비스 아키텍처 설계 능력 탁월
- **1문제 정답**: 서비스 간 통신 패턴 또는 글로벌 아키텍처 보완 필요
- **0문제 정답**: Week 3 전체 내용 통합 복습 필요

### 추가 학습 권장사항

#### 7점 이하인 경우:
1. **이론 재복습**: Week 3 각 일차별 theory.md 파일 재학습
2. **실습 진행**: 각 서비스별 hands-on 실습 수행
3. **AWS 공식 문서**: 틀린 문제 관련 서비스 문서 읽기
4. **아키텍처 패턴**: AWS Well-Architected Framework 학습

#### 8-12점인 경우:
1. **실무 시나리오**: 복합적인 아키텍처 설계 연습
2. **성능 최적화**: 각 서비스별 최적화 기법 학습
3. **보안 강화**: 보안 모범 사례 추가 학습
4. **비용 최적화**: 비용 효율적인 아키텍처 설계 연습

#### 13점 이상인 경우:
1. **고급 패턴**: 엔터프라이즈 아키텍처 패턴 학습
2. **실제 프로젝트**: 학습한 내용을 실제 프로젝트에 적용
3. **AWS 인증**: Solutions Architect Professional 준비
4. **커뮤니티 참여**: AWS 커뮤니티에서 지식 공유

### 다음 단계

1. **Week 4 준비**: 모니터링, 보안, 비용 최적화 학습 준비
2. **실습 프로젝트**: Day 21 마이크로서비스 아키텍처 실습 진행
3. **복습 계획**: 틀린 문제 관련 내용 집중 복습
4. **모의고사 준비**: Week 4 완료 후 종합 모의고사 대비

---

**퀴즈 완료 시간**: ___분 ___초  
**정답 개수**: ___/15  
**정답률**: ___%

Week 3 학습을 완료하신 것을 축하합니다! 🎉  
이제 AWS 애플리케이션 서비스와 배포에 대한 실무 수준의 지식을 갖추셨습니다.