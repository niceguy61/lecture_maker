# Day 11 실습: DynamoDB 테이블 생성 및 데이터 조작

## 실습 개요
이번 실습에서는 AWS Console을 통해 DynamoDB 테이블을 생성하고, 다양한 데이터 조작 작업을 수행해보겠습니다. 실제 전자상거래 애플리케이션의 사용자 및 주문 관리 시스템을 구축하는 시나리오로 진행합니다.

## 실습 목표
- DynamoDB 테이블 생성 및 설정
- 기본 키와 보조 인덱스 구성
- 데이터 입력, 조회, 수정, 삭제 작업
- 쿼리와 스캔 작업 이해
- DynamoDB의 성능 모니터링

## 사전 준비사항
- AWS 계정 및 Console 액세스
- 적절한 IAM 권한 (DynamoDB 전체 액세스)
- 예상 소요 시간: 45-60분
- 예상 비용: AWS Free Tier 내에서 무료

## 실습 1: 사용자 테이블 생성

### 1.1 DynamoDB 서비스 접속

1. **AWS Management Console에 로그인**
   - https://console.aws.amazon.com 접속
   - 계정 정보로 로그인

2. **DynamoDB 서비스 찾기**
   - 상단 검색창에 "DynamoDB" 입력
   - 검색 결과에서 "DynamoDB" 클릭
   - 또는 서비스 메뉴 → 데이터베이스 → DynamoDB 선택

3. **DynamoDB 대시보드 확인**
   - 현재 리전 확인 (우측 상단)
   - 기존 테이블 목록 확인
   - 좌측 메뉴의 주요 기능들 살펴보기

### 1.2 사용자 테이블 생성

1. **테이블 생성 시작**
   - "테이블 생성" 버튼 클릭
   - 또는 좌측 메뉴에서 "테이블" → "테이블 생성" 선택

2. **기본 설정 구성**
   ```
   테이블 이름: Users
   파티션 키: user_id (String)
   정렬 키: 사용하지 않음 (체크 해제)
   ```

3. **테이블 설정**
   - **테이블 클래스**: DynamoDB Standard
   - **용량 모드**: 온디맨드 선택
     - 이유: 실습용이므로 예측하기 어려운 트래픽 패턴

4. **보조 인덱스 설정**
   - "보조 인덱스 생성" 클릭
   - **글로벌 보조 인덱스 (GSI) 추가**:
     ```
     인덱스 이름: email-index
     파티션 키: email (String)
     정렬 키: 사용하지 않음
     프로젝션: 모든 속성
     ```

5. **암호화 설정**
   - **저장 시 암호화**: 활성화됨 (기본값)
   - **암호화 키**: AWS 소유 키 (기본값)

6. **태그 설정 (선택사항)**
   ```
   키: Environment, 값: Learning
   키: Project, 값: SAA-Study
   ```

7. **테이블 생성 완료**
   - "테이블 생성" 버튼 클릭
   - 테이블 생성 상태 확인 (약 1-2분 소요)
   - 상태가 "활성"이 될 때까지 대기

### 1.3 테이블 구조 확인

1. **테이블 세부 정보 확인**
   - 생성된 "Users" 테이블 클릭
   - "개요" 탭에서 기본 정보 확인
   - ARN, 생성 시간, 항목 수 등 확인

2. **인덱스 확인**
   - "인덱스" 탭 클릭
   - 기본 테이블과 GSI(email-index) 확인
   - 각 인덱스의 키 스키마 검토

## 실습 2: 데이터 입력 및 조회

### 2.1 항목 생성 (사용자 데이터 입력)

1. **항목 생성 시작**
   - "항목 탐색" 탭 클릭
   - "항목 생성" 버튼 클릭

2. **첫 번째 사용자 데이터 입력**
   ```json
   {
     "user_id": "user001",
     "email": "john.doe@example.com",
     "name": "John Doe",
     "age": 28,
     "city": "Seoul",
     "registration_date": "2024-01-15",
     "is_premium": true,
     "preferences": {
       "newsletter": true,
       "notifications": false
     }
   }
   ```

3. **데이터 입력 방법**
   - **JSON 뷰 사용**:
     - "JSON 뷰" 토글 활성화
     - 위의 JSON 데이터 복사하여 붙여넣기
   
   - **폼 뷰 사용**:
     - 각 속성을 개별적으로 입력
     - 데이터 타입 선택 (String, Number, Boolean 등)

4. **항목 저장**
   - "항목 생성" 버튼 클릭
   - 생성된 항목 확인

### 2.2 추가 사용자 데이터 입력

다음 사용자들을 추가로 생성해보세요:

**사용자 2:**
```json
{
  "user_id": "user002",
  "email": "jane.smith@example.com",
  "name": "Jane Smith",
  "age": 32,
  "city": "Busan",
  "registration_date": "2024-01-20",
  "is_premium": false,
  "preferences": {
    "newsletter": false,
    "notifications": true
  }
}
```

**사용자 3:**
```json
{
  "user_id": "user003",
  "email": "mike.wilson@example.com",
  "name": "Mike Wilson",
  "age": 25,
  "city": "Seoul",
  "registration_date": "2024-02-01",
  "is_premium": true,
  "preferences": {
    "newsletter": true,
    "notifications": true
  }
}
```

### 2.3 데이터 조회 및 검색

1. **전체 항목 보기**
   - "항목 탐색" 탭에서 모든 항목 확인
   - 각 항목의 속성들 검토

2. **특정 항목 조회 (GetItem)**
   - "항목 탐색" 탭에서 "쿼리" 버튼 클릭
   - **쿼리 조건**:
     ```
     파티션 키: user_id = user001
     ```
   - "쿼리 실행" 클릭
   - 결과 확인

3. **GSI를 사용한 쿼리**
   - 인덱스 드롭다운에서 "email-index" 선택
   - **쿼리 조건**:
     ```
     파티션 키: email = john.doe@example.com
     ```
   - "쿼리 실행" 클릭
   - 결과 확인

## 실습 3: 주문 테이블 생성 (복합 키 사용)

### 3.1 주문 테이블 생성

1. **새 테이블 생성**
   - DynamoDB 대시보드로 돌아가기
   - "테이블 생성" 클릭

2. **테이블 설정**
   ```
   테이블 이름: Orders
   파티션 키: user_id (String)
   정렬 키: order_id (String)
   ```

3. **용량 모드**
   - 온디맨드 모드 선택

4. **GSI 추가**
   ```
   인덱스 이름: order-date-index
   파티션 키: order_date (String)
   정렬 키: order_id (String)
   프로젝션: 모든 속성
   ```

5. **테이블 생성 완료**

### 3.2 주문 데이터 입력

다음 주문 데이터들을 입력해보세요:

**주문 1:**
```json
{
  "user_id": "user001",
  "order_id": "order_20240115_001",
  "order_date": "2024-01-15",
  "total_amount": 89.99,
  "status": "delivered",
  "items": [
    {
      "product_id": "prod001",
      "name": "Wireless Headphones",
      "price": 89.99,
      "quantity": 1
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "Seoul",
    "postal_code": "12345"
  }
}
```

**주문 2:**
```json
{
  "user_id": "user001",
  "order_id": "order_20240120_002",
  "order_date": "2024-01-20",
  "total_amount": 149.98,
  "status": "shipped",
  "items": [
    {
      "product_id": "prod002",
      "name": "Bluetooth Speaker",
      "price": 79.99,
      "quantity": 1
    },
    {
      "product_id": "prod003",
      "name": "Phone Case",
      "price": 19.99,
      "quantity": 1
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "Seoul",
    "postal_code": "12345"
  }
}
```

**주문 3:**
```json
{
  "user_id": "user002",
  "order_id": "order_20240125_003",
  "order_date": "2024-01-25",
  "total_amount": 299.99,
  "status": "processing",
  "items": [
    {
      "product_id": "prod004",
      "name": "Laptop Stand",
      "price": 299.99,
      "quantity": 1
    }
  ],
  "shipping_address": {
    "street": "456 Oak Ave",
    "city": "Busan",
    "postal_code": "67890"
  }
}
```

## 실습 4: 고급 쿼리 및 데이터 조작

### 4.1 복합 키를 사용한 쿼리

1. **특정 사용자의 모든 주문 조회**
   - Orders 테이블의 "항목 탐색" 탭
   - **쿼리 조건**:
     ```
     파티션 키: user_id = user001
     ```
   - 결과: user001의 모든 주문 표시

2. **특정 주문 조회**
   - **쿼리 조건**:
     ```
     파티션 키: user_id = user001
     정렬 키: order_id = order_20240115_001
     ```
   - 결과: 특정 주문 하나만 표시

3. **날짜 범위 쿼리**
   - 인덱스를 "order-date-index"로 변경
   - **쿼리 조건**:
     ```
     파티션 키: order_date = 2024-01-20
     ```

### 4.2 스캔 작업

1. **전체 테이블 스캔**
   - "스캔" 버튼 클릭
   - 모든 항목 조회 (비효율적이지만 소규모 테이블에서는 가능)

2. **필터 조건이 있는 스캔**
   - "필터 추가" 클릭
   - **필터 조건**:
     ```
     속성: total_amount
     조건: 보다 큼
     값: 100
     ```
   - 100달러 이상의 주문만 표시

### 4.3 데이터 수정

1. **항목 수정**
   - 수정할 항목 선택 (예: user001의 첫 번째 주문)
   - "작업" → "항목 편집" 클릭

2. **상태 업데이트**
   - status 속성을 "delivered"에서 "completed"로 변경
   - "변경 사항 저장" 클릭

3. **새 속성 추가**
   - "새 속성 추가" 클릭
   - **속성 추가**:
     ```
     속성 이름: delivery_date
     타입: String
     값: 2024-01-18
     ```

### 4.4 조건부 쓰기

1. **조건부 업데이트 시뮬레이션**
   - 실제 애플리케이션에서는 조건부 쓰기 사용
   - 예: 주문 상태가 "processing"일 때만 "shipped"로 변경
   - Console에서는 직접 지원하지 않지만 개념 이해

## 실습 5: 성능 모니터링 및 메트릭

### 5.1 CloudWatch 메트릭 확인

1. **테이블 메트릭 보기**
   - Users 테이블 선택
   - "모니터링" 탭 클릭

2. **주요 메트릭 확인**
   - **읽기 용량 소비**: 현재 읽기 작업량
   - **쓰기 용량 소비**: 현재 쓰기 작업량
   - **제한된 요청**: 용량 초과로 인한 제한
   - **시스템 오류**: 시스템 레벨 오류

3. **메트릭 해석**
   - 온디맨드 모드에서는 자동 확장
   - 실습 중 발생한 읽기/쓰기 패턴 관찰

### 5.2 항목 수준 메트릭

1. **항목 크기 확인**
   - 각 항목의 크기 (바이트 단위)
   - 큰 항목이 성능에 미치는 영향 이해

2. **인덱스 사용량**
   - GSI의 읽기/쓰기 패턴
   - 기본 테이블 vs 인덱스 사용량 비교

## 실습 6: 데이터 내보내기 및 백업

### 6.1 데이터 내보내기

1. **S3로 내보내기**
   - "백업" 탭 클릭
   - "S3로 내보내기" 선택
   - **설정**:
     ```
     S3 버킷: 새 버킷 생성 또는 기존 버킷 선택
     내보내기 형식: DynamoDB JSON
     ```

2. **내보내기 작업 모니터링**
   - 내보내기 작업 상태 확인
   - 완료 후 S3에서 파일 확인

### 6.2 Point-in-Time Recovery 설정

1. **PITR 활성화**
   - "백업" 탭에서 "Point-in-time recovery" 섹션
   - "편집" 클릭
   - "Point-in-time recovery 활성화" 체크
   - "변경 사항 저장"

2. **백업 정책 이해**
   - 35일간 연속 백업
   - 추가 비용 발생 (실습 후 비활성화 권장)

## 실습 7: 정리 및 리소스 삭제

### 7.1 테이블 삭제

1. **Users 테이블 삭제**
   - Users 테이블 선택
   - "작업" → "테이블 삭제" 클릭
   - 확인 메시지에 "delete" 입력
   - "테이블 삭제" 클릭

2. **Orders 테이블 삭제**
   - 동일한 방법으로 Orders 테이블 삭제

3. **삭제 확인**
   - 테이블 목록에서 삭제된 테이블 확인
   - 완전 삭제까지 몇 분 소요

### 7.2 관련 리소스 정리

1. **S3 버킷 정리** (내보내기를 수행한 경우)
   - S3 Console에서 생성된 버킷 확인
   - 불필요한 파일 삭제

2. **CloudWatch 로그 확인**
   - DynamoDB 관련 로그 확인
   - 필요시 로그 그룹 삭제

## 실습 결과 검증

### 완료해야 할 체크리스트

- [ ] DynamoDB 테이블 2개 생성 (Users, Orders)
- [ ] 기본 키와 GSI 설정 완료
- [ ] 사용자 데이터 3개 입력
- [ ] 주문 데이터 3개 입력
- [ ] GetItem, Query, Scan 작업 수행
- [ ] 데이터 수정 및 새 속성 추가
- [ ] CloudWatch 메트릭 확인
- [ ] 데이터 내보내기 수행
- [ ] 모든 리소스 정리 완료

### 학습 성과 확인

1. **DynamoDB 기본 개념 이해**
   - 파티션 키와 정렬 키의 역할
   - GSI와 LSI의 차이점
   - 온디맨드 vs 프로비저닝 모드

2. **데이터 모델링 경험**
   - NoSQL 데이터 모델링 방식
   - 액세스 패턴 기반 설계
   - 인덱스 전략

3. **운영 관리 기술**
   - 성능 모니터링
   - 백업 및 복구
   - 비용 최적화

## 문제 해결 가이드

### 일반적인 문제들

1. **테이블 생성 실패**
   - 테이블 이름 중복 확인
   - IAM 권한 확인
   - 리전 설정 확인

2. **데이터 입력 오류**
   - JSON 형식 검증
   - 데이터 타입 일치 확인
   - 필수 속성 누락 확인

3. **쿼리 결과 없음**
   - 파티션 키 값 정확성 확인
   - 인덱스 선택 확인
   - 데이터 존재 여부 확인

4. **성능 이슈**
   - 핫 파티션 문제 확인
   - 쿼리 vs 스캔 사용 패턴
   - 인덱스 활용도 검토

### 추가 학습 리소스

- **AWS DynamoDB 개발자 가이드**: 상세한 API 문서
- **DynamoDB 모범 사례**: 성능 최적화 가이드
- **AWS Well-Architected Framework**: 데이터베이스 설계 원칙
- **DynamoDB 워크샵**: 실습 중심 학습 자료

## 다음 단계

이번 실습을 통해 DynamoDB의 기본적인 사용법을 익혔습니다. 다음 학습에서는:

1. **Day 12**: 데이터 마이그레이션 서비스 (DMS)
2. **고급 DynamoDB 기능**: Streams, Global Tables
3. **애플리케이션 통합**: Lambda와 DynamoDB 연동
4. **성능 튜닝**: 실제 운영 환경 최적화

실습을 통해 얻은 경험을 바탕으로 실제 프로젝트에서 DynamoDB를 효과적으로 활용할 수 있을 것입니다!