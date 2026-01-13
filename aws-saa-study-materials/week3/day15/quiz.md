# Day 15 Quiz: Load Balancing & Auto Scaling

## 퀴즈 개요
- **주제**: Application Load Balancer와 Auto Scaling Group
- **문제 수**: 5문제
- **예상 소요 시간**: 10-15분
- **난이도**: 중급

---

## 문제 1: Application Load Balancer 특징

다음 중 Application Load Balancer(ALB)의 특징으로 **올바르지 않은** 것은?

A) OSI 7계층(Application Layer)에서 동작한다  
B) HTTP/HTTPS 트래픽을 처리할 수 있다  
C) 고정 IP 주소를 제공한다  
D) 경로 기반 라우팅을 지원한다  

### 정답: C

### 해설:
Application Load Balancer는 고정 IP 주소를 제공하지 않습니다. 고정 IP 주소를 제공하는 것은 Network Load Balancer(NLB)의 특징입니다.

- **A) 올바름**: ALB는 OSI 7계층에서 동작하여 HTTP 헤더, URL 경로 등을 기반으로 라우팅 결정을 할 수 있습니다.
- **B) 올바름**: ALB는 HTTP/HTTPS 트래픽 처리에 최적화되어 있습니다.
- **C) 틀림**: ALB는 DNS 이름을 제공하며, IP 주소는 동적으로 변경될 수 있습니다. 고정 IP가 필요한 경우 NLB를 사용해야 합니다.
- **D) 올바름**: ALB는 URL 경로에 따라 다른 Target Group으로 트래픽을 라우팅할 수 있습니다.

**관련 개념**: Load Balancer 종류, ALB vs NLB 차이점

---

## 문제 2: Auto Scaling 정책

다음 시나리오에서 가장 적합한 Auto Scaling 정책은?

**시나리오**: 전자상거래 웹사이트에서 평상시에는 CPU 사용률을 50% 수준으로 유지하고 싶지만, 트래픽이 급증할 때는 빠르게 대응하고 싶습니다.

A) Simple Scaling  
B) Step Scaling  
C) Target Tracking Scaling  
D) Scheduled Scaling  

### 정답: C

### 해설:
Target Tracking Scaling이 이 시나리오에 가장 적합합니다.

- **A) Simple Scaling**: 단일 임계값 기반으로 고정된 수만큼 확장/축소하므로, 세밀한 조정이 어렵습니다.
- **B) Step Scaling**: 여러 임계값을 설정할 수 있지만, 설정이 복잡하고 목표값 유지보다는 단계적 확장에 적합합니다.
- **C) 정답**: Target Tracking Scaling은 특정 메트릭(CPU 사용률 50%)의 목표값을 설정하면 자동으로 해당 값을 유지하도록 조정합니다. 설정이 간단하고 AWS에서 권장하는 방식입니다.
- **D) Scheduled Scaling**: 예측 가능한 트래픽 패턴에 적합하지만, 급작스러운 트래픽 변화에는 대응할 수 없습니다.

**관련 개념**: Auto Scaling 정책 종류, Target Tracking의 장점

---

## 문제 3: Health Check 설정

Auto Scaling Group에서 ELB Health Check를 활성화했을 때의 동작으로 **올바른** 것은?

A) EC2 Health Check만 사용하여 인스턴스 상태를 확인한다  
B) ELB Health Check가 실패하면 인스턴스를 즉시 종료한다  
C) ELB Health Check와 EC2 Health Check를 모두 사용하여 더 엄격하게 상태를 확인한다  
D) Health Check Grace Period 동안은 모든 Health Check를 무시한다  

### 정답: C

### 해설:
Auto Scaling Group에서 ELB Health Check를 활성화하면 ELB와 EC2 Health Check를 모두 사용합니다.

- **A) 틀림**: ELB Health Check를 활성화하면 EC2 Health Check와 함께 사용됩니다.
- **B) 틀림**: Health Check가 실패해도 즉시 종료되지 않습니다. Health Check Grace Period와 여러 번의 확인 과정을 거칩니다.
- **C) 정답**: ELB Health Check를 활성화하면 다음 두 조건을 모두 만족해야 인스턴스가 healthy로 간주됩니다:
  - EC2 Health Check: 인스턴스 자체가 running 상태
  - ELB Health Check: Load Balancer의 Target Group에서 healthy 상태
- **D) 틀림**: Health Check Grace Period는 새로 시작된 인스턴스에 대해서만 적용되며, 이 기간 동안 Health Check 실패로 인한 종료를 방지합니다.

**관련 개념**: Health Check 종류, Grace Period, ASG와 ELB 연동

---

## 문제 4: Target Group 구성

다음 중 Application Load Balancer의 Target Group에 등록할 수 **없는** 대상은?

A) EC2 인스턴스  
B) IP 주소 (온프레미스 서버)  
C) Lambda 함수  
D) CloudFront 배포  

### 정답: D

### 해설:
CloudFront 배포는 ALB의 Target Group에 직접 등록할 수 없습니다.

- **A) 가능**: EC2 인스턴스는 가장 일반적인 Target Group 대상입니다.
- **B) 가능**: IP 주소를 통해 온프레미스 서버나 다른 VPC의 리소스를 Target Group에 등록할 수 있습니다.
- **C) 가능**: Lambda 함수를 Target Group에 등록하여 서버리스 아키텍처를 구현할 수 있습니다.
- **D) 불가능**: CloudFront는 CDN 서비스로, ALB의 Target Group에 등록할 수 없습니다. 반대로 CloudFront의 Origin으로 ALB를 설정하는 것은 가능합니다.

**아키텍처 예시**:
```
사용자 → CloudFront → ALB → Target Group (EC2/Lambda/IP)
```

**관련 개념**: Target Group 대상 유형, CloudFront와 ALB 관계

---

## 문제 5: 시나리오 기반 문제

다음 시나리오를 읽고 가장 적절한 해결책을 선택하세요.

**시나리오**: 
온라인 게임 회사에서 다음과 같은 요구사항이 있습니다:
- 게임 API 서버는 매우 낮은 지연시간이 필요함
- 웹 관리 페이지는 일반적인 HTTP 트래픽
- 두 서비스 모두 고가용성이 필요함
- 트래픽 패턴이 예측 가능함 (오후 7-11시 피크)

이 요구사항을 만족하는 가장 적절한 아키텍처는?

A) ALB 하나로 경로 기반 라우팅을 사용하여 두 서비스 모두 처리  
B) 게임 API용 NLB와 웹 페이지용 ALB를 각각 구성  
C) NLB 하나로 포트 기반 라우팅을 사용하여 두 서비스 모두 처리  
D) ALB와 Scheduled Auto Scaling만 사용  

### 정답: B

### 해설:
각 서비스의 특성에 맞는 Load Balancer를 선택하는 것이 최적입니다.

**분석**:
- **게임 API**: 낮은 지연시간 필요 → NLB가 적합 (Layer 4, 마이크로초 단위 지연시간)
- **웹 관리 페이지**: HTTP 트래픽 → ALB가 적합 (Layer 7, HTTP 최적화)
- **고가용성**: 두 Load Balancer 모두 Multi-AZ 배포로 해결
- **예측 가능한 트래픽**: Scheduled Auto Scaling 추가 적용

**선택지 분석**:
- **A) 틀림**: ALB만 사용하면 게임 API의 낮은 지연시간 요구사항을 만족하기 어렵습니다.
- **B) 정답**: 각 서비스의 특성에 맞는 Load Balancer를 사용하는 최적의 아키텍처입니다.
- **C) 틀림**: NLB만 사용하면 웹 페이지의 HTTP 기능 (경로 기반 라우팅 등)을 활용하기 어렵습니다.
- **D) 틀림**: Load Balancer 선택이 부적절하고, Scheduled Scaling만으로는 예상치 못한 트래픽 변화에 대응할 수 없습니다.

**권장 아키텍처**:
```
게임 클라이언트 → NLB → 게임 API 서버 (ASG + Target Tracking)
웹 브라우저 → ALB → 웹 서버 (ASG + Scheduled + Target Tracking)
```

**관련 개념**: Load Balancer 선택 기준, 서비스별 요구사항 분석, 하이브리드 아키텍처

---

## 퀴즈 결과 분석

### 점수별 평가

- **5점 (100%)**: 🎉 완벽합니다! Load Balancing과 Auto Scaling 개념을 잘 이해하고 있습니다.
- **4점 (80%)**: 👍 우수합니다! 몇 가지 세부사항을 복습해보세요.
- **3점 (60%)**: 📚 양호합니다. 틀린 문제의 해설을 다시 읽어보세요.
- **2점 이하 (40% 이하)**: 💪 이론 내용을 다시 복습한 후 퀴즈를 재도전해보세요.

### 추가 학습 권장사항

**3번 문제를 틀린 경우**:
- Health Check 메커니즘과 Grace Period 개념 복습
- ASG와 ELB 연동 시 Health Check 동작 방식 학습

**4번 문제를 틀린 경우**:
- Target Group의 다양한 대상 유형 학습
- CloudFront와 ALB의 관계 및 아키텍처 패턴 복습

**5번 문제를 틀린 경우**:
- ALB vs NLB 선택 기준 복습
- 실제 시나리오에서의 아키텍처 설계 원칙 학습

### 다음 단계

1. **실습 진행**: Day 15 Hands-on Lab에서 실제로 ALB와 ASG를 구성해보세요.
2. **심화 학습**: AWS Well-Architected Framework의 성능 효율성 원칙 학습
3. **다음 주제 준비**: Day 16에서는 CloudFront와 CDN에 대해 학습합니다.

---

**퀴즈 완료 시간**: ___분 ___초  
**정답 개수**: ___/5  
**정답률**: ___%

수고하셨습니다! 🚀