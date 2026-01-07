# Week 4: 모니터링, 보안 및 최적화

## 📚 주차 개요

AWS 환경의 모니터링, 보안, 그리고 비용 최적화를 학습하는 마지막 주입니다.
운영 환경에서 필수적인 모니터링 체계 구축부터 보안 강화, 비용 관리, 그리고 Well-Architected Framework까지 
실무에서 바로 적용할 수 있는 운영 노하우를 다룹니다.

## 🎯 주차 학습 목표

- 포괄적인 모니터링 및 로깅 시스템 구축
- AWS 보안 서비스를 활용한 다층 보안 아키텍처 설계
- 비용 최적화 전략 수립 및 실행
- Well-Architected Framework 기반 아키텍처 검토 및 개선
- SAA-C03 시험 최종 준비

## 📅 일별 학습 계획

### [Day 22: CloudWatch 및 모니터링](./day22/README.md)
**학습 시간**: 3-4시간  
**핵심 주제**:
- CloudWatch 메트릭, 로그, 이벤트
- 커스텀 메트릭 및 대시보드 구성
- CloudWatch Alarms 및 SNS 연동
- X-Ray를 통한 분산 추적

**실습**: 종합 모니터링 대시보드 구축

### [Day 23: CloudTrail 및 보안 서비스](./day23/README.md)
**학습 시간**: 3-4시간  
**핵심 주제**:
- CloudTrail 로깅 및 감사
- AWS Config 규정 준수 모니터링
- GuardDuty 위협 탐지
- Security Hub 통합 보안 관리
- WAF 및 Shield DDoS 보호

**실습**: 보안 모니터링 및 알림 시스템 구축

### [Day 24: 비용 최적화 및 관리](./day24/README.md)
**학습 시간**: 3시간  
**핵심 주제**:
- AWS Cost Explorer 및 Budgets
- Reserved Instances 및 Savings Plans
- Spot Instances 활용 전략
- 리소스 태깅 및 비용 할당
- Trusted Advisor 권장 사항

**실습**: 비용 최적화 계획 수립 및 실행

### [Day 25: Well-Architected Framework](./day25/README.md)
**학습 시간**: 3-4시간  
**핵심 주제**:
- 5개 기둥 (운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화)
- 아키텍처 검토 프로세스
- 설계 원칙 및 모범 사례
- Well-Architected Tool 활용

**실습**: 기존 아키텍처 Well-Architected 검토

### [Day 26: 종합 실습 프로젝트](./day26/README.md)
**학습 시간**: 4-5시간  
**핵심 활동**:
- 전체 과정 통합 프로젝트
- 엔터프라이즈급 3-tier 애플리케이션 구축
- 보안, 모니터링, 백업 포함 완전한 아키텍처
- 비용 최적화 및 성능 튜닝

**실습**: 종합 아키텍처 프로젝트 완성

### [Day 27: 모의고사 및 최종 복습](./day27/README.md)
**학습 시간**: 4-5시간  
**핵심 활동**:
- SAA-C03 모의고사 (65문제)
- 틀린 문제 분석 및 복습
- 핵심 개념 최종 정리
- 시험 전략 및 시간 관리 연습

**평가**: 모의고사 점수 720점 이상 목표

### [Day 28: 시험 준비 및 팁](./day28/README.md)
**학습 시간**: 2-3시간  
**핵심 활동**:
- 시험 당일 준비사항 점검
- 마지막 핵심 개념 복습
- 시험 응시 전략 및 팁
- 자격증 취득 후 계획 수립

**목표**: SAA-C03 시험 응시 준비 완료

## 📊 주차 진도 체크리스트

- [ ] Day 22: 모니터링 시스템 구축 완료
- [ ] Day 23: 보안 아키텍처 강화 완료
- [ ] Day 24: 비용 최적화 전략 수립
- [ ] Day 25: Well-Architected 검토 완료
- [ ] Day 26: 종합 프로젝트 완성
- [ ] Day 27: 모의고사 720점 이상 달성
- [ ] Day 28: 시험 준비 완료

## 🎯 주요 학습 성과

이 주를 마치면 다음을 할 수 있게 됩니다:

1. **운영 모니터링**: CloudWatch를 활용한 포괄적인 모니터링 시스템 구축
2. **보안 강화**: 다층 보안 아키텍처 설계 및 위협 탐지 시스템 구축
3. **비용 관리**: 체계적인 비용 분석 및 최적화 전략 수립
4. **아키텍처 검토**: Well-Architected Framework 기반 아키텍처 평가 및 개선
5. **시험 준비**: SAA-C03 시험 합격을 위한 완전한 준비

## 📚 참고 자료

### AWS 공식 문서
- [CloudWatch 사용 설명서](https://docs.aws.amazon.com/cloudwatch/)
- [CloudTrail 사용 설명서](https://docs.aws.amazon.com/cloudtrail/)
- [AWS Config 사용 설명서](https://docs.aws.amazon.com/config/)
- [Cost Management 사용 설명서](https://docs.aws.amazon.com/cost-management/)

### Well-Architected Framework
- [Well-Architected Framework 백서](https://aws.amazon.com/architecture/well-architected/)
- [5개 기둥 상세 가이드](https://wa.aws.amazon.com/index.html)

### 시험 준비 자료
- [SAA-C03 시험 가이드](https://aws.amazon.com/certification/certified-solutions-architect-associate/)
- [AWS 샘플 문제](https://aws.amazon.com/certification/certification-prep/)

## 💡 학습 팁

1. **실무 중심**: 실제 운영 환경에서 발생할 수 있는 시나리오 중심 학습
2. **비용 의식**: 모든 아키텍처 결정에서 비용 영향 고려
3. **보안 우선**: 보안을 사후 추가가 아닌 설계 단계부터 고려
4. **지속적 개선**: Well-Architected 원칙에 따른 지속적인 아키텍처 개선

## 🏆 시험 준비 전략

### 1. 핵심 도메인별 학습 비중
- **보안 아키텍처 설계** (30%): IAM, VPC 보안, 암호화, 모니터링
- **복원력 있는 아키텍처 설계** (26%): 고가용성, 재해 복구, 백업
- **고성능 아키텍처 설계** (24%): 확장성, 캐싱, 데이터베이스 최적화
- **비용 최적화 아키텍처 설계** (20%): 인스턴스 선택, 스토리지 최적화

### 2. 시험 응시 팁
- **시간 관리**: 문제당 평균 2분, 어려운 문제는 표시 후 나중에 해결
- **키워드 파악**: 문제에서 핵심 키워드와 요구사항 정확히 파악
- **제외법 활용**: 명백히 틀린 선택지부터 제거
- **실무 경험**: 이론보다는 실제 구현 경험 기반으로 답안 선택

## 🔗 네비게이션

- [← Week 3: 애플리케이션 서비스 및 배포](../week3/README.md)
- [메인으로 돌아가기](../README.md)

---

**🏆 4주간의 학습 여정을 마무리하고 AWS Solutions Architect Associate 자격증을 획득해보세요!**

**🎯 목표: SAA-C03 시험 합격 및 실무 적용 가능한 AWS 아키텍처 역량 확보**