# Day 20 퀴즈: AWS 배포 및 관리 도구

## 퀴즈 개요
- **주제**: AWS CodePipeline, CodeDeploy, CodeCommit, CodeBuild, Infrastructure as Code
- **문제 수**: 5문제
- **예상 소요 시간**: 10분
- **난이도**: 중급

---

## 문제 1: CodeDeploy 배포 전략 (다중 선택)

**시나리오**: 온라인 쇼핑몰 웹사이트를 운영하는 회사에서 새로운 기능을 배포해야 합니다. 배포 중 서비스 중단을 최소화하면서도 문제 발생 시 빠른 롤백이 가능한 전략을 선택해야 합니다.

**질문**: 이 요구사항을 만족하는 가장 적절한 Route 53 라우팅 정책은 무엇입니까?

A) In-place 배포 (All-at-once)
B) In-place 배포 (Rolling)
C) Blue/Green 배포
D) Canary 배포

<details>
<summary>정답 및 해설 보기</summary>

**정답: C) Blue/Green 배포**

**해설**: 
Blue/Green 배포는 새로운 환경(Green)에 애플리케이션을 배포한 후 로드 밸런서를 통해 트래픽을 전환하는 방식입니다. 이 방식의 장점은:
- **무중단 배포**: 기존 환경(Blue)이 계속 서비스하는 동안 새 환경 준비
- **빠른 롤백**: 문제 발생 시 트래픽을 즉시 기존 환경으로 되돌림
- **완전한 테스트**: 새 환경에서 충분한 테스트 후 전환 가능

In-place 배포는 기존 인스턴스에서 업데이트하므로 다운타임이 발생할 수 있고, Canary 배포는 점진적 배포이지만 Blue/Green만큼 빠른 롤백은 어렵습니다.
</details>

---

## 문제 2: CodePipeline 구성 요소 (단일 선택)

**시나리오**: 개발팀에서 다음과 같은 CI/CD 워크플로우를 구현하려고 합니다:
1. 개발자가 코드를 Git 저장소에 푸시
2. 자동으로 코드 빌드 및 테스트 실행
3. 테스트 통과 시 스테이징 환경에 배포
4. 수동 승인 후 프로덕션 환경에 배포

**질문**: 위 워크플로우를 CodePipeline으로 구현할 때 필요한 스테이지들을 올바른 순서로 나열한 것은?

A) Source → Build → Test → Deploy → Approval
B) Source → Build → Deploy → Test → Approval
C) Source → Build → Test → Approval → Deploy
D) Build → Source → Test → Approval → Deploy

<details>
<summary>정답 및 해설 보기</summary>

**정답: C) Source → Build → Test → Approval → Deploy**

**해설**:
CodePipeline의 올바른 스테이지 순서는:
1. **Source**: Git 저장소에서 소스 코드 가져오기
2. **Build**: 코드 빌드 및 테스트 실행 (CodeBuild 사용)
3. **Test**: 추가적인 통합 테스트 (선택사항)
4. **Approval**: 수동 승인 단계 (프로덕션 배포 전)
5. **Deploy**: 최종 배포 (CodeDeploy 사용)

승인(Approval) 단계는 배포 전에 위치해야 하며, 빌드와 테스트는 배포보다 먼저 수행되어야 합니다.
</details>

---

## 문제 3: Infrastructure as Code 비교 (단일 선택)

**시나리오**: 스타트업 회사에서 AWS 인프라를 코드로 관리하려고 합니다. 개발팀은 TypeScript에 익숙하며, 기존 프로그래밍 패러다임을 활용하여 인프라를 정의하고 싶어합니다.

**질문**: 위 요구사항에 가장 적합한 Infrastructure as Code 도구는 무엇입니까?

A) AWS CloudFormation (JSON 템플릿)
B) AWS CloudFormation (YAML 템플릿)
C) AWS CDK (Cloud Development Kit)
D) Terraform

<details>
<summary>정답 및 해설 보기</summary>

**정답: C) AWS CDK (Cloud Development Kit)**

**해설**:
AWS CDK는 익숙한 프로그래밍 언어(TypeScript, Python, Java 등)를 사용하여 클라우드 인프라를 정의할 수 있는 도구입니다.

**CDK의 장점**:
- **프로그래밍 언어 사용**: TypeScript, Python, Java, C# 등 지원
- **재사용성**: 클래스와 메서드를 통한 코드 재사용
- **IDE 지원**: 자동 완성, 타입 체크 등
- **추상화**: 고수준 구성 요소(Construct) 제공

CloudFormation은 선언적 템플릿 방식이고, Terraform은 HCL 언어를 사용하므로 기존 프로그래밍 패러다임 활용에는 CDK가 가장 적합합니다.
</details>

---

## 문제 4: Systems Manager Parameter Store (시나리오 기반)

**시나리오**: 마이크로서비스 아키텍처를 사용하는 애플리케이션에서 다음과 같은 구성 정보를 관리해야 합니다:
- 데이터베이스 연결 문자열 (민감하지 않음)
- API 키 (민감함)
- 환경별 설정값 (개발/스테이징/프로덕션)

**질문**: AWS Systems Manager Parameter Store를 사용할 때, 위 요구사항을 만족하는 올바른 구성은 무엇입니까?

A) 모든 파라미터를 Standard 파라미터로 저장하고 IAM으로 접근 제어
B) 데이터베이스 연결 문자열은 Standard, API 키는 SecureString으로 저장하고 계층적 구조 사용
C) 모든 파라미터를 SecureString으로 저장하고 환경별로 별도 AWS 계정 사용
D) AWS Secrets Manager만 사용하고 Parameter Store는 사용하지 않음

<details>
<summary>정답 및 해설 보기</summary>

**정답: B) 데이터베이스 연결 문자열은 Standard, API 키는 SecureString으로 저장하고 계층적 구조 사용**

**해설**:
Parameter Store의 올바른 사용법:

**파라미터 타입**:
- **Standard**: 민감하지 않은 구성 정보 (데이터베이스 연결 문자열)
- **SecureString**: 민감한 정보 (API 키, 암호) - KMS로 암호화

**계층적 구조 예시**:
```
/myapp/dev/database/connection-string
/myapp/dev/api/key
/myapp/staging/database/connection-string
/myapp/staging/api/key
/myapp/prod/database/connection-string
/myapp/prod/api/key
```

이 방식은 비용 효율적이면서도 보안 요구사항을 만족하며, 환경별 구성 관리가 용이합니다.
</details>

---

## 문제 5: CodeBuild buildspec.yml (실습 기반)

**시나리오**: Node.js 웹 애플리케이션을 위한 CodeBuild 프로젝트를 설정하고 있습니다. 빌드 과정에서 다음 작업들을 수행해야 합니다:
1. Node.js 의존성 설치
2. 단위 테스트 실행
3. 애플리케이션 빌드
4. Docker 이미지 생성 및 ECR에 푸시

**질문**: 위 요구사항을 만족하는 buildspec.yml 파일의 올바른 구조는 무엇입니까?

A)
```yaml
version: 0.2
phases:
  build:
    commands:
      - npm install
      - npm test
      - npm run build
      - docker build -t myapp .
      - docker push myapp
```

B)
```yaml
version: 0.2
phases:
  pre_build:
    commands:
      - npm install
  build:
    commands:
      - npm test
      - npm run build
  post_build:
    commands:
      - docker build -t myapp .
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/myapp:latest
```

C)
```yaml
version: 0.2
phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - npm install
  build:
    commands:
      - npm test
      - npm run build
      - docker build -t myapp .
      - docker tag myapp:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/myapp:latest
  post_build:
    commands:
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/myapp:latest
```

D)
```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      nodejs: 18
  build:
    commands:
      - npm install && npm test && npm run build
      - docker build -t myapp . && docker push myapp
```

<details>
<summary>정답 및 해설 보기</summary>

**정답: C)**
```yaml
version: 0.2
phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - npm install
  build:
    commands:
      - npm test
      - npm run build
      - docker build -t myapp .
      - docker tag myapp:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/myapp:latest
  post_build:
    commands:
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/myapp:latest
```

**해설**:
올바른 buildspec.yml 구조는 다음과 같습니다:

**pre_build 단계**:
- ECR 로그인 (Docker 이미지 푸시를 위해 필요)
- 의존성 설치 (npm install)

**build 단계**:
- 테스트 실행 (npm test)
- 애플리케이션 빌드 (npm run build)
- Docker 이미지 생성 및 태깅

**post_build 단계**:
- ECR에 이미지 푸시

**다른 선택지의 문제점**:
- A) ECR 로그인 없음, 단계 구분 없음
- B) ECR 로그인 없음, 이미지 태깅 없음
- D) 단계 구분이 부적절하고 ECR 로그인 없음
</details>

---

## 퀴즈 결과 분석

### 점수 계산
- 각 문제당 20점 (총 100점)
- 80점 이상: 우수
- 60점 이상: 보통
- 60점 미만: 추가 학습 필요

### 추가 학습이 필요한 영역

**1-2문제 틀린 경우**:
- CodeDeploy 배포 전략 비교 학습
- CodePipeline 스테이지 구성 복습

**3-4문제 틀린 경우**:
- Infrastructure as Code 도구들 특징 비교
- Systems Manager 서비스 전반 학습
- buildspec.yml 작성법 실습

**5문제 모두 틀린 경우**:
- Day 20 이론 내용 전체 복습
- 실습 가이드 다시 수행
- AWS Developer Tools 공식 문서 학습

### 다음 학습 준비
내일은 Week 3의 마지막 날로 주간 복습과 마이크로서비스 아키텍처 구축 실습을 진행합니다. 오늘 학습한 CI/CD 도구들을 실제 프로젝트에 적용해보는 시간을 가질 예정입니다.

---

## 정답 요약
1. **C) Blue/Green 배포** - 무중단 배포와 빠른 롤백 지원
2. **C) Source → Build → Test → Approval → Deploy** - 올바른 파이프라인 순서
3. **C) AWS CDK** - 프로그래밍 언어를 활용한 IaC
4. **B) Standard와 SecureString 조합 + 계층적 구조** - 보안과 효율성 균형
5. **C) 완전한 buildspec.yml 구조** - ECR 로그인 포함한 전체 빌드 프로세스