# Day 12 실습: AWS DMS를 이용한 데이터베이스 마이그레이션

## 실습 개요
이번 실습에서는 AWS Database Migration Service (DMS)를 사용하여 MySQL 데이터베이스에서 Amazon RDS MySQL로 데이터를 마이그레이션하는 과정을 체험해보겠습니다. 실제 프로덕션 환경에서 사용되는 마이그레이션 패턴을 학습할 수 있습니다.

## 실습 목표
- DMS 복제 인스턴스 생성 및 구성
- 소스 및 타겟 엔드포인트 설정
- 마이그레이션 태스크 생성 및 실행
- 마이그레이션 모니터링 및 문제 해결

## 사전 준비사항
- AWS 계정 및 적절한 권한
- 기본적인 데이터베이스 지식
- 예상 소요 시간: 60-90분
- 예상 비용: $5-10 (실습 후 리소스 정리 시)

## 실습 아키텍처

```
[Source RDS MySQL] --> [DMS Replication Instance] --> [Target RDS MySQL]
                              |
                              v
                      [CloudWatch Monitoring]
```

## 단계 1: 소스 및 타겟 RDS 인스턴스 준비

### 1.1 소스 RDS MySQL 인스턴스 생성

1. **AWS Console에 로그인**
   - AWS Management Console (https://console.aws.amazon.com)
   - 리전을 `us-east-1` (버지니아 북부)로 설정

2. **RDS 서비스로 이동**
   - 서비스 메뉴에서 "RDS" 검색 후 클릭
   - 또는 직접 URL: https://console.aws.amazon.com/rds/

3. **데이터베이스 생성 - 소스용**
   ```
   Create database 클릭
   
   Database creation method: Standard create
   Engine type: MySQL
   Version: MySQL 8.0.35 (최신 버전)
   
   Templates: Free tier
   
   DB instance identifier: dms-source-mysql
   Master username: admin
   Master password: MyPassword123! (기록해두세요)
   
   DB instance class: db.t3.micro
   Storage type: General Purpose SSD (gp2)
   Allocated storage: 20 GB
   
   VPC: Default VPC
   Subnet group: default
   Public access: Yes (실습용)
   VPC security groups: Create new
   New VPC security group name: dms-source-sg
   
   Database port: 3306
   Database authentication: Password authentication
   
   Initial database name: sampledb
   
   Backup retention period: 7 days
   Enable automated backups: Yes (DMS 요구사항)
   
   Enable Enhanced monitoring: No (비용 절약)
   Enable Performance Insights: No
   ```

4. **Create database 클릭**
   - 생성 완료까지 약 10-15분 소요
   - 상태가 "Available"이 될 때까지 대기

### 1.2 타겟 RDS MySQL 인스턴스 생성

1. **두 번째 데이터베이스 생성**
   ```
   Create database 클릭
   
   Database creation method: Standard create
   Engine type: MySQL
   Version: MySQL 8.0.35
   
   Templates: Free tier
   
   DB instance identifier: dms-target-mysql
   Master username: admin
   Master password: MyPassword123!
   
   DB instance class: db.t3.micro
   Storage type: General Purpose SSD (gp2)
   Allocated storage: 20 GB
   
   VPC: Default VPC
   Subnet group: default
   Public access: Yes
   VPC security groups: Create new
   New VPC security group name: dms-target-sg
   
   Database port: 3306
   Initial database name: targetdb
   ```

2. **Create database 클릭**

### 1.3 보안 그룹 설정

1. **EC2 Console로 이동**
   - 서비스 메뉴에서 "EC2" 검색

2. **Security Groups 설정**
   - 왼쪽 메뉴에서 "Security Groups" 클릭
   - `dms-source-sg` 선택
   - "Inbound rules" 탭 → "Edit inbound rules"
   - 규칙 추가:
     ```
     Type: MySQL/Aurora
     Protocol: TCP
     Port: 3306
     Source: Anywhere-IPv4 (0.0.0.0/0) - 실습용만
     ```
   - "Save rules" 클릭

3. **타겟 보안 그룹도 동일하게 설정**
   - `dms-target-sg`에 대해서도 같은 규칙 적용

## 단계 2: 소스 데이터베이스에 샘플 데이터 생성

### 2.1 MySQL 클라이언트 연결

1. **RDS 엔드포인트 확인**
   - RDS Console → Databases
   - `dms-source-mysql` 클릭
   - "Connectivity & security" 탭에서 Endpoint 복사
   - 예: `dms-source-mysql.xxxxxxxxx.us-east-1.rds.amazonaws.com`

2. **MySQL 클라이언트로 연결** (로컬 환경에 MySQL 클라이언트 필요)
   ```bash
   mysql -h dms-source-mysql.xxxxxxxxx.us-east-1.rds.amazonaws.com -u admin -p sampledb
   ```

### 2.2 샘플 테이블 및 데이터 생성

```sql
-- 고객 테이블 생성
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 주문 테이블 생성
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 샘플 고객 데이터 삽입
INSERT INTO customers (first_name, last_name, email, phone) VALUES
('김', '철수', 'kim.cs@email.com', '010-1234-5678'),
('이', '영희', 'lee.yh@email.com', '010-2345-6789'),
('박', '민수', 'park.ms@email.com', '010-3456-7890'),
('최', '지영', 'choi.jy@email.com', '010-4567-8901'),
('정', '현우', 'jung.hw@email.com', '010-5678-9012');

-- 샘플 주문 데이터 삽입
INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
(1, '2024-01-15', 150000.00, 'completed'),
(2, '2024-01-16', 89000.00, 'completed'),
(3, '2024-01-17', 245000.00, 'pending'),
(1, '2024-01-18', 67000.00, 'shipped'),
(4, '2024-01-19', 123000.00, 'completed');

-- 데이터 확인
SELECT COUNT(*) as customer_count FROM customers;
SELECT COUNT(*) as order_count FROM orders;
```

## 단계 3: DMS 복제 인스턴스 생성

### 3.1 DMS 서비스로 이동

1. **AWS Console에서 DMS 검색**
   - 서비스 메뉴에서 "Database Migration Service" 또는 "DMS" 검색
   - 또는 직접 URL: https://console.aws.amazon.com/dms/

2. **DMS 대시보드 확인**
   - 처음 사용하는 경우 Welcome 페이지가 표시됨
   - "Get started" 클릭 (선택사항)

### 3.2 서브넷 그룹 생성

1. **왼쪽 메뉴에서 "Subnet groups" 클릭**

2. **Create subnet group**
   ```
   Name: dms-subnet-group
   Description: DMS subnet group for migration
   VPC: Default VPC 선택
   
   Add subnets:
   - 사용 가능한 모든 서브넷 선택 (최소 2개 AZ)
   - 각 AZ에서 하나씩 선택
   ```

3. **Create subnet group 클릭**

### 3.3 복제 인스턴스 생성

1. **왼쪽 메뉴에서 "Replication instances" 클릭**

2. **Create replication instance**
   ```
   Name: dms-replication-instance
   Description: MySQL to MySQL migration instance
   
   Instance class: dms.t3.micro (Free tier eligible)
   Engine version: 3.5.2 (최신 버전)
   
   Allocated storage: 20 GB
   
   VPC: Default VPC
   Replication subnet group: dms-subnet-group
   
   Publicly accessible: No (보안상 권장)
   
   Advanced security and network configuration:
   VPC security groups: Create new
   New security group name: dms-replication-sg
   ```

3. **Create replication instance 클릭**
   - 생성 완료까지 약 5-10분 소요
   - 상태가 "Available"이 될 때까지 대기

### 3.4 복제 인스턴스 보안 그룹 설정

1. **EC2 Console → Security Groups**

2. **dms-replication-sg 편집**
   ```
   Inbound rules:
   Type: MySQL/Aurora
   Port: 3306
   Source: dms-source-sg, dms-target-sg
   
   Outbound rules:
   Type: MySQL/Aurora  
   Port: 3306
   Destination: dms-source-sg, dms-target-sg
   ```

## 단계 4: 엔드포인트 생성

### 4.1 소스 엔드포인트 생성

1. **DMS Console → Endpoints → Create endpoint**

2. **소스 엔드포인트 설정**
   ```
   Endpoint type: Source endpoint
   
   Endpoint identifier: mysql-source-endpoint
   Source engine: MySQL
   
   Access to endpoint database: Provide access information manually
   
   Server name: [소스 RDS 엔드포인트]
   Port: 3306
   User name: admin
   Password: MyPassword123!
   
   Test endpoint connection:
   VPC: Default VPC
   Replication instance: dms-replication-instance
   ```

3. **Run test 클릭**
   - 연결 테스트 성공 확인
   - "Create endpoint" 클릭

### 4.2 타겟 엔드포인트 생성

1. **Create endpoint (타겟용)**
   ```
   Endpoint type: Target endpoint
   
   Endpoint identifier: mysql-target-endpoint
   Target engine: MySQL
   
   Access to endpoint database: Provide access information manually
   
   Server name: [타겟 RDS 엔드포인트]
   Port: 3306
   User name: admin
   Password: MyPassword123!
   
   Test endpoint connection:
   VPC: Default VPC
   Replication instance: dms-replication-instance
   ```

2. **Run test → Create endpoint**

## 단계 5: 마이그레이션 태스크 생성 및 실행

### 5.1 데이터베이스 마이그레이션 태스크 생성

1. **DMS Console → Database migration tasks → Create task**

2. **태스크 설정**
   ```
   Task identifier: mysql-migration-task
   Replication instance: dms-replication-instance
   Source database endpoint: mysql-source-endpoint
   Target database endpoint: mysql-target-endpoint
   Migration type: Migrate existing data (Full load)
   
   Task Settings:
   Target table preparation mode: Drop tables on target
   Include LOB columns in replication: Limited LOB mode
   Maximum LOB size: 32 KB
   
   Enable validation: Yes
   Enable CloudWatch logs: Yes
   ```

### 5.2 테이블 매핑 설정

1. **Table mappings 섹션**
   ```
   Editing mode: Wizard
   
   Add new selection rule:
   Schema: Enter a schema
   Schema name: sampledb
   Table name: % (모든 테이블)
   Action: Include
   ```

2. **Create task 클릭**

### 5.3 마이그레이션 실행 및 모니터링

1. **태스크 시작**
   - 태스크가 자동으로 시작됨
   - 상태: "Starting" → "Running" → "Load complete"

2. **진행 상황 모니터링**
   - Task 상세 페이지에서 "Table statistics" 탭 확인
   - 각 테이블별 진행률 확인
   - "CloudWatch metrics" 탭에서 성능 지표 확인

## 단계 6: 마이그레이션 결과 검증

### 6.1 타겟 데이터베이스 연결

```bash
mysql -h dms-target-mysql.xxxxxxxxx.us-east-1.rds.amazonaws.com -u admin -p targetdb
```

### 6.2 데이터 검증

```sql
-- 데이터베이스 목록 확인
SHOW DATABASES;

-- sampledb 사용
USE sampledb;

-- 테이블 목록 확인
SHOW TABLES;

-- 데이터 개수 확인
SELECT COUNT(*) as customer_count FROM customers;
SELECT COUNT(*) as order_count FROM orders;

-- 데이터 내용 확인
SELECT * FROM customers LIMIT 5;
SELECT * FROM orders LIMIT 5;

-- 조인 쿼리 테스트
SELECT 
    c.first_name, 
    c.last_name, 
    o.order_date, 
    o.total_amount, 
    o.status
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC;
```

## 단계 7: 실시간 복제 테스트 (선택사항)

### 7.1 CDC 태스크 생성

1. **새로운 마이그레이션 태스크 생성**
   ```
   Task identifier: mysql-cdc-task
   Migration type: Replicate data changes only (CDC)
   
   또는
   
   Migration type: Migrate existing data and replicate ongoing changes
   ```

### 7.2 실시간 변경 테스트

1. **소스 데이터베이스에서 데이터 변경**
   ```sql
   -- 새 고객 추가
   INSERT INTO customers (first_name, last_name, email, phone) 
   VALUES ('홍', '길동', 'hong.gd@email.com', '010-9999-0000');
   
   -- 기존 주문 상태 변경
   UPDATE orders SET status = 'delivered' WHERE order_id = 1;
   
   -- 새 주문 추가
   INSERT INTO orders (customer_id, order_date, total_amount, status) 
   VALUES (6, CURDATE(), 99000.00, 'pending');
   ```

2. **타겟 데이터베이스에서 변경사항 확인**
   - 몇 초 후 타겟 DB에서 동일한 변경사항 확인

## 단계 8: 모니터링 및 문제 해결

### 8.1 CloudWatch 메트릭 확인

1. **CloudWatch Console 이동**
   - 서비스 메뉴에서 "CloudWatch" 검색

2. **DMS 메트릭 확인**
   ```
   Metrics → All metrics → DMS
   
   주요 메트릭:
   - CPUUtilization
   - DatabaseConnections
   - FreeableMemory
   - NetworkReceiveThroughput
   - NetworkTransmitThroughput
   ```

### 8.2 로그 분석

1. **CloudWatch Logs 확인**
   ```
   CloudWatch → Logs → Log groups
   
   DMS 관련 로그 그룹:
   - /aws/dms/task/[task-id]
   ```

2. **일반적인 오류 및 해결방법**
   ```
   오류: "Connection failed"
   해결: 보안 그룹 및 네트워크 설정 확인
   
   오류: "Insufficient privileges"
   해결: 데이터베이스 사용자 권한 확인
   
   오류: "Table doesn't exist"
   해결: 스키마 매핑 설정 확인
   ```

## 단계 9: 리소스 정리

### 9.1 DMS 리소스 정리

1. **마이그레이션 태스크 삭제**
   - Database migration tasks → 태스크 선택 → Delete

2. **엔드포인트 삭제**
   - Endpoints → 각 엔드포인트 선택 → Delete

3. **복제 인스턴스 삭제**
   - Replication instances → 인스턴스 선택 → Delete

4. **서브넷 그룹 삭제**
   - Subnet groups → 그룹 선택 → Delete

### 9.2 RDS 인스턴스 정리

1. **RDS Console → Databases**

2. **각 인스턴스 삭제**
   ```
   인스턴스 선택 → Actions → Delete
   
   Delete options:
   - Create final snapshot: No (실습용)
   - I acknowledge...: 체크
   ```

### 9.3 보안 그룹 정리

1. **EC2 Console → Security Groups**
2. **생성한 보안 그룹들 삭제**
   - dms-source-sg
   - dms-target-sg  
   - dms-replication-sg

## 실습 정리 및 학습 포인트

### 주요 학습 내용
1. **DMS 아키텍처 이해**: 복제 인스턴스, 엔드포인트, 태스크의 역할
2. **마이그레이션 유형**: Full Load vs CDC vs Full Load + CDC
3. **네트워크 설정**: 보안 그룹과 서브넷 그룹의 중요성
4. **모니터링**: CloudWatch를 통한 성능 및 상태 추적
5. **문제 해결**: 일반적인 오류와 해결 방법

### 실무 적용 팁
- 프로덕션 환경에서는 반드시 테스트 마이그레이션 먼저 수행
- 네트워크 대역폭과 데이터 크기를 고려한 마이그레이션 계획 수립
- 백업 및 롤백 계획 준비
- 애플리케이션 다운타임 최소화를 위한 단계적 전환 전략

### 다음 단계
- 더 복잡한 스키마 변환 (Oracle → PostgreSQL)
- 대용량 데이터 마이그레이션 최적화
- 멀티 AZ 및 고가용성 설정
- 보안 강화 (VPC 엔드포인트, 암호화)

이번 실습을 통해 AWS DMS의 핵심 기능을 체험해보셨습니다. 실제 프로덕션 환경에서는 더 많은 고려사항이 있지만, 기본적인 마이그레이션 프로세스는 동일합니다.