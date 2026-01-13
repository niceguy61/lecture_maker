# Day 10 실습: Amazon RDS 인스턴스 생성 및 연결

## 실습 개요

이 실습에서는 Amazon RDS MySQL 인스턴스를 생성하고, 데이터베이스에 연결하여 기본적인 데이터베이스 작업을 수행합니다. 또한 Multi-AZ 배포와 Read Replica 설정을 통해 고가용성과 성능 최적화를 경험해보겠습니다.

## 실습 목표

- RDS MySQL 인스턴스 생성 및 구성
- VPC 보안 그룹을 통한 데이터베이스 접근 제어
- MySQL 클라이언트를 통한 데이터베이스 연결
- 기본 데이터베이스 작업 수행 (테이블 생성, 데이터 삽입/조회)
- Multi-AZ 배포 설정
- Read Replica 생성 및 테스트
- RDS 모니터링 및 백업 기능 확인

## 사전 준비사항

- AWS 계정 및 적절한 권한
- MySQL 클라이언트 (MySQL Workbench 또는 CLI)
- 기본적인 SQL 지식
- 이전 실습에서 생성한 VPC 및 서브넷 (없는 경우 기본 VPC 사용)

## 예상 소요 시간

약 90분

## 실습 단계

### 1단계: RDS 서브넷 그룹 생성

RDS 인스턴스를 배치할 서브넷 그룹을 먼저 생성합니다.

1. **AWS Management Console에 로그인**
   - AWS Console (https://console.aws.amazon.com)에 접속
   - 리전을 **us-east-1 (N. Virginia)**로 설정

2. **RDS 서비스로 이동**
   - 서비스 메뉴에서 "RDS" 검색 후 선택
   - 또는 직접 URL: https://console.aws.amazon.com/rds/

3. **서브넷 그룹 생성**
   ```
   좌측 메뉴 → Subnet groups → Create DB subnet group
   ```

4. **서브넷 그룹 설정**
   ```
   Name: rds-subnet-group-lab
   Description: RDS subnet group for hands-on lab
   VPC: 기본 VPC 선택 (또는 이전에 생성한 VPC)
   ```

5. **가용 영역 및 서브넷 선택**
   ```
   Availability Zones: us-east-1a, us-east-1b 선택
   Subnets: 각 AZ에서 하나씩 서브넷 선택
   ```

6. **서브넷 그룹 생성 완료**
   - "Create" 버튼 클릭
   - 생성 완료까지 약 1-2분 소요

### 2단계: RDS 보안 그룹 생성

RDS 인스턴스에 대한 네트워크 접근을 제어할 보안 그룹을 생성합니다.

1. **EC2 서비스로 이동**
   - 서비스 메뉴에서 "EC2" 선택
   - 좌측 메뉴에서 "Security Groups" 선택

2. **보안 그룹 생성**
   ```
   Create security group 클릭
   
   Security group name: rds-mysql-sg
   Description: Security group for RDS MySQL instance
   VPC: 기본 VPC 선택 (서브넷 그룹과 동일한 VPC)
   ```

3. **인바운드 규칙 설정**
   ```
   Add rule 클릭
   
   Type: MySQL/Aurora
   Protocol: TCP
   Port range: 3306
   Source: My IP (현재 IP 주소 자동 입력)
   Description: MySQL access from my IP
   ```

4. **보안 그룹 생성 완료**
   - "Create security group" 클릭

### 3단계: RDS MySQL 인스턴스 생성

이제 실제 RDS MySQL 인스턴스를 생성합니다.

1. **RDS 서비스로 돌아가기**
   - RDS 콘솔로 이동
   - "Create database" 버튼 클릭

2. **데이터베이스 생성 방법 선택**
   ```
   Choose a database creation method:
   ○ Standard create (선택)
   ○ Easy create
   ```

3. **엔진 옵션 설정**
   ```
   Engine type: MySQL (선택)
   Version: MySQL 8.0.35 (최신 버전)
   ```

4. **템플릿 선택**
   ```
   Templates:
   ○ Production
   ○ Dev/Test (선택) - Free tier 사용 가능
   ○ Free tier
   ```

5. **설정 구성**
   ```
   DB instance identifier: mysql-lab-instance
   
   Credentials Settings:
   Master username: admin
   Master password: MyPassword123! (강력한 패스워드 설정)
   Confirm password: MyPassword123!
   ```

6. **인스턴스 구성**
   ```
   DB instance class:
   ○ Burstable classes (includes t classes)
   Instance class: db.t3.micro (Free tier eligible)
   ```

7. **스토리지 설정**
   ```
   Storage type: General Purpose SSD (gp2)
   Allocated storage: 20 GiB (최소값)
   
   Storage autoscaling:
   ☑ Enable storage autoscaling
   Maximum storage threshold: 100 GiB
   ```

8. **연결 설정**
   ```
   Compute resource: Don't connect to an EC2 compute resource
   
   Network type: IPv4
   Virtual private cloud (VPC): 기본 VPC
   DB subnet group: rds-subnet-group-lab (이전에 생성한 것)
   Public access: Yes (실습을 위해 허용)
   VPC security groups: Choose existing
   Existing VPC security groups: rds-mysql-sg (이전에 생성한 것)
   ```

9. **데이터베이스 인증**
   ```
   Database authentication options:
   ○ Password authentication (선택)
   ○ Password and IAM database authentication
   ○ Password and Kerberos authentication
   ```

10. **추가 구성**
    ```
    Initial database name: labdb
    
    Backup:
    ☑ Enable automated backups
    Backup retention period: 7 days
    Backup window: No preference
    
    Monitoring:
    ☑ Enable Enhanced monitoring
    Granularity: 60 seconds
    Monitoring Role: Default
    
    Maintenance:
    ☑ Enable auto minor version upgrade
    Maintenance window: No preference
    
    Deletion protection:
    ☐ Enable deletion protection (실습이므로 체크 해제)
    ```

11. **데이터베이스 생성**
    - "Create database" 버튼 클릭
    - 생성 완료까지 약 10-15분 소요

### 4단계: RDS 인스턴스 상태 확인

1. **인스턴스 상태 모니터링**
   ```
   RDS 콘솔 → Databases
   mysql-lab-instance 상태 확인
   
   Status: Creating → Available (완료시)
   ```

2. **엔드포인트 정보 확인**
   - 인스턴스 이름 클릭
   - "Connectivity & security" 탭에서 엔드포인트 확인
   - 예: `mysql-lab-instance.xxxxxxxxx.us-east-1.rds.amazonaws.com`

### 5단계: MySQL 클라이언트 연결

#### 방법 1: MySQL Workbench 사용

1. **MySQL Workbench 설치 및 실행**
   - https://dev.mysql.com/downloads/workbench/ 에서 다운로드
   - 설치 후 실행

2. **새 연결 생성**
   ```
   Connection Name: AWS RDS MySQL Lab
   Connection Method: Standard (TCP/IP)
   Hostname: [RDS 엔드포인트 주소]
   Port: 3306
   Username: admin
   Password: [설정한 패스워드]
   ```

3. **연결 테스트**
   - "Test Connection" 버튼 클릭
   - 성공 메시지 확인 후 "OK"

#### 방법 2: MySQL CLI 사용

1. **MySQL CLI 설치** (Windows)
   ```bash
   # MySQL 공식 사이트에서 MySQL Community Server 다운로드
   # 또는 MySQL Shell 사용
   ```

2. **CLI 연결**
   ```bash
   mysql -h mysql-lab-instance.xxxxxxxxx.us-east-1.rds.amazonaws.com -P 3306 -u admin -p
   ```

3. **패스워드 입력**
   - 프롬프트에서 설정한 패스워드 입력

### 6단계: 기본 데이터베이스 작업

연결이 성공하면 기본적인 데이터베이스 작업을 수행합니다.

1. **데이터베이스 확인**
   ```sql
   SHOW DATABASES;
   USE labdb;
   ```

2. **테이블 생성**
   ```sql
   CREATE TABLE employees (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       department VARCHAR(50),
       salary DECIMAL(10,2),
       hire_date DATE,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

3. **샘플 데이터 삽입**
   ```sql
   INSERT INTO employees (name, email, department, salary, hire_date) VALUES
   ('김철수', 'kim@company.com', 'Engineering', 75000.00, '2023-01-15'),
   ('이영희', 'lee@company.com', 'Marketing', 65000.00, '2023-02-20'),
   ('박민수', 'park@company.com', 'Engineering', 80000.00, '2023-03-10'),
   ('최지영', 'choi@company.com', 'HR', 60000.00, '2023-04-05'),
   ('정수현', 'jung@company.com', 'Finance', 70000.00, '2023-05-12');
   ```

4. **데이터 조회**
   ```sql
   -- 전체 직원 조회
   SELECT * FROM employees;
   
   -- 부서별 평균 급여
   SELECT department, AVG(salary) as avg_salary 
   FROM employees 
   GROUP BY department;
   
   -- 급여가 70000 이상인 직원
   SELECT name, department, salary 
   FROM employees 
   WHERE salary >= 70000 
   ORDER BY salary DESC;
   ```

### 7단계: Multi-AZ 배포 설정

고가용성을 위해 Multi-AZ 배포를 활성화합니다.

1. **RDS 콘솔에서 인스턴스 선택**
   - mysql-lab-instance 선택
   - "Modify" 버튼 클릭

2. **Multi-AZ 설정**
   ```
   Availability & durability:
   ☑ Multi-AZ DB instance
   ```

3. **수정 적용**
   ```
   When to apply modifications:
   ○ Apply during the next scheduled maintenance window
   ○ Apply immediately (선택) - 실습을 위해
   ```

4. **수정 완료**
   - "Modify DB instance" 클릭
   - Multi-AZ 배포 완료까지 약 10-15분 소요

5. **Multi-AZ 상태 확인**
   - 인스턴스 세부 정보에서 "Multi-AZ: Yes" 확인

### 8단계: Read Replica 생성

읽기 성능 향상을 위해 Read Replica를 생성합니다.

1. **Read Replica 생성**
   ```
   mysql-lab-instance 선택 → Actions → Create read replica
   ```

2. **Read Replica 설정**
   ```
   DB instance identifier: mysql-lab-read-replica
   
   Instance configuration:
   DB instance class: db.t3.micro
   
   Connectivity:
   Destination region: US East (N. Virginia) - 같은 리전
   VPC: 기본 VPC
   DB subnet group: rds-subnet-group-lab
   Public access: Yes
   VPC security groups: rds-mysql-sg
   ```

3. **Read Replica 생성 완료**
   - "Create read replica" 클릭
   - 생성 완료까지 약 10-15분 소요

4. **Read Replica 연결 테스트**
   ```sql
   -- Read Replica 엔드포인트로 연결
   mysql -h mysql-lab-read-replica.xxxxxxxxx.us-east-1.rds.amazonaws.com -P 3306 -u admin -p
   
   -- 읽기 전용 확인
   USE labdb;
   SELECT * FROM employees;
   
   -- 쓰기 시도 (에러 발생해야 함)
   INSERT INTO employees (name, email, department, salary, hire_date) 
   VALUES ('테스트', 'test@company.com', 'Test', 50000.00, '2024-01-01');
   ```

### 9단계: RDS 모니터링

CloudWatch를 통해 RDS 성능을 모니터링합니다.

1. **CloudWatch 메트릭 확인**
   ```
   RDS 콘솔 → mysql-lab-instance → Monitoring 탭
   
   확인할 메트릭:
   - CPU Utilization
   - Database Connections
   - Read/Write IOPS
   - Network Receive/Transmit Throughput
   ```

2. **Performance Insights 확인**
   ```
   RDS 콘솔 → mysql-lab-instance → Performance Insights 탭
   
   확인 내용:
   - Top SQL statements
   - Wait events
   - Database load
   ```

3. **로그 확인**
   ```
   RDS 콘솔 → mysql-lab-instance → Logs and events 탭
   
   확인 가능한 로그:
   - Error log
   - General log
   - Slow query log
   ```

### 10단계: 백업 및 스냅샷

RDS의 백업 기능을 테스트합니다.

1. **수동 스냅샷 생성**
   ```
   mysql-lab-instance 선택 → Actions → Take snapshot
   
   Snapshot identifier: mysql-lab-manual-snapshot
   ```

2. **스냅샷 상태 확인**
   ```
   좌측 메뉴 → Snapshots
   mysql-lab-manual-snapshot 상태 확인
   ```

3. **스냅샷에서 복원 테스트**
   ```
   스냅샷 선택 → Actions → Restore snapshot
   
   DB instance identifier: mysql-lab-restored
   DB instance class: db.t3.micro
   (다른 설정은 기본값 사용)
   ```

### 11단계: 비용 모니터링

RDS 사용 비용을 확인합니다.

1. **Billing Dashboard 접근**
   ```
   AWS Console 우상단 계정명 → Billing Dashboard
   ```

2. **Cost Explorer 사용**
   ```
   좌측 메뉴 → Cost Explorer → Launch Cost Explorer
   
   Service: Amazon Relational Database Service
   Time range: Last 7 days
   ```

3. **예상 비용 확인**
   - RDS 인스턴스 실행 비용
   - 스토리지 비용
   - 백업 스토리지 비용
   - 데이터 전송 비용

## 실습 결과 확인

### 성공 기준

다음 항목들이 모두 완료되었는지 확인하세요:

- [ ] RDS MySQL 인스턴스가 "Available" 상태
- [ ] MySQL 클라이언트로 성공적으로 연결
- [ ] 테이블 생성 및 데이터 삽입/조회 성공
- [ ] Multi-AZ 배포 활성화 완료
- [ ] Read Replica 생성 및 연결 테스트 완료
- [ ] CloudWatch 메트릭 확인 가능
- [ ] 수동 스냅샷 생성 완료

### 예상 결과

1. **데이터베이스 연결 성공**
   ```
   MySQL [(none)]> SHOW DATABASES;
   +--------------------+
   | Database           |
   +--------------------+
   | information_schema |
   | labdb              |
   | mysql              |
   | performance_schema |
   | sys                |
   +--------------------+
   ```

2. **테이블 데이터 확인**
   ```sql
   SELECT COUNT(*) FROM employees;
   -- 결과: 5
   ```

3. **Multi-AZ 상태**
   - RDS 콘솔에서 "Multi-AZ: Yes" 표시

4. **Read Replica 상태**
   - 별도의 엔드포인트로 읽기 전용 접근 가능

## 문제 해결

### 일반적인 문제들

1. **연결 실패**
   ```
   문제: "Can't connect to MySQL server"
   해결: 
   - 보안 그룹 인바운드 규칙 확인
   - 퍼블릭 접근 설정 확인
   - 엔드포인트 주소 정확성 확인
   ```

2. **권한 오류**
   ```
   문제: "Access denied for user"
   해결:
   - 사용자명/패스워드 확인
   - 데이터베이스 인증 방법 확인
   ```

3. **성능 이슈**
   ```
   문제: 느린 쿼리 응답
   해결:
   - CloudWatch 메트릭 확인
   - Performance Insights 분석
   - 인스턴스 클래스 업그레이드 고려
   ```

### 디버깅 명령어

```sql
-- 연결 상태 확인
SHOW PROCESSLIST;

-- 데이터베이스 상태 확인
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Uptime';

-- 테이블 정보 확인
DESCRIBE employees;
SHOW CREATE TABLE employees;
```

## 정리 작업

실습 완료 후 비용 절약을 위해 리소스를 정리합니다.

### 리소스 삭제 순서

1. **Read Replica 삭제**
   ```
   mysql-lab-read-replica 선택 → Actions → Delete
   ☐ Create final snapshot (체크 해제)
   확인 텍스트 입력: delete me
   ```

2. **복원된 인스턴스 삭제** (생성한 경우)
   ```
   mysql-lab-restored 선택 → Actions → Delete
   ☐ Create final snapshot (체크 해제)
   ```

3. **메인 RDS 인스턴스 삭제**
   ```
   mysql-lab-instance 선택 → Actions → Delete
   ☐ Create final snapshot (체크 해제)
   ☐ Retain automated backups (체크 해제)
   확인 텍스트 입력: delete me
   ```

4. **스냅샷 삭제**
   ```
   Snapshots → mysql-lab-manual-snapshot 선택 → Delete
   ```

5. **서브넷 그룹 삭제**
   ```
   Subnet groups → rds-subnet-group-lab 선택 → Delete
   ```

6. **보안 그룹 삭제**
   ```
   EC2 콘솔 → Security Groups → rds-mysql-sg 선택 → Delete
   ```

## 추가 학습 자료

### AWS 공식 문서
- [Amazon RDS User Guide](https://docs.aws.amazon.com/rds/)
- [RDS MySQL 설정 가이드](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html)
- [Multi-AZ 배포 가이드](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)

### 실습 확장 아이디어
- 다른 리전에 Cross-Region Read Replica 생성
- RDS Proxy를 통한 연결 풀링 설정
- Aurora로 마이그레이션 실습
- 자동화된 백업 정책 설정

## 실습 완료 체크리스트

- [ ] RDS MySQL 인스턴스 생성 완료
- [ ] 데이터베이스 연결 및 기본 작업 수행
- [ ] Multi-AZ 배포 설정 완료
- [ ] Read Replica 생성 및 테스트 완료
- [ ] 모니터링 메트릭 확인 완료
- [ ] 백업 및 스냅샷 기능 테스트 완료
- [ ] 비용 모니터링 확인 완료
- [ ] 리소스 정리 완료

축하합니다! Amazon RDS의 핵심 기능들을 성공적으로 실습하셨습니다. 이제 실제 프로덕션 환경에서 RDS를 활용할 수 있는 기초 지식을 갖추셨습니다.