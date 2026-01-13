# Day 4 실습: EBS 볼륨 생성 및 EC2 인스턴스 연결

## 실습 개요

이번 실습에서는 AWS Console을 사용하여 EBS 볼륨을 생성하고, 실행 중인 EC2 인스턴스에 연결하는 방법을 배워보겠습니다. 또한 파일 시스템을 생성하고 마운트하는 과정까지 진행합니다.

## 학습 목표

- EBS 볼륨 생성 방법 이해
- EC2 인스턴스에 EBS 볼륨 연결
- Linux에서 볼륨 포맷 및 마운트
- EBS 스냅샷 생성 및 관리
- 볼륨 크기 조정 (확장)

## 사전 준비사항

- AWS 계정 및 Console 접근 권한
- 실행 중인 EC2 인스턴스 (Day 3에서 생성한 인스턴스 사용)
- EC2 인스턴스에 SSH 접근 가능
- 기본적인 Linux 명령어 지식

## 실습 단계

### 1단계: EBS 볼륨 생성

#### 1.1 EC2 Console 접속
1. AWS Management Console에 로그인
2. 서비스 메뉴에서 **EC2** 선택
3. 왼쪽 메뉴에서 **볼륨(Volumes)** 클릭

#### 1.2 새 볼륨 생성
1. **볼륨 생성(Create Volume)** 버튼 클릭
2. 볼륨 설정:
   - **볼륨 유형**: `gp3` (General Purpose SSD) 선택
   - **크기**: `10 GiB` 입력
   - **IOPS**: `3000` (기본값 유지)
   - **처리량**: `125 MiB/s` (기본값 유지)
   - **가용 영역**: EC2 인스턴스와 **동일한 AZ** 선택 (중요!)

> **💡 중요**: EBS 볼륨은 EC2 인스턴스와 같은 가용 영역에 있어야 연결할 수 있습니다.

3. **태그 추가** (선택사항):
   - Key: `Name`, Value: `MyFirstEBSVolume`
   - Key: `Environment`, Value: `Learning`

4. **볼륨 생성** 버튼 클릭

#### 1.3 볼륨 생성 확인
- 볼륨 목록에서 새로 생성된 볼륨 확인
- 상태가 `available`이 될 때까지 대기 (약 1-2분)

### 2단계: EC2 인스턴스에 볼륨 연결

#### 2.1 볼륨 연결 시작
1. 생성된 볼륨을 선택 (체크박스 클릭)
2. **작업(Actions)** → **볼륨 연결(Attach Volume)** 클릭

#### 2.2 연결 설정
1. **인스턴스**: 연결할 EC2 인스턴스 선택
2. **디바이스**: `/dev/sdf` (기본값 사용)
   - Linux에서는 실제로 `/dev/xvdf`로 인식됨

> **📝 참고**: AWS는 `/dev/sd[f-p]` 형식을 권장하지만, 실제 Linux에서는 `/dev/xvd[f-p]`로 표시됩니다.

3. **볼륨 연결** 버튼 클릭

#### 2.3 연결 상태 확인
- 볼륨 상태가 `in-use`로 변경되는지 확인
- EC2 인스턴스 세부 정보에서 **스토리지** 탭 확인

### 3단계: EC2 인스턴스에서 볼륨 설정

#### 3.1 SSH로 인스턴스 접속
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

#### 3.2 연결된 볼륨 확인
```bash
# 블록 디바이스 목록 확인
lsblk

# 파일 시스템 확인
sudo file -s /dev/xvdf
```

예상 출력:
```
NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
xvda1     202:1    0   8G  0 part /
xvdf      202:80   0  10G  0 part
```

#### 3.3 파일 시스템 생성
```bash
# ext4 파일 시스템 생성
sudo mkfs -t ext4 /dev/xvdf
```

> **⚠️ 주의**: 이 명령은 볼륨의 모든 데이터를 삭제합니다. 새 볼륨에만 사용하세요.

#### 3.4 마운트 포인트 생성 및 마운트
```bash
# 마운트 포인트 디렉토리 생성
sudo mkdir /data

# 볼륨 마운트
sudo mount /dev/xvdf /data

# 마운트 확인
df -h
```

#### 3.5 영구 마운트 설정
```bash
# 백업 생성
sudo cp /etc/fstab /etc/fstab.bak

# UUID 확인
sudo blkid /dev/xvdf

# fstab에 추가 (UUID는 실제 값으로 변경)
echo 'UUID=your-uuid-here /data ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab

# 설정 테스트
sudo mount -a
```

#### 3.6 권한 설정 및 테스트
```bash
# 소유권 변경
sudo chown ec2-user:ec2-user /data

# 테스트 파일 생성
echo "Hello EBS!" > /data/test.txt
cat /data/test.txt

# 디스크 사용량 확인
du -sh /data
```

### 4단계: EBS 스냅샷 생성

#### 4.1 Console에서 스냅샷 생성
1. EC2 Console → **볼륨** 메뉴
2. 대상 볼륨 선택
3. **작업** → **스냅샷 생성** 클릭
4. 스냅샷 설정:
   - **설명**: `MyFirstEBSSnapshot - $(date)`
   - **태그**: Name = `FirstSnapshot`
5. **스냅샷 생성** 클릭

#### 4.2 스냅샷 진행 상황 확인
1. 왼쪽 메뉴에서 **스냅샷** 클릭
2. 생성 중인 스냅샷의 진행률 확인
3. 상태가 `completed`가 될 때까지 대기

### 5단계: 볼륨 크기 확장 (선택사항)

#### 5.1 볼륨 크기 수정
1. **볼륨** 메뉴에서 대상 볼륨 선택
2. **작업** → **볼륨 수정** 클릭
3. **크기**: `15 GiB`로 변경
4. **볼륨 수정** 클릭

#### 5.2 파일 시스템 확장
```bash
# 파티션 크기 확인
lsblk

# 파일 시스템 확장
sudo resize2fs /dev/xvdf

# 확장 결과 확인
df -h /data
```

### 6단계: 정리 작업

#### 6.1 볼륨 분리 (실습 완료 후)
```bash
# 마운트 해제
sudo umount /data

# fstab에서 항목 제거
sudo sed -i '/\/data/d' /etc/fstab
```

#### 6.2 Console에서 볼륨 분리
1. **볼륨** 메뉴에서 볼륨 선택
2. **작업** → **볼륨 분리** 클릭
3. **분리** 확인

#### 6.3 리소스 삭제 (선택사항)
1. **볼륨 삭제**: 더 이상 필요하지 않은 경우
2. **스냅샷 유지**: 백업 목적으로 보관

## 실습 검증

### 체크리스트
- [ ] EBS 볼륨이 성공적으로 생성되었는가?
- [ ] 볼륨이 EC2 인스턴스에 연결되었는가?
- [ ] 파일 시스템이 생성되고 마운트되었는가?
- [ ] 테스트 파일을 생성하고 읽을 수 있는가?
- [ ] 스냅샷이 성공적으로 생성되었는가?
- [ ] 볼륨 크기 확장이 정상적으로 작동하는가?

### 문제 해결

**문제 1**: 볼륨을 인스턴스에 연결할 수 없음
- **해결**: 볼륨과 인스턴스가 같은 가용 영역에 있는지 확인

**문제 2**: `/dev/xvdf`가 보이지 않음
- **해결**: `lsblk` 명령으로 실제 디바이스 이름 확인

**문제 3**: 마운트 후 재부팅하면 사라짐
- **해결**: `/etc/fstab` 설정이 올바른지 확인

**문제 4**: 권한 거부 오류
- **해결**: `sudo chown` 명령으로 소유권 변경

## 추가 학습 자료

### AWS 문서
- [Amazon EBS 사용 설명서](https://docs.aws.amazon.com/ebs/)
- [Linux 인스턴스에서 EBS 볼륨 사용](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html)

### 실무 팁
1. **성능 모니터링**: CloudWatch에서 EBS 메트릭 확인
2. **백업 자동화**: AWS Backup 서비스 활용
3. **비용 최적화**: gp2에서 gp3로 마이그레이션 고려
4. **보안**: EBS 암호화 활성화 권장

## 다음 단계

이번 실습을 통해 EBS 볼륨의 기본적인 생성, 연결, 관리 방법을 배웠습니다. 다음 Day 5에서는 VPC(Virtual Private Cloud)를 생성하고 네트워크를 구성하는 방법을 학습하겠습니다.

실습 중 궁금한 점이나 문제가 있다면 AWS 문서를 참조하거나, 실습 환경에서 다양한 설정을 시도해보세요. 직접 해보는 것이 가장 좋은 학습 방법입니다!