# AWS SAA-C03 Study Materials

AWS Solutions Architect Associate (SAA-C03) 시험 합격을 위한 체계적인 4주 학습 자료입니다.

## 프로젝트 정보

이 프로젝트는 **AWS Kiro**를 사용하여 생성되었습니다. Kiro의 **Spec 모드**를 활용하여 요구사항부터 설계, 구현까지 체계적으로 개발되었습니다.

### Kiro 정보
- **웹사이트**: https://kiro.dev
- **사용 모드**: Spec 모드 (Requirements → Design → Tasks)

## 원본 프롬프트

이 프로젝트는 다음 프롬프트를 기반으로 생성되었습니다:

---

AWS SAA-C03을 합격하기 위한 공부 자료를 만들고 싶습니다.

1달간의 공부로 생각하고 있으며, mermaid, svg등의 시각화자료, 학습을 하기 위한 실습용 핸즈온, 그리고 퀴즈를 추가하여 내 진도에 대한 성취도도 알고 싶습니다.

퀴즈는 일별로 작성하면 될거 같고 5문제면 될거 같습니다.

구조는 week(n)/day(n) 형태로 폴더 구성하고 각 폴더별로 readme를 추가하여 index되어 있고 내용을 빠르게 검토하길 원합니다.

대상은 대학교 막학기 컴퓨터 공학과 학생수준이며, 강의를 작성시 overview 성 내용의 경우 서술형으로 작성하여 너무 딱딱하지 않도록 해야 합니다. 핸즈온등 실습에서 프로그래밍이 필요하다면 python을 이용하도록 하겠습니다.

실행을 위한 requirement도 정확히 들어 있어야 하구요. 프로그램 형태로 구현하는 것이 아닌 task 단위로 week, day별로 나눠서 만들어보겠습니다. spec도 그렇게 구성해주시기 바랍니다.

---

## 프로젝트 구조

```
aws-saa-study-materials/
├── week1/
│   ├── day1/ (AWS 기초 및 글로벌 인프라)
│   ├── day2/ (IAM - Identity and Access Management)
│   ├── day3/ (EC2 - Elastic Compute Cloud)
│   ├── day4/ (EBS & EFS - 스토리지 서비스)
│   ├── day5/ (S3 - Simple Storage Service)
│   ├── day6/ (CloudFront & Route 53)
│   └── day7/ (주간 복습 및 실습)
├── week2/
│   ├── day8/ (VPC - Virtual Private Cloud)
│   ├── day9/ (보안 그룹 & NACL)
│   ├── day10/ (ELB - Elastic Load Balancer)
│   ├── day11/ (Auto Scaling)
│   ├── day12/ (RDS - Relational Database Service)
│   ├── day13/ (ElastiCache & DynamoDB)
│   └── day14/ (주간 복습 및 실습)
├── week3/
│   ├── day15/ (Lambda & API Gateway)
│   ├── day16/ (SQS, SNS & EventBridge)
│   ├── day17/ (CloudWatch & CloudTrail)
│   ├── day18/ (CloudFormation)
│   ├── day19/ (Elastic Beanstalk & ECS)
│   ├── day20/ (보안 서비스 심화)
│   └── day21/ (주간 복습 및 실습)
└── week4/
    ├── day22/ (고가용성 아키텍처 설계)
    ├── day23/ (비용 최적화)
    ├── day24/ (성능 최적화)
    ├── day25/ (보안 아키텍처)
    ├── day26/ (재해 복구)
    ├── day27/ (종합 실습)
    └── day28/ (최종 모의고사)
```

## 각 일차별 구성

각 day 폴더는 다음과 같은 구조로 구성됩니다:

- **README.md**: 해당 일차의 학습 목표와 개요
- **theory.md**: 이론 학습 자료 (서술형, 친근한 톤)
- **quiz.md**: 5문제 퀴즈 (진도 확인용)
- **hands-on/**: 실습 자료
  - **setup-guide.md**: 실습 환경 설정 가이드
  - **requirements.txt**: Python 패키지 의존성
  - **[service]-management.py**: 실습용 Python 스크립트
- **visuals/**: 시각화 자료
  - **[topic]-architecture.md**: Mermaid 다이어그램 포함

## 학습 방법

1. **이론 학습**: `theory.md`로 개념 학습
2. **시각화 확인**: `visuals/` 폴더의 아키텍처 다이어그램 검토
3. **실습 진행**: `hands-on/` 폴더의 가이드에 따라 실습
4. **퀴즈 풀이**: `quiz.md`로 학습 내용 점검
5. **진도 체크**: `resources/progress-tracker.md`에서 진도 관리

## 대상 학습자

- 대학교 막학기 컴퓨터공학과 학생 수준
- AWS 기초 지식이 있으면 좋지만 필수는 아님
- Python 기본 문법 이해 (실습용)

## 시작하기

1. 각 주차의 README.md부터 확인
2. Day 1부터 순차적으로 학습 진행
3. 실습 환경은 AWS Free Tier 계정 권장
4. 진도 관리는 `resources/progress-tracker.md` 활용

---

**Generated with AWS Kiro** - https://kiro.dev
