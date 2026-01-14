# 스타트업 사례 기반 심화 강의 시스템

AWS SAA 스터디 자료에 실제 기업 사례 기반 심화 강의를 추가하는 콘텐츠 생성 시스템입니다.

## 프로젝트 구조

```
.
├── src/                          # 소스 코드
│   ├── __init__.py
│   ├── config.py                 # 설정 및 상수
│   ├── daily_topics.py           # 28일간 일별 주제 매핑
│   └── models.py                 # 핵심 데이터 모델
├── templates/                    # 콘텐츠 템플릿
├── tests/                        # 테스트 코드
│   ├── __init__.py
│   └── conftest.py              # pytest 설정
├── requirements.txt              # Python 의존성
└── README.md                     # 프로젝트 문서

```

## 주요 기능

### 1. 일별 주제 매핑 (Day 1-28)
- 각 일별 학습 주제와 주요 AWS 서비스 정의
- 실제 기업 사례 매칭
- 서비스 간 연계 정보 관리

### 2. 콘텐츠 생성
- **Case Study**: 실제 기업의 AWS 활용 사례
- **Best Practices**: 서비스 연계 및 아키텍처 진화
- **Troubleshooting**: 실제 운영 환경 문제 해결
- **Hands-On**: AWS Console 기반 실습 가이드
- **Mermaid Diagrams**: 아키텍처 시각화

### 3. 데이터 모델
- `CaseStudyContent`: 사례 연구 콘텐츠
- `BestPracticesContent`: 베스트 프랙티스
- `TroubleshootingContent`: 트러블슈팅 시나리오
- `HandsOnContent`: 실습 콘텐츠

## 설치

```bash
# 의존성 설치
pip install -r requirements.txt
```

## 일별 주제 구성

### Week 1: 기초 인프라 및 컴퓨팅
- Day 1: AWS 개요 및 글로벌 인프라 (Netflix)
- Day 2: IAM (Airbnb)
- Day 3: EC2 기초 (Spotify)
- Day 4: EC2 고급 (Uber)
- Day 5: VPC 기초 (Slack)
- Day 6: VPC 고급 (Capital One)
- Day 7: Week 1 복습 (Lyft)

### Week 2: 스토리지 및 데이터베이스
- Day 8: S3 (Dropbox)
- Day 9: EBS/EFS (Adobe)
- Day 10: RDS (Expedia)
- Day 11: DynamoDB (Duolingo)
- Day 12: ElastiCache (Tinder)
- Day 13: ELB (Pinterest)
- Day 14: Week 2 복습 (Zillow)

### Week 3: 애플리케이션 서비스
- Day 15: SQS (Robinhood)
- Day 16: SNS/CloudFront (Twitch)
- Day 17: Route 53 (Coursera)
- Day 18: Lambda (Coca-Cola)
- Day 19: API Gateway (Stripe)
- Day 20: Step Functions (Instacart)
- Day 21: Week 3 복습 (DoorDash)

### Week 4: 모니터링 및 보안
- Day 22: CloudWatch (Datadog)
- Day 23: CloudTrail (Goldman Sachs)
- Day 24: Config/Systems Manager (GE Healthcare)
- Day 25: KMS/암호화 (Coinbase)
- Day 26: 엔터프라이즈 패턴 (Samsung)
- Day 27: 시험 준비
- Day 28: 최종 복습

## 사용 예시

```python
from src.daily_topics import get_topic_by_day, get_related_topics

# Day 1 주제 정보 가져오기
day1_topic = get_topic_by_day(1)
print(f"Title: {day1_topic['title']}")
print(f"Company: {day1_topic['case_study_company']}")
print(f"Services: {day1_topic['primary_services']}")

# 연관된 주제들 가져오기
related = get_related_topics(1)
for day, topic in related.items():
    print(f"Day {day}: {topic['title']}")
```

## 개발 가이드

### 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 커버리지 포함
pytest --cov=src

# 특정 테스트 파일 실행
pytest tests/test_daily_topics.py
```

### 코드 품질

```bash
# 코드 포맷팅
black src/ tests/

# 린팅
flake8 src/ tests/

# 타입 체크
mypy src/
```

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 기여

이슈 및 풀 리퀘스트를 환영합니다.
