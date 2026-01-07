#!/usr/bin/env python3
"""
AWS EC2 Management Script
Day 3 실습: EC2 인스턴스 생성, 관리, 모니터링

이 스크립트는 다음 기능을 제공합니다:
1. EC2 인스턴스 생성
2. 보안 그룹 생성 및 관리
3. 키 페어 생성
4. 인스턴스 상태 관리 (시작, 중지, 재시작, 종료)
5. 인스턴스 모니터링
6. 태그 관리

필수 사항:
- AWS CLI 설정 완료
- 적절한 IAM 권한 설정
- boto3 라이브러리 설치
"""

import boto3
import json
import time
import sys
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError


class EC2Manager:
    """EC2 인스턴스 관리를 위한 클래스"""
    
    def __init__(self, region_name='us-east-1'):
        """
        EC2Manager 초기화
        
        Args:
            region_name (str): AWS 리전 이름 (기본값: us-east-1)
        """
        try:
            self.ec2_client = boto3.client('ec2', region_name=region_name)
            self.ec2_resource = boto3.resource('ec2', region_name=region_name)
            self.region = region_name
            print(f"✅ AWS EC2 클라이언트 초기화 완료 (리전: {region_name})")
        except NoCredentialsError:
            print("❌ AWS 자격 증명을 찾을 수 없습니다. AWS CLI를 설정해주세요.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ EC2 클라이언트 초기화 실패: {str(e)}")
            sys.exit(1)
    
    def create_key_pair(self, key_name):
        """
        새로운 키 페어 생성
        
        Args:
            key_name (str): 키 페어 이름
            
        Returns:
            dict: 키 페어 정보 (개인 키 포함)
        """
        try:
            print(f"🔑 키 페어 '{key_name}' 생성 중...")
            
            response = self.ec2_client.create_key_pair(KeyName=key_name)
            
            # 개인 키를 파일로 저장
            private_key = response['KeyMaterial']
            key_file_path = f"{key_name}.pem"
            
            with open(key_file_path, 'w') as key_file:
                key_file.write(private_key)
            
            # 파일 권한 설정 (Linux/Mac)
            import os
            os.chmod(key_file_path, 0o400)
            
            print(f"✅ 키 페어 생성 완료!")
            print(f"   - 키 이름: {key_name}")
            print(f"   - 키 ID: {response['KeyPairId']}")
            print(f"   - 개인 키 파일: {key_file_path}")
            print(f"   - 지문: {response['KeyFingerprint']}")
            
            return {
                'KeyName': key_name,
                'KeyPairId': response['KeyPairId'],
                'KeyFingerprint': response['KeyFingerprint'],
                'PrivateKeyFile': key_file_path
            }
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidKeyPair.Duplicate':
                print(f"⚠️  키 페어 '{key_name}'이 이미 존재합니다.")
                return None
            else:
                print(f"❌ 키 페어 생성 실패: {e.response['Error']['Message']}")
                return None
    
    def create_security_group(self, group_name, description, vpc_id=None):
        """
        보안 그룹 생성
        
        Args:
            group_name (str): 보안 그룹 이름
            description (str): 보안 그룹 설명
            vpc_id (str): VPC ID (선택사항, 기본 VPC 사용)
            
        Returns:
            str: 생성된 보안 그룹 ID
        """
        try:
            print(f"🛡️  보안 그룹 '{group_name}' 생성 중...")
            
            # VPC ID가 지정되지 않으면 기본 VPC 사용
            if not vpc_id:
                vpc_id = self.get_default_vpc_id()
            
            response = self.ec2_client.create_security_group(
                GroupName=group_name,
                Description=description,
                VpcId=vpc_id
            )
            
            security_group_id = response['GroupId']
            
            print(f"✅ 보안 그룹 생성 완료!")
            print(f"   - 그룹 이름: {group_name}")
            print(f"   - 그룹 ID: {security_group_id}")
            print(f"   - VPC ID: {vpc_id}")
            
            return security_group_id
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
                print(f"⚠️  보안 그룹 '{group_name}'이 이미 존재합니다.")
                # 기존 보안 그룹 ID 반환
                return self.get_security_group_id(group_name)
            else:
                print(f"❌ 보안 그룹 생성 실패: {e.response['Error']['Message']}")
                return None
    
    def add_security_group_rules(self, security_group_id, rules):
        """
        보안 그룹에 인바운드 규칙 추가
        
        Args:
            security_group_id (str): 보안 그룹 ID
            rules (list): 규칙 리스트
        """
        try:
            print(f"📋 보안 그룹 규칙 추가 중...")
            
            self.ec2_client.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=rules
            )
            
            print(f"✅ 보안 그룹 규칙 추가 완료!")
            for rule in rules:
                protocol = rule.get('IpProtocol', 'Unknown')
                from_port = rule.get('FromPort', 'N/A')
                to_port = rule.get('ToPort', 'N/A')
                print(f"   - {protocol}:{from_port}-{to_port}")
                
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidPermission.Duplicate':
                print("⚠️  일부 규칙이 이미 존재합니다.")
            else:
                print(f"❌ 보안 그룹 규칙 추가 실패: {e.response['Error']['Message']}")
    
    def launch_instance(self, ami_id, instance_type, key_name, security_group_ids, 
                       subnet_id=None, user_data=None, tags=None):
        """
        EC2 인스턴스 시작
        
        Args:
            ami_id (str): AMI ID
            instance_type (str): 인스턴스 타입 (예: t3.micro)
            key_name (str): 키 페어 이름
            security_group_ids (list): 보안 그룹 ID 리스트
            subnet_id (str): 서브넷 ID (선택사항)
            user_data (str): 사용자 데이터 스크립트 (선택사항)
            tags (dict): 태그 딕셔너리 (선택사항)
            
        Returns:
            str: 생성된 인스턴스 ID
        """
        try:
            print(f"🚀 EC2 인스턴스 시작 중...")
            print(f"   - AMI ID: {ami_id}")
            print(f"   - 인스턴스 타입: {instance_type}")
            print(f"   - 키 페어: {key_name}")
            
            launch_params = {
                'ImageId': ami_id,
                'MinCount': 1,
                'MaxCount': 1,
                'InstanceType': instance_type,
                'KeyName': key_name,
                'SecurityGroupIds': security_group_ids,
                'Monitoring': {'Enabled': True}  # 상세 모니터링 활성화
            }
            
            # 선택적 매개변수 추가
            if subnet_id:
                launch_params['SubnetId'] = subnet_id
            
            if user_data:
                launch_params['UserData'] = user_data
            
            response = self.ec2_client.run_instances(**launch_params)
            
            instance_id = response['Instances'][0]['InstanceId']
            
            # 태그 추가
            if tags:
                self.add_tags(instance_id, tags)
            
            print(f"✅ 인스턴스 시작 요청 완료!")
            print(f"   - 인스턴스 ID: {instance_id}")
            print(f"   - 상태: {response['Instances'][0]['State']['Name']}")
            
            return instance_id
            
        except ClientError as e:
            print(f"❌ 인스턴스 시작 실패: {e.response['Error']['Message']}")
            return None
    
    def get_instance_status(self, instance_id):
        """
        인스턴스 상태 조회
        
        Args:
            instance_id (str): 인스턴스 ID
            
        Returns:
            dict: 인스턴스 상태 정보
        """
        try:
            response = self.ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            
            status_info = {
                'InstanceId': instance_id,
                'State': instance['State']['Name'],
                'InstanceType': instance['InstanceType'],
                'LaunchTime': instance['LaunchTime'],
                'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                'SubnetId': instance.get('SubnetId', 'N/A'),
                'VpcId': instance.get('VpcId', 'N/A')
            }
            
            return status_info
            
        except ClientError as e:
            print(f"❌ 인스턴스 상태 조회 실패: {e.response['Error']['Message']}")
            return None
    
    def wait_for_instance_running(self, instance_id, timeout=300):
        """
        인스턴스가 실행 상태가 될 때까지 대기
        
        Args:
            instance_id (str): 인스턴스 ID
            timeout (int): 타임아웃 시간 (초)
        """
        print(f"⏳ 인스턴스 '{instance_id}' 시작 대기 중...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_instance_status(instance_id)
            if status and status['State'] == 'running':
                print(f"✅ 인스턴스가 실행 상태가 되었습니다!")
                return True
            
            print(f"   현재 상태: {status['State'] if status else 'Unknown'}")
            time.sleep(10)
        
        print(f"⏰ 타임아웃: 인스턴스가 {timeout}초 내에 시작되지 않았습니다.")
        return False
    
    def stop_instance(self, instance_id):
        """인스턴스 중지"""
        try:
            print(f"⏹️  인스턴스 '{instance_id}' 중지 중...")
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            print("✅ 인스턴스 중지 요청 완료!")
        except ClientError as e:
            print(f"❌ 인스턴스 중지 실패: {e.response['Error']['Message']}")
    
    def start_instance(self, instance_id):
        """인스턴스 시작"""
        try:
            print(f"▶️  인스턴스 '{instance_id}' 시작 중...")
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            print("✅ 인스턴스 시작 요청 완료!")
        except ClientError as e:
            print(f"❌ 인스턴스 시작 실패: {e.response['Error']['Message']}")
    
    def reboot_instance(self, instance_id):
        """인스턴스 재시작"""
        try:
            print(f"🔄 인스턴스 '{instance_id}' 재시작 중...")
            self.ec2_client.reboot_instances(InstanceIds=[instance_id])
            print("✅ 인스턴스 재시작 요청 완료!")
        except ClientError as e:
            print(f"❌ 인스턴스 재시작 실패: {e.response['Error']['Message']}")
    
    def terminate_instance(self, instance_id):
        """인스턴스 종료 (삭제)"""
        try:
            print(f"🗑️  인스턴스 '{instance_id}' 종료 중...")
            print("⚠️  주의: 이 작업은 되돌릴 수 없습니다!")
            
            confirm = input("정말로 인스턴스를 종료하시겠습니까? (yes/no): ")
            if confirm.lower() == 'yes':
                self.ec2_client.terminate_instances(InstanceIds=[instance_id])
                print("✅ 인스턴스 종료 요청 완료!")
            else:
                print("❌ 인스턴스 종료가 취소되었습니다.")
        except ClientError as e:
            print(f"❌ 인스턴스 종료 실패: {e.response['Error']['Message']}")
    
    def add_tags(self, resource_id, tags):
        """리소스에 태그 추가"""
        try:
            tag_list = [{'Key': k, 'Value': v} for k, v in tags.items()]
            self.ec2_client.create_tags(Resources=[resource_id], Tags=tag_list)
            print(f"🏷️  태그 추가 완료: {tags}")
        except ClientError as e:
            print(f"❌ 태그 추가 실패: {e.response['Error']['Message']}")
    
    def list_instances(self, filters=None):
        """인스턴스 목록 조회"""
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            response = self.ec2_client.describe_instances(**params)
            
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_info = {
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State']['Name'],
                        'LaunchTime': instance['LaunchTime'],
                        'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                        'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A')
                    }
                    
                    # 태그에서 Name 찾기
                    tags = instance.get('Tags', [])
                    name_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), 'N/A')
                    instance_info['Name'] = name_tag
                    
                    instances.append(instance_info)
            
            return instances
            
        except ClientError as e:
            print(f"❌ 인스턴스 목록 조회 실패: {e.response['Error']['Message']}")
            return []
    
    def get_instance_metrics(self, instance_id, metric_name='CPUUtilization', 
                           start_time=None, end_time=None):
        """
        CloudWatch 메트릭 조회
        
        Args:
            instance_id (str): 인스턴스 ID
            metric_name (str): 메트릭 이름
            start_time (datetime): 시작 시간
            end_time (datetime): 종료 시간
        """
        try:
            cloudwatch = boto3.client('cloudwatch', region_name=self.region)
            
            if not start_time:
                start_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            if not end_time:
                end_time = datetime.utcnow()
            
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName=metric_name,
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,  # 5분 간격
                Statistics=['Average', 'Maximum']
            )
            
            return response['Datapoints']
            
        except ClientError as e:
            print(f"❌ 메트릭 조회 실패: {e.response['Error']['Message']}")
            return []
    
    def get_default_vpc_id(self):
        """기본 VPC ID 조회"""
        try:
            response = self.ec2_client.describe_vpcs(
                Filters=[{'Name': 'isDefault', 'Values': ['true']}]
            )
            if response['Vpcs']:
                return response['Vpcs'][0]['VpcId']
            return None
        except ClientError:
            return None
    
    def get_security_group_id(self, group_name):
        """보안 그룹 이름으로 ID 조회"""
        try:
            response = self.ec2_client.describe_security_groups(
                Filters=[{'Name': 'group-name', 'Values': [group_name]}]
            )
            if response['SecurityGroups']:
                return response['SecurityGroups'][0]['GroupId']
            return None
        except ClientError:
            return None
    
    def get_latest_amazon_linux_ami(self):
        """최신 Amazon Linux 2 AMI ID 조회"""
        try:
            response = self.ec2_client.describe_images(
                Owners=['amazon'],
                Filters=[
                    {'Name': 'name', 'Values': ['amzn2-ami-hvm-*']},
                    {'Name': 'architecture', 'Values': ['x86_64']},
                    {'Name': 'virtualization-type', 'Values': ['hvm']},
                    {'Name': 'state', 'Values': ['available']}
                ]
            )
            
            # 최신 AMI 선택 (생성 날짜 기준)
            if response['Images']:
                latest_ami = sorted(response['Images'], 
                                  key=lambda x: x['CreationDate'], reverse=True)[0]
                return latest_ami['ImageId']
            return None
            
        except ClientError as e:
            print(f"❌ AMI 조회 실패: {e.response['Error']['Message']}")
            return None


def create_web_server_security_group_rules():
    """웹 서버용 보안 그룹 규칙 생성"""
    return [
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'HTTP access from anywhere'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 443,
            'ToPort': 443,
            'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'HTTPS access from anywhere'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'SSH access (제한 권장)'}]
        }
    ]


def create_web_server_user_data():
    """웹 서버 설치를 위한 사용자 데이터 스크립트"""
    return """#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# 간단한 웹 페이지 생성
cat > /var/www/html/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>AWS EC2 웹 서버</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background-color: #232f3e; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .info { background-color: #d4edda; padding: 15px; margin: 10px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 EC2 웹 서버 성공적으로 실행 중!</h1>
        </div>
        <div class="content">
            <div class="info">
                <h3>서버 정보</h3>
                <p><strong>인스턴스 ID:</strong> $(curl -s http://169.254.169.254/latest/meta-data/instance-id)</p>
                <p><strong>가용 영역:</strong> $(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)</p>
                <p><strong>인스턴스 타입:</strong> $(curl -s http://169.254.169.254/latest/meta-data/instance-type)</p>
                <p><strong>퍼블릭 IP:</strong> $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)</p>
                <p><strong>프라이빗 IP:</strong> $(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)</p>
            </div>
            <h3>축하합니다!</h3>
            <p>AWS EC2 인스턴스에서 웹 서버가 성공적으로 실행되고 있습니다.</p>
            <p>이 페이지는 인스턴스 시작 시 자동으로 설치된 Apache 웹 서버에서 제공됩니다.</p>
        </div>
    </div>
</body>
</html>
EOF

# 시스템 정보를 실제 값으로 업데이트
sed -i "s/\$(curl -s http:\/\/169.254.169.254\/latest\/meta-data\/instance-id)/$(curl -s http://169.254.169.254/latest/meta-data/instance-id)/g" /var/www/html/index.html
sed -i "s/\$(curl -s http:\/\/169.254.169.254\/latest\/meta-data\/placement\/availability-zone)/$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)/g" /var/www/html/index.html
sed -i "s/\$(curl -s http:\/\/169.254.169.254\/latest\/meta-data\/instance-type)/$(curl -s http://169.254.169.254/latest/meta-data/instance-type)/g" /var/www/html/index.html
sed -i "s/\$(curl -s http:\/\/169.254.169.254\/latest\/meta-data\/public-ipv4)/$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/g" /var/www/html/index.html
sed -i "s/\$(curl -s http:\/\/169.254.169.254\/latest\/meta-data\/local-ipv4)/$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)/g" /var/www/html/index.html
"""


def main():
    """메인 실습 함수"""
    print("=" * 60)
    print("🚀 AWS EC2 관리 실습 시작!")
    print("=" * 60)
    
    # EC2Manager 초기화
    ec2_manager = EC2Manager()
    
    # 실습 설정
    key_name = "day3-lab-key"
    security_group_name = "day3-web-server-sg"
    instance_name = "Day3-Web-Server"
    
    try:
        # 1. 키 페어 생성
        print("\n📋 1단계: 키 페어 생성")
        key_info = ec2_manager.create_key_pair(key_name)
        
        # 2. 보안 그룹 생성
        print("\n📋 2단계: 보안 그룹 생성")
        security_group_id = ec2_manager.create_security_group(
            security_group_name,
            "Day 3 Lab - Web Server Security Group"
        )
        
        if security_group_id:
            # 보안 그룹 규칙 추가
            rules = create_web_server_security_group_rules()
            ec2_manager.add_security_group_rules(security_group_id, rules)
        
        # 3. 최신 Amazon Linux AMI 조회
        print("\n📋 3단계: AMI 조회")
        ami_id = ec2_manager.get_latest_amazon_linux_ami()
        if ami_id:
            print(f"✅ 최신 Amazon Linux AMI: {ami_id}")
        else:
            print("❌ AMI를 찾을 수 없습니다.")
            return
        
        # 4. EC2 인스턴스 시작
        print("\n📋 4단계: EC2 인스턴스 시작")
        user_data = create_web_server_user_data()
        tags = {
            'Name': instance_name,
            'Environment': 'Lab',
            'Project': 'AWS-SAA-Study',
            'Day': '3'
        }
        
        instance_id = ec2_manager.launch_instance(
            ami_id=ami_id,
            instance_type='t3.micro',  # 프리 티어 사용
            key_name=key_name,
            security_group_ids=[security_group_id],
            user_data=user_data,
            tags=tags
        )
        
        if not instance_id:
            print("❌ 인스턴스 시작에 실패했습니다.")
            return
        
        # 5. 인스턴스 시작 대기
        print("\n📋 5단계: 인스턴스 시작 대기")
        if ec2_manager.wait_for_instance_running(instance_id):
            # 인스턴스 정보 출력
            status = ec2_manager.get_instance_status(instance_id)
            if status:
                print("\n🎉 인스턴스 정보:")
                print(f"   - 인스턴스 ID: {status['InstanceId']}")
                print(f"   - 상태: {status['State']}")
                print(f"   - 인스턴스 타입: {status['InstanceType']}")
                print(f"   - 퍼블릭 IP: {status['PublicIpAddress']}")
                print(f"   - 프라이빗 IP: {status['PrivateIpAddress']}")
                
                if status['PublicIpAddress'] != 'N/A':
                    print(f"\n🌐 웹 서버 접속:")
                    print(f"   http://{status['PublicIpAddress']}")
                    print(f"\n🔑 SSH 접속:")
                    print(f"   ssh -i {key_name}.pem ec2-user@{status['PublicIpAddress']}")
        
        # 6. 인스턴스 관리 메뉴
        print("\n📋 6단계: 인스턴스 관리")
        while True:
            print("\n" + "=" * 40)
            print("인스턴스 관리 메뉴:")
            print("1. 인스턴스 상태 확인")
            print("2. 인스턴스 목록 보기")
            print("3. 인스턴스 중지")
            print("4. 인스턴스 시작")
            print("5. 인스턴스 재시작")
            print("6. CPU 사용률 확인")
            print("7. 인스턴스 종료 (삭제)")
            print("0. 종료")
            print("=" * 40)
            
            choice = input("선택하세요 (0-7): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                status = ec2_manager.get_instance_status(instance_id)
                if status:
                    print(f"\n📊 인스턴스 상태:")
                    for key, value in status.items():
                        print(f"   {key}: {value}")
            elif choice == '2':
                instances = ec2_manager.list_instances()
                print(f"\n📋 인스턴스 목록 ({len(instances)}개):")
                for inst in instances:
                    print(f"   {inst['Name']} ({inst['InstanceId']}) - {inst['State']}")
            elif choice == '3':
                ec2_manager.stop_instance(instance_id)
            elif choice == '4':
                ec2_manager.start_instance(instance_id)
            elif choice == '5':
                ec2_manager.reboot_instance(instance_id)
            elif choice == '6':
                print("📈 CPU 사용률 조회 중...")
                metrics = ec2_manager.get_instance_metrics(instance_id)
                if metrics:
                    print(f"   최근 CPU 사용률 데이터 포인트: {len(metrics)}개")
                    for metric in metrics[-5:]:  # 최근 5개만 표시
                        timestamp = metric['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                        avg_cpu = metric['Average']
                        max_cpu = metric['Maximum']
                        print(f"   {timestamp}: 평균 {avg_cpu:.2f}%, 최대 {max_cpu:.2f}%")
                else:
                    print("   메트릭 데이터가 없습니다. (인스턴스가 최근에 시작되었을 수 있습니다)")
            elif choice == '7':
                ec2_manager.terminate_instance(instance_id)
                break
            else:
                print("❌ 잘못된 선택입니다.")
        
        print("\n🎉 실습 완료!")
        print("💡 팁: 비용 절약을 위해 사용하지 않는 인스턴스는 중지하거나 종료하세요.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류 발생: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🏁 AWS EC2 관리 실습 종료")
    print("=" * 60)


if __name__ == "__main__":
    main()