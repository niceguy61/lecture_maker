#!/usr/bin/env python3
"""
AWS 계정 설정 및 기본 구성 실습
Day 1 Hands-on Lab: AWS Account Setup and Basic Configuration

이 스크립트는 AWS 계정 설정 후 기본적인 구성을 확인하고 
초기 보안 설정을 도와주는 실습용 도구입니다.

Prerequisites:
- AWS 계정 생성 완료
- AWS CLI 설치
- Python 3.7+ 설치
"""

import boto3
import json
import sys
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError


class AWSAccountSetupLab:
    """AWS 계정 설정 실습 클래스"""
    
    def __init__(self):
        """초기화 및 AWS 클라이언트 설정"""
        try:
            # AWS 세션 생성
            self.session = boto3.Session()
            
            # 기본 클라이언트들 초기화
            self.sts_client = self.session.client('sts')
            self.iam_client = self.session.client('iam')
            self.ec2_client = self.session.client('ec2')
            
            print("✅ AWS 클라이언트 초기화 완료")
            
        except NoCredentialsError:
            print("❌ AWS 자격 증명이 설정되지 않았습니다.")
            print("AWS CLI를 설정하거나 환경 변수를 확인해주세요.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 초기화 오류: {str(e)}")
            sys.exit(1)
    
    def check_account_info(self):
        """현재 AWS 계정 정보 확인"""
        print("\n" + "="*50)
        print("1. AWS 계정 정보 확인")
        print("="*50)
        
        try:
            # 현재 계정 정보 가져오기
            identity = self.sts_client.get_caller_identity()
            
            account_id = identity['Account']
            user_arn = identity['Arn']
            user_id = identity['UserId']
            
            print(f"📋 계정 ID: {account_id}")
            print(f"👤 사용자 ARN: {user_arn}")
            print(f"🆔 사용자 ID: {user_id}")
            
            # 현재 리전 확인
            current_region = self.session.region_name
            print(f"🌍 현재 리전: {current_region}")
            
            return {
                'account_id': account_id,
                'user_arn': user_arn,
                'user_id': user_id,
                'region': current_region
            }
            
        except ClientError as e:
            print(f"❌ 계정 정보 조회 실패: {e}")
            return None
    
    def check_available_regions(self):
        """사용 가능한 AWS 리전 목록 확인"""
        print("\n" + "="*50)
        print("2. 사용 가능한 AWS 리전 확인")
        print("="*50)
        
        try:
            # 모든 리전 정보 가져오기
            regions = self.ec2_client.describe_regions()
            
            print(f"📍 총 {len(regions['Regions'])}개 리전 사용 가능:")
            
            for region in regions['Regions']:
                region_name = region['RegionName']
                endpoint = region['Endpoint']
                print(f"  • {region_name}: {endpoint}")
            
            return regions['Regions']
            
        except ClientError as e:
            print(f"❌ 리전 정보 조회 실패: {e}")
            return []
    
    def check_availability_zones(self):
        """현재 리전의 가용 영역 확인"""
        print("\n" + "="*50)
        print("3. 현재 리전의 가용 영역 확인")
        print("="*50)
        
        try:
            # 가용 영역 정보 가져오기
            azs = self.ec2_client.describe_availability_zones()
            
            current_region = self.session.region_name
            print(f"🏢 {current_region} 리전의 가용 영역:")
            
            for az in azs['AvailabilityZones']:
                az_name = az['ZoneName']
                az_id = az['ZoneId']
                state = az['State']
                zone_type = az.get('ZoneType', 'availability-zone')
                
                status_emoji = "✅" if state == "available" else "❌"
                print(f"  {status_emoji} {az_name} (ID: {az_id}, Type: {zone_type})")
            
            return azs['AvailabilityZones']
            
        except ClientError as e:
            print(f"❌ 가용 영역 정보 조회 실패: {e}")
            return []
    
    def check_iam_user_status(self):
        """IAM 사용자 상태 및 권한 확인"""
        print("\n" + "="*50)
        print("4. IAM 사용자 상태 확인")
        print("="*50)
        
        try:
            # 현재 사용자 정보 확인
            identity = self.sts_client.get_caller_identity()
            
            if 'user' in identity['Arn'].lower():
                # IAM 사용자인 경우
                user_name = identity['Arn'].split('/')[-1]
                print(f"👤 IAM 사용자: {user_name}")
                
                # 사용자 세부 정보 가져오기
                try:
                    user_info = self.iam_client.get_user(UserName=user_name)
                    user = user_info['User']
                    
                    print(f"📅 생성일: {user['CreateDate']}")
                    print(f"🔑 사용자 ID: {user['UserId']}")
                    
                    # 사용자 정책 확인
                    self._check_user_policies(user_name)
                    
                except ClientError as e:
                    if e.response['Error']['Code'] == 'AccessDenied':
                        print("⚠️  IAM 사용자 정보 조회 권한이 없습니다.")
                    else:
                        print(f"❌ 사용자 정보 조회 실패: {e}")
            
            elif 'root' in identity['Arn'].lower():
                print("🔴 루트 사용자로 로그인되어 있습니다.")
                print("⚠️  보안을 위해 IAM 사용자 생성을 권장합니다.")
            
            else:
                print(f"🤖 역할 또는 기타 자격 증명: {identity['Arn']}")
                
        except ClientError as e:
            print(f"❌ IAM 상태 확인 실패: {e}")
    
    def _check_user_policies(self, user_name):
        """사용자 정책 확인 (내부 메서드)"""
        try:
            # 직접 연결된 정책 확인
            attached_policies = self.iam_client.list_attached_user_policies(
                UserName=user_name
            )
            
            if attached_policies['AttachedPolicies']:
                print("📋 연결된 관리형 정책:")
                for policy in attached_policies['AttachedPolicies']:
                    print(f"  • {policy['PolicyName']} ({policy['PolicyArn']})")
            
            # 인라인 정책 확인
            inline_policies = self.iam_client.list_user_policies(
                UserName=user_name
            )
            
            if inline_policies['PolicyNames']:
                print("📄 인라인 정책:")
                for policy_name in inline_policies['PolicyNames']:
                    print(f"  • {policy_name}")
            
            # 그룹 멤버십 확인
            groups = self.iam_client.get_groups_for_user(UserName=user_name)
            
            if groups['Groups']:
                print("👥 소속 그룹:")
                for group in groups['Groups']:
                    print(f"  • {group['GroupName']}")
            
        except ClientError as e:
            print(f"⚠️  정책 정보 조회 권한이 제한되어 있습니다: {e}")
    
    def check_billing_preferences(self):
        """결제 및 비용 관리 설정 확인"""
        print("\n" + "="*50)
        print("5. 결제 및 비용 관리 확인")
        print("="*50)
        
        try:
            # Cost Explorer 클라이언트 (us-east-1에서만 사용 가능)
            ce_client = boto3.client('ce', region_name='us-east-1')
            
            # 현재 월 비용 확인 (간단한 예시)
            from datetime import datetime, timedelta
            
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            cost_response = ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost']
            )
            
            if cost_response['ResultsByTime']:
                amount = cost_response['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
                currency = cost_response['ResultsByTime'][0]['Total']['BlendedCost']['Unit']
                print(f"💰 지난 30일 예상 비용: {amount} {currency}")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                print("⚠️  결제 정보 조회 권한이 없습니다.")
                print("💡 루트 계정에서 IAM 사용자에게 결제 권한을 부여해야 합니다.")
            else:
                print(f"❌ 결제 정보 조회 실패: {e}")
        except Exception as e:
            print(f"⚠️  결제 정보 확인 중 오류: {e}")
    
    def security_recommendations(self):
        """보안 권장사항 출력"""
        print("\n" + "="*50)
        print("6. 보안 권장사항")
        print("="*50)
        
        recommendations = [
            "🔐 루트 계정에 MFA(다중 인증) 활성화",
            "👤 일상적인 작업을 위한 IAM 사용자 생성",
            "🔑 IAM 사용자에게 최소 권한 원칙 적용",
            "📱 IAM 사용자에게도 MFA 활성화",
            "🔄 액세스 키 정기적 교체",
            "📊 CloudTrail 활성화로 API 호출 로깅",
            "💰 결제 알림 설정으로 예상치 못한 비용 방지",
            "🏷️ 리소스 태깅 정책 수립",
            "🔒 보안 그룹 규칙 최소화",
            "📈 CloudWatch 모니터링 설정"
        ]
        
        print("다음 보안 권장사항을 검토하고 적용해주세요:")
        for i, recommendation in enumerate(recommendations, 1):
            print(f"{i:2d}. {recommendation}")
    
    def generate_setup_report(self, account_info):
        """설정 보고서 생성"""
        print("\n" + "="*50)
        print("7. 설정 보고서 생성")
        print("="*50)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = {
            "timestamp": timestamp,
            "account_info": account_info,
            "setup_status": "completed",
            "next_steps": [
                "IAM 사용자 생성 및 MFA 설정",
                "결제 알림 설정",
                "CloudTrail 활성화",
                "Day 2 학습 진행 (IAM 심화)"
            ]
        }
        
        # 보고서를 JSON 파일로 저장
        report_filename = f"aws_setup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"📄 설정 보고서가 생성되었습니다: {report_filename}")
            
        except Exception as e:
            print(f"❌ 보고서 생성 실패: {e}")
        
        return report
    
    def run_complete_setup_check(self):
        """전체 설정 확인 실행"""
        print("🚀 AWS 계정 설정 확인을 시작합니다...")
        print("이 과정은 몇 분 정도 소요될 수 있습니다.")
        
        # 1. 계정 정보 확인
        account_info = self.check_account_info()
        
        if not account_info:
            print("❌ 계정 정보를 확인할 수 없어 실습을 중단합니다.")
            return
        
        # 2. 리전 정보 확인
        self.check_available_regions()
        
        # 3. 가용 영역 확인
        self.check_availability_zones()
        
        # 4. IAM 상태 확인
        self.check_iam_user_status()
        
        # 5. 결제 정보 확인
        self.check_billing_preferences()
        
        # 6. 보안 권장사항
        self.security_recommendations()
        
        # 7. 보고서 생성
        self.generate_setup_report(account_info)
        
        print("\n" + "="*50)
        print("✅ AWS 계정 설정 확인이 완료되었습니다!")
        print("="*50)
        print("다음 단계: Day 2 - IAM (Identity and Access Management) 학습")


def main():
    """메인 실행 함수"""
    print("AWS SAA-C03 Study Materials")
    print("Day 1 Hands-on Lab: AWS Account Setup")
    print("="*50)
    
    try:
        # AWS 계정 설정 실습 인스턴스 생성
        lab = AWSAccountSetupLab()
        
        # 전체 설정 확인 실행
        lab.run_complete_setup_check()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 실습이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")
        print("문제가 지속되면 AWS 자격 증명 설정을 확인해주세요.")


if __name__ == "__main__":
    main()