# Day 26 퀴즈: 종합 실습 프로젝트 및 엔터프라이즈 아키텍처

## 📚 학습 목표 확인
- 엔터프라이즈급 3-tier 아키텍처 설계 원리 이해
- AWS Well-Architected Framework 5개 기둥 적용
- 복합적인 AWS 서비스 통합 및 최적화 전략
- 실제 운영 환경에서의 모범 사례 적용
- 아키텍처 패턴별 적절한 사용 사례 판단

---

## 문제 1: 엔터프라이즈 3-Tier 아키텍처 설계

**시나리오:** 
글로벌 전자상거래 회사가 AWS에서 새로운 웹 애플리케이션을 구축하려고 합니다. 다음 요구사항을 만족해야 합니다:
- 99.9% 가용성 보장
- 전 세계 사용자에게 빠른 응답 시간 제공
- 트래픽 급증 시 자동 확장
- 보안 모범 사례 적용

**질문:** 이 요구사항을 만족하는 3-tier 아키텍처에서 **반드시 포함되어야 하는** 구성 요소는?

A) CloudFront + ALB + EC2 Auto Scaling + RDS Single-AZ  
B) Route 53 + CloudFront + ALB + EC2 Auto Scaling + RDS Multi-AZ  
C) API Gateway + Lambda + DynamoDB + S3  
D) ELB Classic + EC2 + RDS + ElastiCache

**정답:** B) Route 53 + CloudFront + ALB + EC2 Auto Scaling + RDS Multi-AZ

**해설:**
엔터프라이즈급 3-tier 아키텍처에서 99.9% 가용성과 글로벌 성능을 보장하려면:

- **Route 53**: DNS 서비스로 글로벌 트래픽 라우팅 및 Health Check
- **CloudFront**: CDN으로 전 세계 사용자에게 빠른 콘텐츠 전송
- **ALB**: Application Load Balancer로 고급 라우팅 및 SSL 종료
- **EC2 Auto Scaling**: 트래픽 변화에 따른 자동 확장/축소
- **RDS Multi-AZ**: 데이터베이스 고가용성 보장

A는 RDS Single-AZ로 고가용성 미보장, C는 서버리스 아키텍처로 3-tier와 다름, D는 구식 ELB Classic 사용으로 부적절합니다.

---

## 문제 2: 마이크로서비스 아키텍처 통신 패턴

**시나리오:**
온라인 쇼핑몰을 마이크로서비스 아키텍처로 구축하고 있습니다. 다음 서비스들이 있습니다:
- User Service (사용자 관리)
- Product Service (상품 관리)  
- Order Service (주문 처리)
- Payment Service (결제 처리)
- Notification Service (알림 발송)

주문 완료 시 결제 처리와 알림 발송이 **비동기적으로** 처리되어야 합니다.

**질문:** 이 요구사항을 만족하는 **가장 적절한** 통신 패턴은?

A) Order Service → API Gateway → Payment Service → Notification Service  
B) Order Service → SQS → Payment Service → SNS → Notification Service  
C) Order Service → EventBridge → Payment Service & Notification Service  
D) Order Service → Step Functions → Payment Service → Notification Service

**정답:** C) Order Service → EventBridge → Payment Service & Notification Service

**해설:**
마이크로서비스에서 비동기 통신을 위한 최적의 패턴:

**EventBridge의 장점:**
- **이벤트 기반 아키텍처**: 서비스 간 느슨한 결합
- **다중 대상**: 하나의 이벤트로 여러 서비스에 동시 전달
- **라우팅 규칙**: 이벤트 내용에 따른 조건부 라우팅
- **재시도 및 DLQ**: 내장된 오류 처리 메커니즘

A는 동기식 통신, B는 순차적 처리로 병렬 처리 불가, D는 Step Functions로 워크플로우 관리에 적합하지만 단순 이벤트 전파에는 과도합니다.

---

## 문제 3: 데이터 레이크 아키텍처 최적화

**시나리오:**
대형 제조업체가 IoT 센서, 생산 데이터베이스, 로그 파일 등 다양한 소스의 데이터를 수집하여 분석하려고 합니다. 데이터 양은 일일 10TB이며, 실시간 분석과 배치 분석이 모두 필요합니다.

**질문:** 이 요구사항에 **가장 적합한** 데이터 레이크 아키텍처는?

A) Kinesis Data Streams → Lambda → RDS → QuickSight  
B) Kinesis Data Firehose → S3 → Glue ETL → Athena → QuickSight  
C) Direct Connect → Redshift → Tableau  
D) API Gateway → Lambda → DynamoDB → ElasticSearch

**정답:** B) Kinesis Data Firehose → S3 → Glue ETL → Athena → QuickSight

**해설:**
대용량 데이터 레이크 아키텍처의 핵심 구성:

**데이터 수집 계층:**
- **Kinesis Data Firehose**: 스트리밍 데이터를 S3로 자동 전송, 압축 및 형식 변환

**저장 계층:**
- **S3**: 페타바이트급 확장 가능한 데이터 레이크 스토리지

**처리 계층:**
- **Glue ETL**: 서버리스 데이터 변환 및 카탈로그 관리

**분석 계층:**
- **Athena**: S3 데이터에 대한 서버리스 SQL 쿼리
- **QuickSight**: 비즈니스 인텔리전스 및 시각화

A는 RDS로 대용량 데이터 처리 부적합, C는 Redshift 단독으로 데이터 레이크 패턴 아님, D는 실시간 검색에 특화되어 배치 분석에 부적합합니다.

---

## 문제 4: 하이브리드 클라우드 연결성 최적화

**시나리오:**
금융 회사가 규정 준수를 위해 민감한 데이터는 온프레미스에 보관하고, 웹 애플리케이션은 AWS에서 운영하려고 합니다. 다음 요구사항이 있습니다:
- 온프레미스-AWS 간 안정적이고 빠른 연결 (최소 1Gbps)
- 백업 연결 방식 필요
- 월 데이터 전송량: 500GB
- 지연시간 최소화 필요

**질문:** 이 요구사항에 **가장 비용 효율적이면서 안정적인** 연결 방식은?

A) Direct Connect (1Gbps) + Site-to-Site VPN (백업)  
B) Site-to-Site VPN (Primary) + Direct Connect (백업)  
C) Direct Connect (10Gbps) 단독  
D) 인터넷 기반 VPN 터널 2개

**정답:** A) Direct Connect (1Gbps) + Site-to-Site VPN (백업)

**해설:**
하이브리드 클라우드 연결성 최적화 전략:

**Primary: Direct Connect (1Gbps)**
- **안정적인 성능**: 전용 네트워크 연결로 일관된 대역폭과 낮은 지연시간
- **비용 효율성**: 500GB/월 전송량에 적합한 1Gbps 용량
- **보안**: 인터넷을 거치지 않는 프라이빗 연결

**Backup: Site-to-Site VPN**
- **고가용성**: Direct Connect 장애 시 자동 페일오버
- **비용 효율성**: 백업용으로 저렴한 VPN 연결
- **빠른 구축**: Direct Connect 구축 기간 동안 임시 연결로도 활용

B는 VPN을 Primary로 사용하여 성능 저하, C는 10Gbps로 과도한 용량과 비용, D는 안정성과 성능 부족합니다.

---

## 문제 5: 서버리스 아키텍처 비용 최적화

**시나리오:**
스타트업이 서버리스 아키텍처로 모바일 앱 백엔드를 구축했습니다. 현재 구성:
- API Gateway + Lambda (Node.js, 512MB, 평균 실행시간 2초)
- DynamoDB (On-Demand)
- S3 (이미지 저장)
- 월 요청 수: 100만 건
- 평균 응답 크기: 50KB

비용을 30% 절감하면서 성능을 유지해야 합니다.

**질문:** **가장 효과적인** 비용 최적화 전략은?

A) Lambda 메모리를 256MB로 줄이고 DynamoDB를 Provisioned로 변경  
B) Lambda 메모리를 1024MB로 늘리고 CloudFront 추가  
C) API Gateway를 ALB로 교체하고 Lambda를 EC2로 변경  
D) Lambda를 Python으로 변경하고 S3 Intelligent Tiering 적용

**정답:** B) Lambda 메모리를 1024MB로 늘리고 CloudFront 추가

**해설:**
서버리스 비용 최적화의 핵심 전략:

**Lambda 메모리 최적화 (512MB → 1024MB):**
- **실행 시간 단축**: 더 많은 CPU로 2초 → 1초로 단축 가능
- **비용 계산**: 메모리 2배 증가하지만 실행시간 50% 단축으로 총 비용 동일하거나 감소
- **성능 향상**: 응답 시간 개선으로 사용자 경험 향상

**CloudFront 추가:**
- **API 캐싱**: 반복적인 GET 요청을 엣지에서 처리
- **데이터 전송 비용 절감**: API Gateway 데이터 전송 비용 대비 CloudFront가 저렴
- **글로벌 성능**: 전 세계 사용자에게 빠른 응답

A는 메모리 감소로 실행시간 증가하여 비용 증가, C는 서버리스 장점 포기, D는 런타임 변경으로 개발 비용 증가하며 효과 제한적입니다.

---

## 🎯 퀴즈 완료!

### 점수 계산
- 5문제 정답: 🏆 **완벽! 엔터프라이즈 아키텍처 전문가**
- 4문제 정답: 🥇 **우수! 실무 적용 가능 수준**  
- 3문제 정답: 🥈 **양호! 추가 학습 권장**
- 2문제 이하: 🥉 **기초 복습 필요**

### 추가 학습 권장사항

**문제 1 관련 (3-Tier 아키텍처):**
- AWS Well-Architected Framework 5개 기둥 심화 학습
- Multi-AZ vs Single-AZ 비용 대비 효과 분석
- CloudFront 캐싱 전략 및 최적화 방법

**문제 2 관련 (마이크로서비스):**
- EventBridge vs SQS/SNS 사용 사례별 비교
- 마이크로서비스 간 데이터 일관성 패턴
- Circuit Breaker 패턴 및 장애 격리 전략

**문제 3 관련 (데이터 레이크):**
- S3 스토리지 클래스별 비용 최적화
- Glue vs EMR vs Athena 사용 사례 비교
- 데이터 거버넌스 및 보안 모범 사례

**문제 4 관련 (하이브리드 클라우드):**
- Direct Connect vs VPN 성능 및 비용 비교
- Transit Gateway를 활용한 네트워크 허브 설계
- 하이브리드 환경에서의 보안 모범 사례

**문제 5 관련 (서버리스 최적화):**
- Lambda 메모리 vs 실행시간 최적화 전략
- API Gateway 캐싱 vs CloudFront 캐싱 비교
- 서버리스 모니터링 및 비용 추적 방법

### 다음 단계
- **Day 27**: 모의고사 65문제로 최종 점검
- **Day 28**: 시험 전략 및 마지막 복습
- **실제 시험**: SAA-C03 자신감 있게 도전!

오늘의 종합 실습과 퀴즈를 통해 엔터프라이즈급 AWS 아키텍처 설계 능력을 크게 향상시키셨습니다. 내일은 실제 시험과 동일한 형태의 모의고사로 최종 점검을 진행하겠습니다! 🚀