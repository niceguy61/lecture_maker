# Day 22 퀴즈: CloudWatch & 모니터링

## 퀴즈 개요
- **주제**: AWS CloudWatch 및 모니터링 서비스
- **문제 수**: 5문제
- **예상 소요 시간**: 10분
- **난이도**: 중급

---

## 문제 1
**AWS CloudWatch에서 기본 메트릭(Default Metrics)과 사용자 정의 메트릭(Custom Metrics)에 대한 설명으로 올바른 것은?**

A) 기본 메트릭은 1분 간격으로 수집되며, 사용자 정의 메트릭은 5분 간격으로만 수집 가능하다

B) 기본 메트릭은 무료로 제공되며 5분 간격으로 수집되고, 사용자 정의 메트릭은 비용이 발생하며 1초 단위까지 수집 가능하다

C) 기본 메트릭과 사용자 정의 메트릭 모두 동일한 비용이 발생한다

D) 사용자 정의 메트릭은 AWS 서비스에서만 생성할 수 있으며, 애플리케이션에서는 생성할 수 없다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B**

**해설:**
- **기본 메트릭**: AWS 서비스에서 자동으로 제공되며 무료입니다. 기본적으로 5분 간격으로 수집되며, 상세 모니터링을 활성화하면 1분 간격으로 수집됩니다.
- **사용자 정의 메트릭**: 애플리케이션에서 직접 전송하는 메트릭으로 비용이 발생합니다. 1초 단위까지 세밀한 모니터링이 가능합니다.
- A는 틀렸습니다. 기본 메트릭도 상세 모니터링 시 1분 간격 가능합니다.
- C는 틀렸습니다. 기본 메트릭은 무료, 사용자 정의 메트릭은 유료입니다.
- D는 틀렸습니다. 사용자 정의 메트릭은 애플리케이션에서 AWS SDK/CLI를 통해 생성할 수 있습니다.

</details>

---

## 문제 2
**CloudWatch 알람의 상태(State)에 대한 설명으로 올바른 것은?**

A) OK, ALARM, PENDING 세 가지 상태가 있다

B) OK, ALARM, INSUFFICIENT_DATA 세 가지 상태가 있으며, INSUFFICIENT_DATA는 메트릭 데이터가 부족할 때 나타난다

C) 알람은 ALARM 상태일 때만 작업(Action)을 수행할 수 있다

D) 알람 상태는 수동으로만 변경할 수 있으며, 자동으로 변경되지 않는다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B**

**해설:**
CloudWatch 알람은 다음 세 가지 상태를 가집니다:
- **OK**: 메트릭이 정의된 임계값 내에 있는 상태
- **ALARM**: 메트릭이 임계값을 초과한 상태
- **INSUFFICIENT_DATA**: 알람을 평가하기에 충분한 데이터가 없는 상태

- A는 틀렸습니다. PENDING 상태는 없습니다.
- C는 틀렸습니다. OK 상태나 INSUFFICIENT_DATA 상태에서도 작업을 수행하도록 설정할 수 있습니다.
- D는 틀렸습니다. 알람 상태는 메트릭 데이터에 따라 자동으로 변경됩니다.

</details>

---

## 문제 3
**다음 CloudWatch Logs Insights 쿼리의 목적으로 가장 적절한 것은?**

```sql
fields @timestamp, @message
| filter @message like /ERROR/
| stats count() by bin(1h)
| sort @timestamp desc
```

A) 최근 에러 메시지 20개를 시간순으로 정렬하여 표시

B) 시간대별로 에러 발생 건수를 집계하여 최신 시간순으로 정렬

C) 에러 메시지를 포함한 모든 로그를 1시간 단위로 그룹화

D) 에러 로그의 타임스탬프와 메시지만 필터링하여 표시

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B**

**해설:**
이 쿼리는 다음과 같이 동작합니다:
1. `fields @timestamp, @message`: 타임스탬프와 메시지 필드 선택
2. `filter @message like /ERROR/`: ERROR가 포함된 메시지만 필터링
3. `stats count() by bin(1h)`: 1시간 단위로 그룹화하여 건수 집계
4. `sort @timestamp desc`: 최신 시간순으로 정렬

- A는 틀렸습니다. `limit 20`이 없고, `stats count()`로 집계하고 있습니다.
- C는 틀렸습니다. 에러 메시지만 필터링하고 있습니다.
- D는 틀렸습니다. `stats count()`로 집계 작업을 수행하고 있습니다.

</details>

---

## 문제 4
**회사에서 EC2 인스턴스의 CPU 사용률이 80%를 초과하면 자동으로 인스턴스를 추가하고, 관리자에게 이메일 알림을 보내려고 합니다. 이를 구현하기 위해 필요한 AWS 서비스 조합으로 가장 적절한 것은?**

A) CloudWatch + SNS + Lambda

B) CloudWatch + SNS + Auto Scaling

C) CloudWatch + SQS + Auto Scaling

D) CloudWatch + EventBridge + EC2

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B**

**해설:**
요구사항을 분석하면:
1. CPU 사용률 80% 초과 감지 → **CloudWatch 알람**
2. 자동으로 인스턴스 추가 → **Auto Scaling 그룹**
3. 관리자에게 이메일 알림 → **SNS (Simple Notification Service)**

CloudWatch 알람은 두 가지 작업을 동시에 수행할 수 있습니다:
- Auto Scaling 작업: 인스턴스 자동 확장
- SNS 알림: 이메일 발송

- A는 틀렸습니다. Lambda는 인스턴스 자동 추가에 직접적으로 사용되지 않습니다.
- C는 틀렸습니다. SQS는 메시지 큐 서비스로 이메일 알림에 적합하지 않습니다.
- D는 틀렸습니다. EventBridge만으로는 이메일 알림을 직접 보낼 수 없습니다.

</details>

---

## 문제 5
**CloudWatch의 이상 탐지(Anomaly Detection) 기능에 대한 설명으로 올바른 것은?**

A) 이상 탐지는 정적 임계값만 사용하여 알람을 트리거한다

B) 이상 탐지 모델은 즉시 생성되며, 설정 후 바로 사용할 수 있다

C) 이상 탐지는 머신러닝을 사용하여 과거 데이터 패턴을 학습하고, 예상 범위를 벗어나는 값을 감지한다

D) 이상 탐지는 사용자 정의 메트릭에서만 사용할 수 있으며, AWS 기본 메트릭에서는 사용할 수 없다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: C**

**해설:**
CloudWatch 이상 탐지(Anomaly Detection)의 특징:
- **머신러닝 기반**: 과거 데이터 패턴을 학습하여 정상 범위를 예측
- **동적 임계값**: 시간대, 요일, 계절성 등을 고려한 동적 임계값 설정
- **예상 범위**: 정상 범위를 밴드 형태로 표시하고, 이를 벗어나는 값을 이상으로 감지
- **학습 기간**: 모델이 충분히 학습하기까지 약 24시간 소요

- A는 틀렸습니다. 이상 탐지는 동적 임계값을 사용합니다.
- B는 틀렸습니다. 모델 학습에 시간이 필요합니다(약 24시간).
- D는 틀렸습니다. AWS 기본 메트릭과 사용자 정의 메트릭 모두에서 사용 가능합니다.

**추가 정보:**
- 이상 탐지 임계값은 표준편차 단위로 설정 (일반적으로 2 표준편차)
- 계절성, 트렌드, 시간대별 패턴을 자동으로 학습
- 정적 임계값보다 거짓 양성(False Positive)을 줄일 수 있음

</details>

---

## 퀴즈 완료

### 점수 계산
- 5문제 중 맞힌 개수: ___/5
- 정답률: ___%

### 복습이 필요한 영역
점수에 따른 복습 권장사항:

**5점 (100%)**: 완벽합니다! CloudWatch 개념을 잘 이해하고 있습니다.

**4점 (80%)**: 우수합니다. 틀린 문제 영역을 한 번 더 복습해보세요.

**3점 (60%)**: 보통입니다. 다음 영역을 중점적으로 복습하세요:
- CloudWatch 메트릭 유형과 특징
- 알람 상태와 작업 설정
- Logs Insights 쿼리 문법

**2점 이하 (40% 이하)**: 이론 내용을 다시 한 번 정독하고, 실습을 통해 실제 경험을 쌓아보세요.

### 다음 학습 단계
- Day 23: CloudTrail & 보안 서비스
- 실습을 통한 실제 CloudWatch 환경 구성 경험
- AWS 공식 문서를 통한 심화 학습

### 추가 학습 자료
- [CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/)
- [CloudWatch Metrics and Dimensions](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/aws-services-cloudwatch-metrics.html)
- [CloudWatch Logs Insights Query Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)