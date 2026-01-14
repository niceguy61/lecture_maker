# {company_name} - {case_study_focus}

> **Day {day_number}: {day_title}**  
> **주요 AWS 서비스**: {primary_services}

---

## 📋 사례 개요

- **기업명**: {company_name}
- **업종**: {industry}
- **규모**: {company_size} <!-- Startup/Medium/Enterprise -->
- **주요 AWS 서비스**: {primary_services}
- **사례 출처**: {case_source} <!-- 공개 자료 링크 또는 "AWS Well-Architected Framework 기반" -->
- **사례 유형**: {case_type} <!-- "실제 기업 사례" 또는 "Best Practice 기반 가상 사례" -->

---

## 🎯 비즈니스 도전과제

### 문제 상황

{business_challenge_description}

**구체적인 문제점**:
- {problem_point_1}
- {problem_point_2}
- {problem_point_3}

**기술적 제약사항**:
- {technical_constraint_1}
- {technical_constraint_2}

**기존 인프라의 한계**:
- {infrastructure_limitation_1}
- {infrastructure_limitation_2}

### 요구사항

**성능 요구사항**:
- {performance_requirement_1} (예: 응답시간 < 100ms)
- {performance_requirement_2} (예: 처리량 > 10,000 TPS)

**확장성 요구사항**:
- {scalability_requirement_1} (예: 동시 사용자 100만명 지원)
- {scalability_requirement_2} (예: 트래픽 10배 증가 대응)

**보안 및 규정 준수 요구사항**:
- {security_requirement_1}
- {compliance_requirement_1}

**비용 제약사항**:
- {cost_constraint_1}
- {cost_constraint_2}

---

## 🏗️ AWS 솔루션 아키텍처

### 아키텍처 다이어그램

```mermaid
{architecture_diagram}
```

> 📁 **상세 다이어그램**: [architecture-diagrams/main-architecture.mmd](./architecture-diagrams/main-architecture.mmd)

### 핵심 서비스 구성

#### {primary_service_1} (Day {day_number} 주요 서비스)

**선택 이유**:
- {selection_reason_1}
- {selection_reason_2}

**구성 방법** (AWS Console 기준):
1. **Console 경로**: Services > {service_category} > {service_name}
2. **주요 설정**:
   - {config_item_1}: {config_value_1}
   - {config_item_2}: {config_value_2}
   - {config_item_3}: {config_value_3}

**다른 서비스와의 연계**:
- **{related_service_1}** (Day {related_day_1}): {integration_description_1}
- **{related_service_2}** (Day {related_day_2}): {integration_description_2}

#### {supporting_service_1}

**역할**: {service_role_description}

**구성 방법**:
- {config_summary}

**연계 방식**: {integration_method}

### 서비스 간 데이터 플로우

```mermaid
{data_flow_diagram}
```

**플로우 설명**:
1. **사용자 요청** → {service_a}
   - {flow_step_1_description}
   
2. **{service_a}** → **{service_b}** (Day {day_number}의 주요 서비스)
   - {flow_step_2_description}
   
3. **{service_b}** → **{service_c}**
   - {flow_step_3_description}

4. **응답 반환** → 사용자
   - {flow_step_4_description}

---

## 💻 구현 세부사항

### AWS Console 기반 설정

#### 1단계: {primary_service} 생성

**Console 경로**: Services > {category} > {service} > Create {resource}

**기본 설정**:
- **Name/ID**: `{resource_name_example}`
- **Region**: `{region}` (예: ap-northeast-2 - 서울)
- **{config_field_1}**: {config_value_1}
- **{config_field_2}**: {config_value_2}

**고급 설정**:
- **{advanced_config_1}**: {advanced_value_1}
  - 설명: {config_explanation_1}
- **{advanced_config_2}**: {advanced_value_2}
  - 설명: {config_explanation_2}

**생성 확인**:
- 상태가 "Available" 또는 "Active"로 변경될 때까지 대기 (약 {wait_time}분)
- Console에서 리소스 상세 정보 확인

#### 2단계: {related_service} 연계 구성

**Console 경로**: Services > {category} > {service}

**연결 설정**:
1. {primary_service}에서 생성한 리소스 선택
2. "Actions" > "Configure {integration_feature}"
3. {related_service} 리소스 선택 또는 생성
4. 연결 설정 저장

**검증**:
- {verification_step_1}
- {verification_step_2}

#### 3단계: 보안 및 접근 제어 설정

**IAM 역할 구성** (Day 2 연계):
- Console 경로: IAM > Roles > Create role
- 신뢰 관계: {trust_policy}
- 권한 정책: {permission_policy}

**네트워크 보안** (Day 5 연계):
- Security Group 설정
- Network ACL 구성 (필요시)

### 설정 파일 예시 (참고용)

#### CloudFormation 템플릿 (선택사항)

```yaml
# {resource_name}-stack.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: '{case_study_name} - {primary_service} 구성'

Resources:
  {ResourceLogicalId}:
    Type: AWS::{ServiceNamespace}::{ResourceType}
    Properties:
      {Property1}: {Value1}
      {Property2}: {Value2}
      Tags:
        - Key: Project
          Value: {project_name}
        - Key: Environment
          Value: {environment}
```

#### Terraform 예시 (선택사항)

```hcl
# main.tf
resource "aws_{resource_type}" "{resource_name}" {
  {property_1} = "{value_1}"
  {property_2} = "{value_2}"
  
  tags = {
    Project     = "{project_name}"
    Environment = "{environment}"
  }
}
```

### 모니터링 설정

#### CloudWatch 메트릭 구성

**Console 경로**: CloudWatch > Metrics > {service_namespace}

**핵심 메트릭**:
- **{metric_1}**: {metric_description_1}
  - 정상 범위: {normal_range_1}
  - 경고 임계값: {warning_threshold_1}
  
- **{metric_2}**: {metric_description_2}
  - 정상 범위: {normal_range_2}
  - 경고 임계값: {warning_threshold_2}

#### 알람 설정

**Console 경로**: CloudWatch > Alarms > Create alarm

**알람 구성**:
```yaml
알람명: {alarm_name}
메트릭: {metric_name}
조건: {condition} (예: >= 80%)
기간: {period} (예: 5분)
평가 기간: {evaluation_periods} (예: 2회 연속)
알림: {sns_topic_arn}
```

#### 대시보드 구성

**Console 경로**: CloudWatch > Dashboards > Create dashboard

**위젯 구성**:
- {widget_1}: {metric_visualization_1}
- {widget_2}: {metric_visualization_2}
- {widget_3}: {metric_visualization_3}

---

## 📊 비즈니스 임팩트

### 성능 개선

| 지표 | 개선 전 | 개선 후 | 개선율 |
|------|---------|---------|--------|
| {metric_1} | {before_value_1} | {after_value_1} | {improvement_1}% |
| {metric_2} | {before_value_2} | {after_value_2} | {improvement_2}% |
| {metric_3} | {before_value_3} | {after_value_3} | {improvement_3}% |

**주요 성과**:
- {achievement_1}
- {achievement_2}
- {achievement_3}

### 비용 최적화

**월간 비용 변화**:
- **개선 전**: ${cost_before}/월
- **개선 후**: ${cost_after}/월
- **절감액**: ${cost_savings}/월 ({cost_reduction_percentage}% 절감)

**비용 절감 요인**:
1. {cost_factor_1}: ${savings_1}/월
2. {cost_factor_2}: ${savings_2}/월
3. {cost_factor_3}: ${savings_3}/월

**ROI 분석**:
- 초기 투자: ${initial_investment}
- 월간 절감: ${monthly_savings}
- 투자 회수 기간: {payback_period}개월

### 운영 효율성

**배포 및 운영 개선**:
- **배포 시간**: {deploy_time_before} → {deploy_time_after} ({deploy_improvement}% 단축)
- **장애 복구 시간**: {mttr_before} → {mttr_after} ({mttr_improvement}% 개선)
- **운영 인력**: {ops_team_before}명 → {ops_team_after}명

**가용성 향상**:
- **서비스 가동률**: {uptime_before}% → {uptime_after}%
- **연간 다운타임**: {downtime_before}시간 → {downtime_after}시간

---

## 🔗 다른 서비스와의 연계

### 이전 학습 내용과의 연결

#### Day {previous_day_1}: {previous_service_1}
**연계 방식**: {integration_description_1}

**이 사례에서의 활용**:
- {usage_in_case_1}
- {usage_in_case_2}

**학습 포인트**:
- {learning_point_1}

#### Day {previous_day_2}: {previous_service_2}
**연계 방식**: {integration_description_2}

**이 사례에서의 활용**:
- {usage_in_case_3}

### 향후 학습 내용 예고

#### Day {future_day_1}: {future_service_1}
**확장 방향**: {expansion_description_1}

**이 사례의 진화**:
- {evolution_point_1}
- {evolution_point_2}

**기대 효과**:
- {expected_benefit_1}

#### Day {future_day_2}: {future_service_2}
**확장 방향**: {expansion_description_2}

**추가 통합 시나리오**:
- {integration_scenario_1}

### 전체 아키텍처에서의 역할

```mermaid
{cross_day_integration_diagram}
```

**통합 시나리오 설명**:
- {integration_scenario_description}

**서비스 의존성**:
- Day {day_1} ({service_1}) → Day {day_2} ({service_2})
- Day {day_2} ({service_2}) → Day {day_3} ({service_3})

---

## 📚 참고 자료

### AWS 공식 문서
- [{service_name} 사용 설명서]({aws_docs_url})
- [{service_name} API 레퍼런스]({api_reference_url})
- [AWS Well-Architected Framework - {pillar}]({well_architected_url})

### 아키텍처 및 베스트 프랙티스
- [AWS 아키텍처 센터 - {architecture_pattern}]({architecture_center_url})
- [{service_name} 베스트 프랙티스]({best_practices_url})
- [보안 베스트 프랙티스 - {security_topic}]({security_docs_url})

### 비용 최적화
- [AWS 요금 계산기]({pricing_calculator_url})
- [{service_name} 요금 안내]({pricing_url})
- [비용 최적화 가이드]({cost_optimization_url})

### 기업 사례 및 발표 자료
- [{company_name} 공식 블로그 포스트]({company_blog_url})
- [AWS re:Invent 발표: {presentation_title}]({reinvent_url})
- [AWS 고객 사례 연구]({case_study_url})

### 화이트페이퍼
- [{whitepaper_title}]({whitepaper_url})

---

## 🎓 학습 포인트

### 1. {primary_service}의 실제 활용 방법
- {learning_point_1_1}
- {learning_point_1_2}
- {learning_point_1_3}

### 2. 대규모 시스템에서의 고려사항
- **확장성**: {scalability_consideration}
- **가용성**: {availability_consideration}
- **성능**: {performance_consideration}
- **보안**: {security_consideration}

### 3. 다른 서비스와의 통합 패턴
- {integration_pattern_1}
- {integration_pattern_2}
- {integration_pattern_3}

### 4. 비용 최적화 전략
- {cost_strategy_1}
- {cost_strategy_2}
- {cost_strategy_3}

### 5. 운영 및 모니터링 베스트 프랙티스
- {ops_best_practice_1}
- {ops_best_practice_2}
- {ops_best_practice_3}

---

## 🚀 다음 단계

### 실습 진행
1. [hands-on-console/README.md](./hands-on-console/README.md)에서 실습 가이드 확인
2. AWS Console을 통해 직접 아키텍처 구성
3. 모니터링 및 최적화 실습

### 심화 학습
1. [best-practices.md](./best-practices.md)에서 프로덕션 환경 고려사항 학습
2. [troubleshooting.md](./troubleshooting.md)에서 문제 해결 방법 학습
3. [architecture-diagrams/](./architecture-diagrams/)에서 상세 다이어그램 확인

### 관련 학습
- Day {related_day_1}: {related_topic_1}
- Day {related_day_2}: {related_topic_2}
- Day {related_day_3}: {related_topic_3}

---

## 📝 작성 가이드 (템플릿 사용 시 삭제)

### 플레이스홀더 치환 규칙

**기본 정보**:
- `{day_number}`: 일차 번호 (1-28)
- `{day_title}`: 일별 학습 주제 제목
- `{company_name}`: 기업명 (실제 또는 가상)
- `{case_study_focus}`: 사례 연구 초점 (예: "글로벌 스트리밍 아키텍처")

**서비스 정보**:
- `{primary_services}`: 주요 AWS 서비스 목록 (쉼표로 구분)
- `{primary_service}`: 주요 서비스 단수형
- `{related_service}`: 연계 서비스명

**다이어그램**:
- `{architecture_diagram}`: Mermaid 아키텍처 다이어그램 코드
- `{data_flow_diagram}`: Mermaid 데이터 플로우 다이어그램 코드
- `{cross_day_integration_diagram}`: 크로스 데이 통합 다이어그램 코드

**메트릭 및 수치**:
- `{metric_name}`: 메트릭 이름
- `{before_value}`: 개선 전 값
- `{after_value}`: 개선 후 값
- `{improvement}`: 개선율 (%)

**URL 및 링크**:
- `{aws_docs_url}`: AWS 공식 문서 URL
- `{api_reference_url}`: API 레퍼런스 URL
- `{company_blog_url}`: 기업 블로그 URL

### 작성 시 주의사항

1. **실제 데이터 사용**: 가능한 한 실제 기업의 공개된 데이터 사용
2. **구체적인 수치**: 모호한 표현 대신 구체적인 수치와 메트릭 제공
3. **Console 경로**: 정확한 AWS Console 경로 명시
4. **한국어 품질**: 전문적이고 일관된 한국어 사용, 기술 용어는 한영 병기
5. **링크 유효성**: 모든 AWS 문서 링크는 최신 URL 사용
6. **다이어그램 품질**: Mermaid 다이어그램은 렌더링 가능한 유효한 구문 사용
7. **크로스 레퍼런스**: 다른 일차 및 문서와의 연계 명확히 표시

### 필수 섹션 체크리스트

- [ ] 사례 개요 (기업 정보, 사례 유형 명시)
- [ ] 비즈니스 도전과제 (구체적 문제 상황 및 요구사항)
- [ ] AWS 솔루션 아키텍처 (다이어그램 포함)
- [ ] 구현 세부사항 (Console 기반 단계별 가이드)
- [ ] 비즈니스 임팩트 (성능, 비용, 운영 개선 수치)
- [ ] 서비스 연계 (이전/향후 학습 내용 연결)
- [ ] 참고 자료 (AWS 공식 문서 링크)
- [ ] 학습 포인트 (핵심 takeaway)

---

**템플릿 버전**: 1.0  
**최종 수정일**: {current_date}  
**작성자**: {author_name}
