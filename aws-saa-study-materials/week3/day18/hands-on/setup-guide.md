# Day 18 실습: Lambda 함수 생성 및 API Gateway 연동

## 🎯 실습 목표

이번 실습에서는 AWS Lambda 함수를 생성하고 API Gateway와 연동하여 완전한 서버리스 REST API를 구축합니다. 실제 운영 환경에서 사용할 수 있는 수준의 API를 만들어보겠습니다.

## 📋 실습 개요

1. **Lambda 함수 생성**: Python으로 간단한 사용자 관리 API 구현
2. **API Gateway 설정**: REST API 생성 및 Lambda 연동
3. **인증 설정**: API Key 기반 인증 구현
4. **테스트 및 배포**: API 테스트 및 스테이지 배포
5. **모니터링 설정**: CloudWatch 로그 및 메트릭 확인

## ⏰ 예상 소요 시간
**총 2시간**

## 🛠️ 사전 준비사항

- AWS 계정 및 Console 접근 권한
- 기본적인 Python 지식
- JSON 형식에 대한 이해

---

## 📝 실습 1: Lambda 함수 생성

### Step 1: Lambda 서비스 접속

1. **AWS Management Console**에 로그인
2. 서비스 검색에서 **"Lambda"** 입력 후 선택
3. **"함수 생성"** 버튼 클릭

### Step 2: 함수 기본 설정

1. **함수 생성 방법 선택**
   - ✅ "새로 작성" 선택
   
2. **기본 정보 입력**
   - **함수 이름**: `user-management-api`
   - **런타임**: `Python 3.11`
   - **아키텍처**: `x86_64`

3. **실행 역할 설정**
   - ✅ "기본 Lambda 권한을 가진 새 역할 생성" 선택

4. **"함수 생성"** 버튼 클릭

### Step 3: Lambda 함수 코드 작성

함수가 생성되면 코드 편집기에서 다음 코드를 입력합니다:

```python
import json
import uuid
from datetime import datetime

# 메모리 내 사용자 데이터 (실제 환경에서는 DynamoDB 사용)
users_db = {
    "1": {
        "id": "1",
        "name": "김철수",
        "email": "kim@example.com",
        "created_at": "2024-01-15T10:30:00Z"
    },
    "2": {
        "id": "2", 
        "name": "이영희",
        "email": "lee@example.com",
        "created_at": "2024-01-16T14:20:00Z"
    }
}

def lambda_handler(event, context):
    """
    사용자 관리 API의 메인 핸들러
    """
    
    print(f"Received event: {json.dumps(event)}")
    
    # HTTP 메서드 및 경로 추출
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    path_parameters = event.get('pathParameters') or {}
    
    try:
        # 라우팅 처리
        if http_method == 'GET' and path == '/users':
            return get_all_users()
        elif http_method == 'GET' and path.startswith('/users/'):
            user_id = path_parameters.get('id')
            return get_user_by_id(user_id)
        elif http_method == 'POST' and path == '/users':
            body = json.loads(event.get('body', '{}'))
            return create_user(body)
        elif http_method == 'PUT' and path.startswith('/users/'):
            user_id = path_parameters.get('id')
            body = json.loads(event.get('body', '{}'))
            return update_user(user_id, body)
        elif http_method == 'DELETE' and path.startswith('/users/'):
            user_id = path_parameters.get('id')
            return delete_user(user_id)
        else:
            return create_response(404, {'error': 'Not Found'})
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_response(500, {'error': 'Internal Server Error'})

def get_all_users():
    """모든 사용자 조회"""
    users_list = list(users_db.values())
    return create_response(200, {
        'users': users_list,
        'count': len(users_list)
    })

def get_user_by_id(user_id):
    """특정 사용자 조회"""
    if not user_id:
        return create_response(400, {'error': 'User ID is required'})
    
    user = users_db.get(user_id)
    if user:
        return create_response(200, user)
    else:
        return create_response(404, {'error': 'User not found'})

def create_user(user_data):
    """새 사용자 생성"""
    # 입력 데이터 검증
    if not user_data.get('name') or not user_data.get('email'):
        return create_response(400, {
            'error': 'Name and email are required'
        })
    
    # 새 사용자 생성
    user_id = str(len(users_db) + 1)
    new_user = {
        'id': user_id,
        'name': user_data['name'],
        'email': user_data['email'],
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    users_db[user_id] = new_user
    
    return create_response(201, new_user)

def update_user(user_id, user_data):
    """사용자 정보 수정"""
    if not user_id:
        return create_response(400, {'error': 'User ID is required'})
    
    user = users_db.get(user_id)
    if not user:
        return create_response(404, {'error': 'User not found'})
    
    # 사용자 정보 업데이트
    if 'name' in user_data:
        user['name'] = user_data['name']
    if 'email' in user_data:
        user['email'] = user_data['email']
    
    user['updated_at'] = datetime.utcnow().isoformat() + 'Z'
    
    return create_response(200, user)

def delete_user(user_id):
    """사용자 삭제"""
    if not user_id:
        return create_response(400, {'error': 'User ID is required'})
    
    if user_id in users_db:
        deleted_user = users_db.pop(user_id)
        return create_response(200, {
            'message': 'User deleted successfully',
            'deleted_user': deleted_user
        })
    else:
        return create_response(404, {'error': 'User not found'})

def create_response(status_code, body):
    """표준 HTTP 응답 생성"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-API-Key'
        },
        'body': json.dumps(body, ensure_ascii=False)
    }
```

### Step 4: 함수 설정 최적화

1. **구성 탭**으로 이동
2. **일반 구성** 편집:
   - **메모리**: `256 MB`
   - **제한 시간**: `30초`
   - **설명**: `사용자 관리 REST API`

3. **환경 변수** 설정 (선택사항):
   - `LOG_LEVEL`: `INFO`
   - `API_VERSION`: `v1`

### Step 5: 함수 테스트

1. **테스트 탭**으로 이동
2. **새 테스트 이벤트 생성**:

```json
{
  "httpMethod": "GET",
  "path": "/users",
  "pathParameters": null,
  "queryStringParameters": null,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

3. **테스트 이벤트 이름**: `get-all-users`
4. **테스트** 버튼 클릭하여 실행 확인

---

## 🌐 실습 2: API Gateway 생성 및 설정

### Step 1: API Gateway 서비스 접속

1. AWS Console에서 **"API Gateway"** 서비스 선택
2. **"API 생성"** 버튼 클릭

### Step 2: API 유형 선택

1. **REST API** 선택 (완전한 기능을 위해)
2. **"구축"** 버튼 클릭

### Step 3: API 기본 설정

1. **API 생성 방법**:
   - ✅ "새 API" 선택

2. **설정**:
   - **API 이름**: `User Management API`
   - **설명**: `서버리스 사용자 관리 REST API`
   - **엔드포인트 유형**: `지역별`

3. **"API 생성"** 버튼 클릭

### Step 4: 리소스 및 메서드 생성

#### 4-1: /users 리소스 생성

1. **작업** → **리소스 생성** 선택
2. **리소스 설정**:
   - **리소스 이름**: `users`
   - **리소스 경로**: `users`
   - ✅ **CORS 활성화** 체크

3. **리소스 생성** 버튼 클릭

#### 4-2: GET /users 메서드 생성

1. `/users` 리소스 선택
2. **작업** → **메서드 생성** 선택
3. 드롭다운에서 **GET** 선택 후 체크 표시 클릭
4. **설정**:
   - **통합 유형**: `Lambda 함수`
   - **Lambda 프록시 통합 사용**: ✅ 체크
   - **Lambda 함수**: `user-management-api`

5. **저장** 버튼 클릭
6. 권한 추가 팝업에서 **확인** 클릭

#### 4-3: POST /users 메서드 생성

1. `/users` 리소스 선택
2. **작업** → **메서드 생성** 선택
3. **POST** 메서드 생성 (위와 동일한 설정)

#### 4-4: /users/{id} 리소스 생성

1. `/users` 리소스 선택
2. **작업** → **리소스 생성** 선택
3. **리소스 설정**:
   - **리소스 이름**: `user`
   - **리소스 경로**: `{id}`
   - ✅ **CORS 활성화** 체크

#### 4-5: GET, PUT, DELETE 메서드 생성

`/users/{id}` 리소스에 대해 GET, PUT, DELETE 메서드를 각각 생성합니다.
(설정은 위와 동일)

### Step 5: API 배포

1. **작업** → **API 배포** 선택
2. **배포 스테이지**: `[새 스테이지]`
3. **스테이지 이름**: `dev`
4. **스테이지 설명**: `개발 환경`
5. **배포** 버튼 클릭

### Step 6: API 엔드포인트 확인

배포 완료 후 **호출 URL**을 확인합니다:
```
https://your-api-id.execute-api.region.amazonaws.com/dev
```

---

## 🔐 실습 3: API Key 인증 설정

### Step 1: API Key 생성

1. API Gateway 콘솔에서 **API 키** 메뉴 선택
2. **작업** → **API 키 생성** 선택
3. **설정**:
   - **이름**: `user-api-key`
   - **설명**: `사용자 관리 API 키`

4. **저장** 버튼 클릭

### Step 2: 사용량 계획 생성

1. **사용량 계획** 메뉴 선택
2. **생성** 버튼 클릭
3. **설정**:
   - **이름**: `basic-plan`
   - **설명**: `기본 사용량 계획`
   - **제한**: `1000 요청/일`
   - **버스트**: `100 요청/초`
   - **속도**: `50 요청/초`

4. **다음** 버튼 클릭

### Step 3: API 스테이지 연결

1. **API 스테이지 추가** 클릭
2. **API**: `User Management API`
3. **스테이지**: `dev`
4. **다음** 버튼 클릭

### Step 4: API 키 연결

1. **API 키 추가** 클릭
2. 앞서 생성한 `user-api-key` 선택
3. **완료** 버튼 클릭

### Step 5: 메서드에 API Key 요구 설정

1. API Gateway에서 각 메서드 선택
2. **메서드 요청** 클릭
3. **API 키 필요**: `true`로 변경
4. 모든 메서드에 대해 반복
5. **작업** → **API 배포**로 변경사항 배포

---

## 🧪 실습 4: API 테스트

### Step 1: Postman 또는 curl을 사용한 테스트

#### 모든 사용자 조회 (GET)
```bash
curl -X GET \
  "https://your-api-id.execute-api.region.amazonaws.com/dev/users" \
  -H "X-API-Key: your-api-key"
```

#### 새 사용자 생성 (POST)
```bash
curl -X POST \
  "https://your-api-id.execute-api.region.amazonaws.com/dev/users" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "name": "박민수",
    "email": "park@example.com"
  }'
```

#### 특정 사용자 조회 (GET)
```bash
curl -X GET \
  "https://your-api-id.execute-api.region.amazonaws.com/dev/users/1" \
  -H "X-API-Key: your-api-key"
```

#### 사용자 정보 수정 (PUT)
```bash
curl -X PUT \
  "https://your-api-id.execute-api.region.amazonaws.com/dev/users/1" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "name": "김철수 (수정됨)",
    "email": "kim.updated@example.com"
  }'
```

#### 사용자 삭제 (DELETE)
```bash
curl -X DELETE \
  "https://your-api-id.execute-api.region.amazonaws.com/dev/users/2" \
  -H "X-API-Key: your-api-key"
```

### Step 2: API Gateway 테스트 콘솔 사용

1. API Gateway 콘솔에서 메서드 선택
2. **테스트** 버튼 클릭
3. **헤더** 섹션에 `X-API-Key: your-api-key` 추가
4. **테스트** 버튼 클릭하여 결과 확인

---

## 📊 실습 5: 모니터링 및 로깅

### Step 1: CloudWatch 로그 확인

1. **CloudWatch** 서비스로 이동
2. **로그** → **로그 그룹** 선택
3. `/aws/lambda/user-management-api` 로그 그룹 클릭
4. 최신 로그 스트림에서 실행 로그 확인

### Step 2: CloudWatch 메트릭 확인

1. **CloudWatch** → **메트릭** 선택
2. **AWS/Lambda** 네임스페이스 선택
3. **함수별 메트릭** 확인:
   - **Invocations**: 호출 횟수
   - **Duration**: 실행 시간
   - **Errors**: 오류 발생 횟수
   - **Throttles**: 제한 발생 횟수

### Step 3: API Gateway 메트릭 확인

1. **AWS/ApiGateway** 네임스페이스 선택
2. **API별, 스테이지별 메트릭** 확인:
   - **Count**: API 호출 횟수
   - **Latency**: 응답 시간
   - **4XXError**: 클라이언트 오류
   - **5XXError**: 서버 오류

---

## 🎯 실습 완료 체크리스트

### Lambda 함수
- [ ] Lambda 함수 생성 완료
- [ ] Python 코드 작성 및 배포 완료
- [ ] 함수 테스트 성공
- [ ] 메모리 및 타임아웃 설정 완료

### API Gateway
- [ ] REST API 생성 완료
- [ ] 리소스 및 메서드 생성 완료
- [ ] Lambda 프록시 통합 설정 완료
- [ ] API 배포 완료

### 인증 및 보안
- [ ] API Key 생성 완료
- [ ] 사용량 계획 설정 완료
- [ ] 메서드별 API Key 요구 설정 완료

### 테스트
- [ ] GET /users 테스트 성공
- [ ] POST /users 테스트 성공
- [ ] GET /users/{id} 테스트 성공
- [ ] PUT /users/{id} 테스트 성공
- [ ] DELETE /users/{id} 테스트 성공

### 모니터링
- [ ] CloudWatch 로그 확인 완료
- [ ] Lambda 메트릭 확인 완료
- [ ] API Gateway 메트릭 확인 완료

---

## 🚀 추가 도전 과제

### 1. DynamoDB 연동
현재 메모리 내 데이터베이스를 DynamoDB로 교체해보세요.

### 2. 입력 검증 강화
더 엄격한 입력 검증 로직을 추가해보세요.

### 3. 에러 처리 개선
더 상세한 에러 메시지와 HTTP 상태 코드를 구현해보세요.

### 4. CORS 설정
프론트엔드 애플리케이션을 위한 CORS 설정을 추가해보세요.

### 5. Lambda Authorizer 구현
JWT 토큰 기반의 커스텀 인증을 구현해보세요.

---

## 🔧 문제 해결 가이드

### 자주 발생하는 문제들

**1. Lambda 함수 실행 오류**
- 로그 그룹에서 상세 오류 메시지 확인
- 함수 권한 설정 확인
- 코드 문법 오류 검토

**2. API Gateway 연동 실패**
- Lambda 프록시 통합 설정 확인
- 리소스 경로 및 메서드 설정 검토
- API 배포 상태 확인

**3. API Key 인증 실패**
- API Key 값 정확성 확인
- 헤더 이름 확인 (X-API-Key)
- 사용량 계획 연결 상태 확인

**4. CORS 오류**
- 메서드별 CORS 설정 확인
- OPTIONS 메서드 추가 고려
- 응답 헤더 설정 검토

---

## 📚 참고 자료

- [AWS Lambda 개발자 가이드](https://docs.aws.amazon.com/lambda/)
- [API Gateway 개발자 가이드](https://docs.aws.amazon.com/apigateway/)
- [서버리스 애플리케이션 모범 사례](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [API Gateway와 Lambda 통합](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-with-lambda-integration.html)

이번 실습을 통해 서버리스 아키텍처의 핵심인 Lambda와 API Gateway를 실제로 구현해보았습니다. 다음 단계에서는 더 복잡한 서버리스 패턴들을 학습해보겠습니다! 🎉