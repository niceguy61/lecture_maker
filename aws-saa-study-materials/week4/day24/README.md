# Day 24: AWS 비용 최적화 및 관리

## 📚 학습 개요
AWS 비용 구조를 이해하고, Cost Explorer와 Budgets를 활용한 비용 분석 및 관리 방법을 학습합니다. 비용 최적화 전략과 모범 사례를 통해 효율적인 AWS 리소스 운영 방법을 익힙니다.

## 🎯 학습 목표
- [ ] AWS 비용 구조와 요금 모델 이해
- [ ] Cost Explorer를 활용한 비용 분석 수행
- [ ] AWS Budgets를 통한 예산 설정 및 알림 구성
- [ ] 비용 최적화 전략 수립 및 적용
- [ ] Reserved Instances와 Savings Plans 활용법 습득

## 📖 학습 자료

### 1. 이론 학습 (60분)
**파일:** `theory.md`

**주요 내용:**
- AWS 요금 모델 (On-Demand, RI, Savings Plans, Spot)
- Cost Explorer 기능 및 활용법
- AWS Budgets를 통한 예산 관리
- 비용 최적화 전략 (Right Sizing, 스토리지 최적화)
- 비용 모니터링 도구 (CUR, Trusted Advisor)
- 비용 할당 및 차지백 방법

**시각화 자료:**
- AWS 요금 모델 비교 다이어그램
- Cost Explorer 분석 차원 구조도
- 예산 유형 및 알림 설정 플로우
- Right Sizing 프로세스 다이어그램
- Savings Plans vs Reserved Instances 비교
- 비용 할당 태그 구조도

### 2. 실습 (90분)
**파일:** `hands-on/setup-guide.md`

**실습 내용:**
1. **Cost Explorer 설정 및 분석**
   - Cost Explorer 활성화
   - 월별/일별 비용 분석
   - 서비스별, 지역별 비용 분석
   - 태그 기반 비용 할당 분석

2. **AWS Budgets 설정**
   - 기본 비용 예산 생성
   - 서비스별 예산 설정
   - 사용량 예산 구성
   - 알림 임계값 및 수신자 설정

3. **비용 최적화 도구 활용**
   - Reserved Instance 권장사항 확인
   - Savings Plans 분석
   - Cost Anomaly Detection 설정
   - Trusted Advisor 권장사항 검토

**실습 환경:**
- AWS Free Tier 계정
- 최소 1개월간의 사용 이력 권장
- Billing 권한이 있는 IAM 사용자

### 3. 퀴즈 (30분)
**파일:** `quiz.md`

**문제 구성:**
- 문제 1: AWS Cost and Usage Reports (CUR) 특징
- 문제 2: Reserved Instances 유형별 특성
- 문제 3: AWS Budgets 활용법
- 문제 4: S3 스토리지 클래스 최적화
- 문제 5: Cost Anomaly Detection 기능

## ⏰ 권장 학습 일정

### 오전 (2시간)
- **09:00-10:00**: 이론 학습 (AWS 비용 구조, Cost Explorer)
- **10:00-11:00**: 실습 1-2 (Cost Explorer 설정 및 분석)

### 오후 (2시간)
- **14:00-15:00**: 이론 학습 (비용 최적화 전략, 모니터링 도구)
- **15:00-16:00**: 실습 3-5 (Budgets 설정, 최적화 도구 활용)

### 저녁 (30분)
- **19:00-19:30**: 퀴즈 및 복습

## 🔗 연관 학습 주제

### 이전 학습과의 연계
- **Day 22**: CloudWatch 모니터링 → 비용 모니터링으로 확장
- **Day 23**: 보안 및 거버넌스 → 비용 거버넌스 연결

### 다음 학습 예고
- **Day 25**: Well-Architected Framework → 비용 최적화 원칙 심화

## 📋 실습 체크리스트

### Cost Explorer 실습
- [ ] Cost Explorer 활성화 완료
- [ ] 월별 비용 트렌드 분석 수행
- [ ] 서비스별 비용 분포 확인
- [ ] 태그 기반 비용 분석 실시

### AWS Budgets 실습
- [ ] 월별 총 비용 예산 생성
- [ ] 서비스별 예산 최소 2개 설정
- [ ] 사용량 예산 1개 이상 생성
- [ ] 알림 설정 및 테스트 완료

### 비용 최적화 실습
- [ ] RI 권장사항 확인 및 분석
- [ ] Savings Plans 옵션 검토
- [ ] Cost Anomaly Detection 설정
- [ ] Trusted Advisor 권장사항 검토

## 💡 학습 팁

### 효과적인 학습 방법
1. **실제 계정 활용**: 가능하면 실제 AWS 계정의 비용 데이터로 실습
2. **시나리오 기반 학습**: 다양한 비즈니스 시나리오에서의 비용 최적화 고려
3. **정기적인 리뷰**: 비용 최적화는 지속적인 과정임을 인식

### 주의사항
- 실습 시 불필요한 리소스 생성 주의
- 예산 설정 시 현실적인 금액으로 설정
- 알림 설정 시 스팸 방지를 위한 적절한 임계값 설정

## 🎯 학습 성과 측정

### 이해도 체크
- [ ] AWS 4가지 요금 모델의 차이점을 설명할 수 있음
- [ ] Cost Explorer를 사용하여 비용 분석을 수행할 수 있음
- [ ] 적절한 예산 설정 및 알림 구성을 할 수 있음
- [ ] 비용 최적화 권장사항을 평가하고 적용할 수 있음
- [ ] 태그 기반 비용 할당 전략을 수립할 수 있음

### 실무 적용 능력
- [ ] 조직의 AWS 비용 구조를 분석할 수 있음
- [ ] 비용 최적화 계획을 수립할 수 있음
- [ ] 비용 모니터링 및 알림 체계를 구축할 수 있음
- [ ] RI/Savings Plans 구매 결정을 내릴 수 있음

## 📚 추가 학습 자료

### AWS 공식 문서
- [AWS Cost Management User Guide](https://docs.aws.amazon.com/cost-management/)
- [AWS Cost Explorer User Guide](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html)
- [AWS Budgets User Guide](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)

### 모범 사례 가이드
- [AWS Cost Optimization Best Practices](https://aws.amazon.com/aws-cost-management/aws-cost-optimization/)
- [AWS Well-Architected Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/)

### 실습 도구
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/cost-optimization-hub/)

---

**다음 학습:** [Day 25 - AWS Well-Architected Framework](../day25/README.md)  
**이전 학습:** [Day 23 - CloudTrail 및 보안](../day23/README.md)