# Day 9 실습: EFS 파일 시스템 생성 및 다중 인스턴스 연결

## 🎯 실습 목표
- Amazon EFS 파일 시스템 생성 및 구성
- 여러 EC2 인스턴스에서 EFS 마운트
- EFS 성능 모드 및 처리량 모드 이해
- EFS 보안 그룹 및 액세스 제어 설정
- EFS 백업 및 모니터링 구성

## 📋 사전 준비사항
- AWS 계정 및 적절한 권한
- 기본 VPC 또는 사용자 정의 VPC
- EC2 인스턴스 2개 이상 (다른 가용 영역 권장)
- SSH 키 페어

## 🔧 실습 1: EFS 파일 시스템 생성

### 1.1 EFS 콘솔 접속
1. AWS Management Console에 로그인
2. 서비스 검색에서 **"EFS"** 입력
3. **"Elastic File System"** 선택

### 1.2 파일 시스템 생성
1. **"파일 시스템 생성"** 버튼 클릭
2. **생성 방법 선택**:
   - **"사용자 지정"** 선택 (더 많은 옵션 제어)

### 1.3 파일 시스템 설정
**일반 설정:**
- **이름**: `my-efs-filesystem`
- **가용성 및 내구성**: 
  - **"리전"** 선택 (다중 AZ 복제)
- **성능 모드**:
  - **"범용"** 선택 (낮은 지연 시간)
- **처리량 모드**:
  - **"버스트"** 선택 (기본값)

**스토리지 클래스:**
- **"Standard"** 선택
- **"Intelligent-Tiering 사용"** 체크 (비용 최적화)

### 1.4 네트워크 설정
1. **VPC 선택**: 기본 VPC 또는 원하는 VPC
2. **마운트 대상 설정**:
   - 각 가용 영역별로 자동 생성됨
   - **보안 그룹**: 새로 생성하거나 기존 선택

### 1.5 파일 시스템 정책 (선택사항)
- 기본값으로 두거나 필요시 사용자 정의 정책 설정

### 1.6 백업 설정
- **"자동 백업 사용"** 체크
- **백업 정책**: AWS Backup 기본 정책 사용

### 1.7 생성 완료
1. **"생성"** 버튼 클릭
2. 파일 시스템 생성 완료까지 대기 (약 1-2분)

## 🔧 실습 2: EFS 보안 그룹 구성

### 2.1 EFS 보안 그룹 생성
1. **EC2 콘솔** → **보안 그룹** 이동
2. **"보안 그룹 생성"** 클릭

**보안 그룹 설정:**
- **이름**: `efs-mount-target-sg`
- **설명**: `Security group for EFS mount targets`
- **VPC**: EFS와 동일한 VPC 선택

**인바운드 규칙:**
- **유형**: NFS
- **프로토콜**: TCP
- **포트**: 2049
- **소스**: EC2 인스턴스 보안 그룹 또는 VPC CIDR

### 2.2 EFS 마운트 대상에 보안 그룹 적용
1. **EFS 콘솔**로 돌아가기
2. 생성한 파일 시스템 선택
3. **"네트워크"** 탭 클릭
4. 각 마운트 대상의 **"관리"** 클릭
5. 생성한 보안 그룹 선택 및 저장

## 🔧 실습 3: EC2 인스턴스 준비

### 3.1 첫 번째 EC2 인스턴스 생성
1. **EC2 콘솔** → **인스턴스 시작**
2. **AMI 선택**: Amazon Linux 2
3. **인스턴스 유형**: t3.micro (프리 티어)
4. **네트워크 설정**:
   - **VPC**: EFS와 동일한 VPC
   - **서브넷**: 가용 영역 A
   - **퍼블릭 IP 자동 할당**: 활성화
5. **보안 그룹**: SSH 액세스 허용
6. **키 페어**: 기존 키 페어 선택 또는 새로 생성

### 3.2 두 번째 EC2 인스턴스 생성
- 첫 번째와 동일한 설정
- **서브넷**: 다른 가용 영역 (예: 가용 영역 B)

### 3.3 인스턴스 보안 그룹 업데이트
1. EC2 인스턴스의 보안 그룹에 NFS 액세스 추가
2. **인바운드 규칙 추가**:
   - **유형**: NFS
   - **소스**: EFS 보안 그룹

## 🔧 실습 4: EFS 마운트 및 테스트

### 4.1 첫 번째 인스턴스에 EFS 마운트

**SSH 연결:**
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

**EFS 유틸리티 설치:**
```bash
sudo yum update -y
sudo yum install -y amazon-efs-utils
```

**마운트 포인트 생성:**
```bash
sudo mkdir /mnt/efs
```

**EFS 파일 시스템 마운트:**
```bash
# EFS 파일 시스템 ID 확인 (EFS 콘솔에서)
sudo mount -t efs fs-xxxxxxxxx:/ /mnt/efs

# 또는 EFS 유틸리티 사용 (권장)
sudo mount -t efs -o tls fs-xxxxxxxxx:/ /mnt/efs
```

**마운트 확인:**
```bash
df -h
mount | grep efs
```

### 4.2 두 번째 인스턴스에 EFS 마운트

**SSH 연결 및 동일한 과정 반복:**
```bash
ssh -i your-key.pem ec2-user@your-second-instance-ip
sudo yum update -y
sudo yum install -y amazon-efs-utils
sudo mkdir /mnt/efs
sudo mount -t efs -o tls fs-xxxxxxxxx:/ /mnt/efs
```

### 4.3 공유 파일 시스템 테스트

**첫 번째 인스턴스에서:**
```bash
# 테스트 파일 생성
echo "Hello from Instance 1" | sudo tee /mnt/efs/test-file.txt

# 디렉터리 생성
sudo mkdir /mnt/efs/shared-directory

# 권한 설정
sudo chmod 777 /mnt/efs/shared-directory
```

**두 번째 인스턴스에서:**
```bash
# 파일 확인
cat /mnt/efs/test-file.txt
ls -la /mnt/efs/

# 새 파일 생성
echo "Hello from Instance 2" | sudo tee /mnt/efs/shared-directory/instance2-file.txt
```

**첫 번째 인스턴스에서 확인:**
```bash
ls -la /mnt/efs/shared-directory/
cat /mnt/efs/shared-directory/instance2-file.txt
```

## 🔧 실습 5: 영구 마운트 설정

### 5.1 fstab 설정
**두 인스턴스 모두에서 실행:**

```bash
# 백업 생성
sudo cp /etc/fstab /etc/fstab.backup

# fstab에 EFS 추가
echo "fs-xxxxxxxxx.efs.region.amazonaws.com:/ /mnt/efs efs defaults,_netdev,tls" | sudo tee -a /etc/fstab
```

### 5.2 마운트 테스트
```bash
# 언마운트 후 재마운트 테스트
sudo umount /mnt/efs
sudo mount -a
df -h
```

### 5.3 부팅 시 자동 마운트 확인
```bash
# 재부팅 후 확인
sudo reboot

# 재연결 후 확인
ssh -i your-key.pem ec2-user@your-instance-ip
df -h | grep efs
```

## 🔧 실습 6: EFS 성능 테스트

### 6.1 기본 성능 테스트

**파일 생성 성능:**
```bash
# 큰 파일 생성 테스트
time dd if=/dev/zero of=/mnt/efs/testfile bs=1M count=100

# 파일 읽기 테스트
time dd if=/mnt/efs/testfile of=/dev/null bs=1M
```

**작은 파일 성능:**
```bash
# 많은 작은 파일 생성
time for i in {1..1000}; do echo "test file $i" > /mnt/efs/small_file_$i.txt; done

# 파일 개수 확인
ls /mnt/efs/small_file_*.txt | wc -l
```

### 6.2 동시 액세스 테스트

**첫 번째 인스턴스에서:**
```bash
# 동시 쓰기 테스트
for i in {1..10}; do
  echo "Writing from instance 1 - $i" >> /mnt/efs/concurrent_test.txt
  sleep 1
done &
```

**두 번째 인스턴스에서:**
```bash
# 동시 쓰기 테스트
for i in {1..10}; do
  echo "Writing from instance 2 - $i" >> /mnt/efs/concurrent_test.txt
  sleep 1
done &

# 결과 확인
tail -f /mnt/efs/concurrent_test.txt
```

## 🔧 실습 7: EFS 모니터링 및 관리

### 7.1 CloudWatch 메트릭 확인
1. **CloudWatch 콘솔** 이동
2. **메트릭** → **EFS** 선택
3. 파일 시스템 메트릭 확인:
   - `TotalIOBytes`: 총 I/O 바이트
   - `MetadataIOBytes`: 메타데이터 I/O
   - `PercentIOLimit`: I/O 한계 대비 사용률

### 7.2 EFS 인사이트 활용
1. **EFS 콘솔**에서 파일 시스템 선택
2. **모니터링** 탭 클릭
3. **인사이트** 섹션에서 성능 분석 확인

### 7.3 액세스 로그 설정 (선택사항)
```bash
# CloudTrail을 통한 EFS API 호출 로깅
# VPC Flow Logs를 통한 네트워크 트래픽 모니터링
```

## 🔧 실습 8: EFS 액세스 포인트 생성

### 8.1 액세스 포인트 생성
1. **EFS 콘솔**에서 파일 시스템 선택
2. **액세스 포인트** 탭 클릭
3. **"액세스 포인트 생성"** 클릭

**액세스 포인트 설정:**
- **이름**: `app-access-point`
- **루트 디렉터리 경로**: `/app-data`
- **POSIX 사용자**:
  - **사용자 ID**: 1001
  - **그룹 ID**: 1001
- **루트 디렉터리 생성 설정**:
  - **소유자 사용자 ID**: 1001
  - **소유자 그룹 ID**: 1001
  - **권한**: 755

### 8.2 액세스 포인트를 통한 마운트
```bash
# 새 마운트 포인트 생성
sudo mkdir /mnt/efs-app

# 액세스 포인트를 통한 마운트
sudo mount -t efs -o tls,accesspoint=fsap-xxxxxxxxx fs-xxxxxxxxx:/ /mnt/efs-app

# 확인
ls -la /mnt/efs-app
```

## 🔧 실습 9: 정리 및 리소스 삭제

### 9.1 EFS 언마운트
**모든 인스턴스에서:**
```bash
# 언마운트
sudo umount /mnt/efs
sudo umount /mnt/efs-app

# fstab에서 제거
sudo sed -i '/efs/d' /etc/fstab
```

### 9.2 AWS 리소스 정리
1. **EFS 액세스 포인트 삭제**
2. **EFS 파일 시스템 삭제**
3. **EC2 인스턴스 종료**
4. **보안 그룹 삭제** (필요시)

## 📊 실습 결과 확인

### 성공 기준
- [ ] EFS 파일 시스템 성공적으로 생성
- [ ] 두 개 이상의 EC2 인스턴스에서 동시 마운트
- [ ] 파일 공유 및 동시 액세스 확인
- [ ] 영구 마운트 설정 완료
- [ ] 성능 테스트 실행 및 결과 분석
- [ ] CloudWatch 메트릭 모니터링 확인
- [ ] 액세스 포인트 생성 및 테스트

### 예상 결과
- 여러 인스턴스에서 동일한 파일 시스템 공유
- 실시간 파일 동기화 확인
- EFS 성능 특성 이해
- 보안 및 액세스 제어 구성 경험

## 🚨 주의사항

### 보안 고려사항
- EFS 마운트 대상 보안 그룹 적절히 구성
- 전송 중 암호화(TLS) 사용 권장
- 액세스 포인트를 통한 세밀한 권한 제어

### 비용 관리
- 사용하지 않는 파일 시스템 즉시 삭제
- Intelligent-Tiering 활용으로 비용 최적화
- 불필요한 백업 정책 비활성화

### 성능 최적화
- 적절한 성능 모드 선택
- 네트워크 대역폭 고려
- I/O 패턴에 맞는 최적화

## 🔍 트러블슈팅

### 일반적인 문제
1. **마운트 실패**:
   - 보안 그룹 NFS 포트(2049) 확인
   - VPC 및 서브넷 설정 확인
   - EFS 유틸리티 설치 확인

2. **성능 이슈**:
   - 성능 모드 확인 (General Purpose vs Max I/O)
   - 네트워크 대역폭 확인
   - I/O 패턴 최적화

3. **권한 문제**:
   - POSIX 권한 설정 확인
   - 액세스 포인트 설정 검토
   - IAM 권한 확인

### 유용한 명령어
```bash
# EFS 마운트 상태 확인
mount | grep efs
df -h

# EFS 유틸리티 로그 확인
sudo tail -f /var/log/amazon/efs/mount.log

# 네트워크 연결 테스트
telnet fs-xxxxxxxxx.efs.region.amazonaws.com 2049
```

이 실습을 통해 EFS의 핵심 기능과 다중 인스턴스 파일 공유 방법을 실제로 경험할 수 있습니다. 다음 단계에서는 이러한 지식을 바탕으로 더 복잡한 아키텍처에서 EFS를 활용하는 방법을 학습하게 됩니다.