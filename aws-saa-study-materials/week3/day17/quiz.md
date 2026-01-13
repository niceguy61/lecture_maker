# Day 17 퀴즈: Route 53 & DNS

## 퀴즈 개요
- **주제**: Route 53 & DNS
- **문제 수**: 5문제
- **예상 소요 시간**: 10-15분
- **난이도**: 중급

---

## 문제 1: Route 53 라우팅 정책

**시나리오**: 글로벌 웹 애플리케이션을 운영하고 있으며, 사용자의 지리적 위치에 따라 가장 가까운 서버로 트래픽을 라우팅하고 싶습니다.

**질문**: 이 요구사항을 만족하는 가장 적절한 Route 53 라우팅 정책은 무엇입니까?

A) Simple Routing  
B) Weighted Routing  
C) Latency-based Routing  
D) Geolocation Routing

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: C) Latency-based Routing**

**해설**:
- **Latency-based Routing**은 사용자와 AWS 리전 간의 네트워크 지연 시간을 측정하여 가장 낮은 지연 시간을 제공하는 리소스로 트래픽을 라우팅합니다.
- 이는 사용자에게 가장 빠른 응답 시간을 제공하는 최적의 방법입니다.

**다른 선택지 설명**:
- A) Simple Routing: 단일 리소스에 대한 기본적인 DNS 응답만 제공
- B) Weighted Routing: 가중치에 따른 트래픽 분산, 지리적 위치와 무관
- D) Geolocation Routing: 사용자의 지리적 위치에 따른 라우팅이지만, 반드시 가장 가까운 서버를 보장하지는 않음

**참고**: Latency-based Routing을 사용하려면 각 리전에 리소스를 배포하고 Route 53에서 각 리소스에 대한 지연 시간 기반 레코드를 생성해야 합니다.
</details>

---

## 문제 2: DNS 레코드 타입

**시나리오**: 회사에서 새로운 웹사이트를 런칭하려고 합니다. 메인 도메인은 example.com이고, 블로그는 blog.example.com으로 설정하려고 합니다. 블로그는 실제로는 www.example.com과 동일한 서버에서 호스팅됩니다.

**질문**: blog.example.com을 www.example.com으로 매핑하기 위해 사용해야 하는 DNS 레코드 타입은 무엇입니까?

A) A 레코드  
B) AAAA 레코드  
C) CNAME 레코드  
D) MX 레코드

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: C) CNAME 레코드**

**해설**:
- **CNAME(Canonical Name) 레코드**는 도메인 이름을 다른 도메인 이름으로 매핑하는 데 사용됩니다.
- blog.example.com을 www.example.com으로 매핑하면, blog.example.com에 대한 DNS 쿼리는 www.example.com의 IP 주소를 반환합니다.
- 이는 별칭(alias) 기능을 제공하여 여러 도메인이 동일한 리소스를 가리킬 수 있게 합니다.

**다른 선택지 설명**:
- A) A 레코드: 도메인을 IPv4 주소로 직접 매핑
- B) AAAA 레코드: 도메인을 IPv6 주소로 직접 매핑
- D) MX 레코드: 메일 서버 정보를 지정

**주의사항**: CNAME 레코드는 루트 도메인(example.com)에는 사용할 수 없으며, 서브도메인에만 사용 가능합니다.
</details>

---

## 문제 3: Route 53 헬스 체크

**시나리오**: 두 개의 웹 서버를 운영하고 있으며, 기본 서버가 실패할 경우 자동으로 보조 서버로 트래픽을 전환하고 싶습니다. Route 53의 Failover 라우팅을 사용하려고 합니다.

**질문**: Failover 라우팅이 올바르게 작동하기 위해 반드시 필요한 구성 요소는 무엇입니까?

A) CloudWatch 알람  
B) Health Check  
C) Auto Scaling Group  
D) Load Balancer

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B) Health Check**

**해설**:
- **Health Check**는 Route 53 Failover 라우팅의 핵심 구성 요소입니다.
- Route 53은 헬스 체크를 통해 기본(Primary) 리소스의 상태를 지속적으로 모니터링합니다.
- 헬스 체크가 실패하면 자동으로 보조(Secondary) 리소스로 트래픽을 전환합니다.
- 헬스 체크 없이는 Route 53이 리소스의 상태를 알 수 없어 자동 장애 조치가 불가능합니다.

**다른 선택지 설명**:
- A) CloudWatch 알람: 모니터링에 유용하지만 Failover 라우팅의 필수 요소는 아님
- C) Auto Scaling Group: 인스턴스 확장/축소 기능, Failover와는 다른 개념
- D) Load Balancer: 트래픽 분산 기능, Failover 라우팅과는 별개

**참고**: 헬스 체크는 HTTP/HTTPS, TCP, 또는 계산된 헬스 체크 타입을 사용할 수 있습니다.
</details>

---

## 문제 4: Route 53 Alias 레코드

**시나리오**: Route 53에서 루트 도메인(example.com)을 Application Load Balancer(ALB)로 연결하려고 합니다. ALB의 DNS 이름은 변경될 수 있으므로 유연한 방법을 찾고 있습니다.

**질문**: 이 상황에서 가장 적절한 Route 53 레코드 설정은 무엇입니까?

A) A 레코드로 ALB의 IP 주소 직접 매핑  
B) CNAME 레코드로 ALB DNS 이름 매핑  
C) Alias A 레코드로 ALB 매핑  
D) MX 레코드로 ALB 매핑

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: C) Alias A 레코드로 ALB 매핑**

**해설**:
- **Alias 레코드**는 AWS 리소스(ALB, CloudFront, S3 등)에 대한 특별한 Route 53 기능입니다.
- 루트 도메인에는 CNAME 레코드를 사용할 수 없지만, Alias 레코드는 사용 가능합니다.
- Alias 레코드는 대상 리소스의 IP 주소가 변경되어도 자동으로 업데이트됩니다.
- DNS 쿼리에 대한 추가 비용이 발생하지 않습니다.

**다른 선택지 설명**:
- A) A 레코드로 IP 직접 매핑: ALB의 IP는 변경될 수 있어 부적절
- B) CNAME 레코드: 루트 도메인에는 사용 불가
- D) MX 레코드: 메일 서버용 레코드로 부적절

**Alias 레코드의 장점**:
- 자동 IP 주소 해석
- 무료 DNS 쿼리
- AWS 서비스와의 완벽한 통합
</details>

---

## 문제 5: Route 53 비용 최적화

**시나리오**: 회사에서 Route 53을 사용하여 여러 도메인을 관리하고 있습니다. 월 DNS 쿼리 수가 매우 높아 비용이 증가하고 있습니다. 성능을 유지하면서 비용을 절약할 수 있는 방법을 찾고 있습니다.

**질문**: Route 53 DNS 쿼리 비용을 절약하기 위한 가장 효과적인 방법은 무엇입니까?

A) 헬스 체크 수를 줄인다  
B) TTL(Time To Live) 값을 증가시킨다  
C) 호스팅 영역 수를 줄인다  
D) 라우팅 정책을 Simple로 변경한다

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: B) TTL(Time To Live) 값을 증가시킨다**

**해설**:
- **TTL 값을 증가**시키면 DNS 레코드가 클라이언트와 DNS 리졸버에서 더 오래 캐시됩니다.
- 캐시 시간이 길어지면 Route 53에 대한 DNS 쿼리 수가 감소하여 비용이 절약됩니다.
- 예: TTL을 300초에서 3600초(1시간)로 증가시키면 쿼리 수가 크게 감소합니다.

**다른 선택지 설명**:
- A) 헬스 체크 수 줄이기: 헬스 체크 비용은 별도이며, DNS 쿼리 비용과는 무관
- C) 호스팅 영역 수 줄이기: 호스팅 영역 비용은 고정이며, 쿼리 수와는 무관
- D) 라우팅 정책 변경: 라우팅 정책 자체는 쿼리 비용에 직접적인 영향을 주지 않음

**TTL 설정 시 고려사항**:
- 높은 TTL: 비용 절약, 하지만 DNS 변경 시 전파 시간 증가
- 낮은 TTL: 빠른 변경 반영, 하지만 높은 쿼리 비용
- 적절한 균형점을 찾는 것이 중요

**추가 비용 절약 팁**:
- 불필요한 DNS 레코드 제거
- CNAME 체인 최소화
- 지리적 라우팅 최적화
</details>

---

## 퀴즈 완료!

### 점수 계산
- 5문제 모두 맞음: 🏆 **완벽!** Route 53 전문가 수준입니다.
- 4문제 맞음: 🎉 **우수!** Route 53을 잘 이해하고 있습니다.
- 3문제 맞음: 👍 **양호!** 기본 개념은 잘 알고 있습니다.
- 2문제 이하: 📚 **복습 필요!** 이론 내용을 다시 검토해보세요.

### 추가 학습 권장사항

**3문제 이하 맞은 경우**:
- Day 17 이론 내용 재검토
- AWS Route 53 공식 문서 학습
- 실습 가이드 재실행

**4-5문제 맞은 경우**:
- 고급 Route 53 기능 학습 (Traffic Flow, Resolver)
- 다른 AWS 서비스와의 통합 시나리오 학습
- 실제 프로덕션 환경에서의 모범 사례 학습

### 다음 학습 주제
내일은 **API Gateway & Lambda**를 통한 서버리스 아키텍처에 대해 학습합니다. Route 53과 API Gateway를 연동하는 방법도 함께 다룰 예정입니다.

---

**수고하셨습니다! 🎯**