# Day 25 실습: Well-Architected Framework를 활용한 아키텍처 검토

## 🎯 실습 목표

이 실습에서는 AWS Well-Architected Tool을 사용하여 기존 아키텍처를 검토하고 개선 계획을 수립합니다. 실제 시나리오를 바탕으로 5개 기둥별 평가를 수행하고 우선순위가 지정된 개선 권장 사항을 도출합니다.

## 📋 사전 준비사항

- AWS 계정 (Free Tier 사용 가능)
- AWS Management Console 접근 권한
- 이전 실습에서 구축한 3-tier 웹 애플리케이션 아키텍처
- Well-Architected Framework 이론 학습 완료

## 🏗️ 실습 시나리오

**시나리오**: 온라인 쇼핑몰을 위한 3-tier 웹 애플리케이션 아키텍처를 Well-Architected Framework 관점에서 검토하고 개선합니다.

**현재 아키텍처**:
- **프레젠테이션 계층**: CloudFront + S3 (정적 웹사이트)
- **애플리케이션 계층**: ALB + EC2 인스턴스 (Auto Scaling)
- **데이터 계층**: RDS MySQL (Multi-AZ)

## 📝 실습 1: Well-Architected Tool 워크로드 생성

### 1.1 Well-Architected Tool 접근

1. **AWS Management Console**에 로그인합니다.

2. **서비스 검색**에서 "Well-Architected Tool"을 검색하고 선택합니다.

3. **Get started** 또는 **Define workload**를 클릭합니다.

### 1.2 워크로드 정의

1. **워크로드 이름**: `ecommerce-web-app`

2. **워크로드 설명**:
   ```
   온라인 쇼핑몰을 위한 3-tier 웹 애플리케이션
   - 일일 활성 사용자: 10,000명
   - 피크 시간대 동시 접속자: 1,000명
   - 주요 기능: 상품 조회, 장바구니, 주문 처리, 결제
   ```

3. **Industry type**: `Retail`

4. **Industry**: `E-commerce`

5. **Environment**: `Production`

6. **AWS Regions**: 현재 사용 중인 리전 선택 (예: `us-east-1`)

7. **Review owner**: 본인의 이메일 주소 입력

8. **Define workload**를 클릭합니다.

### 1.3 아키텍처 개요 작성

**Architecture notes** 섹션에 다음과 같이 작성합니다:

```
현재 아키텍처:

1. 프레젠테이션 계층:
   - Amazon CloudFront (CDN)
   - Amazon S3 (정적 웹사이트 호스팅)

2. 애플리케이션 계층:
   - Application Load Balancer (ALB)
   - Amazon EC2 인스턴스 (t3.medium, Auto Scaling)
   - 가용 영역: 2개 AZ에 분산

3. 데이터 계층:
   - Amazon RDS MySQL (db.t3.micro, Multi-AZ)
   - 자동 백업 활성화 (7일 보존)

4. 보안:
   - VPC with public/private subnets
   - Security Groups
   - IAM roles for EC2 instances

5. 모니터링:
   - CloudWatch 기본 메트릭
   - ALB 액세스 로그
```

## 📝 실습 2: 운영 우수성 기둥 검토

### 2.1 운영 우수성 질문 답변

Well-Architected Tool에서 **Operational Excellence** 기둥을 선택하고 질문에 답변합니다.

#### 주요 질문 예시:

**OPS 1: How do you determine what your priorities are?**
- 답변 선택: "We have a process to evaluate and prioritize opportunities"
- 개선 필요 사항: 비즈니스 우선순위와 기술적 우선순위 연계 프로세스 부족

**OPS 2: How do you structure your organization to support your business outcomes?**
- 답변 선택: "We have a structure that supports our business outcomes"
- 개선 필요 사항: DevOps 문화 및 팀 간 협업 프로세스 개선

**OPS 3: How does your organizational culture support your business outcomes?**
- 답변 선택: "We have a culture that supports our business outcomes"
- 개선 필요 사항: 지속적 학습 및 실험 문화 강화

### 2.2 운영 우수성 개선 계획

식별된 위험 항목:
1. **중위험**: 자동화된 배포 파이프라인 부족
2. **중위험**: 운영 메트릭 및 KPI 정의 부족
3. **저위험**: 인시던트 대응 절차 문서화 부족

## 📝 실습 3: 보안 기둥 검토

### 3.1 보안 질문 답변

**Security** 기둥을 선택하고 주요 질문에 답변합니다.

#### 주요 질문 예시:

**SEC 1: How do you securely operate your workload?**
- 답변 선택: "We have implemented security controls"
- 개선 필요 사항: 보안 거버넌스 프로세스 강화

**SEC 2: How do you manage identities for people and machines?**
- 답변 선택: "We use centralized identity provider"
- 현재 상태: IAM 역할 및 정책 사용 중

**SEC 3: How do you manage permissions for people and machines?**
- 답변 선택: "We grant least privilege access"
- 개선 필요 사항: 정기적인 권한 검토 프로세스 구축

### 3.2 보안 개선 계획

식별된 위험 항목:
1. **고위험**: 데이터베이스 암호화 미적용
2. **중위험**: WAF 미구성
3. **중위험**: 정기적인 보안 감사 프로세스 부족

## 📝 실습 4: 안정성 기둥 검토

### 4.1 안정성 질문 답변

**Reliability** 기둥을 선택하고 주요 질문에 답변합니다.

#### 주요 질문 예시:

**REL 1: How do you manage service quotas and constraints?**
- 답변 선택: "We monitor and manage quotas"
- 현재 상태: 기본 서비스 한도 사용 중

**REL 2: How do you plan your network topology?**
- 답변 선택: "We have planned our network topology"
- 현재 상태: 2개 AZ에 분산된 VPC 구성

**REL 3: How do you design your workload service architecture?**
- 답변 선택: "We have designed for failure"
- 개선 필요 사항: Circuit breaker 패턴 미적용

### 4.2 안정성 개선 계획

식별된 위험 항목:
1. **중위험**: 단일 리전 구성 (재해 복구 계획 부족)
2. **중위험**: 데이터베이스 읽기 전용 복제본 미구성
3. **저위험**: 자동 백업 테스트 프로세스 부족

## 📝 실습 5: 성능 효율성 기둥 검토

### 5.1 성능 효율성 질문 답변

**Performance Efficiency** 기둥을 선택하고 주요 질문에 답변합니다.

#### 주요 질문 예시:

**PERF 1: How do you select the best performing architecture?**
- 답변 선택: "We use a data-driven approach"
- 개선 필요 사항: 성능 테스트 자동화 부족

**PERF 2: How do you select your compute solution?**
- 답변 선택: "We evaluate available compute options"
- 현재 상태: t3.medium 인스턴스 사용 중

**PERF 3: How do you select your storage solution?**
- 답변 선택: "We evaluate available storage options"
- 개선 필요 사항: 스토리지 성능 최적화 검토 필요

### 5.2 성능 효율성 개선 계획

식별된 위험 항목:
1. **중위험**: 데이터베이스 성능 모니터링 부족
2. **중위험**: CDN 캐시 전략 최적화 필요
3. **저위험**: 인스턴스 유형 최적화 검토 필요

## 📝 실습 6: 비용 최적화 기둥 검토

### 6.1 비용 최적화 질문 답변

**Cost Optimization** 기둥을 선택하고 주요 질문에 답변합니다.

#### 주요 질문 예시:

**COST 1: How do you implement cloud financial management?**
- 답변 선택: "We have implemented cost governance"
- 개선 필요 사항: 비용 태깅 전략 개선

**COST 2: How do you govern usage?**
- 답변 선택: "We have policies and procedures"
- 개선 필요 사항: 자동화된 비용 제어 메커니즘 부족

**COST 3: How do you monitor usage and cost?**
- 답변 선택: "We monitor cost and usage"
- 현재 상태: Cost Explorer 사용 중

### 6.2 비용 최적화 개선 계획

식별된 위험 항목:
1. **중위험**: Reserved Instance 활용 부족
2. **중위험**: 자동 스케일링 정책 최적화 필요
3. **저위험**: 사용하지 않는 리소스 정리 프로세스 부족

## 📊 실습 7: 종합 위험 평가 및 우선순위 설정

### 7.1 위험 항목 종합

Well-Architected Tool에서 **Review** 탭을 클릭하여 전체 위험 항목을 확인합니다.

#### 고위험 항목 (High Risk)
1. **보안**: 데이터베이스 암호화 미적용
   - 영향도: 높음
   - 구현 복잡도: 중간
   - 우선순위: 1

#### 중위험 항목 (Medium Risk)
1. **안정성**: 단일 리전 구성
   - 영향도: 높음
   - 구현 복잡도: 높음
   - 우선순위: 2

2. **보안**: WAF 미구성
   - 영향도: 중간
   - 구현 복잡도: 낮음
   - 우선순위: 3

3. **운영 우수성**: 자동화된 배포 파이프라인 부족
   - 영향도: 중간
   - 구현 복잡도: 중간
   - 우선순위: 4

4. **비용 최적화**: Reserved Instance 활용 부족
   - 영향도: 중간
   - 구현 복잡도: 낮음
   - 우선순위: 5

### 7.2 개선 로드맵 작성

#### Phase 1 (즉시 실행 - 1-2주)
1. **RDS 암호화 활성화**
   - 작업: 암호화된 스냅샷 생성 후 복원
   - 예상 시간: 4-6시간
   - 비용 영향: 없음

2. **WAF 구성**
   - 작업: CloudFront 및 ALB에 WAF 연결
   - 예상 시간: 2-3시간
   - 비용 영향: 월 $5-10

#### Phase 2 (단기 실행 - 1-2개월)
1. **Reserved Instance 구매**
   - 작업: 사용량 분석 후 RI 구매
   - 예상 시간: 1주일 (분석 포함)
   - 비용 영향: 30-50% 절약

2. **CI/CD 파이프라인 구축**
   - 작업: CodePipeline + CodeDeploy 구성
   - 예상 시간: 2-3주
   - 비용 영향: 월 $10-20

#### Phase 3 (중기 실행 - 3-6개월)
1. **다중 리전 아키텍처**
   - 작업: 재해 복구 리전 구성
   - 예상 시간: 1-2개월
   - 비용 영향: 50-70% 증가

## 📝 실습 8: 개선 계획 실행 (WAF 구성 예시)

### 8.1 AWS WAF 생성

1. **AWS Management Console**에서 **WAF & Shield**를 검색하고 선택합니다.

2. **Create web ACL**을 클릭합니다.

3. **Web ACL details** 설정:
   - Name: `ecommerce-waf`
   - Description: `WAF for e-commerce application`
   - CloudWatch metric name: `ecommerceWAF`

4. **Associated AWS resources** 설정:
   - Resource type: `CloudFront distribution` 선택
   - 기존 CloudFront 배포 선택

### 8.2 WAF 규칙 구성

1. **Add rules and rule groups**에서 **Add managed rule groups**를 클릭합니다.

2. **AWS managed rule groups** 선택:
   - `Core rule set`: 일반적인 웹 공격 차단
   - `Known bad inputs`: 알려진 악성 입력 차단
   - `SQL database`: SQL 인젝션 공격 차단

3. **Add rules**를 클릭합니다.

4. **Set rule priority**에서 규칙 우선순위를 설정합니다.

5. **Configure metrics**에서 CloudWatch 메트릭을 활성화합니다.

6. **Review and create web ACL**을 클릭합니다.

### 8.3 WAF 모니터링 설정

1. **CloudWatch**로 이동합니다.

2. **Dashboards**에서 새 대시보드를 생성합니다:
   - Name: `WAF-Monitoring`

3. **위젯 추가**:
   - **AllowedRequests**: 허용된 요청 수
   - **BlockedRequests**: 차단된 요청 수
   - **SampledRequests**: 샘플링된 요청

4. **알람 설정**:
   - 차단된 요청이 임계값을 초과할 때 알림

## 📊 실습 9: 개선 효과 측정

### 9.1 메트릭 수집

개선 사항 적용 후 다음 메트릭을 수집합니다:

#### 보안 메트릭
- WAF 차단 요청 수
- 보안 인시던트 감소율
- 취약점 스캔 결과

#### 성능 메트릭
- 응답 시간 개선
- 가용성 향상
- 오류율 감소

#### 비용 메트릭
- Reserved Instance 절약 금액
- 전체 인프라 비용 변화
- 비용 대비 성능 개선

### 9.2 Well-Architected Tool 재검토

1. **Well-Architected Tool**로 돌아갑니다.

2. **워크로드 선택** 후 **Start reviewing**을 클릭합니다.

3. **개선된 항목들을 반영**하여 질문에 다시 답변합니다.

4. **위험 수준 변화**를 확인합니다:
   - 고위험 → 중위험 또는 위험 없음
   - 중위험 → 저위험 또는 위험 없음

5. **개선 보고서**를 생성하고 저장합니다.

## 📋 실습 체크리스트

### 완료 확인 항목

- [ ] Well-Architected Tool에서 워크로드 생성 완료
- [ ] 5개 기둥별 질문 답변 완료
- [ ] 위험 항목 식별 및 분류 완료
- [ ] 우선순위가 지정된 개선 계획 수립 완료
- [ ] 최소 1개 개선 사항 실제 적용 완료 (WAF 구성)
- [ ] 개선 효과 측정 메트릭 설정 완료
- [ ] Well-Architected Tool 재검토 완료
- [ ] 개선 보고서 생성 및 저장 완료

### 추가 실습 (선택사항)

- [ ] RDS 암호화 활성화
- [ ] CloudTrail 로그 분석
- [ ] Cost Explorer를 통한 비용 분석
- [ ] Reserved Instance 구매 계획 수립
- [ ] 다중 AZ 배포 검토

## 🎯 실습 결과물

이 실습을 완료하면 다음과 같은 결과물을 얻게 됩니다:

1. **Well-Architected 검토 보고서**: 현재 아키텍처의 위험 평가
2. **우선순위 개선 계획**: 단계별 개선 로드맵
3. **실제 개선 사항**: WAF 구성을 통한 보안 강화
4. **모니터링 대시보드**: 개선 효과 측정 도구
5. **재검토 결과**: 개선 후 위험 수준 변화

## 💡 실습 팁

1. **현실적인 평가**: 과도하게 낙관적이거나 비관적이지 않게 현재 상태를 정확히 평가하세요.

2. **우선순위 설정**: 비즈니스 영향도와 구현 복잡도를 고려하여 우선순위를 설정하세요.

3. **점진적 개선**: 한 번에 모든 것을 개선하려 하지 말고 단계적으로 접근하세요.

4. **정기적 검토**: Well-Architected 검토는 일회성이 아닌 정기적인 프로세스입니다.

5. **팀 협업**: 다양한 팀의 관점을 반영하여 더 정확한 평가를 수행하세요.

## 🔗 다음 단계

이 실습을 완료한 후에는:

1. **정기적인 검토 일정** 수립 (분기별 또는 주요 변경 시)
2. **팀 교육** 계획 수립 (Well-Architected 원칙 공유)
3. **자동화 도구** 도입 검토 (AWS Config, Trusted Advisor 등)
4. **지속적인 개선** 문화 구축

Well-Architected Framework는 단순한 체크리스트가 아닌 지속적인 개선을 위한 프레임워크입니다. 정기적인 검토와 개선을 통해 더 나은 아키텍처를 구축해 나가세요!