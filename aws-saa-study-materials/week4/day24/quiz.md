# Day 24 퀴즈: AWS 비용 최적화 및 관리

## 문제 1
**시나리오:** 회사에서 AWS 비용이 예상보다 높게 나오고 있어 비용 분석을 시작하려고 합니다. 가장 상세한 비용 및 사용량 데이터를 얻을 수 있는 AWS 서비스는 무엇입니까?

A) AWS Cost Explorer  
B) AWS Cost and Usage Reports (CUR)  
C) AWS Budgets  
D) AWS Trusted Advisor  

<details>
<summary>정답 및 해설</summary>

**정답: B) AWS Cost and Usage Reports (CUR)**

**해설:**
AWS Cost and Usage Reports (CUR)는 AWS에서 제공하는 가장 상세하고 포괄적인 비용 및 사용량 데이터를 제공합니다. CUR은 시간별 사용량 데이터, 리소스 ID, 태그 정보, 할인 적용 내역 등을 포함하여 매우 세밀한 분석이 가능합니다.

- A) Cost Explorer는 시각화 도구이지만 CUR만큼 상세하지 않음
- C) Budgets는 예산 설정 및 모니터링 도구
- D) Trusted Advisor는 권장사항 제공 도구

</details>

---

## 문제 2
**시나리오:** EC2 인스턴스를 1년간 지속적으로 사용할 예정입니다. 비용을 최대한 절약하면서도 인스턴스 타입 변경의 유연성을 유지하고 싶습니다. 어떤 구매 옵션을 선택해야 합니까?

A) On-Demand Instances  
B) Spot Instances  
C) Standard Reserved Instances  
D) Convertible Reserved Instances  

<details>
<summary>정답 및 해설</summary>

**정답: D) Convertible Reserved Instances**

**해설:**
Convertible Reserved Instances는 1-3년 약정으로 최대 54%까지 할인받을 수 있으면서도, 약정 기간 중에 인스턴스 패밀리, 운영체제, 테넌시를 변경할 수 있는 유연성을 제공합니다.

- A) On-Demand는 유연하지만 가장 비쌈
- B) Spot은 가장 저렴하지만 중단 위험이 있음
- C) Standard RI는 더 큰 할인을 제공하지만 변경 불가

</details>

---

## 문제 3
**시나리오:** 개발팀에서 매월 AWS 비용이 $500를 초과하지 않도록 모니터링하고, 80% 도달 시 알림을 받고 싶습니다. 어떤 AWS 서비스를 사용해야 합니까?

A) AWS Cost Explorer  
B) AWS Budgets  
C) AWS CloudWatch  
D) AWS Cost Anomaly Detection  

**정답: B) AWS Budgets**

**해설:**
AWS Budgets는 비용, 사용량, RI 활용률 등에 대한 예산을 설정하고, 설정한 임계값(예: 80%, 100%)에 도달했을 때 이메일이나 SNS를 통해 알림을 보낼 수 있는 서비스입니다.

- A) Cost Explorer는 분석 도구이지만 알림 기능 없음
- C) CloudWatch는 리소스 모니터링 도구
- D) Cost Anomaly Detection은 비정상적인 비용 증가 탐지 도구

---

## 문제 4
**시나리오:** 회사의 S3 버킷에 저장된 데이터 중 30일 이후에는 거의 접근하지 않지만, 가끔 필요할 때 즉시 접근할 수 있어야 합니다. 비용을 최적화하기 위해 어떤 S3 스토리지 클래스를 사용해야 합니까?

A) S3 Standard  
B) S3 Standard-IA (Infrequent Access)  
C) S3 Glacier  
D) S3 Intelligent-Tiering  

**정답: B) S3 Standard-IA (Infrequent Access)**

**해설:**
S3 Standard-IA는 자주 접근하지 않는 데이터를 위한 스토리지 클래스로, Standard보다 저렴하면서도 즉시 접근이 가능합니다. 30일 이후 거의 접근하지 않지만 즉시 접근이 필요한 요구사항에 적합합니다.

- A) S3 Standard는 자주 접근하는 데이터용으로 비용이 높음
- C) S3 Glacier는 아카이브용으로 검색에 시간이 걸림
- D) S3 Intelligent-Tiering은 접근 패턴이 변하는 데이터용

---

## 문제 5
**시나리오:** AWS 계정에서 비정상적으로 높은 비용이 발생했을 때 자동으로 감지하고 알림을 받고 싶습니다. 머신러닝을 사용하여 비용 패턴을 분석하는 AWS 서비스는 무엇입니까?

A) AWS Cost Explorer  
B) AWS Budgets  
C) AWS Cost Anomaly Detection  
D) AWS Trusted Advisor  

**정답: C) AWS Cost Anomaly Detection**

**해설:**
AWS Cost Anomaly Detection은 머신러닝을 사용하여 비정상적인 비용 증가나 사용 패턴을 자동으로 감지하고 알림을 보내는 서비스입니다. 과거 사용 패턴을 학습하여 예상 범위를 벗어나는 비용을 탐지합니다.

- A) Cost Explorer는 수동 분석 도구
- B) Budgets는 미리 설정한 임계값 기반 알림
- D) Trusted Advisor는 정적인 권장사항 제공

---

## 점수 계산
- 5문제 모두 맞음: 100점 (완벽한 이해!)
- 4문제 맞음: 80점 (우수한 이해)
- 3문제 맞음: 60점 (기본 이해, 복습 권장)
- 2문제 이하: 40점 이하 (추가 학습 필요)

## 추가 학습 권장사항

### 3문제 이하 맞은 경우:
1. AWS 비용 모델 (On-Demand, RI, Savings Plans, Spot) 재학습
2. Cost Explorer와 Budgets의 차이점 명확히 구분
3. S3 스토리지 클래스별 특성과 비용 구조 복습

### 4-5문제 맞은 경우:
1. 실제 AWS 계정에서 Cost Explorer 실습 진행
2. 다양한 시나리오에서의 비용 최적화 전략 학습
3. Well-Architected Framework의 비용 최적화 원칙 예습

## 오답 분석 및 추가 설명

### Reserved Instances vs Savings Plans
- **Standard RI**: 최대 75% 할인, 특정 인스턴스 타입에 고정
- **Convertible RI**: 최대 54% 할인, 인스턴스 타입 변경 가능
- **Compute Savings Plans**: 최대 66% 할인, EC2, Lambda, Fargate에 적용
- **EC2 Instance Savings Plans**: 최대 72% 할인, 특정 인스턴스 패밀리에 적용

### 비용 모니터링 도구 비교
- **Cost Explorer**: 과거 비용 분석 및 시각화
- **Budgets**: 예산 설정 및 임계값 기반 알림
- **Cost Anomaly Detection**: ML 기반 이상 비용 탐지
- **Trusted Advisor**: 비용 최적화 권장사항 제공

### S3 스토리지 클래스 선택 가이드
- **Standard**: 자주 접근하는 데이터 (가장 비쌈)
- **Standard-IA**: 월 1회 미만 접근, 즉시 접근 필요
- **One Zone-IA**: 단일 AZ, 더 저렴하지만 가용성 낮음
- **Glacier**: 아카이브, 검색에 분~시간 소요
- **Glacier Deep Archive**: 장기 아카이브, 검색에 12시간 소요
- **Intelligent-Tiering**: 접근 패턴이 변하는 데이터

## 실무 적용 팁

1. **비용 최적화는 지속적인 과정**: 한 번 설정하고 끝이 아니라 정기적인 리뷰가 필요
2. **태그 전략**: 비용 할당을 위해 일관된 태그 전략 수립
3. **Right Sizing**: 정기적인 인스턴스 사용률 모니터링 및 크기 조정
4. **자동화**: Lambda를 활용한 자동 리소스 정리 및 비용 알림