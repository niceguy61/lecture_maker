#!/usr/bin/env python3
"""
AWS IAM 관리 실습 스크립트
Day 2: IAM (Identity and Access Management) 실습

이 스크립트는 AWS IAM의 핵심 기능들을 실습해볼 수 있도록 구성되었습니다.
- 사용자, 그룹, 역할, 정책 생성 및 관리
- IAM 보안 모범 사례 적용
- 실제 시나리오 기반 실습

주의: 이 스크립트는 학습 목적으로 작성되었으며, 실제 운영 환경에서는 
더 엄격한 보안 검토가 필요합니다.
"""

import boto3
import json
import time
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Dict, List, Optional


class IAMManager:
    """AWS IAM 리소스를 관리하는 클래스"""
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        IAM 클라이언트 초기화
        
        Args:
            region_name: AWS 리전 (IAM은 글로벌 서비스이지만 클라이언트 설정용)
        """
        try:
            self.iam_client = boto3.client('iam', region_name=region_name)
            self.sts_client = boto3.client('sts', region_name=region_name)
            print("✅ AWS IAM 클라이언트가 성공적으로 초기화되었습니다.")
        except NoCredentialsError:
            print("❌ AWS 자격 증명을 찾을 수 없습니다. AWS CLI 설정을 확인해주세요.")
            raise
        except Exception as e:
            print(f"❌ IAM 클라이언트 초기화 실패: {e}")
            raise
    
    def get_current_user_info(self) -> Dict:
        """현재 사용자 정보 조회"""
        try:
            # 현재 사용자 정보 가져오기
            user_info = self.sts_client.get_caller_identity()
            print(f"🔍 현재 사용자 정보:")
            print(f"   - Account ID: {user_info['Account']}")
            print(f"   - User ARN: {user_info['Arn']}")
            print(f"   - User ID: {user_info['UserId']}")
            return user_info
        except ClientError as e:
            print(f"❌ 사용자 정보 조회 실패: {e}")
            return {}
    
    def create_user(self, username: str, path: str = '/') -> bool:
        """
        IAM 사용자 생성
        
        Args:
            username: 생성할 사용자명
            path: 사용자 경로 (조직 구조 반영)
        
        Returns:
            bool: 생성 성공 여부
        """
        try:
            response = self.iam_client.create_user(
                UserName=username,
                Path=path
            )
            print(f"✅ 사용자 '{username}' 생성 완료")
            print(f"   - ARN: {response['User']['Arn']}")
            print(f"   - 생성일: {response['User']['CreateDate']}")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print(f"⚠️  사용자 '{username}'이 이미 존재합니다.")
            else:
                print(f"❌ 사용자 생성 실패: {e}")
            return False
    
    def create_group(self, group_name: str, path: str = '/') -> bool:
        """
        IAM 그룹 생성
        
        Args:
            group_name: 생성할 그룹명
            path: 그룹 경로
        
        Returns:
            bool: 생성 성공 여부
        """
        try:
            response = self.iam_client.create_group(
                GroupName=group_name,
                Path=path
            )
            print(f"✅ 그룹 '{group_name}' 생성 완료")
            print(f"   - ARN: {response['Group']['Arn']}")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print(f"⚠️  그룹 '{group_name}'이 이미 존재합니다.")
            else:
                print(f"❌ 그룹 생성 실패: {e}")
            return False
    
    def create_policy(self, policy_name: str, policy_document: Dict, 
                     description: str = "") -> Optional[str]:
        """
        IAM 정책 생성
        
        Args:
            policy_name: 정책명
            policy_document: 정책 문서 (딕셔너리 형태)
            description: 정책 설명
        
        Returns:
            str: 생성된 정책의 ARN (실패시 None)
        """
        try:
            response = self.iam_client.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document, indent=2),
                Description=description
            )
            policy_arn = response['Policy']['Arn']
            print(f"✅ 정책 '{policy_name}' 생성 완료")
            print(f"   - ARN: {policy_arn}")
            return policy_arn
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print(f"⚠️  정책 '{policy_name}'이 이미 존재합니다.")
                # 기존 정책 ARN 반환
                account_id = self.sts_client.get_caller_identity()['Account']
                return f"arn:aws:iam::{account_id}:policy/{policy_name}"
            else:
                print(f"❌ 정책 생성 실패: {e}")
                return None
    
    def create_role(self, role_name: str, trust_policy: Dict, 
                   description: str = "") -> Optional[str]:
        """
        IAM 역할 생성
        
        Args:
            role_name: 역할명
            trust_policy: 신뢰 정책 (어떤 개체가 이 역할을 사용할 수 있는지)
            description: 역할 설명
        
        Returns:
            str: 생성된 역할의 ARN (실패시 None)
        """
        try:
            response = self.iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy, indent=2),
                Description=description
            )
            role_arn = response['Role']['Arn']
            print(f"✅ 역할 '{role_name}' 생성 완료")
            print(f"   - ARN: {role_arn}")
            return role_arn
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print(f"⚠️  역할 '{role_name}'이 이미 존재합니다.")
            else:
                print(f"❌ 역할 생성 실패: {e}")
            return None
    
    def attach_policy_to_user(self, username: str, policy_arn: str) -> bool:
        """사용자에게 정책 연결"""
        try:
            self.iam_client.attach_user_policy(
                UserName=username,
                PolicyArn=policy_arn
            )
            print(f"✅ 사용자 '{username}'에게 정책 연결 완료")
            return True
        except ClientError as e:
            print(f"❌ 정책 연결 실패: {e}")
            return False
    
    def attach_policy_to_group(self, group_name: str, policy_arn: str) -> bool:
        """그룹에 정책 연결"""
        try:
            self.iam_client.attach_group_policy(
                GroupName=group_name,
                PolicyArn=policy_arn
            )
            print(f"✅ 그룹 '{group_name}'에 정책 연결 완료")
            return True
        except ClientError as e:
            print(f"❌ 정책 연결 실패: {e}")
            return False
    
    def add_user_to_group(self, username: str, group_name: str) -> bool:
        """사용자를 그룹에 추가"""
        try:
            self.iam_client.add_user_to_group(
                GroupName=group_name,
                UserName=username
            )
            print(f"✅ 사용자 '{username}'를 그룹 '{group_name}'에 추가 완료")
            return True
        except ClientError as e:
            print(f"❌ 그룹 추가 실패: {e}")
            return False
    
    def list_users(self) -> List[Dict]:
        """모든 IAM 사용자 목록 조회"""
        try:
            response = self.iam_client.list_users()
            users = response['Users']
            print(f"📋 총 {len(users)}명의 사용자가 있습니다:")
            for user in users:
                print(f"   - {user['UserName']} (생성일: {user['CreateDate']})")
            return users
        except ClientError as e:
            print(f"❌ 사용자 목록 조회 실패: {e}")
            return []
    
    def cleanup_resources(self, resource_names: Dict[str, List[str]]) -> None:
        """실습용 리소스 정리"""
        print("\n🧹 실습 리소스 정리 중...")
        
        # 사용자 정리
        for username in resource_names.get('users', []):
            try:
                # 사용자에 연결된 정책 분리
                attached_policies = self.iam_client.list_attached_user_policies(
                    UserName=username
                )
                for policy in attached_policies['AttachedPolicies']:
                    self.iam_client.detach_user_policy(
                        UserName=username,
                        PolicyArn=policy['PolicyArn']
                    )
                
                # 사용자 삭제
                self.iam_client.delete_user(UserName=username)
                print(f"✅ 사용자 '{username}' 삭제 완료")
            except ClientError as e:
                print(f"⚠️  사용자 '{username}' 삭제 실패: {e}")
        
        # 그룹 정리
        for group_name in resource_names.get('groups', []):
            try:
                # 그룹에 연결된 정책 분리
                attached_policies = self.iam_client.list_attached_group_policies(
                    GroupName=group_name
                )
                for policy in attached_policies['AttachedPolicies']:
                    self.iam_client.detach_group_policy(
                        GroupName=group_name,
                        PolicyArn=policy['PolicyArn']
                    )
                
                # 그룹 삭제
                self.iam_client.delete_group(GroupName=group_name)
                print(f"✅ 그룹 '{group_name}' 삭제 완료")
            except ClientError as e:
                print(f"⚠️  그룹 '{group_name}' 삭제 실패: {e}")
        
        # 정책 정리
        for policy_name in resource_names.get('policies', []):
            try:
                account_id = self.sts_client.get_caller_identity()['Account']
                policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
                self.iam_client.delete_policy(PolicyArn=policy_arn)
                print(f"✅ 정책 '{policy_name}' 삭제 완료")
            except ClientError as e:
                print(f"⚠️  정책 '{policy_name}' 삭제 실패: {e}")


def create_sample_policies() -> Dict[str, Dict]:
    """실습용 샘플 정책들 생성"""
    
    # S3 읽기 전용 정책
    s3_readonly_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::*",
                    "arn:aws:s3:::*/*"
                ]
            }
        ]
    }
    
    # EC2 읽기 전용 정책
    ec2_readonly_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:Describe*",
                    "ec2:List*"
                ],
                "Resource": "*"
            }
        ]
    }
    
    # 개발자용 정책 (EC2 + S3 제한적 권한)
    developer_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:RunInstances",
                    "ec2:TerminateInstances",
                    "ec2:Describe*"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "ec2:InstanceType": ["t2.micro", "t3.micro"]
                    }
                }
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject"
                ],
                "Resource": "arn:aws:s3:::dev-*/*"
            }
        ]
    }
    
    return {
        "S3ReadOnlyPolicy": s3_readonly_policy,
        "EC2ReadOnlyPolicy": ec2_readonly_policy,
        "DeveloperPolicy": developer_policy
    }


def create_ec2_trust_policy() -> Dict:
    """EC2 서비스가 사용할 수 있는 신뢰 정책"""
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }


def main():
    """메인 실습 함수"""
    print("🚀 AWS IAM 실습을 시작합니다!")
    print("=" * 50)
    
    # IAM 매니저 초기화
    try:
        iam_manager = IAMManager()
    except Exception:
        print("IAM 매니저 초기화에 실패했습니다. 프로그램을 종료합니다.")
        return
    
    # 현재 사용자 정보 확인
    print("\n1️⃣ 현재 사용자 정보 확인")
    print("-" * 30)
    current_user = iam_manager.get_current_user_info()
    
    # 실습용 리소스 이름 정의
    resource_names = {
        'users': ['study-developer', 'study-admin'],
        'groups': ['StudyDevelopers', 'StudyAdmins'],
        'policies': ['StudyS3ReadOnly', 'StudyEC2ReadOnly', 'StudyDeveloper'],
        'roles': ['StudyEC2Role']
    }
    
    try:
        # 2. 사용자 생성
        print("\n2️⃣ IAM 사용자 생성")
        print("-" * 30)
        iam_manager.create_user('study-developer', '/study/')
        iam_manager.create_user('study-admin', '/study/')
        
        # 3. 그룹 생성
        print("\n3️⃣ IAM 그룹 생성")
        print("-" * 30)
        iam_manager.create_group('StudyDevelopers', '/study/')
        iam_manager.create_group('StudyAdmins', '/study/')
        
        # 4. 정책 생성
        print("\n4️⃣ IAM 정책 생성")
        print("-" * 30)
        policies = create_sample_policies()
        policy_arns = {}
        
        for policy_name, policy_doc in policies.items():
            arn = iam_manager.create_policy(
                f"Study{policy_name}",
                policy_doc,
                f"실습용 {policy_name} 정책"
            )
            if arn:
                policy_arns[policy_name] = arn
        
        # 5. 역할 생성
        print("\n5️⃣ IAM 역할 생성")
        print("-" * 30)
        trust_policy = create_ec2_trust_policy()
        role_arn = iam_manager.create_role(
            'StudyEC2Role',
            trust_policy,
            'EC2 인스턴스가 사용할 실습용 역할'
        )
        
        # 6. 정책 연결
        print("\n6️⃣ 정책 연결")
        print("-" * 30)
        
        # 그룹에 정책 연결
        if 'S3ReadOnlyPolicy' in policy_arns:
            iam_manager.attach_policy_to_group('StudyDevelopers', policy_arns['S3ReadOnlyPolicy'])
        if 'DeveloperPolicy' in policy_arns:
            iam_manager.attach_policy_to_group('StudyDevelopers', policy_arns['DeveloperPolicy'])
        
        # 사용자를 그룹에 추가
        iam_manager.add_user_to_group('study-developer', 'StudyDevelopers')
        iam_manager.add_user_to_group('study-admin', 'StudyAdmins')
        
        # 7. 생성된 리소스 확인
        print("\n7️⃣ 생성된 리소스 확인")
        print("-" * 30)
        iam_manager.list_users()
        
        print("\n✅ IAM 실습이 완료되었습니다!")
        print("\n📚 학습 포인트:")
        print("   - IAM 사용자, 그룹, 역할, 정책의 생성 방법")
        print("   - 정책을 통한 권한 제어")
        print("   - 그룹을 통한 효율적인 권한 관리")
        print("   - EC2 서비스 역할의 신뢰 정책")
        
        # 정리 여부 확인
        cleanup = input("\n🧹 실습용 리소스를 정리하시겠습니까? (y/N): ").lower()
        if cleanup == 'y':
            iam_manager.cleanup_resources(resource_names)
            print("✅ 리소스 정리가 완료되었습니다.")
        else:
            print("⚠️  리소스가 유지됩니다. 나중에 수동으로 정리해주세요.")
            print("   정리할 리소스:")
            for resource_type, names in resource_names.items():
                print(f"   - {resource_type}: {', '.join(names)}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 실습이 중단되었습니다.")
        cleanup = input("🧹 지금까지 생성된 리소스를 정리하시겠습니까? (y/N): ").lower()
        if cleanup == 'y':
            iam_manager.cleanup_resources(resource_names)
    
    except Exception as e:
        print(f"\n❌ 실습 중 오류가 발생했습니다: {e}")
        print("🧹 리소스 정리를 시도합니다...")
        iam_manager.cleanup_resources(resource_names)


if __name__ == "__main__":
    main()