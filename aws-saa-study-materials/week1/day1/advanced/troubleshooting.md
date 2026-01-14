# Troubleshooting: Regions 문제 해결 가이드

## 📋 문서 정보
- **Day**: 1
- **주요 서비스**: Regions, Availability Zones, Edge Locations, CloudFront
- **작성일**: {date}

---

## 🔍 일반적인 문제 상황들

### 문제 1: {primary_service} 성능 저하
**증상**:
- 응답 시간 증가: 평균 {normal_response_time}ms → {degraded_response_time}ms
- 에러율 상승: {normal_error_rate}% → {degraded_error_rate}%
- 사용자 불만 증가
- {additional_symptom}

**진단 단계** (AWS Console 기반):

1. **CloudWatch 메트릭 확인**
   - Console 경로: CloudWatch > Metrics > {service_namespace}
   - 확인할 메트릭:
     - {metric_1}: 정상 범위 {normal_range_1}, 현재 값 확인
     - {metric_2}: 정상 범위 {normal_range_2}, 현재 값 확인
     - {metric_3}: 정상 범위 {normal_range_3}, 현재 값 확인
   - 시간 범위: 지난 1시간 ~ 24시간
   - 이상 패턴 식별

2. **로그 분석**
   - Console 경로: CloudWatch > Log groups > {log_group_name}
   - 검색 쿼리:
     ```
     fields @timestamp, @message
     | filter @message like /ERROR|WARN/
     | sort @timestamp desc
     | limit 100
     ```
   - 주의할 에러 패턴:
     - `{error_pattern_1}`: {error_meaning_1}
     - `{error_pattern_2}`: {error_meaning_2}
     - `{error_pattern_3}`: {error_meaning_3}

3. **리소스 사용률 점검**
   - Console 경로: {service} > Monitoring
   - 확인 항목:
     - CPU 사용률: {cpu_threshold}% 이상이면 문제
     - 메모리 사용률: {memory_threshold}% 이상이면 문제
     - 네트워크 대역폭: {network_threshold} 이상이면 문제
     - 디스크 I/O: {disk_io_threshold} 이상이면 문제

4. **네트워크 연결 상태 점검**
   - Console 경로: VPC > Network ACLs / Security Groups
   - 확인 사항:
     - Security Group 인바운드/아웃바운드 규칙
     - Network ACL 규칙
     - 라우팅 테이블 설정
     - VPC 엔드포인트 연결 상태

**해결 방법**:

1. **즉시 조치** (임시 해결)
   - Console 경로: {service} > {resource_name}
   - Actions > {immediate_action}
   - 설정 변경:
     - {setting_1}: {temporary_value_1}
     - {setting_2}: {temporary_value_2}
   - 예상 효과: {expected_immediate_effect}
   - 소요 시간: 약 {immediate_action_time}분

2. **근본 원인 해결**
   - 원인 분석: {root_cause_analysis}
   - 영구 해결책: {permanent_solution}
   - 구현 방법 (Console 기반):
     1. Console 경로: {console_path_step1}
     2. {action_step1}
     3. Console 경로: {console_path_step2}
     4. {action_step2}
     5. 변경 사항 적용 및 검증

3. **재발 방지 조치**
   - 모니터링 강화:
     - Console 경로: CloudWatch > Alarms > Create alarm
     - 알람 설정:
       - 메트릭: {metric_name}
       - 조건: {alarm_condition}
       - 임계값: {threshold_value}
       - 알림: SNS 토픽 선택
   
   - 자동화 구성:
     - Console 경로: {automation_console_path}
     - 자동 스케일링 정책 설정
     - 자동 복구 옵션 활성화

**예방 조치**:
- **모니터링 알람 설정**
  - Console 경로: CloudWatch > Alarms > Create alarm
  - 알람 조건:
    - {metric_1} > {threshold_1} for {period_1} minutes
    - {metric_2} > {threshold_2} for {period_2} minutes
  - 알림 대상: {sns_topic_name}

- **자동 스케일링 구성** (해당되는 경우)
  - Console 경로: {service} > Auto Scaling
  - 스케일링 정책:
    - 스케일 아웃: {metric} > {scale_out_threshold}
    - 스케일 인: {metric} < {scale_in_threshold}
    - 쿨다운 기간: {cooldown_period}초

- **정기적인 성능 검토**
  - 주간 리뷰 체크리스트:
    - [ ] CloudWatch 대시보드 확인
    - [ ] 에러 로그 검토
    - [ ] 리소스 사용률 분석
    - [ ] 비용 추이 확인
  - 월간 리뷰 체크리스트:
    - [ ] 성능 벤치마크 실행
    - [ ] 용량 계획 업데이트
    - [ ] 보안 패치 적용
    - [ ] 백업 복원 테스트

---

### 문제 2: 보안 이슈 - 무단 접근 시도
**증상**:
- CloudTrail에서 비정상적인 API 호출 감지
- 알 수 없는 IP 주소에서의 접근
- 권한 없는 작업 시도 로그
- {additional_security_symptom}

**진단 단계** (AWS Console 기반):

1. **CloudTrail 로그 분석**
   - Console 경로: CloudTrail > Event history
   - 필터 설정:
     - Event name: {suspicious_event_name}
     - User name: {suspicious_user}
     - Time range: 지난 24시간
   - 의심스러운 활동 패턴 식별

2. **IAM 권한 검토**
   - Console 경로: IAM > Users / Roles
   - 확인 항목:
     - 최근 생성된 사용자/역할
     - 과도한 권한을 가진 사용자
     - 장기간 미사용 액세스 키
     - MFA 미설정 사용자

3. **Security Group 및 Network ACL 검토**
   - Console 경로: VPC > Security Groups
   - 확인 항목:
     - 0.0.0.0/0 (모든 IP) 허용 규칙
     - 불필요하게 열린 포트
     - 최근 변경된 규칙

4. **GuardDuty 알림 확인** (활성화된 경우)
   - Console 경로: GuardDuty > Findings
   - 심각도별 필터링
   - 위협 유형 분석

**해결 방법**:

1. **즉시 조치** (보안 위협 차단)
   - 의심스러운 액세스 키 비활성화:
     - Console 경로: IAM > Users > Security credentials
     - 액세스 키 선택 > Make inactive
   
   - Security Group 규칙 수정:
     - Console 경로: VPC > Security Groups
     - 의심스러운 IP 차단
     - 불필요한 포트 닫기
   
   - 비밀번호 강제 변경:
     - Console 경로: IAM > Users
     - 사용자 선택 > Security credentials > Manage password
     - "Require password reset" 체크

2. **근본 원인 해결**
   - 원인 분석: {security_root_cause}
   - 영구 해결책:
     - IAM 정책 최소 권한 원칙 적용
     - MFA 강제 활성화
     - IP 화이트리스트 구성
     - 정기적인 권한 검토 프로세스 수립

3. **재발 방지 조치**
   - CloudTrail 로그 모니터링 강화
   - GuardDuty 활성화 (미활성화 시)
   - AWS Config 규칙 설정
   - 보안 교육 실시

**예방 조치**:
- **MFA 강제 활성화**
  - Console 경로: IAM > Account settings
  - Password policy 설정
  - MFA 필수 정책 적용

- **CloudWatch 보안 알람**
  - Console 경로: CloudWatch > Alarms
  - 알람 생성:
    - 루트 계정 사용 감지
    - IAM 정책 변경 감지
    - Security Group 변경 감지

- **정기적인 보안 감사**
  - 월간 체크리스트:
    - [ ] IAM 사용자 및 권한 검토
    - [ ] 액세스 키 로테이션
    - [ ] Security Group 규칙 검토
    - [ ] CloudTrail 로그 분석
    - [ ] 패치 및 업데이트 적용

---

### 문제 3: 비용 급증
**증상**:
- 예상보다 높은 월간 청구 금액
- 특정 서비스의 비용 급증
- 비용 알람 트리거
- {additional_cost_symptom}

**진단 단계** (AWS Console 기반):

1. **Cost Explorer 분석**
   - Console 경로: Billing > Cost Explorer
   - 분석 항목:
     - 서비스별 비용 분포
     - 일별 비용 추이
     - 리전별 비용
     - 태그별 비용 (태그 설정 시)

2. **리소스 사용 현황 확인**
   - Console 경로: {service} > Dashboard
   - 확인 항목:
     - 실행 중인 리소스 수
     - 리소스 사이즈 및 타입
     - 데이터 전송량
     - 스토리지 사용량

3. **Cost Anomaly Detection 확인**
   - Console 경로: Billing > Cost Anomaly Detection
   - 이상 비용 패턴 식별
   - 근본 원인 분석

4. **Trusted Advisor 권장사항**
   - Console 경로: Trusted Advisor > Cost Optimization
   - 확인 항목:
     - 유휴 리소스
     - 과도하게 프로비저닝된 리소스
     - 예약 인스턴스 권장사항

**해결 방법**:

1. **즉시 조치** (비용 절감)
   - 불필요한 리소스 중지/삭제:
     - Console 경로: {service} > Resources
     - 미사용 리소스 식별
     - Actions > Stop / Terminate
   
   - 과도한 리소스 다운사이징:
     - Console 경로: {service} > Modify
     - 적절한 사이즈로 변경
     - 변경 적용

2. **근본 원인 해결**
   - 원인 분석: {cost_root_cause}
   - 영구 해결책:
     - 자동 스케일링 구성
     - 예약 인스턴스 구매
     - 스팟 인스턴스 활용
     - 데이터 전송 최적화

3. **재발 방지 조치**
   - 비용 알람 설정:
     - Console 경로: Billing > Budgets > Create budget
     - 예산 금액 설정
     - 알람 임계값: {threshold_percentage}%
   
   - 태그 정책 적용:
     - 리소스별 비용 추적
     - 프로젝트/팀별 비용 할당
     - 정기적인 비용 리뷰

**예방 조치**:
- **비용 예산 및 알람**
  - Console 경로: Billing > Budgets
  - 예산 설정:
    - 월간 예산: ${monthly_budget}
    - 알람 임계값: 80%, 100%, 120%
    - 알림 이메일 설정

- **리소스 태깅 전략**
  - 필수 태그:
    - Environment: production/staging/development
    - Project: {project_name}
    - Owner: {owner_email}
    - CostCenter: {cost_center}

- **정기적인 비용 검토**
  - 주간 체크리스트:
    - [ ] Cost Explorer 대시보드 확인
    - [ ] 이상 비용 패턴 식별
    - [ ] 미사용 리소스 정리
  - 월간 체크리스트:
    - [ ] 서비스별 비용 분석
    - [ ] 예약 인스턴스 최적화
    - [ ] 비용 절감 기회 식별

---

## 🧪 실습 시나리오 (AWS Console 기반)

### 시나리오 1: {primary_service} 트래픽 급증 대응
**상황 설정**:
- 예상치 못한 트래픽 10배 증가
- 현재 리소스: {current_resource_config}
- 현재 처리량: {current_throughput}
- 목표 처리량: {target_throughput}
- 즉각적인 대응 필요

**단계별 대응 방법** (Console 기반):

1. **현재 상태 확인**
   - Console 경로: CloudWatch > Dashboards
   - 확인 항목:
     - 현재 트래픽: {current_traffic}
     - 응답 시간: {current_response_time}ms
     - 에러율: {current_error_rate}%
     - 리소스 사용률: CPU {cpu_usage}%, Memory {memory_usage}%

2. **긴급 스케일 아웃**
   - Console 경로: {service} > {resource_name}
   - Actions > {scale_action}
   - 설정 변경:
     - 인스턴스 수: {current_count} → {target_count}
     - 인스턴스 타입: {current_type} → {target_type} (필요시)
   - 적용 및 대기 (약 {scale_time}분)

3. **로드 밸런서 확인** (해당되는 경우)
   - Console 경로: EC2 > Load Balancers
   - 확인 항목:
     - 헬스 체크 상태
     - 타겟 그룹 등록 상태
     - 연결 수 및 처리량

4. **모니터링 및 검증**
   - Console 경로: CloudWatch > Metrics
   - 확인 메트릭:
     - 응답 시간 개선 확인
     - 에러율 감소 확인
     - 리소스 사용률 정상화 확인
   - 예상 결과:
     - 응답 시간: {target_response_time}ms 이하
     - 에러율: {target_error_rate}% 이하
     - CPU 사용률: {target_cpu_usage}% 이하

**결과 검증 방법**:
- 성능 지표 확인:
  - [ ] 응답 시간이 목표치 이하인가?
  - [ ] 에러율이 정상 범위인가?
  - [ ] 모든 인스턴스가 정상 작동하는가?

- 비용 영향 분석:
  - 시간당 추가 비용: ${additional_hourly_cost}
  - 일일 추가 비용: ${additional_daily_cost}
  - 비용 최적화 계획 수립

- 사용자 경험 개선 확인:
  - 사용자 피드백 모니터링
  - 전환율 변화 확인
  - 이탈률 변화 확인

### 시나리오 2: 데이터베이스 연결 실패
**상황 설정**:
- 애플리케이션에서 데이터베이스 연결 불가
- 에러 메시지: "{db_connection_error}"
- 영향 범위: {affected_scope}
- 긴급도: 높음

**단계별 대응 방법** (Console 기반):

1. **데이터베이스 상태 확인**
   - Console 경로: RDS > Databases
   - 확인 항목:
     - DB 인스턴스 상태: Available/Stopped/Failed
     - CPU 사용률
     - 연결 수
     - 스토리지 용량

2. **네트워크 연결 확인**
   - Console 경로: VPC > Security Groups
   - DB Security Group 확인:
     - 인바운드 규칙에 애플리케이션 Security Group 허용 여부
     - 포트 {db_port} 개방 여부
   
   - Console 경로: VPC > Route Tables
   - 라우팅 테이블 확인:
     - 서브넷 간 라우팅 설정
     - NAT Gateway/Internet Gateway 설정

3. **연결 문자열 및 자격 증명 확인**
   - Console 경로: RDS > Databases > Connectivity & security
   - 엔드포인트 주소 확인
   - 포트 번호 확인
   - Secrets Manager에서 자격 증명 확인 (사용 시)

4. **로그 분석**
   - Console 경로: RDS > Databases > Logs & events
   - 에러 로그 확인
   - 슬로우 쿼리 로그 확인 (활성화 시)

**결과 검증 방법**:
- [ ] 데이터베이스 연결 성공
- [ ] 애플리케이션 정상 작동
- [ ] 에러 로그 없음
- [ ] 성능 메트릭 정상

---

## 📊 모니터링 및 알람 설정

### CloudWatch 대시보드 구성
**Console 경로**: CloudWatch > Dashboards > Create dashboard

**대시보드 이름**: Regions-monitoring-dashboard

**핵심 메트릭 정의** (Day 1 서비스 기준):

1. **메트릭 1: {metric_name_1}**
   - 설명: {metric_description_1}
   - 정상 범위: {normal_range_1}
   - 경고 임계값: {warning_threshold_1}
   - 위험 임계값: {critical_threshold_1}
   - 위젯 유형: Line chart

2. **메트릭 2: {metric_name_2}**
   - 설명: {metric_description_2}
   - 정상 범위: {normal_range_2}
   - 경고 임계값: {warning_threshold_2}
   - 위험 임계값: {critical_threshold_2}
   - 위젯 유형: Number

3. **메트릭 3: {metric_name_3}**
   - 설명: {metric_description_3}
   - 정상 범위: {normal_range_3}
   - 경고 임계값: {warning_threshold_3}
   - 위험 임계값: {critical_threshold_3}
   - 위젯 유형: Stacked area

### 알람 임계값 설정
**Console 경로**: CloudWatch > Alarms > Create alarm

**알람 구성 예시**:
```yaml
알람명: Regions-{metric_name}-alert
메트릭: {namespace}/{metric_name}
통계: {statistic} (Average/Sum/Maximum/Minimum)
기간: {period}분
조건: {comparison_operator} {threshold_value}
데이터 포인트: {evaluation_periods} 중 {datapoints_to_alarm}
알림: {sns_topic_arn}
```

**권장 알람 설정**:

1. **성능 알람**
   - 응답 시간 > {response_time_threshold}ms
   - 에러율 > {error_rate_threshold}%
   - 처리량 < {throughput_threshold}

2. **리소스 알람**
   - CPU 사용률 > {cpu_threshold}%
   - 메모리 사용률 > {memory_threshold}%
   - 디스크 사용률 > {disk_threshold}%

3. **비용 알람**
   - 일일 비용 > ${daily_cost_threshold}
   - 월간 비용 > ${monthly_cost_threshold}

### 알람 액션 설정
**SNS 토픽 생성**:
- Console 경로: SNS > Topics > Create topic
- 토픽 이름: Regions-alerts
- 구독 추가:
  - 프로토콜: Email
  - 엔드포인트: {alert_email}

**자동 복구 액션** (해당되는 경우):
- Console 경로: EC2 > Instances > Actions > Instance Settings > Create alarm
- 알람 액션: Recover this instance
- 조건: StatusCheckFailed_System

---

## 🔗 관련 AWS 문서

### 공식 트러블슈팅 가이드
- [Regions Troubleshooting]({troubleshooting_guide_link})
- [Common Errors and Solutions]({common_errors_link})
- [Performance Optimization]({performance_optimization_link})

### CloudWatch 모니터링
- [CloudWatch User Guide]({cloudwatch_guide_link})
- [Creating CloudWatch Alarms]({alarms_guide_link})
- [Using CloudWatch Logs]({logs_guide_link})

### 서비스별 베스트 프랙티스
- [Regions Best Practices]({best_practices_link})
- [AWS Well-Architected Framework]({well_architected_link})
- [Operational Excellence Pillar]({operational_excellence_link})

---

## 🎓 학습 포인트

1. **체계적인 문제 진단**: CloudWatch 메트릭과 로그를 활용한 단계별 진단 방법
2. **신속한 대응**: 즉시 조치와 근본 원인 해결의 균형
3. **예방적 모니터링**: 문제 발생 전 감지할 수 있는 알람 설정
4. **비용 최적화**: 성능과 비용의 균형을 맞추는 전략
5. **보안 강화**: 보안 위협을 조기에 감지하고 대응하는 방법

---

## 🔗 관련 학습 내용

### 실습 및 사례 연계
- [Case Study](./case-study.md) - 실제 기업에서 발생한 문제와 해결 사례
- [Best Practices](./best-practices.md) - 문제 예방을 위한 베스트 프랙티스
- [Hands-On Console](./hands-on-console/README.md) - 트러블슈팅 시나리오 실습

### 이전/향후 학습
- Day {previous_day}: [{previous_service}](../../day{previous_day}/theory.md) - 관련 서비스 이해
- Day {next_day}: [{next_service}](../../day{next_day}/theory.md) - 확장 서비스 학습

---

**작성 가이드**:
- 각 섹션의 `{placeholder}` 부분을 실제 내용으로 대체하세요
- Console 경로는 정확하게 작성하세요 (Services > Category > Service)
- 실제 에러 메시지와 해결 방법을 포함하세요
- 모든 진단 단계는 AWS Console 기반으로 작성하세요
- CloudWatch 쿼리는 실제 작동하는 구문을 사용하세요
