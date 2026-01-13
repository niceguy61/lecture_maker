# Day 22 실습: CloudWatch 대시보드 및 알람 설정

## 실습 개요
이번 실습에서는 AWS CloudWatch를 사용하여 EC2 인스턴스를 모니터링하는 대시보드를 생성하고, 성능 임계값을 초과할 때 알람을 받을 수 있도록 설정해보겠습니다.

## 사전 준비사항
- AWS 계정 및 Console 접근 권한
- 실행 중인 EC2 인스턴스 (없다면 t2.micro 인스턴스 1개 생성)
- SNS 알림을 받을 이메일 주소

## 실습 목표
- CloudWatch 메트릭 이해 및 확인
- 사용자 정의 대시보드 생성
- CloudWatch 알람 설정
- SNS를 통한 알림 구성
- 로그 그룹 생성 및 관리

---

## 실습 1: EC2 인스턴스 메트릭 확인

### 1.1 CloudWatch Console 접근
1. AWS Management Console에 로그인
2. 서비스 검색에서 "CloudWatch" 입력 후 선택
3. 왼쪽 메뉴에서 "Metrics" → "All metrics" 클릭

### 1.2 EC2 메트릭 탐색
1. "Browse" 탭에서 "EC2" 클릭
2. "Per-Instance Metrics" 선택
3. 실행 중인 EC2 인스턴스 확인
4. 다음 메트릭들을 확인해보세요:
   - `CPUUtilization`: CPU 사용률
   - `NetworkIn`: 네트워크 입력 바이트
   - `NetworkOut`: 네트워크 출력 바이트
   - `DiskReadOps`: 디스크 읽기 작업 수
   - `DiskWriteOps`: 디스크 쓰기 작업 수

### 1.3 메트릭 그래프 보기
1. `CPUUtilization` 메트릭 체크박스 선택
2. "Graphed metrics" 탭으로 이동
3. 시간 범위를 "Last 1 hour"로 설정
4. 그래프에서 CPU 사용률 패턴 관찰

**📸 스크린샷 포인트**: EC2 메트릭 목록과 CPU 사용률 그래프

---

## 실습 2: CloudWatch 대시보드 생성

### 2.1 새 대시보드 생성
1. 왼쪽 메뉴에서 "Dashboards" 클릭
2. "Create dashboard" 버튼 클릭
3. 대시보드 이름: `EC2-Monitoring-Dashboard` 입력
4. "Create dashboard" 클릭

### 2.2 첫 번째 위젯 추가 (CPU 사용률)
1. "Add widget" 버튼 클릭
2. "Line" 위젯 타입 선택 → "Next"
3. "Metrics" 데이터 소스 선택
4. "EC2" → "Per-Instance Metrics" 선택
5. 해당 인스턴스의 `CPUUtilization` 선택
6. "Create widget" 클릭

### 2.3 두 번째 위젯 추가 (네트워크 트래픽)
1. "Add widget" 버튼 클릭
2. "Line" 위젯 타입 선택 → "Next"
3. "Metrics" 데이터 소스 선택
4. "EC2" → "Per-Instance Metrics" 선택
5. 해당 인스턴스의 `NetworkIn`과 `NetworkOut` 모두 선택
6. "Create widget" 클릭

### 2.4 세 번째 위젯 추가 (디스크 I/O)
1. "Add widget" 버튼 클릭
2. "Line" 위젯 타입 선택 → "Next"
3. "Metrics" 데이터 소스 선택
4. "EC2" → "Per-Instance Metrics" 선택
5. 해당 인스턴스의 `DiskReadOps`와 `DiskWriteOps` 선택
6. "Create widget" 클릭

### 2.5 대시보드 저장
1. "Save dashboard" 버튼 클릭
2. 대시보드 레이아웃 확인

**📸 스크린샷 포인트**: 완성된 대시보드 화면

---

## 실습 3: SNS 토픽 생성 (알람용)

### 3.1 SNS Console 접근
1. 새 탭에서 AWS Console 열기
2. 서비스 검색에서 "SNS" 입력 후 선택
3. "Topics" 메뉴 클릭

### 3.2 SNS 토픽 생성
1. "Create topic" 버튼 클릭
2. Type: "Standard" 선택
3. Name: `cloudwatch-alerts` 입력
4. Display name: `CloudWatch Alerts` 입력
5. "Create topic" 클릭

### 3.3 이메일 구독 추가
1. 생성된 토픽 클릭
2. "Create subscription" 버튼 클릭
3. Protocol: "Email" 선택
4. Endpoint: 알림을 받을 이메일 주소 입력
5. "Create subscription" 클릭
6. 이메일 확인 후 구독 승인

**📸 스크린샷 포인트**: SNS 토픽 생성 완료 화면

---

## 실습 4: CloudWatch 알람 생성

### 4.1 CPU 사용률 알람 생성
1. CloudWatch Console로 돌아가기
2. 왼쪽 메뉴에서 "Alarms" → "All alarms" 클릭
3. "Create alarm" 버튼 클릭

### 4.2 메트릭 선택
1. "Select metric" 클릭
2. "EC2" → "Per-Instance Metrics" 선택
3. 해당 인스턴스의 `CPUUtilization` 선택
4. "Select metric" 클릭

### 4.3 알람 조건 설정
1. **Metric name**: CPUUtilization (자동 설정됨)
2. **Statistic**: Average 선택
3. **Period**: 5 minutes 선택
4. **Threshold type**: Static 선택
5. **Whenever CPUUtilization is**: Greater 선택
6. **than**: `80` 입력
7. **Datapoints to alarm**: `2 out of 2` 선택
8. **Missing data treatment**: "Treat missing data as not breaching threshold" 선택
9. "Next" 클릭

### 4.4 알람 작업 설정
1. **Alarm state trigger**: In alarm 선택
2. **Send a notification to**: 앞서 생성한 SNS 토픽 선택
3. "Next" 클릭

### 4.5 알람 이름 및 설명
1. **Alarm name**: `High-CPU-Utilization` 입력
2. **Alarm description**: `Alert when CPU utilization exceeds 80% for 2 consecutive periods` 입력
3. "Next" 클릭
4. 설정 검토 후 "Create alarm" 클릭

### 4.6 추가 알람 생성 (네트워크 트래픽)
1. "Create alarm" 버튼 클릭
2. "EC2" → "Per-Instance Metrics" → `NetworkOut` 선택
3. 조건 설정:
   - **Statistic**: Sum
   - **Period**: 5 minutes
   - **Threshold**: Greater than `1000000` (1MB)
4. 동일한 SNS 토픽으로 알림 설정
5. **Alarm name**: `High-Network-Out` 입력

**📸 스크린샷 포인트**: 생성된 알람 목록

---

## 실습 5: CloudWatch Logs 설정

### 5.1 로그 그룹 생성
1. 왼쪽 메뉴에서 "Logs" → "Log groups" 클릭
2. "Create log group" 버튼 클릭
3. **Log group name**: `/aws/ec2/application-logs` 입력
4. **Retention setting**: 7 days 선택
5. "Create" 클릭

### 5.2 로그 스트림 생성
1. 생성된 로그 그룹 클릭
2. "Create log stream" 버튼 클릭
3. **Log stream name**: `instance-i-1234567890abcdef0` (실제 인스턴스 ID 사용)
4. "Create log stream" 클릭

### 5.3 샘플 로그 이벤트 추가 (선택사항)
1. 생성된 로그 스트림 클릭
2. "Upload batch" 버튼 클릭
3. 샘플 로그 메시지 입력:
```
2024-01-13 10:00:00 INFO Application started successfully
2024-01-13 10:01:00 INFO Processing user request
2024-01-13 10:02:00 ERROR Database connection failed
2024-01-13 10:03:00 INFO Retrying database connection
2024-01-13 10:04:00 INFO Database connection restored
```
4. "Upload" 클릭

**📸 스크린샷 포인트**: 로그 그룹과 로그 이벤트 화면

---

## 실습 6: CloudWatch Insights 쿼리

### 6.1 Logs Insights 접근
1. 왼쪽 메뉴에서 "Logs" → "Logs Insights" 클릭
2. **Select log group(s)**: 앞서 생성한 로그 그룹 선택
3. **Time range**: Last 1 hour 선택

### 6.2 기본 쿼리 실행
1. 쿼리 편집기에 다음 입력:
```sql
fields @timestamp, @message
| sort @timestamp desc
| limit 20
```
2. "Run query" 버튼 클릭
3. 결과 확인

### 6.3 에러 로그 필터링 쿼리
1. 새 쿼리 입력:
```sql
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
```
2. "Run query" 버튼 클릭
3. 에러 로그만 필터링된 결과 확인

**📸 스크린샷 포인트**: Logs Insights 쿼리 결과

---

## 실습 7: 알람 테스트

### 7.1 CPU 부하 생성 (선택사항)
EC2 인스턴스에 SSH 접속 후 다음 명령어로 CPU 부하 생성:
```bash
# Linux의 경우
stress --cpu 2 --timeout 600s

# 또는 간단한 무한 루프
while true; do echo "CPU load test"; done
```

### 7.2 알람 상태 확인
1. CloudWatch Console의 "Alarms" 페이지에서 알람 상태 모니터링
2. 알람이 "In alarm" 상태로 변경되는지 확인
3. 이메일 알림 수신 확인

### 7.3 대시보드에서 실시간 모니터링
1. 생성한 대시보드로 이동
2. CPU 사용률 그래프에서 부하 증가 확인
3. 자동 새로고침 설정: "Auto refresh" → "1m" 선택

**📸 스크린샷 포인트**: 알람 트리거된 상태와 이메일 알림

---

## 실습 8: 이상 탐지 알람 (고급)

### 8.1 이상 탐지 알람 생성
1. "Create alarm" 버튼 클릭
2. "EC2" → "Per-Instance Metrics" → `CPUUtilization` 선택
3. **Threshold type**: "Anomaly detection" 선택
4. **Anomaly threshold**: 2 (표준편차) 입력
5. 나머지 설정은 이전과 동일하게 구성
6. **Alarm name**: `CPU-Anomaly-Detection` 입력

### 8.2 이상 탐지 모델 확인
1. 알람 생성 후 메트릭 그래프에서 예상 범위 밴드 확인
2. 모델이 학습되는 과정 관찰 (24시간 소요)

**📸 스크린샷 포인트**: 이상 탐지 알람 설정 화면

---

## 실습 9: 복합 알람 생성

### 9.1 복합 알람 생성
1. "Create alarm" 버튼 클릭
2. **Alarm type**: "Composite alarm" 선택
3. **Alarm name**: `Critical-System-Alert` 입력
4. **Alarm rule**: 다음과 같이 설정
```
ALARM("High-CPU-Utilization") OR ALARM("High-Network-Out")
```
5. 알림 설정은 동일한 SNS 토픽 사용
6. "Create alarm" 클릭

### 9.2 복합 알람 테스트
1. 개별 알람 중 하나를 수동으로 "In alarm" 상태로 변경
2. 복합 알람도 함께 트리거되는지 확인

**📸 스크린샷 포인트**: 복합 알람 설정 및 상태

---

## 실습 10: 비용 모니터링 설정

### 10.1 Billing 알람 활성화
1. AWS Console 우상단 계정명 클릭 → "Billing and Cost Management"
2. "Billing preferences" 메뉴 클릭
3. "Receive CloudWatch billing alerts" 체크박스 활성화
4. "Save preferences" 클릭

### 10.2 비용 알람 생성
1. CloudWatch Console로 돌아가기
2. 리전을 "US East (N. Virginia)"로 변경 (Billing 메트릭은 us-east-1에서만 사용 가능)
3. "Create alarm" 버튼 클릭
4. "Billing" → "Total Estimated Charge" 선택
5. **Currency**: USD 선택
6. **Threshold**: Greater than `10` (10달러) 입력
7. SNS 알림 설정
8. **Alarm name**: `Monthly-Billing-Alert` 입력

**📸 스크린샷 포인트**: 비용 알람 설정 완료

---

## 정리 및 리소스 삭제

### 실습 완료 후 정리사항
1. **알람 삭제**: 불필요한 알람들 삭제하여 비용 절약
2. **대시보드 유지**: 학습용으로 대시보드는 유지 (무료)
3. **SNS 구독 해제**: 필요시 이메일 구독 해제
4. **로그 그룹 삭제**: 테스트용 로그 그룹 삭제

### 삭제 순서
1. CloudWatch Alarms 삭제
2. SNS 구독 및 토픽 삭제 (선택사항)
3. 로그 그룹 삭제 (선택사항)
4. 대시보드는 유지 권장

---

## 실습 검증 체크리스트

- [ ] EC2 메트릭을 성공적으로 확인했습니다
- [ ] 3개 위젯이 포함된 대시보드를 생성했습니다
- [ ] SNS 토픽과 이메일 구독을 설정했습니다
- [ ] CPU 사용률 알람을 생성하고 테스트했습니다
- [ ] 네트워크 트래픽 알람을 생성했습니다
- [ ] CloudWatch Logs 그룹과 스트림을 생성했습니다
- [ ] Logs Insights로 로그를 쿼리했습니다
- [ ] 이상 탐지 알람을 설정했습니다 (선택사항)
- [ ] 복합 알람을 생성했습니다 (선택사항)
- [ ] 비용 모니터링 알람을 설정했습니다

## 추가 학습 리소스

- [CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/)
- [CloudWatch Metrics and Dimensions Reference](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/aws-services-cloudwatch-metrics.html)
- [CloudWatch Logs Insights Query Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)
- [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/)

## 문제 해결

### 일반적인 문제들

**Q: 메트릭이 표시되지 않습니다**
A: EC2 인스턴스가 실행 중인지 확인하고, 메트릭 생성까지 5-10분 대기해보세요.

**Q: 알람이 트리거되지 않습니다**
A: 임계값 설정과 데이터포인트 조건을 확인하고, 충분한 시간(최소 2개 기간) 대기해보세요.

**Q: 이메일 알림을 받지 못했습니다**
A: SNS 구독이 확인되었는지, 스팸 폴더를 확인해보세요.

**Q: Logs Insights 쿼리가 실행되지 않습니다**
A: 로그 그룹에 데이터가 있는지, 시간 범위가 적절한지 확인해보세요.

이번 실습을 통해 CloudWatch의 핵심 기능들을 실제로 경험해보셨습니다. 실제 운영 환경에서는 더 정교한 임계값 설정과 알람 전략이 필요합니다.