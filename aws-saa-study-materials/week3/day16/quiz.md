# Day 16 퀴즈: CloudFront & CDN

## 퀴즈 개요
- **주제**: Amazon CloudFront와 CDN (Content Delivery Network)
- **문제 수**: 5문제
- **예상 소요 시간**: 10-15분
- **난이도**: 중급

---

## 문제 1: CloudFront 기본 개념

**문제**: Amazon CloudFront의 Edge Location에 대한 설명으로 가장 적절한 것은?

A) AWS 리전 내에서만 운영되는 캐시 서버  
B) 사용자와 가장 가까운 위치에서 콘텐츠를 캐시하고 제공하는 서버  
C) Origin 서버와 동일한 위치에 있는 백업 서버  
D) CloudFront Distribution을 관리하는 중앙 서버  

**정답**: B

**해설**: 
Edge Location은 사용자와 가장 가까운 지리적 위치에 배치된 캐시 서버로, 콘텐츠를 캐시하여 사용자에게 빠르게 제공하는 역할을 합니다. AWS는 전 세계 400개 이상의 Edge Location을 운영하고 있으며, 이는 AWS 리전보다 훨씬 많은 수입니다. Edge Location은 사용자의 요청에 대해 캐시된 콘텐츠가 있으면 즉시 제공하고, 없으면 Origin 서버에서 콘텐츠를 가져와 캐시한 후 사용자에게 제공합니다.

---

## 문제 2: Origin Access Control (OAC)

**문제**: S3 버킷을 CloudFront의 Origin으로 사용할 때 Origin Access Control (OAC)을 설정하는 주된 목적은?

A) CloudFront의 캐시 성능을 향상시키기 위해  
B) S3 버킷에 대한 직접 접근을 차단하고 CloudFront를 통해서만 접근하도록 제한하기 위해  
C) S3 버킷의 스토리지 비용을 절약하기 위해  
D) CloudFront Distribution의 배포 속도를 높이기 위해  

**정답**: B

**해설**: 
Origin Access Control (OAC)은 S3 버킷에 대한 보안을 강화하는 기능입니다. OAC를 설정하면 S3 버킷에 대한 직접 접근을 차단하고, 오직 CloudFront를 통해서만 콘텐츠에 접근할 수 있도록 제한합니다. 이를 통해 콘텐츠의 무단 접근을 방지하고, 모든 요청이 CloudFront를 거치도록 하여 캐싱의 이점을 최대화할 수 있습니다. OAC는 이전의 Origin Access Identity (OAI)를 대체하는 더 안전하고 기능이 향상된 방식입니다.

---

## 문제 3: 캐시 동작 및 TTL

**문제**: CloudFront에서 캐시된 콘텐츠를 강제로 삭제하여 Origin에서 새로운 콘텐츠를 가져오도록 하는 기능은?

A) Cache Refresh  
B) Content Update  
C) Cache Invalidation  
D) Origin Sync  

**정답**: C

**해설**: 
Cache Invalidation(캐시 무효화)은 CloudFront Edge Location에 캐시된 콘텐츠를 강제로 삭제하는 기능입니다. 이를 통해 Origin 서버의 콘텐츠가 업데이트되었을 때, TTL이 만료되기 전에도 사용자가 최신 콘텐츠를 받을 수 있도록 할 수 있습니다. 무효화는 특정 파일(`/images/logo.png`), 와일드카드(`/images/*`), 또는 전체 콘텐츠(`/*`)에 대해 수행할 수 있습니다. 단, 무효화 요청은 비용이 발생하므로(월 1,000건까지 무료) 신중하게 사용해야 합니다.

---

## 문제 4: CloudFront 보안 기능

**문제**: 다음 중 CloudFront에서 프리미엄 콘텐츠에 대한 접근을 제어하는 데 사용되는 기능은?

A) AWS WAF Rules  
B) Signed URLs and Signed Cookies  
C) Security Groups  
D) Network ACLs  

**정답**: B

**해설**: 
Signed URLs와 Signed Cookies는 CloudFront에서 프리미엄 콘텐츠나 제한된 콘텐츠에 대한 접근을 제어하는 기능입니다. Signed URL은 개별 파일에 대한 시간 제한 접근을 제공하며, 주로 다운로드 링크나 개별 비디오 파일에 사용됩니다. Signed Cookie는 여러 파일이나 웹사이트 전체에 대한 접근을 제어할 때 사용되며, 사용자 세션 관리에 적합합니다. 이 기능들을 통해 인증된 사용자만 특정 콘텐츠에 접근할 수 있도록 제한할 수 있습니다.

---

## 문제 5: CloudFront 성능 최적화

**시나리오**: 
글로벌 e-commerce 웹사이트를 운영하는 회사에서 다음과 같은 요구사항이 있습니다:
- 전 세계 사용자에게 빠른 페이지 로딩 제공
- 텍스트 기반 파일(HTML, CSS, JS)의 전송 속도 향상
- 특정 국가에서의 접근 차단
- HTTPS 사용 강제

**문제**: 위 요구사항을 모두 만족하기 위한 CloudFront 설정으로 가장 적절한 조합은?

A) Price Class 100 + 압축 비활성화 + Geo Restriction 설정 + HTTP 허용  
B) Price Class All + 압축 활성화 + Geo Restriction 설정 + Redirect HTTP to HTTPS  
C) Price Class 200 + 압축 비활성화 + WAF 설정 + HTTPS Only  
D) Price Class All + 압축 활성화 + Security Groups + HTTP/HTTPS 모두 허용  

**정답**: B

**해설**: 
글로벌 서비스를 위해서는 Price Class All을 사용하여 전 세계 모든 Edge Location을 활용해야 최고의 성능을 제공할 수 있습니다. 텍스트 기반 파일의 전송 속도 향상을 위해서는 압축(Compression)을 활성화해야 합니다. 특정 국가 접근 차단을 위해서는 Geo Restriction 기능을 사용하고, HTTPS 사용 강제를 위해서는 "Redirect HTTP to HTTPS" 정책을 설정해야 합니다. 

- Price Class All: 전 세계 최적 성능
- 압축 활성화: HTML, CSS, JS 파일 크기 감소로 전송 속도 향상
- Geo Restriction: 국가별 접근 제어
- Redirect HTTP to HTTPS: 모든 HTTP 요청을 HTTPS로 자동 리디렉션

---

## 퀴즈 결과 분석

### 점수별 평가
- **5점 (100%)**: 우수! CloudFront의 핵심 개념과 기능을 완벽히 이해하고 있습니다.
- **4점 (80%)**: 양호! 대부분의 개념을 이해하고 있으나, 일부 세부사항을 복습해보세요.
- **3점 (60%)**: 보통! 기본 개념은 이해하고 있으나, 실습과 추가 학습이 필요합니다.
- **2점 이하 (40% 이하)**: 복습 필요! 이론 내용을 다시 학습하고 실습을 진행해보세요.

### 주요 학습 포인트
1. **Edge Location의 역할**: 사용자와 가까운 위치에서 콘텐츠 캐싱
2. **OAC의 보안 기능**: S3 직접 접근 차단 및 CloudFront 전용 접근
3. **캐시 무효화**: 콘텐츠 업데이트 시 즉시 반영 방법
4. **접근 제어**: Signed URL/Cookie를 통한 프리미엄 콘텐츠 보호
5. **성능 최적화**: 압축, 지리적 제한, HTTPS 리디렉션 등의 조합

### 추가 학습 권장사항
- 틀린 문제의 해설을 다시 읽고 이론 내용 복습
- 실습 가이드를 통해 실제 CloudFront 설정 경험
- AWS 공식 문서에서 CloudFront 모범 사례 학습
- 다른 CDN 서비스와의 비교 분석

---

## 다음 학습 주제 미리보기
내일(Day 17)은 **Route 53 & DNS**에 대해 학습합니다:
- DNS의 기본 개념과 작동 원리
- Route 53의 주요 기능과 라우팅 정책
- 도메인 등록 및 호스팅 영역 설정
- CloudFront와 Route 53 연동

오늘 학습한 CloudFront와 내일 학습할 Route 53을 함께 사용하면 완전한 글로벌 웹 서비스 인프라를 구축할 수 있습니다!