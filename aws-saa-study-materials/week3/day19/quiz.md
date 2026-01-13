# Day 19 퀴즈: ECS, EKS, Fargate

## 📝 퀴즈 개요

**주제**: AWS 컨테이너 서비스 (ECS, EKS, Fargate)  
**문제 수**: 5문제  
**예상 소요 시간**: 10분  
**합격 기준**: 80% 이상 (4문제 이상 정답)

---

## 문제 1

**AWS ECS의 핵심 구성 요소에 대한 설명으로 올바른 것은?**

A) Task Definition은 실행 중인 컨테이너 인스턴스를 의미한다  
B) Service는 원하는 수의 Task를 유지하고 로드 밸런서와 통합할 수 있다  
C) Cluster는 단일 가용 영역에서만 생성할 수 있다  
D) Task는 여러 개의 Task Definition을 포함할 수 있다

<details>
<summary>정답 및 해설</summary>

**정답: B**

**해설:**
- **A) 틀림**: Task Definition은 컨테이너 실행을 위한 청사진(blueprint)이며, 실행 중인 인스턴스는 Task입니다.
- **B) 정답**: Service는 원하는 수의 Task를 유지하고, Application Load Balancer나 Network Load Balancer와 통합하여 트래픽을 분산할 수 있습니다.
- **C) 틀림**: Cluster는 여러 가용 영역에 걸쳐 생성할 수 있으며, 고가용성을 위해 권장됩니다.
- **D) 틀림**: Task는 하나의 Task Definition을 기반으로 생성되며, 여러 개의 컨테이너를 포함할 수 있습니다.

**관련 개념**: ECS 아키텍처, Service 관리, Task Definition
</details>

---

## 문제 2

**다음 시나리오에서 가장 적합한 AWS 컨테이너 서비스는?**

*"기존에 Kubernetes를 사용하던 팀이 AWS로 마이그레이션하려고 합니다. 기존 Kubernetes 매니페스트와 kubectl 명령어를 그대로 사용하고 싶어하며, 멀티 클라우드 환경도 고려하고 있습니다."*

A) Amazon ECS with EC2 launch type  
B) Amazon ECS with Fargate launch type  
C) Amazon EKS  
D) AWS Batch

<details>
<summary>정답 및 해설</summary>

**정답: C**

**해설:**
Amazon EKS가 가장 적합한 선택입니다:

- **기존 Kubernetes 경험 활용**: EKS는 표준 Kubernetes API를 제공하므로 기존 매니페스트와 kubectl 명령어를 그대로 사용할 수 있습니다.
- **멀티 클라우드 호환성**: Kubernetes는 클라우드 중립적인 플랫폼이므로 다른 클라우드로의 이식성이 높습니다.
- **표준 준수**: CNCF 인증을 받은 표준 Kubernetes 환경을 제공합니다.

**다른 옵션들:**
- **A, B) ECS**: AWS 전용 서비스로 Kubernetes 매니페스트를 직접 사용할 수 없습니다.
- **D) AWS Batch**: 배치 작업 전용 서비스로 일반적인 컨테이너 오케스트레이션에는 적합하지 않습니다.

**관련 개념**: EKS vs ECS 비교, Kubernetes 이식성, 멀티 클라우드 전략
</details>

---

## 문제 3

**AWS Fargate에 대한 설명으로 틀린 것은?**

A) 서버리스 컨테이너 플랫폼으로 EC2 인스턴스를 관리할 필요가 없다  
B) ECS와 EKS 모두에서 사용할 수 있다  
C) 사용한 CPU와 메모리 리소스에 대해서만 비용을 지불한다  
D) 컨테이너에 직접 SSH 접속이 가능하다

<details>
<summary>정답 및 해설</summary>

**정답: D**

**해설:**
**D) 틀림**: Fargate는 서버리스 플랫폼으로, 기본 인프라에 대한 직접적인 접근을 제공하지 않습니다. 컨테이너에 SSH로 직접 접속할 수 없으며, 디버깅이나 문제 해결을 위해서는 CloudWatch Logs나 ECS Exec 기능을 사용해야 합니다.

**올바른 설명들:**
- **A) 정답**: Fargate는 완전 관리형 서비스로 EC2 인스턴스 관리가 불필요합니다.
- **B) 정답**: ECS와 EKS 모두에서 Fargate를 launch type으로 선택할 수 있습니다.
- **C) 정답**: 실제 사용한 vCPU와 메모리에 대해서만 초 단위로 과금됩니다.

**관련 개념**: Fargate 특징, 서버리스 컨테이너, ECS Exec
</details>

---

## 문제 4

**다음 중 ECS Task Definition에서 설정할 수 있는 항목이 아닌 것은?**

A) 컨테이너 이미지 URI  
B) CPU 및 메모리 할당량  
C) 환경 변수  
D) Auto Scaling 정책

<details>
<summary>정답 및 해설</summary>

**정답: D**

**해설:**
**D) 정답**: Auto Scaling 정책은 Task Definition이 아닌 ECS Service 레벨에서 설정됩니다. Task Definition은 컨테이너 실행을 위한 청사진 역할을 하며, 스케일링 정책은 Service가 관리합니다.

**Task Definition에서 설정 가능한 항목들:**
- **A) 컨테이너 이미지 URI**: 사용할 Docker 이미지 지정
- **B) CPU 및 메모리 할당량**: 태스크와 컨테이너별 리소스 할당
- **C) 환경 변수**: 컨테이너 실행 시 필요한 환경 변수 설정
- 포트 매핑, 볼륨 마운트, 로깅 설정, IAM 역할 등

**ECS Service에서 설정하는 항목들:**
- Auto Scaling 정책
- 로드 밸런서 연동
- 배포 전략
- 서비스 디스커버리

**관련 개념**: Task Definition vs Service, ECS 구성 요소 역할 분담
</details>

---

## 문제 5

**다음 시나리오에서 가장 비용 효율적인 ECS 실행 옵션은?**

*"웹 애플리케이션이 하루 중 특정 시간대(오전 9시-오후 6시)에만 높은 트래픽을 받고, 나머지 시간에는 거의 사용되지 않습니다. 트래픽 패턴이 예측 가능하며, 인프라 관리에 시간을 투자하고 싶지 않습니다."*

A) ECS with EC2 launch type + Spot Instances  
B) ECS with EC2 launch type + Reserved Instances  
C) ECS with Fargate + Auto Scaling  
D) EKS with EC2 Spot Instances

<details>
<summary>정답 및 해설</summary>

**정답: C**

**해설:**
이 시나리오에서는 **ECS with Fargate + Auto Scaling**이 가장 적합합니다:

**선택 이유:**
1. **서버리스**: 인프라 관리 불필요 (요구사항 충족)
2. **사용량 기반 과금**: 실제 사용한 리소스에 대해서만 지불
3. **자동 스케일링**: 트래픽 패턴에 따라 자동으로 확장/축소
4. **즉시 시작**: 트래픽 증가 시 빠른 스케일 아웃 가능

**다른 옵션들의 문제점:**
- **A) EC2 + Spot**: 인프라 관리 필요, Spot 인스턴스 중단 위험
- **B) EC2 + Reserved**: 24시간 고정 비용, 유휴 시간 비용 낭비
- **D) EKS + Spot**: 복잡한 설정, 인프라 관리 필요

**비용 최적화 포인트:**
- 트래픽이 없는 시간에는 태스크 수를 0에 가깝게 축소
- 사용한 만큼만 지불하는 Fargate의 과금 모델 활용
- Auto Scaling으로 리소스 낭비 최소화

**관련 개념**: 비용 최적화, Auto Scaling, Fargate 과금 모델
</details>

---

## 📊 퀴즈 결과 분석

### 점수별 해석

- **5점 (100%)**: 완벽! AWS 컨테이너 서비스에 대한 깊은 이해를 보여줍니다.
- **4점 (80%)**: 우수! 대부분의 개념을 잘 이해하고 있습니다.
- **3점 (60%)**: 보통! 기본 개념은 이해했지만 추가 학습이 필요합니다.
- **2점 이하 (40% 이하)**: 이론 내용을 다시 복습하고 실습을 통해 이해를 높이세요.

### 틀린 문제가 있다면...

1. **문제 1번 틀림**: ECS 구성 요소와 역할 관계 재학습
2. **문제 2번 틀림**: ECS vs EKS 선택 기준 복습
3. **문제 3번 틀림**: Fargate 특징과 제약사항 확인
4. **문제 4번 틀림**: Task Definition vs Service 역할 구분 학습
5. **문제 5번 틀림**: 비용 최적화 전략과 사용 사례 분석 복습

## 🎯 추가 학습 권장사항

### 점수가 낮은 경우 (3점 이하)
1. 이론 내용 재학습 (특히 ECS 구성 요소)
2. AWS 공식 문서의 ECS/EKS 시작 가이드 읽기
3. 실습 가이드를 따라 직접 실습 수행

### 점수가 높은 경우 (4-5점)
1. 고급 주제 학습: Service Mesh, CI/CD 통합
2. 실제 프로젝트에 컨테이너 서비스 적용
3. 다른 AWS 서비스와의 통합 패턴 학습

## 🔗 관련 학습 자료

- [AWS ECS 공식 문서](https://docs.aws.amazon.com/ecs/)
- [AWS EKS 공식 문서](https://docs.aws.amazon.com/eks/)
- [AWS Fargate 공식 문서](https://docs.aws.amazon.com/fargate/)
- [컨테이너 보안 모범 사례](https://aws.amazon.com/blogs/containers/)

---

**다음 학습**: [Day 20 - 배포 및 관리 도구](../day20/README.md)로 이어집니다!