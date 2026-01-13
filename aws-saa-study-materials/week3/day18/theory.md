# Day 18: API Gateway & Lambda - 서버리스 컴퓨팅의 핵심

## 🎯 학습 목표

오늘은 AWS의 서버리스 컴퓨팅 서비스인 Lambda와 API Gateway에 대해 깊이 있게 학습합니다. 이 두 서비스는 현대적인 클라우드 애플리케이션의 핵심 구성 요소로, 확장성과 비용 효율성을 동시에 제공합니다.

## 📚 AWS Lambda 완전 정복

### Lambda란 무엇인가?

AWS Lambda는 서버를 관리할 필요 없이 코드를 실행할 수 있게 해주는 컴퓨팅 서비스입니다. 마치 전기를 사용할 때 발전소를 직접 운영하지 않는 것처럼, Lambda를 사용하면 서버 관리 없이 코드 실행에만 집중할 수 있습니다.

```mermaid
graph TB
    A[이벤트 발생] --> B[Lambda 함수 트리거]
    B --> C[컨테이너 생성/재사용]
    C --> D[코드 실행]
    D --> E[결과 반환]
    E --> F[컨테이너 대기/종료]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fce4ec
    style F fill:#f1f8e9
```

### Lambda의 핵심 특징

**1. 이벤트 기반 실행**
Lambda는 다양한 AWS 서비스의 이벤트에 반응하여 실행됩니다:

```mermaid
graph LR
    A[S3 객체 업로드] --> L[Lambda 함수]
    B[DynamoDB 변경] --> L
    C[API Gateway 요청] --> L
    D[CloudWatch 이벤트] --> L
    E[SQS 메시지] --> L
    
    L --> F[비즈니스 로직 실행]
    
    style L fill:#ff9800
    style F fill:#4caf50
```

**2. 자동 스케일링**
Lambda는 동시 실행 요청 수에 따라 자동으로 확장됩니다. 1개의 요청이든 1000개의 요청이든 자동으로 처리합니다.

**3. 사용한 만큼만 지불**
서버가 항상 실행되는 EC2와 달리, Lambda는 코드가 실행되는 시간만큼만 비용을 지불합니다.

### Lambda 실행 환경

```mermaid
graph TB
    subgraph "Lambda 실행 환경"
        A[런타임 환경] --> B[함수 코드]
        A --> C[환경 변수]
        A --> D[메모리 할당]
        A --> E[임시 스토리지 /tmp]
        
        B --> F[핸들러 함수]
        F --> G[이벤트 처리]
        G --> H[응답 반환]
    end
    
    style A fill:#2196f3
    style F fill:#ff9800
    style G fill:#4caf50
```

**지원 런타임:**
- Python 3.8, 3.9, 3.10, 3.11
- Node.js 16.x, 18.x
- Java 8, 11, 17
- .NET Core 3.1, 6
- Go 1.x
- Ruby 2.7, 3.2
- 커스텀 런타임 (Lambda Layers 사용)

### Lambda 함수 구조

```python
import json

def lambda_handler(event, context):
    """
    Lambda 함수의 진입점
    
    Args:
        event: 트리거 이벤트 데이터
        context: 런타임 정보 객체
    
    Returns:
        dict: 응답 데이터
    """
    
    # 이벤트 데이터 처리
    print(f"Received event: {json.dumps(event)}")
    
    # 비즈니스 로직 실행
    result = process_business_logic(event)
    
    # 응답 반환
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(result)
    }

def process_business_logic(event):
    """실제 비즈니스 로직을 처리하는 함수"""
    # 여기에 실제 로직 구현
    return {"message": "Hello from Lambda!"}
```

## 🚪 API Gateway - 서버리스 API의 관문

### API Gateway란?

API Gateway는 개발자가 어떤 규모에서든 API를 생성, 게시, 유지 관리, 모니터링 및 보안할 수 있게 해주는 완전관리형 서비스입니다. 마치 건물의 리셉션 데스크처럼, 모든 API 요청을 받아서 적절한 백엔드 서비스로 라우팅합니다.

```mermaid
graph LR
    A[클라이언트] --> B[API Gateway]
    B --> C[Lambda 함수]
    B --> D[EC2 인스턴스]
    B --> E[HTTP 엔드포인트]
    B --> F[AWS 서비스]
    
    B --> G[인증/권한부여]
    B --> H[요청/응답 변환]
    B --> I[속도 제한]
    B --> J[캐싱]
    
    style B fill:#ff9800
    style G fill:#f44336
    style H fill:#2196f3
    style I fill:#9c27b0
    style J fill:#4caf50
```

### API Gateway 유형 비교

**1. REST API**
- 완전한 기능을 제공하는 API Gateway
- 복잡한 인증, 변환, 캐싱 등 고급 기능 지원
- 비용이 상대적으로 높음

**2. HTTP API**
- 간단하고 빠른 API 구축에 최적화
- REST API 대비 70% 저렴
- 기본적인 기능에 집중

```mermaid
graph TB
    subgraph "REST API"
        A1[완전한 기능]
        A2[복잡한 인증]
        A3[요청/응답 변환]
        A4[캐싱]
        A5[SDK 생성]
    end
    
    subgraph "HTTP API"
        B1[빠른 성능]
        B2[저렴한 비용]
        B3[간단한 설정]
        B4[JWT 인증]
        B5[CORS 지원]
    end
    
    style A1 fill:#2196f3
    style B1 fill:#4caf50
```

### API Gateway 요청 처리 플로우

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant AG as API Gateway
    participant L as Lambda
    participant DB as DynamoDB
    
    C->>AG: HTTP 요청
    AG->>AG: 인증 확인
    AG->>AG: 권한 부여
    AG->>AG: 요청 변환
    AG->>L: Lambda 호출
    L->>DB: 데이터 조회
    DB->>L: 데이터 반환
    L->>AG: 응답 반환
    AG->>AG: 응답 변환
    AG->>C: HTTP 응답
```

## 🔐 인증 및 권한 부여

### 인증 방법 비교

```mermaid
graph TB
    subgraph "API Gateway 인증 방법"
        A[IAM 인증]
        B[Cognito User Pool]
        C[Lambda Authorizer]
        D[API Key]
    end
    
    A --> A1[AWS 자격 증명 사용]
    A --> A2[AWS SDK/CLI 클라이언트]
    
    B --> B1[사용자 풀 기반]
    B --> B2[JWT 토큰 검증]
    
    C --> C1[커스텀 인증 로직]
    C --> C2[외부 인증 시스템 연동]
    
    D --> D1[간단한 API 키 기반]
    D --> D2[사용량 제한 가능]
    
    style A fill:#ff9800
    style B fill:#2196f3
    style C fill:#4caf50
    style D fill:#9c27b0
```

### Lambda Authorizer 구현 예제

```python
import json
import jwt
from jwt.exceptions import InvalidTokenError

def lambda_handler(event, context):
    """
    Lambda Authorizer 함수
    JWT 토큰을 검증하고 IAM 정책을 반환
    """
    
    # 토큰 추출
    token = event['authorizationToken'].replace('Bearer ', '')
    
    try:
        # JWT 토큰 검증
        payload = jwt.decode(
            token, 
            'your-secret-key', 
            algorithms=['HS256']
        )
        
        # 사용자 정보 추출
        user_id = payload['sub']
        
        # IAM 정책 생성
        policy = generate_policy(user_id, 'Allow', event['methodArn'])
        
        return policy
        
    except InvalidTokenError:
        # 토큰이 유효하지 않은 경우
        raise Exception('Unauthorized')

def generate_policy(principal_id, effect, resource):
    """IAM 정책 문서 생성"""
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': resource
                }
            ]
        },
        'context': {
            'userId': principal_id
        }
    }
```

## 🏗️ 서버리스 아키텍처 패턴

### 1. 기본 웹 API 패턴

```mermaid
graph TB
    A[클라이언트] --> B[CloudFront]
    B --> C[API Gateway]
    C --> D[Lambda 함수]
    D --> E[DynamoDB]
    
    F[S3] --> B
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fce4ec
    style F fill:#f1f8e9
```

### 2. 마이크로서비스 패턴

```mermaid
graph TB
    A[API Gateway] --> B[사용자 서비스]
    A --> C[주문 서비스]
    A --> D[결제 서비스]
    A --> E[알림 서비스]
    
    B --> B1[Lambda]
    B --> B2[DynamoDB]
    
    C --> C1[Lambda]
    C --> C2[RDS]
    
    D --> D1[Lambda]
    D --> D2[외부 결제 API]
    
    E --> E1[Lambda]
    E --> E2[SNS/SES]
    
    style A fill:#ff9800
    style B fill:#2196f3
    style C fill:#4caf50
    style D fill:#9c27b0
    style E fill:#f44336
```

### 3. 이벤트 기반 처리 패턴

```mermaid
graph TB
    A[S3 업로드] --> B[Lambda 트리거]
    B --> C[이미지 처리]
    C --> D[썸네일 생성]
    D --> E[S3 저장]
    
    B --> F[메타데이터 추출]
    F --> G[DynamoDB 저장]
    
    G --> H[SNS 알림]
    H --> I[이메일 발송]
    
    style A fill:#4caf50
    style B fill:#ff9800
    style C fill:#2196f3
    style D fill:#9c27b0
    style E fill:#4caf50
    style F fill:#ff5722
    style G fill:#795548
    style H fill:#607d8b
    style I fill:#3f51b5
```

## ⚡ Lambda 성능 최적화

### Cold Start 최소화

```python
import json
import boto3

# 전역 변수로 클라이언트 초기화 (재사용됨)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

def lambda_handler(event, context):
    """
    Cold Start를 최소화하는 Lambda 함수 구조
    """
    
    # 함수 내부에서 클라이언트를 초기화하지 않음
    # 전역 변수 사용으로 재사용 가능
    
    user_id = event['pathParameters']['userId']
    
    try:
        response = table.get_item(Key={'userId': user_id})
        
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### 메모리 및 타임아웃 최적화

```mermaid
graph TB
    A[메모리 설정] --> B[128MB - 10GB]
    A --> C[CPU 성능 비례]
    A --> D[비용 영향]
    
    E[타임아웃 설정] --> F[최대 15분]
    E --> G[적절한 값 설정]
    E --> H[무한 대기 방지]
    
    style A fill:#2196f3
    style E fill:#ff9800
```

## 🔍 모니터링 및 디버깅

### CloudWatch 통합

```mermaid
graph TB
    A[Lambda 함수] --> B[CloudWatch Logs]
    A --> C[CloudWatch Metrics]
    A --> D[X-Ray 트레이싱]
    
    B --> B1[실행 로그]
    B --> B2[에러 로그]
    
    C --> C1[호출 횟수]
    C --> C2[실행 시간]
    C --> C3[에러율]
    
    D --> D1[요청 추적]
    D --> D2[성능 분석]
    
    style A fill:#ff9800
    style B fill:#4caf50
    style C fill:#2196f3
    style D fill:#9c27b0
```

### 로깅 모범 사례

```python
import json
import logging

# 로거 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    적절한 로깅을 포함한 Lambda 함수
    """
    
    # 요청 정보 로깅
    logger.info(f"Request ID: {context.aws_request_id}")
    logger.info(f"Event: {json.dumps(event)}")
    
    try:
        # 비즈니스 로직 실행
        result = process_request(event)
        
        # 성공 로깅
        logger.info(f"Successfully processed request")
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        # 에러 로깅
        logger.error(f"Error processing request: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }

def process_request(event):
    """비즈니스 로직 처리"""
    # 처리 단계별 로깅
    logger.info("Starting business logic processing")
    
    # 실제 로직 구현
    result = {"message": "Success"}
    
    logger.info("Business logic processing completed")
    return result
```

## 💰 비용 최적화 전략

### Lambda 비용 구조

```mermaid
graph TB
    A[Lambda 비용] --> B[요청 수]
    A --> C[실행 시간]
    A --> D[메모리 사용량]
    
    B --> B1[월 100만 요청 무료]
    B --> B2[추가 요청당 $0.0000002]
    
    C --> C1[GB-초 단위 과금]
    C --> C2[월 40만 GB-초 무료]
    
    D --> D1[128MB ~ 10GB]
    D --> D2[메모리 증가 = 비용 증가]
    
    style A fill:#ff9800
    style B fill:#4caf50
    style C fill:#2196f3
    style D fill:#9c27b0
```

### API Gateway 비용 구조

```mermaid
graph TB
    A[API Gateway 비용] --> B[REST API]
    A --> C[HTTP API]
    
    B --> B1[요청당 $0.0000035]
    B --> B2[캐싱 비용 별도]
    B --> B3[데이터 전송 비용]
    
    C --> C1[요청당 $0.000001]
    C --> C2[REST API 대비 70% 저렴]
    C --> C3[기본 기능만 제공]
    
    style A fill:#ff9800
    style B fill:#f44336
    style C fill:#4caf50
```

## 🔒 보안 모범 사례

### 1. 최소 권한 원칙

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem"
            ],
            "Resource": "arn:aws:dynamodb:region:account:table/specific-table"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

### 2. 환경 변수 암호화

```python
import os
import boto3
from botocore.exceptions import ClientError

def get_secret_value(secret_name):
    """AWS Secrets Manager에서 비밀 값 조회"""
    
    session = boto3.session.Session()
    client = session.client('secretsmanager')
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        raise e

def lambda_handler(event, context):
    """보안이 강화된 Lambda 함수"""
    
    # 환경 변수에서 시크릿 이름 조회
    secret_name = os.environ['DB_SECRET_NAME']
    
    # Secrets Manager에서 실제 값 조회
    db_credentials = get_secret_value(secret_name)
    
    # 비즈니스 로직 실행
    return process_with_credentials(db_credentials)
```

## 🎯 핵심 정리

### Lambda 핵심 포인트
1. **서버리스 컴퓨팅**: 서버 관리 없이 코드 실행
2. **이벤트 기반**: 다양한 AWS 서비스 이벤트에 반응
3. **자동 스케일링**: 요청량에 따른 자동 확장
4. **사용량 기반 과금**: 실행 시간만큼만 비용 지불

### API Gateway 핵심 포인트
1. **완전관리형 API 서비스**: API 생성, 배포, 관리 자동화
2. **다양한 백엔드 연동**: Lambda, EC2, HTTP 엔드포인트 등
3. **보안 및 인증**: 다양한 인증 방법 지원
4. **모니터링 및 분석**: CloudWatch 통합 모니터링

### 서버리스 아키텍처 장점
1. **운영 부담 감소**: 서버 관리, 패치, 확장 자동화
2. **비용 효율성**: 사용한 만큼만 지불
3. **빠른 개발**: 인프라 설정 시간 단축
4. **자동 확장**: 트래픽 증가에 자동 대응

오늘 학습한 Lambda와 API Gateway는 현대적인 클라우드 애플리케이션의 핵심입니다. 다음 실습에서는 실제로 서버리스 API를 구축해보며 이론을 실전에 적용해보겠습니다! 🚀