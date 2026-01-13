# Day 22: CloudWatch & 모니터링

## 📚 학습 개요
AWS CloudWatch를 사용한 종합적인 모니터링 시스템 구축 방법을 학습합니다. 메트릭 수집, 로그 관리, 알람 설정, 대시보드 구성을 통해 AWS 리소스를 효과적으로 모니터링하는 방법을 익힙니다.

## 🎯 학습 목표
- AWS CloudWatch의 핵심 개념과 구성 요소 이해
- 메트릭, 로그, 이벤트의 차이점과 활용 방법 학습
- CloudWatch 대시보드와 알람 설정 실습
- 모니터링 모범 사례와 비용 최적화 전략 습득
- CloudWatch Logs Insights를 활용한 로그 분석

## 📖 학습 자료

### 1. 이론 학습
- **파일**: `theory.md`
- **내용**: 
  - CloudWatch 개요 및 구성 요소
  - 메트릭 유형과 특징 (기본 vs 사용자 정의)
  - CloudWatch Logs 구조와 수집 방법
  - 알람 설정과 이상 탐지
  - 대시보드 구성과 시각화
  - 모니터링 모범 사례
- **예상 소요 시간**: 45분

### 2. 실습 학습
- **파일**: `hands-on/setup-guide.md`
- **내용**:
  - EC2 메트릭 확인 및 분석
  - CloudWatch 대시보드 생성 (3개 위젯)
  - SNS 토픽 생성 및 이메일 구독 설정
  - CPU 사용률 및 네트워크 트래픽 알람 생성
  - CloudWatch Logs 그룹 및 스트림 생성
  - Logs Insights를 활용한 로그 쿼리
  - 이상 탐지 알람 설정 (고급)
  - 복합 알람 생성
  - 비용 모니터링 알람 설정
- **예상 소요 시간**: 90분

### 3. 퀴즈
- **파일**: `quiz.md`
- **내용**: CloudWatch 핵심 개념 확인 (5문제)
- **예상 소요 시간**: 10분

## ⏰ 권장 학습 순서
1. **이론 학습** (45분) - CloudWatch 개념과 구성 요소 이해
2. **실습 진행** (90분) - 실제 대시보드와 알람 설정
3. **퀴즈 풀이** (10분) - 학습 내용 점검
4. **복습 및 정리** (15분) - 핵심 포인트 재확인

**총 예상 소요 시간: 2시간 40분**

## 🔧 사전 준비사항
- AWS 계정 및 Console 접근 권한
- 실행 중인 EC2 인스턴스 (t2.micro 권장)
- 알림을 받을 이메일 주소
- 기본적인 AWS Console 사용 경험

## 📋 실습 체크리스트
- [ ] EC2 메트릭 확인 및 그래프 분석
- [ ] 3개 위젯이 포함된 대시보드 생성
- [ ] SNS 토픽 생성 및 이메일 구독 설정
- [ ] CPU 사용률 알람 생성 및 테스트
- [ ] 네트워크 트래픽 알람 생성
- [ ] CloudWatch Logs 그룹 및 스트림 생성
- [ ] Logs Insights 쿼리 실행
- [ ] 이상 탐지 알람 설정 (선택사항)
- [ ] 복합 알람 생성 (선택사항)
- [ ] 비용 모니터링 알람 설정

## 🎓 핵심 개념 요약

### CloudWatch 구성 요소
- **Metrics**: 성능 지표 수집 및 분석
- **Logs**: 애플리케이션 및 시스템 로그 중앙 관리
- **Alarms**: 임계값 기반 자동 알림 및 대응
- **Dashboards**: 시각적 모니터링 인터페이스
- **Events/EventBridge**: 이벤트 기반 자동화

### 메트릭 유형
- **기본 메트릭**: AWS 서비스에서 자동 제공 (무료, 5분 간격)
- **사용자 정의 메트릭**: 애플리케이션에서 직접 전송 (유료, 1초 단위 가능)

### 알람 상태
- **OK**: 정상 범위 내
- **ALARM**: 임계값 초과
- **INSUFFICIENT_DATA**: 데이터 부족

## 🔗 연관 서비스
- **SNS**: 알람 알림 전송
- **Auto Scaling**: 자동 확장/축소 트리거
- **Lambda**: 이벤트 기반 자동화
- **X-Ray**: 분산 추적과 연동
- **Systems Manager**: 자동화된 문제 해결

## 📚 추가 학습 자료
- [AWS CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/)
- [CloudWatch Metrics and Dimensions Reference](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/aws-services-cloudwatch-metrics.html)
- [CloudWatch Logs Insights Query Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)
- [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/)

## ⚠️ 주의사항
- 사용자 정의 메트릭과 상세 모니터링은 추가 비용이 발생합니다
- 로그 보존 기간을 적절히 설정하여 비용을 관리하세요
- 알람 피로도를 방지하기 위해 적절한 임계값을 설정하세요
- 실습 후 불필요한 리소스는 삭제하여 비용을 절약하세요

## 🚀 다음 단계
Day 23에서는 **CloudTrail & 보안 서비스**에 대해 학습합니다. CloudWatch로 구축한 모니터링 시스템에 보안 감사와 컴플라이언스 기능을 추가하는 방법을 배우게 됩니다.