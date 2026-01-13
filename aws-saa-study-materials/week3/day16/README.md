# Day 16: CloudFront & CDN

## 📚 학습 개요
Amazon CloudFront와 CDN(Content Delivery Network)의 개념, 구성, 그리고 실제 구현 방법을 학습합니다.

## 🎯 학습 목표
- CDN의 개념과 CloudFront의 작동 원리 이해
- CloudFront Distribution 생성 및 구성 방법 학습
- Origin Access Control (OAC) 보안 설정 이해
- 캐싱 전략과 성능 최적화 기법 습득
- CloudFront 모니터링 및 문제 해결 방법 학습

## 📖 학습 자료

### 1. 이론 학습
- **파일**: [theory.md](theory.md)
- **내용**: 
  - CDN 기본 개념과 장점
  - CloudFront 핵심 구성 요소
  - 캐싱 전략 및 TTL 설정
  - 보안 기능 (OAC, Signed URL/Cookie)
  - 성능 최적화 방법
  - 모니터링 및 로깅
- **소요 시간**: 약 30-40분

### 2. 실습 활동
- **파일**: [hands-on/setup-guide.md](hands-on/setup-guide.md)
- **내용**:
  - S3 정적 웹사이트 설정
  - CloudFront Distribution 생성
  - Origin Access Control 구성
  - 캐시 동작 확인 및 무효화 테스트
  - 성능 최적화 설정
- **소요 시간**: 약 45-60분

### 3. 퀴즈
- **파일**: [quiz.md](quiz.md)
- **내용**: CloudFront 핵심 개념 확인 (5문제)
- **소요 시간**: 약 10-15분

## 🗓️ 학습 일정
| 시간 | 활동 | 내용 |
|------|------|------|
| 30분 | 이론 학습 | CDN과 CloudFront 개념 학습 |
| 60분 | 실습 | CloudFront Distribution 구축 |
| 15분 | 퀴즈 | 학습 내용 확인 |
| 15분 | 복습 | 핵심 개념 정리 |

## 🔑 핵심 개념

### CDN (Content Delivery Network)
- 전 세계 분산 서버를 통한 콘텐츠 가속화
- Edge Location에서 사용자와 가까운 위치에서 서비스 제공
- 성능 향상, 가용성 증대, 대역폭 절약

### CloudFront 주요 구성 요소
- **Distribution**: 콘텐츠 배포 단위
- **Origin**: 원본 콘텐츠 소스 (S3, ALB, EC2 등)
- **Edge Location**: 캐시 서버 (400+ 글로벌 위치)
- **Cache Behavior**: 캐싱 규칙 및 정책

### 보안 기능
- **Origin Access Control (OAC)**: S3 직접 접근 차단
- **Signed URL/Cookie**: 프리미엄 콘텐츠 접근 제어
- **AWS WAF 통합**: 웹 애플리케이션 방화벽
- **지리적 제한**: 국가별 접근 제어

## 🛠️ 실습 환경
- **AWS 서비스**: CloudFront, S3
- **필요 권한**: CloudFront, S3 관리 권한
- **예상 비용**: AWS Free Tier 범위 내 (거의 무료)
- **정리 필요**: 실습 후 리소스 삭제 권장

## 📋 체크리스트

### 이론 학습 완료
- [ ] CDN 개념과 장점 이해
- [ ] CloudFront 구성 요소 파악
- [ ] 캐싱 전략 및 TTL 이해
- [ ] 보안 기능 (OAC, Signed URL) 학습
- [ ] 성능 최적화 방법 학습

### 실습 완료
- [ ] S3 버킷 생성 및 정적 웹사이트 설정
- [ ] CloudFront Distribution 생성
- [ ] Origin Access Control 설정
- [ ] 캐시 동작 확인 (Hit/Miss)
- [ ] 캐시 무효화 테스트
- [ ] 압축 및 HTTPS 설정 확인

### 퀴즈 완료
- [ ] 5문제 퀴즈 완료
- [ ] 틀린 문제 복습
- [ ] 핵심 개념 재정리

## 🔗 연관 학습 주제

### 이전 학습 (Day 15)
- Load Balancing & Auto Scaling
- Application Load Balancer 설정

### 다음 학습 (Day 17)
- Route 53 & DNS
- 도메인 관리 및 라우팅 정책

### 관련 서비스
- **S3**: Origin 서버로 활용
- **Route 53**: 도메인 및 DNS 관리
- **AWS WAF**: 웹 애플리케이션 보안
- **Certificate Manager**: SSL/TLS 인증서

## 💡 학습 팁

### 효과적인 학습 방법
1. **이론 먼저**: CDN 개념을 확실히 이해한 후 실습 진행
2. **단계별 실습**: 각 단계를 차근차근 따라하며 결과 확인
3. **캐시 동작 관찰**: 개발자 도구로 캐시 Hit/Miss 확인
4. **보안 설정 중요**: OAC 설정으로 S3 보안 강화

### 주의사항
- CloudFront Distribution 배포에 5-15분 소요
- 캐시 무효화는 비용 발생 (월 1,000건까지 무료)
- 실습 후 리소스 삭제로 비용 절약
- HTTPS 설정 시 인증서 확인 필요

## 🎯 학습 성과 측정

### 이해도 확인
- CDN과 CloudFront의 차이점 설명 가능
- Edge Location의 역할과 캐싱 원리 이해
- OAC와 Signed URL의 보안 기능 구분
- 캐시 무효화와 TTL 설정 방법 숙지

### 실무 적용 능력
- 정적 웹사이트 CDN 구축 가능
- CloudFront 보안 설정 구성 가능
- 성능 최적화 설정 적용 가능
- 모니터링 및 문제 해결 수행 가능

---

## 📞 도움이 필요한 경우

### 일반적인 문제
- **403 Forbidden**: S3 버킷 정책 및 OAC 설정 확인
- **캐시 미적용**: TTL 설정 및 캐시 정책 검토
- **느린 성능**: 압축 설정 및 Price Class 확인

### 추가 학습 자료
- [AWS CloudFront 공식 문서](https://docs.aws.amazon.com/cloudfront/)
- [CloudFront 모범 사례](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/best-practices.html)
- [CDN 성능 최적화 가이드](https://aws.amazon.com/cloudfront/getting-started/)

**화이팅! 오늘도 AWS 전문가로 한 걸음 더 나아가세요! 🚀**