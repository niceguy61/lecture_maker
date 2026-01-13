# 추가 학습 자료 및 리소스

## 📚 영역별 집중 학습 자료

### 1. AWS 기초 및 글로벌 인프라

#### 핵심 개념 복습
- **리전과 가용 영역**: 물리적 위치와 네트워크 연결성 이해
- **엣지 로케이션**: CloudFront와 Route 53 서비스 제공
- **공동 책임 모델**: AWS vs 고객 책임 영역 명확히 구분

#### 추천 학습 자료
- [AWS 글로벌 인프라 개요](https://aws.amazon.com/about-aws/global-infrastructure/)
- [AWS 공동 책임 모델 상세 가이드](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [Well-Architected Framework 백서](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

#### 실습 권장사항
- AWS 콘솔에서 다양한 리전의 서비스 가용성 확인
- 계정 설정 및 결제 대시보드 탐색
- Support 케이스 생성 및 Service Health Dashboard 확인

---

### 2. IAM 및 보안

#### 핵심 개념 복습
- **IAM 정책 평가 순서**: 기본 거부 → 명시적 허용 → 명시적 거부
- **역할 vs 사용자**: 임시 vs 영구 자격 증명
- **Cross-Account Access**: 역할 기반 접근 방식

#### 추천 학습 자료
- [IAM 모범 사례](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [IAM 정책 평가 로직](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [AWS 보안 백서](https://docs.aws.amazon.com/whitepapers/latest/aws-security-best-practices/aws-security-best-practices.html)

#### 실습 권장사항
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        }
      }
    }
  ]
}
```
- 다양한 조건을 포함한 IAM 정책 작성 연습
- Cross-Account 역할 생성 및 테스트
- MFA 설정 및 임시 자격 증명 사용

---

### 3. EC2 및 컴퓨팅

#### 핵심 개념 복습
- **인스턴스 타입**: 범용, 컴퓨팅 최적화, 메모리 최적화, 스토리지 최적화
- **구매 옵션**: 온디맨드, 예약, 스팟, 전용 호스트
- **Auto Scaling**: 동적 스케일링 vs 예측 스케일링

#### 추천 학습 자료
- [EC2 인스턴스 타입 가이드](https://aws.amazon.com/ec2/instance-types/)
- [Auto Scaling 모범 사례](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-benefits.html)
- [Lambda 개발자 가이드](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)

#### 실습 시나리오
1. **웹 서버 Auto Scaling 구성**
   - Launch Template 생성
   - Auto Scaling Group 설정
   - CloudWatch 알람 기반 스케일링 정책

2. **Lambda 함수 최적화**
   - 메모리 및 타임아웃 설정 최적화
   - 환경 변수 및 레이어 활용
   - VPC 내 Lambda 함수 구성

---

### 4. 스토리지

#### 핵심 개념 복습
- **S3 스토리지 클래스**: 액세스 패턴에 따른 선택
- **EBS 볼륨 타입**: 성능 요구사항에 따른 선택
- **백업 전략**: 스냅샷, 복제, 아카이빙

#### 추천 학습 자료
- [S3 스토리지 클래스 비교](https://aws.amazon.com/s3/storage-classes/)
- [EBS 성능 최적화 가이드](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-optimized.html)
- [데이터 아카이빙 전략](https://aws.amazon.com/getting-started/hands-on/backup-to-s3-cli/)

#### 비용 최적화 팁
```bash
# S3 Lifecycle 정책 예시
{
  "Rules": [
    {
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    }
  ]
}
```

---

### 5. 네트워킹

#### 핵심 개념 복습
- **VPC 구성 요소**: 서브넷, 라우팅 테이블, 게이트웨이
- **보안 계층**: 보안 그룹, NACL, WAF
- **연결 옵션**: VPC Peering, Transit Gateway, Direct Connect

#### 추천 학습 자료
- [VPC 사용자 가이드](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [네트워크 보안 모범 사례](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/introduction.html)
- [하이브리드 네트워킹 옵션](https://aws.amazon.com/hybrid/)

#### 네트워크 설계 패턴
1. **3-Tier 아키텍처**
   - Public Subnet: Load Balancer
   - Private Subnet: Application Servers
   - Database Subnet: RDS

2. **Hub-and-Spoke 모델**
   - Transit Gateway 중심
   - 여러 VPC 연결
   - 중앙집중식 라우팅

---

### 6. 데이터베이스

#### 핵심 개념 복습
- **관계형 vs NoSQL**: 사용 사례에 따른 선택
- **고가용성 옵션**: Multi-AZ, Read Replica, 클러스터링
- **성능 최적화**: 인덱싱, 캐싱, 파티셔닝

#### 추천 학습 자료
- [RDS 모범 사례](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)
- [DynamoDB 설계 패턴](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [데이터베이스 마이그레이션 가이드](https://aws.amazon.com/dms/)

#### 성능 튜닝 체크리스트
- [ ] 적절한 인스턴스 타입 선택
- [ ] 스토리지 타입 최적화 (gp2 vs gp3 vs io1)
- [ ] 읽기 전용 복제본 활용
- [ ] 연결 풀링 구현
- [ ] 쿼리 최적화 및 인덱스 튜닝

---

### 7. 모니터링 및 관리

#### 핵심 개념 복습
- **CloudWatch**: 메트릭, 로그, 알람, 대시보드
- **CloudTrail**: API 호출 감사 및 규정 준수
- **Config**: 리소스 구성 변경 추적

#### 추천 학습 자료
- [CloudWatch 사용자 가이드](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/)
- [운영 모범 사례](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)
- [비용 최적화 전략](https://aws.amazon.com/aws-cost-management/)

#### 모니터링 설정 예시
```python
# CloudWatch 사용자 지정 메트릭 전송
import boto3

cloudwatch = boto3.client('cloudwatch')

cloudwatch.put_metric_data(
    Namespace='MyApp/Performance',
    MetricData=[
        {
            'MetricName': 'ResponseTime',
            'Value': 0.5,
            'Unit': 'Seconds',
            'Dimensions': [
                {
                    'Name': 'Environment',
                    'Value': 'Production'
                }
            ]
        }
    ]
)
```

---

## 🎯 시험 전 마지막 점검 사항

### 1. 서비스별 핵심 포인트 암기
- **EC2**: 인스턴스 타입, 구매 옵션, 배치 그룹
- **S3**: 스토리지 클래스, 일관성 모델, 보안 기능
- **VPC**: CIDR, 라우팅, 보안 그룹 vs NACL
- **RDS**: Multi-AZ vs Read Replica, 백업 옵션
- **IAM**: 정책 평가, 역할 vs 사용자, 조건

### 2. 아키텍처 패턴 이해
- **고가용성**: Multi-AZ, Auto Scaling, Load Balancing
- **확장성**: 수평/수직 스케일링, 캐싱, CDN
- **보안**: 심층 방어, 최소 권한 원칙, 암호화
- **비용 최적화**: 예약 인스턴스, 스팟 인스턴스, 라이프사이클 정책

### 3. 문제 해결 접근법
1. **요구사항 분석**: 성능, 가용성, 보안, 비용
2. **제약사항 확인**: 기술적, 비즈니스적 제약
3. **옵션 비교**: 각 선택지의 장단점 분석
4. **최적 솔루션 선택**: 요구사항에 가장 적합한 옵션

### 4. 자주 틀리는 함정 문제
- **"가장 비용 효율적인" vs "가장 성능이 좋은"**: 요구사항 정확히 파악
- **"즉시" vs "최종적으로"**: 일관성 모델 이해
- **"고가용성" vs "재해 복구"**: RTO/RPO 요구사항 구분
- **"모니터링" vs "로깅"**: CloudWatch vs CloudTrail 역할 구분

---

## 📖 추가 참고 자료

### AWS 공식 문서
- [AWS 아키텍처 센터](https://aws.amazon.com/architecture/)
- [AWS 솔루션 라이브러리](https://aws.amazon.com/solutions/)
- [AWS 백서 모음](https://aws.amazon.com/whitepapers/)

### 실습 환경
- [AWS 실습 랩](https://aws.amazon.com/training/hands-on-labs/)
- [AWS 워크샵](https://workshops.aws/)
- [Qwiklabs AWS 실습](https://www.qwiklabs.com/catalog?keywords=aws)

### 커뮤니티 자료
- [AWS re:Invent 세션](https://reinvent.awsevents.com/)
- [AWS 블로그](https://aws.amazon.com/blogs/)
- [AWS 포럼](https://forums.aws.amazon.com/)

### 시험 준비 도구
- [AWS 공식 샘플 문제](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Sample-Questions.pdf)
- [AWS 시험 가이드](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf)

이 자료들을 활용하여 취약한 영역을 집중적으로 보완하고 실제 시험에서 좋은 결과를 얻으시기 바랍니다!