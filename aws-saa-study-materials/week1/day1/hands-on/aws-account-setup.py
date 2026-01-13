#!/usr/bin/env python3
"""
AWS Account Setup Automation Script
Day 1 실습용 - AWS 계정 초기 설정 자동화

이 스크립트는 AWS 계정 생성 후 초기 설정을 자동화합니다.
주의: 루트 계정 액세스 키는 사용하지 않으며, IAM 사용자 생성 후 사용하세요.
"""

import boto3
import json
import sys
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError

class AWSAccountSetup:
    def __init__(self):
        """AWS 계정 설정 클래스 초기화"""
        self.session = None
        self.region = 'ap-northeast-2'  # 서울 리전
        
    def check_credentials(self):
        """AWS 자격 증명 확인"""
        try:
            # STS를 사용하여 현재 자격 증명 확인
            sts = boto3.client('sts', region_name=self.region)
            identity = sts.get_caller_identity()
            
            print("✅ AWS 자격 증명 확인 완료")
            print(f"   계정 ID: {identity['Account']}")
            print(f"   사용자 ARN: {identity['Arn']}")
            print(f"   사용자 ID: {identity['UserId']}")
            return True
            
        except NoCredentialsError:
            print("❌ AWS 자격 증명이 설정되지 않았습니다.")
            print("   AWS CLI 설정 또는 환경 변수를 확인하세요.")
            return False
        except Exception as e:
            print(f"❌ 자격 증명 확인 중 오류 발생: {str(e)}")
            return False
    
    def check_region_availability(self):
        """선택한 리전의 서비스 가용성 확인"""
        try:
            ec2 = boto3.client('ec2', region_name=self.region)
            regions = ec2.describe_regions()
            
            available_regions = [r['RegionName'] for r in regions['Regions']]
            
            if self.region in available_regions:
                print(f"✅ 리전 {self.region} 사용 가능")
                return True
            else:
                print(f"❌ 리전 {self.region} 사용 불가")
                print(f"   사용 가능한 리전: {', '.join(available_regions[:5])}...")
                return False
                
        except Exception as e:
            print(f"❌ 리전 확인 중 오류 발생: {str(e)}")
            return False
    
    def setup_billing_alerts(self, threshold_amount=5.0):
        """결제 알림 설정 (CloudWatch 경보)"""
        try:
            # CloudWatch는 결제 메트릭을 위해 us-east-1 리전 사용
            cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
            sns = boto3.client('sns', region_name='us-east-1')
            
            # SNS 토픽 생성
            topic_name = 'billing-alerts'
            try:
                topic_response = sns.create_topic(Name=topic_name)
                topic_arn = topic_response['TopicArn']
                print(f"✅ SNS 토픽 생성 완료: {topic_arn}")
            except ClientError as e:
                if e.response['Error']['Code'] == 'TopicAlreadyExists':
                    # 기존 토픽 ARN 가져오기
                    topics = sns.list_topics()
                    topic_arn = None
                    for topic in topics['Topics']:
                        if topic_name in topic['TopicArn']:
                            topic_arn = topic['TopicArn']
                            break
                    print(f"✅ 기존 SNS 토픽 사용: {topic_arn}")
                else:
                    raise e
            
            # CloudWatch 경보 생성
            alarm_name = 'BillingAlert'
            cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=1,
                MetricName='EstimatedCharges',
                Namespace='AWS/Billing',
                Period=86400,  # 24시간
                Statistic='Maximum',
                Threshold=threshold_amount,
                ActionsEnabled=True,
                AlarmActions=[topic_arn],
                AlarmDescription=f'Billing alert when charges exceed ${threshold_amount}',
                Dimensions=[
                    {
                        'Name': 'Currency',
                        'Value': 'USD'
                    },
                ],
                Unit='None'
            )
            
            print(f"✅ 결제 알림 설정 완료 (임계값: ${threshold_amount})")
            print(f"   경보 이름: {alarm_name}")
            print(f"   SNS 토픽: {topic_arn}")
            
            return True
            
        except Exception as e:
            print(f"❌ 결제 알림 설정 중 오류 발생: {str(e)}")
            print("   수동으로 AWS Console에서 설정하세요.")
            return False
    
    def check_free_tier_services(self):
        """Free Tier 서비스 가용성 확인"""
        try:
            print("\n📊 Free Tier 주요 서비스 확인:")
            
            # EC2 인스턴스 타입 확인
            ec2 = boto3.client('ec2', region_name=self.region)
            instance_types = ec2.describe_instance_types(
                InstanceTypes=['t2.micro', 't3.micro']
            )
            
            for instance_type in instance_types['InstanceTypes']:
                print(f"   ✅ {instance_type['InstanceType']}: "
                      f"{instance_type['VCpuInfo']['DefaultVCpus']} vCPU, "
                      f"{instance_type['MemoryInfo']['SizeInMiB']} MiB RAM")
            
            # S3 서비스 확인
            s3 = boto3.client('s3', region_name=self.region)
            print("   ✅ S3: 5GB 스토리지, 20,000 GET 요청, 2,000 PUT 요청")
            
            # RDS 인스턴스 클래스 확인
            rds = boto3.client('rds', region_name=self.region)
            print("   ✅ RDS: db.t2.micro 또는 db.t3.micro (750시간/월)")
            
            # Lambda 서비스 확인
            lambda_client = boto3.client('lambda', region_name=self.region)
            print("   ✅ Lambda: 1백만 요청/월, 400,000 GB-초")
            
            return True
            
        except Exception as e:
            print(f"❌ Free Tier 서비스 확인 중 오류 발생: {str(e)}")
            return False
    
    def run_setup(self):
        """전체 설정 프로세스 실행"""
        print("🚀 AWS 계정 초기 설정을 시작합니다...\n")
        
        # 1. 자격 증명 확인
        if not self.check_credentials():
            print("\n❌ 설정을 중단합니다. AWS 자격 증명을 먼저 설정하세요.")
            return False
        
        # 2. 리전 가용성 확인
        if not self.check_region_availability():
            print(f"\n❌ 설정을 중단합니다. 리전 {self.region}을 사용할 수 없습니다.")
            return False
        
        # 3. Free Tier 서비스 확인
        self.check_free_tier_services()
        
        print("\n🎉 AWS 계정 초기 설정이 완료되었습니다!")
        
        return True

def main():
    """메인 함수"""
    print("=" * 60)
    print("AWS 계정 초기 설정 자동화 스크립트")
    print("Day 1 실습용 - AWS SAA-C03 학습 자료")
    print("=" * 60)
    
    # 설정 실행
    setup = AWSAccountSetup()
    success = setup.run_setup()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()