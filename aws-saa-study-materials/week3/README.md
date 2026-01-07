# Week 3: 애플리케이션 서비스 및 배포

## 📚 주차 개요

애플리케이션의 배포, 확장, 그리고 관리를 위한 AWS 서비스들을 학습하는 세 번째 주입니다.
로드 밸런싱부터 서버리스 컴퓨팅, 컨테이너 서비스까지 현대적인 애플리케이션 아키텍처의 핵심 요소들을 다룹니다.

## 🎯 주차 학습 목표

- 고가용성 및 확장 가능한 애플리케이션 아키텍처 설계
- 서버리스 및 컨테이너 기반 애플리케이션 개발 방법 습득
- CDN과 DNS를 활용한 글로벌 서비스 구축
- CI/CD 파이프라인 및 인프라 자동화 이해

## 📅 일별 학습 계획

### [Day 15: Load Balancing 및 Auto Scaling](./day15/README.md)
**학습 시간**: 3-4시간  
**핵심 주제**:
- ELB (Elastic Load Balancer) 유형별 특징
- Application Load Balancer vs Network Load Balancer
- Auto Scaling Group 구성 및 정책
- 헬스 체크 및 장애 조치

**실습**: ALB와 Auto Scaling Group 구성

### [Day 16: CloudFront 및 CDN](./day16/README.md)
**학습 시간**: 3시간  
**핵심 주제**:
- CloudFront 배포 및 구성
- 오리진 서버 설정 (S3, EC2, ALB)
- 캐싱 정책 및 TTL 관리
- 보안 기능 (OAI, WAF 연동)

**실습**: CloudFront를 통한 정적/동적 콘텐츠 배포

### [Day 17: Route 53 및 DNS](./day17/README.md)
**학습 시간**: 3시간  
**핵심 주제**:
- DNS 기본 개념 및 레코드 유형
- Route 53 호스팅 영역 관리
- 라우팅 정책 (Simple, Weighted, Latency 등)
- 헬스 체크 및 장애 조치

**실습**: 다중 리전 장애 조치 DNS 구성

### [Day 18: API Gateway 및 Lambda](./day18/README.md)
**학습 시간**: 3-4시간  
**핵심 주제**:
- AWS Lambda 함수 개발 및 배포
- API Gateway REST/HTTP API
- 인증 및 권한 부여 (Cognito, IAM)
- 서버리스 아키텍처 패턴

**실습**: 서버리스 REST API 구축

### [Day 19: ECS, EKS, Fargate](./day19/README.md)
**학습 시간**: 4시간  
**핵심 주제**:
- 컨테이너 기본 개념 (Docker)
- ECS 클러스터 및 서비스 관리
- EKS 클러스터 구성 및 관리
- Fargate를 활용한 서버리스 컨테이너

**실습**: ECS Fargate를 활용한 컨테이너 애플리케이션 배포

### [Day 20: 배포 및 관리 도구](./day20/README.md)
**학습 시간**: 3시간  
**핵심 주제**:
- AWS CodeCommit, CodeBuild, CodeDeploy
- CodePipeline을 통한 CI/CD
- CloudFormation 템플릿 작성
- AWS CDK 소개

**실습**: CI/CD 파이프라인 구축

### [Day 21: 주간 복습 및 실습 프로젝트](./day21/README.md)
**학습 시간**: 4-5시간  
**핵심 활동**:
- 3주차 내용 종합 복습
- 실습 프로젝트: 마이크로서비스 아키텍처 구축
- 주간 퀴즈 (35문제)
- 서버리스 vs 컨테이너 비교 분석

## 📊 주차 진도 체크리스트

- [ ] Day 15: 로드 밸런싱 및 오토 스케일링 구현
- [ ] Day 16: CDN을 통한 글로벌 콘텐츠 배포
- [ ] Day 17: DNS 기반 트래픽 라우팅
- [ ] Day 18: 서버리스 API 개발
- [ ] Day 19: 컨테이너 기반 애플리케이션 배포
- [ ] Day 20: CI/CD 파이프라인 구축
- [ ] Day 21: 주간 프로젝트 완성

## 🎯 주요 학습 성과

이 주를 마치면 다음을 할 수 있게 됩니다:

1. **확장 가능한 아키텍처**: 로드 밸런서와 오토 스케일링을 활용한 탄력적 시스템 구축
2. **글로벌 서비스**: CloudFront와 Route 53을 통한 전 세계 사용자 대상 서비스 제공
3. **서버리스 개발**: Lambda와 API Gateway를 활용한 이벤트 기반 애플리케이션 개발
4. **컨테이너 오케스트레이션**: ECS/EKS를 통한 컨테이너 기반 애플리케이션 관리
5. **자동화된 배포**: CI/CD 파이프라인을 통한 안전하고 효율적인 배포 프로세스 구축

## 📚 참고 자료

### AWS 공식 문서
- [Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/)
- [CloudFront 사용 설명서](https://docs.aws.amazon.com/cloudfront/)
- [Route 53 사용 설명서](https://docs.aws.amazon.com/route53/)
- [Lambda 사용 설명서](https://docs.aws.amazon.com/lambda/)
- [ECS 사용 설명서](https://docs.aws.amazon.com/ecs/)

### 아키텍처 패턴
- [서버리스 애플리케이션 패턴](https://aws.amazon.com/serverless/)
- [마이크로서비스 아키텍처](https://aws.amazon.com/microservices/)
- [컨테이너 서비스 비교](https://aws.amazon.com/containers/)

## 💡 학습 팁

1. **아키텍처 다이어그램**: 각 서비스 간의 관계를 시각적으로 이해
2. **비용 비교**: 서버리스 vs 컨테이너 vs EC2 비용 모델 비교 분석
3. **실제 사례**: 실무에서 자주 사용되는 아키텍처 패턴 중심 학습
4. **모니터링**: 각 서비스별 핵심 메트릭 및 알람 설정 방법 학습

## 🏗️ 주요 아키텍처 패턴

### 1. 3-Tier 웹 애플리케이션
```
Internet → CloudFront → ALB → EC2 (Auto Scaling) → RDS
```

### 2. 서버리스 API
```
API Gateway → Lambda → DynamoDB
```

### 3. 마이크로서비스
```
Route 53 → CloudFront → ALB → ECS/EKS Services → RDS/DynamoDB
```

## 🔗 네비게이션

- [← Week 2: 스토리지 및 데이터베이스](../week2/README.md)
- [Week 4: 모니터링, 보안 및 최적화 →](../week4/README.md)

---

**🚀 현대적인 클라우드 애플리케이션 아키텍처의 핵심을 마스터해보세요!**