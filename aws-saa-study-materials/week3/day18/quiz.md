# Day 18 퀴즈: API Gateway & Lambda

## 📝 퀴즈 개요

**주제**: API Gateway & Lambda 서버리스 컴퓨팅  
**문제 수**: 5문제  
**예상 소요 시간**: 15분  
**합격 기준**: 80% 이상 (4문제 이상 정답)

---

## 문제 1: Lambda 기본 개념 (난이도: ⭐⭐)

AWS Lambda에 대한 설명으로 **가장 적절하지 않은** 것은?

**A)** Lambda는 서버를 관리할 필요 없이 코드를 실행할 수 있는 서버리스 컴퓨팅 서비스이다  
**B)** Lambda 함수는 최대 15분까지 실행될 수 있다  
**C)** Lambda는 코드가 실행되지 않을 때도 지속적으로 비용이 발생한다  
**D)** Lambda는 다양한 AWS 서비스의 이벤트에 반응하여 자동으로 실행될 수 있다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: C**

**해설:**
- **C가 정답인 이유**: Lambda는 "사용한 만큼만 지불(Pay-as-you-go)" 모델을 사용합니다. 코드가 실행되지 않을 때는 비용이 발생하지 않으며, 실제 코드 실행 시간과 메모리 사용량에 대해서만 비용을 지불합니다.

- **다른 선택지 설명**:
  - **A**: 맞습니다. Lambda는 서버리스 컴퓨팅의 대표적인 서비스입니다.
  - **B**: 맞습니다. Lambda 함수의 최대 실행 시간은 15분입니다.
  - **D**: 맞습니다. S3, DynamoDB, API Gateway 등 다양한 서비스의 이벤트에 반응할 수 있습니다.

**관련 개념**: 서버리스 컴퓨팅, Lambda 과금 모델, 이벤트 기반 아키텍처
</details>

---

## 문제 2: API Gateway 유형 비교 (난이도: ⭐⭐⭐)

다음 시나리오에서 **가장 적합한** API Gateway 유형은?

**시나리오**: 간단한 마이크로서비스 API를 구축하려고 합니다. 복잡한 인증이나 요청 변환 기능은 필요하지 않고, 비용을 최소화하면서 빠른 성능을 원합니다.

**A)** REST API - 완전한 기능을 제공하므로 모든 상황에 적합  
**B)** HTTP API - 간단하고 비용 효율적이며 빠른 성능 제공  
**C)** WebSocket API - 실시간 통신에 최적화  
**D)** GraphQL API - 유연한 데이터 쿼리 지원

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B**

**해설:**
- **B가 정답인 이유**: HTTP API는 간단한 API 구축에 최적화되어 있으며, REST API 대비 약 70% 저렴하고 더 빠른 성능을 제공합니다. 복잡한 기능이 필요하지 않은 시나리오에 완벽하게 부합합니다.

- **다른 선택지 설명**:
  - **A**: REST API는 완전한 기능을 제공하지만 비용이 높고, 이 시나리오에서는 과도한 기능입니다.
  - **C**: WebSocket API는 실시간 양방향 통신이 필요할 때 사용하며, 이 시나리오와 맞지 않습니다.
  - **D**: GraphQL API는 API Gateway의 기본 유형이 아닙니다.

**관련 개념**: API Gateway 유형, HTTP API vs REST API, 비용 최적화
</details>

---

## 문제 3: Lambda 실행 환경 및 성능 (난이도: ⭐⭐⭐)

Lambda 함수의 Cold Start를 최소화하기 위한 **가장 효과적인** 방법은?

**A)** 함수 내부에서 매번 새로운 AWS SDK 클라이언트를 생성한다  
**B)** 함수의 메모리를 최소값인 128MB로 설정한다  
**C)** AWS SDK 클라이언트를 전역 변수로 선언하여 재사용한다  
**D)** 함수 실행 시간을 최대값인 15분으로 설정한다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: C**

**해설:**
- **C가 정답인 이유**: AWS SDK 클라이언트를 전역 변수로 선언하면 Lambda 컨테이너가 재사용될 때 클라이언트도 재사용되어 초기화 시간을 절약할 수 있습니다. 이는 Cold Start 시간을 줄이는 가장 일반적이고 효과적인 방법입니다.

- **다른 선택지 설명**:
  - **A**: 매번 새로운 클라이언트를 생성하면 오히려 성능이 저하됩니다.
  - **B**: 메모리를 너무 낮게 설정하면 CPU 성능도 낮아져 전체적인 실행 시간이 늘어날 수 있습니다.
  - **D**: 실행 시간 설정은 Cold Start와 직접적인 관련이 없습니다.

**관련 개념**: Lambda Cold Start, 성능 최적화, AWS SDK 재사용
</details>

---

## 문제 4: API Gateway 인증 방법 (난이도: ⭐⭐⭐⭐)

다음 중 **Lambda Authorizer**에 대한 설명으로 **올바른** 것은?

**A)** Lambda Authorizer는 AWS IAM 정책만 사용할 수 있다  
**B)** Lambda Authorizer는 JWT 토큰 검증을 위해 사용할 수 없다  
**C)** Lambda Authorizer는 커스텀 인증 로직을 구현할 수 있으며 외부 인증 시스템과 연동 가능하다  
**D)** Lambda Authorizer는 API Key 인증 방식과 동시에 사용할 수 없다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: C**

**해설:**
- **C가 정답인 이유**: Lambda Authorizer는 커스텀 인증 로직을 구현할 수 있는 가장 유연한 인증 방법입니다. JWT 토큰 검증, OAuth, 외부 인증 시스템 연동 등 다양한 인증 방식을 구현할 수 있습니다.

- **다른 선택지 설명**:
  - **A**: Lambda Authorizer는 IAM 정책뿐만 아니라 다양한 인증 방식을 지원합니다.
  - **B**: JWT 토큰 검증은 Lambda Authorizer의 대표적인 사용 사례 중 하나입니다.
  - **D**: Lambda Authorizer와 API Key는 서로 다른 인증 레이어에서 동작하므로 함께 사용할 수 있습니다.

**관련 개념**: Lambda Authorizer, 커스텀 인증, JWT 토큰, 외부 인증 시스템 연동
</details>

---

## 문제 5: 서버리스 아키텍처 시나리오 (난이도: ⭐⭐⭐⭐)

다음 요구사항을 만족하는 서버리스 아키텍처를 설계할 때, **가장 적절한** 구성은?

**요구사항**:
- 사용자가 이미지를 업로드하면 자동으로 썸네일을 생성
- 썸네일 생성 완료 시 사용자에게 이메일 알림 발송
- 이미지 메타데이터를 데이터베이스에 저장

**A)** S3 → Lambda → DynamoDB → SES  
**B)** S3 → Lambda → DynamoDB → SNS → Lambda → SES  
**C)** API Gateway → Lambda → S3 → DynamoDB → SES  
**D)** CloudFront → S3 → Lambda → RDS → SES

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B**

**해설:**
- **B가 정답인 이유**: 이벤트 기반 서버리스 아키텍처의 모범 사례를 따릅니다:
  1. **S3**: 이미지 업로드 시 이벤트 발생
  2. **Lambda**: 썸네일 생성 및 메타데이터 처리
  3. **DynamoDB**: 메타데이터 저장 (서버리스 데이터베이스)
  4. **SNS**: 비동기 알림 처리 (디커플링)
  5. **Lambda**: 이메일 발송 처리
  6. **SES**: 실제 이메일 발송

- **다른 선택지 설명**:
  - **A**: SNS 없이 직접 SES를 호출하면 결합도가 높아지고 확장성이 떨어집니다.
  - **C**: API Gateway는 이 시나리오에서 불필요하며, 이미지 업로드는 S3 직접 업로드가 더 효율적입니다.
  - **D**: CloudFront는 CDN 서비스이고, RDS는 서버리스 아키텍처에 적합하지 않습니다.

**관련 개념**: 이벤트 기반 아키텍처, 서버리스 패턴, 비동기 처리, 서비스 디커플링
</details>

---

## 📊 퀴즈 결과 분석

### 점수별 평가

- **5점 (100%)**: 🏆 완벽! 서버리스 아키텍처 전문가 수준
- **4점 (80%)**: 🎉 우수! SAA-C03 시험 준비 완료
- **3점 (60%)**: 📚 양호! 추가 학습 후 재도전 권장
- **2점 이하 (40% 이하)**: 🔄 이론 복습 후 퀴즈 재응시 필요

### 틀린 문제가 있다면...

**문제 1-2번을 틀렸다면**: Lambda와 API Gateway 기본 개념 복습  
**문제 3번을 틀렸다면**: Lambda 성능 최적화 부분 재학습  
**문제 4번을 틀렸다면**: API Gateway 인증 방법들 비교 학습  
**문제 5번을 틀렸다면**: 서버리스 아키텍처 패턴 실습 권장

---

## 🎯 핵심 복습 포인트

### 1. Lambda 핵심 개념
- 서버리스 컴퓨팅의 특징
- 이벤트 기반 실행 모델
- 사용량 기반 과금 구조
- Cold Start 최적화 방법

### 2. API Gateway 유형별 특징
- REST API: 완전한 기능, 높은 비용
- HTTP API: 간단한 기능, 저렴한 비용
- 적절한 유형 선택 기준

### 3. 인증 및 보안
- IAM 인증
- API Key 인증
- Cognito User Pool
- Lambda Authorizer (커스텀 인증)

### 4. 서버리스 아키텍처 패턴
- 이벤트 기반 처리
- 비동기 메시징 (SNS/SQS)
- 서비스 디커플링
- 확장 가능한 설계

---

## 📚 추가 학습 자료

- [AWS Lambda 모범 사례](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [API Gateway 개발자 가이드](https://docs.aws.amazon.com/apigateway/latest/developerguide/)
- [서버리스 애플리케이션 렌즈](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/)
- [Lambda 성능 최적화 가이드](https://aws.amazon.com/blogs/compute/operating-lambda-performance-optimization-part-1/)

수고하셨습니다! 🎉 다음 Day 19에서는 컨테이너 서비스인 ECS, EKS, Fargate에 대해 학습하겠습니다.