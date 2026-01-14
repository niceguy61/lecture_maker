# Hands-On Console: {service_name} 실습 가이드

## 🎯 실습 개요
이 실습에서는 Day {day_number}에서 학습한 **{service_name}**을 AWS Console을 통해 직접 구성하고 테스트합니다.

**학습 목표**:
- {service_name}의 핵심 기능을 Console에서 직접 구성
- 실제 운영 환경에서 사용되는 설정 방법 이해
- 다른 AWS 서비스와의 통합 경험
- 문제 해결 및 모니터링 방법 습득

---

## 📋 사전 요구사항

실습을 시작하기 전에 다음 사항을 준비해주세요:

### 필수 준비사항
- [ ] [AWS 계정 설정](../../../resources/prerequisites/aws-account-setup.md)
  - AWS Free Tier 계정 생성 완료
  - 결제 알람 설정 완료
  - 루트 계정 MFA 활성화 완료

- [ ] [IAM 사용자 설정](../../../resources/prerequisites/iam-user-setup.md)
  - 관리자 IAM 사용자 생성 완료
  - IAM 사용자로 로그인 가능
  - 필요한 권한 확인

- [ ] [Console 탐색 기본](../../../resources/prerequisites/console-navigation.md)
  - AWS Console 기본 탐색 방법 숙지
  - 리전 선택 방법 이해
  - 서비스 검색 및 즐겨찾기 설정

### 실습 환경 정보
- **예상 비용**: ${estimated_cost} ({free_tier_status})
  - Free Tier 범위 내: {free_tier_resources}
  - Free Tier 초과: {paid_resources}
- **소요 시간**: 약 {estimated_time}분
- **권장 리전**: {recommended_region} (서울)
- **필요한 권한**: {required_permissions}

### 선택 사항
- [ ] [AWS CLI 설정](../../../resources/prerequisites/cli-configuration.md) (선택사항)
  - CLI를 통한 검증을 원하는 경우

---

## 🏗️ 실습 아키텍처

이 실습에서 구축할 아키텍처:

```mermaid
graph TB
    subgraph "사용자"
        A[실습 참가자]
    end
    
    subgraph "AWS Console"
        B[{primary_service}]
        C[{related_service_1}]
        D[{related_service_2}]
    end
    
    subgraph "모니터링"
        E[CloudWatch]
    end
    
    A --> B
    B --> C
    B --> D
    B --> E
    C --> E
    D --> E
```

**아키텍처 설명**:
- {architecture_description}
- 주요 구성 요소: {main_components}
- 데이터 플로우: {data_flow}

---

## 📝 실습 목표

이 실습을 완료하면 다음을 할 수 있습니다:

1. **{goal_1}**: {goal_1_description}
2. **{goal_2}**: {goal_2_description}
3. **{goal_3}**: {goal_3_description}
4. **{goal_4}**: {goal_4_description}

---

## 🚀 실습 진행

### Exercise 1: {primary_service} 생성 및 기본 설정
**목표**: {exercise_1_goal}

**예상 소요 시간**: {exercise_1_time}분

**단계**:

1. **{primary_service} 생성**
   - Console 경로: Services > {category} > {primary_service}
   - 화면 상단의 "Create {resource}" 버튼 클릭
   
2. **기본 설정**
   - **Name**: `day{day_number}-{resource_name}`
     - 명명 규칙: day 번호 + 리소스 유형
     - 예시: `day8-my-bucket`
   
   - **Region**: `ap-northeast-2` (서울)
     - 화면 우측 상단에서 리전 선택
     - 서울 리전 선택 이유: {region_reason}
   
   - **{setting_1}**: {setting_1_value}
     - 설명: {setting_1_description}
     - 권장 이유: {setting_1_reason}
   
   - **{setting_2}**: {setting_2_value}
     - 설명: {setting_2_description}
     - 권장 이유: {setting_2_reason}

3. **고급 설정** (선택사항)
   - "Advanced settings" 또는 "Additional configuration" 섹션 확장
   
   - **{advanced_setting_1}**: {advanced_setting_1_value}
     - 설명: {advanced_setting_1_description}
     - 사용 시기: {advanced_setting_1_use_case}
   
   - **{advanced_setting_2}**: {advanced_setting_2_value}
     - 설명: {advanced_setting_2_description}
     - 사용 시기: {advanced_setting_2_use_case}

4. **태그 추가** (권장)
   - "Tags" 섹션으로 이동
   - 다음 태그 추가:
     | Key | Value | 설명 |
     |-----|-------|------|
     | Name | day{day_number}-{resource_name} | 리소스 식별 |
     | Environment | learning | 환경 구분 |
     | Project | aws-saa-study | 프로젝트 구분 |
     | Owner | {your_name} | 소유자 |

5. **생성 확인**
   - 모든 설정 검토
   - "Create {resource}" 버튼 클릭
   - 생성 완료까지 대기 (약 {creation_time}분)
   - 상태 확인: {status_check_method}

**검증**:
- [ ] {resource}가 "Available" 또는 "Active" 상태인가?
- [ ] 리소스 이름이 올바르게 설정되었는가?
- [ ] 리전이 `ap-northeast-2`로 설정되었는가?
- [ ] 모든 필수 설정이 올바르게 적용되었는가?

**문제 해결**:
- 생성 실패 시:
  - Console 경로: {service} > Events 또는 Logs
  - 에러 메시지 확인
  - 일반적인 원인: {common_creation_errors}

---

### Exercise 2: {related_service_1} 통합
**목표**: {exercise_2_goal}

**예상 소요 시간**: {exercise_2_time}분

**단계**:

1. **{related_service_1} 생성**
   - Console 경로: Services > {category_2} > {related_service_1}
   - "Create {resource_2}" 버튼 클릭

2. **기본 설정**
   - **Name**: `day{day_number}-{resource_2_name}`
   - **Region**: `ap-northeast-2` (서울)
   - **{setting_3}**: {setting_3_value}
   - **{setting_4}**: {setting_4_value}

3. **{primary_service}와 연결**
   - "{primary_service} integration" 또는 "Attach {primary_service}" 섹션으로 이동
   - 이전에 생성한 `day{day_number}-{resource_name}` 선택
   - 연결 옵션 구성:
     - **{connection_setting_1}**: {connection_value_1}
     - **{connection_setting_2}**: {connection_value_2}

4. **권한 설정**
   - "Permissions" 또는 "IAM role" 섹션으로 이동
   - 옵션 선택:
     - [ ] 기존 역할 사용: {existing_role_name}
     - [x] 새 역할 생성 (권장)
       - 역할 이름: `day{day_number}-{service_role_name}`
       - 정책: {required_policies}

5. **생성 및 연결 확인**
   - "Create" 또는 "Attach" 버튼 클릭
   - 생성 완료 대기
   - 연결 상태 확인:
     - Console 경로: {primary_service} > {resource_name} > Integrations
     - {related_service_1} 연결 상태: Connected

**검증**:
- [ ] {related_service_1}가 정상적으로 생성되었는가?
- [ ] {primary_service}와 연결이 완료되었는가?
- [ ] IAM 역할이 올바르게 설정되었는가?
- [ ] 연결 테스트가 성공하는가?

**연결 테스트 방법**:
1. Console 경로: {primary_service} > {resource_name}
2. "Test connection" 또는 "Validate" 버튼 클릭
3. 예상 결과: {expected_test_result}

---

### Exercise 3: 모니터링 및 알람 설정
**목표**: {exercise_3_goal}

**예상 소요 시간**: {exercise_3_time}분

**단계**:

1. **CloudWatch 대시보드 생성**
   - Console 경로: CloudWatch > Dashboards
   - "Create dashboard" 버튼 클릭
   - 대시보드 이름: `day{day_number}-{service_name}-monitoring`

2. **위젯 추가 - 메트릭 차트**
   - "Add widget" 버튼 클릭
   - 위젯 유형: Line chart
   - 메트릭 선택:
     - Namespace: {metric_namespace}
     - Metric name: {metric_name_1}
     - Dimensions: {metric_dimensions}
   - 위젯 제목: "{metric_display_name}"
   - "Create widget" 클릭

3. **위젯 추가 - 숫자 표시**
   - "Add widget" 버튼 클릭
   - 위젯 유형: Number
   - 메트릭 선택:
     - Namespace: {metric_namespace}
     - Metric name: {metric_name_2}
   - 통계: {statistic} (Average/Sum/Maximum)
   - 위젯 제목: "{metric_display_name_2}"
   - "Create widget" 클릭

4. **알람 생성**
   - Console 경로: CloudWatch > Alarms > All alarms
   - "Create alarm" 버튼 클릭
   
   - **메트릭 선택**:
     - "Select metric" 클릭
     - Namespace: {metric_namespace}
     - Metric: {alarm_metric_name}
     - "Select metric" 클릭
   
   - **조건 설정**:
     - Threshold type: Static
     - Whenever {metric_name} is: {comparison_operator}
     - than: {threshold_value}
     - Datapoints to alarm: {datapoints} out of {evaluation_periods}
   
   - **알림 설정**:
     - Alarm state trigger: In alarm
     - SNS topic: Create new topic
     - Topic name: `day{day_number}-alerts`
     - Email endpoint: {your_email}
     - "Create topic" 클릭
   
   - **알람 이름**:
     - Alarm name: `day{day_number}-{metric_name}-alert`
     - Alarm description: {alarm_description}
   
   - "Create alarm" 클릭

5. **이메일 구독 확인**
   - 이메일 확인
   - "Confirm subscription" 링크 클릭
   - 구독 확인 완료

**검증**:
- [ ] 대시보드가 생성되고 메트릭이 표시되는가?
- [ ] 알람이 "OK" 상태인가?
- [ ] SNS 토픽 구독이 확인되었는가?
- [ ] 테스트 알람이 정상 작동하는가?

**알람 테스트 방법** (선택사항):
1. 임계값을 현재 메트릭 값보다 낮게 설정
2. 약 5분 대기
3. 알람 이메일 수신 확인
4. 임계값을 원래대로 복원

---

### Exercise 4: 실제 사용 시나리오 테스트
**목표**: {exercise_4_goal}

**예상 소요 시간**: {exercise_4_time}분

**단계**:

1. **테스트 데이터 준비**
   - {test_data_preparation_step_1}
   - {test_data_preparation_step_2}

2. **기능 테스트**
   - Console 경로: {service} > {resource_name}
   - {test_action_1}:
     - 단계: {test_action_1_steps}
     - 예상 결과: {test_action_1_expected_result}
   
   - {test_action_2}:
     - 단계: {test_action_2_steps}
     - 예상 결과: {test_action_2_expected_result}

3. **성능 확인**
   - Console 경로: CloudWatch > Dashboards > day{day_number}-{service_name}-monitoring
   - 확인 항목:
     - {performance_metric_1}: {expected_value_1}
     - {performance_metric_2}: {expected_value_2}
     - {performance_metric_3}: {expected_value_3}

4. **로그 확인**
   - Console 경로: CloudWatch > Log groups > {log_group_name}
   - 최근 로그 스트림 선택
   - 확인 항목:
     - 에러 메시지 없음
     - 성공 로그 확인
     - 처리 시간 확인

**검증**:
- [ ] 모든 테스트 액션이 성공했는가?
- [ ] 성능 메트릭이 예상 범위 내인가?
- [ ] 로그에 에러가 없는가?
- [ ] 전체 워크플로우가 정상 작동하는가?

---

## ✅ 실습 완료 체크리스트

### 생성된 리소스 확인
- [ ] Exercise 1: {primary_service} 생성 완료
- [ ] Exercise 2: {related_service_1} 통합 완료
- [ ] Exercise 3: 모니터링 및 알람 설정 완료
- [ ] Exercise 4: 실제 사용 시나리오 테스트 완료

### 검증 항목
- [ ] 모든 리소스가 정상 상태인가?
- [ ] 서비스 간 통합이 올바르게 작동하는가?
- [ ] CloudWatch 메트릭이 수집되고 있는가?
- [ ] 알람이 정상 작동하는가?

### 학습 목표 달성
- [ ] {service_name}의 핵심 기능을 이해했는가?
- [ ] Console을 통한 리소스 생성 방법을 익혔는가?
- [ ] 다른 서비스와의 통합 방법을 이해했는가?
- [ ] 모니터링 및 문제 해결 방법을 익혔는가?

### 비용 확인
- [ ] Billing Dashboard에서 현재까지 발생한 비용 확인
- [ ] 예상 비용: ${estimated_total_cost}
- [ ] Free Tier 사용량 확인

---

## 🧹 리소스 정리

**중요**: 불필요한 비용 발생을 방지하기 위해 실습 후 반드시 리소스를 삭제하세요.

### 정리 순서 (역순으로 삭제)

#### 1. CloudWatch 알람 및 대시보드 삭제
**알람 삭제**:
- Console 경로: CloudWatch > Alarms > All alarms
- 선택: `day{day_number}-{metric_name}-alert`
- Actions > Delete
- 확인: "Delete" 버튼 클릭

**SNS 토픽 삭제**:
- Console 경로: SNS > Topics
- 선택: `day{day_number}-alerts`
- Delete
- 확인: "delete me" 입력 후 Delete

**대시보드 삭제**:
- Console 경로: CloudWatch > Dashboards
- 선택: `day{day_number}-{service_name}-monitoring`
- Delete dashboard
- 확인: "Delete" 버튼 클릭

#### 2. {related_service_1} 삭제
- Console 경로: {related_service_1} > Resources
- 선택: `day{day_number}-{resource_2_name}`
- Actions > Delete 또는 Remove
- 확인 메시지 입력 (필요시): `delete` 또는 리소스 이름
- 삭제 완료 대기 (약 {deletion_time_2}분)

**삭제 확인**:
- [ ] 리소스 목록에서 사라졌는가?
- [ ] 연결된 IAM 역할도 삭제되었는가? (자동 삭제되지 않는 경우 수동 삭제)

#### 3. {primary_service} 삭제
- Console 경로: {primary_service} > Resources
- 선택: `day{day_number}-{resource_name}`
- Actions > Delete
- 확인 옵션:
  - [ ] Delete associated resources (연결된 리소스도 함께 삭제)
  - [ ] Create final snapshot (필요시 - 추가 비용 발생)
- 확인 메시지 입력: `delete` 또는 리소스 이름
- 삭제 완료 대기 (약 {deletion_time_1}분)

**삭제 확인**:
- [ ] 리소스가 완전히 삭제되었는가?
- [ ] 연결된 보안 그룹이 삭제되었는가? (필요시 수동 삭제)
- [ ] 연결된 IAM 역할이 삭제되었는가? (필요시 수동 삭제)

#### 4. IAM 역할 정리 (자동 삭제되지 않은 경우)
- Console 경로: IAM > Roles
- 검색: `day{day_number}`
- 선택: 실습에서 생성한 역할들
- Delete
- 확인: "Delete" 버튼 클릭

#### 5. CloudWatch 로그 그룹 삭제 (선택사항)
- Console 경로: CloudWatch > Log groups
- 검색: `day{day_number}` 또는 `{service_name}`
- 선택: 관련 로그 그룹
- Actions > Delete log group(s)
- 확인: "Delete" 버튼 클릭

### 정리 확인 체크리스트
- [ ] 모든 {primary_service} 리소스 삭제 완료
- [ ] 모든 {related_service_1} 리소스 삭제 완료
- [ ] CloudWatch 알람 및 대시보드 삭제 완료
- [ ] SNS 토픽 삭제 완료
- [ ] IAM 역할 정리 완료 (필요시)
- [ ] CloudWatch 로그 그룹 삭제 완료 (선택사항)

### 비용 최종 확인
- Console 경로: Billing > Bills
- 확인 항목:
  - 이번 달 누적 비용: ${final_cost}
  - {service_name} 관련 비용: ${service_cost}
  - 예상 월말 비용: ${projected_cost}

**예상 비용**:
- Free Tier 범위 내 실습: $0.00
- Free Tier 초과 시: ${estimated_excess_cost}
- 리소스 정리 완료 후: $0.00 (추가 비용 없음)

---

## 🎓 학습 포인트

### 핵심 개념
1. **{concept_1}**: {concept_1_description}
   - 실습에서 배운 점: {concept_1_learning}
   - 실무 적용: {concept_1_application}

2. **{concept_2}**: {concept_2_description}
   - 실습에서 배운 점: {concept_2_learning}
   - 실무 적용: {concept_2_application}

3. **{concept_3}**: {concept_3_description}
   - 실습에서 배운 점: {concept_3_learning}
   - 실무 적용: {concept_3_application}

### Console 사용 팁
- **빠른 탐색**: Services 메뉴 대신 검색 기능 활용 (Alt+S)
- **즐겨찾기**: 자주 사용하는 서비스를 즐겨찾기에 추가
- **리전 확인**: 작업 전 항상 올바른 리전 선택 확인
- **태그 활용**: 리소스 관리를 위해 일관된 태그 전략 사용
- **비용 모니터링**: Billing Dashboard를 정기적으로 확인

### 문제 해결 경험
이 실습에서 발생할 수 있는 일반적인 문제:

1. **권한 부족 에러**
   - 원인: IAM 사용자에게 필요한 권한 없음
   - 해결: IAM 정책 확인 및 필요한 권한 추가

2. **리소스 생성 실패**
   - 원인: {common_failure_reason}
   - 해결: {common_failure_solution}

3. **연결 실패**
   - 원인: Security Group 또는 Network ACL 설정 문제
   - 해결: 네트워크 설정 검토 및 수정

### 다음 단계
이 실습을 완료한 후:

1. **심화 학습**:
   - [Case Study](../case-study.md) - 실제 기업 사례 분석
   - [Best Practices](../best-practices.md) - 프로덕션 환경 고려사항
   - [Troubleshooting](../troubleshooting.md) - 고급 문제 해결 방법

2. **추가 실습**:
   - 다른 리전에서 동일한 구성 재현
   - 다른 서비스와의 추가 통합
   - 성능 테스트 및 최적화

3. **실무 적용**:
   - 학습한 내용을 실제 프로젝트에 적용
   - 팀과 지식 공유
   - 추가 AWS 서비스 탐색

---

## 🔗 관련 학습 자료

### 이론 학습
- [Day {day_number} Theory](../theory.md) - {service_name} 기본 개념
- [Day {previous_day} Theory](../../day{previous_day}/theory.md) - 사전 학습 내용
- [Day {next_day} Theory](../../day{next_day}/theory.md) - 다음 학습 내용

### 심화 학습
- [Case Study](../case-study.md) - {company_name}의 {service_name} 활용 사례
- [Best Practices](../best-practices.md) - {service_name} 베스트 프랙티스
- [Troubleshooting](../troubleshooting.md) - 일반적인 문제 및 해결 방법

### AWS 공식 문서
- [{service_name} User Guide]({user_guide_link})
- [{service_name} API Reference]({api_reference_link})
- [AWS Console User Guide]({console_guide_link})
- [Getting Started with {service_name}]({getting_started_link})

### 추가 실습 자료
- [AWS Hands-On Tutorials]({aws_tutorials_link})
- [AWS Workshops]({aws_workshops_link})
- [AWS Skill Builder]({skill_builder_link})

---

## 💬 피드백 및 질문

### 실습 피드백
이 실습에 대한 피드백을 공유해주세요:
- 어려웠던 부분
- 개선이 필요한 부분
- 추가로 다루었으면 하는 내용

### 자주 묻는 질문

**Q1: Free Tier를 초과하면 어떻게 되나요?**
A: {free_tier_answer}

**Q2: 실습 중 에러가 발생하면 어떻게 하나요?**
A: {error_handling_answer}

**Q3: 리소스 정리를 잊어버리면 어떻게 되나요?**
A: {cleanup_forgotten_answer}

**Q4: 다른 리전에서도 동일하게 작동하나요?**
A: {region_compatibility_answer}

**Q5: 실무에서는 어떻게 다르게 구성하나요?**
A: {production_difference_answer}

---

## 📝 실습 노트

### 개인 메모
실습 중 배운 점이나 중요한 사항을 기록하세요:

```
날짜: {date}
실습 시간: {actual_time}분
어려웠던 점:
-

배운 점:
-

다음에 시도해볼 것:
-
```

### 스크린샷 저장 (권장)
주요 단계의 스크린샷을 저장하여 나중에 참고하세요:
- [ ] {primary_service} 생성 완료 화면
- [ ] {related_service_1} 통합 완료 화면
- [ ] CloudWatch 대시보드
- [ ] 테스트 결과 화면

---

**작성 가이드**:
- 각 섹션의 `{placeholder}` 부분을 실제 내용으로 대체하세요
- Console 경로는 정확하게 작성하세요 (Services > Category > Service)
- 모든 단계는 AWS Console 기반으로 작성하세요
- 스크린샷 참조는 선택사항으로 표시하세요
- 사전 요구사항 문서는 상대 경로로 링크하세요
- 예상 비용과 소요 시간은 실제 테스트 기반으로 작성하세요
- 리소스 정리 단계는 역순으로 명확하게 작성하세요
