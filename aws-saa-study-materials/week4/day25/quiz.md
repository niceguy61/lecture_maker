# Day 25 퀴즈: AWS Well-Architected Framework

## 📝 퀴즈 개요

**주제**: AWS Well-Architected Framework  
**문제 수**: 5문제  
**예상 소요 시간**: 10-15분  
**합격 기준**: 80% 이상 (4문제 이상 정답)

---

## 문제 1

**AWS Well-Architected Framework의 5개 기둥에 포함되지 않는 것은?**

A) 운영 우수성 (Operational Excellence)  
B) 보안 (Security)  
C) 확장성 (Scalability)  
D) 안정성 (Reliability)  
E) 성능 효율성 (Performance Efficiency)

<details>
<summary>정답 및 해설</summary>

**정답: C) 확장성 (Scalability)**

**해설**: 
AWS Well-Architected Framework의 5개 기둥은 다음과 같습니다:
1. 운영 우수성 (Operational Excellence)
2. 보안 (Security)
3. 안정성 (Reliability)
4. 성능 효율성 (Performance Efficiency)
5. 비용 최적화 (Cost Optimization)

확장성(Scalability)은 별도의 기둥이 아니라 안정성과 성능 효율성 기둥에서 다루는 개념입니다. 확장성은 수요 변화에 따라 리소스를 늘리거나 줄일 수 있는 능력을 의미하며, Auto Scaling, Elastic Load Balancing 등의 서비스를 통해 구현됩니다.

**관련 개념**: Well-Architected Framework 기본 구조, 5개 기둥의 정의
</details>

---

## 문제 2

**Well-Architected Framework의 "보안" 기둥에서 강조하는 핵심 설계 원칙이 아닌 것은?**

A) 강력한 자격 증명 기반 구현  
B) 추적 가능성 활성화  
C) 모든 계층에서 보안 적용  
D) 수평적 확장을 통한 가용성 증대  
E) 전송 중 및 저장 시 데이터 보호

<details>
<summary>정답 및 해설</summary>

**정답: D) 수평적 확장을 통한 가용성 증대**

**해설**: 
"수평적 확장을 통한 가용성 증대"는 안정성(Reliability) 기둥의 핵심 설계 원칙입니다.

보안 기둥의 핵심 설계 원칙은 다음과 같습니다:
- 강력한 자격 증명 기반 구현 (최소 권한 원칙)
- 추적 가능성 활성화 (모든 작업과 변경 사항 로깅)
- 모든 계층에서 보안 적용 (심층 방어 전략)
- 보안 모범 사례 자동화
- 전송 중 및 저장 시 데이터 보호
- 데이터에 대한 사람의 접근 최소화
- 보안 이벤트 대비

각 기둥은 고유한 설계 원칙과 모범 사례를 가지고 있으며, 이를 정확히 구분하여 이해하는 것이 중요합니다.

**관련 개념**: 보안 기둥 설계 원칙, 심층 방어, 최소 권한 원칙
</details>

---

## 문제 3

**다음 시나리오에서 Well-Architected Framework의 어떤 기둥을 우선적으로 검토해야 할까요?**

**시나리오**: 온라인 쇼핑몰 애플리케이션에서 블랙 프라이데이 세일 기간 동안 트래픽이 평소의 10배로 증가했습니다. 일부 사용자들이 페이지 로딩 속도가 느리다고 불만을 제기하고 있으며, 데이터베이스 연결 타임아웃 오류가 간헐적으로 발생하고 있습니다.

A) 운영 우수성 (Operational Excellence)  
B) 보안 (Security)  
C) 안정성 (Reliability)  
D) 성능 효율성 (Performance Efficiency)  
E) 비용 최적화 (Cost Optimization)

<details>
<summary>정답 및 해설</summary>

**정답: D) 성능 효율성 (Performance Efficiency)**

**해설**: 
이 시나리오는 성능 효율성 기둥과 관련된 문제입니다.

**문제 분석**:
- 트래픽 10배 증가 → 부하 증가
- 페이지 로딩 속도 저하 → 성능 문제
- 데이터베이스 연결 타임아웃 → 리소스 부족

**성능 효율성 기둥에서 다뤄야 할 사항**:
1. **컴퓨팅 리소스 최적화**: Auto Scaling 설정 검토
2. **데이터베이스 성능**: 읽기 전용 복제본, 연결 풀링
3. **캐싱 전략**: CloudFront, ElastiCache 활용
4. **로드 밸런싱**: 트래픽 분산 최적화

**다른 기둥과의 연관성**:
- 안정성(C): 시스템이 완전히 다운되지 않았으므로 2순위
- 비용 최적화(E): 성능 문제 해결 후 고려
- 운영 우수성(A): 모니터링 및 대응 프로세스 개선
- 보안(B): 현재 시나리오와 직접적 연관성 낮음

**관련 개념**: 성능 효율성, Auto Scaling, 데이터베이스 최적화, 캐싱
</details>

---

## 문제 4

**AWS Well-Architected Tool에 대한 설명으로 올바른 것은?**

A) 유료 서비스로, 엔터프라이즈 지원 플랜에서만 사용 가능하다  
B) 아키텍처 검토 후 자동으로 리소스를 최적화해준다  
C) 5개 기둥별 질문에 답변하여 위험을 평가하고 개선 권장 사항을 제공한다  
D) 오직 AWS 파트너만 사용할 수 있는 도구이다  
E) 실시간으로 아키텍처를 모니터링하고 알람을 발송한다

<details>
<summary>정답 및 해설</summary>

**정답: C) 5개 기둥별 질문에 답변하여 위험을 평가하고 개선 권장 사항을 제공한다**

**해설**: 
AWS Well-Architected Tool의 특징과 기능을 정확히 이해해야 합니다.

**올바른 설명 (정답)**:
- 5개 기둥별로 구조화된 질문 제공
- 답변을 바탕으로 위험 수준 평가 (고위험, 중위험, 위험 없음)
- 우선순위가 지정된 개선 권장 사항 제공
- 시간 경과에 따른 개선 사항 추적 가능

**잘못된 설명들**:
- A) **무료 서비스**이며, 모든 AWS 계정에서 사용 가능
- B) 권장 사항만 제공하며, **자동 최적화는 수행하지 않음**
- D) **모든 AWS 사용자**가 사용 가능 (파트너 전용 아님)
- E) **정적 검토 도구**이며, 실시간 모니터링 기능 없음

**Well-Architected Tool 사용 프로세스**:
1. 워크로드 정의
2. 아키텍처 검토 (질문 답변)
3. 위험 평가 및 우선순위 설정
4. 개선 계획 수립
5. 정기적 재검토

**관련 개념**: Well-Architected Tool 기능, 아키텍처 검토 프로세스
</details>

---

## 문제 5

**다음 중 "비용 최적화" 기둥의 모범 사례로 가장 적절하지 않은 것은?**

A) 클라우드 재무 관리 구현을 통한 조직 전반의 재무 책임 확립  
B) 소비 모델 채택으로 필요한 만큼만 지불  
C) 모든 데이터를 최고 성능의 스토리지 클래스에 저장  
D) 차별화되지 않는 작업에 대한 지출 중단 (관리형 서비스 활용)  
E) 지출 분석 및 귀속을 통한 정확한 비용 추적

<details>
<summary>정답 및 해설</summary>

**정답: C) 모든 데이터를 최고 성능의 스토리지 클래스에 저장**

**해설**: 
비용 최적화 기둥의 핵심은 **적절한 리소스를 적절한 비용으로 사용**하는 것입니다.

**잘못된 접근 (정답)**:
- 모든 데이터를 최고 성능 스토리지에 저장하는 것은 **과도한 비용 발생**
- 데이터 액세스 패턴에 따라 **적절한 스토리지 클래스 선택**이 필요
- 예: S3 Standard → S3 IA → S3 Glacier → S3 Deep Archive

**올바른 비용 최적화 모범 사례**:

**A) 클라우드 재무 관리**:
- FinOps 문화 구축
- 비용 거버넌스 프로세스
- 팀별 비용 책임 할당

**B) 소비 모델 채택**:
- Pay-as-you-use 모델 활용
- Reserved Instance, Savings Plans
- Spot Instance 활용

**D) 관리형 서비스 활용**:
- 운영 오버헤드 감소
- 인프라 관리 비용 절약
- 예: RDS vs EC2 + 직접 DB 설치

**E) 지출 분석 및 귀속**:
- 태깅 전략 구현
- Cost Explorer 활용
- 부서별/프로젝트별 비용 추적

**스토리지 최적화 예시**:
- 자주 액세스: S3 Standard
- 가끔 액세스: S3 Standard-IA
- 아카이브: S3 Glacier
- 장기 보관: S3 Deep Archive

**관련 개념**: 비용 최적화 원칙, 스토리지 클래스 선택, FinOps
</details>

---

## 📊 퀴즈 결과 분석

### 점수별 해석

**5점 (100%)**: 🎉 완벽합니다!
- Well-Architected Framework를 매우 잘 이해하고 있습니다
- 실무에서 아키텍처 검토를 주도할 수 있는 수준입니다

**4점 (80%)**: ✅ 우수합니다!
- 핵심 개념을 잘 이해하고 있습니다
- 실습을 통해 실무 경험을 쌓아보세요

**3점 (60%)**: ⚠️ 보통입니다
- 기본 개념은 이해했지만 심화 학습이 필요합니다
- 이론 내용을 다시 한 번 복습해보세요

**2점 이하 (40% 이하)**: 📚 추가 학습 필요
- Well-Architected Framework 이론을 다시 학습하세요
- 실습 가이드를 따라 직접 체험해보세요

### 틀린 문제별 추가 학습 가이드

**문제 1번을 틀렸다면**:
- Well-Architected Framework 5개 기둥 정의 복습
- 각 기둥의 핵심 목적과 범위 이해

**문제 2번을 틀렸다면**:
- 각 기둥별 설계 원칙 상세 학습
- 보안 기둥의 심층 방어 전략 이해

**문제 3번을 틀렸다면**:
- 실제 시나리오와 기둥 매핑 연습
- 성능 효율성과 안정성 기둥의 차이점 이해

**문제 4번을 틀렸다면**:
- Well-Architected Tool 실습 수행
- 도구의 기능과 한계 명확히 이해

**문제 5번을 틀렸다면**:
- 비용 최적화 모범 사례 상세 학습
- AWS 스토리지 클래스별 특성과 비용 비교

## 🎯 다음 학습 단계

1. **실습 수행**: Well-Architected Tool을 사용한 실제 아키텍처 검토
2. **심화 학습**: 각 기둥별 상세 모범 사례 학습
3. **사례 연구**: 실제 기업의 Well-Architected 적용 사례 분석
4. **정기적 검토**: 기존 프로젝트에 Well-Architected 원칙 적용

## 📚 추가 학습 자료

- [AWS Well-Architected Framework 백서](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [Well-Architected Tool 사용자 가이드](https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html)
- [Well-Architected Labs](https://wellarchitectedlabs.com/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)

---

**퀴즈 완료 후 체크리스트**:
- [ ] 모든 문제의 해설을 읽고 이해했습니다
- [ ] 틀린 문제의 관련 개념을 추가로 학습했습니다
- [ ] Well-Architected Tool 실습을 계획했습니다
- [ ] 다음 학습 단계를 설정했습니다