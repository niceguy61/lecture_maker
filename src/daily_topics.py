# Daily Topics Mapping (Day 1-28)
"""
28일간 일별 주제 및 AWS 서비스 매핑
각 일별 학습 주제, 주요 서비스, 기업 사례, 연계 일차 정의
"""

from typing import Dict, List, TypedDict


class DailyTopicConfig(TypedDict):
    """일별 주제 설정 타입"""
    title: str
    primary_services: List[str]
    case_study_company: str
    case_study_focus: str
    related_days: List[int]
    week: int
    difficulty: str  # 'basic', 'intermediate', 'advanced'
    estimated_hours: float


# 28일간 일별 주제 매핑
DAILY_TOPICS: Dict[int, DailyTopicConfig] = {
    # Week 1: 기초 인프라 및 컴퓨팅
    1: {
        "title": "AWS 개요 및 글로벌 인프라",
        "primary_services": ["CloudFront", "Regions", "Availability Zones", "Edge Locations"],
        "case_study_company": "Netflix",
        "case_study_focus": "글로벌 스트리밍을 위한 멀티 리전 아키텍처",
        "related_days": [16, 17],  # CloudFront(Day 16), Route 53(Day 17)
        "week": 1,
        "difficulty": "basic",
        "estimated_hours": 2.0
    },
    2: {
        "title": "IAM (Identity and Access Management)",
        "primary_services": ["IAM Users", "Groups", "Roles", "Policies", "MFA"],
        "case_study_company": "Airbnb",
        "case_study_focus": "대규모 조직의 IAM 보안 아키텍처",
        "related_days": [3, 5, 23],  # EC2(Day 3), VPC(Day 5), CloudTrail(Day 23)
        "week": 1,
        "difficulty": "basic",
        "estimated_hours": 2.5
    },
    3: {
        "title": "EC2 (Elastic Compute Cloud) 기초",
        "primary_services": ["EC2 Instances", "Instance Types", "AMI", "Security Groups"],
        "case_study_company": "Spotify",
        "case_study_focus": "음악 스트리밍을 위한 확장 가능한 컴퓨팅 인프라",
        "related_days": [4, 5, 13],  # EC2 고급(Day 4), VPC(Day 5), ELB(Day 13)
        "week": 1,
        "difficulty": "basic",
        "estimated_hours": 3.0
    },
    4: {
        "title": "EC2 고급 기능",
        "primary_services": ["Auto Scaling", "Load Balancing", "Placement Groups", "Elastic IP"],
        "case_study_company": "Uber",
        "case_study_focus": "실시간 차량 매칭을 위한 고가용성 컴퓨팅",
        "related_days": [3, 13, 14],  # EC2 기초(Day 3), ELB(Day 13), Auto Scaling(Day 14)
        "week": 1,
        "difficulty": "intermediate",
        "estimated_hours": 3.5
    },
    5: {
        "title": "VPC (Virtual Private Cloud) 기초",
        "primary_services": ["VPC", "Subnets", "Route Tables", "Internet Gateway"],
        "case_study_company": "Slack",
        "case_study_focus": "엔터프라이즈급 네트워크 격리 및 보안",
        "related_days": [6, 2, 3],  # VPC 고급(Day 6), IAM(Day 2), EC2(Day 3)
        "week": 1,
        "difficulty": "intermediate",
        "estimated_hours": 3.0
    },
    6: {
        "title": "VPC 고급 기능",
        "primary_services": ["NAT Gateway", "VPC Peering", "VPN", "Direct Connect"],
        "case_study_company": "Capital One",
        "case_study_focus": "금융 서비스를 위한 하이브리드 클라우드 네트워킹",
        "related_days": [5, 23, 24],  # VPC 기초(Day 5), CloudTrail(Day 23), Config(Day 24)
        "week": 1,
        "difficulty": "advanced",
        "estimated_hours": 4.0
    },
    7: {
        "title": "Week 1 복습 및 통합",
        "primary_services": ["All Week 1 Services"],
        "case_study_company": "Lyft",
        "case_study_focus": "Week 1 서비스 통합 아키텍처 - 승차 공유 플랫폼",
        "related_days": [1, 2, 3, 4, 5, 6],
        "week": 1,
        "difficulty": "intermediate",
        "estimated_hours": 4.0
    },
    
    # Week 2: 스토리지 및 데이터베이스
    8: {
        "title": "S3 (Simple Storage Service)",
        "primary_services": ["S3 Buckets", "Storage Classes", "Lifecycle Policies", "Versioning"],
        "case_study_company": "Dropbox",
        "case_study_focus": "페타바이트급 파일 스토리지 아키텍처",
        "related_days": [1, 16, 18],  # CloudFront(Day 1,16), Lambda(Day 18)
        "week": 2,
        "difficulty": "basic",
        "estimated_hours": 3.0
    },
    9: {
        "title": "EBS 및 EFS",
        "primary_services": ["EBS Volumes", "EBS Snapshots", "EFS", "FSx"],
        "case_study_company": "Adobe",
        "case_study_focus": "크리에이티브 클라우드를 위한 고성능 스토리지",
        "related_days": [3, 8, 10],  # EC2(Day 3), S3(Day 8), RDS(Day 10)
        "week": 2,
        "difficulty": "intermediate",
        "estimated_hours": 3.0
    },
    10: {
        "title": "RDS (Relational Database Service)",
        "primary_services": ["RDS", "Multi-AZ", "Read Replicas", "Aurora"],
        "case_study_company": "Expedia",
        "case_study_focus": "글로벌 여행 예약 시스템의 관계형 데이터베이스",
        "related_days": [11, 5, 23],  # DynamoDB(Day 11), VPC(Day 5), CloudTrail(Day 23)
        "week": 2,
        "difficulty": "intermediate",
        "estimated_hours": 3.5
    },
    11: {
        "title": "DynamoDB",
        "primary_services": ["DynamoDB", "DAX", "Global Tables", "Streams"],
        "case_study_company": "Duolingo",
        "case_study_focus": "언어 학습 앱의 NoSQL 데이터베이스 아키텍처",
        "related_days": [10, 18, 19],  # RDS(Day 10), Lambda(Day 18), API Gateway(Day 19)
        "week": 2,
        "difficulty": "intermediate",
        "estimated_hours": 3.5
    },
    12: {
        "title": "ElastiCache",
        "primary_services": ["ElastiCache", "Redis", "Memcached"],
        "case_study_company": "Tinder",
        "case_study_focus": "실시간 매칭을 위한 인메모리 캐싱 전략",
        "related_days": [10, 11, 3],  # RDS(Day 10), DynamoDB(Day 11), EC2(Day 3)
        "week": 2,
        "difficulty": "advanced",
        "estimated_hours": 3.0
    },
    13: {
        "title": "ELB (Elastic Load Balancing)",
        "primary_services": ["ALB", "NLB", "CLB", "Target Groups"],
        "case_study_company": "Pinterest",
        "case_study_focus": "이미지 공유 플랫폼의 트래픽 분산 아키텍처",
        "related_days": [3, 4, 14],  # EC2(Day 3), EC2 고급(Day 4), Auto Scaling(Day 14)
        "week": 2,
        "difficulty": "intermediate",
        "estimated_hours": 3.0
    },
    14: {
        "title": "Week 2 복습 및 통합",
        "primary_services": ["All Week 2 Services"],
        "case_study_company": "Zillow",
        "case_study_focus": "Week 2 서비스 통합 - 부동산 플랫폼 데이터 아키텍처",
        "related_days": [8, 9, 10, 11, 12, 13],
        "week": 2,
        "difficulty": "intermediate",
        "estimated_hours": 4.0
    },
    
    # Week 3: 애플리케이션 서비스 및 통합
    15: {
        "title": "SQS (Simple Queue Service)",
        "primary_services": ["SQS", "Standard Queue", "FIFO Queue", "Dead Letter Queue"],
        "case_study_company": "Robinhood",
        "case_study_focus": "금융 거래 처리를 위한 메시지 큐 아키텍처",
        "related_days": [16, 18, 19],  # SNS(Day 16), Lambda(Day 18), API Gateway(Day 19)
        "week": 3,
        "difficulty": "intermediate",
        "estimated_hours": 3.0
    },
    16: {
        "title": "SNS (Simple Notification Service) 및 CloudFront",
        "primary_services": ["SNS", "CloudFront", "Edge Locations", "Lambda@Edge"],
        "case_study_company": "Twitch",
        "case_study_focus": "실시간 스트리밍 및 알림 시스템",
        "related_days": [1, 8, 15],  # 글로벌 인프라(Day 1), S3(Day 8), SQS(Day 15)
        "week": 3,
        "difficulty": "intermediate",
        "estimated_hours": 3.5
    },
    17: {
        "title": "Route 53",
        "primary_services": ["Route 53", "DNS", "Health Checks", "Routing Policies"],
        "case_study_company": "Coursera",
        "case_study_focus": "글로벌 교육 플랫폼의 DNS 및 트래픽 라우팅",
        "related_days": [1, 13, 16],  # 글로벌 인프라(Day 1), ELB(Day 13), CloudFront(Day 16)
        "week": 3,
        "difficulty": "intermediate",
        "estimated_hours": 3.0
    },
    18: {
        "title": "Lambda (서버리스 컴퓨팅)",
        "primary_services": ["Lambda", "Lambda Layers", "Lambda@Edge", "Event Sources"],
        "case_study_company": "Coca-Cola",
        "case_study_focus": "자판기 IoT 데이터 처리를 위한 서버리스 아키텍처",
        "related_days": [11, 15, 19],  # DynamoDB(Day 11), SQS(Day 15), API Gateway(Day 19)
        "week": 3,
        "difficulty": "intermediate",
        "estimated_hours": 3.5
    },
    19: {
        "title": "API Gateway",
        "primary_services": ["API Gateway", "REST API", "WebSocket API", "API Keys"],
        "case_study_company": "Stripe",
        "case_study_focus": "결제 API 플랫폼의 게이트웨이 아키텍처",
        "related_days": [18, 2, 11],  # Lambda(Day 18), IAM(Day 2), DynamoDB(Day 11)
        "week": 3,
        "difficulty": "intermediate",
        "estimated_hours": 3.5
    },
    20: {
        "title": "Step Functions 및 EventBridge",
        "primary_services": ["Step Functions", "EventBridge", "State Machines", "Event Bus"],
        "case_study_company": "Instacart",
        "case_study_focus": "주문 처리 워크플로우 오케스트레이션",
        "related_days": [18, 15, 11],  # Lambda(Day 18), SQS(Day 15), DynamoDB(Day 11)
        "week": 3,
        "difficulty": "advanced",
        "estimated_hours": 4.0
    },
    21: {
        "title": "Week 3 복습 및 통합",
        "primary_services": ["All Week 3 Services"],
        "case_study_company": "DoorDash",
        "case_study_focus": "Week 3 서비스 통합 - 음식 배달 플랫폼 이벤트 기반 아키텍처",
        "related_days": [15, 16, 17, 18, 19, 20],
        "week": 3,
        "difficulty": "advanced",
        "estimated_hours": 4.0
    },
    
    # Week 4: 모니터링, 보안, 고급 주제
    22: {
        "title": "CloudWatch",
        "primary_services": ["CloudWatch", "Metrics", "Logs", "Alarms", "Dashboards"],
        "case_study_company": "Datadog",
        "case_study_focus": "대규모 모니터링 플랫폼의 메트릭 수집 아키텍처",
        "related_days": [3, 10, 18],  # EC2(Day 3), RDS(Day 10), Lambda(Day 18)
        "week": 4,
        "difficulty": "intermediate",
        "estimated_hours": 3.0
    },
    23: {
        "title": "CloudTrail 및 보안 서비스",
        "primary_services": ["CloudTrail", "GuardDuty", "Inspector", "Macie"],
        "case_study_company": "Goldman Sachs",
        "case_study_focus": "금융 기관의 규정 준수 및 보안 감사",
        "related_days": [2, 5, 24],  # IAM(Day 2), VPC(Day 5), Config(Day 24)
        "week": 4,
        "difficulty": "advanced",
        "estimated_hours": 3.5
    },
    24: {
        "title": "AWS Config 및 Systems Manager",
        "primary_services": ["Config", "Systems Manager", "Parameter Store", "Patch Manager"],
        "case_study_company": "GE Healthcare",
        "case_study_focus": "의료 시스템의 구성 관리 및 컴플라이언스",
        "related_days": [23, 3, 22],  # CloudTrail(Day 23), EC2(Day 3), CloudWatch(Day 22)
        "week": 4,
        "difficulty": "advanced",
        "estimated_hours": 3.5
    },
    25: {
        "title": "KMS 및 암호화",
        "primary_services": ["KMS", "CloudHSM", "Secrets Manager", "Certificate Manager"],
        "case_study_company": "Coinbase",
        "case_study_focus": "암호화폐 거래소의 데이터 암호화 전략",
        "related_days": [8, 10, 2],  # S3(Day 8), RDS(Day 10), IAM(Day 2)
        "week": 4,
        "difficulty": "advanced",
        "estimated_hours": 3.5
    },
    26: {
        "title": "엔터프라이즈 아키텍처 패턴",
        "primary_services": ["Organizations", "Control Tower", "Service Catalog", "Well-Architected"],
        "case_study_company": "Samsung Electronics",
        "case_study_focus": "대기업의 멀티 어카운트 거버넌스 전략",
        "related_days": [2, 23, 24],  # IAM(Day 2), CloudTrail(Day 23), Config(Day 24)
        "week": 4,
        "difficulty": "advanced",
        "estimated_hours": 4.0
    },
    27: {
        "title": "시험 준비 및 모의고사",
        "primary_services": ["All Services Review"],
        "case_study_company": "AWS Certified Solutions Architect",
        "case_study_focus": "실전 시험 시나리오 및 문제 해결 전략",
        "related_days": list(range(1, 27)),  # 모든 이전 일차
        "week": 4,
        "difficulty": "advanced",
        "estimated_hours": 5.0
    },
    28: {
        "title": "최종 복습 및 실전 프로젝트",
        "primary_services": ["All Services Integration"],
        "case_study_company": "Startup Best Practices",
        "case_study_focus": "스타트업을 위한 종합 AWS 아키텍처 설계",
        "related_days": list(range(1, 28)),  # 모든 이전 일차
        "week": 4,
        "difficulty": "advanced",
        "estimated_hours": 6.0
    }
}


def get_topic_by_day(day: int) -> DailyTopicConfig:
    """특정 일차의 주제 정보 반환"""
    if day not in DAILY_TOPICS:
        raise ValueError(f"Invalid day number: {day}. Must be between 1 and 28.")
    return DAILY_TOPICS[day]


def get_topics_by_week(week: int) -> Dict[int, DailyTopicConfig]:
    """특정 주차의 모든 주제 반환"""
    if week < 1 or week > 4:
        raise ValueError(f"Invalid week number: {week}. Must be between 1 and 4.")
    return {day: topic for day, topic in DAILY_TOPICS.items() if topic["week"] == week}


def get_related_topics(day: int) -> Dict[int, DailyTopicConfig]:
    """특정 일차와 연관된 주제들 반환"""
    topic = get_topic_by_day(day)
    related_days = topic["related_days"]
    return {d: DAILY_TOPICS[d] for d in related_days if d in DAILY_TOPICS}


def get_all_companies() -> List[str]:
    """모든 사례 연구 기업 목록 반환"""
    return list(set(topic["case_study_company"] for topic in DAILY_TOPICS.values()))


def get_topics_by_difficulty(difficulty: str) -> Dict[int, DailyTopicConfig]:
    """난이도별 주제 필터링"""
    if difficulty not in ["basic", "intermediate", "advanced"]:
        raise ValueError(f"Invalid difficulty: {difficulty}")
    return {day: topic for day, topic in DAILY_TOPICS.items() if topic["difficulty"] == difficulty}
